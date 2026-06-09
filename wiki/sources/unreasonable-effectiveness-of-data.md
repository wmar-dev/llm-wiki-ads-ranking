---
title: "The Unreasonable Effectiveness of Data"
type: "source_summary"
sources:
  - "web/unreasonable-effectiveness-of-data.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# The Unreasonable Effectiveness of Data

**Authors:** Alon Halevy, Peter Norvig, Fernando Pereira (Google)

**Published:** IEEE Intelligent Systems, Vol. 24(2), March/April 2009, pp. 8–12

**DOI:** [10.1109/MIS.2009.36](https://doi.org/10.1109/MIS.2009.36)

**Source type:** `peer_reviewed`

---

## Summary

This influential opinion piece, written by three senior Google researchers, argues that the field of AI and NLP should abandon the pursuit of elegant mathematical theories and instead "embrace complexity and make use of the best ally we have: the unreasonable effectiveness of data." The article draws its title and inspiration from Eugene Wigner's 1960 essay on the unreasonable effectiveness of mathematics in physics.

The authors present several key lessons:

1. **Use available large-scale data** rather than waiting for expensive annotated data. The biggest successes (speech recognition, machine translation) come from tasks with naturally occurring training data.

2. **Memorization is good policy with enough data** — simple n-gram models with billions of training examples outperform elaborate models with less data. "Simple models and a lot of data trump more elaborate models based on less data."

3. **There exists a threshold of sufficient data** — once you cross it (e.g., millions of photos instead of thousands), the same algorithm that performed poorly suddenly works well.

4. **Language is inherently complex**, suggesting we can't reduce it to a small set of general rules. Instead, systems should scale with data, using millions of specific features.

## Key Claims

| Claim | Evidence |
|---|---|
| Simple models + lots of data > complex models + less data | N-gram language models, statistical MT phrase tables |
| Memorization is effective at scale | Phrase-based MT outperforms rule-based approaches |
| There is a threshold of sufficient data | Scene completion: poor with thousands, good with millions |
| Unlabeled web data can replace annotated data | Semantic relationships from search query statistics |
| Web-scale corpora capture rare aspects of human behavior | Trillion-word corpus vs. Brown Corpus |

## Relevance to Ads Ranking

While the article focuses on NLP, its core thesis applies directly to production ads ranking systems:

- **Feature scale**: Ads ranking systems use millions of features (user context, ad attributes, historical interactions) — simple models (logistic regression, gradient-boosted trees) with massive feature spaces outperform complex models with fewer features.
- **Natural training data**: Clicks, conversions, and user engagement provide naturally occurring training signals at scale, without expensive human annotation.
- **Memorization vs. generalization**: Large-scale look-up tables (e.g., learned embeddings for every ad or user segment) capture rare patterns that generalize poorly from small samples.
- **Data threshold**: The quality gap between simple and complex ranking models narrows as training data volume passes a threshold — explaining why industry often uses "boring" models with excellent data pipelines.

## Open Questions

- Does the "simple models + lots of data" thesis still hold in the era of deep learning and foundation models, or do sophisticated architectures extract more value from large data?
- What is the data threshold for modern ads ranking systems — when does adding more data yield diminishing returns?
- How does the rise of privacy regulations and signal loss (cookie deprecation, ATT) affect the availability of "free" training data?

## Related Pages

- [[wiki/concepts/web-scale-learning.md]]
