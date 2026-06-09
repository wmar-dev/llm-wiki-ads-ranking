---
title: "Monolith Real-Time Recommendation System"
type: "entity"
sources:
  - "web/monolith-realtime-recommendation-system.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Monolith Real-Time Recommendation System

Monolith is ByteDance's production-scale real-time recommendation system deployed in the BytePlus Recommend product. It is designed to address the challenges of sparse categorical features and non-stationary data distributions (concept drift) in recommendation workloads.

## Architecture

Monolith follows a TensorFlow-style Worker-ParameterServer distributed architecture with key customizations:

| Component | Role |
|---|---|
| **Training Workers** | Consume streaming or batch data, compute forward/backward passes |
| **Training PS** | Store and update model parameters (dense + sparse) at minute-level cadence |
| **Serving PS** | Serve inference parameters; receive incremental sync from Training PS |
| **Model Server** | Serve live prediction requests |
| **Online Joiner (Flink)** | Join user action logs with features to produce training examples in real time |
| **Streaming Engine (Kafka)** | Message queues for user actions, features, and training examples |

## Key Features

### Collisionless Embedding Table
- Cuckoo HashMap-based key-value store for sparse parameters
- O(1) worst-case lookups, amortized O(1) insertions
- Frequency filtering and expirable embeddings for memory efficiency
- Native TensorFlow resource operation for tight integration

### Two-Stage Training
1. **Batch training** — single pass on historical data (for model architecture changes)
2. **Online training** — continuous consumption of streaming data from Kafka

### Incremental Parameter Synchronization
- Minute-level sync of only "touched" sparse embedding keys
- Day-level sync of dense parameters
- On-the-fly updates without serving interruption

### Fault Tolerance
- Daily snapshot of training PS
- Trade-off: lose ≤1 day of updates on PS failure, with negligible impact on model quality

## Performance

- Collisionless embedding consistently outperforms hash-trick approaches with comparable memory usage
- 30-minute sync interval achieves AUC 79.80 (Criteo) vs 79.43 for batch-only
- 14–18% AUC improvement in live A/B test on ads model
- Deployed in BytePlus Recommend product

## Related Pages

- [[wiki/sources/monolith-realtime-recommendation-system.md]] — source summary
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — TikTok's recommendation algorithm, which uses Monolith-like principles
- [[wiki/concepts/online-training-recommendation.md]] — broader concept of online training
- [[wiki/concepts/collisionless-embedding-table.md]] — collisionless embedding concept
