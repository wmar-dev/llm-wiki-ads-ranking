# Network interference in A/B testing

Source: https://arxiv.org/abs/2411.19789

## Summary

Network interference occurs when one unit's treatment affects another's outcome, violating SUTVA. Several approaches exist:

1. **Cluster-randomized design**: Randomize over clusters rather than individuals to contain spillover within clusters. Used at Facebook/Meta (Guber et al., KDD 2023).
2. **Exposure modeling**: Define exposure conditions based on neighborhood treatment and use IPW estimators (Aronow & Samii, Ann. Appl. Stat. 2017).
3. **Regression adjustment**: Adjust for network covariates to reduce bias and variance (Han & Ugander, J. Causal Inference 2023).
4. **Causal message-passing**: Dynamic framework for multi-period experiments under unknown interference (Shirani & Bayati, PNAS 2024).
5. **Staggered rollout**: Merge data from experiments with varying treatment proportions to identify global treatment effects (Cortez et al., NeurIPS 2022).

No universal solution exists — the best approach depends on network structure, whether the interference structure is known, and available data.
