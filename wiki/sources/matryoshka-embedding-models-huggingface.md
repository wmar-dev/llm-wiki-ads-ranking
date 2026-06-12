---
title: "Matryoshka Embedding Models (Hugging Face)"
type: "source_summary"
sources:
  - "web/matryoshka-embedding-models-huggingface.md"
source_url: "https://huggingface.co/blog/matryoshka"
status: "draft"
source_type: "other"
processing_status: "processed"
ingest_count: 1
created: "2026-06-12"
last_updated: "2026-06-12"
---

# Matryoshka Embedding Models (Hugging Face)

**Authors:** Tom Aarsen, Joshua (Xenova), Omar Sanseviero (Hugging Face)

**Published:** February 23, 2024

**Source type:** `other` (official company engineering blog post)

---

## Overview

This Hugging Face engineering blog post explains Matryoshka embedding models from a practitioner's perspective and provides a concrete training recipe via the Sentence Transformers library. It frames the same idea as the original MRL paper — embeddings whose earlier dimensions carry more information so the vector can be truncated with minimal quality loss — and explicitly connects it to OpenAI's `text-embedding-3-small`/`text-embedding-3-large` models, which expose a `dimensions` parameter for native, server-side embedding shortening
[[raw/web/matryoshka-embedding-models-huggingface.md]].

## Training Mechanism

Rather than computing a single embedding-similarity loss (e.g., `CoSENTLoss`, `MultipleNegativesRankingLoss`) at the model's full output dimensionality, Matryoshka training computes that same loss repeatedly at several truncated dimensions (e.g., 768, 512, 256, 128, 64) and **sums all of these per-dimension losses into one final loss** that is backpropagated. Sentence Transformers implements this via a `MatryoshkaLoss` wrapper around any base loss, with an optional per-dimension weighting
[[raw/web/matryoshka-embedding-models-huggingface.md]].

## Inference and Practical Tradeoffs

At inference, a Matryoshka-trained Sentence Transformers model accepts a `truncate_dim` argument and automatically slices the output embedding to that size; normalized embeddings must be re-normalized after truncation since slicing changes the vector's norm
[[raw/web/matryoshka-embedding-models-huggingface.md]].

## Key Results

On the STSBenchmark semantic-similarity evaluation, a Matryoshka-trained model retained **98.37% of full-size performance at just 8.3% of the embedding size** (e.g., 64 of 768 dimensions) — illustrating a steep diminishing-returns curve for embedding dimensionality once a model is trained with the Matryoshka multi-granularity objective
[[raw/web/matryoshka-embedding-models-huggingface.md]]. The post frames embedding dimension as a single tunable knob that trades retrieval quality against vector storage size, memory, ANN index size, and search latency — without retraining or maintaining multiple model variants.
