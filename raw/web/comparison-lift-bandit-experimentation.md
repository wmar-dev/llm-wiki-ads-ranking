# Comparison Lift: Bandit-Based Experimentation System for Online Advertising

**Source:** arXiv:2009.07899 — "Comparison Lift: Bandit-based Experimentation System for Online Advertising"
**URL:** https://arxiv.org/abs/2009.07899
**Date:** September 2020

## Summary (fetched)

Traditional fixed-sample A/B testing for online advertising (testing audiences,
creatives, etc.) is costly: a fixed fraction of traffic must be allocated to
under-performing variants for the duration of the test, wasting ad spend and
delaying decisions.

**Comparison Lift** is an experimentation-as-a-service (EaaS) platform deployed
at JD.com that replaces fixed-sample A/B allocation with an adaptive
multi-armed-bandit algorithm. Rather than splitting traffic evenly across
variants for a fixed duration, the bandit dynamically reallocates traffic
toward better-performing variants as evidence accumulates.

## Claimed Advantages over Fixed A/B Testing

1. **Goal alignment** — "It aligns the randomization induced in the test with
   the advertiser's goals from testing," i.e., the test itself spends less
   budget on the variants the advertiser cares least about.
2. **Cost reduction** — adaptive allocation reduces the amount of ad spend
   "wasted" on inferior variants during the experiment itself.

## Production Results

Deployed since May 2019:

- **1,500+ experiments** run across advertising campaigns on the platform
- **46% average increase in CTR** for campaigns that participated, relative to
  baseline
- **27% additional clicks generated during the testing period itself**,
  compared to what a traditional fixed-sample A/B design would have produced

## Notes

- This is a direct example of multi-armed bandits used as an *alternative to
  A/B testing* for online advertising — relevant to the wiki's existing
  coverage of A/B testing methodology and confidence-sequence methods.
