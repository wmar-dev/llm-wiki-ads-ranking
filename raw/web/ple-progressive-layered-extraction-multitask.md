# Progressive Layered Extraction (PLE): A Novel Multi-Task Learning (MTL) Model for Personalized Recommendations

Source: https://dl.acm.org/doi/10.1145/3383313.3412236 (fetched via blog summary:
https://blog.bayjarvis.com/paper/progressive-layered-extraction-for-multi-task-learning-in-personalized-recommendations)

**Authors:** Hongyan Tang, Junning Liu, Ming Zhao, Xudong Gong (Tencent PCG)
**Venue:** RecSys 2020 (14th ACM Conference on Recommender Systems)

## Problem Addressed

Multi-task learning (MTL) models that jointly predict related objectives
(e.g., CTR and CVR, or click and watch-time) commonly suffer from two related
failure modes:

- **Seesaw phenomenon**: improving one task's accuracy degrades another's —
  the tasks compete rather than cooperate.
- **Negative transfer**: when tasks are loosely correlated or even
  conflicting, naive parameter sharing (shared-bottom architectures) hurts
  *all* tasks rather than helping any.

Prior architectures address this only partially:

- **Shared-bottom**: a single shared encoder feeds separate task-specific
  heads — simple, but prone to negative transfer when tasks conflict.
- **MMoE (Multi-gate Mixture-of-Experts)**: a set of shared expert
  sub-networks, with a separate gating network per task that learns how to
  combine experts. MMoE mitigates (but doesn't eliminate) negative transfer
  and the seesaw effect, since experts are still fully shared across tasks.

## PLE / CGC Architecture

PLE builds on a **Customized Gate Control (CGC)** module that explicitly
separates:

- **Shared experts** — available to all tasks
- **Task-specific experts** — dedicated to a single task

Each task's gating network combines its own task-specific experts with the
shared experts. PLE then stacks multiple CGC layers with a **progressive
routing/separation** mechanism: deeper layers progressively refine which
shared vs. task-specific representations each task draws on, extracting
increasingly task-relevant semantic knowledge while limiting cross-task
interference.

## Key Results

- Evaluated on a real-world Tencent video recommendation dataset (~1 billion
  samples) with both complicatedly-correlated and normally-correlated task
  pairs; PLE significantly outperformed shared-bottom, MMoE, and other
  state-of-the-art MTL baselines on offline metrics for both tasks
  simultaneously (mitigating the seesaw effect).
- **Online A/B test** on Tencent's large-scale video recommender: **+2.23%
  view-count** and **+1.84% watch time** versus the best prior MTL baseline.
- PLE has been deployed in Tencent's production video recommender system.

## Relevance

PLE (and its predecessor MMoE) are the standard production architectures for
**jointly modeling CTR and CVR as related-but-distinct tasks** — an
alternative/complement to ESMM's entire-space CTR/CVR/CTCVR framing
[[raw/web/esmm-entire-space-multi-task-model.md]]. Where ESMM solves *sample
selection bias* via an entire-space training signal, MMoE/PLE solve *negative
transfer between tasks* via expert-sharing architecture — the two concerns are
orthogonal, and production systems can combine entire-space training with a
PLE-style expert/gating backbone.
