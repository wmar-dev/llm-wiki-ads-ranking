---
title: "Scaling Recommendation Systems with Request-Level Deduplication at Pinterest"
type: "source_summary"
sources:
  - "web/pinterest-request-level-deduplication.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Scaling Recommendation Systems with Request-Level Deduplication at Pinterest

**Source:** Pinterest Engineering Blog (Lawhon et al.)

**URL:** [medium.com/pinterest-engineering](https://medium.com/pinterest-engineering/scaling-recommendation-systems-with-request-level-deduplication-93bd514142d9)

**Source type:** `industry_report` (official company engineering blog)

---

Pinterest Engineering's walkthrough of infrastructure for scaling PinFM. Request-level deduplication eliminates redundant processing of user data (16K action tokens) across every candidate item. Storage: 10-50x compression via Apache Iceberg with request-sorted data. Training: 4x retrieval speedup (two-tower natural dedup), 2.8x ranking speedup (DCAT). Fixes for IID disruption (SyncBatchNorm) and false negatives in in-batch negatives (user-level masking). Serving: 7x throughput increase for ranking via DCAT KV cache sharing with custom Triton kernels.
