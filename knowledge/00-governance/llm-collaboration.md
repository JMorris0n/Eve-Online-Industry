---
type: Concept
title: LLM Collaboration Protocol
description: Rules for research, critical review, change proposals, and human-controlled integration.
tags:
  - governance
  - llm
generated:
  by: process:starter-scaffold
  at: 2026-11-14T05:30:25Z
status: draft
---

## Roles

- **Research model:** locates authoritative sources and extracts mechanics.
- **Analytical model:** derives formulas, expected values, and economic implications.
- **Critical reviewer:** identifies contradictions, missing dependencies, stale claims, and unsupported assumptions.
- **Synthesis model:** proposes the smallest coherent update to canonical documents.
- **Human maintainer:** decides what enters the canonical branch.

## Required output from an LLM task

1. Executive finding.
2. Exact claims added, corrected, or rejected.
3. Sources with stable URLs and relevant sections or dates.
4. Formulas with named variables and assumptions.
5. Worked examples where useful.
6. Conflicts, limitations, and unresolved questions.
7. Proposed file changes or unified diff.
8. A concise change summary.

## Change rules

- Never replace the entire corpus for a narrow assignment.
- Preserve existing source IDs and cross-links unless there is a documented reason to change them.
- Never mark content `stable` or add `verified` based only on model agreement.
- Do not turn a hypothesis into a mechanic without evidence.
- Keep proposed edits isolated in a branch or patch until reviewed.
