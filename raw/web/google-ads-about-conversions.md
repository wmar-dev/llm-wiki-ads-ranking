# About Conversions and Conversion Tracking (Google Ads Help)

**Source URL:** https://support.google.com/google-ads/answer/1722022

**Source type:** official_documentation

---

## What Counts as a Conversion

Google defines a conversion as a specific customer activity that is valuable to
your business. You choose what you identify as valuable. Main categories:

- **Website conversions**: purchases, sign-ups, and other actions completed on
  your site.
- **App conversions**: mobile app installs and in-app purchases or activities.
- **Phone call conversions**: calls placed directly from ads, or to phone numbers
  shown on your website (via Google forwarding numbers).
- **Offline conversions**: in-store sales or other offline actions, tracked via
  data imports (e.g., CRM upload, store visits).
- **Imported conversions**: conversions tracked in a third-party or in-house
  system and imported into Google Ads (e.g., Google Analytics goals/events,
  Firebase events, CRM data).

## Tracking Mechanisms

- **Website/app tagging**: when a user clicks an ad, a temporary click identifier
  (e.g., a cookie, GCLID) is associated with their device. A conversion tracking
  tag/snippet on the "thank you"/confirmation page fires when the user completes
  the action, matching it back to the click.
- **Phone call tracking**: Google forwarding numbers automatically record and
  attribute calls without additional tagging.
- **App conversions**: installs and in-app purchases reported through Google Play
  / app SDKs are automatically recorded — no manual tracking code required.
- **Enhanced Conversions / Conversion API**: first-party customer data (e.g.,
  hashed email) is sent server-side to improve match rates as browser-based
  tracking (cookies) degrades.

## Attribution

"All conversions" reporting aggregates cross-device and cross-browser conversion
data, attributing a conversion back to the ad click (or view, for view-through
conversions) that preceded it within a defined attribution/lookback window.

## Connection to Bidding

Conversion data is the core input to **Smart Bidding** strategies:

- **Maximize Conversions** — spend the budget to get as many conversions as
  possible.
- **Target CPA** — hold average cost-per-conversion near a target.
- **Target ROAS** — maximize conversion *value* relative to ad spend.

These strategies use machine-learned predicted conversion rate (pCVR) /
predicted conversion value at auction time to set bids automatically.
