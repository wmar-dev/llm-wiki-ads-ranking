# The Unspoken Truth: Why Importing GA4 Conversions to Google Ads Is a Data Minefield

**Source URL:** https://www.joindatacops.com/resources/the-unspoken-truth-why-importing-ga4-conversions-to-google-ads-is-a-data-minefield/

**Source type:** blog_post (agency/practitioner blog)

---

## Double counting and attribution-model conflict

"Double counting fires when both a native Google Ads conversion tag and a
GA4-imported conversion track the same event simultaneously." GA4 and Google Ads
"are not designed to match": they use different attribution windows, different
counting methods (GA4 counts sessions; Google Ads counts ad interactions), and
different models for cross-device credit.

Recommended fix: **pick one signal as the Smart Bidding source of truth.** "Most
practitioners use native Google Ads tags as the primary Smart Bidding signal
(unaffected by GA4 updates) and GA4 for cross-channel attribution analysis."

This implies there is no automatic reconciliation between a GA4-attributed
conversion and a native-Google-Ads-attributed conversion for the same event —
whichever conversion ACTION the advertiser has marked "primary" / included in
"Conversions" is the one Smart Bidding optimizes against, and if that action is a
GA4-imported one, the credit value GA4's data-driven attribution model assigned is
what Smart Bidding receives.

## Latency

GA4-imported key events go through a multi-step pipeline: GA4 ingests and
processes the event, classifies it as a key event, and only then exports it to
Google Ads. Each step adds latency, typically totaling **6–18 hours** end-to-end —
versus **seconds** for the native Google Ads conversion tag (gtag.js / Google
tag), which reports directly to Google Ads without passing through GA4's
processing pipeline.

For Smart Bidding strategies that bid on conversion volume (Maximize Conversions,
Target CPA, Target ROAS), this latency sets the effective granularity at which the
algorithm observes new conversion data — GA4-imported signals are always several
hours stale relative to native-tag signals.
