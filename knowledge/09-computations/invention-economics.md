---
type: Computation
title: Invention Economics
description: Expected cost per successful Tech II BPC and manufacturing run, including attempt variance, decryptors, datacores, BPC opportunity cost, and job fees.
tags:
  - computation
  - invention
  - tech-ii
  - expected-value
sources:
  - id: ccp-invention
    resource: https://support.eveonline.com/hc/en-us/articles/203210642-Invention
    title: Invention | EVE Online Support (updated 2024-08-29)
  - id: ccp-decryptors
    resource: https://support.eveonline.com/hc/en-us/articles/203270631-Decryptors
    title: Decryptors | EVE Online Support (updated 2024-08-29)
  - id: eveuni-invention
    resource: https://wiki.eveuniversity.org/Invention
    title: Invention | EVE University Wiki (last modified 2026-10-09)
  - id: ccp-activities-jobs
    resource: https://support.eveonline.com/hc/en-us/articles/203210272-Activities-and-Job-Types
    title: Activities and Job Types | EVE Online Support (updated 2024-08-29)
generated:
  by: openai/gpt-6
  at: 2026-11-14T10:10:00Z
status: draft
---

## Purpose

This computation estimates the economic cost of generating Tech II BPCs through probabilistic invention. The correct denominator is expected successful output, not the number of attempts. Failed attempts still consume the input BPC run and the quoted invention inputs. [^ccp-invention] [^eveuni-invention]

This model is intended for repeated production planning. It does not predict the exact outcome of one invention job.

## Required inputs

For one invention job containing N attempts, record:

| Symbol | Input | Source |
|---|---|---|
| N | Number of invention attempts | Industry job setup |
| p | Success probability per attempt, decimal 0–1 | Industry UI |
| C_BPC | Economic value of all input Tech I BPC runs consumed | Acquisition cost or opportunity cost |
| C_DC | Total datacore cost for the job | Live input quote and current market prices |
| C_D | Total decryptor cost for the job | Live input quote and current market prices |
| C_O | Other consumed inputs | Live job quote |
| C_F | Total invention installation fee | Live Industry quote |
| R_out | Licensed manufacturing runs on each successful Tech II BPC | Output preview |
| U_out | Finished units per Tech II manufacturing run | Blueprint |
| T_job | Invention job duration | Live Industry quote |

Do not infer datacore or decryptor quantities from the number of attempts. Use the actual job input list. The underlying Tech II Invention concept records the remaining quantity/stacking questions and item-specific output behavior.

## Probability model

The Tech II invention probability formula and base chance categories are documented in [Tech II Invention](../02-production-systems/tech-2-invention.md). Use the chance displayed by the Industry UI as the operational input.

For N independent attempts with identical success probability p:

```text
Expected successful BPCs
  = N × p

Expected failed attempts
  = N × (1 - p)

Probability of at least one success
  = 1 - (1 - p)^N

Variance of successful BPC count
  = N × p × (1 - p)

Standard deviation
  = sqrt(N × p × (1 - p))
```

The independence and equal-probability assumptions are a planning model. If attempts use different decryptors, skills, or job settings, calculate each group separately.

## Total job cost

Include every consumed input and the full installation fee:

```text
Total invention job cost
  = C_BPC + C_DC + C_D + C_O + C_F
```

C_BPC should value the licensed Tech I BPC runs consumed, not necessarily the entire BPC object. If a purchased BPC has K licensed runs and acquisition cost C_copy, a simple allocation is:

```text
Cost per licensed input run
  = C_copy / K

C_BPC
  = invention attempts × cost per licensed input run
```

For internally copied BPCs, include the economic cost of copying and the opportunity cost of the BPO/Science capacity. Do not treat a self-produced BPC as free.

If a cost is already included in the quoted total job inputs, do not add it a second time.

## Expected cost per successful BPC

```text
Expected cost per successful BPC
  = total invention job cost / expected successful BPCs

  = (C_BPC + C_DC + C_D + C_O + C_F) / (N × p)
```

This is the most robust batch-level form because it allows installation fee and input quantities to scale nonlinearly with the job's attempt count.

If every attempt has the same cost c and the total job cost is exactly N × c, then the simplified formula is:

```text
Expected attempts per success = 1 / p

Expected cost per successful BPC = c / p
```

Do not use the simplified form when fixed job fees, decryptor quantities, or other inputs do not scale linearly with N.

## Expected Tech II manufacturing-run cost

Each successful output BPC has R_out licensed Manufacturing runs:

```text
Expected Tech II manufacturing runs
  = N × p × R_out

Expected invention cost per Tech II run
  = total invention job cost / (N × p × R_out)
```

This is the invention component only. Add the Tech II manufacturing materials, installation fee, and other costs separately.

For U_out finished units per manufacturing run:

```text
Expected invention cost per finished unit
  = total invention job cost
    / (N × p × R_out × U_out)
```

This assumes the expected successful BPCs are used for the intended product and all licensed output runs are consumed.

## Worked example

The following numbers are illustrative assumptions, not live market values or a universal invention result.

Assume:
- N = 20 attempts.
- p = 45% (0.45).
- Total cost of all input BPC runs, datacores, decryptors, other inputs, and installation fee = 300,000,000 ISK.
- Each successful output BPC has R_out = 10 licensed manufacturing runs.
- Each manufacturing run produces U_out = 1 finished item.

Expected successful BPCs:

```text
20 × 0.45 = 9 expected successful BPCs
```

Probability of at least one success:

```text
1 - (1 - 0.45)^20
  = 1 - 0.55^20
  ≈ 99.64%
```

Expected Tech II manufacturing runs:

```text
9 × 10 = 90 expected manufacturing runs
```

Expected invention cost per successful BPC:

```text
300,000,000 / 9
  = 33,333,333 ISK
```

Expected invention cost per Tech II manufacturing run:

```text
300,000,000 / 90
  = 3,333,333 ISK
```

The actual job may produce fewer or more than nine successful BPCs. The expected value becomes more useful across repeated jobs or a longer production horizon.

## Decryptor comparison

For each candidate decryptor, calculate a separate scenario using:
- Its probability multiplier.
- Its purchase cost and actual consumed quantity.
- Its output BPC run modifier.
- Its output ME and TE modifiers.
- The resulting Tech II manufacturing material and time requirements.

For decryptor d:

```text
Expected T2 run cost(d)
  = total invention cost(d)
    / (N × p(d) × R_out(d))
```

This metric alone is not enough if decryptors change output ME/TE. Calculate the downstream manufacturing cost for the resulting BPC and compare the full cost per finished unit.

The best decryptor is the one that minimizes expected total cost or maximizes expected net contribution for the target product and production constraints. It is not necessarily the one with the highest probability or most runs. [^ccp-decryptors]

## Science slot-hour efficiency

Invention consumes Science capacity. To compare invention with other Science activities:

```text
Expected successful BPCs per Science slot-hour
  = (N × p) / job duration in hours

Expected T2 manufacturing runs per Science slot-hour
  = (N × p × R_out) / job duration in hours
```

Use the actual quoted duration and account for any idle time between jobs. Copying and ME/TE research use the same Science pool, so invention's opportunity cost includes the best alternative use of those slot-hours. [^ccp-activities-jobs]

## Expected cost versus realized cost

For a completed job:

```text
Realized cost per successful BPC
  = actual total job cost / actual successful BPC count
```

If the job has zero successful outputs, realized cost per successful BPC is undefined; the entire job cost is a realized loss for that batch. Do not remove failed jobs from the dataset.

For a series of jobs, aggregate costs and successful outputs:

```text
Portfolio realized cost per successful BPC
  = sum(total invention job costs)
    / sum(successful BPCs)
```

This avoids the distortion of averaging each job's cost-per-success equally when job sizes differ.

## Model limitations and verification

- The model assumes each attempt has the same probability unless attempts are grouped by settings.
- Use the Industry UI's displayed probability and output preview.
- Confirm datacore and decryptor quantities from the actual multi-run job quote.
- Confirm installation fee and job duration from the live quote.
- Include input BPC opportunity cost and failed-attempt consumption.
- Confirm output BPC runs/ME/TE by item and decryptor.
- Track actual success counts over multiple jobs and compare with the expected binomial distribution.
- Do not use a single small sample to declare the probability formula wrong or right.

## Related concepts

- [Tech II Invention](../02-production-systems/tech-2-invention.md)
- [Science and Invention Throughput](../05-optimization/science-and-invention-throughput.md)
- [Industrial Cost Accounting](../04-industrial-economics/cost-accounting.md)
- [Manufacturing Profitability](../04-industrial-economics/manufacturing-profitability.md)
- [Installation Cost Computation](installation-costs.md)
- [Production Scheduling](../05-optimization/production-scheduling.md)

[^ccp-invention]: CCP Support, Invention (updated 2024-08-29).
[^ccp-decryptors]: CCP Support, Decryptors (updated 2024-08-29).
[^eveuni-invention]: EVE University Wiki, Invention (last modified 2026-10-09).
[^ccp-activities-jobs]: CCP Support, Activities and Job Types (updated 2024-08-29).
