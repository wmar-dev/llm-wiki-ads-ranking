# Better Generalization with Semantic IDs: A Case Study in Ranking for Recommendations

**arXiv:2306.08121** (cs.IR, cs.LG)

**Authors:** Anima Singh, Trung Vu, Nikhil Mehta, Raghunandan Keshavan (Google), Maheswaran Sathiamoorthy (Google DeepMind), Yilin Zheng (Google), Lichan Hong (Google DeepMind), Lukasz Heldt (Google), Li Wei (Google), Devansh Tandon (Google), Ed H. Chi (Google DeepMind), Xinyang Yi (Google DeepMind)

**Submitted:** 13 Jun 2023 (v1), last revised 30 May 2024 (v2)

**DOI:** https://doi.org/10.48550/arXiv.2306.08121

**License:** CC BY 4.0

---

## Abstract

Randomly-hashed item ids are used ubiquitously in recommendation models. However, the learned representations from random hashing prevents generalization across similar items, causing problems of learning unseen and long-tail items, especially when item corpus is large, power-law distributed, and evolving dynamically. In this paper, we propose using content-derived features as a replacement for random ids. We show that simply replacing ID features with content-based embeddings can cause a drop in quality due to reduced memorization capability. To strike a good balance of memorization and generalization, we propose to use Semantic IDs — a compact discrete item representation learned from frozen content embeddings using RQ-VAE that captures the hierarchy of concepts in items — as a replacement for random item ids. Similar to content embeddings, the compactness of Semantic IDs poses a problem of easy adaption in recommendation models. We propose novel methods for adapting Semantic IDs in industry-scale ranking models, through hashing sub-pieces of the Semantic-ID sequences. In particular, we find that the SentencePiece model that is commonly used in LLM tokenization outperforms manually crafted pieces such as N-grams. To the end, we evaluate our approaches in a real-world ranking model for YouTube recommendations. Our experiments demonstrate that Semantic IDs can replace the direct use of video IDs by improving the generalization ability on new and long-tail item slices without sacrificing overall model quality.

---

## 1 Introduction

Neural models with large embedding tables are widely used in industry-scale recommender systems for scoring and ranking vast collections of items. These tables, often containing millions or even billions of rows, facilitate rapid memorization of item quality by modeling randomly-hashed item identifiers. Learning good item representations is crucial for personalization, as users are typically modeled as a sequence of items. In this paper, we consider a neural ranking in a video recommendation system at YouTube. In this model, every video gets a unique identifier referred to as video ID, which is a random string devoid of meaning.

This paper studies content-based item representations that can improve generalization for new and long-tail item distributions while keeping models' power of memorization without sacrificing overall quality, with a focus on recommendation ranking models. A common technique for encoding item ID is to learn one-hot embeddings. However, given an extremely large item corpus with billions of videos, learning one embedding vector per video can be resource-intensive and vulnerable to data sparsity of torso and tail items.

A recent study (Ni et al. 2023) has demonstrated the effectiveness of video encoders that use end-to-end training (VideoRec) to replace video ID in recommendation models for short videos. However, this approach comes with 10-50x computational cost over the ID baseline.

We propose a new framework of adapting content embeddings in ranking models with the flexibility of controlling generalization and memorization. Our method is based on item Semantic IDs (SIDs) which are originally proposed in TIGER (Rajput et al. 2023) as a hierarchical, sequential and compact representation for generative retrieval. The hierarchical nature of SID offers the flexibility of granularity control by using various levels of prefixes, and the sequential property draws the connection to subword tokenization, e.g., SentencePiece model (SPM) in LLMs. Notably, TIGER uses SIDs for generative retrieval where efficiency is not a primary consideration, while our work focuses on using Semantic IDs in resource-constrained and latency-sensitive production-scale ranking models, where the hashing and adaptation through embeddings is the key.

**Contributions:**
1. Two ways of adapting SIDs as replacement for item IDs: n-gram and SPM. Key idea is content-based hashing through sub-pieces of item SIDs, while SPM provides a learnable approach from item distribution by grouping sub-pieces with variable lengths.
2. Extensive experiments on YouTube dataset showing SID-based adaptation outperforms directly using content embeddings. SPM superior to n-gram with large embedding tables.
3. Productionization of SIDs for billions of YouTube videos with meaningful hierarchical relationships, replacing video IDs in production.

## 2 Related Work

**Embedding learning.** Recommender models rely on learning good representation of categorical features. Common technique: one-hot embeddings. Hashing trick (Weinberger et al. 2009) is used when cardinality is high but causes random collisions. Multiple hashing (Zhang et al. 2020) offers relief but still has random collisions. Deep Hash Embedding (Kang et al. 2021) avoids embedding tables but at higher computation cost. Semantic IDs provide a compute-efficient way to avoid random collisions during embedding learning for item IDs by enabling collisions between semantically related items.

**Cold-start and content information.** Content-based recommender models combat cold-start issues. DropoutNet (Volkovs et al. 2017), CC-CC (Shi et al. 2019), and Du et al. (2020) use content-derived embeddings. PinSage (Ying et al. 2018) aggregates visual, text, and engagement information. PinnerFormer (Pancha et al. 2022) uses sequences of PinSage embeddings. VideoRec (Ni et al. 2023) trains end-to-end video encoders with recommendation models for short videos. TransRec (Wang et al. 2022) trains end-to-end with multiple modalities. Both approaches significantly increase training costs. Semantic IDs offer efficient compression of content embeddings into discrete tokens, making content signals feasible in production.

**Discrete representations.** VQ-VAE (Van Den Oord et al. 2017), VQ-GAN (Esser et al. 2021), and variants used for generative modeling. TIGER (Rajput et al. 2023) used RQ-VAE for recommender applications. Conventional techniques like Product Quantization (Jegou et al. 2010) and variants (MGQE, Hou et al. 2022) do not offer hierarchical semantics, which this work leverages.

## 3 Proposed Approaches

### 3.1 Overview

Given content embeddings for a corpus of items, a two-stage approach:

**Stage 1: Efficient compression of content embeddings into discrete Semantic IDs.** Uses RQ-VAE to quantize dense content embeddings into discrete tokens capturing semantic information about videos. Once trained, the RQ-VAE model is frozen and used for training the downstream ranking model in Stage 2.

**Stage 2: Training the ranking model with Semantic IDs.** Maps each item to its Semantic ID and trains embeddings for Semantic ID along with the rest of the ranking model.

A key design choice is to freeze the RQ-VAE model after Stage 1. The frozen model generates Semantic IDs for training and serving. Analysis of YouTube ranking models using SIDs from RQ-VAE models trained on both older and recent data reveals comparable performance, indicating stability of learned semantic representations over time.

### 3.2 RQ-VAE for Semantic IDs (SIDs)

SIDs are generated from item content embeddings using Residual-Quantized Variational AutoEncoder (RQ-VAE). Three jointly-trained components:
1. An encoder E that maps the content embedding x to a latent vector z
2. A residual quantizer with L levels, each with a codebook C_l = {e^l_k} of size K
3. A decoder D that maps the quantized latent back to the original embedding space

The quantizer recursively quantizes the residual r_l at each level l to the nearest codebook vector. Loss: L = L_recon + L_rqvae, where L_recon = ||x - x_hat||^2 and L_rqvae encourages the encoder and codebook vectors to move toward each other.

### 3.3 Semantic ID Representation in Ranking

For a given item v, an RQ-VAE model with L levels generates a SID as a sequence (c^v_1, ..., c^v_L). Two adaptation techniques:

**N-gram-based:** Groups SID codes into subwords of length N. Each subword associated with a learnable embedding. Item representation constructed by summing embeddings of all N-gram subwords. Unigram has L subwords, bigram has L/2 subwords. Embedding table size for N-gram group is K^N rows.

**SPM-based:** Uses SentencePiece Model to dynamically learn subwords based on the distribution of impressed items. Allows variable-length subwords: popular co-occurring codes combine as a single subgroup; codes that rarely co-occur may fallback to unigram. Single embedding table where each row corresponds to a particular variable-length subpiece.

## 4 Experiments

### 4.1 Experimental Setup

**Ranking Model.** Multitask production ranking model used for YouTube next-video recommendation. Uses O(10) million buckets for random hashing to accommodate O(100) million videos. Trained sequentially on logged data. Random hashing of video IDs used for three key features: users' watch history, watch video, and candidate video.

**Content Embeddings.** Semantic IDs generated using dense content embeddings from a video encoder (transformer with Video-BERT backbone), taking audio and visual features, outputting 2048-dimensional embeddings.

**Experimental Settings.** Compares two SID-based representations (N-gram and SPM) with Dense Input (raw content embeddings) and Random Hashing. Uses L=8 depth (8 codes per SID), codebook size K=2048.

**Evaluation metrics.** AUC for CTR. CTR/1D AUC for cold-start items (items introduced on test day). A 0.1% change in CTR AUC is considered significant.

### 4.2 Performance of Semantic ID

**Dense Content Embedding vs. Random Hashing.** Directly using content embeddings (Dense Input) to replace random hashing performs worse than the video-ID baseline. The ranking models rely heavily on memorization from ID-based embedding tables; replacing them with fixed dense embeddings leads to poor CTR. Increasing model depth (1.5x-2x layers) helps but increases serving cost considerably.

**SID vs. Baselines.** When user history is not used, Unigram-SID and Bigram-SID perform worse than Random Hashing due to skew in training content causing sparse embedding table usage. When user history IS used, both methods perform much better than random hashing because diverse content in watch history leads to more uniform embedding table usage.

**SPM-SID** consistently outperformed N-gram representations with larger embedding tables, especially on cold-start CTR/1D AUC. For smaller embedding tables, N-gram methods show slight advantage. SPM dynamically generates subwords based on training data, optimizing representation within size constraints.

## 5 Conclusion and Future Work

This paper tackles removing reliance on widely used item IDs in recommendation models. Using YouTube ranking model as a case study, Semantic IDs are developed for billions of YouTube videos from frozen content embeddings using RQ-VAE. Semantic IDs are demonstrated as an effective method for replacing video IDs to improve generalization by introducing meaningful collisions.

## References

(32 references from the paper — see original for full list)
