# Vickrey–Clarke–Groves Mechanism

**Source URL:** https://en.wikipedia.org/wiki/Vickrey%E2%80%93Clarke%E2%80%93Groves_mechanism

**Source type:** other (encyclopedia)

---

## Core Concept and Generalization

The VCG mechanism extends the Vickrey second-price auction to broad social choice
problems. Rather than limiting application to single-item sales, it addresses any
scenario requiring outcome selection from multiple possibilities. The mechanism
generalizes the Vickrey auction into a general-purpose mechanism for social choice
that can allocate multiple items or handle complex combinatorial scenarios.

## How the VCG Mechanism Works

1. **Elicit valuations**: Each participant reports their value for every possible
   outcome.
2. **Select optimal outcome**: The mechanism chooses the allocation maximizing total
   reported values (the utilitarian-efficient outcome).
3. **Base payment**: Each agent receives "credit" equal to other agents' combined
   values for the chosen outcome.
4. **Additional payment**: An arbitrary function of others' valuations (denoted
   h_i) provides flexibility in the final payment rule.

## The Clarke Pivot Rule and Externalities

The Clarke pivot rule is a specific choice of h_i:

    h_i(v_-i) = -max_{x in X} sum_{j != i} v_j(x)

This makes agent i's payment equal to the externality agent i imposes on everyone
else: "others' max total welfare without i" minus "others' total welfare in the
chosen allocation with i present." Intuitively, each agent pays for the marginal
harm their presence causes to the rest of the system.

## Truthfulness and Efficiency

Because each agent's payment depends only on others' reports (not their own),
misreporting cannot change an agent's payment in a way that benefits them relative
to truthful reporting — truth-telling is a dominant strategy. The resulting
allocation maximizes aggregate (utilitarian) value across all participants —
allocative efficiency.

In a single-item auction, VCG reduces exactly to the Vickrey (second-price)
auction: the highest bidder wins and pays the second-highest bid.

## Notable Weaknesses and Limitations

- **Budget-balance problems**: VCG mechanisms often run a deficit — total payments
  collected can be less than the cost of the chosen outcome (e.g., public-goods
  provision), or in double auctions may require an external subsidy.
- **Computational complexity**: in combinatorial auctions, computing the
  welfare-maximizing allocation is NP-hard, which limits practical deployment at
  scale.
- **Collusion vulnerability**: coordinated misreporting by a coalition of bidders
  can subvert the mechanism's truthfulness guarantees.
- **Non-participation / default risk**: the mechanism assumes participants will pay
  their computed bids, which can fail in practice.
