Source: https://cloud.google.com/architecture/implement-two-tower-retrieval-large-scale-candidate-generation

Implement two-tower retrieval for large-scale candidate generation | Google Cloud Documentation

---

This document provides a reference architecture for implementing an end-to-end two-tower candidate generation workflow with Vertex AI. The two-tower modeling framework is a powerful retrieval technique for personalization use cases because it learns the semantic similarity between two different entities, such as web queries and candidate items.

## Architecture

The reference architecture trains a two-tower-based retrieval model. Each tower is a neural network that processes either query or candidate item features, and then produces an embedding representation. Each tower is deployed separately:

- Candidate tower: used to precompute embeddings for all candidate items. Deployed to a Vertex AI Vector Search index endpoint optimized for low-latency retrieval.
- Query tower (deployed): during online serving, converts raw user queries to embedding representations, which are then used to look up similar item embeddings in the deployed index.

### Pipeline steps:
1. Training data files stored in Cloud Storage
2. Combined two-tower model trained offline using Vertex AI Training
3. Each tower saved separately for different serving tasks
4. Query tower deployed to Vertex AI online endpoint
5. Candidate tower used in batch prediction to precompute embeddings
6. Embeddings JSON saved to Cloud Storage
7. Vertex AI Vector Search creates ANN index
8. ANN index deployed to Vector Search index endpoint

## Benefits

Two-tower architectures capture semantic relationships between query and candidate entities and map them to a shared embedding space. When entities are mapped to a shared embedding space, semantically similar entities cluster closer together.

Primary benefit: ability to decouple inference of query and candidate representations:
1. Serve new (fresh) items without retraining: feed any set of item features to the candidate tower to compute embeddings, even for unseen items. Addresses the cold-start problem.
2. Optimize retrieval inference by precomputing all candidate item embeddings and indexing them for low-latency retrieval.
3. Co-learning of towers lets you describe items in terms of queries and the other way around.

## Problem framing

Large-scale recommenders are deployed as two-stage or multi-stage systems. The first stage, candidate generation, sifts through a large collection to retrieve a relevant subset of hundreds of items for downstream filtering and ranking.

Two core objectives for retrieval:
1. During training, learn the best representation of the problem
2. During serving, retrieve relevant items fast enough to meet latency requirements

## Cold-start handling

The candidate tower can support an arbitrary set of candidate items, including items that haven't yet interacted with the recommendation system. This is possible because two-tower architectures process rich content and metadata features about each pair. This lets the system describe an unknown item in terms of items that it knows.
