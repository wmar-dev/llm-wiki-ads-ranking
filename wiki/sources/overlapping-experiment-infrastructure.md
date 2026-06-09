---
title: "Overlapping Experiment Infrastructure: More, Better, Faster Experimentation"
source: "raw/pdf/overlapping-experiment-infrastructure.pdf"
source_url: "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36500.pdf"
source_type: "pdf"
ingested_at: "2026-06-08"
---

**Authors**: Diane Tang, Ashish Agarwal, Deirdre O'Brien, Mike Meyer (Google, Inc.)
**Venue**: KDD 2010, July 25–28, Washington, DC

## Overview

This paper describes Google's overlapping experiment infrastructure — a layered A/B testing system designed to support running many experiments simultaneously across web search, ads, and UI without experiments interfering with each other. The system addresses three design goals: **more** (scalability), **better** (validity and consistency), and **faster** (speed of setup and analysis).

The core problem with naive A/B testing at scale is that a single experiment layer means every query is in at most one experiment — insufficient throughput for a data-driven company running thousands of concurrent tests. Full multi-factorial design is infeasible because not all parameters are independent (e.g., pink text on a pink background is unreadable). The solution is to partition parameters into subsets, each subset associated with a **layer**, with traffic diversion across layers being orthogonal. Each query can simultaneously be in N experiments, one per layer.

## Infrastructure Design

### Key Concepts

Three core abstractions govern the system:

- **Domain**: a segmentation of traffic. Domains can be nested within layers.
- **Layer**: corresponds to a subset of system parameters. Experiments in different layers modify disjoint parameter sets.
- **Experiment**: a segmentation of traffic paired with alternate parameter values; traffic not in the experiment sees default values.

Parameters from different binaries (web server, organic results server, ads results server) naturally belong in different layers. Parameters within a single binary can be further partitioned based on which ones must vary together.

### Traffic Diversion

Four diversion types are supported, evaluated in priority order so each query is assigned at most once per layer:

1. **User-id mod**: uses signed-in user ID; strongest consistency across sessions
2. **Cookie mod**: `f(cookie, layer) % 1000` — layer ID is incorporated into the hash to ensure orthogonality across layers
3. **Cookie-day mod**: `f(cookie, day) % 1000` — set of cookies in an experiment rotates daily, useful for detecting learning effects
4. **Random traffic**: per-request random number; least consistent but simplest

**Conditions** further restrict which events within a diverted slice are assigned to an experiment (e.g., Japan-only, English-only, specific datacenter). Conditions enable sharing of cookie mods across experiments that target non-overlapping audiences.

### Launch Layers

**Launch layers** are distinct from experiment layers and are used for gradual production rollouts:

- They run over all traffic (always in the default domain)
- They provide an *alternative default value* for parameters, not an override
- If an experiment layer experiment overrides the same parameter, the experiment layer takes precedence
- They are created per launched feature and deleted once fully rolled out

This design enables gradually ramping a change to 100% of traffic without disturbing existing experiments, and enables detection of interactions between launched features.

## Tools and Processes

### Automated Data File Checks

Experiments are configured in human-readable data files (not code), enabling non-engineers to create experiments. Automated pre-submit checks enforce: syntax validity, ID uniqueness, correct layer assignment for the parameters used, traffic availability, and presence of a matching control.

### Real-time Monitoring

Key metrics (e.g., CTR) are computed in near-real-time. Experimenters set expected metric ranges; automated alerts fire if metrics fall outside bounds. This allows aggressive experimentation — mistakes are caught quickly before causing significant harm.

### Experiment Sizing

Effective experiment size is: `N = (1/queries_control + 1/queries_experiment)^{-1}`

With a large shared control per layer (shared across multiple experiments), the per-experiment traffic requirement drops from `2N` to `N`, and statistical power increases from 80% to 90%. Required size: `queries_experiment ≥ 10.5 * (s/θ)^2` where `s` is standard error per experimental unit and `θ` is the minimum detectable effect.

For ratio metrics (e.g., coverage = queries with ads / total queries), the **delta method** is used to compute `s` properly — cookie-mod experiments must account for correlation across queries from the same user. The key finding: cookie-mod experiments require substantially more traffic than random-traffic experiments to detect the same effect size.

A **sizing tool** allows experimenters to specify desired metrics, minimum detectable change, diversion type, and traffic conditions, then returns the required experiment size. Continuously running **uniformity trials** (A vs. A tests) calibrate the sizing tool's variance estimates.

### Triggering and Counter-factuals

An experiment may be **diverted** to a set of traffic but only **triggered** (actually changing behavior) on a subset. The control must log the **counter-factual** — when the experiment would have triggered but didn't. Restricting analysis to the trigger set removes dilution from unchanged requests, improving power and reducing required traffic (`1/θ^2` scaling means focusing on the triggered subset matters significantly).

### Pre- and Post-periods

- **Pre-period**: the same cookie mods are diverted but serving is not changed; used to verify traffic is unbiased (not contaminated by spam or robot traffic)
- **Post-period**: same traffic after the experiment ends; used to detect learned user behavior effects

### Analysis Tool

A single canonical analysis tool provides: consistent metric definitions and spam filters across teams, correctly-computed confidence intervals (delta method or empirical carve-up method), sparkline visualizations, support for slicing to detect Simpson's paradox (mix shifts masking real metric changes), and extensibility for custom metrics.

### Educational Processes

**Experiment Council**: engineers review a lightweight checklist covering hypotheses, parameters, diversion, analysis plan, sizing, and design. Eliminates misconfigured experiments and serves as a knowledge-transfer mechanism.

**Interpretation Forum**: open forum where experimenters present results to experts. Goals: validate the results, ensure metrics are complete, and reach a decision on whether to launch. Open attendance allows future experimenters to learn in advance.

## Results (2007–2010)

Deployed in March 2007. By 2010, Google had achieved approximately **an order of magnitude more** concurrent experiments, more product launches, and more unique experimenters — all with fewer errors. Qualitative improvements: fewer misconfigured experiments, fewer debates about metric definitions (single canonical tool resolves this), and better anomaly detection through pre-periods. The slowest remaining phase is feature implementation itself; experiment configuration, push, and analysis are now fast relative to development.

## Significance for Ads Ranking

The paper is foundational for understanding how large-scale ads systems evolve incrementally. The layered infrastructure directly addresses ads-specific constraints: the ads results server has its own layer(s), preventing experiment starvation by upstream binaries. The CTR prediction algorithm is explicitly cited as a parameter type (learning rate, shrinkage rate) that benefits from this infrastructure. Triggering and counter-factual logging are particularly important for ads experiments, where changes may only affect a subset of queries (e.g., only queries where ads are shown), and dilution-free analysis is essential for accurate measurement.
