---
title: "GA4 Update April 2026: What Changed for Google Ads Conversion Tracking"
type: "source_summary"
sources:
  - "web/ga4-april-2026-conversion-tracking-update.md"
source_url: "https://www.groas.com/post/ga4-update-april-2026-what-changed-google-ads-conversion-tracking-fix"
status: "draft"
source_type: "blog_post"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# GA4 Update April 2026: What Changed for Google Ads Conversion Tracking

**Source type:** `blog_post` (agency/practitioner blog)

## Summary

In April 2026, Google tightened GA4's "key event" qualification rules and
recalibrated GA4's data-driven attribution (DDA) model. `generate_lead` events now
require `currency` and `value` parameters to qualify as a key event; `purchase`
events require unique transaction IDs within a 24-hour window; `begin_checkout`
lost its automatic key-event status; and the default attribution lookback window
for acquisition conversions shortened from 90 days to 30 days
[[raw/web/ga4-april-2026-conversion-tracking-update.md]] *(blog post)*.

## Key Claims

| Claim | Status |
|---|---|
| GA4 key-event criteria tightened (currency/value, transaction-ID dedup, begin_checkout demoted) in April 2026 | Stated |
| GA4's DDA model was recalibrated, redistributing conversion credit across campaigns | Stated |
| Acquisition attribution lookback window shortened 90 → 30 days | Stated |
| Smart Bidding receives the redistributed per-campaign credit even with unchanged user behavior, for GA4-imported conversion actions | Inference (the article describes the redistribution but does not name Smart Bidding explicitly) |

## Relevance to Ads Ranking

This directly informs the [[wiki/synthesis/how-does-google-analytics-work.md]]
open question about how GA4's attribution model interacts with Smart Bidding: for
a **GA4-imported conversion action**, GA4's own DDA model computes the credit
value before that conversion ever reaches Google Ads — so a recalibration of GA4's
DDA model changes Smart Bidding's training signal even when no advertiser setting
in Google Ads itself changed. See
[[wiki/sources/ga4-conversions-google-ads-data-minefield.md]] for how this
interacts with native Google Ads conversion tags.

## Related Pages

- [[wiki/synthesis/how-does-google-analytics-work.md]]
- [[wiki/sources/ga4-conversions-google-ads-data-minefield.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
