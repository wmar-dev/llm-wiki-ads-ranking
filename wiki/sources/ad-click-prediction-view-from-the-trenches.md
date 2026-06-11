---
title: "Ad Click Prediction: a View from the Trenches"
type: "source_summary"
sources:
  - "web/ad-click-prediction-view-from-the-trenches.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-09"
---

# Ad Click Prediction: a View from the Trenches

**Authors:** H. Brendan McMahan, Gary Holt, D. Sculley, Michael Young, Dietmar Ebner, Julian Grady, Lan Nie, Todd Phillips, Eugene Davydov, Daniel Golovin, Sharat Chikkerur, Dan Liu, Martin Wattenberg, Arnar Mar Hrafnkelsson, Tom Boulos, Jeremy Kubica (Google, Inc.)

**Published:** KDD 2013, August 11–14, Chicago, Illinois, USA. ACM 978-1-4503-2174-7/13/08

**Source type:** `peer_reviewed`

**Processing:** chunked (3 chunks, 8,663 words extracted from PDF)

---

## Summary

This paper presents case studies from Google's deployed CTR prediction system for sponsored search advertising. It covers the FTRL-Proximal online learning algorithm, per-coordinate learning rates, memory-saving techniques at massive scale, evaluation methodology, confidence estimation, calibration, automated feature management, and several unsuccessful experiments. The core message is that practical large-scale learning requires close integration of theoretical advances with engineering pragmatism.

## Key Contributions

### Online Learning and Sparsity (Sections 1–3)

- **FTRL-Proximal algorithm**: Follow The (Proximally) Regularized Leader combines the sparsity of RDA with the accuracy of online gradient descent. Without L1 regularization, it is identical to OGD; with L1, it produces significantly sparser models without accuracy loss. Stores one number per coefficient (z ∈ R^d). Algorithm 1 in the paper gives the full per-coordinate FTRL-Proximal update with L1 and L2 regularization for logistic regression [[raw/web/ad-click-prediction-view-from-the-trenches.md]].

- **Per-coordinate learning rates**: Instead of a global learning rate η_t = 1/√t, each coordinate i uses η_{t,i} = α / (β + √(Σ_{s=1}^{t} g_{s,i}^2)). This accounts for different feature frequencies — rare features keep higher learning rates longer. Reduced AucLoss by 11.2% versus a global learning rate baseline *(peer_reviewed)*. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **Experimental results**: FTRL-Proximal significantly outperformed RDA (+0.6% AucLoss), FOBOS (0.0% AucLoss but +38% non-zero coefficients), and OGD-Count (+216% non-zero coefficients for equal accuracy). [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Memory Saving at Massive Scale (Section 4)

- **Probabilistic feature inclusion**: Poisson Inclusion and Bloom Filter Inclusion methods add rare features to the model probabilistically, avoiding storage of statistics for features that appear only once. Bloom filtering (n=1) saved 55% RAM with only 0.003% AucLoss detriment. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **q2.13 fixed-point encoding**: Replaces 64-bit floating point with 16-bit fixed-point values for coefficient storage. Randomized rounding corrects accumulated roundoff errors. Saved 75% of RAM with no measurable accuracy loss. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **Training many similar models**: Sharing a single hash table across model variants amortizes key storage costs. The per-model cost is only the additional coefficient values. Saves memory, network bandwidth, CPU (one hash lookup instead of many), and disk space. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **Single Value Structure**: An even more compressed approach storing one coefficient value per coordinate shared by all model variants that include that feature. Uses a bit-field to track which variants include the feature. Saved an order of magnitude in RAM compared to the shared hash table approach. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **Learning rates with counts**: Approximates Σ g_{t,i}^2 using only positive/negative event counts (N and P): Σ g^2 ≈ PN/(N+P). This ruthless approximation works as well as the full sum empirically. Combined with shared hash tables, eliminates per-model storage of gradient sums. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **Subsampling training data**: Includes all clicked queries and a fraction r of unclicked queries. Importance weights ω_t = 1 for clicked queries, ω_t = 1/r for unclicked queries correct the bias. The expected weighted objective equals the original objective. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Evaluation Methodology (Section 5)

- **Progressive validation** (online loss) replaces cross-validation. Computing a gradient requires a prediction anyway, so streaming predictions for analysis costs nearly nothing. Measures performance on the most recent data before training on it — analogous to production serving. Uses 100% of data for both training and testing. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **GridViz** interactive visualization enables comprehensive model performance analysis by slicing data across hundreds of dimensions (country, query topic, layout). Color-coded cells with column widths reflecting impression count enable fast outlier detection. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

- **AucLoss** (1 − AUC) and **LogLoss** are the primary metrics. Relative changes (percent change from baseline) are more stable than absolute values, which vary with base click rate. All metrics are designed so smaller is always better. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Confidence Estimation (Section 6)

- **Uncertainty score**: A heuristic confidence measure computable in a single sparse dot product (same cost as prediction). Upper bounds the change in log-odds score from observing one training example: u(x) = αη · x. Validated against a ground-truth model trained on re-labeled data. Performed comparably to bootstrap with 32 models at a fraction of the cost. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Calibration (Section 7)

- **Isotonic regression** for calibration correction: fits a piecewise-linear monotonically increasing function τ(p) to map predicted CTRs to observed CTRs. Significantly reduced bias at both high and low prediction ranges. Without strong assumptions, the feedback loop in the system prevents theoretical guarantees for calibration impact. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Automated Feature Management (Section 8)

- A metadata index manages consumption of thousands of input signals by hundreds of active models. Signals are annotated for deprecation, platform-specific availability, and domain applicability. Automatic alerts vet signals consumed by new and active models. [[raw/web/ad-click-prediction-view-from-the-trenches.md]]

### Unsuccessful Experiments (Section 9)

| Technique | Result | Likely Cause |
|---|---|---|
| Aggressive feature hashing (2^24 features) | Observable loss; no savings at billions of features | Feature count too large for effective hashing |
| Dropout (p = 0.1–0.5) | No benefit; most often detrimental | Sparse features + noisy labels — dropout reduces data rather than regularizing |
| Feature bagging (k models) | −0.1% to −0.6% AucLoss | No benefit; slight degradation |
| Feature vector normalization | Slightly detrimental | Interaction with per-coordinate learning rates and regularization |

## Related Pages

- [[wiki/concepts/web-scale-learning.md]] — scale thesis; this paper provides concrete engineering evidence
- [[wiki/sources/google-ad-rank-briefing.md]] — Google's ad ranking system context
- [[wiki/sources/overlapping-experiment-infrastructure.md]] — Google's experimentation platform
- [[wiki/synthesis/how-ab-tests-work.md]] — evaluation methodology (progressive validation complements A/B testing)
- [[wiki/synthesis/confidence-interval-methods.md]] — uncertainty quantification methods
- [[wiki/synthesis/how-do-ad-systems-predict-conversions.md]] — how this CTR infrastructure (FTRL-Proximal, calibration) is reused and extended for pCVR prediction

## Open Questions

- How do modern deep learning CTR models (e.g., DLRM, DCN) compare with the FTRL-Proximal approach on sparsity-accuracy tradeoffs?
- Does the uncertainty score generalize to modern neural network-based CTR prediction systems with non-linear feature interactions?
- The count-based learning rate approximation Σg²ᵢ ≈ PN/(N+P) (Section 4.5) has a specific consequence for very rare features (<<100 occurrences): if a feature has so far appeared with only one outcome (P=0 or N=0 — common at low counts given typical CTRs of 1–2%), the approximation evaluates to **exactly 0**, which sets the per-coordinate learning rate to its maximum, η_{t,i} = α/β. In effect, the cheaper count-based approximation *amplifies* the "rare features keep higher learning rates longer" property baked into the exact formula — very-low-count features take the largest possible gradient steps per labeled example. The paper does not run a dedicated ablation at the <<100-occurrence regime, but this behavior is mitigated upstream by **probabilistic feature inclusion** (Poisson/Bloom-filter inclusion, Section 4.3): features below the inclusion-count threshold *n* are excluded from the model entirely, so they never receive a learning rate at all. The combination — exclude until count > n, then apply a near-maximal learning rate via the count-based approximation — is the paper's implicit answer to handling very rare features, though a formal variance/accuracy analysis specifically for the <<100-occurrence band remains unpublished [[raw/web/ad-click-prediction-view-from-the-trenches.md]].
