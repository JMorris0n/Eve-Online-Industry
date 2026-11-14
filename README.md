# EVE Online Industrial Knowledge Base

A VS Code-first, Git-managed research repository for EVE Online industry. The canonical knowledge bundle is in [`knowledge/`](knowledge/index.md) and follows **Open Knowledge Format (OKF) v0.2**.

## Start here

1. Read [`LLM-START-HERE.md`](LLM-START-HERE.md) before asking an LLM to work on this project.
2. Open this folder in VS Code.
3. Review [`knowledge/00-governance/project-charter.md`](knowledge/00-governance/project-charter.md) and [`knowledge/00-governance/research-standards.md`](knowledge/00-governance/research-standards.md).
4. Start with the P0 items in [`knowledge/10-research-management/research-backlog.md`](knowledge/10-research-management/research-backlog.md).
5. Use Git branches or diffs for proposed changes. Do not let an LLM silently replace canonical knowledge.

## Repository layout

- `knowledge/`: canonical, source-backed OKF knowledge bundle.
- `exports/`: task-specific LLM packages and reusable handoff templates.
- `LLM-START-HERE.md`: compact onboarding context for new model sessions.
- `references/`: reserved inside the knowledge bundle for source catalogs and tool documentation.

## OKF specification

This project targets OKF v0.2. The canonical specification is maintained at the [GoogleCloudPlatform/open-knowledge-format repository](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). The former `knowledge-catalog/okf` copy is not the canonical home.

## Project status

This is an initial scaffold. Concept files are drafts and placeholders unless their body explicitly says otherwise. No EVE Online game mechanic should be treated as verified merely because a placeholder exists.
