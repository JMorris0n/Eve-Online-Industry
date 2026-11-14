---
type: Concept
title: Research and Verification Standards
description: Evidence hierarchy, claim classification, source traceability, and verification workflow.
tags:
  - governance
  - research
generated:
  by: process:starter-scaffold
  at: 2026-11-14T05:30:25Z
status: draft
---

## Claim classes

| Class | Meaning | Evidence expectation |
|---|---|---|
| Mechanic | A game rule or system behavior | Current CCP documentation, patch notes, official UI/ESI, or reproducible in-game test |
| Derived calculation | A result calculated from mechanics and explicit inputs | Reproducible formula, units, assumptions, and input provenance |
| Strategic recommendation | Advice for a defined objective | Mechanics plus economic model, constraints, and stated assumptions |
| Hypothesis | A plausible but unverified proposition | Explicitly label as unverified and state what would test it |

## Evidence hierarchy

1. Current CCP official documentation.
2. CCP patch notes and official announcements for changes and historical behavior.
3. In-game UI and official ESI for live or account-specific values.
4. Reproducible player tests for undocumented or ambiguous mechanics.
5. Maintained community databases and wikis.
6. Third-party calculators and tools.
7. Forums, Reddit, and older guides as research leads, not sole authority for current mechanics.

The best source depends on the claim. Official documentation does not establish a live market price, current structure tax, or an individual character's standings.

## Verification workflow

1. State the claim precisely.
2. Find the best available source for that claim type.
3. Record source identity, URL, publication/update date when available, and accessed date in research notes.
4. Check whether the source is current and whether a patch may have changed the rule.
5. Reproduce calculations independently.
6. Record conflicting evidence and test limitations.
7. Add an OKF `verified` event only when an actual independent verification has occurred.

## Citation convention

Use OKF `sources` frontmatter with stable source IDs. Cite claims in the body using Markdown footnotes keyed to those IDs. Do not carry over chat-specific citation tokens as permanent source identifiers.

## Freshness

Volatile claims should have explicit review triggers or an appropriate `stale_after` timestamp. Do not apply an arbitrary freshness deadline to stable conceptual material.
