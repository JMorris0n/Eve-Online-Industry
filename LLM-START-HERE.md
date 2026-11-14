# LLM Project Handoff: EVE Industrial Knowledge Base

## First five minutes

1. Read this file completely.
2. Read [the LLM Collaboration Protocol](knowledge/00-governance/llm-collaboration.md) and [Research and Verification Standards](knowledge/00-governance/research-standards.md).
3. Read [the knowledge index](knowledge/index.md) and the relevant topic index.
4. Check the [research backlog](knowledge/10-research-management/research-backlog.md), [open questions](knowledge/10-research-management/open-questions.md), and [claims requiring verification](knowledge/10-research-management/claims-requiring-verification.md).
5. Record the repository baseline commit SHA before making changes. Inspect the target files and their dependencies before editing.

## Project purpose

Maintain a rigorous, portable, low-context knowledge base about EVE Online industry. The repository is designed for human use, VS Code, Git, and multiple LLM providers. It is not a transcript archive. Each LLM session should receive a small, self-contained assignment and return a reproducible result.

## Source of truth and architecture

- `knowledge/` is the canonical knowledge base and targets OKF v0.2.
- `knowledge/00-governance/` defines collaboration, evidence, and document rules.
- `exports/templates/` contains reusable, provider-neutral task packets and review prompts.
- `exports/generated/` is a local temporary staging area and is ignored by Git.
- `tools/` contains local acquisition, inspection, and deterministic calculation scripts.
- Root `README.md` explains repository use.
- This file is the compact onboarding context for a new model session.

Never maintain the same mechanic as competing copies. A handoff package is context for a task, not a second canonical knowledge base.

## Standard task workflow

1. **Frame:** define one research question or bounded deliverable, scope, acceptance criteria, risk, dependencies, and files likely to change.
2. **Package:** create a self-contained assignment from [the handoff template](exports/templates/LLM-HANDOFF-TEMPLATE.md). Include baseline SHA, exact file paths, source links, data timestamps, constraints, and the required return format.
3. **Research:** use [the research handoff](exports/templates/research-handoff.md) where evidence gathering is the primary task. Return a claim ledger and direct source trail.
4. **Challenge:** for consequential or uncertain work, use a separate model session with [the critical-review template](exports/templates/critical-review.md). Prefer an independent first pass before revealing the researcher's conclusion.
5. **Synthesize:** reconcile conflicts, retain unresolved claims as unresolved, and prepare the smallest coherent change proposal.
6. **Implement:** modify canonical files only within the assignment's scope. Preserve source IDs, metadata, cross-links, and existing verified claims.
7. **Validate:** check citations, calculations, tests, links, dependent pages, indexes, and the research log as applicable.
8. **Return:** report findings, exact paths changed, baseline/resulting SHAs, validation results, open questions, and recommended next step.

Do not run every task through every role. Small editorial changes need not use multiple models. Use separate researcher and reviewer sessions for patch-sensitive mechanics, formulas, live economic assumptions, and material strategy recommendations. LLM agreement is not evidence.

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

## Claim and validation discipline

For every material finding, state whether it is supported, contradicted, unresolved, or out of scope. Distinguish a source's statement from independent verification of the underlying game behavior.

For calculations and code, define inputs, units, formulas, rounding, limitations, and reproducible examples. Run the relevant tests whenever the environment permits. Report each check as passed, failed, not run, or not applicable, with the command and environment. Do not claim a test passed merely because code appears correct.

When blocked by user input or unavailable data, write the exact question to the appropriate research-management file and continue with independent work. Do not invent live prices, character skills, structures, or market conditions.

## Upload budget and portable handoffs

For a focused LLM assignment, prefer:

1. `LLM-HANDOFF.md`: assignment, acceptance criteria, baseline SHA, relevant paths, and constraints.
2. `SUPPORTING-DATA.md`: only when numerical inputs or datasets matter.
3. `PRIMARY-SOURCES.md`: only when source excerpts or source-specific instructions are necessary.

Do not upload the entire repository for a narrow task. The packet must be self-contained because another provider or session may not have this conversation's history. Use [the task packet template](exports/templates/LLM-HANDOFF-TEMPLATE.md), [primary sources template](exports/templates/PRIMARY-SOURCES-TEMPLATE.md), and [supporting data template](exports/templates/SUPPORTING-DATA-TEMPLATE.md).

## Current scope

The scope is comprehensive: foundations, T1/T2/T3 production, invention, reactions, planetary industry, sourcing, industrial economics, optimization, market intelligence, tooling, playbooks, and deterministic calculations. The repository contains source-backed draft concepts and computations, but `status: draft` means the content has not necessarily passed independent in-game verification. Consult the research backlog and verification queue before treating a claim as operationally confirmed.

## Local tooling

- `tools/sde/`: download and inspect CCP's current SDE with Python's standard library.
- `tools/esi/`: collect selected public market orders/history, adjusted prices, and industry system indices without EVE SSO credentials.
- `tools/calculations/`: deterministic calculators with reproducible JSON scenarios and standard-library unit tests.
- `.github/workflows/python-tests.yml`: run the calculation test suite on pushes, pull requests, or manual dispatch.

## Format reference

OKF v0.2 canonical specification: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
