# DeepFM: A Factorization-Machine based Neural Network for CTR Prediction

Source: https://arxiv.org/abs/1703.04247 (arXiv:1703.04247)

**Authors:** Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He (Huawei Noah's Ark Lab)
**Venue:** IJCAI 2017
**Submitted:** March 13, 2017

## Problem Addressed

Learning sophisticated **feature interactions** behind user behavior is critical
for CTR (and CVR) prediction, but existing approaches each have a blind spot:

- **Factorization Machines (FM)** model pairwise (low-order) feature
  interactions well via learned latent vectors, but don't capture higher-order
  interactions.
- **Deep neural networks** capture high-order, non-linear interactions but are
  weak at the low-order interactions FM handles natively.
- **Wide & Deep** (Google) combines a linear "wide" component with a "deep"
  component, but the wide component still requires manual feature-engineering
  (cross-product feature transformations) to capture low-order interactions.

## DeepFM Architecture

DeepFM replaces Wide & Deep's hand-engineered wide component with an **FM
component**, and shares a single embedding layer between the FM component and
the deep component:

- **FM component**: models order-1 (linear) and order-2 (pairwise) feature
  interactions via the FM formulation, operating directly on the shared
  embeddings.
- **Deep component**: a standard feed-forward DNN over the same shared
  embeddings, learning higher-order, implicit feature interactions.
- **Output**: the FM and deep component outputs are summed (then passed
  through a sigmoid) to produce the final prediction.

Because both components consume the same embedding vectors and require **no
manual feature engineering** beyond raw categorical/numerical inputs, DeepFM
trains end-to-end and avoids the cross-feature engineering cost of Wide & Deep.

## Key Results

Experiments on benchmark and commercial (Huawei App Store) datasets showed
DeepFM outperforming logistic regression, standalone FM, and Wide & Deep on
CTR prediction AUC/Logloss, while being more efficient to train than models
requiring separate feature-engineering pipelines.

## Relevance

DeepFM is one of the standard **feature-interaction backbone architectures**
used for the CTR and CVR towers inside production ranking models — it
represents the "what neural network actually computes pCTR/pCVR from raw
features" layer, complementary to ESMM's entire-space multi-task framing
(which addresses *which population* the CVR tower trains on, not *what
architecture* the tower itself uses)
[[raw/web/esmm-entire-space-multi-task-model.md]].
