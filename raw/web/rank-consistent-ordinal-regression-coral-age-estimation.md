# Rank Consistent Ordinal Regression for Neural Networks with Application to Age Estimation

Source: https://arxiv.org/abs/1901.07884 (arXiv:1901.07884, PDF fetched from https://arxiv.org/pdf/1901.07884)
Fetched: 2026-06-12

**Authors:** Wenzhi Cao (University of Wisconsin-Madison, Dept. of Statistics), Vahid Mirjalili (Michigan State University, Dept. of Computer Science & Engineering), Sebastian Raschka (University of Wisconsin-Madison)

**Venue:** Pattern Recognition Letters 140 (2020) 325-331; https://doi.org/10.1016/j.patrec.2020.11.008; arXiv submission January 2019, latest revision Nov 13 2020.

---

## Abstract

In many real-world prediction tasks, class labels include information about
the relative ordering between labels, which is not captured by commonly-used
loss functions such as multi-category cross-entropy. Recently, the deep
learning community adopted ordinal regression frameworks to take such
ordering information into account. Neural networks were equipped with ordinal
regression capabilities by transforming ordinal targets into binary
classification subtasks. However, this method suffers from inconsistencies
among the different binary classifiers. To resolve these inconsistencies, we
propose the COnsistent RAnk Logits (CORAL) framework with strong theoretical
guarantees for rank-monotonicity and consistent confidence scores. Moreover,
the proposed method is architecture-agnostic and can extend arbitrary
state-of-the-art deep neural network classifiers for ordinal regression
tasks. The empirical evaluation of the proposed rank-consistent method on a
range of face-image datasets for age prediction shows a substantial reduction
of the prediction error compared to the reference ordinal regression network.

## 1. Introduction

Ordinal regression (also called ordinal classification) describes the task of
predicting labels on an ordinal scale. Here, a ranking rule or classifier h
maps each object x_i in X into an ordered set h: X -> Y, where Y = {r_1 <
... < r_K}. In contrast to classification, the labels provide enough
information to order objects. As opposed to metric regression, the difference
between label values is arbitrary.

The "extended binary classification" approach proposed by Li and Lin (2007)
forms the basis of many ordinal regression implementations. However, neural
network-based implementations of this approach commonly suffer from
classifier inconsistencies among the binary rankings (Niu et al., 2016).

Main contributions:
1. The CORAL framework for ordinal regression with theoretical guarantees for
   classifier consistency.
2. Implementation of CORAL to adapt common CNN architectures (e.g., ResNet)
   for ordinal regression.
3. Experiments on age estimation datasets showing CORAL's guaranteed binary
   classifier consistency improves predictive performance compared to OR-CNN
   (Niu et al., 2016), the reference ordinal regression framework.

## 2. Related Work

Several multivariate extensions of generalized linear models have been
developed for ordinal regression in the past, including the popular
**proportional odds** and **proportional hazards** models (McCullagh, 1980).
The machine learning field developed ordinal regression models based on
extensions of well-studied classification techniques, by reformulating the
problem to utilize multiple binary classification tasks (Baccianella et al.,
2009). Early work includes perceptrons (Crammer and Singer, 2002; Shen and
Joshi, 2005) and support vector machines (Herbrich et al., 1999; Shashua and
Levin, 2003; Rajaram et al., 2003; Chu and Keerthi, 2005). Li and Lin (2007)
proposed a general reduction framework that unified the view of a number of
these existing algorithms.

OR-CNN (Niu et al., 2016) adopted the Li and Lin (2007) general reduction
framework: an ordinal regression problem with K ranks is transformed into K-1
binary classification problems, with the k-th task predicting whether the age
label of a face image exceeds rank r_k, k = 1, ..., K-1. All K-1 tasks share
the same intermediate layers but are assigned distinct weight parameters in
the output layer. While OR-CNN achieves state-of-the-art results on benchmark
datasets, it does not guarantee consistent predictions -- e.g., it would be
contradictory if the k-th binary task predicted the age of a person was more
than 30, but a previous task predicted the age was less than 20. Niu et al.
(2016) acknowledged this inconsistency but noted ensuring consistency would
substantially increase training complexity.

## 3. Proposed Method (CORAL)

### 3.1 Preliminaries

Let D = {(x_i, y_i)}_{i=1}^N be the training dataset, where x_i is the i-th
training example and y_i is the corresponding rank, with ordered rank
r_K > r_{K-1} > ... > r_1. The ordinal regression task is to find a ranking
rule h: X -> Y that minimizes a loss function L(h).

### 3.2.1 Label extension and rank prediction

Given a training dataset, a rank y_i is first extended into K-1 binary labels
y_i^{(1)}, ..., y_i^{(K-1)} such that y_i^{(k)} in {0,1} indicates whether y_i
exceeds rank r_k, i.e., y_i^{(k)} = 1{y_i > r_k}.

Using the extended binary labels during model training, a single CNN is
trained with K-1 binary classifiers in the output layer. The predicted rank
label for an input x_i is obtained via h(x_i) = r_q, where the rank index q is
given by:

  q = 1 + sum_{k=1}^{K-1} f_k(x_i)                                      (Eq. 1)

where f_k(x_i) in {0,1} is the prediction of the k-th binary classifier in the
output layer. Rank-monotonicity requires f_1(x_i) >= f_2(x_i) >= ... >=
f_{K-1}(x_i), so that the binary tasks produce consistent predictions.

### 3.2.2 Loss function

Let W denote the weight parameters of the network excluding the bias units of
the final layer. The penultimate layer's output g(x_i, W) shares a single
weight with all nodes in the final output layer; K-1 independent bias units
b_1, ..., b_{K-1} are added to g(x_i, W) such that {g(x_i, W) + b_k}_{k=1}^{K-1}
are the inputs to the corresponding binary classifiers in the final layer.

With sigma(z) = 1 / (1 + exp(-z)) the logistic sigmoid, the predicted
probability for task k is:

  P_hat(y_i^{(k)} = 1) = sigma(g(x_i, W) + b_k)                          (Eq. 3)

The loss function minimized during training is:

  L(W, b) = - sum_{i=1}^N sum_{k=1}^{K-1} lambda^{(k)} [
      log(sigma(g(x_i, W) + b_k)) * y_i^{(k)}
      + log(1 - sigma(g(x_i, W) + b_k)) * (1 - y_i^{(k)}) ]              (Eq. 4)

This is a weighted cross-entropy of K-1 binary classifiers, where
lambda^{(k)} > 0 is the importance weight of the k-th task. In the paper's
experiments, uniform task weighting was used (lambda^{(k)} = 1 for all k). At
prediction time, binary labels are obtained via f_k(x_i) =
1{P_hat(y_i^{(k)}=1) > 0.5}.

### 3.2.3 Theoretical guarantee (Theorem 1: Ordered bias units)

By minimizing the loss L (Eq. 4), the optimal solution (W*, b*) satisfies:

  b_1* >= b_2* >= ... >= b_{K-1}*                                        (Eq. 6)

Consequently, the predicted confidence scores are non-increasing:

  P_hat(y_i^{(1)}=1) >= P_hat(y_i^{(2)}=1) >= ... >= P_hat(y_i^{(K-1)}=1)  (Eq. 7)

for all i, ensuring classifier consistency, and {f_k} are rank-monotonic. The
key mechanism: because the K-1 binary tasks share the **same weight
parameters** in the final layer (the "weight-sharing constraint") and differ
only in their bias units, the S-shaped sigmoid probability curves for each
task are horizontal shifts of one another and therefore never cross --
guaranteeing rank consistency without needing a cost-matrix or
example-specific task weights (as required by Li and Lin's 2007 framework).

## 4. Experiments

### Datasets

- **MORPH-2** (Ricanek and Tesafaye, 2006): 55,608 face images, ages 16-70.
- **CACD** (Chen et al., 2014): 159,449 images, ages 14-62.
- **AFAD** (Asian Face Database, Niu et al., 2016): 165,501 faces, ages 15-40.

All experiments used a ResNet-34 backbone, trained for 200 epochs with Adam
(beta_1=0.90, beta_2=0.99), batch size 256, learning rate 5e-5 (selected via
hyperparameter search). Each experiment was repeated 3 times with different
random seeds (0, 1, 2).

Three models were compared:
- **CE-CNN**: standard ResNet-34 with cross-entropy classification loss
  (baseline, no ordinal structure).
- **OR-CNN** (Niu et al., 2016): the existing extended-binary-classification
  ordinal regression CNN (rank-inconsistent).
- **CORAL-CNN** (proposed): ResNet-34 with the CORAL output layer.

### Results: Mean Absolute Error (MAE) / Root Mean Squared Error (RMSE), avg +/- SD across 3 seeds

| Method     | MORPH-2 MAE | MORPH-2 RMSE | AFAD MAE | AFAD RMSE | CACD MAE | CACD RMSE |
|------------|-------------|--------------|----------|-----------|----------|-----------|
| CE-CNN     | 3.34 +/- 0.07 | 4.74 +/- 0.11 | 3.60 +/- 0.02 | 5.03 +/- 0.03 | 5.65 +/- 0.11 | 8.07 +/- 0.14 |
| OR-CNN     | 2.83 +/- 0.03 | 3.97 +/- 0.11 | 3.51 +/- 0.04 | 4.75 +/- 0.06 | 5.38 +/- 0.02 | 7.70 +/- 0.09 |
| CORAL-CNN  | **2.64 +/- 0.02** | **3.65 +/- 0.04** | **3.47 +/- 0.05** | **4.71 +/- 0.06** | **5.25 +/- 0.01** | **7.48 +/- 0.06** |

Both OR-CNN and CORAL-CNN outperform CE-CNN (which ignores rank ordering
information) across all three datasets. CORAL-CNN further improves over
OR-CNN on every metric and dataset.

### Rank inconsistency analysis (Table 2)

CORAL-CNN had **zero** rank inconsistencies across all test sets and seeds (by
construction/Theorem 1). OR-CNN exhibited an average of 0.8-2.28
inconsistencies per prediction depending on dataset/seed, and inconsistencies
were *more frequent* on examples OR-CNN predicted incorrectly than on examples
it predicted correctly -- evidence that rank inconsistency harms predictive
performance and that CORAL's consistency guarantee is beneficial.

## 6. Conclusions

CORAL provides classifier consistency for ordinal regression via extended
binary classification, with theoretical guarantees, without requiring
rank- or training-label-dependent weighting schemes. This permits
straightforward implementation and efficient training. CORAL substantially
improved CNN age-estimation performance on three independent datasets and can
be generalized to other ordinal regression problems (e.g., crowd-counting,
depth estimation, customer satisfaction) and architectures (MLPs, RNNs).

Code: https://github.com/Raschka-research-group/coral-cnn
