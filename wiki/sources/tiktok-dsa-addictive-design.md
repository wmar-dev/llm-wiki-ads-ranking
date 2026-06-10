---
title: "Addictive Design on Online Platforms (TikTok DSA Enforcement)"
type: "source_summary"
sources:
  - "web/tiktok-dsa-addictive-design.md"
source_url: "https://epthinktank.eu/2026/05/06/addictive-design-on-online-platforms/"
status: "current"
source_type: "official_documentation"
processing_status: "processed"
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Addictive Design on Online Platforms (TikTok DSA Enforcement)

**Publisher:** European Parliamentary Research Service (EPRS), European Parliament Think Tank

**Published:** May 6, 2026

**Source type:** `official_documentation` (EU Parliament briefing summarizing European Commission enforcement action)

## Overview

This EPRS briefing summarizes the European Commission's **February 6, 2026** preliminary finding that TikTok breached the Digital Services Act (DSA) due to the addictive design of its recommender system — the first DSA enforcement action targeting platform/algorithm architecture itself rather than illegal content, data protection, or competition [[raw/web/tiktok-dsa-addictive-design.md]].

## Key Findings

- **Engagement design**: Infinite scroll, autoplay, push notifications, and TikTok's highly personalized recommender system drive average daily usage of **137 minutes**, up from 27 minutes in 2019.
- **Minor well-being**: TikTok's recommender "generate[s] systemic risks to the mental well-being of minors" via "prolonged, compulsive engagement that users struggle to control" — linked to higher depression/anxiety. A 2025 survey found ~50% of US teens (13–17) describe themselves as online "almost constantly." TikTok is the most-used platform after midnight among 13–18 year-olds in the EU; 7% of 12-15 year-olds spend 4-5 hrs/day on the app.
- **Regulatory finding**: The Commission found TikTok "disregarded important indicators of compulsive use," specifically **time spent at night** and **app-opening frequency** — i.e., DSA audits target *behavioral proxies* of the recommender's effects, not the ranking algorithm's internals.
- **Remedies under discussion**: disabling key addictive features (e.g., infinite scroll over time) and restructuring the platform's "core architecture." DSA Article 35 requires VLOPs to adapt the algorithmic/recommender system, age verification, and parental controls as part of systemic-risk mitigation.
- **TikTok's own mitigations**: 50+ teen-account features/settings; 25M+ suspected under-13 accounts removed globally in the most recent quarter.

## Relevance to Ads Ranking / Recommendation Systems

This source provides a current, authoritative answer to two related questions about TikTok's recommendation algorithm:

1. **Watch-time vs. well-being**: TikTok's algorithm does not appear to distinguish "healthy" from "compulsive" engagement at the optimization level — the same signals (watch time, session frequency, night-time usage) that the algorithm uses to maximize engagement are the signals regulators now flag as evidence of harm. The EU's Feb 2026 finding treats this as a *systemic risk requiring architectural mitigation*, not merely a content-moderation issue.
2. **DSA auditability of unsupervised recommendation**: Yes, in practice — but the audit doesn't require introspecting the unsupervised clustering/embedding pipeline itself. Instead, DSA Article 35 enforcement operationalizes "addictive design" via **behavioral outcome proxies** (time-of-day usage patterns, session frequency/duration) that can be measured without algorithmic transparency, then mandates *design-level* remedies (disabling autoplay/infinite scroll, age verification) rather than algorithmic changes per se [[raw/web/tiktok-dsa-addictive-design.md]].
