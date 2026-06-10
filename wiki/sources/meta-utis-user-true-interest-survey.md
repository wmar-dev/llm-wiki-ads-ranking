---
title: "User True Interest Survey (UTIS)"
type: "source_summary"
sources:
  - "web/meta-utis-user-true-interest-survey.md"
status: "current"
source_type: other
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# User True Interest Survey (UTIS)

**Source:** Engineering at Meta — [Adapting the Facebook Reels RecSys AI Model Based on User Feedback](https://engineering.fb.com/2026/01/14/ml-applications/adapting-the-facebook-reels-recsys-ai-model-based-on-user-feedback/)

**Date:** January 14, 2026

UTIS collects randomized in-feed survey responses ("How well does this video match your interests?" 1-5 scale) and trains a lightweight Perception Layer on binarized responses. Integrated into late-stage ranking, early retrieval, and sequence-based retrieval via knowledge distillation. Key findings: +5.4% high survey ratings, -6.84% low ratings, +5.2% total engagement, -0.34% integrity violations. Precision improved from 48.3% (heuristic) to 63.2%. Accuracy 59.5% → 71.5%. Demonstrated that true interest alignment and engagement are complementary, not conflicting.
