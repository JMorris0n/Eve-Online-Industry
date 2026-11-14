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

To extract the archive:

```powershell
py -3 tools/sde/fetch_sde.py --variant jsonl --extract
```

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
