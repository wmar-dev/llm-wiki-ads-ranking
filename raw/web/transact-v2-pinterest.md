# TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation

Source: https://arxiv.org/abs/2506.02267 (arXiv:2506.02267)

**Authors:** Xue Xia, Saurabh Vishwas Joshi, Kousik Rajesh, Kangnan Li, Yangyi Lu, Nikil Pancha, Dhruvil Deven Badani, Jiajing Xu, Pong Eksombatchai (Pinterest)
**Submitted:** June 2, 2025

## Abstract

Modeling user action sequences has become a popular focus in industrial recommendation system research, particularly for Click-Through Rate (CTR) prediction tasks. However, industry-scale CTR models often rely on short user sequences, limiting their ability to capture long-term behavior. Additionally, these models typically lack an integrated action-prediction task within a point-wise ranking framework, reducing their predictive power. They also rarely address the infrastructure challenges involved in efficiently serving large-scale sequential models. In this paper, we introduce TransAct V2, a production model for Pinterest's Homefeed ranking system, featuring three key innovations: (1) leveraging very long user sequences to improve CTR predictions, (2) integrating a Next Action Loss function for enhanced user action forecasting, and (3) employing scalable, low-latency deployment solutions tailored to handle the computational demands of extended user action sequences.

## Key Findings

- **Lifelong sequences**: TransActV2 scales user action sequences to up to ~16,000 actions — a ~160x increase over the prior TransAct (real-time, RT-only) sequences — covering years of explicit user actions (repins, clicks, hides), excluding mere impressions.
- **Next Action Loss (NAL)**: An auxiliary multi-task objective that forecasts the user's next action, integrated into the point-wise ranking framework alongside the primary CTR objective.
- **Offline results** (RT + Lifelong-sequence + NAL vs. RT-only baseline): **+13.31% HIT@3/repin**, **−11.25% HIT@3/hide**.
- **Online A/B test results** (vs. RT-only TransAct baseline): **+6.35% Homefeed Repin Volume**, **−12.80% Homefeed Hide Volume**, **+0.45% Impression Diversity**, **+1.41% Time Spent on App**.
- **Infrastructure**: scalable, low-latency serving solutions specifically engineered to handle the computational cost of scoring 16K-action sequences in real time for Pinterest's Homefeed ranking.

## Relationship to PinFM

TransActV2 is a **production ranking model** for Pinterest's Homefeed, evaluated via offline HIT@k metrics and online A/B tests on engagement (repins, hides, diversity, time spent). PinFM (arXiv:2507.12704, RecSys 2025) is a **20B+ parameter pretrained foundation model** for user activity sequences, fine-tuned per-surface and evaluated primarily via engagement-with-new-items and serving-throughput metrics (DCAT). Neither paper benchmarks against the other on a shared task or metric — they were developed in parallel as complementary pieces of Pinterest's recommendation stack rather than as competing solutions to the same problem [[raw/web/transact-v2-pinterest.md]].
