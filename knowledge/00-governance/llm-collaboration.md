---
type: Concept
title: LLM Collaboration Protocol
description: A repeatable, human-controlled process for coordinating LLM research, independent review, synthesis, implementation, and handoff.
tags:
  - governance
  - llm
  - workflow
generated:
  by: openai/gpt-6
  at: 2026-11-14T08:45:00Z
status: draft
---

## Operating principle

Treat each LLM session as a replaceable specialist, not as a persistent project owner. The repository is the shared memory and canonical record. A task packet carries the minimum context needed to complete one bounded assignment. The coordinator reconciles outputs, while the human maintainer controls acceptance into canonical knowledge.

Use multiple models when independent review is likely to catch material errors. Do not add model calls merely to create the appearance of rigor. Agreement between models is not independent factual verification.

## Roles

| Role | Responsibility | Required output |
|---|---|---|
| **Coordinator** | Frames the task, selects context, assigns work, tracks dependencies, reconciles results, and maintains project records | Task packet, decisions, integrated change proposal, handoff summary |
| **Primary researcher** | Investigates a bounded question using the best evidence for that claim type | Claim ledger, source trail, limitations, proposed findings |
| **Independent reviewer** | Tries to disprove or qualify findings, checks sources and reasoning independently, and identifies omissions | Severity-ranked issue list and independent conclusion |
| **Technical implementer** | Implements an accepted calculation, parser, test, or documentation change | Minimal patch, reproducible test results, implementation notes |
| **Human maintainer** | Sets objectives and constraints, resolves judgment calls, and accepts or rejects canonical changes | Review decision and approval to integrate |

One model may perform multiple roles for a low-risk task. For consequential, patch-sensitive, economic, or formula-heavy work, separate the researcher and reviewer into distinct sessions. When possible, use different model providers or materially different approaches.

## Task lifecycle

Use this state sequence for substantive tasks:

`queued -> packet-ready -> research -> independent-review -> synthesis -> implementation -> validation -> human-review -> accepted`

A task may also be `blocked`, `deferred`, or `rejected`. Do not leave an item marked complete if its acceptance criteria have not been met.

### 1. Frame one bounded task

The coordinator records:

- **Decision or knowledge gap:** what the work should resolve.
- **Research question:** precise wording that can be answered or explicitly left unresolved.
- **Scope:** included topics, excluded topics, and the files likely to change.
- **Acceptance criteria:** observable conditions that define completion.
- **Risk:** low, medium, or high, based on gameplay impact, economic consequence, volatility, and difficulty of reversal.
- **Dependencies:** upstream facts, data, tools, or user decisions needed.

Prefer one question, one formula, one dataset, or one cohesive documentation change per task. Split broad requests into ordered tasks and parallelize only independent work.

### 2. Build a portable context packet

Start with [LLM-START-HERE.md](../../../LLM-START-HERE.md), then include only the relevant project rules, concept pages, dependencies, source references, and data excerpts.

Every handoff must identify:

- Task ID and task mode: research, review, synthesis, implementation, or audit.
- Repository and baseline commit SHA.
- Exact assignment and acceptance criteria.
- Relevant repository paths, not vague references to prior chat.
- Source URLs, source dates, and retrieval timestamps for volatile data.
- Allowed changes and explicit no-go areas.
- Required return format and validation expectations.

The packet must stand on its own. Do not require the receiving model to infer missing context from another provider's conversation history. Do not upload the whole repository for a narrow assignment. Use `exports/generated/` for local, temporary packets; that directory is ignored by Git. Move accepted, durable knowledge into its canonical location.

### 3. Research with a claim ledger

The primary researcher must separate findings into:

- **Supported:** the cited evidence directly supports the claim.
- **Contradicted:** credible evidence conflicts with the claim.
- **Unresolved:** evidence is incomplete, ambiguous, stale, or inaccessible.
- **Out of scope:** the claim was not investigated.

For each material claim, provide its classification as a mechanic, derived calculation, strategic recommendation, or hypothesis. Cite a stable source URL and identify the supporting section, table, patch note, API field, or in-game observation. Record publication/update date and access/retrieval date when available.

For calculations, define variables, units, formula, rounding, inputs, and an independently reproducible example. For live market or facility values, record region, location, retrieval time, and relevant filters.

A source citation proves what the source says. It does not automatically prove that the source is current, that its interpretation is correct, or that an in-game value applies to every character or facility.

### 4. Run an independent challenge

Use a separate reviewer session for high-risk or material changes. Reduce anchoring by first providing the reviewer with the research question, relevant source links, and acceptance criteria, but not the researcher's final conclusion. Ask the reviewer to determine the answer independently. Then provide the findings and ask for a claim-by-claim comparison.

The reviewer should actively look for:

- A more authoritative or newer source.
- Patch changes, exceptions, hidden conditions, and scope mismatches.
- Incorrect interpretation of source language or API fields.
- Missing variables, dependencies, units, rounding, and edge cases.
- Formula errors reproduced independently.
- Conflicts with adjacent concepts, existing claims, or current data.
- Conclusions that exceed the evidence.

For code, require executable tests or a reproducible manual test. A second model reading code is a useful review, not a substitute for running it. For undocumented game behavior, only a controlled in-game test or sufficiently direct evidence can resolve the mechanic.

Small editorial changes may skip independent review. Record that the review was skipped when the change is consequential enough that the omission matters.

### 5. Reconcile and synthesize

The coordinator reconciles disagreements using the project's [research standards](research-standards.md). Do not average conflicting claims or silently select whichever answer sounds more plausible.

When evidence does not settle a question:

1. Preserve the uncertainty and competing interpretations.
2. Add or update an item in [Open Questions](../10-research-management/open-questions.md) or [Claims Requiring Verification](../10-research-management/claims-requiring-verification.md).
3. Define the evidence or test needed to resolve it.
4. Continue with independent tasks that do not depend on the unresolved answer.

Prepare the smallest coherent set of canonical edits. Preserve existing paths, source IDs, metadata, verified events, and useful cross-links.

### 6. Implement and validate

Before integration, check the following as applicable:

- Claim-level source links and OKF source IDs.
- Correct separation of mechanics, calculations, strategy, and hypotheses.
- Formula dimensions, units, rounding, edge cases, and example arithmetic.
- Current data timestamps, region, filters, and provenance.
- Internal links, relevant indexes, and dependent documents.
- Required code tests, with exact command and result.
- Research backlog, open questions, and chronological log.
- No credentials, SSO tokens, private character exports, or raw SDE archives.

Validation reporting must distinguish **passed**, **failed**, **not run**, and **not applicable**. Never describe an unrun test as successful. Link to the exact CI run or commit check when available. A successful documentation build does not verify EVE mechanics.

### 7. Return control to the maintainer

Every substantive handoff returns:

1. Task ID, baseline SHA, and resulting commit or patch reference.
2. Concise findings and decision-relevant conclusion.
3. Claim ledger with classifications, evidence, and confidence limitations.
4. Files changed and the reason for each change.
5. Validation performed, exact commands, and results.
6. Remaining conflicts, assumptions, and open questions.
7. Recommended next task and any decision required from the maintainer.

The human maintainer decides whether proposed changes are accepted. Direct commits to the primary branch are allowed only when the maintainer has explicitly delegated repository maintenance for the current task. Otherwise, use a branch and pull request or deliver a unified diff. Never force-push.

## Routing work efficiently

| Task type | Minimum useful route | Add independent review when |
|---|---|---|
| Small editorial or link fix | Implement, inspect diff, check links | The change alters meaning or lifecycle status |
| New mechanic or patch-sensitive fact | Research, source check, focused review | It changes eligibility, inputs, outputs, or strategy |
| Formula or economic model | Derive, reproduce numerically, edge-case tests, review | Results materially affect capital or production decisions |
| Code or data parser | Implement, run tests, inspect sample output | Parser assumptions, data schema, or edge cases are uncertain |
| Strategy or optimization | Define objective/constraints, compare scenarios, challenge assumptions | Recommendations depend on volatile data or costly choices |
| Broad audit | Decompose into bounded workstreams, parallelize independent reviews, reconcile centrally | Always, for material conclusions |

## Escalation and blocked work

Do not wait indefinitely for missing input. Record the exact question, why it matters, the affected task, and the default assumption that would be required. Put durable questions in the research-management files. Continue with work that is independent of the missing answer.

If a source is inaccessible, record the URL, the access failure, and an alternate evidence path. If a script cannot be executed in the current environment, provide the exact local command and mark execution as not run.

## Canonical project records

- `LLM-START-HERE.md`: concise onboarding and the shortest path into the workflow.
- `knowledge/00-governance/`: enduring collaboration and evidence rules.
- `exports/templates/`: portable task and review templates.
- `exports/generated/`: local temporary task packets, excluded from Git.
- `knowledge/10-research-management/research-backlog.md`: prioritized work and acceptance criteria.
- `knowledge/10-research-management/open-questions.md`: unresolved questions and evidence needed.
- `knowledge/log.md`: concise chronological record of material corpus changes.
- `knowledge/index.md` and topic indexes: canonical navigation.

Update the canonical source once. Exports and handoff packets should link to that source instead of creating competing copies.
