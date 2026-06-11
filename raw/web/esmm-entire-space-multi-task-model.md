# Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate

Source: https://arxiv.org/abs/1804.07931 (arXiv:1804.07931)

**Authors:** Xiao Ma, Liqin Zhao, Guan Huang, Zhi Wang, Zelin Hu, Xiaoqiang Zhu, Kun Gai (Alibaba)
**Venue:** SIGIR 2018
**Submitted:** April 21, 2018

## Abstract / Summary

Estimating post-click conversion rate (CVR) accurately is crucial for ranking
systems in industrial applications such as recommendation and advertising.
Conventional CVR modeling applies popular deep learning methods and achieves
state-of-the-art performance. However it encounters several task-specific
problems in practice, making CVR modeling challenging.

- **Sample selection bias (SSB)**: conventional CVR models are trained on
  clicked-and-converted-or-not samples (i.e., the dataset is built only from
  impressions that received a click), but applied to predict on the entire
  space of all impressions. This means the training data and the data used at
  inference time come from different distributions, biasing the model.
- **Data sparsity (DS)**: conversions are far rarer than clicks, so the
  clicked-sample training set used by conventional CVR models is orders of
  magnitude smaller than the impression set used by CTR models, leading to a
  data sparsity problem that hurts model fitting.

## Proposed Solution: ESMM

ESMM (Entire Space Multi-task Model) addresses both problems by exploiting the
sequential pattern of user actions: **impression -> click -> conversion**.
Instead of directly modeling CVR = P(conversion | click) on the clicked
subspace, ESMM introduces two auxiliary tasks defined over the *entire*
impression space:

- **CTR**: P(click | impression)
- **CTCVR**: P(click and conversion | impression) = P(click | impression) x
  P(conversion | click, impression)

CVR is then a sub-network shared between the CTCVR and CTR towers; its output
is multiplied by the CTR tower's output to produce the CTCVR prediction. Both
CTR and CTCVR are estimated over the entire space of impressions (where labels
are always available, unlike CVR labels which only exist for clicked
impressions), so:

1. **SSB is eliminated** — the CVR sub-network's parameters are trained via
   gradients flowing from the entire-space CTCVR loss, not from a
   clicked-only subspace.
2. **DS is mitigated** — the CVR sub-network shares embedding-layer parameters
   with the CTR sub-network, which is trained on much more abundant
   click/no-click labels across all impressions (transfer learning of feature
   representations).

## Key Results

- Evaluated on Taobao production traffic logs and a newly released public
  dataset (Product, sampled from Taobao recommender system logs) containing
  sequential click->conversion sample data — the first such public benchmark
  for CVR research.
- ESMM significantly outperforms competitive CVR modeling methods (e.g.,
  naive deep CVR models trained on clicked impressions, and the
  oversampling-based DivisionModel) on both CVR (clicked-impression AUC) and
  CTCVR (entire-space AUC) metrics.
- The entire-space, multi-task framework is model-agnostic — any base
  network for the CVR/CTR sub-networks can be substituted.

## Relevance

ESMM is the canonical production architecture for **post-click CVR
prediction** (pCVR), the signal that feeds Smart Bidding and oCPM/CPA bid
strategies in ad ranking systems
[[raw/web/google-ads-about-conversions.md]]. It directly explains *how* pCVR
models avoid being trained on a biased (clicked-only) sample while still
producing well-calibrated probabilities across the full impression space that
the auction scores every candidate against.
