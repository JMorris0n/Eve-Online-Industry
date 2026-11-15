"""Tests for the local ESI-to-operating-profile importer."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "profile"))

from import_esi_profile import (  # noqa: E402
    REQUIRED_SCOPES,
    SNAPSHOT_FILES,
    ProfileImportError,
    assign_slots,
    load_latest_snapshot,
    run_import,
)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_payloads(
    *,
    skills=None,
    queue=None,
    blueprints=None,
    jobs=None,
    assets=None,
    facilities=None,
):
    skill_rows = []
    for skill in skills or []:
        normalized = dict(skill)
        normalized.setdefault("active_skill_level", normalized.get("trained_skill_level", 0))
        normalized.setdefault("trained_skill_level", normalized.get("active_skill_level", 0))
        skill_rows.append(normalized)
    return {
        "skills": {"skills": skill_rows},
        "skill_queue": queue or [],
        "blueprints": blueprints or [],
        "assets": assets or [],
        "industry_jobs": jobs or [],
        "public_industry_facilities": facilities or [],
    }


def make_snapshot(root: Path, character_id: int, payloads, retrieved_at: datetime) -> Path:
    stamp = retrieved_at.strftime("%Y%m%dT%H%M%S000000Z")
    directory = root / str(character_id) / stamp
    directory.mkdir(parents=True)
    files = {}
    for name in SNAPSHOT_FILES:
        filename = f"{name}.json"
        content = json.dumps(payloads[name], indent=2, ensure_ascii=False) + "\n"
        output = directory / filename
        output.write_text(content, encoding="utf-8")
        files[name] = {
            "file": filename,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "record_count": len(payloads[name]) if isinstance(payloads[name], list) else None,
        }
    manifest = {
        "snapshot_version": 1,
        "character_id": character_id,
        "character_name": f"Pilot {character_id}",
        "retrieved_at": iso(retrieved_at),
        "compatibility_date": "2026-11-13",
        "granted_scopes": sorted(REQUIRED_SCOPES),
        "endpoint_metadata": {},
        "files": files,
    }
    write_json(directory / "manifest.json", manifest)
    return directory


def make_registry(path: Path, character_ids=(101, 202, 303)) -> None:
    write_json(path, [
        {
            "character_id": character_id,
            "character_name": f"Pilot {character_id}",
            "scopes": sorted(REQUIRED_SCOPES),
            "authorized_at": "2026-11-14T00:00:00Z",
        }
        for character_id in character_ids
    ])


def make_profile() -> dict:
    return json.loads((ROOT / "config" / "operating-profile.example.json").read_text(encoding="utf-8"))


class EsiProfileImporterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.snapshot_root = self.root / "snapshots"
        self.registry = self.root / "authorized-characters.json"
        self.profile = self.root / "operating-profile.json"
        self.example = ROOT / "config" / "operating-profile.example.json"
        self.import_manifest = self.root / "profile-import-manifest.json"
        self.readiness = self.root / "profile-readiness.json"
        make_registry(self.registry)
        self.now = datetime.now(timezone.utc).replace(microsecond=0)

    def tearDown(self):
        self.temp.cleanup()

    def write_three_snapshots(self, payload_by_id=None, retrieved_at=None):
        payload_by_id = payload_by_id or {}
        retrieved_at = retrieved_at or self.now
        for character_id in (101, 202, 303):
            make_snapshot(
                self.snapshot_root,
                character_id,
                payload_by_id.get(character_id, make_payloads()),
                retrieved_at,
            )

    def args(self, max_age=24):
        return SimpleNamespace(
            registry=self.registry,
            snapshot_root=self.snapshot_root,
            profile=self.profile,
            example=self.example,
            import_manifest=self.import_manifest,
            readiness_output=self.readiness,
            max_snapshot_age_hours=max_age,
        )

    def test_import_populates_skills_blueprints_and_current_free_slots(self):
        payloads = make_payloads(
            skills=[
                {"skill_id": 3387, "trained_skill_level": 4, "active_skill_level": 4, "skillpoints_in_skill": 45255},
                {"skill_id": 24625, "trained_skill_level": 2, "active_skill_level": 2, "skillpoints_in_skill": 256000},
                {"skill_id": 3406, "trained_skill_level": 3, "active_skill_level": 3, "skillpoints_in_skill": 8000},
                {"skill_id": 24624, "trained_skill_level": 1, "active_skill_level": 1, "skillpoints_in_skill": 45255},
                {"skill_id": 45748, "trained_skill_level": 2, "active_skill_level": 2, "skillpoints_in_skill": 256000},
                {"skill_id": 45749, "trained_skill_level": 1, "active_skill_level": 1, "skillpoints_in_skill": 45255},
            ],
            jobs=[
                {"activity_id": 1, "status": "active"},
                {"activity_id": 3, "status": "ready"},
                {"activity_id": 8, "status": "paused"},
                {"activity_id": 9, "status": "active"},
            ],
            blueprints=[
                {
                    "item_id": 7001, "type_id": 111,
                    "location_id": 60000001, "location_flag": "Hangar",
                    "material_efficiency": 10, "time_efficiency": 20,
                    "quantity": -1, "runs": -1,
                },
                {
                    "item_id": 7002, "type_id": 222,
                    "location_id": 60000002, "location_flag": "CorpSAG1",
                    "material_efficiency": 4, "time_efficiency": 8,
                    "quantity": -2, "runs": 55,
                },
                {
                    "item_id": 7003, "type_id": 333,
                    "location_id": 60000003, "location_flag": "Hangar",
                    "material_efficiency": 0, "time_efficiency": 0,
                    "quantity": 4, "runs": -1,
                },
            ],
        )
        self.write_three_snapshots({101: payloads})

        existing = make_profile()
        existing["capital"]["working_capital_isk"] = 123456
        write_json(self.profile, existing)

        profile, manifest, readiness = run_import(self.args())
        char = next(row for row in profile["characters"] if row["label"] == "Pilot 101")

        self.assertEqual(char["skills"]["3387"], 4)
        self.assertEqual(char["skills_state"], "verified")
        self.assertEqual(char["job_capacity"], {
            "manufacturing": 6,
            "science": 3,
            "reaction": 3,
        })
        self.assertEqual(profile["blueprints_state"], "partial")
        self.assertEqual(manifest["personal_blueprints_state"], "verified")
        self.assertEqual(
            readiness["blueprint_inventory"]["coverage"],
            "Personal blueprints for the three authorized characters only; "
            "corporation-owned blueprints are not imported.",
        )
        self.assertEqual(len(profile["blueprints"]), 3)
        original = next(
            row for row in profile["blueprints"]
            if row["kind"] == "BPO" and row["type_id"] == 111
        )
        stacked_original = next(
            row for row in profile["blueprints"]
            if row["kind"] == "BPO" and row["type_id"] == 333
        )
        copy = next(row for row in profile["blueprints"] if row["kind"] == "BPC")
        self.assertEqual(original["quantity"], 1)
        self.assertIsNone(original["licensed_runs"])
        self.assertEqual(stacked_original["quantity"], 4)
        self.assertIsNone(stacked_original["licensed_runs"])
        self.assertEqual(copy["licensed_runs"], 55)
        self.assertEqual(profile["capital"]["working_capital_isk"], 123456)
        self.assertEqual(profile["facilities_state"], "unknown")
        self.assertFalse(manifest["facility_access_verified"])
        self.assertTrue(readiness["profile_schema_valid"])
        serialized_readiness = json.dumps(readiness)
        for private in ("Pilot 101", "3387", "7001", "60000001", "123456"):
            self.assertNotIn(private, serialized_readiness)
        serialized_profile = json.dumps(profile)
        self.assertNotIn('"character_id"', serialized_profile)
        self.assertNotIn('"101"', serialized_profile)


    def test_active_skill_levels_and_reverse_engineering_consume_current_capacity(self):
        payloads = make_payloads(
            skills=[
                {"skill_id": 3387, "trained_skill_level": 5, "active_skill_level": 2},
                {"skill_id": 3406, "trained_skill_level": 4, "active_skill_level": 1},
            ],
            jobs=[
                {"activity_id": 1, "status": "active"},
                {"activity_id": 7, "status": "ready"},
            ],
        )
        self.write_three_snapshots({101: payloads})
        profile, manifest, _ = run_import(self.args())
        character = profile["characters"][0]
        self.assertEqual(character["skills"]["3387"], 2)
        self.assertEqual(character["skills"]["3406"], 1)
        self.assertEqual(character["job_capacity"]["manufacturing"], 2)
        self.assertEqual(character["job_capacity"]["science"], 1)
        self.assertEqual(manifest["character_mapping"][0]["industry_job_summary"]["occupied_jobs"]["science"], 1)

    def test_completed_but_unapplied_queue_entry_marks_skills_partial(self):
        payloads = make_payloads(
            skills=[{"skill_id": 3387, "trained_skill_level": 1}],
            queue=[{
                "skill_id": 3387,
                "finished_level": 2,
                "finish_date": iso(self.now - timedelta(hours=1)),
            }],
        )
        self.write_three_snapshots({101: payloads})
        profile, manifest, _ = run_import(self.args())
        row = next(item for item in manifest["character_mapping"] if item["character_id"] == 101)
        self.assertEqual(row["skills_state"], "partial")
        self.assertIsNone(row["job_capacity"]["manufacturing"]["free_slots"])
        char = profile["characters"][0]
        self.assertEqual(char["skills_state"], "partial")
        self.assertIsNone(char["job_capacity"]["manufacturing"])
        self.assertIn(
            "completed_skill_queue_level_not_reflected",
            readiness["character_slots"][0]["skills_diagnostic_codes"],
        )
        self.assertIn(
            "job_capacity_blocked_by_partial_skills",
            readiness["character_slots"][0]["job_capacity_diagnostic_codes"],
        )
        self.assertNotIn(
            "other_import_warning",
            readiness["character_slots"][0]["skills_diagnostic_codes"],
        )

    def test_unknown_active_job_activity_prevents_slot_inference(self):
        payloads = make_payloads(jobs=[{"activity_id": 77, "status": "active"}])
        self.write_three_snapshots({101: payloads})
        profile, manifest, _ = run_import(self.args())
        row = next(item for item in manifest["character_mapping"] if item["character_id"] == 101)
        self.assertFalse(row["industry_job_summary"]["complete"])
        self.assertIsNone(row["job_capacity"]["manufacturing"]["free_slots"])
        self.assertTrue(any("unrecognized activity" in message for message in row["warnings"]))

    def test_old_snapshot_is_imported_but_marked_partial(self):
        old = self.now - timedelta(days=2)
        self.write_three_snapshots(retrieved_at=old)
        profile, manifest, _ = run_import(self.args(max_age=24))
        self.assertEqual(profile["blueprints_state"], "partial")
        self.assertTrue(all(row["snapshot_stale"] for row in manifest["character_mapping"]))
        self.assertTrue(all(row["skills_state"] == "partial" for row in manifest["character_mapping"]))
        self.assertIsNone(profile["characters"][0]["job_capacity"]["manufacturing"])

    def test_corrupt_snapshot_file_is_rejected(self):
        self.write_three_snapshots()
        char_dir = self.snapshot_root / "101"
        latest = sorted(char_dir.iterdir(), key=lambda item: item.name)[-1]
        with (latest / "skills.json").open("a", encoding="utf-8") as stream:
            stream.write(" ")
        with self.assertRaisesRegex(ProfileImportError, "SHA-256"):
            load_latest_snapshot(
                {"character_id": 101},
                self.snapshot_root,
                24,
            )

    def test_slot_assignments_remain_stable_after_registry_sorting(self):
        rows = [
            {"character_id": 101, "character_name": "A"},
            {"character_id": 202, "character_name": "B"},
            {"character_id": 303, "character_name": "C"},
        ]
        assigned = assign_slots(rows, {303: 1, 101: 3})
        self.assertEqual(
            {row["character_id"]: row["slot"] for row in assigned},
            {303: 1, 202: 2, 101: 3},
        )

    def test_missing_one_snapshot_aborts_without_creating_profile(self):
        for character_id in (101, 202):
            make_snapshot(self.snapshot_root, character_id, make_payloads(), self.now)
        with self.assertRaises(ProfileImportError):
            run_import(self.args())
        self.assertFalse(self.profile.exists())


if __name__ == "__main__":
    unittest.main()
