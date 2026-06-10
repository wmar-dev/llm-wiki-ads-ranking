---
title: "Deep Neural Networks for YouTube Recommendations"
type: "source_summary"
sources:
  - "web/youtube-deep-neural-networks-recommendations-covington.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# Deep Neural Networks for YouTube Recommendations

**Source:** Covington, Adams & Sargin (Google), ACM RecSys 2016

**Source type:** `peer_reviewed` (ACM RecSys 2016)

**Processing:** single-pass

---

## Summary

The foundational paper describing YouTube's industrial recommendation
system as a "classic two-stage information retrieval dichotomy": a deep
candidate-generation network followed by a separate deep ranking network.
This architecture became the template for video/feed recommendation across
the industry.

## Key Claims

- **Candidate generation** is framed as **extreme multiclass classification**
  — predicting, from a catalog of millions of videos, which video a user
  will watch next, using a feed-forward network over watch history, search
  history, and demographic features. This narrows millions of videos down to
  a few hundred candidates
  [[raw/web/youtube-deep-neural-networks-recommendations-covington.md]]
  *(peer-reviewed)*.
- **Ranking** uses a separate deep network with a richer joint user/video
  feature set (now feasible since the candidate set is small) and predicts
  **expected watch time** rather than raw click probability — aligning the
  objective with engagement depth and satisfaction rather than clickbait
  [[raw/web/youtube-deep-neural-networks-recommendations-covington.md]]
  *(peer-reviewed)*.
- The **"example age"** feature explicitly encodes how recently a video was
  uploaded relative to training time, counteracting the natural bias of
  historical training data toward older videos with more accumulated
  interactions — i.e., a built-in freshness correction
  [[raw/web/youtube-deep-neural-networks-recommendations-covington.md]]
  *(peer-reviewed)*.
- This candidate-generation/ranking funnel is the same dichotomy used by the
  two-tower retrieval architectures and ranking models documented elsewhere
  in this wiki [[wiki/synthesis/two-tower-factorized-models.md]]
  [[wiki/synthesis/tiktok-recommendation-algorithm.md]].

## Related Pages

- [[wiki/synthesis/youtube-shorts-recommendation.md]] — synthesis on YouTube
  recommendation, including how Shorts diverges from this architecture
- [[wiki/synthesis/two-tower-factorized-models.md]] — dual-encoder retrieval
  architecture descended from this candidate-generation stage
- [[wiki/synthesis/semantic-id.md]] — Semantic IDs later replaced raw video
  IDs in YouTube's ranking model
- [[wiki/sources/better-generalization-semantic-ids-ranking.md]] — 2024
  follow-on work applying Semantic IDs to YouTube's ranking stage
