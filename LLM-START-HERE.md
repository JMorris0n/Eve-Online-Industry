# LLM Project Handoff: EVE Industrial Knowledge Base

## Purpose

Help maintain a rigorous, portable, low-context knowledge base about EVE Online industry. The repository is designed for human use, VS Code, Git, and multiple LLM providers, including models with strict upload limits.

## Canonical structure

- `knowledge/` is the canonical knowledge base and targets OKF v0.2.
- `exports/` contains task-specific handoffs and templates. Exports are derived from canonical documents and are not competing sources of truth.
- Root `README.md` explains repository use.
- This file is the compact onboarding context for a new model session.

## Required working behavior

1. Inspect relevant existing files before proposing changes.
2. Do not rewrite the entire knowledge base for a narrow task.
3. Distinguish four epistemic categories:
   - **Mechanic:** a stated or observed game rule.
   - **Derived calculation:** a reproducible result from mechanics and inputs.
   - **Strategic recommendation:** advice based on stated objectives and assumptions.
   - **Hypothesis:** a claim awaiting verification.
4. Cite factual claims at claim level using source IDs in OKF frontmatter and Markdown footnotes.
5. Prefer current CCP documentation, patch notes, in-game UI, and official ESI data for mechanics and live values. Use reproducible tests for undocumented behavior. Treat community references and third-party tools as secondary evidence.
6. Record conflicts, limitations, test conditions, and unresolved questions. Do not silently choose between conflicting sources.
7. Never treat agreement between LLMs as independent factual verification.
8. Preserve existing paths, metadata, source IDs, cross-links, and verified claims.
9. Return complete revised files or a unified diff, plus a concise change summary.
10. Do not fabricate source URLs, patch dates, formula inputs, market prices, or test results.
11. Do not commit to the primary branch unless the user explicitly delegated direct maintenance. Otherwise use a branch or unified diff.
12. Never commit EVE SSO tokens, refresh tokens, client secrets, local ESI cache, or raw SDE archives.

## Suggested task workflow

- Read `knowledge/index.md` and the relevant directory index.
- Read the target concept and its dependencies.
- Research only the assigned question.
- Return findings with sources, confidence limitations, calculations, and open questions.
- Propose the smallest necessary edits.
- Wait for human review before integrating changes into the primary branch.

## Upload budget

For a focused LLM assignment, prefer one self-contained file in this order:
1. `LLM-HANDOFF.md` with the task and essential context.
2. `SUPPORTING-DATA.md` only when numerical inputs or datasets matter.
3. `PRIMARY-SOURCES.md` only when source excerpts or source-specific instructions are necessary.

Do not upload the entire repository for a narrow task.

## Current scope

The initial scope is comprehensive: foundations, T1/T2/T3 production, invention, reactions, planetary industry, sourcing, industrial economics, optimization, market intelligence, tooling, playbooks, and deterministic calculations. The repository contains source-backed draft concepts and computations, but `status: draft` means the content has not necessarily passed independent in-game verification. Consult the research backlog and verification queue before treating a claim as operationally confirmed.

## Format reference

OKF v0.2 canonical specification: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
