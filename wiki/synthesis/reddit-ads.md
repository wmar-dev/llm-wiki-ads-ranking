---
title: "How Reddit Ads Work"
type: "synthesis"
sources:
  - "web/reddit-ads-how-it-works.md"
  - "web/reddit-max-campaigns.md"
  - "web/reddit-audience-targeting.md"
  - "web/reddit-contextual-relevance-ads.md"
  - "web/reddit-max-campaigns-trajectory.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# How Reddit Ads Work

Reddit's advertising system runs a real-time auction every time a user loads a page with ad inventory — deciding which ad fills each slot within milliseconds, billions of times per day.

## The Auction

![synthesis-reddit-ads-diagram-1](/assets/synthesis-reddit-ads-diagram-1.svg)

Reddit uses a **second-price auction** — you set a maximum bid but pay just above the next-highest bidder. The winner is determined by a combination of factors, not just bid amount [[wiki/sources/reddit-ads-how-it-works.md]] *(blog post)*:

| Factor | Description |
|---|---|
| **Bid amount** | Maximum you're willing to pay per click, impression, or view |
| **Ad quality** | Historical CTR and engagement performance |
| **Relevance** | How well targeting matches the user |
| **User experience** | Ads delivering value rank higher |

## Delivery Funnel

Reddit's ad delivery pipeline consists of four sequential stages [[wiki/sources/contextual-relevance-of-ads-reddit.md]] *(company engineering blog)*:

![synthesis-reddit-ads-diagram-2](/assets/synthesis-reddit-ads-diagram-2.svg)

1. **Targeting Layer** — Advertiser criteria (community, interest, keyword, custom) filter eligible ads
2. **Light Rankers** — Fast, lightweight models narrow the candidate list for heavy scoring
3. **Heavy Rankers** — Deep neural networks predict calibrated probabilities for CTR, conversion rate, and other outcomes
4. **Auction** — Selects ad maximizing utility: P(outcome) × Value (e.g., pCTR × Bid)

## Contextual Relevance

Reddit developed a fine-tuned embedding system for matching ads to post-level content context [[wiki/sources/contextual-relevance-of-ads-reddit.md]] *(company engineering blog)*. The system uses:

- **LLM-as-judge** (Gemini 2.5 Flash Lite) to label <post, ad> relevance for ground truth
- **Multi-tower embedding model** (Stella encoder + subreddit features + landing page summaries) scoring relevance at inference
- **Selective auction boosting** applied preferentially for search-referred traffic (high-intent users)

Inference: Fine-tuned embeddings achieved 3.2× PRAUC vs IAB taxonomy matching alone, and are now integrated across targeting, retrieval, and all ranker stages.

## The 4-Step Delivery Pipeline

### Step 1: Campaign Setup
Campaign → Ad Group → Ads hierarchy. All targeting at Ad Group level [[wiki/sources/reddit-audience-targeting.md]].

### Step 2: Targeting

Reddit's key differentiator is **community-based targeting** — reaching users through the subreddits they actively participate in.

| Targeting type | Signal | Best for |
|---|---|---|
| **Community** | Subreddit subscription/engagement | Highest intent, specific products |
| **Interest** | Cross-Reddit behavioral clusters | Awareness, broad reach |
| **Keyword** | Real-time conversation content | Lower-funnel, purchase intent |
| **Custom audiences** | CRM lists, Pixel/CAPI retargeting, lookalikes | Conversion, retargeting |

**Logic**: OR within a type (user matches ANY selected community); AND across types (user must match community AND keyword). [[wiki/sources/reddit-audience-targeting.md]]

### Step 3: Bidding

| Strategy | How it works |
|---|---|
| **Manual bidding** | Set specific max bids per action |
| **Automatic bidding** | Reddit optimizes bids within budget |
| **MAX Campaigns** (2026) | AI predicts impression value; auto-selects creative, placements, budget allocation |

MAX Campaigns, launched in beta January 2026, use **Reddit Community Intelligence** — structured signals from 23B+ posts and comments — to predict the value of every impression in real-time. Results from 600+ beta testers: 17% lower CPA, 27% more conversions. [[wiki/sources/reddit-max-campaigns.md]]

### Step 4: Delivery & Learning

- **Learning phase**: 7–14 days for data accumulation. Avoid major changes during this period.
- **Pacing**: Standard (even spread) or Accelerated (fast as possible).
- **Conversion optimization**: Reddit Pixel tracks actions; algorithm shifts delivery toward high-converting audiences.

## Pricing

| Pricing model | Use case |
|---|---|
| **CPM** (cost per 1,000 impressions) | Awareness, reach |
| **CPC** (cost per click) | Traffic, consideration |
| **CPV** (cost per view) | Video awareness |

**Typical costs (2025-2026)**:

| Metric | Range |
|---|---|
| CPM | $0.50 – $15.00 |
| CPC | $0.20 – $4.00 |
| CPV | $0.03 – $0.20 |
| Min daily budget | $5.00 (effective: $50-100/day) |

Reddit is significantly cheaper than Meta and Google — CPMs are typically 50-70% lower than Facebook, and CPCs 30-50% lower.

## Key Differences from Other Platforms

| Dimension | Reddit | Meta ([[wiki/synthesis/meta-ad-ranking.md]]) | Google ([[wiki/concepts/google-ad-rank-ltv-scoring.md]]) |
|---|---|---|---|
| **Auction type** | Second-price | GSP (Bid × EAR + Ad Quality) | rGSP (LTV = eCPM - costs) |
| **Primary targeting** | Community/subreddit | Creative-as-targeting (Andromeda) | Keyword + quality score |
| **Audience intent** | Research/consideration | Entertainment/social | High purchase intent |
| **AI automation** | MAX Campaigns (beta) | GEM → Lattice teacher-student | Smart Bidding |
| **Learning phase** | 7-14 days | 50 events in 7 days | Depends on conversion volume |
| **Typical CPM** | $2-5 | $8-15 | N/A (CPC model) |

## Answered Questions

### Max Campaigns trajectory

Reddit Max is following a similar automation trajectory to Meta Advantage+, but with deliberate differentiation on transparency. Max launched beta Jan 2026 showing 17% lower CPA and 27% more conversions. By Q1 2026 earnings (May 2026), 50% of beta advertisers were using AI creative features, with Reddit reporting $625M ad revenue (+74% YoY) and 75% more active advertisers. Reddit's CEO stated Max is a top sales priority, and the format is being expanded to app campaigns. However, Reddit emphasizes open-box reporting (Top Audience Personas, community intelligence insights) — explicitly positioned against the "black box" criticism of Meta Advantage+ and Google PMax. If Max maintains its performance edge and transparency differentiation, it may follow Advantage+'s default path without the same advertiser backlash [[wiki/sources/reddit-max-campaigns-trajectory.md]].

### Conversation velocity and second-price auction

*Open question:* How does Reddit's conversation velocity signal interact with the second-price auction? This remains partially unanswered — internal mechanics of the quality engagement weighting are not publicly documented. The interaction likely works through the relevance utility boost documented in Reddit's contextual relevance system, where higher-engagement communities generate higher-quality signals that improve the contextual relevance matching model, which in turn affects auction outcomes [[wiki/sources/contextual-relevance-of-ads-reddit.md]].

### Community-based targeting scalability

*Open question:* Can community-based targeting scale to match Meta/Google reach? This also remains partially unanswered. Reddit's DAUq grew 19% YoY to ~53.5M US daily users in Q1 2026, with a stated target of 100M. The platform's ad load remains low relative to peers, and search advertising has not yet launched — both represent untapped inventory. The community-based approach provides stronger intent signals (40% of conversations have commercial intent) but inherently limits scale compared to Meta's cross-platform identity graph or Google's search query coverage [[wiki/sources/reddit-ads-how-it-works.md]].

## Open Questions

*None remaining.*
