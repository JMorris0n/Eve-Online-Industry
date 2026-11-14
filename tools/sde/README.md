# Local SDE tools

These scripts download and inspect CCP's official EVE Online Static Data Export (SDE). They use only the Python standard library.

## Requirements

- Python 3.10 or newer.
- Internet access to `developers.eveonline.com`.
- Disk space for the selected SDE archive and, if requested, its extracted contents.

## Download the latest JSON Lines SDE

From the repository root:

```powershell
py -3 tools/sde/fetch_sde.py --variant jsonl
```

The script:
1. Fetches CCP's `latest.jsonl` build manifest.
2. Downloads the latest JSON Lines archive using CCP's documented redirect URL.
3. Determines the build number from the final redirected archive URL.
4. Calculates SHA-256 and checks ZIP integrity.
5. Saves a `manifest.json` with build, URL, timestamp, hash, and HTTP metadata.

To extract during download:

```powershell
py -3 tools/sde/fetch_sde.py --variant jsonl --extract
```

To extract an archive that is already downloaded, without downloading it again:

```powershell
$archive = Get-ChildItem data/raw/sde/*/*.zip |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
$extracted = Join-Path $archive.DirectoryName "extracted"
Expand-Archive -LiteralPath $archive.FullName -DestinationPath $extracted
```

The local `data/derived/` directory is Git-ignored because normalized recipe and analysis outputs are generated from the local SDE. Preserve small, hand-reviewed reference tables separately only when they are intentionally part of the knowledge base.

To use YAML instead:

```powershell
py -3 tools/sde/fetch_sde.py --variant yaml --extract
```

To replace an existing build archive:

```powershell
py -3 tools/sde/fetch_sde.py --variant jsonl --force
```

## Inspect the archive

```powershell
py -3 tools/sde/inspect_sde.py data/raw/sde/BUILD/eve-online-static-data-BUILD-jsonl.zip
```

Replace `BUILD` with the build number printed by the downloader. The inspector lists relevant files and prints one sample JSONL record so the current schema can be examined before writing parsers.

## Normalize manufacturing and reaction recipes

After extracting the SDE archive, the current-format parser can produce a normalized JSON Lines file:

```powershell
py -3 tools/sde/parse_industry_recipes.py \
    --sde-dir data/raw/sde/BUILD/extracted \
    --activity all \
    --output data/derived/industry-recipes.jsonl
```

Replace `BUILD` with the downloaded build number. The parser reads the current `blueprints.jsonl` and `types.jsonl` tables, joins English type names and useful type metadata (published status, group/market group, tech level, portion size, and volume), and emits one record per manufacturing or reaction activity. Materials and products retain their type metadata; required-skill entries retain the joined name, required level, and publication status when present in the SDE. A missing metadata join remains unknown rather than being inferred as unpublished. Manufacturing skill requirements in the SDE may explicitly be level 0. Preserve this as a valid zero-level requirement, not missing data or a training target.

The output is a normalized recipe reference, **not** a final job quote. It does not apply blueprint ME, structure/facility bonuses, system cost indices, job installation fees, character skill effects, or market prices. Do not use it directly as a profitability result.

The parser supports direct SDE records and the documented generic `_key`/`_value` envelope. In the current schema, manufacturing material/product/skill arrays are optional while reaction arrays are required. Omitted manufacturing arrays are retained as explicit source-field states; an omitted material list makes the recipe incomplete and unsuitable for cost calculation. Records without a product array are skipped and counted. The parser prints counts for examined activities, skipped records, and incomplete recipe fields so ingestion results can be audited.

## Data placement

Downloaded data belongs under `data/raw/sde/` and is intentionally excluded from Git. Do not commit the full SDE archive or extracted data into the knowledge repository. Keep only:
- Build number and manifest.
- Parser code.
- Small, curated derived outputs where licensing and size permit.
- Reproducible extraction notes and validation results.

## Important source rules

- CCP publishes both JSON Lines and YAML. JSON Lines is the default because it is more suitable for large datasets.
- The latest archive URL redirects to a build-numbered file. The resolved URL and SHA-256 are recorded.
- CCP publishes a schema changelog. Review it before changing parsers.
- The SDE is static data, not current market data or character state.
- Do not assume old CSV conversions or pre-September-2025 parsers match the current schema.

Official documentation: https://developers.eveonline.com/docs/services/static-data/


## Audit normalized recipe quality

After the parser has written `data/derived/industry-recipes.jsonl`, run:

```powershell
py -3 tools/sde/audit_industry_recipes.py `
    --input "data/derived/industry-recipes.jsonl" `
    --output "data/derived/industry-recipes-audit.json"
```

This local-only audit checks activity counts, complete/incomplete source-field states, duplicate blueprint/activity keys, joined type-name/publication metadata, duplicate item IDs, invalid records, and exceptional zero-time or unpublished records. Audit version 2 also reports distinct unpublished and unknown-publication skill type IDs separately from reference counts, with small ID samples. It does not print the recipe file. The JSONL and audit output stay in Git-ignored `data/derived/`. The report is a data-quality check, not proof that any product is marketable or profitable.

## Build the local skill-requirements reference

After the corrected recipe parser has produced data/derived/industry-recipes.jsonl, build a local reference of skills required by complete, published recipes:

```powershell
py -3 tools/sde/build_skill_requirements.py `
    --input "data/derived/industry-recipes.jsonl" `
    --output "data/derived/skill-requirements.json" `
    --activity all
```

Use --activity manufacturing to limit the reference to manufacturing, or --activity reaction for reactions. The default includes both and reports them separately.

The tool ranks required skills by how many recipes pass its static-data filters. The profile-capture list includes only skills with a known name and published status that are required by at least one eligible recipe. Each entry reports recipe coverage, activity coverage, and the required-level distribution. The full observed-skill section retains unpublished or otherwise excluded skill references for review rather than silently discarding them.

A recipe enters the skill-reference candidate set only when its material/product data is explicitly complete, its blueprint is published and named, its base time is positive, its material names resolve, at least one named published product output exists, and its skill array plus each required skill's name, level, and publication status are known and published. Omitted/null skill arrays are not treated as an empty list.

This is a **skill-inventory planning reference**, not a marketability, character-feasibility, blueprint-ownership, facility-access, or profitability result. Published output types and complete SDE recipes still need to be checked against actual market access, demand, available blueprints, facilities, and the user's three-character profile. The generated JSON stays under Git-ignored data/derived/; do not commit private profile data or upload the raw recipe JSONL.
