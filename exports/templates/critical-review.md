# Critical Review Handoff

## Review target

- Task ID:
- Baseline commit SHA:
- Files, claims, formulas, dataset, or proposed change:
- Risk: low / medium / high

## Review sequence

**Independent pass first:** receive the assignment, acceptance criteria, and relevant source links. Determine the answer independently before reading the researcher's conclusion where practical.

**Comparison pass second:** inspect the researcher's claim ledger and proposed edits. Compare each material claim against your independent result. Identify where the researcher's conclusion is unsupported, incomplete, stale, or stronger than the evidence.

The goal is to find defects, not to agree with the primary researcher or rewrite the whole knowledge base.

## Audit checklist

- Are factual claims supported by appropriate, current sources?
- Does a primary source directly support the claim, or is the claim inferred?
- Are patch-sensitive mechanics current?
- Are source publication dates and retrieval timestamps clear?
- Are scope, exceptions, facility, activity, region, character, or skill conditions omitted?
- Are formulas dimensionally and algebraically correct?
- Are variables, units, operation order, rounding, and assumptions defined?
- Are inputs, outputs, prerequisites, and dependencies complete?
- Are examples independently recalculated?
- Are code tests executed, or are they merely proposed?
- Are mechanics separated from strategic advice?
- Are citations attached to the claims they support?
- Are conclusions stronger than the evidence allows?
- Are there duplicated or contradictory claims elsewhere?
- Would a controlled in-game test or live data snapshot change the conclusion?

## Required output

For each issue, provide:

- Severity: critical / major / minor / informational.
- File and section.
- Exact claim or omission.
- Why it is a problem.
- Independent evidence or calculation.
- Recommended correction.
- Whether more research, code execution, or an in-game test is required.

Finish with:

1. **Independent conclusion:** agree / agree with qualification / disagree / unable to determine.
2. **Highest-risk issues:** prioritized.
3. **Claim-by-claim comparison:** supported, contradicted, or unresolved.
4. **Missing evidence or tests:** exact next action.
5. **Acceptance recommendation:** accept / revise / reject / defer, with reasons.

Do not mark a claim verified solely because multiple models reach the same conclusion.
