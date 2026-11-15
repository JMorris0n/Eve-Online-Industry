#!/usr/bin/env python3
"""Build the private operating profile from verified local ESI snapshots.

This tool is deliberately offline: it reads files created by sso_local.py and
never contacts EVE, refreshes tokens, or sends character data anywhere.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from readiness_report import build_readiness_report
from validate_profile import validate_profile_data

DEFAULT_REGISTRY = Path("data/private/esi/authorized-characters.json")
DEFAULT_SNAPSHOT_ROOT = Path("data/private/esi/snapshots")
DEFAULT_PROFILE = Path("local/operating-profile.json")
DEFAULT_EXAMPLE = Path("config/operating-profile.example.json")
DEFAULT_IMPORT_MANIFEST = Path("data/private/esi/profile-import-manifest.json")
DEFAULT_READINESS = Path("local/profile-readiness.json")

REQUIRED_SCOPES = {
    "esi-skills.read_skills.v1",
    "esi-skills.read_skillqueue.v1",
    "esi-characters.read_blueprints.v1",
    "esi-assets.read_assets.v1",
    "esi-industry.read_character_jobs.v1",
    "esi-search.search_structures.v1",
    "esi-universe.read_structures.v1",
}

# These are the skills that add concurrent job slots. The one-slot base
# allowance is separate from the active-skill bonuses used by ESI today.
CAPACITY_SKILLS = {
    "manufacturing": (3387, 24625),  # Mass Production, Advanced Mass Production
    "science": (3406, 24624),        # Laboratory Operation, Advanced Laboratory Operation
    "reaction": (45748, 45749),      # Mass Reactions, Advanced Mass Reactions
}
ACTIVITY_TO_POOL = {
    1: "manufacturing",
    3: "science",   # Time Efficiency Research
    4: "science",   # Material Efficiency Research
    5: "science",   # Copying
    7: "science",   # Reverse engineering
    8: "science",   # Invention
    9: "reaction",
}
OCCUPYING_JOB_STATUSES = {"active", "paused", "ready"}
TERMINAL_JOB_STATUSES = {"delivered", "cancelled", "reverted"}
SNAPSHOT_FILES = (
    "skills",
    "skill_queue",
    "blueprints",
    "assets",
    "industry_jobs",
    "public_industry_facilities",
)


class ProfileImportError(RuntimeError):
    """Raised when private ESI snapshots cannot safely populate the profile."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_iso(value: datetime | None = None) -> str:
    moment = value or utc_now()
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_utc(value: Any, description: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ProfileImportError(f"{description} is missing or invalid.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProfileImportError(f"{description} is not a valid ISO-8601 timestamp.") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProfileImportError(f"Required local file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileImportError(f"Invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise ProfileImportError(f"Could not read {path}: {exc}") from exc


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    temporary.write_text(rendered, encoding="utf-8")
    temporary.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def positive_id(value: Any, description: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ProfileImportError(f"{description} must be a positive integer.")
    return value


def read_authorized_characters(path: Path) -> list[dict[str, Any]]:
    rows = read_json(path)
    if not isinstance(rows, list):
        raise ProfileImportError("The authorized-character registry must be a JSON array.")

    normalized = []
    seen_ids = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ProfileImportError(f"Authorized-character record {index} is not an object.")
        character_id = positive_id(row.get("character_id"), f"Registry record {index} character_id")
        if character_id in seen_ids:
            raise ProfileImportError("The authorized-character registry contains duplicate IDs.")
        seen_ids.add(character_id)
        name = row.get("character_name")
        scopes = row.get("scopes", [])
        if not isinstance(name, str) or not name.strip():
            name = f"Character {index + 1}"
        if not isinstance(scopes, list) or any(not isinstance(item, str) for item in scopes):
            raise ProfileImportError(f"Registry record {index} has an invalid scopes list.")
        missing = REQUIRED_SCOPES - set(scopes)
        if missing:
            raise ProfileImportError(
                f"An authorized character is missing required scopes ({len(missing)}). "
                "Reauthorize that character before importing."
            )
        normalized.append({
            "character_id": character_id,
            "character_name": name.strip(),
            "scopes": sorted(set(scopes)),
        })

    if len(normalized) != 3:
        raise ProfileImportError(
            f"Expected exactly three authorized characters; found {len(normalized)}."
        )
    return sorted(normalized, key=lambda row: row["character_id"])


def previous_slot_assignments(import_manifest_path: Path) -> dict[int, int]:
    if not import_manifest_path.is_file():
        return {}
    previous = read_json(import_manifest_path)
    if not isinstance(previous, dict):
        raise ProfileImportError("The previous private import manifest is malformed.")
    rows = previous.get("character_mapping", [])
    if not isinstance(rows, list):
        raise ProfileImportError("The previous import manifest has an invalid character mapping.")
    assignments: dict[int, int] = {}
    used_slots = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        character_id = row.get("character_id")
        slot = row.get("slot")
        if (
            isinstance(character_id, int) and not isinstance(character_id, bool)
            and character_id > 0
            and isinstance(slot, int) and not isinstance(slot, bool)
            and slot in (1, 2, 3)
            and character_id not in assignments and slot not in used_slots
        ):
            assignments[character_id] = slot
            used_slots.add(slot)
    return assignments


def assign_slots(
    characters: list[dict[str, Any]],
    existing: dict[int, int],
) -> list[dict[str, Any]]:
    assignments = {
        row["character_id"]: existing[row["character_id"]]
        for row in characters if row["character_id"] in existing
    }
    used = set(assignments.values())
    free_slots = [slot for slot in (1, 2, 3) if slot not in used]
    for row in characters:
        if row["character_id"] not in assignments:
            assignments[row["character_id"]] = free_slots.pop(0)
    return [
        {**row, "slot": assignments[row["character_id"]]}
        for row in sorted(characters, key=lambda item: assignments[item["character_id"]])
    ]


def load_latest_snapshot(
    character: dict[str, Any],
    snapshot_root: Path,
    max_snapshot_age_hours: float,
) -> dict[str, Any]:
    character_id = character["character_id"]
    character_dir = snapshot_root / str(character_id)
    if not character_dir.is_dir():
        raise ProfileImportError(
            f"No local ESI snapshot folder exists for one authorized character. "
            "Run sso_local.py sync first."
        )
    directories = sorted(
        (item for item in character_dir.iterdir() if item.is_dir()),
        key=lambda item: item.name,
    )
    if not directories:
        raise ProfileImportError(
            f"No timestamped ESI snapshot exists for one authorized character. "
            "Run sso_local.py sync first."
        )
    snapshot_dir = directories[-1]
    manifest_path = snapshot_dir / "manifest.json"
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("snapshot_version") != 1:
        raise ProfileImportError(f"Unsupported or malformed snapshot manifest: {manifest_path}")
    if manifest.get("character_id") != character_id:
        raise ProfileImportError("Snapshot character ID does not match the authorized registry.")

    retrieved_at = parse_utc(manifest.get("retrieved_at"), "Snapshot retrieved_at")
    age_hours = (utc_now() - retrieved_at).total_seconds() / 3600
    if age_hours < -0.1:
        raise ProfileImportError("A snapshot timestamp is in the future.")
    stale = age_hours > max_snapshot_age_hours

    granted_scopes = manifest.get("granted_scopes", [])
    if not isinstance(granted_scopes, list) or not REQUIRED_SCOPES.issubset(set(granted_scopes)):
        raise ProfileImportError("A snapshot is missing one or more required ESI scopes.")

    file_metadata = manifest.get("files")
    if not isinstance(file_metadata, dict):
        raise ProfileImportError("Snapshot manifest has no file metadata.")

    payloads: dict[str, Any] = {}
    for name in SNAPSHOT_FILES:
        metadata = file_metadata.get(name)
        if not isinstance(metadata, dict):
            raise ProfileImportError(f"Snapshot is missing file metadata for {name}.")
        filename = metadata.get("file")
        if not isinstance(filename, str) or Path(filename).name != f"{name}.json":
            raise ProfileImportError(f"Snapshot has an unsafe or unexpected filename for {name}.")
        source_path = snapshot_dir / filename
        if not source_path.is_file():
            raise ProfileImportError(f"Snapshot file is missing: {source_path}")
        expected_hash = metadata.get("sha256")
        if not isinstance(expected_hash, str) or sha256_file(source_path) != expected_hash:
            raise ProfileImportError(f"Snapshot SHA-256 verification failed for {name}.")
        payload = read_json(source_path)
        if name == "skills":
            if not isinstance(payload, dict) or not isinstance(payload.get("skills"), list):
                raise ProfileImportError("The ESI skills response has an unexpected shape.")
        elif not isinstance(payload, list):
            raise ProfileImportError(f"The ESI {name} response must be a JSON array.")
        expected_count = metadata.get("record_count")
        actual_count = len(payload) if isinstance(payload, list) else None
        if expected_count is not None and actual_count is not None and expected_count != actual_count:
            raise ProfileImportError(f"Snapshot record-count verification failed for {name}.")
        payloads[name] = payload

    return {
        "snapshot_dir": snapshot_dir,
        "manifest": manifest,
        "retrieved_at": retrieved_at,
        "age_hours": max(0.0, age_hours),
        "stale": stale,
        "payloads": payloads,
    }


def normalize_skills(
    skills_payload: dict[str, Any],
    *,
    level_field: str = "active_skill_level",
) -> dict[str, int]:
    """Normalize either ESI active levels or trained levels by SDE skill type ID."""
    skills: dict[str, int] = {}
    for index, row in enumerate(skills_payload["skills"]):
        if not isinstance(row, dict):
            raise ProfileImportError(f"Skill record {index} is not an object.")
        skill_id = positive_id(row.get("skill_id"), f"Skill record {index} skill_id")
        level = row.get(level_field)
        if isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 5:
            raise ProfileImportError(
                f"Skill record {index} has an invalid {level_field}."
            )
        if str(skill_id) in skills:
            raise ProfileImportError(f"Duplicate skill ID {skill_id} in ESI response.")
        skills[str(skill_id)] = level
    return dict(sorted(skills.items(), key=lambda item: int(item[0])))


def check_skill_queue(
    queue: list[Any],
    skills: dict[str, int],
    retrieved_at: datetime,
) -> list[str]:
    warnings = []
    for index, row in enumerate(queue):
        if not isinstance(row, dict):
            warnings.append(f"Skill-queue row {index} is malformed.")
            continue
        finish_date = row.get("finish_date")
        if not finish_date:
            continue
        try:
            finished_at = parse_utc(finish_date, f"Skill-queue row {index} finish_date")
        except ProfileImportError:
            warnings.append(f"Skill-queue row {index} has an unreadable completion time.")
            continue
        if finished_at <= retrieved_at:
            skill_id = row.get("skill_id")
            finished_level = row.get("finished_level")
            if (
                isinstance(skill_id, int) and not isinstance(skill_id, bool)
                and skill_id > 0
                and isinstance(finished_level, int) and not isinstance(finished_level, bool)
                and finished_level > skills.get(str(skill_id), 0)
            ):
                warnings.append(
                    "The skill API level is behind a queue entry whose finish time has passed."
                )
    return warnings


def summarize_jobs(jobs: list[Any]) -> dict[str, Any]:
    occupied = {pool: 0 for pool in CAPACITY_SKILLS}
    status_counts: dict[str, int] = {}
    warnings = []
    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            warnings.append(f"Industry-job row {index} is malformed.")
            continue
        status = job.get("status")
        activity_id = job.get("activity_id")
        if not isinstance(status, str):
            warnings.append(f"Industry-job row {index} has no valid status.")
            continue
        status = status.lower()
        status_counts[status] = status_counts.get(status, 0) + 1
        if status in TERMINAL_JOB_STATUSES:
            continue
        if status not in OCCUPYING_JOB_STATUSES:
            warnings.append(f"Industry-job row {index} has an unrecognized status.")
            continue
        if isinstance(activity_id, bool) or not isinstance(activity_id, int):
            warnings.append(f"Industry-job row {index} has no valid activity ID.")
            continue
        pool = ACTIVITY_TO_POOL.get(activity_id)
        if pool is None:
            warnings.append(f"Industry-job row {index} has an unrecognized activity ID.")
            continue
        occupied[pool] += 1

    return {
        "occupied_jobs": occupied,
        "status_counts": dict(sorted(status_counts.items())),
        "warnings": warnings,
        "complete": not warnings,
        "reported_job_count": len(jobs),
    }


def calculate_job_capacity(
    skills: dict[str, int],
    occupied_jobs: dict[str, int],
    *,
    skills_complete: bool,
    jobs_complete: bool,
) -> dict[str, dict[str, int | None]]:
    capacity: dict[str, dict[str, int | None]] = {}
    for pool, skill_ids in CAPACITY_SKILLS.items():
        if not skills_complete or not jobs_complete:
            capacity[pool] = {
                "maximum_slots": None,
                "occupied_jobs": occupied_jobs[pool],
                "free_slots": None,
            }
            continue
        maximum = 1 + sum(skills.get(str(skill_id), 0) for skill_id in skill_ids)
        occupied = occupied_jobs[pool]
        capacity[pool] = {
            "maximum_slots": maximum,
            "occupied_jobs": occupied,
            "free_slots": maximum - occupied if occupied <= maximum else None,
        }
    return capacity


def normalize_blueprints(
    rows: list[Any],
    character_name: str,
) -> list[dict[str, Any]]:
    normalized = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ProfileImportError(f"Blueprint record {index} is not an object.")
        type_id = positive_id(row.get("type_id"), f"Blueprint record {index} type_id")
        item_id = positive_id(row.get("item_id"), f"Blueprint record {index} item_id")
        runs = row.get("runs")
        quantity = row.get("quantity")
        if (
            isinstance(runs, bool) or not isinstance(runs, int)
            or isinstance(quantity, bool) or not isinstance(quantity, int)
        ):
            raise ProfileImportError(f"Blueprint record {index} has invalid runs or quantity.")
        if quantity < -2:
            raise ProfileImportError(f"Blueprint record {index} has an invalid quantity marker.")
        is_original = quantity == -1 and runs == -1
        is_copy = quantity == -2 and runs >= 0
        if is_original:
            kind = "BPO"
            blueprint_quantity = 1
            licensed_runs = None
        elif is_copy:
            kind = "BPC"
            blueprint_quantity = 1
            licensed_runs = runs
        else:
            raise ProfileImportError(
                f"Blueprint record {index} has inconsistent ESI quantity/runs markers."
            )

        me = row.get("material_efficiency")
        te = row.get("time_efficiency")
        if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in (me, te)):
            raise ProfileImportError(f"Blueprint record {index} has invalid ME or TE values.")

        location_id = row.get("location_id")
        location_flag = row.get("location_flag")
        if isinstance(location_id, int) and not isinstance(location_id, bool):
            flag_text = location_flag if isinstance(location_flag, str) else "unknown location flag"
            location_label = f"ESI location {location_id} ({flag_text})"
        else:
            location_label = None

        normalized.append({
            "type_id": type_id,
            "state": "verified",
            "kind": kind,
            "quantity": max(1, blueprint_quantity),
            "material_efficiency": me,
            "time_efficiency": te,
            "licensed_runs": licensed_runs,
            "location_label": location_label,
            "notes": [f"Owner: {character_name}", f"Local ESI item reference: {item_id}"],
        })
    return normalized


def import_character(
    character: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    payloads = snapshot["payloads"]
    # Active levels govern current EVE capability. Keep trained levels separate
    # for detecting skill-queue entries that completed before this snapshot.
    skills = normalize_skills(payloads["skills"], level_field="active_skill_level")
    trained_skills = normalize_skills(
        payloads["skills"], level_field="trained_skill_level"
    )
    retrieved_at = snapshot["retrieved_at"]
    warnings = check_skill_queue(
        payloads["skill_queue"], trained_skills, retrieved_at
    )
    if snapshot["stale"]:
        warnings.append("The snapshot exceeds the configured freshness window.")

    skill_state = "verified" if not warnings else "partial"
    job_summary = summarize_jobs(payloads["industry_jobs"])
    warnings.extend(job_summary["warnings"])
    jobs_complete = job_summary["complete"] and not snapshot["stale"]
    capacity = calculate_job_capacity(
        skills,
        job_summary["occupied_jobs"],
        skills_complete=(skill_state == "verified"),
        jobs_complete=jobs_complete,
    )
    for pool, result in capacity.items():
        if result["free_slots"] is None:
            warnings.append(f"{pool.capitalize()} free-slot count could not be verified.")

    blueprint_rows = normalize_blueprints(
        payloads["blueprints"], character["character_name"]
    )
    character_state = (
        "verified"
        if skill_state == "verified" and jobs_complete
        and all(value["free_slots"] is not None for value in capacity.values())
        else "partial"
    )

    return {
        "character": character,
        "snapshot_dir": str(snapshot["snapshot_dir"]),
        "snapshot_retrieved_at": utc_iso(retrieved_at),
        "snapshot_age_hours": round(snapshot["age_hours"], 2),
        "snapshot_stale": snapshot["stale"],
        "skills": skills,
        "skill_state": skill_state,
        "skill_queue_count": len(payloads["skill_queue"]),
        "blueprints": blueprint_rows,
        "blueprint_count": len(blueprint_rows),
        "asset_record_count": len(payloads["assets"]),
        "public_facility_record_count": len(payloads["public_industry_facilities"]),
        "industry_job_summary": job_summary,
        "job_capacity": capacity,
        "record_state": character_state,
        "warnings": sorted(set(warnings)),
    }


def build_operating_profile(
    profile: dict[str, Any],
    imported_characters: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = json.loads(json.dumps(profile))
    existing_characters = {
        row["slot"]: row for row in result["characters"]
    }
    blueprints = []
    mapping = []

    for imported in imported_characters:
        registry_row = imported["character"]
        slot = registry_row["slot"]
        character = existing_characters[slot]
        old_label = character.get("label")
        default_labels = {
            f"Character {slot}",
            f"Character slot {slot}",
            "",
            None,
        }
        if old_label in default_labels:
            character["label"] = registry_row["character_name"]

        character["skills"] = imported["skills"]
        character["skills_state"] = imported["skill_state"]
        character["state"] = imported["record_state"]
        character["job_capacity"] = {
            pool: capacity["free_slots"]
            for pool, capacity in imported["job_capacity"].items()
        }
        existing_notes = character.get("notes", [])
        if not isinstance(existing_notes, list):
            existing_notes = []
        retained_notes = [
            note for note in existing_notes
            if not (isinstance(note, str) and note.startswith("ESI import:"))
        ]
        retained_notes.append(
            "ESI import: active skill levels and derived free job slots reflect the latest local snapshot."
        )
        retained_notes.append(
            "ESI import: verify any ready-to-deliver jobs older than 90 days in-game; "
            "ESI completed-job history is limited to 90 days."
        )
        if imported["warnings"]:
            retained_notes.append(
                "ESI import: one or more values remain partial; see the private import manifest."
            )
        character["notes"] = retained_notes
        blueprints.extend(imported["blueprints"])
        mapping.append({
            "slot": slot,
            "character_id": registry_row["character_id"],
            "character_name": registry_row["character_name"],
            "snapshot_retrieved_at": imported["snapshot_retrieved_at"],
            "snapshot_age_hours": imported["snapshot_age_hours"],
            "snapshot_stale": imported["snapshot_stale"],
            "skills_state": imported["skill_state"],
            "known_skill_count": len(imported["skills"]),
            "skill_queue_count": imported["skill_queue_count"],
            "blueprint_count": imported["blueprint_count"],
            "asset_record_count": imported["asset_record_count"],
            "industry_job_summary": imported["industry_job_summary"],
            "job_capacity": imported["job_capacity"],
            "record_state": imported["record_state"],
            "warnings": imported["warnings"],
        })

    result["blueprints"] = sorted(
        blueprints,
        key=lambda row: (
            row["type_id"],
            row["kind"],
            row["material_efficiency"] or 0,
            row["time_efficiency"] or 0,
            row["licensed_runs"] if row["licensed_runs"] is not None else -1,
            row["location_label"] or "",
            tuple(row["notes"]),
        ),
    )
    # Character endpoints give a complete personal blueprint list, but this
    # project has not imported corporation-owned blueprints. Keep the combined
    # operating inventory partial so absence is not treated as proof of no access.
    result["blueprints_state"] = "partial"
    root_notes = result.get("notes", [])
    if not isinstance(root_notes, list):
        root_notes = []
    scope_note = (
        "ESI import covers personal blueprints owned by the three authorized characters; "
        "corporation-owned blueprints are not included, so total operation blueprint "
        "coverage remains partial."
    )
    root_notes = [note for note in root_notes if note != scope_note]
    root_notes.append(scope_note)
    result["notes"] = root_notes

    errors = validate_profile_data(result)
    if errors:
        raise ProfileImportError(
            "Imported profile failed schema validation: " + "; ".join(errors)
        )
    return result, mapping


def load_base_profile(profile_path: Path, example_path: Path) -> dict[str, Any]:
    if profile_path.is_file():
        profile = read_json(profile_path)
    else:
        profile = read_json(example_path)
    if not isinstance(profile, dict):
        raise ProfileImportError("The operating profile root must be a JSON object.")
    errors = validate_profile_data(profile)
    if errors:
        raise ProfileImportError(
            "Existing operating profile is invalid; no files were changed: "
            + "; ".join(errors)
        )
    return profile


def run_import(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if args.max_snapshot_age_hours <= 0:
        raise ProfileImportError("--max-snapshot-age-hours must be greater than zero.")

    registry_rows = read_authorized_characters(args.registry)
    existing_map = previous_slot_assignments(args.import_manifest)
    slotted_characters = assign_slots(registry_rows, existing_map)

    imported = []
    for character in slotted_characters:
        snapshot = load_latest_snapshot(
            character,
            args.snapshot_root,
            args.max_snapshot_age_hours,
        )
        imported.append(import_character(character, snapshot))

    profile = load_base_profile(args.profile, args.example)
    populated_profile, character_mapping = build_operating_profile(profile, imported)

    # /industry/facilities/ is a public directory fetched once per character.
    # Do not sum the same public directory three times and imply unique facilities.
    public_facility_count = imported[0]["public_facility_record_count"]
    personal_blueprints_state = (
        "verified"
        if all(not item["snapshot_stale"] for item in imported)
        else "partial"
    )
    import_manifest = {
        "import_version": 1,
        "created_at": utc_iso(),
        "source": "Local EVE ESI snapshots",
        "character_mapping": character_mapping,
        "blueprint_total": len(populated_profile["blueprints"]),
        "personal_blueprints_state": personal_blueprints_state,
        "blueprint_coverage": (
            "Complete for the three authorized characters' personal blueprint lists; "
            "corporation-owned blueprints are not included."
        ),
        "public_industry_facility_record_count": public_facility_count,
        "facility_access_verified": False,
        "industry_jobs_include_completed": True,
        "job_capacity_caveat": (
            "ESI completed-job history is limited to the past 90 days. Check the "
            "in-game Industry window for any ready-to-deliver jobs older than 90 days "
            "before treating slot counts as definitive."
        ),
        "facility_access_note": (
            "The public ESI facility directory does not establish character access, "
            "service availability, or structure ACL coverage."
        ),
        "manual_profile_sections_preserved": [
            "capital",
            "operations",
            "facilities",
            "market_access",
            "logistics",
        ],
        "privacy": {
            "contains_character_ids_and_names": True,
            "contains_skill_ids_and_levels": False,
            "contains_blueprint_type_ids": False,
            "contains_asset_or_job_item_ids": False,
            "contains_skill_levels": False,
            "contains_access_or_refresh_tokens": False,
            "must_remain_local": True,
        },
    }
    readiness = build_readiness_report(populated_profile)
    readiness["blueprint_inventory"]["coverage"] = (
        "Personal blueprints for the three authorized characters only; "
        "corporation-owned blueprints are not imported."
    )
    readiness["esi_import"] = {
        "snapshot_count": len(imported),
        "fresh_snapshot_count": sum(1 for item in imported if not item["snapshot_stale"]),
        "stale_snapshot_count": sum(1 for item in imported if item["snapshot_stale"]),
        "personal_blueprints_state": personal_blueprints_state,
        "facility_access_verified": False,
        "industry_jobs_include_completed": True,
        "job_capacity_method": (
            "Active skill levels less active, paused, and ready jobs, grouped by "
            "Manufacturing, Science, and Reaction."
        ),
        "job_capacity_caveat": (
            "ESI completed-job history is limited to the past 90 days. Verify any "
            "ready-to-deliver jobs older than 90 days in-game."
        ),
        "facility_access_limitation": (
            "Public facility-directory records do not prove character access, "
            "service availability, or complete structure ACL coverage."
        ),
    }

    # Validate everything in memory before writing any output.
    errors = validate_profile_data(populated_profile)
    if errors:
        raise ProfileImportError("Final profile validation failed: " + "; ".join(errors))
    return populated_profile, import_manifest, readiness


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--snapshot-root", type=Path, default=DEFAULT_SNAPSHOT_ROOT)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--example", type=Path, default=DEFAULT_EXAMPLE)
    parser.add_argument("--import-manifest", type=Path, default=DEFAULT_IMPORT_MANIFEST)
    parser.add_argument("--readiness-output", type=Path, default=DEFAULT_READINESS)
    parser.add_argument(
        "--max-snapshot-age-hours",
        type=float,
        default=24.0,
        help="Snapshots older than this remain imported but are marked partial (default: 24).",
    )
    args = parser.parse_args()

    try:
        profile, manifest, readiness = run_import(args)
        write_json_atomic(args.profile, profile)
        write_json_atomic(args.import_manifest, manifest)
        write_json_atomic(args.readiness_output, readiness)
    except (ProfileImportError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    complete = sum(
        1 for row in manifest["character_mapping"]
        if row["record_state"] == "verified"
    )
    print(
        f"PASS: imported three character profiles; {complete} of 3 have fully verified "
        "skills and current free job-slot counts."
    )
    print(
        f"PASS: imported {manifest['blueprint_total']} personal blueprint records."
    )
    print(f"PASS: wrote private operating profile to {args.profile}")
    print(f"PASS: wrote private import manifest to {args.import_manifest}")
    print(f"PASS: wrote redacted readiness report to {args.readiness_output}")
    print(
        "NOTE: verify any ready-to-deliver jobs older than 90 days in-game. "
        "Corporation-owned blueprints, facility access, capital, market access, "
        "and logistics are not inferred by this import."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
