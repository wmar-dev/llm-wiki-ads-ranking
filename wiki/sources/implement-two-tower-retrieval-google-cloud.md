---
title: "Implement Two-Tower Retrieval for Large-Scale Candidate Generation"
type: "source_summary"
sources:
  - "web/implement-two-tower-retrieval-google-cloud.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Implement Two-Tower Retrieval for Large-Scale Candidate Generation

**Source:** Google Cloud Architecture Center

**URL:** [cloud.google.com](https://cloud.google.com/architecture/implement-two-tower-retrieval-large-scale-candidate-generation)

**Source type:** `other` (reference architecture documentation)

---

Google Cloud's reference architecture for end-to-end two-tower candidate generation on Vertex AI. Describes decoupled tower deployment: the query tower runs on a Vertex AI online endpoint, the candidate tower precomputes embeddings via batch prediction and deploys to Vector Search (ANN index). Identifies the key benefit as decoupling query and candidate inference: new items can be embedded without retraining by feeding features through the candidate tower, addressing cold-start. Notes the two-stage system pattern (candidate generation + ranking) for large-scale recommenders.
