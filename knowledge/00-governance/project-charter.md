---
type: Concept
title: Project Charter
description: Mission, scope, principles, and maintenance model for the EVE industrial knowledge base.
tags:
  - governance
  - scope
generated:
  by: process:starter-scaffold
  at: 2026-11-14T05:30:25Z
status: draft
---

## Mission

Maintain a durable, accurate, source-traceable knowledge base that explains EVE Online industry mechanics and supports repeatable economic and operational decisions.

## Scope

The initial scope is comprehensive: industry foundations, blueprints and research, manufacturing, invention, reactions, Tech III production, planetary industry, materials sourcing, industrial economics, optimization, market intelligence, tools, playbooks, and deterministic calculations.

## Principles

- Mechanics are separated from economic models and strategic recommendations.
- Claims are traceable to specific sources or explicitly marked as hypotheses.
- Live market data and personal assets are kept separate from evergreen mechanics.
- LLMs may research and propose edits; human review controls integration.
- One canonical concept per file, with derived handoffs and guides kept separate.
- Prefer simple Markdown and Git over custom infrastructure until a demonstrated need exists.

## Out of scope for the initial build

- A custom database or knowledge-management application.
- Automatic production of final guides before source claims are verified.
- Automatic ingestion of personal assets or market snapshots into evergreen concepts.
- Autonomous commits to the primary branch.

## Success criteria

1. Core concepts are modular, navigable, and source-backed.
2. Important mechanics and calculations can be independently reproduced.
3. LLM handoffs are self-contained and economical in upload/context use.
4. Proposed changes are reviewable through Git diffs.
5. User-facing guides can be generated from the canonical corpus without duplicating its underlying facts.
