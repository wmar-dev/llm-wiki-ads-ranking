---
title: "What Are the Different ML Losses Used in Ad Systems?"
type: "synthesis"
sources:
  - "web/ad-click-prediction-view-from-the-trenches.md"
  - "web/deepfm-factorization-machine-deep-learning-ctr.md"
  - "web/esmm-entire-space-multi-task-model.md"
  - "web/ple-progressive-layered-extraction-multitask.md"
  - "web/follow-the-prophet-delayed-feedback-cvr.md"
  - "web/linucb-contextual-bandit-news-recommendation.md"
  - "web/fatigue-aware-ad-creative-selection.md"
  - "web/bayesian-deep-learning-ctr-uncertainty-quantification.md"
  - "web/survey-uncertainty-deep-neural-networks-gawlikowski.md"
  - "web/two-tower-models-engineers-of-ai.md"
  - "web/implement-two-tower-retrieval-google-cloud.md"
  - "web/tiger-transformer-index-generative-recommenders.md"
  - "web/better-generalization-semantic-ids-ranking.md"
  - "web/transact-v2-pinterest.md"
  - "web/a-simple-approach-to-ordinal-classification-frank-hall.md"
  - "web/rank-consistent-ordinal-regression-coral-age-estimation.md"
  - "web/how-to-perform-ordinal-regression-classification-in-pytorch.md"
  - "web/matryoshka-representation-learning.md"
  - "web/matryoshka-embedding-models-huggingface.md"
status: "current"
created: "2026-06-12"
last_updated: "2026-06-12"
---

# What Are the Different ML Losses Used in Ad Systems?

An ad-ranking stack is not trained with one loss function — it is trained
with a *portfolio* of losses, each solving a distinct problem: predicting a
probability (CTR/CVR), balancing competing objectives (multi-task), correcting
for label timing (delayed feedback), choosing among arms under uncertainty
(bandits), quantifying confidence (uncertainty/calibration), scoring on
ordered tiers (ad/landing-page quality), retrieving from billions of
candidates (two-tower), and generating discrete item identifiers (Semantic
IDs). This page organizes the losses surfaced across the wiki's source pages
into families, shows where each is used, and compares what each one actually
optimizes for.

## 1. Pointwise Classification Losses for CTR/CVR

The foundational loss for ad ranking is **binary cross-entropy / log loss**,
used to train a model to output a calibrated click or conversion
probability.

- **FTRL-Proximal online logistic regression**: Google's production CTR
  system fits a per-coordinate logistic regression online via the
  FTRL-Proximal algorithm, with L1 regularization for sparsity and L2 for
  shrinkage. The implicit loss being minimized at each step is logistic
  (log) loss plus L1/L2 penalty terms; AucLoss (1 − AUC) and LogLoss are the
  primary evaluation metrics
  [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
  [[wiki/entities/ftrl-proximal-algorithm.md]].
- **DeepFM**: combines an FM component (order-1/order-2 feature interactions)
  and a DNN component (implicit high-order interactions) whose summed
  outputs pass through a sigmoid; trained end-to-end with logloss for CTR,
  outperforming LR, standalone FM, and Wide & Deep on CTR AUC/Logloss
  [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]].
- **TransAct V2 (Next Action Loss)**: Pinterest's production Homefeed ranking
  model adds an auxiliary **Next Action Loss (NAL)** on top of point-wise
  ranking — a sequence-modeling objective over a user's lifelong action
  history (up to ~16,000 actions) that, combined with real-time sequences,
  improved HIT@3/repin by +13.31% and reduced HIT@3/hide by 11.25% offline,
  and produced +6.35% Homefeed Repin Volume / −12.80% Hide Volume online
  [[wiki/sources/transact-v2-pinterest.md]]. *Inference: NAL is layered on
  top of — not a replacement for — the point-wise CTR/CVR cross-entropy
  losses described above; it is an auxiliary sequence-prediction loss added
  to the same training objective.*

Both FTRL-Proximal and DeepFM optimize the same fundamental quantity
(probability of a binary outcome via cross-entropy), but differ in *how* the
score is computed from features — linear+L1/L2 vs. FM+DNN
[[wiki/synthesis/model-structures-for-pcvr.md]].

## 2. Multi-Task Losses (CTR + CVR, Entire-Space Training)

Predicting CVR (post-click conversion) introduces two problems that pure
cross-entropy on clicked impressions doesn't solve: **sample selection bias**
(a CVR model trained only on clicks is applied to the entire impression space
at serving time) and **data sparsity** (conversions are far rarer than
clicks) [[wiki/sources/esmm-entire-space-multi-task-model.md]].

- **ESMM (Entire Space Multi-Task Model)**: trains two auxiliary
  cross-entropy losses jointly — one for **CTR** = P(click | impression) and
  one for **CTCVR** = P(click and conversion | impression) = pCTR × pCVR —
  both defined over the *entire* impression space (not just clicks). Because
  CTR and CTCVR labels exist for every impression, gradients for the shared
  CVR sub-network flow from entire-space supervision, eliminating sample
  selection bias, while shared embeddings with the data-rich CTR tower
  mitigate data sparsity via implicit transfer learning
  [[wiki/sources/esmm-entire-space-multi-task-model.md]].
- **PLE (Progressive Layered Extraction)**: addresses a different multi-task
  failure mode — the **seesaw phenomenon** (improving one task's loss
  degrades another) and **negative transfer** from naive parameter sharing.
  PLE's Customized Gate Control (CGC) architecture separates shared experts
  from task-specific experts, with each task retaining its own loss (e.g.,
  per-task cross-entropy for CTR, CVR, watch-time), combined via per-task
  gating. On a ~1B-sample Tencent dataset, PLE outperformed shared-bottom and
  MMoE on both tasks simultaneously, with a +2.23% view-count / +1.84%
  watch-time online lift
  [[wiki/sources/ple-progressive-layered-extraction-multitask.md]].

**Inference**: ESMM and PLE solve orthogonal problems at the loss level —
ESMM specifies *which population* (and which auxiliary CTCVR loss) the CVR
task trains against, while PLE specifies *how* per-task losses (CTR, CVR,
and others) share representations without each task's gradient harming the
others. A production system plausibly composes both: per-task cross-entropy
losses for CTR/CVR routed through a PLE-style expert/gate backbone, with the
CVR loss additionally wrapped in ESMM's entire-space CTCVR formulation
[[wiki/synthesis/model-structures-for-pcvr.md]].

## 3. Delayed-Feedback Correction Losses

Conversions arrive on a much longer and more variable timescale than clicks
(minutes to weeks), so a CVR model must decide how to label a training
example *before* knowing whether a delayed conversion will occur — the
**delayed feedback problem**
[[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]].

- **Fixed waiting window**: delays labeling until a window elapses — long
  windows slow training-signal freshness; short windows mislabel future
  converters as negatives, biasing the model toward under-prediction
  [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]].
- **Stream-as-negative + duplicate-as-positive with importance weighting**:
  every impression is ingested as a negative immediately; if a conversion
  later arrives, a positive duplicate is inserted with an importance weight.
  This is effectively a *reweighted* cross-entropy loss, but the
  importance-weighting correction only partially removes bias
  [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]].
- **FTP ("Follow the Prophet")**: defines an idealized "prophet" model — the
  CVR model that would exist if every conversion's true label were observed
  instantly — and approximates it via a **learned aggregation policy over
  multiple time-windowed sub-models**, each trained on the conversion pattern
  observable within a different elapsed-time interval. The aggregation loss
  imitates the zero-delay prophet's output, outperforming fixed-window and
  duplicate/importance-weighting baselines on three industrial advertising
  datasets [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]].

**Inference**: FTP's multi-window aggregation can be read as a *meta-loss*
sitting on top of the pointwise cross-entropy losses from Section 1 and the
entire-space losses from Section 2 — it doesn't replace the underlying
CTR/CVR cross-entropy, it changes *which labels and weights* feed into that
cross-entropy at training time
[[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]
[[wiki/sources/esmm-entire-space-multi-task-model.md]].

## 4. Bandit / Regression Losses for Exploration

Outside the supervised CTR/CVR setting, ad systems use **contextual
bandits** for per-impression decisions (creative selection, budget
allocation) where exploration-exploitation tradeoffs matter.

- **LinUCB**: maintains, per arm, a **ridge regression** (L2-regularized
  squared-error loss) fit of "reward as a linear function of context":
  `theta_hat_a = (D_a^T D_a + I_d)^-1 D_a^T c_a`. At decision time, LinUCB
  scores each arm by predicted reward (from the ridge-regression fit) plus a
  confidence-bonus term `alpha * sqrt(x^T A^-1 x)`, where `A^-1` is literally
  the posterior covariance of the ridge regression read as Bayesian linear
  regression [[wiki/synthesis/what-is-linucb.md]]
  [[wiki/sources/linucb-contextual-bandit-news-recommendation.md]]. On ~36M
  Yahoo! Front Page events, LinUCB achieved a 12.5% CTR lift over a
  context-free bandit baseline, with the largest gains for low-traffic arms
  (cold start) [[wiki/sources/linucb-contextual-bandit-news-recommendation.md]].
  LinUCB-style contextual bandits are also used for fatigue-aware ad creative
  selection, where the context includes wear-in/wear-out exposure history
  [[wiki/sources/fatigue-aware-ad-creative-selection.md]].

The ridge-regression squared-error loss here serves a dual purpose: it both
fits the reward predictor *and*, via its closed-form posterior covariance,
directly produces the uncertainty estimate that drives exploration — a
single loss function doing double duty for prediction and confidence
[[wiki/synthesis/what-is-linucb.md]]
[[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]].

## 5. Uncertainty & Calibration Losses

A predicted probability is only useful for downstream auction math (eCPM,
LTV) if it is both a good *point estimate* and *correctly calibrated* — and
ad systems also need to know *how confident* that estimate is, to drive
exploration decisions
[[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]].

- **FTRL-Proximal's per-coordinate uncertainty score**: `u(x) = alpha * eta . x`
  is a heuristic confidence measure computed in a single sparse dot product
  (the same cost as the prediction itself), upper-bounding how much the
  model's log-odds score would change after observing one more training
  example with features x. It performed comparably to bootstrapping with 32
  models at a fraction of the cost
  [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]. This is
  not a *training* loss per se, but is derived directly from the same
  gradient accumulators (`n_i`, `z_i`) used by the FTRL-Proximal update
  [[wiki/entities/ftrl-proximal-algorithm.md]].
- **MC dropout (Monte Carlo dropout) for deep CTR models**: dropout is kept
  active at inference time; T stochastic forward passes are averaged,
  approximating a Bayesian posterior over the network's weights without
  explicit Bayesian layers. The training objective is still cross-entropy /
  NLL (with dropout), but predictive uncertainty is decomposed
  post-hoc into **epistemic** (mutual information across the T passes) and
  **aleatoric** (entropy of the averaged prediction) components. This
  improved Logloss by 0.19–0.42% and RMSE by 0.07–0.26% versus non-dropout
  baselines, and uncertainty estimates shrink as the training set grows
  [[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]
  [[wiki/sources/survey-uncertainty-deep-neural-networks-gawlikowski.md]].
- **Isotonic regression / Platt scaling for calibration**: a *post-hoc*
  correction, not part of the primary training loss — a piecewise-linear,
  monotonically increasing function tau(p) is fit to map predicted CTR to
  observed CTR, separately from the cross-entropy objective that trained the
  underlying model. McMahan et al.'s isotonic regression "significantly
  reduced bias at both high and low prediction ranges"
  [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
  [[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]].

**Inference**: across this family, only MC dropout's training objective
(cross-entropy with dropout) is a true *training* loss in the same sense as
Sections 1–2; the FTRL uncertainty score and isotonic/Platt calibration are
both *derived from* or *applied after* a primary loss, rather than being
separate end-to-end objectives — yet all three feed directly into
production decisions (confidence-aware serving, exploration, and
auction-pricing accuracy, respectively)
[[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]].

## 6. Ordinal / Tiered-Score Losses

Where a prediction target is an **ordered, discrete scale** — graded
relevance labels, quality tiers, star ratings — plain multi-class
cross-entropy and plain MSE are both suboptimal: cross-entropy ignores
ordinal distance (predicting class 1 vs. class 5 when the truth is 5 costs
the same as predicting class 4), and MSE on a numeric encoding of ordinal
labels assumes equal-sized gaps between categories that ordinal data doesn't
actually have [[wiki/concepts/ordinal-regression-loss.md]].

- **Binary decomposition (Frank & Hall)**: converts a K-class ordinal
  problem into K-1 binary "is the true label > r_k?" sub-problems, each
  trained with a standard probability-estimating classifier — requires no
  modification to the underlying algorithm, but independently-trained
  sub-classifiers can produce rank-inconsistent predictions
  [[wiki/concepts/ordinal-regression-loss.md]].
- **CORAL**: extends each label into K-1 binary tasks that **share a single
  weight vector** with per-task biases, trained with a weighted
  cross-entropy across the K-1 tasks. CORAL proves the learned biases satisfy
  b_1 >= b_2 >= ... >= b_{K-1}, guaranteeing rank-monotonic predictions by
  construction. On face-age benchmarks, CORAL-CNN reduced MAE versus plain
  cross-entropy and the rank-inconsistent OR-CNN baseline, with zero rank
  inconsistencies [[wiki/concepts/ordinal-regression-loss.md]].
- **CORN**: CORAL's successor — achieves rank consistency via conditional
  training on subsets rather than weight sharing
  [[wiki/concepts/ordinal-regression-loss.md]].
- **Cumulative-encoding + MSE**: encodes each ordinal label as a cumulative
  binary vector (e.g., "Medium" of 5 -> [1,1,1,0,0]) and trains
  multiple sigmoid outputs with MSE against the expanded target — a
  lightweight way to embed ordinal distance into the loss magnitude, with
  mixed empirical results across datasets
  [[wiki/concepts/ordinal-regression-loss.md]].

**Inference**: none of the ordinal-loss source pages describe a published ad
system that uses these losses directly, but the natural fit is Google's
predicted creative quality (pCQ) and predicted landing page quality (pLQ)
components of Ad Rank — *if* these are represented internally as discrete
ordered tiers, an ordinal loss like CORAL would guarantee rank-monotonic
tier probabilities, a property plain cross-entropy or unconstrained
regression do not provide
[[wiki/concepts/ordinal-regression-loss.md]]
[[wiki/concepts/google-ad-rank-ltv-scoring.md]].

## 7. Retrieval / Contrastive Embedding Losses

The retrieval stage of ad/recommendation delivery (finding ~1,000 candidates
from a catalog of 100M+ within ~20ms) is trained with a fundamentally
different loss family: **contrastive losses over embeddings**, not
classification losses over labels.

- **Two-tower in-batch-negative / sampled-softmax loss**: for a batch of B
  positive (user, item) pairs, every other item in the batch serves as a
  negative for each user — an InfoNCE / batch-softmax loss that is "free"
  because the forward pass already computed all embeddings
  [[wiki/synthesis/two-tower-factorized-models.md]]. **Sampling bias
  correction** is critical: popular items appear as negatives in more
  batches, so the model subtracts log q(i) (item i's sampling probability)
  from its logit before softmax — skipping this silently degrades long-tail
  performance [[wiki/sources/two-tower-models-engineers-of-ai.md]]. Key
  hyperparameters are batch size (1024-4096) and temperature tau
  (0.05-0.2, often learned)
  [[wiki/synthesis/two-tower-factorized-models.md]].

This loss optimizes for **relative** similarity (is the positive item closer
to the user embedding than the in-batch negatives?), in contrast to the
**absolute** probability calibration that cross-entropy CTR/CVR losses (and
isotonic calibration) target — a two-tower retrieval score is not, and is not
meant to be, a calibrated probability
[[wiki/synthesis/two-tower-factorized-models.md]]
[[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]].

## 8. Multi-Granularity Embedding Losses (Matryoshka)

**Matryoshka Representation Learning (MRL)** modifies the loss used to train
an embedding so that every *prefix* of the embedding vector (e.g., the first
8, 16, 32, ... dimensions of a 2048-d vector) is independently useful, not
just the full vector. Instead of minimizing a single task loss
`L(W * F(x), y)` on the full d-dimensional embedding, MRL jointly minimizes,
for each nested size m in a set M, the same task loss computed on only the
first m coordinates via a per-granularity head W^(m):

```
min  (1/N) * sum_i sum_{m in M} c_m * L( W^(m) * F(x_i)[1:m], y_i )
```

[[wiki/concepts/matryoshka-representation-learning.md]]. The Sentence
Transformers library implements this as `MatryoshkaLoss`, a wrapper that
sums any base contrastive/similarity loss (e.g., `MultipleNegativesRankingLoss`,
the same family as the two-tower in-batch-negative loss above) across several
truncated dimensions into one final loss value
[[wiki/concepts/matryoshka-representation-learning.md]].

**Inference**: MRL is not a new loss *family* so much as a **wrapper** around
an existing loss (classification cross-entropy on ImageNet, or contrastive
similarity loss for text/retrieval embeddings) — applied redundantly across
multiple embedding-prefix lengths. For two-tower retrieval specifically, MRL
could wrap the in-batch-negative/sampled-softmax loss from Section 7 so a
single trained item-embedding index supports both a cheap low-dimensional
shortlist pass and a higher-dimensional re-rank pass from the *same* vectors
— though no source describes this combination as implemented in a production
ad system [[wiki/concepts/matryoshka-representation-learning.md]]
[[wiki/synthesis/two-tower-factorized-models.md]].

## 9. Generative Retrieval / Quantization Losses (Semantic IDs)

**Semantic IDs (SIDs)** replace traditional item IDs with a discrete tuple of
codewords (c0, c1, c2, ...) produced by quantizing a dense content embedding,
then train a sequence-to-sequence model to autoregressively decode the next
item's SID tokens from a user's past SID sequence
[[wiki/synthesis/semantic-id.md]].

- **RQ-VAE quantization (TIGER)**: TIGER's pipeline encodes item content via
  a pre-trained encoder (e.g., SentenceT5) into a dense embedding, then
  quantizes it via **Residual Vector Quantization-VAE (RQ-VAE)** into a
  hierarchical codeword tuple, with each residual level captured by a
  separate learned codebook
  [[wiki/synthesis/semantic-id.md]]
  [[wiki/sources/tiger-transformer-index-generative-recommenders.md]].
  *Inference: RQ-VAE training combines a reconstruction loss (decoded
  embedding vs. original dense embedding) with commitment and codebook
  losses standard to VQ-VAE-family quantizers — the source pages describe
  RQ-VAE only as "learned hierarchical codebooks" and do not spell out the
  individual loss terms, so the reconstruction/commitment/codebook
  decomposition here is general VQ-VAE knowledge, not a claim stated in the
  ingested sources.*
- **Seq2seq cross-entropy for autoregressive SID decoding**: the
  sequence-to-sequence Transformer (T5-style) that decodes the next item's
  SID tokens is trained with standard autoregressive **token-level
  cross-entropy** — the same loss family as Section 1, but over a vocabulary
  of codeword tokens rather than a binary click/no-click label
  [[wiki/synthesis/semantic-id.md]]. TIGER outperformed SASRec, BERT4Rec, and
  other SOTA dense sequential models, and demonstrated cold-start
  generalization (unseen items map to existing semantic clusters)
  [[wiki/synthesis/semantic-id.md]].
- **SIDs as ranking-model inputs**: beyond generative retrieval, SIDs from
  RQ-VAE (L=8, K=2048) can replace item IDs directly in a multi-task ranking
  model's embedding tables (Singh et al., YouTube scale), trained with the
  ranking model's own multi-task losses (Sections 1-2) rather than a
  separate quantization loss at this stage — the SID is just a different
  (semantically structured) key into the embedding table
  [[wiki/sources/better-generalization-semantic-ids-ranking.md]]
  [[wiki/synthesis/semantic-id.md]].

**Inference**: Semantic IDs sit at the intersection of two loss families in
this page — the quantizer (RQ-VAE) is trained with a reconstruction-style
loss closer in spirit to the embedding losses of Sections 7-8, while the
downstream seq2seq retrieval model and ranking-model adaptation are trained
with cross-entropy losses closer in spirit to Sections 1 and 6
[[wiki/synthesis/semantic-id.md]].

## Comparison Table

| Loss family | Core idea / formula sketch | Used in (system/model) | What it optimizes for |
|---|---|---|---|
| **Binary cross-entropy / log loss (online, L1/L2-regularized)** | Logistic loss + L1 (sparsity) + L2 (shrinkage); per-coordinate FTRL-Proximal update | Google's production CTR system [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] [[wiki/entities/ftrl-proximal-algorithm.md]] | Calibrated click probability at billion-coefficient scale with a sparse model |
| **Binary cross-entropy / log loss (FM+DNN)** | sigmoid(FM order-1/2 terms + DNN output), trained end-to-end with logloss | DeepFM [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]] | CTR with implicit feature interactions, no manual cross-features |
| **Entire-space multi-task cross-entropy (CTR + CTCVR)** | Joint CE losses for P(click) and P(click & conversion) = pCTR x pCVR, both over all impressions | ESMM [[wiki/sources/esmm-entire-space-multi-task-model.md]] | Unbiased pCVR over the entire impression space (fixes sample selection bias) |
| **Per-task cross-entropy with expert/gate sharing** | Each task (CTR, CVR, watch-time, ...) keeps its own CE loss; CGC layers control which experts/gradients each task sees | PLE [[wiki/sources/ple-progressive-layered-extraction-multitask.md]] | Avoiding seesaw/negative transfer between jointly-trained task losses |
| **Delayed-feedback aggregation loss** | Learned aggregation over multiple elapsed-time-windowed sub-models approximating a zero-delay "prophet" CE loss | FTP [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]] | Unbiased, timely CVR labels despite multi-day conversion delays |
| **Ridge regression (L2-regularized squared loss)** | `theta_hat = (D^T D + I)^-1 D^T c`; posterior covariance A^-1 gives confidence bonus | LinUCB [[wiki/synthesis/what-is-linucb.md]] [[wiki/sources/linucb-contextual-bandit-news-recommendation.md]] | Reward prediction + exploration bonus per arm (creative, targeting, budget) |
| **NLL / cross-entropy with MC dropout** | T stochastic forward passes (dropout active), averaged; epistemic = mutual info, aleatoric = entropy | Bayesian deep CTR [[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]] [[wiki/sources/survey-uncertainty-deep-neural-networks-gawlikowski.md]] | Decomposed predictive uncertainty for deep CTR models |
| **Isotonic regression (post-hoc calibration)** | Piecewise-linear monotonic tau(p) fit to map predicted -> observed CTR, applied after the primary loss | Google CTR calibration [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] | Correcting absolute pCTR/pCVR scale for auction pricing (eCPM/LTV) |
| **Ordinal losses (CORAL/CORN, binary decomposition, cumulative MSE)** | K-1 rank-consistent binary tasks (shared weights + per-task biases for CORAL) or cumulative-encoding + MSE | Ordinal/age-estimation benchmarks [[wiki/concepts/ordinal-regression-loss.md]] | Rank-monotonic predictions over ordered tiers (graded relevance, quality tiers) |
| **In-batch-negative / sampled-softmax (InfoNCE)** | Batch softmax over (user, item) pairs with log q(i) sampling-bias correction; temperature tau | Two-tower retrieval [[wiki/synthesis/two-tower-factorized-models.md]] [[wiki/sources/two-tower-models-engineers-of-ai.md]] | Relative embedding similarity for ANN retrieval from 100M+ candidates |
| **Multi-granularity nested loss (Matryoshka)** | Sum of base loss L over multiple embedding-prefix lengths m in M, each with its own head W^(m) | MRL / Matryoshka embeddings [[wiki/concepts/matryoshka-representation-learning.md]] | A single embedding whose truncated prefixes are each independently usable |
| **RQ-VAE quantization loss** | Reconstruction of dense content embedding via hierarchical residual codebooks | TIGER Semantic IDs [[wiki/synthesis/semantic-id.md]] [[wiki/sources/tiger-transformer-index-generative-recommenders.md]] | Discrete, semantically-structured item codes for generative retrieval |
| **Autoregressive token cross-entropy** | Standard seq2seq CE over a vocabulary of Semantic ID codeword tokens | TIGER decoder [[wiki/synthesis/semantic-id.md]] | Generating the next item's SID tokens via beam search |

## Cross-Cutting Observations

- **Inference**: Most of the loss families above ultimately reduce to one of
  two primitives — **cross-entropy/log loss** (Sections 1, 2, 5's MC-dropout
  variant, 6's CORAL/CORN, 7's InfoNCE, 9's seq2seq decoder) or
  **L2-regularized squared loss / ridge regression** (Section 4's LinUCB,
  Section 1's L2 term in FTRL-Proximal). What differs across systems is
  *what the label is* (click, conversion, next-token, reward, ordinal tier,
  in-batch positive/negative) and *what wraps around* the core loss
  (entire-space sampling in ESMM, multi-window aggregation in FTP, expert
  gating in PLE, sampling-bias correction in two-tower, multi-granularity
  summation in MRL).
- **Inference**: calibration (Section 5) is the one family that is explicitly
  *not* a training-time loss in any source — it is a deliberate post-hoc
  step, which matters because every other family here produces a *score*,
  but only a calibrated score can be plugged directly into eCPM/LTV auction
  math [[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]]
  [[wiki/synthesis/what-is-ad-rank.md]].

## Open Questions

- Open question: none of the pages read for this synthesis cover **pairwise
  or listwise learning-to-rank losses** (e.g., RankNet, LambdaMART/LambdaRank,
  softmax listwise losses) — which are a standard part of the ranking-stage
  loss landscape in large-scale recommendation/ads systems and would sit
  alongside the pointwise CTR/CVR losses in Section 1 and the ordinal losses
  in Section 6. This is a gap in the wiki's current loss-function coverage.

## Related Pages

- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/entities/ftrl-proximal-algorithm.md]]
- [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]]
- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/ple-progressive-layered-extraction-multitask.md]]
- [[wiki/synthesis/model-structures-for-pcvr.md]]
- [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]
- [[wiki/synthesis/what-is-linucb.md]]
- [[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]
- [[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]]
- [[wiki/synthesis/two-tower-factorized-models.md]]
- [[wiki/synthesis/semantic-id.md]]
- [[wiki/sources/transact-v2-pinterest.md]]
- [[wiki/concepts/ordinal-regression-loss.md]]
- [[wiki/concepts/matryoshka-representation-learning.md]]
