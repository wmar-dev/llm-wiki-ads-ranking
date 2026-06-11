---
title: "What Are Some Model Structures for pCVR?"
type: "synthesis"
sources:
  - "web/deepfm-factorization-machine-deep-learning-ctr.md"
  - "web/ple-progressive-layered-extraction-multitask.md"
  - "web/esmm-entire-space-multi-task-model.md"
  - "web/follow-the-prophet-delayed-feedback-cvr.md"
  - "web/ad-click-prediction-view-from-the-trenches.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# What Are Some Model Structures for pCVR?

"Model structure for pCVR" actually splits into two largely independent design
axes:

1. **Feature-interaction backbone** — what network computes a probability from
   raw features (linear model? factorization machine + DNN? explicit feature
   crosses?).
2. **Multi-task framing** — how the CVR objective shares parameters and
   training signal with CTR (and other objectives), to address CVR's sample
   selection bias, data sparsity, and the seesaw/negative-transfer problem of
   joint training.

A third dimension — **entire-space training (ESMM)** and **delayed-feedback
correction (FTP)** — wraps *either* backbone in a training/labeling scheme that
fixes CVR-specific data problems; that layer is covered in depth in
[[wiki/synthesis/how-do-ad-systems-predict-conversions.md]]. This page focuses
on axes 1 and 2 and how all three compose.

## Axis 1: Feature-Interaction Backbones

| Architecture | Interaction order | Feature engineering | Notes |
|---|---|---|---|
| **LR / FTRL-Proximal** | Order-1 (linear) only | Manual cross-features needed for any interaction signal | Google's production CTR baseline at billion-coefficient scale; FTRL-Proximal's L1 regularization gives sparse, memory-efficient models with per-coordinate learning rates [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] *(peer reviewed)* |
| **Wide & Deep** | Linear (wide) + implicit high-order (deep) | Wide component still needs hand-engineered cross-product features | Predecessor that DeepFM and DCN both directly address [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]] |
| **DeepFM** | Order-1, order-2 (FM) + implicit high-order (DNN) | None — FM and DNN share one embedding layer, trained end-to-end | Outperformed LR, FM, and Wide & Deep on CTR AUC/Logloss in benchmark and Huawei App Store experiments [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]] *(peer reviewed, IJCAI 2017)* |
| **DCN (Deep & Cross Network)** | Explicit bounded-degree polynomial crosses (cross network) + implicit high-order (DNN) | None — cross network learns feature crosses automatically | Sibling to DeepFM: replaces FM's pairwise factorization with an explicit cross network, concatenated with a parallel DNN before a final output layer |

**Inference:** DeepFM and DCN solve the same problem (avoid Wide & Deep's
manual cross-feature engineering) via two different mechanisms — FM-style
factorization vs. an explicit cross network — and both are common choices for
the CTR/CVR tower "backbone" inside larger production architectures.

## Axis 2: Multi-Task Architectures for CTR + CVR

Jointly predicting CTR and CVR (or other related objectives like watch-time)
runs into the **seesaw phenomenon** — improving one task degrades another —
and **negative transfer**, where naive parameter sharing hurts all tasks when
objectives conflict [[wiki/sources/ple-progressive-layered-extraction-multitask.md]].

| Architecture | Mechanism | Limitation |
|---|---|---|
| **Shared-Bottom** | Single shared encoder feeds separate per-task heads | Simple, but prone to negative transfer when tasks conflict [[wiki/sources/ple-progressive-layered-extraction-multitask.md]] |
| **MMoE (Multi-gate Mixture-of-Experts)** | A pool of shared expert sub-networks, with a separate gating network per task that learns how to weight experts | Mitigates but doesn't eliminate seesaw/negative transfer — all experts remain fully shared across tasks [[wiki/sources/ple-progressive-layered-extraction-multitask.md]] |
| **PLE (Progressive Layered Extraction)** | Customized Gate Control (CGC): separates *shared* experts from *task-specific* experts; stacks multiple CGC layers with progressive routing so deeper layers refine shared-vs-task-specific representations | Significantly outperformed shared-bottom and MMoE on Tencent's ~1B-sample video dataset; **+2.23% view-count, +1.84% watch-time** in online A/B test [[wiki/sources/ple-progressive-layered-extraction-multitask.md]] *(blog summary of RecSys 2020 paper)* |

## How the Two Axes Combine With ESMM and FTP

The feature-interaction backbone (axis 1) and multi-task architecture (axis 2)
are not alternatives to ESMM's entire-space CTR/CVR/CTCVR framing — they
operate at a different layer:

- **ESMM** [[wiki/sources/esmm-entire-space-multi-task-model.md]] specifies
  *which population* the CVR sub-network trains on (the entire impression
  space, via the CTCVR = pCTR x pCVR auxiliary loss) and provides a *minimal*
  multi-task wiring (a shared CVR sub-network whose output is multiplied by the
  CTR tower's output).
- **DeepFM/DCN** specify *what network* implements each tower (CTR tower, CVR
  sub-network) internally.
- **MMoE/PLE** specify *how* the CTR and CVR towers (and any other objectives)
  share parameters — generalizing ESMM's single shared CVR sub-network into a
  full expert/gating structure.
- **FTP** [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]] specifies
  *when* a CVR training example's label is finalized, independent of the
  network architecture.

**Inference:** a production pCVR stack plausibly composes all four —
e.g., DeepFM/DCN-style towers, wired together with a PLE-style expert/gate
layer for CTR+CVR (+other objectives), trained under ESMM's entire-space CTCVR
loss, with FTP-style aggregation correcting for delayed conversion labels. None
of the sources read for this query describe a single published architecture
that names all four pieces together — see Open Questions.

![model-structures-for-pcvr-diagram-1](/assets/model-structures-for-pcvr-diagram-1.svg)

## Why It Matters for Ads Ranking

- "What model computes pCVR" has no single answer — it's a **stack of mostly
  orthogonal design decisions** (backbone, multi-task sharing, entire-space
  training, delayed-feedback correction), each solving a distinct failure mode.
- The feature-interaction backbone (DeepFM/DCN) determines *prediction
  quality from features*; the multi-task architecture (MMoE/PLE) determines
  *how cleanly CTR and CVR can be improved together* without one regressing the
  other — both matter for the calibrated, per-candidate pCTR/pCVR pair that
  feeds Ad Rank/LTV and Smart Bidding [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
- PLE's reported online lift (+2.23% view-count, +1.84% watch-time over prior
  MTL baselines) shows that the *multi-task* axis alone — independent of
  backbone choice or entire-space training — is a meaningful source of
  production gains [[wiki/sources/ple-progressive-layered-extraction-multitask.md]].

## Open Questions

- Open question: is there a published production architecture (Google, Meta,
  Alibaba, Tencent, etc.) that combines a feature-interaction backbone
  (DeepFM/DCN-style), a PLE/MMoE-style multi-task expert/gate layer, ESMM's
  entire-space CTCVR loss, and FTP-style delayed-feedback correction in one
  system — or are these four pieces typically deployed as separate
  pipeline/model stages?

## Related Pages

- [[wiki/synthesis/how-do-ad-systems-predict-conversions.md]] — deep dive on
  the entire-space (ESMM) and delayed-feedback (FTP) layers that wrap the
  backbones and multi-task architectures covered here
- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]
- [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]]
- [[wiki/sources/ple-progressive-layered-extraction-multitask.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]]
