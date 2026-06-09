---
title: "What Types of Ads Are There?"
type: "synthesis"
sources:
  - "web/digital-ad-formats-epom.md"
  - "web/google-ad-rank-briefing-paper.md"
  - "web/meta-ads-algorithm-2026-guide.md"
  - "web/reddit-ads-how-it-works.md"
  - "web/en-wikipedia-org-wiki-banner-blindness.html"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# What Types of Ads Are There?

Online advertising spans dozens of formats, but they can be grouped into two broad categories: **display** (visual ads on web pages and apps) and **non-display** (search, social, email). The Interactive Advertising Bureau (IAB) defines five standard display formats, with several non-display categories alongside [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

![synthesis-types-of-ads-diagram-1](/assets/synthesis-types-of-ads-diagram-1.svg)

---

## Display Ad Formats (IAB Taxonomy)

### 1. Banner (Display) Ads

Standard image or animated ads in designated slots on web pages and apps — the oldest ad format. Common IAB-standard sizes include 300×250 "medium rectangle" and 728×90 "leaderboard" [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

- **Pricing**: CPM $2–10; CPC $0.30–3
- **Performance**: Global average CTR ~0.06% (1 click per 1,600 impressions)
- **Best for**: Top-of-funnel brand awareness, retargeting, broad reach
- **Platforms**: Google Display Network, ad networks, programmatic exchanges
- **Alias**: referred to as **display advertising** broadly, though IAB separates it as a sub-format

Banner ads suffer from **banner blindness** — users consciously or unconsciously ignore elements they perceive as ads, triggered by ad-specific placement, visual treatment, and proximity to other ads [[wiki/synthesis/ad-blindness.md]].

### 2. Interstitial Ads

Full-screen ad units that take over the entire screen during natural transition points in mobile apps or websites (between pages, between game levels). Can be static images, HTML5, or video [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

- **Pricing**: CPM $5–15; CPC $0.50–2
- **Performance**: CTR 2–5% (5–10× higher than banners); 100% viewability
- **Best for**: Mobile apps, game transitions, natural flow breaks
- **Risk**: Intrusive if poorly timed; may increase bounce/uninstall rates

### 3. Rich Media Ads

Interactive display units incorporating video, audio, 3D elements, forms, or user interactions — built with HTML5 for immersive storytelling. Include expandable banners, in-banner video, overlays, and floating units [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

- **Pricing**: CPM $10–25+; CPC $1–4
- **Performance**: Interaction rates >20%; generates 3× longer site visits post-click than static banners
- **Best for**: Mid-to-bottom funnel, product demos, data capture, tech/retail/entertainment
- **Distinction from banners**: Rich media contains interactive elements beyond animation; banners are limited to static or looped animation

### 4. Native Ads

Ad units integrated into the user's content experience, matching the look, feel, and function of the surrounding content. They do not look like ads at first glance [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

- **Pricing**: CPC $0.10–1.00; CPM $5–15 (premium native can exceed $25 CPM)
- **Performance**: Higher engagement and brand recall than banners; 15–20% of programmatic budgets (2025)
- **Best for**: Mid-funnel engagement, content promotion, storytelling, lead nurturing
- **Platforms**: Taboola, Outbrain, in-feed social ads, recommended content widgets
- **Trade-off**: Requires strong disclosure labeling to avoid ethical concerns

**Inference:** Native advertising is conceptually similar to Reddit's in-feed promoted posts, Meta's feed ads, and TikTok's in-feed video ads — the ad format matches the platform's organic content format [[wiki/synthesis/reddit-ads.md]] [[wiki/synthesis/meta-ad-ranking.md]].

### 5. Video Ads

Motion-based creatives delivering messages through audio-visual storytelling. Two main subtypes [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*:

| Subtype | Player | Sound | Skip | Example |
|---|---|---|---|---|
| **In-stream** | Requires video player | Autoplay with sound | Skippable or non-skippable | YouTube pre-roll, Hulu |
| **Out-stream** | No player needed | Muted by default | Can be scrolled past | In-article video, in-feed video |

- **Pricing**: CPM $10–30+; CPV ~$0.05–0.10; CTV can exceed $40 CPM
- **Performance**: 27× higher CTR than static banners; completion rate and brand lift are primary metrics
- **Best for**: Brand storytelling, product demos, Gen Z/mobile audiences, CTV/OTT
- **Platforms**: YouTube, TikTok, Facebook/Instagram Reels, Connected TV (CTV)

### 6. Push and Pop-Under Ads

Non-traditional formats used primarily in performance and affiliate marketing [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*:

| Format | Mechanism | CTR | Pricing |
|---|---|---|---|
| **Push** | Real-time message to device/browser notification | 2–8% | CPC $0.01–0.10 |
| **Pop-under** | Opens new tab behind active window | N/A (direct landing page) | CPM $0.50–4 |

Push ads work for retargeting and seasonal promotions. Pop-unders offer high volume and bypass most ad blockers but appear spammy.

---

## Non-Display Ad Formats

### 7. Search Ads (SEM)

Text-based ads on search engine results pages, triggered by user queries. The advertiser bids on keywords and pays per click [[wiki/sources/google-ad-rank-briefing.md]].

- **Pricing**: CPC $1–10+ (average $5.26); no CPM model
- **Performance**: CTR 3–5%; conversion rate 5–10%
- **Best for**: Bottom-funnel, high-intent queries, direct response
- **Platforms**: Google Ads, Microsoft Bing, Apple Search Ads
- **Ranking mechanism**: Generalized second-price (GSP) auction ranking by `bid × quality score`; Google uses LTV scoring (eCPM minus costs) [[wiki/concepts/google-ad-rank-ltv-scoring.md]]

### 8. Social Media Ads

Platform-specific ads blending images, video, carousels, story formats, and interactive elements into social feeds [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*. Each platform has unique native formats:

| Platform | Native Formats | Key Differentiator |
|---|---|---|
| Meta (FB/IG) | Feed ads, Stories, Reels, Carousel, Collection | Creative-is-targeting via Andromeda neural retrieval |
| TikTok | In-feed video, Spark Ads, Brand Takeover, Hashtag Challenge | Unsupervised recommendation algorithm; short-form video |
| Reddit | Promoted Posts, MAX Campaigns | Community-based targeting; contextual relevance boosting |
| LinkedIn | Sponsored Content, InMail, Text Ads, Carousel | Professional/job-role targeting |
| Pinterest | Promoted Pins, Shopping Ads, Idea Pins | Visual discovery; product intent |

[[wiki/synthesis/meta-ad-ranking.md]] [[wiki/synthesis/reddit-ads.md]]

- **Pricing**: CPM $5–15; CPC $0.50–2
- **Performance**: CTR 1–2%; conversion rate 5–10%
- **Best for**: Full-funnel marketing; strong for awareness (video/story) and conversion (feed/carousel)

### 9. Email Ads

Promotional messages or sponsored placements in newsletters and email campaigns [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

- **Pricing**: CPM $10–50 for sponsored placements; low production costs (~$0.01 per send)
- **Performance**: CTR 2–5%; open rates 20–30%
- **Best for**: Retention, nurture, loyalty offers, content promotion

---

## Pricing Models by Format

| Pricing Model | Common Formats | Typical Range |
|---|---|---|
| **CPM** (cost per 1,000 impressions) | Banner, native, interstitial, email | $0.50 – $50 |
| **CPC** (cost per click) | Search, social, native, banner | $0.10 – $10+ |
| **CPA** (cost per acquisition) | Performance campaigns (any format) | Varies by vertical |
| **CPV** (cost per view) | Video (in-stream, out-stream) | $0.03 – $0.20 |

**Inference:** The same ad format can perform 3–10× differently depending on placement. A banner in the main content column will outperform the same banner in the right rail due to banner blindness effects [[wiki/sources/digital-ad-formats-epom.md]] *(blog post)*.

---

## Format vs Channel vs Placement

The industry distinguishes three orthogonal dimensions:

- **Format**: How the ad renders (banner, video, native, text)
- **Channel**: Where the budget is allocated (display, search, social, CTV, retail media)
- **Placement**: Where the ad appears on the page (in-feed, pre-roll, sidebar, sticky)

A search ad uses a text format on the search channel via top-of-SERP placement. A Meta feed ad uses a native format on the social channel via in-feed placement.

---

## Open Questions

- How do emerging formats (AR/VR ads, AI-assistant sponsored intelligence, in-game ads) map onto the existing IAB taxonomy?
- Can the ad format × placement performance interaction be predicted algorithmically, or does it require empirical A/B testing per campaign?
- As privacy regulations reduce behavioral targeting, which formats are most resilient — native and contextual, or search (high intent)?

## Related Pages

- [[wiki/synthesis/why-ads-have-auctions.md]] — economic rationale for search/social ad auctions
- [[wiki/synthesis/ad-blindness.md]] — banner blindness and display ad effectiveness
- [[wiki/synthesis/meta-ad-ranking.md]] — social/feed ad formats on Facebook/Instagram
- [[wiki/synthesis/reddit-ads.md]] — community-targeted promoted posts
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — search ad ranking mechanics
- [[wiki/sources/digital-ad-formats-epom.md]] — IAB taxonomy reference
