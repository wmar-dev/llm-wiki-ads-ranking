# GA4 BigQuery Export Schema (Analytics Help)

**Source URL:** https://support.google.com/analytics/answer/7029846

**Source type:** official_documentation

---

## Tables

Each GA4 property linked to BigQuery gets a dataset named `analytics_<property_id>`:

- **`events_YYYYMMDD`** — daily table of raw event data, created if Daily export
  is enabled. Receives updates for up to ~3 days after the event date to account
  for device-side latency.
- **`events_intraday_YYYYMMDD`** — populated continuously throughout the current
  day if Streaming export is enabled; deleted once the corresponding daily table
  is finalized.

## Row/Record Structure

A single event may span multiple rows depending on repeated `RECORD` fields:

- **`event_params`** — repeatable key/value records holding event-scoped and
  campaign-level parameters (string, int, or double values).
- **`user_properties`** — repeatable key/value records of custom user
  attributes, each with a `set_timestamp_micros`.
- **`items`** — repeatable record for ecommerce line items (product ID, name,
  price, quantity, plus custom `item_params`).

## Predictive Metrics and Google Ads Integration (from related search results)

- GA4 also exports **user-level tables** with one row per user identifier,
  including audience memberships, lifetime value metrics, and **predictive
  scores** (e.g., purchase-probability, churn-probability) computed by GA4's
  built-in ML models.
- **BigQuery ML** can be layered on top of the raw export to build custom
  **predictive audiences** (e.g., propensity to purchase, predicted LTV).
- To join GA4 data with Google Ads click data, the BigQuery Data Transfer
  Service for Google Ads is configured, then `collected_traffic_source.gclid`
  from GA4 events is joined to `ads_ClickStats_customer_id.gclid` from the Google
  Ads transfer — connecting on-site conversion events back to the specific ad
  click that drove them.
