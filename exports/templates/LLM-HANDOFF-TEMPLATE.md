# LLM-HANDOFF.md

> Copy this file into `exports/generated/<task-id>/LLM-HANDOFF.md`, fill every relevant field, and send it with only the supporting context listed below. The generated directory is ignored by Git.

## Task identity

- Task ID:
- Status: queued / packet-ready / research / independent-review / synthesis / implementation / validation / human-review / accepted / blocked / deferred / rejected
- Task mode: research / review / synthesis / implementation / audit
- Risk: low / medium / high
- Date created:
- Coordinator:
- Repository:
- Branch:
- Baseline commit SHA:

## Objective

[What decision or knowledge gap should this task resolve?]

## Exact assignment

[One precise question or bounded deliverable. State what a successful answer must establish.]

## Scope

### In scope
- 

### Out of scope
- 

### Acceptance criteria

- [ ] 
- [ ] 
- [ ] 

## Permitted changes

- Files or directories that may be changed:
- Files that must not be changed:
- May the assignee edit files directly? yes / no
- Required delivery: findings / complete revised file(s) / unified diff / code and tests

Do not expand scope without recording the reason and requesting approval where needed.

## Context to load

Start with `LLM-START-HERE.md`. Load only what is needed:

- Canonical project rules:
- Relevant knowledge pages:
- Dependencies or adjacent concepts:
- Existing implementation or tests:
- Research backlog / open question:
- Supporting excerpts or data:

Use exact repository-relative paths and identify the relevant sections. Do not assume the receiving model can access another provider's chat history.

## Sources and data

- Primary source URLs:
- Relevant sections or source IDs:
- Publication/update dates:
- Data retrieval timestamp and timezone:
- Region, system, or market location:
- Filters, scope, and units:
- Known limitations or conflicts:

[Use `PRIMARY-SOURCES.md` and/or `SUPPORTING-DATA.md` when the source or data details do not fit here.]

## Required method

1. Inspect the supplied context and relevant canonical files.
2. Separate mechanics, derived calculations, strategic recommendations, and hypotheses.
3. Prefer current CCP documentation, patch notes, official UI/ESI, and reproducible tests according to the claim type.
4. Attach evidence to each material claim. Do not invent citations, dates, prices, data, or test results.
5. State assumptions, uncertainty, conflicts, exclusions, and evidence gaps.
6. Make the smallest change consistent with the assignment.
7. Do not mark a claim verified based on model agreement.
8. If blocked, record the exact missing input and continue with independent work.

## Required return format

1. **Finding:** concise decision-relevant result.
2. **Claim ledger:** claim, class, status (supported / contradicted / unresolved / out of scope), evidence, limitations.
3. **Sources:** stable URL, publisher/title, relevant section, source date, access date.
4. **Calculation or test:** formula, variables, units, assumptions, rounding, reproducible example.
5. **Files changed or proposed:** path, reason, change summary.
6. **Validation:** exact command/environment and passed, failed, not run, or not applicable.
7. **Unresolved items:** question, why it matters, evidence needed.
8. **Next handoff:** recommended role, task, and dependencies.

## Constraints and no-go areas

- Preserve existing source IDs, paths, metadata, verified events, and cross-links unless a documented correction is necessary.
- Do not rewrite unrelated files or duplicate canonical facts in exports.
- Do not treat LLM consensus as factual verification.
- Do not commit EVE SSO tokens, refresh tokens, client secrets, private character data, local caches, or raw SDE archives.
- Do not commit to the primary branch unless direct maintenance has been explicitly delegated.
- Do not report tests as passing unless they were actually run and passed.
