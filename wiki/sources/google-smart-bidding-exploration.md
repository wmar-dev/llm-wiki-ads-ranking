---
title: "Smart Bidding Exploration (Google Ads, 2025)"
type: "source_summary"
sources:
  - "web/google-smart-bidding-exploration.md"
source_url: "https://blog.google/products/ads-commerce/smart-bidding-exploration-ai/"
status: "current"
source_type: "official_documentation"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Smart Bidding Exploration (Google Ads, 2025)

**Source type:** `official_documentation`

## Summary

Announced May 2025, **Smart Bidding Exploration** gives Target-ROAS Smart
Bidding a dual mandate: keep hitting the campaign's ROAS target on
established queries, while using an advertiser-configurable **ROAS-tolerance
band (10-30%)** to bid on previously-untargeted "potentially high-performing"
search queries. Google frames this as "expanding the addressable opportunity
set" rather than using bandit/explore-exploit terminology, but functionally
the tolerance band trades short-term ROAS for coverage of untested queries —
the same tradeoff structure as a bandit's explore/exploit balance. March-April
2025 global testing showed **+18%** more unique converting query categories
and **+19%** more conversions
[[raw/web/google-smart-bidding-exploration.md]].

## Key Claims

| Claim | Status |
|---|---|
| Smart Bidding Exploration adds a 10-30% advertiser-configurable ROAS-tolerance band to Target ROAS campaigns, used to bid on previously-untargeted query categories | Stated |
| Google frames this as "opportunity expansion," not as bandit/explore-exploit terminology; no algorithm (UCB, Thompson Sampling, etc.) is named | Stated |
| March-April 2025 testing: +18% unique converting search-query categories, +19% conversions | Stated |
| Eligible campaigns require >=15 conversions in the trailing 30 days | Stated |

## Relevance to Ads Ranking

This is the most direct public evidence addressing the open question on
[[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] about whether Google's
Smart Bidding ([[wiki/concepts/google-ad-rank-ltv-scoring.md]]) uses
bandit-style exploration internally: Google **does** ship an
explore/exploit-shaped mechanism (a tunable ROAS-tolerance band that
deliberately bids into untested query categories at a controlled cost to
short-term ROAS) directly inside Smart Bidding's auction-time bidding — but
publicly frames it as "expansion," not as a named bandit algorithm, and
discloses no mechanics for how the tolerance maps to per-auction bid
adjustments.

## Open Questions

- Open question: Google has not disclosed the underlying algorithm (e.g.,
  whether the ROAS-tolerance band is implemented via a Thompson-Sampling- or
  UCB-style posterior/confidence mechanism, or via a simpler rule-based
  threshold) nor how it composes with the pacing layer described in
  [[wiki/synthesis/ad-pacing.md]].

## Related Pages

- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/synthesis/ad-pacing.md]]
