---
title: "How Google Analytics 4 Collects Data (Analytics Help)"
type: "source_summary"
sources:
  - "web/google-analytics-data-collection.md"
source_url: "https://support.google.com/analytics/answer/9304153"
status: "current"
source_type: "official_documentation"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# How Google Analytics 4 Collects Data (Analytics Help)

**Source type:** `official_documentation`

## Summary

GA4 collects data via the Google tag (gtag.js), Google Tag Manager, the Firebase
SDK (mobile apps), or native CMS integrations. Its **enhanced measurement**
feature automatically captures page views and common interactions (scrolls,
outbound clicks, site search, video engagement, file downloads) without extra
code. Beyond automatic events, GA4 defines **recommended events** with
standardized parameter names (e.g., `purchase`, `sign_up`, `login`) and supports
fully custom events. Newly configured collection appears within ~30 minutes,
verifiable via the Realtime report [[raw/web/google-analytics-data-collection.md]].

## Key Claims

| Claim | Status |
|---|---|
| GA4 is event-based: page views, clicks, purchases, etc. are all "events" | Stated |
| Enhanced measurement auto-collects common events with no code changes | Stated |
| Recommended + custom events extend the standard event vocabulary | Stated |
| GA4 data feeds Google Ads ("powering advertising") | Stated (high-level) |

## Relevance to Ads Ranking

GA4's event stream is one of the primary **conversion-import** sources for Google
Ads [[wiki/synthesis/what-is-a-conversion.md]] [[wiki/sources/google-ads-about-conversions.md]],
and (via BigQuery export, see [[wiki/sources/ga4-bigquery-export-schema.md]]) the
raw data underlying GA4's predictive audiences and conversion-rate signals.

## Related Pages

- [[wiki/synthesis/how-does-google-analytics-work.md]]
- [[wiki/sources/ga4-bigquery-export-schema.md]]
- [[wiki/synthesis/what-is-a-conversion.md]]
