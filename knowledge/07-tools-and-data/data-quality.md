---
type: Concept
title: Data Quality and Reconciliation
description: Evidence hierarchy, provenance, freshness, normalization, validation, source conflicts, and verification status for the industrial knowledge base.
tags:
  - data
  - quality
  - provenance
  - verification
sources:
  - id: ccp-esi-overview
    resource: https://developers.eveonline.com/docs/services/esi/overview/
    title: ESI Overview | EVE Developer Documentation
  - id: ccp-esi-best-practices
    resource: https://developers.eveonline.com/docs/services/esi/best-practices/
    title: Best Practices for ESI
  - id: ccp-esi-api-explorer
    resource: https://esi.evetech.net/ui/?version=latest
    title: ESI API Explorer
  - id: ccp-sde-docs
    resource: https://developers.eveonline.com/docs/services/static-data/
    title: Static Data Export Documentation
  - id: ccp-sde-rework
    resource: https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data
    title: "Reworking the SDE: a fresh start for static data (2025-09-22)"
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Open Knowledge Format Specification v0.2
generated:
  by: openai/gpt-6
  at: 2026-11-14T09:30:00Z
status: draft
---

## Purpose

Data quality is the control system that prevents incorrect, stale, incomplete, or untraceable information from entering the industrial knowledge base and its calculations. A fact without provenance is not a reliable input; a calculation without reproducible inputs is not an auditable result.

The project uses OKF v0.2 metadata and claim-level citations to preserve source lineage. [^okf-spec]

## Claim classes

Every substantive statement should be classified as one of:

| Claim class | Meaning | Example |
|---|---|---|
| Mechanic | A game rule or behavior | ME research reduces material requirements |
| Derived calculation | A reproducible result from stated inputs and formulas | Expected invention output from success probability |
| Strategic recommendation | Advice conditional on stated assumptions | Use a low-SCI facility if total landed cost is lower |
| Hypothesis | A plausible but unverified explanation or forecast | A product may become more liquid after a patch |

Do not present a derived calculation as a direct CCP mechanic. Do not present a strategic recommendation as universally optimal. Hypotheses must remain visibly provisional.

## Evidence hierarchy

Use evidence appropriate to the claim:

1. Current in-game UI or reproducible in-game behavior for live job quotes, current structure taxes, character-specific eligibility, and operational outcomes.
2. CCP official documentation and patch notes for published mechanics and intended behavior.
3. CCP SDE for static definitions, IDs, recipes, and schematic data.
4. CCP ESI for current supported market, industry, universe, and character state.
5. Reproducible player tests for undocumented or ambiguous mechanics.
6. Maintained community references such as EVE University for detailed skill and operational guidance.
7. Third-party calculators and data services for cross-checking formulas and data.
8. Forums, Reddit, old guides, and videos as investigative leads, not final authority without corroboration.

A source's authority is claim-dependent. CCP documentation may be authoritative for an intended rule but cannot establish today's market price or a character's actual skill state. ESI can provide a current market snapshot but does not by itself explain why a mechanic works.

## Provenance requirements

For every external source, preserve:
- Stable source ID.
- Publisher/maintainer.
- Title.
- Canonical URL.
- Source type.
- Publication/update date where available.
- Access date.
- Claim scope and known limitations.

For every ESI-derived record, preserve:
- Endpoint and parameters.
- Retrieval timestamp.
- ESI compatibility date.
- Expires, ETag, Last-Modified, and pagination metadata where available.
- Region, system, location, character, corporation, and type IDs as applicable.
- Raw response or a stable reference to it.
- Normalization and transformation version.

For every SDE-derived record, preserve:
- SDE build identifier.
- Schema version or changelog reference.
- File/table name.
- Type/schematic/blueprint IDs.
- Extraction timestamp.
- Parser version and transformation rules.

ESI's compatibility date, cache behavior, rate limits, and pagination are part of data provenance. The SDE schema changed substantially in September 2025; do not combine data from incompatible SDE builds without an explicit migration. [^ccp-esi-overview] [^ccp-esi-best-practices] [^ccp-sde-docs] [^ccp-sde-rework]

## Freshness classes

Use freshness appropriate to the data:

| Data | Recommended refresh behavior |
|---|---|
| Market order book | Respect ESI cache expiry; refresh before committing a large trade |
| Market history | Refresh according to endpoint cache and archive update cadence |
| System cost indices | Refresh before comparing or installing jobs |
| Facility tax/service state | Verify in the live Industry window before installation |
| Character skills and active jobs | Refresh when a plan or schedule is generated |
| SDE recipes/types/blueprints | Pin to a specific SDE build; refresh after game data updates |
| CCP support article | Recheck when the concept is revised or patch notes indicate a change |
| Community wiki | Record last-modified/access date and check its warnings/limitations |

A source can be authoritative and still be stale. Record both authority and freshness.

## Normalization rules

1. Use stable IDs as primary keys. Names are display labels and may change.
2. Preserve raw source fields before normalization.
3. Store quantities with explicit units.
4. Store ISK values as decimal/currency values, not binary floating-point approximations where exact reconciliation matters.
5. Keep timestamps in UTC internally; convert to local time only for display.
6. Preserve region, system, and location separately.
7. Distinguish market price, adjusted price, historical average, replacement cost, and opportunity cost.
8. Do not round intermediate calculations unless the game mechanic requires rounding at that specific stage.
9. Record whether a quantity is per run, per job, per batch, per unit, or per cycle.
10. Keep source values separate from derived values.

## Data validation dimensions

| Dimension | Validation question | Example check |
|---|---|---|
| Completeness | Are all required fields present? | Blueprint has type ID, activity, output, and input list |
| Validity | Do values conform to expected schema/range? | Skill level is 0–5 |
| Uniqueness | Are duplicate records handled? | Market order ID unique within snapshot |
| Consistency | Do related records agree? | Schematic inputs and output match the SDE schema |
| Freshness | Is the observation recent enough? | Order book cache has not expired |
| Accuracy | Does the value match a trusted source or test? | Industry quote matches computed fee |
| Lineage | Can the result be traced to inputs and transformations? | Profit result links to market snapshot and job quote |
| Reproducibility | Can the same output be regenerated? | Formula and code version are recorded |

## ESI-specific validation

- Respect Expires and ETag headers.
- Respect the X-Compatibility-Date used for the request.
- Handle HTTP 420 and 429 without tight retry loops.
- Deduplicate paginated records using stable IDs.
- Handle X-Pages cache-expiry overlap and cursor-based record updates.
- Reconstruct zero-trade days when calculating average daily market volume.
- Treat market-history order_count as completed transactions/orders, not current open orders.
- Keep current order-book snapshots separate from daily market history.
- Do not treat adjusted price as a live market quote.
- Check authorization scopes and route access before interpreting an empty result as zero assets or zero orders.

See [ESI and Market Data](esi-and-market-data.md) and [Demand and Liquidity](../06-market-intelligence/demand-and-liquidity.md). [^ccp-esi-api-explorer] [^ccp-esi-best-practices]

## SDE-specific validation

- Pin every dataset to an SDE build.
- Use the current YAML or JSON Lines schema.
- Validate parser output against the schema changelog.
- Preserve stable type, blueprint, schematic, and activity IDs.
- Check input/output quantity direction and unit semantics.
- Compare generated recipes with the in-game Industry/PI interface for representative cases.
- Never silently merge old CSV conversions with the post-September-2025 SDE.

The SDE is a static data source. It does not provide current market prices, character assets, active jobs, or live structure tax rates. [^ccp-sde-docs] [^ccp-sde-rework]

## Source conflict resolution

When two sources disagree:

1. Identify the exact claim and the version/date of each source.
2. Determine whether the disagreement is about intended mechanics, current live state, or a derived interpretation.
3. Check relevant patch notes and the current in-game interface.
4. Reproduce the behavior where practical.
5. Record both claims and the reason one is preferred.
6. If unresolved, preserve the conflict as an open question and avoid presenting either value as certain.

Do not resolve a conflict by majority vote or by choosing the source with the most detailed wording.

## Verification states

The project uses these workflow states:

- **Unverified:** researched or drafted, but not independently checked.
- **Machine-confirmed:** a script or validator confirms schema, arithmetic, referential integrity, or data consistency. This does not prove the game mechanic itself is correct.
- **Human-reviewed:** a person independently checked the claim against the source, current client, or reproducible test.

Model agreement is not independent verification. A document should only receive an OKF verified event when an actual verification action has occurred. [^okf-spec]

## Research-to-publication workflow

1. Define the claim and classify it.
2. Find the best available primary source.
3. Record source metadata and limitations.
4. Draft the concept with claim-level citations.
5. Separate sourced mechanics from derived calculations and recommendations.
6. Run structural and numeric validation.
7. Conduct critical review for contradictions and missing assumptions.
8. Perform independent in-game or source verification where required.
9. Update indexes, source catalogs, and chronological log.
10. Record unresolved questions in the research backlog or verification queue.

## LLM and automation controls

- Treat model-generated content as a proposal until validated.
- Do not allow an LLM to invent sources, IDs, live values, or verification events.
- Require a change summary and complete revised files or unified diff.
- Preserve existing IDs, metadata, cross-links, and verified claims.
- Review source dates and game patches before accepting a change.
- Keep write access and repository commits under explicit user-controlled workflows.
- Store credentials and personal character data outside the public knowledge corpus.

## Related concepts

- [ESI and Market Data](esi-and-market-data.md)
- [Third-Party Industry Tools](third-party-tools.md)
- [Research Standards](../00-governance/research-standards.md)
- [Document Conventions](../00-governance/document-conventions.md)
- [Research Backlog](../10-research-management/research-backlog.md)
- [Claims Requiring Verification](../10-research-management/claims-requiring-verification.md)

[^ccp-esi-overview]: CCP, ESI Overview.
[^ccp-esi-best-practices]: CCP, Best Practices for ESI.
[^ccp-esi-api-explorer]: CCP, ESI API Explorer.
[^ccp-sde-docs]: CCP, Static Data Export Documentation.
[^ccp-sde-rework]: CCP, Reworking the SDE: a fresh start for static data (2025-09-22).
[^okf-spec]: Google Cloud Platform, Open Knowledge Format Specification v0.2.
