# LLM Workflow Quick Start

This is the practical VS Code and PowerShell path for moving one task between ChatGPT, Claude, Gemini, or another model. The repository is the shared memory. Each model receives a bounded handoff, not the full conversation history.

## 1. Start from a clean, known repository state

Open the repository root in VS Code. In the integrated PowerShell terminal:

```powershell
git status --short
git rev-parse HEAD
```

Resolve unexpected local changes before starting. Record the commit SHA in the task packet so every model knows which repository state it reviewed.

For work that should not go directly to the primary branch:

```powershell
git switch -c task/IND-YYYYMMDD-001
```

Use a branch and pull request by default. Direct commits to the primary branch require explicit maintainer delegation.

## 2. Create a task packet

Choose one precise question or bounded deliverable. Use a task ID such as `IND-20261114-001`.

```powershell
$TaskId = "IND-20261114-001"
$TaskDir = "exports/generated/$TaskId"
New-Item -ItemType Directory -Force -Path $TaskDir | Out-Null
Copy-Item "exports/templates/LLM-HANDOFF-TEMPLATE.md" "$TaskDir/LLM-HANDOFF.md"
```

Fill out the packet with:

- The task question, objective, scope, exclusions, and acceptance criteria.
- Task mode and risk.
- Repository branch and baseline commit SHA.
- Exact canonical file paths and relevant dependencies.
- Source URLs, relevant sections, dates, and data retrieval timestamps.
- Permitted edits, no-go areas, and expected return format.

Use the [supporting data template](templates/SUPPORTING-DATA-TEMPLATE.md) for numerical inputs and the [primary sources template](templates/PRIMARY-SOURCES-TEMPLATE.md) when a source packet is needed. Do not copy the entire repository into the task folder.

## 3. Assign the right model role

Open [LLM role prompts](templates/LLM-ROLE-PROMPTS.md) and select only the stage needed:

| Work | Model role | Packet to send |
|---|---|---|
| Break a broad request into tasks | Coordinator | User request, onboarding, backlog |
| Establish facts or resolve a mechanic | Primary researcher | Task packet, relevant concepts, source links |
| Challenge important findings | Independent reviewer | Task question, acceptance criteria, sources; hide the research conclusion during the first pass |
| Reconcile findings and prepare edits | Synthesizer / integrator | Task packet, research findings, review findings, current repository files |

For high-risk work, use a separate reviewer session. Prefer a different provider when convenient. Ask the reviewer to determine the answer independently before seeing the researcher's conclusion, then ask for a claim-by-claim comparison.

For small editorial fixes, skip the multi-model stages and use a focused implementation plus validation. Do not use model count as a proxy for evidence quality.

## 4. Integrate the smallest coherent change

Before editing, inspect the current target files again. Reconcile source conflicts instead of silently choosing one. Preserve existing source IDs, OKF metadata, verified events, and useful links.

For unresolved questions, update the relevant file in `knowledge/10-research-management/`. Continue work that does not depend on the missing answer.

Update these records when the task materially changes the knowledge base:

- Canonical concept or playbook in `knowledge/`.
- Relevant topic index and `knowledge/index.md` when navigation changes.
- `research-backlog.md` and/or `open-questions.md`.
- `knowledge/log.md` for a notable corpus-level change.

## 5. Run one local validation command

From the repository root:

```powershell
py -3 tools/validation/run_all.py
git diff --check
git diff --stat
git status --short
```

The validation runner executes the calculation tests, validation-tool tests, and local Markdown link scan. It returns a non-zero exit code if any check group fails.

Check the exact GitHub Actions run for the commit being reviewed. Do not use an older green run to claim that a newer commit passed. Record tests as passed, failed, not run, or not applicable. This local workflow does not independently verify live EVE mechanics, current prices, or in-game job quotes.

## 6. Return a complete handoff

Use [the change-proposal template](templates/change-proposal.md). Include:

- Task ID, baseline SHA, resulting branch/commit, and files changed.
- Findings and the claim-level evidence trail.
- Research/review conflicts and how they were resolved.
- Exact validation commands and outcomes.
- Open questions and the next useful handoff.

The next model should be able to continue from the task packet, canonical repository files, and recorded result without needing this conversation.

## Short decision rule

- **Low risk, editorial:** implement, inspect diff, validate.
- **Medium risk, source-backed concept:** research, focused review, synthesize, validate.
- **High risk, formula, patch-sensitive mechanic, or economic decision:** research, independent first-pass review, reproduce calculations or tests, synthesize, validate, maintainer acceptance.
