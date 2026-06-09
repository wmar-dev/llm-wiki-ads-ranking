---
title: "Reddit Ads System"
type: "entity"
sources:
  - "web/reddit-ads-how-it-works.md"
  - "web/reddit-max-campaigns.md"
  - "web/reddit-audience-targeting.md"
  - "web/reddit-contextual-relevance-ads.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# Reddit Ads System

Reddit's advertising platform operates a **second-price auction** with community-based targeting, running across 450M+ weekly active users. The system prioritizes engagement quality over raw volume.

## Ad Delivery Funnel

Reddit's delivery pipeline consists of four sequential stages [[wiki/sources/contextual-relevance-of-ads-reddit.md]] *(company engineering blog)*:

![entities-reddit-ads-system-diagram-1](/assets/entities-reddit-ads-system-diagram-1.svg)

1. **Targeting Layer** — Advertiser criteria (community, interest, keyword, custom) filter eligible ads
2. **Light Rankers** — Fast, lightweight models narrow the candidate list [[wiki/sources/contextual-relevance-of-ads-reddit.md]]
3. **Heavy Rankers** — Deep neural networks predict calibrated probabilities for CTR / conversion rate
4. **Auction** — Selects ad maximizing utility: P(outcome) × Value (e.g., pCTR × Bid)

## Auction Mechanics

Second-price auction — winners pay just above the next-highest bidder. Ranking considers: bid amount, ad quality (CTR/engagement), relevance (targeting match), and user experience.

## Targeting

Three core native targeting pillars, plus custom audiences:

| Type | Signal strength | Funnel stage |
|---|---|---|
| Community (subreddits) | Highest intent | Consideration |
| Interest (cross-Reddit clusters) | Medium | Awareness |
| Keyword (conversation content) | High | Conversion |
| Custom (Pixel/CAPI/CRM) | Varies | Retargeting |

## Contextual Relevance System

Reddit developed a fine-tuned embedding model for post-ad contextual relevance, integrated across all funnel stages [[wiki/sources/contextual-relevance-of-ads-reddit.md]] *(company engineering blog)*:

- **Ground truth**: LLM-as-judge (Gemini 2.5 Flash Lite) with few-shot prompting labels <post, ad> pairs as No/Low/Medium/High relevance
- **Model**: Multi-tower architecture using Stella (stella_en_400M_v5) as text encoder, augmented with subreddit embeddings, LLM-generated landing page summaries, and product attributes
- **Performance**: Fine-tuned embeddings achieved 3.2× PRAUC vs 1× for IAB category matching
- **Integration**: Embeddings used in targeting, retrieval, and as features in light + heavy rankers
- **Selective application**: Relevance boost applied preferentially for search-referred traffic (high-intent users benefit most)

## Bidding

Manual, Automatic, and MAX Campaigns (AI-powered, beta Jan 2026). MAX uses Reddit Community Intelligence from 23B+ posts/comments.

## Pricing

CPM, CPC, CPV models. CPM: $0.50-15, CPC: $0.20-4.00, CPV: $0.03-0.20. Min budget $5/day (effective $50-100/day).
