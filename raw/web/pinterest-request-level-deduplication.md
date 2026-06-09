Source: https://medium.com/pinterest-engineering/scaling-recommendation-systems-with-request-level-deduplication-93bd514142d9

Title: Scaling Recommendation Systems with Request-Level Deduplication

Authors: Matt Lawhon, Filip Ryzner, Kousik Rajesh, Chen Yang, Saurabh Vishwas Joshi (Pinterest Engineering)

Published: Apr 13, 2026; Pinterest Engineering Blog

---

A walkthrough of Pinterest's request-level deduplication techniques for scaling PinFM and other models.

Background: A request triggers a recommendation funnel: retrieval -> ranking. The same user data (16K tokens encoding all user actions) flows through every stage, duplicated across every item scored.

Impact of deduplication:
- Storage: 10-50x compression on user-heavy feature columns via Apache Iceberg with user ID and request ID based sorting
- Training: 4x retrieval speedup (user tower runs on deduplicated batch in two-tower architecture), 2.8x ranking speedup (40% from deduplicated data loading + 2x from DCAT cross-attention)
- Serving: 7x throughput increase for ranking via DCAT KV cache sharing

Technical details:
- IID disruption with request-sorted data: fixed with SyncBatchNorm (aggregates statistics across all devices)
- False negatives in in-batch negatives: fixed with user-level masking (exclude negatives from same user)
- DCAT separates transformer into context encoding (once per request) and candidate crossing (cross-attention with cached KV)
- DCAT implemented with custom Triton kernels for both training and serving
- For retrieval: deduplication is natural due to two-tower architecture (user tower on deduplicated, item tower on full batch)
