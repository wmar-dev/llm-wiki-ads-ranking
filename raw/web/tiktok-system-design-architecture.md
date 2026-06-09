# TikTok System Design and Recommendation Architecture

**Source:** TechAhead / DEV Community
**URL:** https://dev.to/techahead/how-tiktok-works-decoding-system-design-architecture-with-recommendation-system-ok3
**Type:** Technical blog post
**Date:** September 15, 2024

---

## Architecture Overview

TikTok's architecture is built on three primary components: Big Data Frameworks, Machine Learning, and Microservices.

### Big Data Frameworks
- **Real-time data processing:** Apache Kafka for streaming user interactions
- **Data storage:** Distributed databases for user profiles, videos, engagement metrics

### Machine Learning
- **Deep learning models:** Neural networks analyze video content and user interactions
- **Candidate Generation and Ranking:** Two-stage process — candidate generation selects ~100 relevant videos from hundreds of millions, fine ranking orders them

### Microservices Architecture
- Service mesh for inter-service communication
- Kubernetes for container orchestration

## System Layers
1. Client Layer — mobile apps and web interfaces
2. API Gateway Layer — route requests
3. Application Layer — microservices (User, Content, Feed, Interaction, Search, Analytics, Notification)
4. Data Storage Layer — relational (MySQL/PostgreSQL), NoSQL (Cassandra/MongoDB), in-memory (Redis/Memcached), object storage (S3/GCS)
5. CDN — content delivery worldwide

## Video Processing Pipeline
Upload → object storage → transcoding (multiple formats/resolutions) → feature extraction (AI analyzes objects, scenes, audio) → thumbnail generation → content moderation → indexing

## Recommendation System

### Candidate Generation (Deep Retrieval Model)
Uses a multi-layer perceptron (MLP) with tree-structured output layer. Maps users to items through binary decisions, creating paths through a tree. Each leaf node = set of items. Training uses Expectation-Maximization (EM) algorithm.

### Fine Ranking
With ~100 candidates, more computationally intensive models can be used. Likely employs Transformer/BERT architectures. Multi-objective optimization balancing engagement, creator fairness, platform health.
