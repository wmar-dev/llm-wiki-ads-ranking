Source: https://arxiv.org/abs/2507.12704

Title: PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform

Authors: Xiangyi Chen, Kousik Rajesh, Matthew Lawhon, Zelun Wang, Hanyu Li, Haomiao Li, Saurabh Vishwas Joshi, Pong Eksombatchai, Jaewon Yang, Yi-Ping Hsu, Jiajing Xu, Charles Rosenberg

Published: RecSys 2025 (oral spotlight), arXiv:2507.12704

---

Abstract: User activity sequences have emerged as one of the most important signals in recommender systems. We present a foundational model, PinFM, for understanding user activity sequences across multiple applications at a billion-scale visual discovery platform. We pretrain a transformer model with 20B+ parameters using extensive user activity data, then fine-tune it for specific applications, efficiently coupling it with existing models. While this pretraining-and-fine-tuning approach has been popular in other domains, such as Vision and NLP, its application in industrial recommender systems presents numerous challenges. The foundational model must be scalable enough to score millions of items every second while meeting tight cost and latency constraints imposed by these systems. Additionally, it should capture the interactions between user activities and other features and handle new items that were not present during the pretraining stage. We developed innovative techniques to address these challenges. Our infrastructure and algorithmic optimizations, such as the Deduplicated Cross-Attention Transformer (DCAT), improved our throughput by 600% on Pinterest internal data. We demonstrate that PinFM can learn interactions between user sequences and candidate items by altering input sequences, leading to a 20% increase in engagement with new items. PinFM is now deployed to help improve the experience of more than half a billion users across various applications.

Key facts:
- 20B+ parameter transformer pretrained on user activity data
- DCAT separates context encoding (one pass per request) from crossing (cross-attention per candidate) for 600% throughput improvement
- Fine-tuning couples with existing downstream ranking models
- 20% increase in engagement with new items
- Deployed for 500M+ users across multiple applications
- Request-level deduplication: 4x retrieval training speedup, 2.8x ranking speedup, 7x ranking serving throughput
- 100x increase in transformer dense parameter counts, 10x increase in model dimension over prior systems
