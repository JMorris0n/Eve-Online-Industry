---
type: Reference
title: Open Knowledge Format v0.2
description: Canonical format specification used by this repository.
tags:
  - references
  - okf
  - format
generated:
  by: process:starter-scaffold
  at: 2026-11-14T05:30:25Z
status: draft
---

## Canonical source

- Specification: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
- Repository: https://github.com/GoogleCloudPlatform/open-knowledge-format

## Project usage

This repository uses OKF v0.2 as a portable Markdown-plus-YAML convention. The format requires each non-reserved Markdown concept file to contain parseable YAML frontmatter with a non-empty `type`. `index.md` and `log.md` are reserved filenames with their own conventions.

## Maintenance note

Always re-check the canonical specification before adopting new fields or changing conventions. Do not use the frozen `knowledge-catalog/okf` copy as the canonical home.
