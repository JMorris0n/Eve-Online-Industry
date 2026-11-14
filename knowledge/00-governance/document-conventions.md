---
type: Concept
title: Document Conventions
description: Naming, metadata, linking, document structure, and lifecycle conventions.
tags:
  - governance
  - documentation
generated:
  by: process:starter-scaffold
  at: 2026-11-14T05:30:25Z
status: draft
---

## File naming

- Use lowercase kebab-case paths.
- Use one cohesive concept per file.
- Prefer descriptive nouns for mechanics and models, and action-oriented names for playbooks.

## Concept body structure

Use only the sections that materially help the concept:

- Summary
- Core Mechanics
- Inputs and Outputs
- Formulas
- Dependencies
- Economic Implications
- Operational Considerations
- Limitations and Exceptions
- Examples
- Related Concepts
- Sources

## Metadata

- `type` is required by OKF.
- Use a descriptive type such as `Mechanic`, `Model`, `Playbook`, `Reference`, `Computation`, or `Question`.
- `title`, `description`, and `tags` are recommended.
- Use `generated` for provenance and `verified` only for actual verification events.
- Use `status: draft`, `stable`, or `deprecated` as a project lifecycle convention.

## Links

Use relative Markdown links to related concepts. Broken links should be repaired during review, but do not silently remove useful relationships.

## Tables and formulas

Define every variable, unit, and scope. Keep the formula separate from a worked example. State rounding behavior and any assumptions about in-game settings.
