# Matryoshka Representation Learning (arXiv:2205.13147)

Source: https://arxiv.org/abs/2205.13147 (fetched 2026-06-12)

**Authors:** Aditya Kusupati, Gantavya Bhatt, Aniket Rege, Matthew Wallingford, Aditya Sinha, Vivek Ramanujan, William Howard-Snyder, Kaifeng Chen, Sham Kakade, Prateek Jain, Ali Farhadi

**Venue:** NeurIPS 2022 (originally titled "Matryoshka Representations for Adaptive Deployment"; submitted 26 May 2022, latest revision v4 8 Feb 2024)

---

## Abstract / Summary

Learned representations are a central component in modern ML systems, serving a multitude of downstream tasks. When training such representations, it is often the case that computational and statistical constraints for each downstream task are unknown. In this context, rigid, fixed-capacity representations can be either over- or under-accommodating to the task at hand. This leads to the question: can one construct a flexible representation that can adapt to multiple downstream tasks with varying computational resources?

The paper introduces **Matryoshka Representation Learning (MRL)**, which encodes information at different granularities and allows a single embedding to adapt to the computational constraints of downstream tasks. MRL minimally modifies existing representation learning pipelines and imposes no additional cost during inference and deployment. MRL learns coarse-to-fine representations that are as accurate as independently trained low-dimensional representations.

## Training Objective

MRL jointly optimizes a shared encoder F (e.g., a ResNet or ViT backbone) and a set of linear classifier/projection heads {W^(m)} across multiple nested representation sizes m drawn from a set M. The objective (informally):

```
min over {W^(m)}_{m in M}, theta_F  of
  (1/N) * sum_{i in [N]} sum_{m in M} c_m * L( W^(m) * F(x_i)[1:m] ,  y_i )
```

- `F(x_i)` is the full d-dimensional embedding produced by the encoder for input x_i.
- `F(x_i)[1:m]` denotes the **first m dimensions** of that embedding (a nested prefix, not a separate projection).
- `L` is the task loss (e.g., softmax cross-entropy for classification).
- `c_m` is a per-granularity weighting factor (in most experiments set to 1 / equal weighting, i.e., a simple sum of multi-granularity losses).
- The representation sizes M form a set of nested dimensions that are typically powers of two, e.g., **M = {8, 16, 32, 64, ..., 1024, 2048}** for a full 2048-dimensional ResNet representation — O(log d) sizes total.

Because the lower-dimensional representations are literal prefixes (the first m coordinates) of the full embedding, the same vector can be truncated at serving time to any m in M (or interpolated between) without retraining or extra storage — "Matryoshka" nesting like Russian dolls.

## Key Distinctions from Alternatives

- **vs. independently trained fixed-size models**: training N separate models (one per target dimension) is N times the training cost and produces representations that are not nested/compatible with each other. MRL trains once and produces all granularities jointly, matching or exceeding the accuracy of independently trained fixed-size baselines.
- **vs. post-hoc dimensionality reduction (PCA/SVD)**: applying PCA/SVD to a full-size embedding after training is a separate, unsupervised compression step that does not optimize for downstream task accuracy at the reduced size; MRL bakes the multi-granularity objective into representation learning itself, so the truncated prefixes remain task-discriminative.
- **vs. random feature selection / slimmable networks**: the paper shows that selecting a random subset of dimensions from a standard embedding, or using slimmable-network-style approaches, substantially underperforms MRL's nested prefixes.

## Key Quantitative Results

- **ImageNet-1K classification**: MRL representations achieve up to **14x smaller embedding size at the same accuracy** as the original (fixed-size) representation, using an adaptive classification scheme that uses softmax confidence to decide when a coarser (cheaper) embedding suffices and escalates to a finer one otherwise.
- **Large-scale adaptive retrieval (ImageNet-1K and ImageNet-4K/ImageNet-21K-style large retrieval sets)**: up to **14x real-world wall-clock speed-ups** via a funnel/adaptive retrieval scheme — retrieve an initial candidate shortlist with low-dimensional (cheap) embeddings, then re-rank that shortlist with higher-dimensional (expensive) embeddings, measured via mAP@10.
- **Long-tail / few-shot classification**: up to **2% accuracy improvement** for long-tail few-shot classification relative to fixed-representation baselines, while maintaining comparable robustness to distribution shift.
- MRL was evaluated across modalities and architectures: vision (ResNet, ViT on ImageNet-1K), vision-language (ALIGN), and language (BERT), and across training paradigms including supervised learning, contrastive learning (ALIGN), and masked language modeling, demonstrating the approach generalizes beyond a single architecture/modality.
- The method requires **minimal modification** to existing training pipelines (multi-granularity loss term added to the standard objective) and **no additional cost at inference/deployment** — the same single embedding vector is produced; only the chosen prefix length determines compute/storage cost downstream.
- Code was open-sourced by the authors on GitHub.
