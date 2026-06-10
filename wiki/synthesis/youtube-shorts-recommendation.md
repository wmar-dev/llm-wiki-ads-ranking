---
title: "How Does YouTube Shorts Recommendation Work?"
type: "synthesis"
sources:
  - "web/youtube-deep-neural-networks-recommendations-covington.md"
  - "web/youtube-algorithm-five-systems-2026.md"
  - "web/youtube-shorts-algorithm-2026-mediacube.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# How Does YouTube Shorts Recommendation Work?

YouTube does not run a single recommendation algorithm. It runs (at least)
five separate per-surface systems — Home Feed, Suggested Videos, Search,
Subscriptions Feed, and Shorts Feed — each tuned to different signals
[[wiki/sources/youtube-algorithm-five-systems-2026.md]]. Shorts is the most
structurally distinct of the five: it is decoupled from the
candidate-generation/ranking funnel that has anchored YouTube's long-form
feeds since 2016, and instead runs an **explore-and-exploit promotion loop**
driven by swipe behavior rather than clicks.

![synthesis-youtube-shorts-recommendation-diagram-1](/assets/synthesis-youtube-shorts-recommendation-diagram-1.svg)

---

## The Foundational Architecture (Long-Form Feeds)

YouTube's long-form feeds (Home, Suggested Videos, Search, Subscriptions)
descend from the architecture in Covington, Adams & Sargin's 2016 RecSys
paper, *Deep Neural Networks for YouTube Recommendations*
[[wiki/sources/youtube-deep-neural-networks-recommendations-covington.md]]:

- **Candidate generation** — framed as **extreme multiclass classification**:
  predict which video, out of millions, a user will watch next, using a
  feed-forward network over watch history, search history, and demographics.
  This narrows millions of videos to a few hundred candidates.
- **Ranking** — a separate deep network scores the few hundred candidates
  using joint user/video features, optimizing for **expected watch time**
  rather than click probability.
- **"Example age"** — an explicit freshness feature that counteracts the
  bias of historical training data toward older, more-interacted-with
  videos.

This candidate-generation → ranking funnel is the same dichotomy underlying
the two-tower retrieval architectures documented elsewhere in this wiki
[[wiki/synthesis/two-tower-factorized-models.md]], and YouTube's ranking
stage has since been updated to use **Semantic IDs** in place of raw video
IDs for better cold-start generalization
[[wiki/synthesis/semantic-id.md]] [[wiki/sources/better-generalization-semantic-ids-ranking.md]].

---

## How Shorts Diverges

By 2026, the Shorts Feed is a **separate system** from the long-form feeds,
with its own signals and promotion mechanism
[[wiki/sources/youtube-algorithm-five-systems-2026.md]]
[[wiki/sources/youtube-shorts-algorithm-2026-mediacube.md]]:

| Dimension | Long-form feeds (2016 architecture) | Shorts feed (2026) |
|---|---|---|
| Primary quality signal | Click-through rate (which thumbnail is clicked) | **Swipe/skip rate** — CTR is irrelevant since there's no thumbnail to click |
| Depth signal | Expected watch time | **Replays / looping** — substitutes for "completion," which is undiscriminating for short videos |
| "View" threshold | N/A (ranking is continuous) | Standard videos need ~10s to count as a view; Shorts instead weigh active engagement over passive duration |
| Distribution mechanism | Ranked list from candidate generation + ranking scores | **Explore & exploit**: seed audience → expand or halt based on engagement |
| Freshness handling | "Example age" feature biases toward recent uploads | Virality window no longer capped at 48 hours (was previously capped); content can go viral well after upload |
| Format constraint | N/A | Max length expanded from 60 seconds to 3 minutes (2026) |

### The Explore & Exploit Promotion Loop

1. **Explore phase** — a new Short is shown to a small seed audience,
   selected partly from the uploader's existing watch-history-based
   audience segments.
2. **Signal collection** — YouTube observes swipe/skip rate, rewatches and
   looping, and engagement actions (likes, comments, shares, saves).
3. **Exploit decision** — positive signals trigger progressively wider
   distribution over subsequent weeks; negative signals halt further
   promotion
   [[wiki/sources/youtube-algorithm-five-systems-2026.md]]
   [[wiki/sources/youtube-shorts-algorithm-2026-mediacube.md]].

**Inference:** This loop is structurally analogous to the explore/exploit
loop used in bandit-based ad delivery and budget allocation
[[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — a small "exploration
budget" of impressions is spent to estimate quality, and the estimate then
gates how much additional "budget" (distribution) the item receives. Neither
source frames Shorts promotion explicitly as a multi-armed bandit, but the
explore-then-scale structure is the same pattern.

### Personalization

Beyond the per-Short promotion loop, individual feeds are personalized from
watch history at the category level — e.g., a user who frequently watches
ASMR content may see a Shorts feed that is "70% from such content"
[[wiki/sources/youtube-shorts-algorithm-2026-mediacube.md]]. Topical/niche
relevance (informative vs. entertaining categories) also factors into
promotion decisions.

---

## The 2025 Satisfaction-Weighted Discovery Shift

Across YouTube's feeds (including Shorts), 2025 brought a platform-wide
shift from pure engagement metrics (watch time, CTR, swipe-through) toward
**satisfaction-inclusive ranking**:

- ML models predict satisfaction-survey responses for the entire user base,
  not just the small sample who answer surveys.
- Sentiment analysis of comments is incorporated as a ranking signal.
- "Not interested" feedback actively suppresses similar content, rather than
  only affecting the individual item marked.

This represents a deliberate move away from "engagement at all costs" —
content that drives clicks/swipes but leaves viewers dissatisfied is now
penalized rather than rewarded
[[wiki/sources/youtube-algorithm-five-systems-2026.md]]. The system as a
whole processes "80 billion signals daily."

---

## Comparison to TikTok's For You Page

YouTube Shorts' explore-and-exploit promotion loop is broadly comparable to
TikTok's For You Page, which also tests new content with a seed audience
before wider distribution and uses a fixed-ratio explore/exploit split
[[wiki/synthesis/tiktok-recommendation-algorithm.md]]. The key documented
difference: TikTok's published framing emphasizes a fixed exploration ratio
applied across all content, whereas YouTube's 2026 Shorts framing describes
an open-ended, signal-gated expansion (no fixed ratio is given in the
sources reviewed) — an asymmetry that may reflect differing maturity of
public documentation rather than a true architectural difference.

---

## Open Questions

- Open question: None of the sources reviewed describe Shorts' explore phase
  in algorithmic detail (e.g., seed-audience size, statistical test for
  "positive" vs. "negative" signal, or whether a formal bandit algorithm like
  UCB or Thompson Sampling governs the exploit decision). Is YouTube's Shorts
  promotion loop a tuned heuristic, or does it use an explicit
  multi-armed-bandit formulation comparable to
  [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]]?
- Open question: How does YouTube's 2025 satisfaction-weighted ranking
  reconcile with the 2016 expected-watch-time objective for long-form video —
  is satisfaction prediction an additional ranking-stage feature, a separate
  re-ranking pass, or a replacement for the watch-time label entirely? No
  source reviewed describes the integration mechanism.

## Related Pages

- [[wiki/sources/youtube-deep-neural-networks-recommendations-covington.md]] — foundational candidate-generation/ranking architecture (2016)
- [[wiki/sources/youtube-algorithm-five-systems-2026.md]] — 2026 overview of YouTube's five recommendation systems and Shorts' explore/exploit model
- [[wiki/sources/youtube-shorts-algorithm-2026-mediacube.md]] — Shorts-specific ranking signals (swipe/skip rate, replays, engagement)
- [[wiki/synthesis/two-tower-factorized-models.md]] — dual-encoder retrieval descended from the 2016 candidate-generation stage
- [[wiki/synthesis/semantic-id.md]] — Semantic IDs in YouTube's ranking model
- [[wiki/sources/better-generalization-semantic-ids-ranking.md]] — Semantic ID case study using YouTube's ranking model
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — comparable short-form explore/exploit feed at TikTok
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — explore/exploit framing for budget allocation
