# Computationally Feasible VCG Mechanisms

**Source URL:** https://arxiv.org/pdf/1110.0025
**Authors:** Noam Nisan, Amir Ronen
**Venue:** Journal of Artificial Intelligence Research (JAIR), Vol. 29 (2007)
**Source type:** peer_reviewed

---

## Why exact VCG is computationally infeasible

Computing exact VCG payments requires solving the underlying social-welfare
maximization problem (the winner-determination problem). For combinatorial
allocation problems — many items/slots, many bidders, exponentially many possible
allocations — this optimization is NP-hard. Exhaustive evaluation of all
allocations is intractable at any realistic scale.

## Why approximation + VCG payments breaks truthfulness

A natural fix is to replace exact optimization with a fast approximation
algorithm and still apply the standard VCG (Clarke pivot) payment formula. This
breaks incentive-compatibility: because the approximation algorithm may treat a
bidder's declared value differently depending on what is declared (not just
whether it changes the optimal allocation), a bidder can sometimes profit by
misreporting. "VCG-based" mechanisms built on arbitrary approximation algorithms
are therefore generally **not truthful**.

## Maximal-in-Range (MIR) mechanisms

MIR mechanisms restore truthfulness while remaining tractable:

- Fix in advance a restricted "range" — a subset of all possible allocations —
  over which optimization can be done in polynomial time.
- The mechanism always outputs the welfare-maximizing allocation **within that
  restricted range** (never the true global optimum, which may be outside the
  range).
- VCG (Clarke pivot) payments are computed relative to this restricted range, not
  the full allocation space.

Because the mechanism always optimizes exactly over its fixed range — agents
cannot profit by lying, since the mechanism's behavior over the range is itself
exactly optimized — truthfulness (dominant-strategy incentive compatibility) is
preserved. This is, per the paper, essentially the only known general-purpose
technique for building truthful mechanisms in NP-hard multi-parameter
(combinatorial) domains.

## Approximation guarantees and examples

- For combinatorial auctions, restricting the range to allocations reachable by
  fast greedy/local-search algorithms can yield **constant-factor
  approximations** (e.g., 2-approximation) to the true optimal social welfare
  while remaining poly-time.
- For ad/slot allocation specifically, restricting the range to weighted-matching
  allocations (assign each ad to at most one slot, by some fast matching
  heuristic) gives a tractable, truthful mechanism — at the cost of allocative
  efficiency relative to the unrestricted optimum.
- The trade-off is explicit: the narrower/faster the range, the further the MIR
  mechanism's welfare can fall below the true (NP-hard) optimum — there is no
  free lunch between tractability, truthfulness, and optimality.

## Limitations

Subsequent inapproximability results (e.g., "VC v. VCG", arXiv:0905.1995) show
that for general combinatorial auctions, polynomial-time + polynomial-communication
MIR mechanisms cannot achieve arbitrarily tight approximation ratios — there are
provable lower bounds on how close to optimal a tractable, truthful mechanism can
get.
