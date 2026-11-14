---
type: Concept
title: Tool and Format Documentation
description: Catalog of technical specifications and documentation used by the repository's OKF, SDE, ESI, and local Python tooling.
tags:
  - references
  - tools
  - specifications
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Open Knowledge Format Specification v0.2
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: ESI Overview | EVE Developer Documentation
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-esi-versioning-blog
    resource: https://developers.eveonline.com/blog/changing-versions-v42-was-getting-out-of-hand
    title: "Changing versions: /v42/ was getting out of hand"
  - id: ccp-esi-rate-limit-blog
    resource: https://developers.eveonline.com/blog/hold-your-horses-introducing-rate-limiting-to-esi
    title: "Hold your horses: introducing rate limiting to ESI"
  - id: ccp-esi-openapi-blog
    resource: https://developers.eveonline.com/blog/changing-specs-from-swagger-to-openapi
    title: "Changing specs: from Swagger to OpenAPI"
  - id: ccp-esi-cursor-pagination
    resource: https://developers.eveonline.com/docs/services/esi/pagination/cursor-based/
    title: Cursor-Based Pagination
  - id: ccp-esi-xpages-pagination
    resource: https://developers.eveonline.com/docs/services/esi/pagination/x-pages/
    title: X-Pages Pagination
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
  - id: ccp-sde-rework
    resource: https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data
    title: "Reworking the SDE: a fresh start for static data"
  - id: python-urllib-docs
    resource: https://docs.python.org/3/library/urllib.request.html
    title: Python urllib.request documentation
  - id: python-zipfile-docs
    resource: https://docs.python.org/3/library/zipfile.html
    title: Python zipfile documentation
generated:
  by: openai/gpt-6
  at: 2026-11-14T11:30:00Z
status: draft
---

## Catalog policy

Add sources only after confirming that the URL resolves and the source is relevant. Prefer direct documentation and canonical specifications over search result URLs.

For each source, preserve its stable ID, publisher, title, canonical URL, source type, publication/update date when available, access date, and scope/limitations. Concept documents should cite the specific source that supports each claim rather than relying on this catalog as a blanket citation.

## Format and knowledge structure

| Source ID | Documentation | How this project uses it |
|---|---|---|
| `okf-spec` | [Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) | Required metadata, reserved index/log files, source lineage, lifecycle status, and verification events |

OKF is the format contract for the canonical `knowledge/` bundle. The project-specific conventions in `00-governance/` supplement the specification but do not replace it. [^okf-spec]

## ESI documentation

| Source ID | Documentation | How this project uses it |
|---|---|---|
| `ccp-esi-overview` | [ESI Overview](https://developers.eveonline.com/docs/services/esi/overview/) | Endpoint conventions, response headers, and API fundamentals |
| `ccp-esi-best-practices` | [Best Practices for ESI](https://developers.eveonline.com/docs/services/esi/best-practices/) | Cache handling, User-Agent, rate limits, and request behavior |
| `ccp-esi-api-explorer` | [ESI API Explorer](https://esi.evetech.net/ui/?version=latest) | Current route schemas, parameters, and response models |
| `ccp-esi-versioning-blog` | [Changing versions: /v42/ was getting out of hand](https://developers.eveonline.com/blog/changing-versions-v42-was-getting-out-of-hand) | Compatibility-date versioning and API migration |
| `ccp-esi-rate-limit-blog` | [Hold your horses: introducing rate limiting to ESI](https://developers.eveonline.com/blog/hold-your-horses-introducing-rate-limiting-to-esi) | Floating-window rate limiting and HTTP 429 behavior |
| `ccp-esi-openapi-blog` | [Changing specs: from Swagger to OpenAPI](https://developers.eveonline.com/blog/changing-specs-from-swagger-to-openapi) | OpenAPI specification and API schema publication |
| `ccp-esi-cursor-pagination` | [Cursor-Based Pagination](https://developers.eveonline.com/docs/services/esi/pagination/cursor-based/) | Cursor-based pagination for supported routes |
| `ccp-esi-xpages-pagination` | [X-Pages Pagination](https://developers.eveonline.com/docs/services/esi/pagination/x-pages/) | Page-number pagination, X-Pages, and cache-expiry overlap |

The project collector currently uses public read-only routes. It pins an explicit X-Compatibility-Date, respects Expires/ETag, follows X-Pages for market orders, honors Retry-After, and stops on HTTP 420 error-limit responses. See [tools/esi](../../tools/esi/README.md). [^ccp-esi-overview] [^ccp-esi-best-practices] [^ccp-esi-xpages-pagination]

## Static Data Export documentation

| Source ID | Documentation | How this project uses it |
|---|---|---|
| `ccp-sde-docs` | [Static Data Export](https://developers.eveonline.com/docs/services/static-data/) | Download URLs, JSONL/YAML formats, latest build manifest, and schema files |
| `ccp-sde-rework` | [Reworking the SDE: a fresh start for static data](https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data) | Current SDE data model and schema transition |

The SDE is the source for static type, blueprint, reaction, and planetary schematic definitions. It is not a source for live market orders, character assets, or current facility taxes. See [tools/sde](../../tools/sde/README.md). [^ccp-sde-docs] [^ccp-sde-rework]

## Local Python tooling references

| Source ID | Documentation | How this project uses it |
|---|---|---|
| `python-urllib-docs` | [urllib.request](https://docs.python.org/3/library/urllib.request.html) | Standard-library HTTP requests and response handling |
| `python-zipfile-docs` | [zipfile](https://docs.python.org/3/library/zipfile.html) | SDE archive validation and safe extraction |

The local scripts intentionally use Python's standard library to avoid external dependency drift. They are acquisition/inspection helpers, not a replacement for source review or in-game verification. [^python-urllib-docs] [^python-zipfile-docs]

## Project-local documentation

- [SDE downloader and inspector](../../tools/sde/README.md)
- [Public ESI collector](../../tools/esi/README.md)
- [Data Quality and Reconciliation](../07-tools-and-data/data-quality.md)
- [ESI and Market Data](../07-tools-and-data/esi-and-market-data.md)

## Source limitations

Documentation can change independently of the game client. Record the date checked and compatibility date used when updating parsers or API clients. Do not infer live endpoint behavior from an old blog post if the current API Explorer or current service documentation disagrees.

[^okf-spec]: Google Cloud Platform, Open Knowledge Format Specification v0.2.
[^ccp-esi-overview]: CCP, ESI Overview.
[^ccp-esi-best-practices]: CCP, Best Practices for ESI.
[^ccp-esi-api-explorer]: CCP, ESI API Explorer.
[^ccp-esi-versioning-blog]: CCP Developer Blog, Changing versions: /v42/ was getting out of hand (2025-07-10).
[^ccp-esi-rate-limit-blog]: CCP Developer Blog, Hold your horses: introducing rate limiting to ESI (2025-10-07).
[^ccp-esi-openapi-blog]: CCP Developer Blog, Changing specs: from Swagger to OpenAPI (2025-07-22).
[^ccp-esi-cursor-pagination]: CCP Developer Documentation, Cursor-Based Pagination.
[^ccp-esi-xpages-pagination]: CCP Developer Documentation, X-Pages Pagination.
[^ccp-sde-docs]: CCP, Static Data Export documentation.
[^ccp-sde-rework]: CCP Developer Blog, Reworking the SDE: a fresh start for static data (2025-09-22).
[^python-urllib-docs]: Python Software Foundation, urllib.request documentation.
[^python-zipfile-docs]: Python Software Foundation, zipfile documentation.
