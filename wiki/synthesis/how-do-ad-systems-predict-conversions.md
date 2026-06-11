---
title: "How Do Ad Systems Predict Conversions?"
type: "synthesis"
sources:
  - "web/google-ads-about-conversions.md"
  - "web/statistical-learning-attribution-sets.md"
  - "web/ad-click-prediction-view-from-the-trenches.md"
  - "web/esmm-entire-space-multi-task-model.md"
  - "web/follow-the-prophet-delayed-feedback-cvr.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# How Do Ad Systems Predict Conversions?

Ad ranking systems predict conversions by computing a per-candidate **pCVR**
(predicted conversion rate) — and often a predicted conversion *value* — that
feeds directly into Smart Bidding strategies (Target CPA, Target ROAS, Maximize
Conversions) and oCPM delivery decisions
[[wiki/synthesis/what-is-a-conversion.md]]. Architecturally, pCVR looks like a
sibling of pCTR (predicted click-through rate): both are machine-learned
probabilities computed on every auction candidate
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]. But CVR prediction has two
problems that CTR prediction does not, and the production techniques for
solving them are what actually define "how ad systems predict conversions."

## Why CVR Prediction Is Harder Than CTR Prediction

| Problem | CTR prediction | CVR prediction |
|---|---|---|
| **Label availability** | Click/no-click is observed within seconds of the impression | Conversion may occur minutes to weeks after the click [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]] |
| **Training population** | Every impression has a click/no-click label | A "did this click convert?" label only naturally exists for *clicked* impressions, but the model must score *all* impressions [[wiki/sources/esmm-entire-space-multi-task-model.md]] |
| **Event rarity** | ~1-2% click rates are already sparse [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] | Conversions are rarer still — often orders of magnitude fewer positive examples than clicks [[wiki/sources/esmm-entire-space-multi-task-model.md]] |
| **Attribution** | Click is directly observed by the platform | Conversion must be linked back to the originating click/impression, increasingly through coarsened, privacy-preserving "attribution sets" rather than a deterministic join [[wiki/sources/statistical-learning-attribution-sets.md]] |

These four issues — **sample selection bias**, **data sparsity**, **delayed
feedback**, and **attribution uncertainty** — are addressed by distinct (but
complementary) modeling techniques.

## Sample Selection Bias and Data Sparsity: Entire-Space Multi-Task Models

A naive CVR model trains a click->conversion classifier only on clicked
impressions. At serving time, however, the auction needs a pCVR for *every*
candidate, including the ~98%+ that were never clicked. Training and serving
distributions diverge — a textbook **sample selection bias** problem
[[wiki/sources/esmm-entire-space-multi-task-model.md]].

The production answer, popularized by Alibaba's **ESMM** (Entire Space
Multi-Task Model, SIGIR 2018), is to stop training a standalone CVR model
entirely. Instead, ESMM exploits the sequential dependency
**impression -> click -> conversion** and trains two auxiliary tasks that *are*
defined over every impression:

- **CTR** = P(click | impression)
- **CTCVR** = P(click and conversion | impression) = pCTR x pCVR

![how-do-ad-systems-predict-conversions-diagram-1](/assets/how-do-ad-systems-predict-conversions-diagram-1.svg)

The CVR sub-network's output is multiplied by the CTR tower's output to form
the CTCVR prediction, and the loss is computed on CTR and CTCVR — both of
which have valid labels for every impression. This means:

- **Sample selection bias is eliminated**: the CVR sub-network's parameters
  receive gradient signal from entire-space CTCVR labels, not from a
  clicked-only subspace [[wiki/sources/esmm-entire-space-multi-task-model.md]].
- **Data sparsity is mitigated**: the CVR sub-network shares embedding
  parameters with the CTR tower, which trains on the much larger
  click/no-click signal — an implicit transfer-learning effect
  [[wiki/sources/esmm-entire-space-multi-task-model.md]].

ESMM was validated on Taobao production traffic and a public benchmark dataset
of sequential click->conversion logs, and it significantly outperformed
clicked-only CVR baselines and oversampling-based corrections on both CVR and
CTCVR AUC [[wiki/sources/esmm-entire-space-multi-task-model.md]] *(peer
reviewed)*. Successors such as ESCM2 add counterfactual regularization on top
of the same entire-space framing.

## Delayed Feedback: The "Follow the Prophet" Approach

Even with an entire-space architecture, CVR models face a second problem that
CTR models largely avoid: **the positive label may not exist yet**. A click
that will eventually convert might not show that conversion for hours, days,
or weeks [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]. Two
older approaches each trade off bias against freshness:

- **Fixed waiting window** — don't finalize a label until N days have passed.
  Long windows produce accurate labels but stale training data; short windows
  mislabel future converters as negatives, systematically under-predicting
  CVR.
- **Stream-as-negative, duplicate-as-positive** — label every impression
  negative immediately, and if a conversion arrives later, re-ingest a
  positive duplicate with an importance weight to correct the bias. This keeps
  the model fresh, but the importance-weighting correction is only an
  approximation [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]].

**FTP (Follow the Prophet, SIGIR 2021)** reframes the problem around an
idealized **"prophet" model** — the CVR model that would exist if every
conversion's true label arrived instantly. FTP can't observe the prophet's
labels, but approximates its predictions via a learned aggregation over
multiple sub-models, each trained on the conversion pattern observable within
a different elapsed-time interval since the click. On three real-world
advertising datasets, FTP outperformed both the fixed-window and
duplicate-with-importance-weighting baselines
[[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]] *(peer reviewed)*.

**Inference:** entire-space architectures (ESMM) and delayed-feedback
correction (FTP) solve different problems and are layered together in
production — ESMM fixes *which population* the CVR model is trained on, while
FTP fixes *when and how* a given training example's label is finalized.

## Attribution Uncertainty: Training Under Privacy-Preserving APIs

A third complication sits upstream of the model itself: as third-party cookies
are deprecated, browsers increasingly expose only **privacy-preserving
attribution APIs** that return an *attribution set* — a group of candidate
clicks that could have caused a conversion — rather than a single deterministic
click->conversion link [[wiki/sources/statistical-learning-attribution-sets.md]].
Recent work constructs an **unbiased loss estimator** for pCVR models that
remains correct under this coarsened labeling, with generalization guarantees
that scale with how informative the attribution-set prior is. Naive
credit-splitting heuristics (e.g., uniform credit across an attribution set)
lose accuracy as attribution sets grow larger and more overlapping — exactly
the direction privacy APIs are pushing the ecosystem
[[wiki/sources/statistical-learning-attribution-sets.md]] *(preprint)*.

## Shared Infrastructure with CTR Prediction

CVR models are not built from scratch — they typically reuse the same
large-scale online-learning infrastructure proven for CTR prediction. Google's
FTRL-Proximal system trains billion-coefficient models with per-coordinate
learning rates, L1/L2 sparsity, and aggressive memory optimizations (fixed-point
encoding, probabilistic feature inclusion)
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] *(peer
reviewed)*. The same calibration techniques (e.g., isotonic regression to map
predicted probabilities to observed rates) apply to pCVR, and arguably matter
*more* for CVR given how much rarer and noisier conversion labels are than
click labels.

## How pCVR Feeds Back into the Auction

pCVR rarely enters the Ad Rank/LTV formula directly
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]. Instead, it shapes the **bid
itself**:

- **Smart Bidding** (Target CPA, Target ROAS, Maximize Conversions) uses pCVR
  and predicted conversion value to compute a per-auction bid automatically
  [[wiki/synthesis/what-is-a-conversion.md]].
- **oCPM** is nominally billed per impression, but the platform uses pCVR to
  decide *which* impressions to deliver in order to maximize conversions
  [[wiki/synthesis/bidding-types.md]].

That bid then enters the same GSP/Ad Rank auction as any other bid
[[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]].

## Why It Matters for Ads Ranking

- Conversion prediction is the **economic engine** behind performance
  advertising — every CPA/ROAS bid strategy is a bet on pCVR accuracy.
- The dominant production pattern is **entire-space multi-task learning**
  (ESMM-style CTR/CVR/CTCVR towers), not a standalone CVR classifier — this is
  what makes pCVR well-defined and well-calibrated across the *entire*
  candidate pool the auction scores, not just historically-clicked ads.
- **Delayed feedback** and **privacy-preserving attribution** are two separate
  sources of label noise that production systems must correct for
  independently of the model architecture itself.

## Open Questions

- Open question: do production systems (Google, Meta) combine ESMM-style
  entire-space architectures with delayed-feedback correction (FTP or
  similar) in a single jointly-trained model, or as separate pipeline stages?
- Open question: how do unbiased attribution-set loss estimators
  [[wiki/sources/statistical-learning-attribution-sets.md]] interact with
  entire-space CVR architectures — does coarsened attribution affect the CTCVR
  label, the CVR label, or both?

## Related Pages

- [[wiki/synthesis/what-is-a-conversion.md]]
- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]
- [[wiki/sources/statistical-learning-attribution-sets.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/synthesis/bidding-types.md]]
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]]
