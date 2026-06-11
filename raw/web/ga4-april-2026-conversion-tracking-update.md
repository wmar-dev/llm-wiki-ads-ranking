# GA4 Update April 2026: What Changed, What Broke For Google Ads Advertisers, And What To Fix Right Now

**Source URL:** https://www.groas.com/post/ga4-update-april-2026-what-changed-google-ads-conversion-tracking-fix

**Source type:** blog_post (agency/practitioner blog)

---

## What changed in the April 2026 GA4 update

- `generate_lead` events now require both `currency` and `value` parameters to be
  populated to qualify as a "key event" (GA4's term for what feeds Google Ads as a
  conversion). Previously, lead submissions could count without these fields —
  conversion volume can drop even though user behavior is unchanged, because GA4
  simply stops counting events that no longer meet the stricter criteria.
- `purchase` events now require unique transaction IDs within a 24-hour window to
  be counted (de-duplication).
- `begin_checkout` was demoted from an automatic key event — it can still be
  manually promoted, but no longer counts by default.
- The default attribution lookback window for acquisition conversions shifted from
  90 days to 30 days.
- Google "recalibrated its data-driven attribution model" as part of this update.

## Effect on Smart Bidding signals

Because GA4-imported conversions carry GA4's own attribution-assigned credit value
into Google Ads, the April 2026 DDA recalibration redistributes credit across
touchpoints differently than before — "the same number of actual conversions may
be distributed differently across campaigns, making some campaigns appear to have
lost volume." Smart Bidding (Target CPA/ROAS, Maximize Conversions) receives these
altered per-campaign signals even when total user behavior hasn't changed, and now
operates on a narrower (30-day vs 90-day) historical attribution window for
acquisition conversions.

## Recovery guidance

After re-linking GA4 properties to Google Ads or adjusting key-event definitions,
the article recommends allowing 24–48 hours before expecting full data flow to
resume — this is setup-recovery time, not normal operating latency.

## What the article does NOT cover

- No specifics on real-time vs. batch (BigQuery) latency for the GA4 → Google Ads
  conversion-import pipeline under normal operation.
- No explicit statement on which attribution model (GA4's vs. Google Ads')
  Smart Bidding consults when both are configured for the same physical
  conversion event — only that GA4's DDA model determines the *credit value*
  baked into a GA4-imported conversion action before it reaches Google Ads.
