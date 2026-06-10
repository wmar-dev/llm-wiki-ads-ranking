---
title: "How Does Google Analytics Work?"
type: "synthesis"
sources:
  - "web/google-analytics-data-collection.md"
  - "web/ga4-bigquery-export-schema.md"
  - "web/google-ads-about-conversions.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# How Does Google Analytics Work?

Google Analytics 4 (GA4) is an **event-based measurement platform**: every user
interaction — a page view, a click, a video play, a purchase — is recorded as an
**event** with a name and a set of parameters, rather than being grouped into
"sessions" the way the older Universal Analytics did
[[wiki/sources/google-analytics-data-collection.md]] *(official documentation)*.

![how-does-google-analytics-work-diagram-1](/assets/how-does-google-analytics-work-diagram-1.svg)

## 1. Data Collection

GA4 collects events from multiple surfaces:

| Surface | Mechanism |
|---|---|
| Website | Google tag (`gtag.js`) snippet, or a GA4 Configuration tag managed via Google Tag Manager |
| Mobile app | Google Analytics for Firebase SDK |
| CMS platforms | Native plugin/integration using a GA4 Measurement ID |

**Enhanced measurement** automatically captures common interactions (page views,
scrolls, outbound clicks, site search, video engagement, file downloads) with no
extra code. Beyond that, GA4 defines **recommended events** with standardized
parameter names (`purchase`, `sign_up`, `login`, etc.) and supports fully
**custom events** for anything else
[[wiki/sources/google-analytics-data-collection.md]]. Newly configured collection
typically appears within ~30 minutes and can be verified in the Realtime report.

## 2. The Event-Based Data Model

Every event is a row (or set of rows) with:

- **`event_params`** — key/value parameters scoped to that event (e.g., page
  location, campaign info)
- **`user_properties`** — custom attributes attached to the user, each with a
  timestamp
- **`items`** — for ecommerce events, a repeatable record of product line items
  (ID, name, price, quantity)

[[wiki/sources/ga4-bigquery-export-schema.md]] *(official documentation)*

## 3. Reporting and Raw-Data Export

GA4's standard UI aggregates this event stream into reports (Realtime,
acquisition, engagement, monetization, exploration). For raw access, GA4 can
**export to BigQuery**: each property gets a dataset
(`analytics_<property_id>`) containing daily `events_YYYYMMDD` tables (and
optional `events_intraday_YYYYMMDD` tables for streaming, deleted once the daily
table finalizes) [[wiki/sources/ga4-bigquery-export-schema.md]].

GA4 also maintains **user-level tables** with audience memberships,
lifetime-value metrics, and **predictive scores** — e.g., purchase-probability
and churn-probability — computed by GA4's built-in ML models. **BigQuery ML** can
layer custom predictive audiences (propensity to purchase, predicted LTV) on top
of the raw export [[wiki/sources/ga4-bigquery-export-schema.md]].

## 4. The Connection to Google Ads and Ad Ranking

This is where GA4 plugs directly into the systems described elsewhere in this
wiki:

- **Conversion import**: GA4 events (e.g., `purchase`, `sign_up`) are one of the
  standard "imported conversions" sources for Google Ads
  [[wiki/synthesis/what-is-a-conversion.md]] [[wiki/sources/google-ads-about-conversions.md]].
- **Click-to-conversion attribution**: the `gclid` (Google Click ID) captured by
  GA4 in `collected_traffic_source` is joined against Google Ads' click-transfer
  data in BigQuery, linking an on-site conversion event back to the specific ad
  click that produced it [[wiki/sources/ga4-bigquery-export-schema.md]].
- **Audiences for targeting and bidding**: GA4's predictive audiences (e.g., users
  with high purchase probability) can be exported to Google Ads for remarketing
  and as signals into **Smart Bidding** (Target CPA/ROAS)
  [[wiki/synthesis/what-is-a-conversion.md]] [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
- **Attribution model**: GA4's default attribution model is **data-driven
  attribution**, which uses machine learning over observed touchpoint sequences
  to assign fractional conversion credit, rather than rigid rules like
  last-click *(Inference: based on aggregated search results, not the primary
  fetched documentation pages — flagged for verification)*.

## Why It Matters for Ads Ranking

GA4 is best understood as the **measurement layer** that sits upstream of the
bidding and ranking systems documented elsewhere in this wiki:

- It is one of the main sources of the **conversion events**
  [[wiki/synthesis/what-is-a-conversion.md]] that train pCVR models.
- Its `gclid`-based join is the concrete plumbing behind **attribution**
  [[wiki/sources/statistical-learning-attribution-sets.md]] — and like
  cookie-based attribution generally, is affected by the same privacy-driven
  shift toward coarser, set-based attribution.
- Its predictive audiences feed **Smart Bidding** and remarketing, which in turn
  determine the bids that enter Google's **Ad Rank** auction
  [[wiki/synthesis/what-is-ad-rank.md]] [[wiki/concepts/google-ad-rank-ltv-scoring.md]].

## Open Questions

- Open question: How does GA4's data-driven attribution model interact with
  Google Ads' own attribution settings when both are active for the same
  conversion — which one ultimately determines the credit used by Smart Bidding?
- Open question: How much latency exists between a GA4-recorded conversion event
  and that signal becoming available to Smart Bidding / Ad Rank for the next
  auction (real-time vs. batch via BigQuery export)?

## Related Pages

- [[wiki/sources/google-analytics-data-collection.md]]
- [[wiki/sources/ga4-bigquery-export-schema.md]]
- [[wiki/synthesis/what-is-a-conversion.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/synthesis/what-is-ad-rank.md]]
