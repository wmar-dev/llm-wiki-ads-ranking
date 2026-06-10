# Deep Neural Networks for YouTube Recommendations

**Source:** Covington, Adams & Sargin (Google), ACM RecSys 2016
**URL:** https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/
**Date:** 2016

## Summary (fetched)

The foundational paper describing YouTube's industrial recommendation
system, structured as the "classic two-stage information retrieval
dichotomy": a deep candidate generation model followed by a separate deep
ranking model.

## Candidate Generation

- Frames recommendation as **extreme multiclass classification** — predict,
  from a catalog of millions of videos, which video a user will watch next.
- Input features: watch history, search query history, demographics, and
  other contextual signals, concatenated and fed through a feed-forward
  network with fully connected layers and ReLU activations.
- Narrows millions of videos down to a few hundred candidates.

## Ranking

- A separate deep network scores and orders the few hundred candidates into
  a final personalized list.
- Uses a richer feature set (user AND video features, since the candidate set
  is now small enough for joint features).
- **Key innovation**: predicts **expected watch time** rather than raw click
  probability — aligning the optimization target with user satisfaction and
  engagement depth, not just clickbait.
- **"Example age" feature**: explicitly encodes how recently a video was
  uploaded relative to training time, biasing the model toward fresh content
  (correcting for the natural bias of training on historical data, where
  older videos have accumulated more interactions).

## Significance

Established the standard "candidate generation → ranking" funnel
architecture later adopted across the industry (TikTok, Reddit, Pinterest,
etc., as seen elsewhere in this wiki). The expected-watch-time ranking
objective and example-age freshness feature remain foundational design
patterns for video recommendation a decade later.
