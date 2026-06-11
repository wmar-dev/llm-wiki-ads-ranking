---
title: "Follow the Prophet: CVR Prediction Under Delayed Feedback"
type: "source_summary"
sources:
  - "web/follow-the-prophet-delayed-feedback-cvr.md"
source_url: "https://arxiv.org/abs/2108.06167"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Follow the Prophet: CVR Prediction Under Delayed Feedback

**Authors:** Haoming Li, Feiyang Pan, Xiang Ao, Zhao Yang, Min Lu, Junwei Pan, Dapeng Liu, Lei Xiao, Qing He

**Venue:** SIGIR 2021 (44th International ACM SIGIR Conference, July 11-15, 2021)

**Source type:** `peer_reviewed`

---

## Overview

Conversions arrive on a much longer and more variable timescale than clicks —
minutes to days or weeks after the click — so an online CVR model must decide
how to label a training example **before** knowing whether a delayed
conversion will eventually occur. This is the **delayed feedback problem**,
and it is a defining difference between CVR and CTR prediction
[[raw/web/follow-the-prophet-delayed-feedback-cvr.md]].

## Prior Approaches and Their Limits

| Approach | Mechanism | Limitation |
|---|---|---|
| **Fixed waiting window** | Don't label an example until a window (e.g., 7 days) has elapsed | Long windows delay the training signal and slow adaptation; short windows mislabel future converters as negatives, biasing the model toward under-prediction |
| **Stream-as-negative + duplicate-as-positive** | Ingest every impression as negative immediately; insert a positive duplicate with importance weighting if a conversion later arrives | Keeps the model fresh, but the importance-weighting correction is an approximation that only partially removes bias |

[[raw/web/follow-the-prophet-delayed-feedback-cvr.md]]

## The FTP Solution

FTP defines an idealized **"prophet" model** — the CVR model that would exist
if every conversion's true label were observed instantly. FTP approximates the
prophet's predictions via an **aggregation policy over multiple time-windowed
sub-models**, each capturing the conversion pattern observable within a
different elapsed-time interval since the click. The learned aggregation
imitates the zero-delay prophet's output without the long wait or the bias of
duplicate/importance-weighting heuristics
[[raw/web/follow-the-prophet-delayed-feedback-cvr.md]].

## Key Results

Evaluated on three real-world industrial advertising datasets, FTP
outperformed prior delayed-feedback baselines (fixed-window and
duplicate-with-importance-weighting methods) on standard CVR prediction
metrics [[raw/web/follow-the-prophet-delayed-feedback-cvr.md]].

## Relevance to Ads Ranking

Delayed feedback is why CVR prediction cannot simply reuse a CTR model's
online-learning loop (e.g., Google's FTRL-Proximal, which relies on
near-immediate click/no-click labels
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]). Production
pCVR systems must layer delayed-feedback-aware training (FTP and related
methods such as elapsed-time sampling or unbiased label correction) on top of
entire-space architectures like ESMM
[[wiki/sources/esmm-entire-space-multi-task-model.md]] to keep predictions
both unbiased and timely.

## Related Pages

- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/what-is-a-conversion.md]]
- [[wiki/synthesis/model-structures-for-pcvr.md]] — where FTP's delayed-feedback correction fits relative to feature-interaction backbones and multi-task (MMoE/PLE) architectures
