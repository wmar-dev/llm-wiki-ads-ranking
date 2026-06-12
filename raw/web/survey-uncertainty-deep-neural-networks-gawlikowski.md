# A Survey of Uncertainty in Deep Neural Networks

**Authors:** Jakob Gawlikowski, Cedrique Rovile Njieutcheu Tassi, Mohsin Ali,
Jongseok Lee, Matthias Humt, Jianxiang Feng, Anna Kruspe, Rudolph Triebel,
Peter Jung, Ribana Roscher, Muhammad Shahzad, Wen Yang, Richard Bamler, Xiao
Xiang Zhu — arXiv:2107.03342 (2021, published in *Artificial Intelligence
Review* / Machine Learning journal).

Source URL: https://arxiv.org/abs/2107.03342

## Epistemic vs. Aleatoric Uncertainty

- **Epistemic (model) uncertainty**: arises from shortcomings of the model
  itself — inadequate architecture, insufficient training, or training data
  that doesn't cover the input distribution. It is, in principle,
  **reducible** with better models/more data.
- **Aleatoric (data) uncertainty**: arises from the data-generating process
  itself — measurement noise, label noise, inherent randomness. It is
  **irreducible**.

## Core Uncertainty Quantification Methods

### Bayesian Neural Networks (BNNs)

Model network parameters as probability distributions instead of fixed point
estimates; predictive uncertainty comes from marginalizing over the parameter
posterior via Bayes' theorem. Three approximation families:

- **Variational inference**: approximate the intractable posterior with a
  tractable distribution by minimizing KL divergence. **Monte Carlo (MC)
  dropout** is a special case — dropout layers are reinterpreted as Bernoulli
  variational distributions, so running many stochastic forward passes at
  inference approximates sampling from the posterior. Cheap and easy to add
  to existing networks, but the approximation is biased and sensitive to
  hyperparameters (dropout rate).
- **Sampling methods (MCMC / SG-MCMC)**: draw samples directly from the
  posterior via Markov chain methods. Unbiased and can represent multimodal
  posteriors, but computationally expensive with hard-to-assess convergence.
- **Laplace approximation**: approximate the posterior as a Gaussian centered
  at the MAP estimate using the Hessian. Can be applied post-hoc to an
  already-trained network, but the local quadratic approximation can underfit
  complex posteriors.

### Single Deterministic Methods

Extract an uncertainty estimate from a **single forward pass** of a single
deterministic network — no sampling required.

- **Internal methods** (e.g., Evidential Deep Learning, Prior Networks): the
  network directly outputs parameters of a distribution over outputs (e.g.,
  parameters of a Dirichlet distribution over class probabilities, drawing on
  Dempster-Shafer evidence theory). Computationally cheap at inference, but
  the loss functions are more complex to train and some formulations cannot
  cleanly separate epistemic from aleatoric uncertainty.
- **External methods**: a separate auxiliary model/component (e.g.,
  gradient-based metrics, density-estimation networks) estimates uncertainty
  on top of an unmodified base predictor — preserves the original prediction
  but adds inference-time overhead for the auxiliary model.

### Deep Ensembles

Train multiple networks independently (different initializations/data
orderings) and combine their predictions; the **spread across ensemble
members** is the uncertainty signal. Diversity among members is what makes
this work. Strong empirical performance and simple to implement, but the cost
is multiplied by the ensemble size for both training and inference.

### Test-Time Augmentation

Apply multiple input transformations (crops, rotations, noise) to the same
input at inference time on a single deterministic model, and use the
**variance across the resulting predictions** as the uncertainty estimate.
Cheap to add (no extra training), but adds inference-time cost proportional
to the number of augmentations and is sensitive to which augmentations are
chosen.

## Calibration

A model can produce confident-looking scores that don't match its actual
accuracy ("badly calibrated"). Common post-hoc calibration methods:

- **Temperature scaling**: divide logits by a single learned scalar
  temperature before the softmax/sigmoid.
- **Platt scaling**: fit a sigmoid (with learned scale + bias) on top of the
  raw scores.
- **Isotonic regression**: fit a non-parametric, monotonically increasing
  mapping from predicted scores to observed outcome rates.

**Measurement**: calibration quality is assessed via **reliability diagrams**
(binned predicted-confidence vs. observed-accuracy plots) and the **Expected
Calibration Error (ECE)** — the average gap between predicted confidence and
observed accuracy across confidence bins.

## Practical Trade-offs

- Single deterministic methods: cheapest, but limited ability to decompose
  epistemic vs. aleatoric uncertainty.
- Bayesian methods (BNNs, MC dropout): principled probabilistic framing, but
  computational cost scales with the number of posterior samples (forward
  passes).
- Deep ensembles: strong empirical results, but cost scales linearly with
  ensemble size for both training and serving.
- Calibration methods are typically applied **on top of** any of the above —
  a model can have a good *ranking* of uncertainty estimates but still be
  poorly *calibrated* in absolute terms, and vice versa.
