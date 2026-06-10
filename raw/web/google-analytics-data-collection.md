# How Google Analytics 4 Collects Data (Analytics Help)

**Source URL:** https://support.google.com/analytics/answer/9304153

**Source type:** official_documentation

---

## Data Collection Methods

GA4 collects data via several mechanisms:

1. **Google tag (gtag.js)**: a snippet pasted immediately after `<head>` on each
   page of a website, which sends events directly to GA4.
2. **Google Tag Manager (GTM)**: a "Google Analytics: GA4 Configuration" tag
   configured in GTM, which manages the Google tag without editing site code
   directly.
3. **Firebase SDK**: for mobile apps, the Google Analytics for Firebase SDK is
   added to the app to collect events.
4. **CMS integrations**: many website platforms offer native GA4 connections via
   a measurement ID.

## Event-Based Model

GA4's **enhanced measurement** automatically collects page views and a set of
standard events (scrolls, outbound clicks, site search, video engagement, file
downloads) without additional code. Beyond automatic events, GA4 defines
**recommended events** (e.g., `purchase`, `sign_up`, `login`) with standardized
parameter names, plus fully **custom events** for anything else.

## Data Latency

Newly configured data collection may take up to ~30 minutes to begin appearing,
after which it can be verified in the **Realtime report**.

## Connection to Advertising

GA4 configurations feed into "powering advertising" — i.e., GA4 event/conversion
data can be used by Google Ads for conversion measurement, audiences, and bidding
(see the BigQuery export schema source for the mechanics of joining GA4 data to
Google Ads click data).
