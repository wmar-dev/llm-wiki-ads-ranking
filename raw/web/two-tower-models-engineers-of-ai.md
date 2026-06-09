Source: https://engineersofai.com/docs/ml/recommender-systems/Two-Tower-Models

Two-Tower Models - The Architecture Powering Google, TikTok, and YouTube | EngineersOfAI - Technical Education for AI Engineers

---

Reading time: ~40 minutes | Level: Recommender Systems | Role: MLE, AI Engineer, MLOps

---

## The Constraint That Changed Everything

Picture a TikTok engineer at their desk in 2020. The app has crossed 1 billion active users. Every time someone opens TikTok - which happens billions of times a day - the system has roughly 100 milliseconds to find the best 50 videos from a catalog of over 100 million items. That is the product requirement: 100ms, 100 million items, 1 billion users, billions of requests per day.

Run the numbers on a NeuMF model. A single forward pass for one user-item pair takes about 0.1 milliseconds on a modern GPU. For one user, scoring all 100 million items would take 10,000 seconds - nearly three hours, even batched aggressively. You would need millions of GPUs dedicated to a single user's request to hit the 100ms target. That is not a resource problem you can throw hardware at. It is a fundamental architectural incompatibility.

The breakthrough that solved this - that made billion-scale real-time recommendation physically possible - came from a deceptively simple architectural constraint. What if you could design the model so that the user computation and the item computation were completely independent? If you could precompute item representations offline and store them in a fast lookup structure, then at serving time you would only need to: (1) compute the user representation in real time (one forward pass, ~1ms), and (2) find the nearest precomputed item vectors (approximate nearest neighbor search, ~5-10ms). Total: under 15ms for a billion-item catalog.

This is the two-tower model. The name describes the architecture: a user tower that processes user features into a single user embedding, and a separate item tower that processes item features into a single item embedding. The two towers are trained jointly, but they are architecturally independent - the user tower's computation never touches item features, and the item tower's computation never touches user features. This constraint is the entire point. It is what makes precomputation possible.

The two-tower model is now the dominant architecture for the retrieval stage of large-scale recommendation systems. Google uses it in YouTube. TikTok uses it. Pinterest uses it. Spotify uses it.

---

## Why This Exists

The previous lesson covered NeuMF: a powerful model that concatenates user and item embeddings and passes them through a deep network. NeuMF is expressive and accurate. It is also architecturally unsuitable for real-time retrieval at scale.

The problem is user-item coupling at inference time. In any model where the user and item representations are processed jointly - concatenated, attended over, or otherwise mixed before the final prediction - you cannot precompute anything. You must run the entire forward pass for every user-item pair you want to score.

Two-tower imposes the strongest possible constraint: the final similarity score must be decomposable as a function of independent user and item representations:

s(u,i) = <f_theta(x_u), g_phi(x_i)>

The user tower f_theta maps user features x_u to a user embedding. The item tower g_phi maps item features x_i to an item embedding. The score is their dot product (or cosine similarity). Because the two towers share no parameters and have no information flow between them, item embeddings can be computed once and stored. User embeddings are computed at query time. The nearest stored item embeddings are retrieved with FAISS.

This architectural constraint is the reason two-tower models are slightly less expressive than joint models - the model cannot leverage fine-grained user-item feature interactions during the forward pass. But at retrieval scale, this is an acceptable trade-off. The retrieval stage does not need to be perfect; it needs to produce a set of 1,000 plausible candidates that a more expressive ranking model can then re-score.

---

## Historical Context

### The Foundational Papers

**DSSM (2013)** - Huang et al., "Learning Deep Structured Semantic Models for Web Search using Clickthrough Data," Microsoft Research. The first large-scale dual-encoder trained with click signals. Used for document retrieval in Bing. Established the in-batch negative training approach.

**YouTube DNN (2016)** - Covington et al., "Deep Neural Networks for YouTube Recommendations." Google's paper describing their two-stage system: a deep retrieval model followed by a deep ranking model. The retrieval model is a precursor to the modern two-tower: it outputs a single user embedding, finds nearest neighbors in the item embedding space, and passes candidates to the ranking model.

**Sampling-Bias-Corrected Neural Modeling (2019)** - Yi et al., Google Brain. The paper that formalized the modern two-tower training with in-batch negatives and introduced the crucial sampling bias correction technique. This is the paper that most practitioners reference when they say "two-tower."

**FAISS (2021)** - Johnson et al., Meta AI. The library that made billion-scale approximate nearest neighbor search practical.

### The "Aha Moment"

The key insight that Yi et al. formalized was that the two-tower architecture creates a natural tension: the model is trained to distinguish the correct item for a user from negative items, but at training time the negatives are sampled from the same batch. Popular items appear as negatives more often (because they are more likely to be someone else's positive in the batch). This biases the model against popular items - exactly the opposite of the popularity bias you usually worry about. The solution (sampling bias correction) is both mathematically elegant and practically critical.

---

## Core Concepts

### Concept 1: The Two-Tower Architecture

The defining equation:

s(u,i) = <f_theta(x_u), g_phi(x_i)>

where:
- x_u is the user feature vector (user ID, demographics, watch history, search history, device, time-of-day, etc.)
- x_i is the item feature vector (item ID, category, tags, duration, creator features, content embeddings, etc.)
- f_theta: R^d_u -> R^k is the user tower - a deep neural network mapping user features to a k-dimensional embedding
- g_phi: R^d_i -> R^k is the item tower - a separate deep neural network mapping item features to the same k-dimensional space
- dot product or cosine similarity

Both towers can be arbitrarily complex - they can include attention layers, recurrent layers, cross-feature interactions within each tower. The only architectural constraint is that no information crosses from one tower to the other.

The output dimension k is typically 64-256. Smaller k means faster ANN search but less expressive representations. Larger k stores more information but increases memory and search latency.

### Concept 2: Training with In-Batch Negatives

Two-tower models are almost always trained with in-batch negatives (also called batch softmax or sampled softmax).

Given a batch of B (user, item) positive pairs, treat every other item in the batch as a negative for each user. The loss is InfoNCE / NT-Xent as used in contrastive learning (SimCLR, CLIP).

Why in-batch negatives? Because they are free. Every forward pass already computes all item embeddings in the batch. Using them as negatives adds zero additional computation. With batch size 2048, you get 2047 negatives per positive.

Temperature tau controls the sharpness of the distribution. Values in [0.05, 0.2] work well for most recommendation problems.

### Concept 3: Sampling Bias Correction

In-batch negatives introduce a subtle but serious bias. Items are sampled into batches proportionally to their popularity. This means popular items appear as negatives much more often than rare items. The model interprets "item appears as negative often" as "item is generally bad."

Yi et al.'s fix: subtract the log of the item's sampling probability from its logit before computing the softmax: s'(u,i) = s(u,i) - log q(i).

The correction penalizes the model for scoring an item high beyond what its popularity already predicts. A popular item gets its logit heavily penalized, so the model only recommends it if it genuinely fits the user. An unpopular item gets a logit bonus, making it easier for the model to recommend niche items.

### Concept 4: Serving - FAISS and ANN Search

At serving time:
1. Offline: run all items through the item tower. Store in a FAISS index.
2. Online: compute user embedding (1 forward pass), query FAISS for top-1000 nearest item embeddings, return candidates.

FAISS index types (fastest to most accurate):
- IndexFlatL2: exact search, up to ~1M items
- IndexIVFFlat: IVF with exact inner-cluster search, up to ~100M items
- IndexIVFPQ: IVF + product quantization, billions in RAM
- IndexHNSW: graph-based, excellent recall-latency trade-off

### Concept 5: Production Pipeline

Multi-stage: retrieval (two-tower) -> pre-ranking (light model) -> ranking (heavy model / NeuMF / DIN / DLRM) -> post-processing (diversity, freshness, safety).

---

## Common Mistakes

1. Not correcting for sampling bias: model systematically under-recommends popular items.
2. Using the same model for retrieval and ranking: two-tower cannot learn cross-feature interactions.
3. Item embedding staleness: FAISS index may contain old embeddings after model retraining.
4. Small batch size: two-tower models need batches of 1024-4096. Use gradient accumulation if needed.

---

## Key Fact

Two-tower imposes the strongest possible constraint: the final similarity score must be decomposable as a function of independent user and item representations. This is the reason two-tower models are slightly less expressive than joint models - the model cannot leverage fine-grained user-item feature interactions during the forward pass. But at retrieval scale, this is an acceptable trade-off. The retrieval stage does not need to be perfect; it needs to produce a set of 1,000 plausible candidates that a more expressive ranking model can then re-score.
