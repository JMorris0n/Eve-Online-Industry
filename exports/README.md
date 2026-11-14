# LLM Exports and Handoffs

Start with the [Workflow Quick Start](WORKFLOW-QUICKSTART.md) for the VS Code and PowerShell sequence.

This directory contains task-specific context packages derived from the canonical `knowledge/` bundle. It is the transport layer between separate LLM sessions and providers, not a second source of truth.

## Quick workflow

1. Copy [the LLM handoff template](templates/LLM-HANDOFF-TEMPLATE.md) into `generated/<task-id>/LLM-HANDOFF.md`.
2. Fill in the task ID, mode, risk, baseline commit SHA, exact assignment, scope, acceptance criteria, allowed files, context paths, sources, and expected return format.
3. Add [supporting data](templates/SUPPORTING-DATA-TEMPLATE.md) or [primary source notes](templates/PRIMARY-SOURCES-TEMPLATE.md) only when useful.
4. Assign the relevant role using [LLM role prompts](templates/LLM-ROLE-PROMPTS.md). Use the [research handoff](templates/research-handoff.md) for evidence gathering and the [critical review](templates/critical-review.md) for independent challenge.
5. Return findings in a [change proposal](templates/change-proposal.md). Integrate approved durable knowledge into `knowledge/`.

## Directory rules

- `templates/`: version-controlled reusable templates and prompts.
- `generated/`: temporary local task packets, ignored by Git by default.
- Accepted permanent knowledge belongs in its canonical topic file, not only in an export.
- Do not copy the entire repository or chat transcript into a narrow handoff. Include exact paths and the minimum self-contained context another model needs.
- Include a baseline commit SHA so results can be compared with the repository state that was actually reviewed.
- Never place credentials, EVE SSO tokens, private character data, local caches, or raw SDE archives in a handoff.
