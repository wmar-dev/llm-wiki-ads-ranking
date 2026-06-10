---
title: "About Conversions and Conversion Tracking (Google Ads Help)"
type: "source_summary"
sources:
  - "web/google-ads-about-conversions.md"
source_url: "https://support.google.com/google-ads/answer/1722022"
status: "current"
source_type: "official_documentation"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# About Conversions and Conversion Tracking (Google Ads Help)

**Source type:** `official_documentation`

## Summary

Google's official documentation defines a **conversion** as any specific customer
activity an advertiser has decided is valuable — purchases, sign-ups, app
installs, in-app purchases, phone calls, offline/in-store sales, or actions
imported from third-party systems (e.g., Google Analytics, Firebase, CRM).
Conversions are tracked via on-page tags/snippets matched to a click identifier
(cookie, GCLID), automatic app/Play Store reporting, call-forwarding numbers, or
server-side **Enhanced Conversions / Conversion API** uploads of hashed
first-party data. "All conversions" reporting aggregates these across devices and
browsers, attributing each conversion back to the ad click or view that preceded
it within an attribution window. Conversion data — particularly predicted
conversion rate (pCVR) and predicted conversion value — is the primary input to
**Smart Bidding** strategies (Maximize Conversions, Target CPA, Target ROAS)
[[raw/web/google-ads-about-conversions.md]].

## Key Claims

| Claim | Status |
|---|---|
| A conversion is any advertiser-defined valuable customer action (not a fixed taxonomy) | Stated |
| Conversions are tracked via tags/cookies, automatic app reporting, call forwarding, or server-side uploads | Stated |
| Enhanced Conversions / Conversion API send hashed first-party data server-side as cookie tracking degrades | Stated |
| Smart Bidding (Target CPA, Target ROAS, Maximize Conversions) is driven by predicted conversion rate/value | Stated |

## Relevance to Ads Ranking

Conversion-rate prediction (pCVR) and conversion value are the demand-side inputs
that automated bid strategies turn into per-auction bids
[[wiki/synthesis/bidding-types.md]] [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
Privacy-driven changes to conversion tracking (cookie deprecation, Privacy
Sandbox attribution APIs) directly affect how precisely pCVR models can be trained
[[wiki/sources/statistical-learning-attribution-sets.md]].

## Related Pages

- [[wiki/synthesis/what-is-a-conversion.md]]
- [[wiki/synthesis/bidding-types.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/sources/statistical-learning-attribution-sets.md]]
