---
type: Concept
title: ESI and Market Data
description: EVE Swagger Interface architecture, authentication, compatibility dates, caching, rate limits, pagination, market/industry endpoints, and SDE separation.
tags:
  - esi
  - api
  - market-data
  - sde
sources:
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: ESI Overview | EVE Developer Documentation
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-esi-versioning-blog
    resource: https://developers.eveonline.com/blog/changing-versions-v42-was-getting-out-of-hand
    title: "Changing versions: /v42/ was getting out of hand (published 2025-07-10)"
  - id: ccp-esi-rate-limit-blog
    resource: https://developers.eveonline.com/blog/hold-your-horses-introducing-rate-limiting-to-esi
    title: "Hold your horses: introducing rate limiting to ESI (published 2025-10-07)"
  - id: ccp-esi-openapi-blog
    resource: https://developers.eveonline.com/blog/changing-specs-from-swagger-to-openapi
    title: "Changing specs: from Swagger to OpenAPI (published 2025-07-22)"
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
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
    title: "Reworking the SDE: a fresh start for static data (published 2025-09-22)"
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:20:00Z
status: draft
---

## Purpose

The EVE Swagger Interface (ESI) is CCP's official REST API for third-party applications. It provides live and character-specific game data, while the Static Data Export (SDE) provides static definitions such as item types, blueprints, recipes, and planetary schematics. A reliable industrial data pipeline uses both: SDE for stable definitions and ESI for current state. [^ccp-esi-overview] [^ccp-sde-docs]

## ESI architecture and data classes

ESI endpoints are described in CCP's API Explorer. Some endpoints are public; others require EVE Single Sign-On (SSO) authentication and specific OAuth scopes. The API Explorer is the source of truth for the current route, required scopes, parameters, response schema, and endpoint behavior. [^ccp-esi-overview] [^ccp-esi-api-explorer]

| Data class | Example resources | Typical access |
|---|---|---|
| Public market data | Regional orders, market history, adjusted/average prices | Public |
| Public industry data | System cost indices | Public |
| Universe/static lookup | Types, groups, regions, systems, stations | Public |
| Character state | Skills, skill queue, assets, active industry jobs, PI colonies | SSO + route-specific scopes |
| Corporation state | Corporation assets, industry jobs, structures, wallets | SSO + corporation role and route-specific scopes |
| Structure market data | Orders in a player-owned structure | Route-specific access/authorization |

Do not assume a route is public or that a character token grants all scopes. The current API Explorer lists the exact authorization requirement for each endpoint. Request only the scopes needed for the operation. [^ccp-esi-overview]

## Compatibility dates and API versioning

CCP changed ESI's versioning strategy in July 2025. New routes no longer rely on version numbers embedded in URL paths. Instead, the application can pin its API behavior with an ISO date using the X-Compatibility-Date request header or the compatibility_date query parameter. Existing versioned URLs remain supported for the foreseeable future, but new routes use compatibility dates. [^ccp-esi-versioning-blog]

Recommended request practice:

```http
X-Compatibility-Date: YYYY-MM-DD
User-Agent: EveIndustrialKnowledge/1.0 (contact: your-contact)
```

The compatibility date is a reviewed API contract, not simply a request timestamp. Pin it to a date that the client has tested. If no compatibility date is supplied, ESI uses the oldest available compatibility date. Future dates are rejected. The API compatibility date rolls over at downtime, 11:00 UTC. The response includes the compatibility date ESI matched. [^ccp-esi-overview] [^ccp-esi-versioning-blog]

For this project, store the compatibility date with every collected dataset and update it deliberately after reviewing the ESI changelog and testing schema changes.

## API specification format

CCP announced the transition from Swagger 2.0 to OpenAPI 3.0/3.1 in July 2025. New updates are published through the OpenAPI specification and the current API Explorer; the older Swagger specification is read-only. New integrations should use the current OpenAPI schema rather than generating clients from old Swagger artifacts. [^ccp-esi-openapi-blog]

## Caching and request discipline

ESI uses cache headers to indicate when a response should be refreshed. A client should:
- Respect the Expires header and not request a resource again before its cache expires.
- Store ETags and use conditional requests where supported.
- Store Last-Modified and other provenance headers.
- Avoid repeatedly downloading unchanged resources.
- Use bounded retries for transient failures.
- Include a meaningful User-Agent identifying the application and contact information.

The cache window is endpoint-specific. Do not hardcode one universal TTL for market orders, market history, system indices, or character data. [^ccp-esi-best-practices]

## Rate limits and error limits

CCP announced the introduction of ESI rate limiting in October 2025, with a floating-window system being rolled out across routes. As of this project date, integrations must treat rate limits as part of normal API behavior. Use response headers and the current developer documentation rather than assuming a fixed global requests-per-second limit. [^ccp-esi-rate-limit-blog]

Recommended handling:
- HTTP 429: honor Retry-After and retry within a bounded policy.
- HTTP 420: stop requests until the ESI error-limit window resets; do not retry in a tight loop.
- HTTP 5xx: bounded exponential backoff with jitter.
- HTTP 4xx other than transient rate-limit responses: inspect the request, scope, compatibility date, and route contract before retrying.
- Authentication failures: refresh/re-authorize through SSO; never repeatedly submit invalid tokens.

A client must not attempt to evade rate limits by rotating IP addresses, tokens, or endpoints. Respect CCP's service rules and ESI error-limit behavior. [^ccp-esi-rate-limit-blog] [^ccp-esi-best-practices]

## Pagination

ESI does not use one pagination scheme for every endpoint. The API specification identifies the mechanism for each route.

### X-Pages pagination

Traditional page-based routes use a page parameter starting at 1 and return an X-Pages header with the total number of pages. If the cache expires while fetching different pages, results can overlap or duplicate. Use a stable cache window, deduplicate records by stable ID, and avoid beginning a multi-page collection near expiry. [^ccp-esi-xpages-pagination]

### Cursor-based pagination

Some newer routes use before/after cursor tokens. Treat tokens as opaque values and pass them back unchanged. Cursor results are ordered by creation/modification time. Records may appear more than once across pages because they were modified or because of caching; deduplicate by stable record ID and prefer the newest record when using the after cursor. [^ccp-esi-cursor-pagination]

### From-ID pagination

Some routes use a from_id parameter to page backward through records. Follow the route-specific API description and stop condition; do not assume from_id is interchangeable with X-Pages or cursor tokens.

## ESI endpoints relevant to industrial operations

The following route families are useful starting points. Exact parameters, scopes, and response fields must be verified in the current API Explorer.

| Endpoint family | Use |
|---|---|
| GET /markets/{region_id}/orders/ | Current regional buy/sell order book |
| GET /markets/{region_id}/history/ | Daily item market history |
| GET /markets/prices/ | Adjusted and average prices |
| GET /industry/systems/ | Activity-specific system cost indices |
| GET /characters/{character_id}/skills/ | Character skill levels and skill points |
| GET /characters/{character_id}/skillqueue/ | Current skill queue |
| GET /characters/{character_id}/industry/jobs/ | Character industry job state |
| GET /characters/{character_id}/assets/ | Character asset inventory |
| GET /characters/{character_id}/planets/ | Character PI colony list |
| GET /universe/types/{type_id}/ | Item type metadata |
| GET /markets/structures/{structure_id}/ | Market orders in an Upwell structure, subject to authorization |

Some endpoints are paginated, some cached, and some require scopes. Use the current OpenAPI schema to confirm the exact response and scope before implementation. [^ccp-esi-api-explorer]

## SDE versus ESI

| Concern | SDE | ESI |
|---|---|---|
| Item type names and IDs | Yes | Lookup routes can return metadata |
| Blueprint/activity definitions | Yes | Not a complete substitute |
| PI schematics and recipes | Yes | No |
| Current market orders | No | Yes |
| Market history | No | Yes |
| Current system cost indices | No | Yes |
| Character skills and assets | No | Authenticated routes |
| Current facility access/service state | Partial/static definitions only | Route coverage varies; verify in client |

CCP reworked the SDE in September 2025 and changed the format/schema. The current SDE is distributed in JSON Lines and YAML formats. Older converted CSV packages and parsers may not be compatible. Record the SDE build identifier, schema version, and extraction date whenever generating derived data. [^ccp-sde-docs] [^ccp-sde-rework]

## Recommended data architecture

Use three layers:

1. **Raw source layer:** original SDE files and raw ESI responses, retained with provenance.
2. **Normalized layer:** stable type IDs, blueprint IDs, schematic IDs, system IDs, region IDs, and normalized market/job/character records.
3. **Derived layer:** cost calculations, throughput models, product rankings, and market analytics.

Each data record should preserve:
- Source and endpoint.
- Retrieval timestamp.
- ESI compatibility date.
- ESI cache expiry, ETag, and Last-Modified where available.
- SDE build and schema version where applicable.
- Region/system/location/type IDs.
- Transformations and assumptions.
- Validation status.

Do not overwrite raw source data with normalized or calculated values. Derived data should be reproducible from the raw inputs and transformation version.

## Security and credentials

- Use EVE SSO OAuth for authenticated data.
- Request only the required scopes.
- Keep access/refresh tokens outside the Git repository.
- Never place tokens, client secrets, or authorization headers in Markdown, logs, source control, or LLM handoff packages.
- Prefer read-only scopes for knowledge-base collection.
- Do not call state-changing ESI routes unless a separate, explicit workflow requires them and the user authorizes the action.
- Treat character/corporation assets and wallet information as private operational data.

## Recommended initial integration

The local SDE acquisition helper is documented in [tools/sde/README.md](../../tools/sde/README.md). It downloads the current CCP archive, records its build/hash provenance, and inspects the archive layout before a parser is written. A public, read-only ESI collector is documented in [tools/esi/README.md](../../tools/esi/README.md); it collects market orders/history, adjusted prices, and system indices while respecting compatibility dates, cache headers, and rate limits.

The first ESI integration should remain read-only and focus on:
1. Public regional market orders and history.
2. Adjusted prices.
3. System cost indices.
4. Universe type and location lookups.
5. Optional authenticated character skills, assets, and active industry jobs after a clear need and explicit scope review.

This provides enough information to build market and installation-cost models without immediately introducing write access or broad account permissions.

## Related concepts

- [Market Mechanics](../06-market-intelligence/market-mechanics.md)
- [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md)
- [Price Analysis](../06-market-intelligence/price-analysis.md)
- [Data Quality](data-quality.md)
- [Third-Party Tools](third-party-tools.md)
- [Static Data Export and Planetary Commodities](../03-materials-and-sourcing/planetary-commodities.md)

[^ccp-esi-overview]: CCP, EVE Developer Documentation, ESI Overview.
[^ccp-esi-best-practices]: CCP, EVE Developer Documentation, Best Practices for ESI.
[^ccp-esi-versioning-blog]: CCP, Changing versions: /v42/ was getting out of hand (2025-07-10).
[^ccp-esi-rate-limit-blog]: CCP, Hold your horses: introducing rate limiting to ESI (2025-10-07).
[^ccp-esi-openapi-blog]: CCP, Changing specs: from Swagger to OpenAPI (2025-07-22).
[^ccp-esi-api-explorer]: CCP, ESI API Explorer (accessed 2026-11-14).
[^ccp-esi-cursor-pagination]: CCP, Cursor-Based Pagination documentation.
[^ccp-esi-xpages-pagination]: CCP, X-Pages Pagination documentation.
[^ccp-sde-docs]: CCP, Static Data Export documentation.
[^ccp-sde-rework]: CCP, Reworking the SDE: a fresh start for static data (2025-09-22).
