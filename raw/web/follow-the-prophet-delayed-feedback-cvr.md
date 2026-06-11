# Follow the Prophet: Accurate Online Conversion Rate Prediction in the Face of Delayed Feedback

Source: https://arxiv.org/abs/2108.06167 (arXiv:2108.06167)

**Authors:** Haoming Li, Feiyang Pan, Xiang Ao, Zhao Yang, Min Lu, Junwei Pan, Dapeng Liu, Lei Xiao, Qing He
**Venue:** SIGIR 2021 (44th International ACM SIGIR Conference)
**Date:** July 11-15, 2021

## The Delayed Feedback Problem

Unlike clicks, which are observed within seconds of an impression, **conversions
can occur anywhere from minutes to days (or weeks) after the click**. An online
CVR model must make a training decision (label an example as a conversion or
not) before knowing whether a delayed conversion will eventually arrive. The
feedback delay is also **highly diversified** — it varies across ads, users,
and verticals — so a single fixed waiting window cannot cleanly separate
"true negatives" from "not-yet-converted positives."

### Prior approaches and their limits

- **Wait a fixed window, then label**: waiting long enough to observe most
  conversions delays the training signal and makes the model react slowly to
  distribution shift; waiting too short mislabels future converters as
  negatives (biasing the model toward under-prediction).
- **Stream as negative, duplicate as positive on conversion**: ingest every
  impression as a negative immediately, then re-ingest a positive duplicate if
  a conversion arrives later, with importance weighting to correct the bias
  this introduces. This keeps the model fresh but the duplicate/importance-
  weighting correction is itself an approximation, and elapsed-time-based
  weighting schemes (e.g., elapsed-time sampling) only partially correct it.

## The FTP (Follow the Prophet) Solution

FTP defines an idealized **"prophet" model**: the CVR model that *would* exist
if every conversion's true label were available instantly (zero delay). FTP
cannot observe the prophet's labels directly, but it can approximate the
prophet's *predictions* via an **aggregation policy over multiple
time-windowed sub-models**, each trained to capture the conversion pattern
observable within a different elapsed-time interval since the click. The
aggregation is learned so that, in combination, the sub-models' weighted
output imitates what the zero-delay prophet model would have predicted —
without requiring the long wait or the bias-correction heuristics of prior
methods.

## Key Results

Evaluated on three real-world industrial advertising datasets, FTP
outperformed prior state-of-the-art delayed-feedback baselines (including
fixed-window and duplicate-with-importance-weighting approaches) on standard
CVR prediction metrics (the abstract does not report exact numeric deltas).

## Relevance

The delayed feedback problem is a defining characteristic that separates
**CVR prediction from CTR prediction**: CTR models like Google's
FTRL-Proximal system [[raw/web/ad-click-prediction-view-from-the-trenches.md]]
can use near-immediate click/no-click labels for online learning, but a CVR
model's positive label may not arrive until long after the impression that
needs to be scored has already been auctioned. This is why production CVR
systems need delayed-feedback-aware training (FTP and related methods) layered
on top of (or combined with) entire-space architectures like ESMM
[[raw/web/esmm-entire-space-multi-task-model.md]].
