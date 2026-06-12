---
title: "How to Perform Ordinal Regression / Classification in PyTorch"
type: "source_summary"
sources:
  - "web/how-to-perform-ordinal-regression-classification-in-pytorch.md"
source_url: "https://towardsdatascience.com/how-to-perform-ordinal-regression-classification-in-pytorch-361a2a095a99/"
status: "draft"
source_type: "blog_post"
created: "2026-06-12"
last_updated: "2026-06-12"
---

# How to Perform Ordinal Regression / Classification in PyTorch

**Author:** Mathias Gruber

**Venue:** Towards Data Science (Medium), published July 10, 2021

**Source type:** `blog_post`

---

## Overview

This practical tutorial walks through implementing an **ordinal-aware loss**
in PyTorch using the cumulative-binary-encoding method of Cheng et al. (2008).
On a lipophilicity dataset discretized into five ordered classes (Lowest <
Low < Medium < High < Highest), the author shows that plain cross-entropy
produces a less "diagonal" confusion matrix (more far-off errors) than an
ordinal-aware loss, because cross-entropy penalizes "Lowest predicted as
Highest" the same as "Lowest predicted as Low"
[[raw/web/how-to-perform-ordinal-regression-classification-in-pytorch.md]].

## Method

Each ordinal label is encoded as a **cumulative binary vector** (e.g., Medium
-> [1,1,1,0,0] for 5 classes), and the network produces num_classes sigmoid
outputs trained with **mean squared error** against this expanded target. This
embeds ordinal distance directly into the loss magnitude: a "Lowest predicted
as Highest" error differs from the target vector in 4 positions, while
"Lowest predicted as Medium" differs in only 2. At inference, outputs are
thresholded at 0.5 and the predicted class is the count of consecutive `True`
values from the left
[[raw/web/how-to-perform-ordinal-regression-classification-in-pytorch.md]].
The article also references **CORAL** (Cao et al., 2020) as an alternative
that uses a shared penultimate layer with rank-consistency guarantees
[[raw/web/how-to-perform-ordinal-regression-classification-in-pytorch.md]].

## Key Results

Using RMSE over predicted label indices: a single-split comparison showed
RMSE improving from 1.06 (cross-entropy) to 0.93 (~12% improvement) with the
ordinal loss. However, 10-fold cross-validation across multiple dataset splits
gave "mixed results" -- improvements in most folds but occasional regressions
-- with the ordinal approach helping most consistently on smaller datasets
(~500 molecules)
[[raw/web/how-to-perform-ordinal-regression-classification-in-pytorch.md]].
The author's takeaway: ordinal losses are not guaranteed to beat
cross-entropy/MSE on every dataset and should be tried empirically.

## Relevance to Ads Ranking / ML Systems

Provides a concrete, low-friction implementation pattern (cumulative-encoding
+ MSE on sigmoid outputs) for any model with an ordered categorical target --
e.g., a 1-5 ad-quality star rating -- without needing a custom framework like
CORAL/CORN
[[raw/web/how-to-perform-ordinal-regression-classification-in-pytorch.md]].

## Related Pages

- [[wiki/concepts/ordinal-regression-loss.md]]
