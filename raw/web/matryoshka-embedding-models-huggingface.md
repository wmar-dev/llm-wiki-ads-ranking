# Matryoshka Embedding Models (Hugging Face blog)

Source: https://huggingface.co/blog/matryoshka (fetched 2026-06-12)

**Authors:** Tom Aarsen, Joshua (Xenova), Omar Sanseviero (Hugging Face)

**Published:** February 23, 2024

---

## What They Are

Matryoshka embedding models produce numerical representations (embeddings) where "more important information" is concentrated in the earlier dimensions and less critical information is concentrated in later dimensions. This design allows embeddings to be **truncated to smaller sizes** while largely preserving downstream performance — analogous to Matryoshka / Russian nesting dolls, where smaller dolls are nested inside larger ones.

This directly mirrors the approach taken by OpenAI's `text-embedding-3-small` and `text-embedding-3-large` models, which support a `dimensions` parameter allowing users to request shorter embeddings natively from the API rather than truncating client-side.

## Training Mechanism

Standard embedding model training optimizes a single loss (e.g., a contrastive/cosine-similarity loss such as `CoSENTLoss`, `MultipleNegativesRankingLoss`, etc.) computed on the full-dimensional embedding output by the model.

Matryoshka training instead computes that **same loss function repeatedly at multiple truncated dimensionalities** (e.g., full size 768, then 512, 256, 128, 64), then **sums all of these per-dimension losses together** into a single final loss value that is backpropagated. As the post states: "The loss values for each dimensionality are added together, resulting in a final loss value." This trains the model so that the embedding remains useful and discriminative even when only its first k dimensions are kept.

**Sentence Transformers implementation**: the library provides a `MatryoshkaLoss` wrapper that takes a base loss (e.g., `CoSENTLoss`, `MultipleNegativesRankingLoss`) plus a list of target dimensions, and applies/sums the base loss across each of those truncated dimensions during training. An optional per-dimension weighting can be supplied.

## Inference / Truncation

At inference time, a Matryoshka-trained Sentence Transformers model can be loaded with a `truncate_dim` parameter, and the model automatically truncates output embeddings to that size. Important caveat: if embeddings are normalized (e.g., L2-normalized for cosine similarity), they must be **re-normalized after truncation**, since truncating a normalized vector changes its norm.

## Benchmark Results

On the STSBenchmark (semantic textual similarity) evaluation, a Matryoshka-trained model retained almost all of its quality even at drastically reduced sizes: **even at 8.3% of the original embedding size (e.g., 64 of 768 dimensions), the Matryoshka model preserved 98.37% of the full-size performance**. This illustrates the steep diminishing-returns curve of embedding dimensionality for retrieval/similarity tasks once the model is trained with the Matryoshka objective.

## Practical Implication

This gives practitioners a single tunable knob — embedding dimension at inference/storage time — to trade off between retrieval quality and infrastructure cost (vector storage size, memory, ANN index size, network transfer, and search latency), without retraining or maintaining multiple separate models.
