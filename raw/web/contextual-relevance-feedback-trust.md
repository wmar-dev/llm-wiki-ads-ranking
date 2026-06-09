# Feedback loops, contextual relevance, and user trust in advertising

Sources:
- https://arxiv.org/abs/2509.00109 — Bias Mitigation for AI-Feedback Loops (2025 survey)
- https://blog.ghostads.io/blog/contextual-advertising-complete-guide/ — Ghost Ad Server (2026)
- https://darge.com/contextual-advertising-vs-behavioral-why-context-wins-in-2026/ — Darge (2026)
- https://www.kantar.com/north-america/company-news/kantar-us-media-reactions-2024 — Kantar (2024)

## Feedback loops in ranker training

Recommender systems that retrain on user reactions to their own predictions create AI feedback loops that amplify biases over time. The 2025 survey "Bias Mitigation for AI-Feedback Loops" (arXiv:2509.00109) found only 24 of 347 papers validated mitigation techniques in multi-round or live settings. Mitigation strategies include:
- **In-processing**: Fairness constraints (FADE, FairAgent), DPO modifications (SPRec)
- **Resampling**: Re-weighting training data to reduce popularity bias
- **Self-play**: Models iteratively suppress biased predictions using their own outputs
- **Simulation-based auditing**: Multi-round simulations reveal that initially-successful mitigations fail in the long term

## When contextual relevance dominates

Research from 2025–2026 shows contextual advertising closing the gap with behavioral targeting:
- Contextual CTR within 5-8% of behavioral (DoubleVerify/IAS 2025)
- Contextual viewability 62-68% vs behavioral 52-58% (+10-15%)
- Contextual brand safety incidents <1% vs behavioral 4-7%
- Contextual CPM 30-40% lower ($2.50-5 vs $4.50-8)
- Contextual reaches 100% of visitors vs 40-55% post-consent
- Seedtag/Nielsen: contextual boosted consumer interest 32% vs demographic targeting
- GumGum: contextual ads generated 43% more neural engagement, 2.2x better recall

Contextual dominates when: privacy regulations limit tracking, brand safety is critical, user intent is clearly signaled by content, and cost efficiency is paramount.

## Balancing relevance with engagement quality and trust

Key findings:
- 40% of consumers find ads irrelevant (Bain 2024)
- Over-targeting drives users to ad blockers (22% mobile ad block rate)
- 40% of consumers don't mind relevant ads if helpful to their shopping experience
- Kantar (2024): consumers prefer "natural" ad experiences; over-targeting drives users offline
- The industry needs cross-stakeholder standards (eyeo-Harris Poll)

The balance requires: user-centric ad formats (native, non-intrusive), AI-powered contextual targeting that doesn't require personal data, Acceptable Ads standards, and transparency about data use.
