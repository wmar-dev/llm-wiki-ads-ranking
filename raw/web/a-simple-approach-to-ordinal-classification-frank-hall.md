# A Simple Approach to Ordinal Classification

Source: https://hdl.handle.net/10289/64 (University of Waikato Working Paper Series 01/5, ISSN 1170-487X; also published in Proceedings of the 12th European Conference on Machine Learning, ECML 2001)
Fetched: 2026-06-12

**Authors:** Eibe Frank and Mark Hall, Department of Computer Science, University of Waikato, Hamilton, New Zealand

**Date:** November 2001

---

## Abstract

Machine learning methods for classification problems commonly assume that the
class values are unordered. However, in many practical applications the class
values do exhibit a natural order -- for example, when learning how to grade.
The standard approach to ordinal classification converts the class value into
a numeric quantity and applies a regression learner to the transformed data,
translating the output back into a discrete class value in a post-processing
step. A disadvantage of this method is that it can only be applied in
conjunction with a regression scheme. In this paper we present a simple method
that enables standard classification algorithms to make use of ordering
information in class attributes. By applying it in conjunction with a decision
tree learner we show that it outperforms the naive approach, which treats the
class values as an unordered set. Compared to special-purpose algorithms for
ordinal classification our method has the advantage that it can be applied
without any modification to the underlying learning scheme.

## 1. Introduction

Statisticians differentiate between four levels of measurement: nominal,
ordinal, interval, and ratio. Nominal and ordinal quantities both represent
categories, but ordinal quantities additionally exhibit an order among their
values (e.g., an attribute representing outdoor temperature with values Hot,
Mild, Cool, where Hot > Mild > Cool). Interval and ratio quantities exhibit
order *and* fixed, equal units between values; ordinal values lack this
property, so arithmetic differences between ordinal labels are not meaningful.

Standard classification algorithms can be applied to ordinal problems by
discarding the ordering information, but this loses information that could
improve predictive performance. Standard regression techniques can be applied
when the target is an interval/ratio quantity, but applying them to truly
ordinal targets is "necessarily ad hoc." This paper presents a simple method
that enables standard classification algorithms to exploit ordering
information in ordinal prediction problems, without requiring any modification
to the underlying learning algorithm -- it only requires that the classifier
produce class probability estimates.

## 2. Transforming the Ordinal Classification Problem (the method)

The core idea: transform a k-class ordinal problem into **k-1 binary
classification problems**.

Given an ordinal attribute A* with ordered values V_1 < V_2 < ... < V_k, the
method derives k-1 binary attributes A*_1, ..., A*_{k-1}, one for each of the
first k-1 original values. The i-th binary attribute represents the test
A* > V_i (i.e., A*_i = 1 if the true class exceeds V_i, else 0).

**Training:** k-1 new datasets are derived from the original training set, one
per binary attribute. Each derived dataset contains the same attribute values
as the original (minus the class attribute) but with a binary class label
encoding "is the true ordinal value greater than V_i?" A standard
probability-estimating classifier (the paper uses C4.5 decision trees) is
trained on each derived dataset, producing k-1 models that each estimate
Pr(Target > V_i | X).

**Prediction:** For an unseen instance, each of the k-1 classifiers is queried
to obtain Pr(Target > V_i | X) for i = 1, ..., k-1. The probability of each
original ordinal class value V_i is then reconstructed as:

  Pr(V_1)   = 1 - Pr(Target > V_1)
  Pr(V_i)   = Pr(Target > V_{i-1}) - Pr(Target > V_i),   for 1 < i < k
  Pr(V_k)   = Pr(Target > V_{k-1})

That is: the probability of the lowest class depends only on the first
classifier (1 minus its output); the probability of the highest class depends
only on the last classifier; and the probability of each intermediate class is
the *difference* between two adjacent cumulative-probability classifiers. The
class with maximum reconstructed probability is assigned as the predicted
label.

A key practical advantage: this method requires **no modification to the
underlying learning algorithm** -- it works with any classifier that produces
class probability estimates (decision trees, k-NN, etc.), unlike
special-purpose ordinal regression algorithms that require custom model
formulations.

## 3. Experimental Results

The method was evaluated using the C4.5 decision tree learner against the
naive approach (treating ordinal classes as an unordered nominal attribute).
Since ordinal-labeled benchmark datasets were scarce, the authors took 29
publicly available numeric regression datasets (e.g., Abalone, Ailerons,
Delta Ailerons, Elevators, 2D Planes, Pole Telecomm, Auto MPG, Boston Housing,
California Housing, Census Domain, Computer Activity, Pumadyn, Bank Domain,
Kinematics of Robot Arm, etc. -- ranging from 43 to 40,768 instances) and
discretized each numeric target into ordinal classes via **equal-frequency
binning** into 3, 5, and 10 intervals, producing three ordinal versions of
each dataset (87 total ordinal problems). Equal-frequency binning divides the
range of observed values into intervals each containing approximately the same
number of instances, yielding ordered class values representing variable-size
ranges of the original numeric quantity.

Results (referenced in the abstract and conclusions) show the proposed
ordinal-decomposition method improves the predictive accuracy of C4.5 decision
trees on unseen data compared to the naive nominal-classification approach,
across this collection of discretized regression benchmarks.

## 4. Related Work / Discussion

The paper discusses prior custom-built algorithms for ordinal classification
(both classification-based and regression-based extensions) and contrasts
them with the proposed approach's main advantage: applicability "without any
modification of the underlying learning scheme," since it only requires the
base classifier to output class probabilities. This generality is what made
the Frank & Hall "extended binary classification" reduction influential as a
baseline framework that later neural-network ordinal regression methods (e.g.,
OR-CNN, CORAL) build upon and aim to fix rank-consistency issues in.
