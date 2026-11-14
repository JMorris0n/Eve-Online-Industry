---
type: Concept
title: Blueprint Copying
description: BPO-to-BPC copying workflow, inherited ME/TE, copy job parameters, licensed-run limits, time, skills, materials, costs, and operational use.
tags:
  - blueprint-copying
  - bpo
  - bpc
  - science
  - manufacturing
sources:
  - id: ccp-copying
    resource: https://support.eveonline.com/hc/en-us/articles/203210602-Copying
    title: Copying | EVE Online Support (updated 2024-07-15)
  - id: ccp-blueprints
    resource: https://support.eveonline.com/hc/en-us/articles/203269951-Blueprints
    title: Blueprints | EVE Online Support (updated 2024-08-29)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
  - id: ccp-manufacturing
    resource: https://support.eveonline.com/hc/en-us/articles/203210292-Manufacturing
    title: Manufacturing | EVE Online Support (updated 2024-08-29)
  - id: eveuni-research
    resource: https://wiki.eveuniversity.org/Research
    title: Research | EVE University Wiki (last modified 2026-03-21)
  - id: eveuni-production
    resource: https://wiki.eveuniversity.org/Production
    title: Manufacturing | EVE University Wiki
generated:
  by: openai/gpt-6
  at: 2026-11-14T06:25:24Z
status: draft
---

## Summary

Blueprint copying takes a Blueprint Original (BPO) and produces one or more Blueprint Copies (BPCs). The BPCs inherit the BPO's Material Efficiency (ME) and Time Efficiency (TE) values at the moment the copy job is made. Later research on the original does not update copies that already exist. A BPC cannot be researched further and has a finite number of licensed production runs. [^ccp-copying] [^ccp-blueprints]

Copying is a **Science** job. It uses the same character job pool as ME research, TE research, and invention. Copying is useful for protecting valuable originals, enabling parallel Manufacturing jobs, preparing T1 inputs for Tech II invention, moving production to other facilities or regions, and selling BPCs to other industrialists. [^ccp-activities-jobs] [^eveuni-research]

## Copying model: two independent quantities

A copy job has two separate run-count fields:

| Field | Meaning | Effect |
|---|---|---|
| Job Runs | Number of copies the job produces | Determines the number of BPC items created |
| Runs per Copy | Licensed Manufacturing runs assigned to each produced BPC | Determines the manufacturing/invention capacity of each output copy and contributes to total copy duration |

Let:

- (C) = Job Runs, the number of copies produced.
- (R) = Runs per Copy, the licensed production runs assigned to each copy.
- (T) = total licensed runs created across all copies.

Then:

```text
Total licensed runs created = C × R
```

For example, setting Job Runs to 5 and Runs per Copy to 10 produces five BPCs with ten licensed runs each. The output contains 50 licensed runs in total. [^ccp-copying] [^eveuni-research]

### Why the distinction matters

Two configurations can create the same total licensed-run capacity but different numbers of physical BPC items:

| Job Runs | Runs per Copy | BPCs produced | Total licensed runs |
|---:|---:|---:|---:|
| 5 | 10 | 5 | 50 |
| 10 | 5 | 10 | 50 |
| 1 | 50 | 1 | 50 |

The second configuration creates more separate BPCs, which can be useful when distributing copies among several characters, corporation members, facilities, or concurrent jobs. The first or third may be more convenient when fewer physical copies are needed. This is an operational choice; it does not change the total licensed-run capacity represented by the copy job.

## BPC output properties

Each produced BPC inherits the BPO's ME and TE values at the time of copying. If the BPO is researched after the copy job is completed, existing BPCs keep the older values. If improved copies are required, another copy job must be installed from the now-improved BPO. [^ccp-copying]

BPCs cannot receive ME or TE research. After the final licensed Manufacturing run has been consumed, the BPC is not returned at delivery and is destroyed. [^ccp-copying]

### Maximum Runs per Copy

The maximum value of Runs per Copy is blueprint-specific. CCP states that the maximum is displayed in the Bill of Materials for the BPO's Copy activity. Use that value for the selected BPO, not a universal assumed limit. [^ccp-copying]

EVE University's current reference gives examples of ship BPCs having a 10-run maximum, while many module and ammunition BPCs can have up to 600 runs. These are examples, not universal category guarantees. A calculator or copy plan must read the blueprint's actual Copy activity value. [^eveuni-research]

## Copy job input materials

Most copying jobs from Tech I BPOs do not require additional materials or trained skills solely to install the copy job. CCP documents exceptions, usually involving Tech II BPOs and the Prototype Cloaking Device BPO. Depending on the blueprint, additional inputs can include:

- Data Sheets, which are NPC trade goods.
- R.Db items of the required fields.
- Skills associated with the blueprint's copy activity.

The exact inputs are specified by the blueprint's Copy activity Bill of Materials. [^ccp-copying]

**Important scaling rule:** if a copy job has input materials, CCP says those material quantities change with Job Runs (the number of copies produced), not with Runs per Copy (the licensed runs per BPC). [^ccp-copying]

This creates a material-efficiency decision in copy configuration. If an exceptional BPO requires one Data Sheet per copy, then a 5-copy job and a 10-copy job do not have the same input requirement, even when both create 50 total licensed runs. Do not assume that a copy job's optional or required input cost is proportional only to total licensed-run capacity.

## Copy job duration

CCP states that total copy-job duration is based on the total licensed production runs across all copies. EVE University provides the base-time model: copying one licensed run takes 80% of the blueprint's base Manufacturing run time before character skill and facility bonuses. The base Copy time is not affected by the BPO's TE level. [^ccp-copying] [^eveuni-research]

Let:

- (M) = base Manufacturing time per run for the BPO's item.
- (C) = number of BPCs produced (Job Runs).
- (R) = Runs per Copy.

The community-documented base copy-time model is:

```text
Base copy time per licensed run = M × 0.80

Base copy-job time = M × 0.80 × C × R
```

### Worked example

Assume the blueprint's base Manufacturing run time is 300 seconds:

- Base copy time per licensed run = 300 × 0.80 = 240 seconds.
- Five copies with ten runs per copy = 50 licensed runs.
- Base copy-job duration = 240 × 50 = 12,000 seconds = 3 hours 20 minutes.

Ten copies with five runs per copy also create 50 total licensed runs, so the base copy duration is also 3 hours 20 minutes. The two configurations may differ in copy-job inputs if the selected BPO requires per-copy materials. [^ccp-copying] [^eveuni-research]

### Time modifiers

EVE University documents the following copying-related skill effects:

| Skill | Copy-time effect |
|---|---|
| Science | 5% reduction per level |
| Advanced Industry | 3% reduction per level |

Advanced Industry reduces Manufacturing and research times. The Science skill is a copy-time bonus. The exact individual effects are useful for planning, but combined stacking and final time rounding should be compared against the live Industry quote before using this document as a deterministic time calculator. [^eveuni-research]

Blueprint TE does not reduce the base copy time. Do not use the manufacturing TE factor in the Copy time formula. The 80% relationship is stated against **base Manufacturing time**, before applying skills and facility modifiers, not the final time of the character's own Manufacturing job. [^eveuni-research]

Engineering Complexes have Science job time role bonuses and may have activity-specific copy time rigs. The appropriate copy-specific structure and rig effects are covered in [Facilities and Rigs](../01-foundations/facilities-and-rigs.md). Never apply a Manufacturing time rig to copying unless its supported activity explicitly includes Copying. [^eveuni-research]

## Skills, job slots, and remote installation

Copying consumes one Science job slot, not one Manufacturing slot. The Science job pool is shared with ME research, TE research, and invention. A character's Science slot capacity is:

```text
Science slots
  = 1 + Laboratory Operation level
      + Advanced Laboratory Operation level
```

The maximum is 11 Science jobs when both slot skills are trained to V. See [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md). [^ccp-activities-jobs] [^eveuni-research]

Copying can be started remotely using Scientific Networking. EVE University lists a five-jump range increase per skill level, up to 25 jumps at level V. Without the skill, Science jobs can be started within the character's current solar system. Remote initiation does not move the BPO or output copies; the required blueprint and any required inputs must be at the destination facility. [^eveuni-research] [^ccp-manufacturing]

## Why copy a BPO?

### Protect an original

A BPO may represent a substantial ISK investment and long research investment. A BPC can be moved or used in a more exposed facility while leaving the BPO in a safer location. CCP explicitly identifies using copies for Manufacturing in dangerous locations as a purpose of copying. [^ccp-copying]

### Increase manufacturing concurrency

EVE University documents that a single BPO can be used for only one active Manufacturing job at a time. Copying the BPO into several BPCs allows those copies to be used for separate Manufacturing jobs, subject to the character's job slots, BPC run limits, material availability, and facility capacity. [^eveuni-research]

This is a key way to separate blueprint asset ownership from factory throughput. A researched BPO can remain protected while copies are distributed to multiple manufacturing locations or characters.

### Feed Tech II invention

Tech II invention requires a Tech I BPC rather than a BPO. A copy line can therefore supply the T1 BPC inputs for a separate invention operation. One licensed T1 BPC run is consumed per invention run, regardless of invention success. See [Tech II Invention](tech-2-invention.md). [^ccp-blueprints] [^ccp-activities-jobs]

### Sell copies as an industrial product

BPCs can be supplied to other manufacturers through contracts and other in-game exchange routes. The value of a copy is influenced by item demand, licensed run count, inherited ME/TE, copy acquisition cost, and the buyer's alternative supply. A copy's theoretical manufacturing potential is not automatically its market value.

## Copy job cost and economic evaluation

Copying installation fees use the Copying activity's SCI and fee configuration. Do not simply use Manufacturing SCI or assume the Copy job has the same fee valuation basis as a Manufacturing job.

EVE University publishes a secondary Copying job-cost equation using activity SCI, copy count, runs per copy, and an EIV-like material-price basis. That reference also says the price inputs are based on the Manufacturing inputs for the final item. However, the EVE University page warns that its older SCI derivation may no longer reflect CCP's more volatile index update. For a production calculator, treat this as a candidate model only and compare it to a current in-game Copy job quote. [^eveuni-research]

The current fee model and unresolved activity-specific EIV questions are documented in [Installation Cost Computation](../09-computations/installation-costs.md), especially Q-002 in the research log.

When evaluating copy economics, separate:

- Copy-job installation fee.
- Any copy-specific input materials.
- Opportunity value of the BPO's use and exposure during the process.
- Time occupied in the Science job pool.
- Value and replacement cost of the resulting BPC inventory.
- Logistics and contract costs if copies are distributed or sold.

A low nominal copy fee does not necessarily mean that producing many low-run copies is optimal. More copies can simplify manufacturing distribution but increase handling and, for exceptional blueprints, copy-specific input materials.

## Copy planning workflow

1. **Select the BPO.** Confirm that the desired item supports Copying.
2. **Complete required ME/TE research first.** The resulting BPCs inherit the BPO's current values; existing copies do not update later.
3. **Inspect the Copy activity.** Record the maximum runs per copy, base copy time, required skills, and any input materials.
4. **Choose Job Runs and Runs per Copy.** Plan both the number of physical BPCs and the total licensed-run capacity required.
5. **Check the destination.** Confirm a Research service, ACL access, BPO location, and output BPC location.
6. **Check character capacity.** Confirm an available Science job slot and any remote-start range requirement.
7. **Review time and cost.** The Industry quote includes current job duration, facility modifiers, required inputs, and installation fee.
8. **Install and deliver.** Check the resulting BPCs and verify their ME, TE, and licensed runs before moving them to manufacturing or invention.

## Common errors

1. **Confusing Job Runs with Runs per Copy.** The first is how many BPC objects are produced; the second is how many licensed runs each object receives.
2. **Copying before research is finished.** Existing BPCs do not inherit later BPO research.
3. **Assuming every BPC can have the same run count.** The Copy activity BOM defines the blueprint-specific maximum.
4. **Applying BPO TE to copy time.** EVE University's base-copy-time reference explicitly says TE does not affect Copy time.
5. **Treating 80% as a final personal time ratio.** It is the base Copy time relative to base Manufacturing time before activity-specific skills and facility bonuses.
6. **Scaling copy input materials by licensed runs.** CCP says required copy input materials, if any, scale with number of copies produced, not Runs per Copy.
7. **Forgetting the Science job pool.** Copy jobs compete with ME/TE research and invention for Science slots.
8. **Assuming copying moves assets.** A remote-start skill does not transport the BPO, input materials, or output BPCs.
9. **Applying Manufacturing fees or rigs by analogy.** Copying has its own activity SCI and may have copy-specific facility/rig effects.

## Verification backlog

The documentation is source-backed, but the following should be validated in game before a copy-planning calculator is treated as authoritative:

- Record matched copy quotes for equal total licensed runs but different Job Runs/Runs per Copy configurations.
- Verify copy input quantities for a BPO with exceptional copy materials and confirm that only Job Runs changes them.
- Compare the base time estimate of 80% × base Manufacturing run time against the blueprint's displayed Copy time.
- Compare copy duration with Science, Advanced Industry, Engineering Complex role, and copying-specific rig effects.
- Confirm whether multiple concurrent copy jobs from the same BPO are restricted, and whether this differs between personal and corporation BPOs.
- Compare predicted Copy installation fees with current quotes in different systems/facilities.

## Related concepts

- [Blueprints and Research](../01-foundations/blueprints-and-research.md)
- [Skills and Job Capacity](../01-foundations/skills-and-job-capacity.md)
- [Facilities and Rigs](../01-foundations/facilities-and-rigs.md)
- [Tech I Manufacturing](tech-1-manufacturing.md)
- [Tech II Invention](tech-2-invention.md)
- [Installation Cost Computation](../09-computations/installation-costs.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)

[^ccp-copying]: CCP Support, Copying (updated 2024-07-15).
[^ccp-blueprints]: CCP Support, Blueprints (updated 2024-08-29).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
[^ccp-manufacturing]: CCP Support, Manufacturing (updated 2024-08-29).
[^eveuni-research]: EVE University Wiki, Research (last modified 2026-03-21).
[^eveuni-production]: EVE University Wiki, Production.
