# How the YouTube Algorithm Works (5 Systems Explained)

**Source:** posteverywhere.ai blog
**URL:** https://posteverywhere.ai/blog/how-the-youtube-algorithm-works
**Date:** accessed 2026-06-09 (describes 2026 state)

## Summary (fetched)

YouTube does not run one recommendation algorithm — it runs (at least) five
separate systems, one per surface, each optimizing for different signals.

## The Five Systems

1. **Home Feed** — personalizes from broad viewing history over weeks/months;
   emphasizes long-run watch history, engagement patterns, viewer
   preferences.
2. **Suggested Videos** (sidebar/autoplay) — real-time, context-driven;
   prioritizes videos commonly watched in sequence after the current video;
   rewards videos that extend total session time.
3. **Search** — intent-driven; weighs keyword relevance first, then
   satisfaction signals.
4. **Subscriptions Feed** — testing a "Most Relevant" sort based on
   interaction frequency rather than pure chronological order.
5. **Shorts Feed** — a fundamentally different model (see below).

## Shorts Algorithm: Explore & Exploit Model

- **Explore phase**: a new Short is shown to a small seed audience; YouTube
  monitors initial response.
- **Exploit phase**: positive signals (replays, completion, engagement)
  trigger progressively wider distribution; negative signals halt promotion.
- **Click-through rate is irrelevant** for Shorts (users swipe, they don't
  click a thumbnail) — this is the single biggest structural difference from
  Home/Suggested/Search, which all use CTR as a primary signal.
- **Replay count** becomes a critical signal (absent from long-form ranking).
- **Virality window** for Shorts is no longer capped at 48 hours (an earlier
  constraint).
- **Max length**: expanded from 60 seconds to 3 minutes in 2026.
- Channels combining Shorts + long-form see "41% faster growth" than
  single-format channels (per platform messaging).

## The 2025 Satisfaction-Weighted Discovery Shift

YouTube shifted from pure engagement (watch time, CTR) to
**satisfaction-inclusive ranking**: ML models predict satisfaction-survey
responses for all users (not just the small sample who answer surveys),
sentiment analysis of comments is incorporated, and "not interested"
feedback actively suppresses similar content. Content that drives clicks but
leaves viewers unsatisfied is now penalized — a shift away from optimizing
for engagement alone.

## Scale

The system processes "80 billion signals daily." Initial ranking considers
metadata relevance, then personalized signals are applied dynamically based
on device type, content category, and viewing surface. The guiding question
is framed as: "Will this specific viewer enjoy this specific video right
now?"

## Significance

Provides the 2026 production-context update to the 2016 Covington et al.
candidate-generation/ranking architecture: the core funnel idea persists, but
(a) Shorts now runs as an entirely separate system from long-form, with
swipe/replay-based signals instead of CTR/click-based signals, and (b) the
ranking objective has broadened from "expected watch time" (2016) to
predicted satisfaction (2025-2026), incorporating negative feedback and
sentiment.
