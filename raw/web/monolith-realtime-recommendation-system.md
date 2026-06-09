---
title: "Monolith: Real Time Recommendation System With Collisionless Embedding Table"
source_url: "https://arxiv.org/abs/2209.07663"
fetched: "2026-06-09"
---

# Monolith: Real Time Recommendation System With Collisionless Embedding Table

Zhuoran Liu (ByteDance), Leqi Zou (ByteDance), Xuan Zou (ByteDance), Caihua Wang (ByteDance), Biao Zhang (ByteDance), Da Tang (ByteDance), Bolin Zhu (Fudan University), Yijie Zhu (ByteDance), Peng Wu (ByteDance), Ke Wang (ByteDance), Youlong Cheng (ByteDance)

Published at ORSUM@ACM RecSys 2022

## Abstract

Building a scalable and real-time recommendation system is vital for many businesses driven by time-sensitive customer feedback, such as short-videos ranking or online ads. Despite the ubiquitous adoption of production-scale deep learning frameworks like TensorFlow or PyTorch, these general-purpose frameworks fall short of business demands in recommendation scenarios for various reasons: on one hand, tweaking systems based on static parameters and dense computations for recommendation with dynamic and sparse features is detrimental to model quality; on the other hand, such frameworks are designed with batch-training stage and serving stage completely separated, preventing the model from interacting with customer feedback in real-time. These issues led us to reexamine traditional approaches and explore radically different design choices. In this paper, we present Monolith, a system tailored for online training. Our design has been driven by observations of our application workloads and production environment that reflects a marked departure from other recommendations systems. Our contributions are manifold: first, we crafted a collisionless embedding table with optimizations such as expirable embeddings and frequency filtering to reduce its memory footprint; second, we provide an production-ready online training architecture with high fault-tolerance; finally, we proved that system reliability could be traded-off for real-time learning. Monolith has successfully landed in the BytePlus Recommend product.

## 1. Introduction

The past decade witnessed a boom of businesses powered by recommendation techniques. In pursuit of a better customer experience, delivering personalized content for each individual user as real-time response is a common goal of these business applications. To this end, information from a user's latest interaction is often used as the primary input for training a model, as it would best depict a user's portrait and make predictions of user's interest and future behaviors.

Deep learning have been dominating recommendation models (Covington et al., 2016; Gupta et al., 2020; Xie et al., 2020; Zhao et al., 2019; Jiang et al., 2019; Cheng et al., 2016) as the gigantic amount of user data is a natural fit for massively data-driven neural models. However, efforts to leverage the power of deep learning in industry-level recommendation systems are constantly encountered with problems arising from the unique characteristics of data derived from real-world user behavior. These data are drastically different from those used in conventional deep learning problems like language modeling or computer vision in two aspects:

1. The features are mostly sparse, categorical and dynamically changing;
2. The underlying distribution of training data is non-stationary, a.k.a. Concept Drift.

Such differences have posed unique challenges to researchers and engineers working on recommendation systems.

### 1.1. Sparsity and Dynamism

The data for recommendation mostly contain sparse categorical features, some of which appear with low frequency. The common practice of mapping them to a high-dimensional embedding space would give rise to a series of issues:

- Unlike language models where number of word-pieces are limited, the amount of users and ranking items are orders of magnitude larger. Such an enormous embedding table would hardly fit into single host memory;
- Worse still, the size of embedding table is expected to grow over time as more users and items are admitted, while frameworks like TensorFlow and PyTorch uses a fixed-size dense variables to represent embedding table.

In practice, many systems adopt low-collision hashing (Covington et al., 2016; Bredillet, 2019) as a way to reduce memory footprint and to allow growing of IDs. This relies on an over-idealistic assumption that IDs in the embedding table is distributed evenly in frequency, and collisions are harmless to the model quality. Unfortunately this is rarely true for a real-world recommendation system, where a small group of users or items have significantly more occurrences. With the organic growth of embedding table size, chances of hash key collision increases and lead to deterioration of model quality.

Therefore it is a natural demand for production-scale recommendation systems to have the capacity to capture as many features in its parameters, and also have the capability of elastically adjusting the number of users and items it tries to book-keep.

### 1.2. Non-stationary Distribution

Visual and linguistic patterns barely develop in a time scale of centuries, while the same user interested in one topic could shift their zeal every next minute. As a result, the underlying distribution of user data is non-stationary, a phenomenon commonly referred to as Concept Drift.

Intuitively, information from a more recent history can more effectively contribute to predicting the change in a user's behavior. To mitigate the effect of Concept Drift, serving models need to be updated from new user feedback as close to real-time as possible to reflect the latest interest of a user.

In light of these distinction and in observation of issues that arises from our production, we designed Monolith, a large-scale recommendation system to address these pain-points. Monolith is able to:

1. Provide full expressive power for sparse features by designing a collisionless hash table and a dynamic feature eviction mechanism;
2. Loop serving feedback back to training in real-time with online training.

Empowered by these architectural capacities, Monolith consistently outperforms systems that adopts hash-tricks with collisions with roughly similar memory usage, and achieves state-of-the-art online serving AUC without overly burdening our servers' computation power.

## 2. Design

The overall architecture of Monolith generally follows TensorFlow's distributed Worker-ParameterServer setting. In a Worker-PS architecture, machines are assigned different roles; Worker machines are responsible for performing computations as defined by the graph, and PS machines stores parameters and updates them according to gradients computed by Workers.

In recommendation models, parameters are categorized into two sets: dense and sparse. Dense parameters are weights/variables in a deep neural network, and sparse parameters refer to embedding tables that corresponds to sparse features. In our design, both dense and sparse parameters are part of TensorFlow Graph, and are stored on parameter servers.

### 2.1. Hash Table

A first principle in our design of sparse parameter representation is to avoid cramping information from different IDs into the same fixed-size embedding. Simulating a dynamic size embedding table with an out-of-the-box TensorFlow Variable inevitably leads to ID collision, which exacerbates as new IDs arrive and table grows. Therefore instead of building upon Variable, we developed a new key-value HashTable for our sparse parameters.

Our HashTable utilizes Cuckoo Hashmap under the hood, which supports inserting new keys without colliding with existing ones. Cuckoo Hashing achieves worst-case O(1) time complexity for lookups and deletions, and an expected amortized O(1) time for insertions. It maintains two tables T0, T1 with different hash functions h0(x), h1(x), and an element would be stored in either one of them. When trying to insert an element A into T0, it first attempts to place A at h0(A); If h0(A) is occupied by another element B, it would evict B from T0 and try inserting B into T1 with the same logic. This process will be repeated until all elements stabilize, or rehash happens when insertion runs into a cycle.

Memory footprint reduction is also an important consideration. A naive approach of inserting every new ID into the HashTable will deplete memory quickly. Observation of real production models lead to two conclusions:

1. IDs that appears only a handful of times have limited contribution to improving model quality. IDs are long-tail distributed, where popular IDs may occur millions of times while the unpopular ones appear no more than ten times. Embeddings corresponding to these infrequent IDs are underfit due to lack of training data.
2. Stale IDs from a distant history seldom contribute to the current model as many of them are never visited. This could be due to a user that is no longer active, or a short-video that is out-of-date.

Based on these observations, we designed several feature ID filtering heuristics:

1. IDs are filtered before they are admitted into embedding tables. Two filtering methods: frequency threshold (tunable hyperparameter) and a probabilistic filter to further reduce memory usage.
2. IDs are timed and set to expire after being inactive for a predefined period of time. The expire time is tunable for each embedding table.

The HashTable is implemented as a TensorFlow resource operation. Like Variable, look-ups and updates are implemented as native TensorFlow operations.

### 2.2. Online Training

In Monolith, training is divided into two stages:

1. Batch training stage. Works as an ordinary TensorFlow training loop. In each step, a training worker reads a mini-batch of examples from storage, requests parameters from PS, computes forward and backward pass, and pushes updated parameters to the training PS. The dataset is only trained for one pass.
2. Online training stage. After a model is deployed to online serving, the training does not stop. Instead of reading mini-batch examples from storage, a training worker consumes realtime data on-the-fly and updates the training PS. The training PS periodically synchronizes its parameters to the serving PS, which takes effect immediately.

#### 2.2.1. Streaming Engine

Monolith uses one Kafka queue to log actions of users (e.g., click, like) and another Kafka queue for features. At the core is a Flink streaming job for online feature Joiner. The online joiner concatenates features with labels from user actions and produces training examples, which are then written to a Kafka queue consumed by both online and batch training.

#### 2.2.2. Online Joiner

User action logs and features are streamed without time order guarantee. A unique key per request ensures correct pairing. The lag of user action is handled via an on-disk key-value storage for features waiting over a certain time period. The distribution of negative and positive examples is highly uneven, so negative sampling is applied with log odds correction during serving as an unbiased estimator.

#### 2.2.3. Parameter Synchronization

Key insights enabling efficient synchronization:

1. Sparse parameters dominate model size.
2. Within a short time window, only a small subset of IDs get trained and updated.
3. Dense variables move much slower than sparse embeddings due to momentum accumulation at scale.

Monolith maintains a hash set of touched keys (IDs whose embeddings got trained since last sync). It pushes the subset of sparse parameters with touched keys at minute-level intervals. Dense parameters are synced less frequently (day-level). This dramatically reduces network I/O.

### 2.3. Fault Tolerance

Monolith snapshots all training PS every day. Although a PS loses one day's updates in case of failure, the performance degradation is tolerable. With a 0.01% failure rate per day and 1000 PS shards, one PS fails every 10 days. For a DAU of 15M with even distribution, this means losing 1 day's feedback from 15,000 users every 10 days — negligible for both sparse and dense parameters.

## 3. Evaluation

### 3.1. Experimental Setup

#### 3.1.1. Embedding Table

Two groups of experiments:

1. **MovieLens ml-25m dataset**: ~162K users, ~62K movies. Standard DeepFM model. Comparison of collisionless vs MD5-hash-collision embedding tables. Collision rate: 7.73% for user IDs, 2.86% for movie IDs. The collisionless version consistently outperformed.
2. **Internal Recommendation dataset**: Production model with ~1000 embedding tables using 2^48 ID space. Baseline used hashing trick decomposition to 2^25. Compared via online AUC with real serving traffic.

#### 3.1.2. Online Training

Two groups of experiments:

1. **Update frequency**: Criteo Display Ads Challenge dataset (7 days chronologically ordered). 5 days batch training, 2 days for online training. Simulated sync intervals of 5hr, 1hr, 30min. DeepFM model.
2. **Live experiment**: A/B test on an Ads model in production comparing online training vs batch training.

### 3.2. Results and Analysis

#### 3.2.1. The Effect of Embedding Collision

Models with collisionless HashTable consistently outperform collision-based counterparts regardless of training epochs or concept drift. No overfitting observed with collisionless tables.

#### 3.2.2. Online Training: Trading-off Reliability for Realtime

- Higher parameter synchronization frequency consistently improves online serving AUC.
- Criteo results: Sync every 30min achieved highest AUC (79.80 ± 0.008) vs 5hr sync (79.66 ± 0.020). All online training variants outperformed batch training (~79.43).
- Live A/B experiment on an Ads model showed AUC improvement of 14–18% across 7 days.
- PS reliability: With daily snapshots and 0.01% failure rate, model quality loss was negligible. This allowed a radical reduction in snapshot frequency, saving computation overhead.

## 4. Related Work

Prior work on sparse feature representation includes:
- Fixed-size embedding table with hash-trick: Covington et al. (YouTube), Bredillet (Instagram)
- Collision-reducing hashing: Egg (Grubhub), Bredillet
- Native key-value hash tables for dynamic growth: Xie et al. (Kraken), Jiang et al. (XDL), Meituan, Zhao et al. (AIBox)
- Online training: Jiang et al. (XDL), Lian et al. (Persia)

Monolith's hash-table is a native TensorFlow operation — developer-friendly with high cross-platform interoperability, suitable for ToB scenarios. Its parameter synchronization is more lightweight than prior approaches.

## 5. Conclusion

Monolith provides a general solution for production-scale recommendation systems with:
1. Collisionless embedding table (Cuckoo HashMap based) proven essential for model quality.
2. Real-time serving with parameter synchronization as frequent as possible (minute-level for sparse, day-level for dense).
3. Fault tolerance that trades off reliability for real-time learning, finding the right balance.

## References

1. Abadi et al. (2016). TensorFlow: A system for large-scale machine learning. arXiv:1605.08695.
2. Bradley (1997). The use of the area under the ROC curve.
3. Bredillet (2019). Core modeling at Instagram.
4. Carbone et al. (2015). Apache Flink.
5. Cheng et al. (2016). Wide & Deep Learning for Recommender Systems.
6. Covington et al. (2016). Deep Neural Networks for YouTube Recommendations.
7. Egg (2021). Online Learning for Recommendations at Grubhub.
8. Gama et al. (2014). A survey on concept drift adaptation.
9. Guo et al. (2017). DeepFM: A Factorization-Machine based Neural Network for CTR Prediction.
10. Gupta et al. (2020). The Architectural Implications of Facebook's DNN-Based Personalized Recommendation.
11. Harper and Konstan (2015). The MovieLens Datasets.
12. Jiang et al. (2019). XDL: an industrial deep learning framework.
13. Kreps (2011). Kafka: a Distributed Messaging System for Log Processing.
14. Lian et al. (2021). Persia: An Open, Hybrid System Scaling Deep Learning-based Recommenders.
15. Meituan (2021). Distributed Training Optimization for TensorFlow in Recommender Systems.
16. Pagh and Rodler (2001). Cuckoo Hashing.
17. Paszke et al. (2019). PyTorch: An Imperative Style.
18. Shvachko et al. (2010). The Hadoop Distributed File System.
19. Wang et al. (2021). Nonuniform Negative Sampling and Log Odds Correction.
20. Xie et al. (2020). Kraken: Memory-Efficient Continual Learning.
21. Zhao et al. (2019). AIBox: CTR Prediction Model Training on a Single Node.
