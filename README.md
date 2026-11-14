# EVE Online Industrial Knowledge Base

A VS Code-first, Git-managed research repository for EVE Online industry. The canonical knowledge bundle is in [`knowledge/`](knowledge/index.md) and follows **Open Knowledge Format (OKF) v0.2**.

## Start here

1. Read [`LLM-START-HERE.md`](LLM-START-HERE.md) before asking an LLM to work on this project.
2. Open this folder in VS Code.
3. Review [the project charter](knowledge/00-governance/project-charter.md) and [research standards](knowledge/00-governance/research-standards.md).
4. Review the [research backlog](knowledge/10-research-management/research-backlog.md) and [claims requiring verification](knowledge/10-research-management/claims-requiring-verification.md).
5. Use Git branches or diffs for proposed changes. Do not let an LLM silently replace canonical knowledge.

## Repository layout

- `knowledge/`: canonical, source-backed OKF knowledge bundle.
- `exports/`: task-specific LLM packages and reusable handoff templates.
- `tools/`: local data-acquisition and inspection scripts.
- `tools/sde/`: standard-library Python tools for downloading and inspecting CCP's Static Data Export.
- `LLM-START-HERE.md`: compact onboarding context for new model sessions.

## Local SDE workflow

The SDE downloader uses Python 3.10+ and no third-party dependencies:

```powershell
py -3 tools/sde/fetch_sde.py --variant jsonl
py -3 tools/sde/fetch_sde.py --variant jsonl --extract
```

See [`tools/sde/README.md`](tools/sde/README.md) for details. Raw SDE archives and extracted datasets belong under `data/raw/` and are excluded from Git. Keep build metadata, parser code, and reproducible derived outputs instead of committing the full archive.

A public, read-only ESI collector is available under [`tools/esi/`](tools/esi/README.md). It collects selected regional market orders/history, adjusted prices, and industry system indices without EVE SSO credentials.

## Research status

This repository has moved beyond its initial scaffold. It now contains source-backed draft concepts covering blueprint mechanics, job capacity, facilities, production systems, industrial economics, throughput, market intelligence, ESI/SDE data practices, and operational playbooks.

**Draft does not mean verified.** The concept status and verification notes must reflect actual independent checks. Several mechanics and formulas still require comparison with current in-game Industry/PI quotes or controlled tests. The research backlog and verification queue distinguish documented topics from completed verification.

## OKF specification

This project targets OKF v0.2. The canonical specification is maintained at the [GoogleCloudPlatform/open-knowledge-format repository](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). The former `knowledge-catalog/okf` copy is not the canonical home.
