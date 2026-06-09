# How TikTok's Algorithm Really Works: A Deep Dive Into the Unsupervised Learning Engine Behind the For You Page

**Source:** Kingy AI (curtis Pyke)
**URL:** https://kingy.ai/uncategorized/how-tiktoks-algorithm-really-works-a-deep-dive-into-the-unsupervised-learning-engine-behind-the-for-you-page/
**Type:** Technical blog post
**Date:** May 18, 2026

---

## Core Thesis

TikTok's For You Page (FYP) is powered primarily by unsupervised and self-supervised machine learning. The system does not define categories and match users to them — it lets data organize itself by clustering videos that behave alike, clustering users who swipe alike, and drawing connections between the two without ever being told what those connections mean.

## Video Ingestion Pipeline

When a video is uploaded, three parallel pipelines extract raw signal:
1. **Computer vision** reads frames (faces, objects, scenes, motion, colors) via deep learning
2. **Natural language processing** reads audio (transcription) and on-screen text/captions
3. **Metadata** from creator side: hashtags, sound, effects, creator historical fingerprint

All pipelines output numerical feature vectors — no human-readable labels.

## Clustering

Videos are clustered using techniques including K-means (coarse buckets), hierarchical clustering (nested niches), DBSCAN (density-based), and Gaussian Mixture Models (soft memberships). **Clusters are not given human-readable names** — cluster 4,281 is just cluster 4,281.

## User Modeling

Users become vectors from millions of micro-signals: likes, comments, shares, completions, re-watches, but most importantly implicit signals — how long you paused, whether you scrolled away in the first second, whether you muted, whether you swiped back. Implicit signals are 10-100x more dense than explicit feedback.

**Cold start:** First feed seeded from device type, language, country, IP geography, and optional category selection at sign-up. Every swipe sharpens the estimate.

## Embeddings (The Representation Revolution)

Modern approach uses dense numerical vectors (16-1,024 dimensions) in continuous space. Trained via:
- **Autoencoders** — compress and reconstruct to discover compact representations
- **Contrastive learning** — pull similar items together, push unrelated apart
- **Two-tower models** — separate neural nets for user and video embeddings trained jointly

## Monolith (ByteDance's System)

Published in arXiv 2022 (https://arxiv.org/abs/2209.07663). Key features:
- **Collisionless embedding tables** using Cuckoo HashMap — each ID has its own slot
- **Online training** — Parameter Server updates weights from live user event stream
- **Expirable embeddings** — dormant users/items have embeddings retired
- Real-time training with 30-minute sync cycles outperformed batch training on every metric

## Collaborative Filtering

Two flavors: user-user CF and item-item CF. TikTok's advantage is structural — short videos mean 10-100x more engagement events per session than YouTube or Netflix, filling the co-engagement matrix faster.

## Self-Supervised Learning

Used in three key areas:
1. **Video representation** — predict next frame or masked patches
2. **Language** — BERT-based models for caption/comment analysis
3. **Behavior sequences** — treat watch history as sequence, train to predict next video (same objective as LLMs)

## Two-Stage Architecture

**Stage 1: Candidate Generation** — billions → thousands. Uses approximate nearest-neighbor search in embedding space, item-item CF, cluster lookups, trending pool.

**Stage 2: Ranking** — supervised multi-task deep model predicts: probability of like, completion, share, comment, watch-time. Combined into single score. Diversity and safety filters applied last.

**Exploration:** ~30-50% of videos exploit user interests; the rest are exploration. Dual purpose: prevents filter bubbles AND feeds unsupervised learning with new taste connections.

## Case Study: First 50 Swipes

A new user's embedding shifts dramatically within 50 swipes based on implicit watch-time signals — without any explicit follows, likes, or comments. By swipe 50, their feed is highly personalized based on fine-grained behavioral patterns.

## Regulatory Concerns

- Rabbit holes: optimization for watch-time leads to problematic content patterns
- Opacity: no cluster has a name; no one can answer "why did this user see this video?" precisely
- Bad actors can reverse-engineer the cluster map
- EU Digital Services Act requires non-personalized feed option and auditability
