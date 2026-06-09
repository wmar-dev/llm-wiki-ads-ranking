---
title: "Collisionless Embedding Table"
type: "concept"
sources:
  - "web/monolith-realtime-recommendation-system.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Collisionless Embedding Table

A collisionless embedding table is a data structure for storing learned embeddings of sparse categorical features (user IDs, item IDs, ad IDs) that guarantees no two distinct IDs map to the same embedding vector. This contrasts with hash-trick approaches where IDs are hashed into a fixed-size table, inevitably causing collisions that degrade model quality.

## The Collision Problem

In production recommendation systems, categorical features (users, items, ads) have extremely large and growing ID spaces — often 2^48 or larger. Standard practice uses a fixed-size embedding table with hashing:

```
embedding = table[hash(id) % table_size]
```

This causes collisions when two IDs hash to the same slot. As tables grow organically, collision rates increase. On ByteDance's production models, even modest collision rates (2.86–7.73%) measurably reduced AUC [[wiki/sources/monolith-realtime-recommendation-system.md]].

## Cuckoo HashMap Approach

Monolith implements collisionless embedding using a Cuckoo HashMap:

- Two hash tables T0, T1 with different hash functions h0(x), h1(x)
- Insertions can evict existing entries ("cuckoo" behavior) and re-insert at alternate positions
- Worst-case O(1) lookups, amortized O(1) insertions
- Dynamic growth without collisions

## Memory Optimization

Collisionless tables require more memory per embedding (no collision compression). Key mitigations:

| Technique | Description | Rationale |
|---|---|---|
| **Frequency filtering** | Only admit IDs above an occurrence threshold | Low-frequency IDs are underfit and don't affect predictions |
| **Probabilistic filtering** | Additional stochastic filter before admission | Further reduces long-tail ID admission |
| **Expirable embeddings** | TTL-based eviction of stale IDs | Dormant users/outdated items drain memory without contributing |

## Comparison

| Aspect | Hash-trick (collision) | Collisionless (Cuckoo) |
|---|---|---|
| Memory usage | Fixed, compact | Dynamic, grows with unique IDs |
| Collision rate | Increases over time | Zero |
| Model quality | Degrades with collisions | Consistent |
| Lookup complexity | O(1) | Worst-case O(1) |
| Insert complexity | N/A (fixed table) | Amortized O(1) |

## Related Pages

- [[wiki/sources/monolith-realtime-recommendation-system.md]] — Monolith paper *(peer_reviewed)*
- [[wiki/entities/monolith-realtime-system.md]] — Monolith system entity
- [[wiki/concepts/online-training-recommendation.md]] — online training concept
- [[wiki/concepts/web-scale-learning.md]] — web-scale learning paradigm
