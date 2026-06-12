---
title: "A Simple Approach to Ordinal Classification"
type: "source_summary"
sources:
  - "web/a-simple-approach-to-ordinal-classification-frank-hall.md"
source_url: "https://researchcommons.waikato.ac.nz/items/ce0009f5-92fa-4113-b8b2-7ac929cfd32c"
status: "current"
source_type: "peer_reviewed"
created: "2026-06-12"
last_updated: "2026-06-12"
---

# A Simple Approach to Ordinal Classification

**Authors:** Eibe Frank and Mark Hall, Department of Computer Science,
University of Waikato

**Venue:** University of Waikato Working Paper 01/5 (November 2001), ISSN
1170-487X; also published in *Proceedings of the 12th European Conference on
Machine Learning* (ECML 2001).

**Source type:** `peer_reviewed`

---

## Overview

This is the foundational paper for the **"extended binary classification"**
(a.k.a. binary-decomposition) approach to ordinal classification. The authors
observe that standard classification algorithms discard the natural ordering
in ordinal class attributes (e.g., Cool < Mild < Hot), while standard
regression requires interval/ratio targets, making its application to ordinal
labels "necessarily ad hoc." Their proposed method lets *any* probability-
estimating classifier exploit ordering information without modifying the
underlying learning algorithm
[[raw/web/a-simple-approach-to-ordinal-classification-frank-hall.md]].

## Method

A k-class ordinal problem with ordered values V_1 < V_2 < ... < V_k is
transformed into **k-1 binary classification problems**: the i-th derived
dataset has a binary label encoding the test "is the true class > V_i?". A
standard classifier (the paper uses C4.5 decision trees) is trained on each
derived dataset, producing k-1 probability estimators Pr(Target > V_i | X).
At prediction time, the original class probabilities are reconstructed via:

`Pr(V_1) = 1 - Pr(Target > V_1)`, `Pr(V_i) = Pr(Target > V_{i-1}) - Pr(Target
> V_i)` for 1 < i < k, and `Pr(V_k) = Pr(Target > V_{k-1})` -- i.e., the
probability of an intermediate class is the *difference* between two adjacent
cumulative classifiers' outputs, and the class with maximum reconstructed
probability is predicted
[[raw/web/a-simple-approach-to-ordinal-classification-frank-hall.md]].

## Key Results

The method was tested with C4.5 against the naive (unordered nominal)
approach on 29 numeric regression benchmark datasets (e.g., Abalone,
Ailerons, Auto MPG, Boston Housing, California Housing -- 43 to 40,768
instances each), with each dataset's continuous target discretized into
ordinal classes via equal-frequency binning into 3, 5, and 10 intervals (87
ordinal problems total). The ordinal-decomposition method improved C4.5's
predictive accuracy on unseen data relative to the naive nominal-classification
baseline across this benchmark collection
[[raw/web/a-simple-approach-to-ordinal-classification-frank-hall.md]].

## Relevance to Ads Ranking / ML Systems

This reduction is the conceptual ancestor of modern neural ordinal-regression
frameworks (OR-CNN, CORAL, CORN): any model with K ordered output categories
(e.g., a 1-10 quality score) can be decomposed into K-1 "greater than
threshold" binary classifiers and recombined via the cumulative-probability
formula above. Its main limitation -- which CORAL and CORN later address -- is
that the K-1 binary classifiers can produce mutually inconsistent (non-rank-
monotonic) probability estimates when trained independently
[[raw/web/a-simple-approach-to-ordinal-classification-frank-hall.md]].

## Related Pages

- [[wiki/concepts/ordinal-regression-loss.md]]
- [[wiki/sources/rank-consistent-ordinal-regression-coral-age-estimation.md]]
