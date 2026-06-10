---
title: "What is RGSP? Google's Randomized Generalized Second-Price Ad Auctions Explained"
type: "source_summary"
sources:
  - "web/rgsp-randomized-second-price-explained.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# What is RGSP? Google's Randomized Generalized Second-Price Ad Auctions Explained

**Source:** Search Engine Land

**URL:** [searchengineland.com](https://searchengineland.com/google-rgsp-randomized-generalized-second-price-ad-auctions-explained-433053)

**Source type:** `news_article` (industry trade publication, reporting on US v. Google DOJ antitrust trial testimony and exhibits)

---

This article fills the gap left by Google's own [[wiki/sources/google-ad-rank-briefing.md]], which named **rGSP (Randomized General Second-Price Auction)** as launched globally in January 2019 but stated "the document does not fully detail the randomization logic." This source, drawing on DOJ trial testimony and internal Google documents made public during *US v. Google*, fills in that mechanism.

## Mechanism

- Ads are ranked by [[wiki/concepts/google-ad-rank-ltv-scoring.md|LTV]] (Ad Rank), as in standard GSP.
- When multiple ads' LTV scores are **close enough** to each other, Google does not deterministically award the slot to the single highest-LTV ad — the winner is selected **at random** from that close-LTV group.
- The winner pays **the next-highest qualifying bid plus one cent** (second-price-plus-epsilon), applied to whichever bid ends up as runner-up after randomization.

## Stated Rationale

- Prevents "winner-take-all" dynamics where one large advertiser (e.g., Amazon) permanently occupies top slots.
- Reduces advertiser anxiety about needing to constantly re-tune bids.

## Revenue and Pricing Impact (DOJ Trial Testimony, Jerry Dischler)

- RGSP "increases Google's ad revenue" — Dischler could not confirm whether it directly raises advertiser bids.
- Auction-mechanic changes (including RGSP) raised costs ~5% for the average advertiser, up to ~10% for some queries.
- Introduced January 2019; associated with a roughly 10% overall revenue increase the DOJ argued was unrelated to ad quality improvements.

## DOJ Controversy

- DOJ position: the highest bidder should always win; RGSP's randomization is anticompetitive.
- DOJ claim: advertisers must bid **~3.7x** higher than competitors to reliably avoid randomized demotion.
- Google provides no transparent guidance on how advertisers can raise their LTV score, leaving "bid higher" as the practical lever.
- Cited internal email from Google VP Adam Juda acknowledging the optics risk of disclosing "we randomly disable you if you don't bid high enough."

## Discrepancies vs. Existing Wiki Pages

No contradictions — this source is a direct enrichment of [[wiki/concepts/google-ad-rank-ltv-scoring.md]] and [[wiki/sources/google-ad-rank-briefing.md]], both of which flagged the rGSP randomization mechanism as undocumented. *(news article — DOJ trial reporting; treat specific figures like "3.7x" and "~10% revenue increase" as litigation claims, not confirmed by Google.)*

## Related Pages

- [[wiki/concepts/randomized-gsp-rgsp.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/sources/google-ad-rank-briefing.md]]
