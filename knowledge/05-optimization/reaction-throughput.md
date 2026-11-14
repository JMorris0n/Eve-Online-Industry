---
type: Concept
title: Reaction Throughput
description: Reaction slot utilization, formula output rates, cycle time, reactor compatibility, material demand, and reaction-chain bottlenecks.
tags:
  - optimization
  - reactions
  - throughput
sources:
  - id: ccp-reactions
    resource: https://support.eveonline.com/hc/en-us/articles/115005405785-Reactions
    title: Reactions | EVE Online Support (updated 2024-08-29)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-service-modules
    resource: https://support.eveonline.com/hc/en-us/articles/207574929-Service-Modules
    title: Service Modules | EVE Online Support (updated 2024-08-29)
  - id: eveuni-reactions
    resource: https://wiki.eveuniversity.org/Reactions
    title: Reactions | EVE University Wiki (last modified 2025-06-22)
  - id: eveuni-resource-skills
    resource: https://wiki.eveuniversity.org/Skills:Resource_Processing
    title: Skills: Resource Processing | EVE University Wiki
  - id: eve-reactions-calculator-method
    resource: https://reactions.coalition.space/about
    title: EVE Reactions Calculator methodology
generated:
  by: openai/gpt-6
  at: 2026-11-14T07:50:00Z
status: draft
---

## Purpose

Reaction throughput measures how quickly a character and refinery can convert reaction inputs into outputs. The limiting factors include Reaction job slots, formula output and duration, reactor-family compatibility, facility role bonuses and rigs, raw input supply, fuel blocks, capital, and downstream demand.

Reaction jobs form their own job pool, independent from Manufacturing and Science. A character can therefore run reaction jobs while separately manufacturing components or conducting research, provided each pool has available slots. [^ccp-activities-jobs]

## Reaction job-slot capacity

The Reaction slot formula is:

```text
Reaction slots
  = 1 + Mass Reactions level + Advanced Mass Reactions level
```

The base capacity is one slot. Mass Reactions and Advanced Mass Reactions each add one slot per level, giving a theoretical maximum of 11 concurrent Reaction jobs at both skills V. Advanced Mass Reactions requires Mass Reactions V. [^eveuni-resource-skills] [^eveuni-reactions]

The Reaction slot-hour budget over H days is:

```text
Available Reaction slot-hours
  = Reaction slots × 24 × H
```

Reaction job capacity is separate from Manufacturing and Science capacity. Do not add the three pools together when estimating how many reaction jobs can run.

## Formula output and throughput

A Reaction Formula defines its input quantities, output quantity, fuel-block requirement, and base time. Unlike BPOs, Reaction Formulas cannot be researched, copied, or invented. Each formula must be evaluated from its own recipe and reactor family. [^ccp-reactions] [^eveuni-reactions]

For one reaction job:

```text
Reaction output units
  = formula output per run × job runs

Reaction input quantity for material i
  = formula input quantity i per run × job runs

Reaction fuel requirement
  = formula fuel blocks per run × job runs
```

The formula's actual values are authoritative. Do not assume all reactions use the same batch size, fuel quantity, or output volume.

For a job producing Q output units in T hours:

```text
Output rate per slot-hour = Q / T

Input demand rate for material i
  = total material i required / T

Fuel demand rate
  = total fuel blocks required / T
```

For S continuously utilized Reaction slots, a simplified theoretical output per day is:

```text
Theoretical output per day
  = S × 24 × (Q / T)
```

This assumes all slots can be continuously reinstalled, all required inputs are available, the compatible reactor service remains online, and the output can be moved or consumed. Use the actual Industry quote for job duration and fee.

## Time modifiers and facility configuration

Reaction job duration can be affected by:
- **Reactions skill:** reduces reaction time by 4% per level.
- **Tatara role bonus:** 25% reaction-time reduction.
- **Reaction time rigs:** specific to the reactor family and rig size.
- Other applicable structure/facility effects shown in the job quote.

The Reactions skill does not add job slots; Mass Reactions and Advanced Mass Reactions do. Remote Reactions is a separate skill that expands remote job start/delivery range. [^eveuni-resource-skills] [^eveuni-reactions]

The EVE Reactions Calculator methodology lists the following representative rig values: T1 Reactor Efficiency rigs reduce material use by 2%, T2 by 2.4%; T1 time rigs reduce reaction time by 20%, T2 by 24%. It documents a reaction rig security multiplier of 1.0 in low security and 1.1 in null security/wormhole space. These are secondary calculator values, not a universal rig rule. Confirm the exact family, rig type, structure size, and effect in the current SDE and live Industry quote. [^eve-reactions-calculator-method]

Reaction rig security scaling is different from manufacturing rig scaling. Do not apply the manufacturing 1.9x low-sec or 2.1x null/wormhole multipliers to reaction rigs. See [Facilities and Rigs](../01-foundations/facilities-and-rigs.md).

## Facility and space constraints

Reactions can only be performed in an Upwell Refinery with the compatible reactor service module fitted and online. CCP states that reactors can only be installed in systems with a security rating of 0.4 or lower. The required reactor family depends on the formula: Composite, Hybrid, and Biochemical formulas are not interchangeable. [^ccp-reactions] [^ccp-service-modules]

The Tatara has a 25% reaction-time role bonus. The Athanor does not share that bonus. Reaction rigs are also family-specific; a Composite Reactor rig does not improve Hybrid or Biochemical reactions. [^eveuni-reactions]

The Reaction system cost index applies to reaction activity in the system rather than being calculated separately by reactor family, according to EVE University's reference. The live Industry job quote remains the final installation-fee check. [^eveuni-reactions]

## Remote job management

Remote Reactions allows a character to start and complete reaction jobs remotely. EVE University documents a range increase of five jumps per skill level, up to 25 jumps at V. The skill does not transport reaction formulas, materials, or output. Required assets must already be at the destination facility. [^eveuni-resource-skills] [^eveuni-reactions]

## Mixed-formula scheduling

A reaction character may need to produce several intermediate products for different downstream chains. The optimal schedule is not necessarily to keep every Reaction slot occupied with the formula that has the highest output volume.

For each candidate formula, calculate:
- Output units per slot-hour.
- Input material demand per slot-hour.
- Fuel-block demand per slot-hour.
- Installation fee per output unit.
- Material cost per output unit.
- Expected value or transfer value of the output.
- Downstream component demand and inventory target.

For a planning horizon H:

```text
Σ active Reaction slot-hours
  ≤ Reaction slots × 24 × H
```

Allocate slot-hours to formulas based on marginal contribution and downstream need. If a formula produces a high-value intermediate that is not currently needed or liquid, its apparent output rate may not translate into useful economic throughput.

## Reaction-chain bottlenecks

The sustainable output of a reaction-supported product chain is constrained by the slowest normalized stage:

1. Gas, moon-material, or biochemical input acquisition.
2. Reaction job capacity and formula throughput.
3. Component manufacturing or other downstream processing.
4. Logistics and asset staging.
5. Working capital and installation-fee funding.
6. Market absorption or internal consumption.

Convert every stage into equivalent final-product units per day before comparing. For example, Hybrid Polymer output should be converted through the relevant Hybrid Tech Component recipe and final T3 bill of materials before comparing reaction capacity with final manufacturing capacity.

A temporary inventory buffer can let downstream production continue when reactions pause, but it does not raise long-run sustainable throughput.

## Operational workflow

1. Select the Reaction Formula and confirm its reactor family.
2. Confirm the Refinery, system security, online service module, and facility access.
3. Record formula inputs, output quantity, fuel blocks, and base duration.
4. Record character Reaction slots, Reactions skill, and Remote Reactions range.
5. Record structure role bonus, reaction rig family/size, and current rig effect.
6. Obtain the live Industry quote for job duration and installation fee.
7. Calculate output and input demand per slot-hour.
8. Compare formula output with downstream demand and inventory targets.
9. Schedule jobs against available Reaction slot-hours and raw input availability.
10. Verify delivered output and actual consumed inputs against the formula.

## Common optimization errors

1. Treating Reaction slots as part of Manufacturing or Science slots.
2. Applying manufacturing rig security multipliers to reaction rigs.
3. Using a rig for the wrong reactor family.
4. Assuming all reaction formulas have identical run inputs or fuel requirements.
5. Ignoring the Tatara's reaction-time role bonus.
6. Treating the Reactions skill as a slot skill.
7. Assuming Remote Reactions transports materials or outputs.
8. Maximizing output volume without checking downstream demand and sale liquidity.
9. Using an outdated recipe table without checking the live formula.
10. Treating reaction job time as the only throughput constraint while ignoring gas/mineral supply and logistics.

## Verification requirements

The framework is source-backed but needs controlled in-game comparison:
- Verify formula output/input quantities and fuel consumption for representative Composite, Hybrid, and Biochemical formulas.
- Compare reaction job durations at Reactions I and V.
- Compare Athanor and Tatara job quotes for the same formula and character.
- Compare T1/T2 reaction rig material/time effects in low-sec and null/wormhole structures.
- Verify reaction job maximum run count and any job-duration cap.
- Compare theoretical slot utilization with actual job delivery/reinstallation intervals.

## Related concepts

- [Reactions](../02-production-systems/reactions.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Manufacturing Throughput](manufacturing-throughput.md)
- [Science and Invention Throughput](science-and-invention-throughput.md)
- [Tech II Components](../02-production-systems/tech-2-components.md)
- [Tech III Manufacturing](../02-production-systems/tech-3-manufacturing.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)

[^ccp-reactions]: CCP Support, Reactions (updated 2024-08-29).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-service-modules]: CCP Support, Service Modules (updated 2024-08-29).
[^eveuni-reactions]: EVE University Wiki, Reactions (last modified 2025-06-22).
[^eveuni-resource-skills]: EVE University Wiki, Skills: Resource Processing (accessed 2026-11-14).
[^eve-reactions-calculator-method]: EVE Reactions Calculator, methodology (accessed 2026-11-14).
