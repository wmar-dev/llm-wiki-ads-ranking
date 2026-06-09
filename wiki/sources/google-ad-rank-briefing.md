---
title: "How Search Ads are Ranked and Priced on Google"
type: "source_summary"
sources:
  - "web/google-ad-rank-briefing-paper.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# How Search Ads are Ranked and Priced on Google

**Source:** Google (submitted in DOJ antitrust case, Exhibit UPX0010)

**URL:** [justice.gov](https://www.justice.gov/d9/2023-10/416881.pdf)

**Source type:** `other` (regulatory filing — internal Google briefing paper prepared for UK CMA, submitted as evidence in US v. Google)

**Processing:** 4,765 words extracted from 31 MB PDF; single pass.

---

Google's internal briefing paper explaining the Ad Rank system used in Google Search ads. Prepared for the UK Competition & Markets Authority in response to its RFI dated 14 February 2020. This is the most detailed public description of Google's ad ranking mechanics.

## Core Ad Rank Formula

Google ranks ads using a **Long-Term Value (LTV) Score**, which accounts for both expected revenue and expected costs of showing an ad:

```
LTV = eCPM - (impression cost + click cost)

Where:
  eCPM = bid × pCTR            (expected revenue per mille impressions)
  Impression cost = f(1 - pCQ) (cost of showing a low-quality ad creative)
  Click cost     = f(1 - pLQ)  (cost of a poor landing page experience)
```

### Components

| Component | Full name | What it measures |
|---|---|---|
| Bid (Max CPC) | Maximum cost-per-click | Advertiser's willingness to pay per click |
| pCTR | Predicted click-through rate | Likelihood user will click the ad |
| pCQ | Predicted creative quality | Quality of ad copy/creative |
| pLQ | Predicted landing page quality | Quality of post-click landing page experience |

**Key property:** Inverse relationship between bid and quality — low-quality ads need higher bids to compete; high-quality ads can win with lower bids.

## Eligibility and Pricing

- Only ads with **LTV > 0** are eligible to show on the SERP
- Ads ranked by LTV score, highest to lowest
- **Actual CPC** = minimum required to: (a) clear the Ad Rank threshold (LTV = 0) AND (b) beat the next-best competitor's LTV score
- If no competitor cleared the threshold, the winner pays the **reserve price** (minimum bid achieving LTV > 0)
- Top-slot and bottom-slot thresholds differ

## rGSP (Randomized General Second-Price Auction)

Launched globally since January 2019. A variant of GSP that introduces randomization into the auction mechanism. The document does not fully detail the randomization logic.

## Key Signals Used in Automated Bidding

Google's Smart Bidding uses auction-time signals to set bids dynamically. Signals include: device, location, time of day, remarketing lists, and other contextual features. Bid strategies: Target CPA, Target ROAS, Maximize Clicks, Maximize Conversions, Enhanced CPC, Target Impression Share.

## Discrepancies vs. Existing Wiki Pages

| Existing page claim | Google paper | Note |
|---|---|---|
| GSP ranks by `bid × quality score` | LTV = eCPM - costs (more complex) | The simplification omits the cost side of LTV |
| GSP winners pay next bidder's adjusted price | Winners pay max(threshold, next competitor's price) | Reserve pricing is a significant factor (~XX% of clicks, redacted) |
| GSP is the current mechanism | rGSP launched Jan 2019 (randomized variant) | Existing pages do not reference rGSP |

These are not contradictions — the existing pages describe the theoretical model; this source reveals the production implementation.
