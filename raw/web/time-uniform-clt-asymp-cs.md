# Time-uniform central limit theory and asymptotic confidence sequences

Source: https://arxiv.org/abs/2103.06476

Authors: Ian Waudby-Smith, David Arbour, Ritwik Sinha, Edward H. Kennedy, Aaditya Ramdas
Venue: Annals of Statistics, 52(6), 2613–2640 (2024)
DOI: 10.1214/24-AOS2408

## Summary

This paper introduces "asymptotic confidence sequences" (AsympCS) — time-uniform analogues of CLT-based confidence intervals that provide valid inference at arbitrary stopping times without penalizing "peeking" at the data. AsympCSs forgo nonasymptotic validity for CLT-like versatility and asymptotic time-uniform guarantees.

## Key findings

- AsympCSs achieve the optimal asymptotic width of O(√(log log n / n)) per the law of the iterated logarithm (LIL).
- The Gaussian mixture boundary is tighter at moderate sample sizes, though the LIL-optimal boundary eventually outperforms it.
- Nonasymptotic CSs (Howard et al., 2021) stay within a factor of ~2 of fixed-sample CLT bounds over five orders of magnitude in time.
- AsympCSs extend naturally to causal inference (ATE estimation) in both randomized experiments and observational studies.
- The width penalty for anytime validity is bounded: approximately 2× width, or equivalently 2–7× sample size depending on construction.

## References

- Howard, S.R., Ramdas, A., McAuliffe, J., Sekhon, J. (2021). "Time-uniform, nonparametric, nonasymptotic confidence sequences." Annals of Statistics, 49(2), 1055–1080.
- Waudby-Smith, I. et al. (2024). "Time-uniform central limit theory and asymptotic confidence sequences." Annals of Statistics, 52(6), 2613–2640.
- Johari, R. et al. (2022). "Always valid inference: Continuous monitoring of A/B tests." Operations Research, 70(3), 1800–1817.
