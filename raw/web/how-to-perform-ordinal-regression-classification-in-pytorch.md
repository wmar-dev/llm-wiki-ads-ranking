# How to Perform Ordinal Regression / Classification in PyTorch

Source: https://towardsdatascience.com/how-to-perform-ordinal-regression-classification-in-pytorch-361a2a095a99/
Fetched: 2026-06-12

**Author:** Mathias Gruber
**Published:** July 10, 2021
**Venue:** Towards Data Science (Medium)

---

## Overview

Standard multiclass classification treats all misclassifications equally. But
when target classes have an inherent ordering -- e.g., student grades (A > B
> C > D > E) or efficiency ratings (High > Medium > Low) -- this is suboptimal:
"the model will assume that the error of misclassifying an A as a D is just as
bad as misclassifying A as a B," when in reality, errors that are farther apart
on the ordinal scale should incur a larger penalty. Cross-entropy loss, designed
for nominal (unordered) categories, ignores this ordinal structure entirely.

## Demonstration Dataset

The article uses a lipophilicity dataset, with the continuous target
discretized into five ordered classes (Lowest < Low < Medium < High <
Highest). It shows that a model trained with plain cross-entropy on these
five classes produces a *less diagonal* confusion matrix (more far-off
errors) than a model trained with an ordinal-aware loss.

## Primary Method Described: Cheng et al. (2008) cumulative binary encoding

Each ordinal class is encoded as a **cumulative binary vector** ("extended
target"), where the network has num_classes sigmoid outputs and the target
vector has 1s up to and including the true class index, then 0s:

- Lowest  -> [1,0,0,0,0]
- Low     -> [1,1,0,0,0]
- Medium  -> [1,1,1,0,0]
- High    -> [1,1,1,1,0]
- Highest -> [1,1,1,1,1]

The network outputs five independent sigmoid activations and is trained with
**mean squared error (MSE)** between the predicted sigmoid vector and this
expanded cumulative target vector. This encoding naturally embeds ordinal
distance into the loss: the squared-error difference between predicting
"Lowest" when the truth is "Highest" (4 positions of mismatch) is larger than
predicting "Lowest" when the truth is "Medium" (2 positions of mismatch),
unlike one-hot cross-entropy where all wrong classes are penalized equally.

At inference, a 0.5 threshold is applied to each of the five sigmoid outputs,
and the predicted ordinal class is obtained by counting the number of
consecutive `True` values starting from the left (position 1).

## Alternative Method Mentioned: CORAL (Cao et al., 2020)

The article also mentions CORAL, which uses a shared penultimate layer (single
shared weight vector) with separate bias units for each binary output,
emphasizing rank-consistency among the binary sub-classifiers -- contrasted
with the simpler Cheng et al. cumulative-encoding + MSE approach used as the
article's primary method.

## Implementation Recipe

1. **Input:** raw network logits/predictions of shape [batch_size,
   num_labels], plus integer target label indices.
2. **Process:** expand each integer target label into its cumulative binary
   vector (as shown above).
3. **Loss:** compute MSE between the sigmoid-activated predictions and the
   expanded cumulative target vectors.
4. **Inference:** threshold each output at 0.5, then count consecutive `True`
   values from the left to recover the predicted ordinal class index.

## Empirical Results

Using RMSE over predicted label indices as the evaluation metric:
- On a single dataset split, the ordinal (cumulative-encoding) loss improved
  RMSE from 1.06 (plain cross-entropy) to 0.93 -- a ~12% improvement.
- Across a 10-fold cross-validation over multiple datasets, results were
  "mixed" -- improvements in most cases but occasional regressions.
- On smaller datasets (~500 molecules), the ordinal approach gave more
  consistent improvements over plain cross-entropy.

## Key Takeaway

The author's conclusion: "there is no free lunch, and one should train models
with different loss functions to see what works best for a given dataset" --
i.e., ordinal losses are not guaranteed to beat cross-entropy/MSE on every
dataset, but are worth trying whenever target classes have a meaningful order.
