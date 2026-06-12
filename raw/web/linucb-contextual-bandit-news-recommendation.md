# A Contextual-Bandit Approach to Personalized News Article Recommendation

**Authors:** Lihong Li, Wei Chu, John Langford, Robert E. Schapire (Yahoo! Labs / Princeton) — WWW 2010. arXiv:1003.0146.

Source URL: https://arxiv.org/abs/1003.0146

## Abstract / Problem

Personalized recommendation of news articles is modeled as a **contextual
bandit problem**: a learning algorithm sequentially selects articles to serve
users based on contextual information about the user and the articles, while
adapting its article-selection strategy based on user-click feedback to
maximize total clicks. The paper proposes **LinUCB**, a new contextual bandit
algorithm, and an **offline evaluation method** for reliably evaluating bandit
algorithms on logged, randomized data.

## Contextual Bandit Formulation

At each trial t = 1, 2, 3, ...:

1. The algorithm observes the current user u_t and a set of arms (articles)
   A_t together with their feature vectors x_{t,a} for a in A_t. The vector
   x_{t,a} (the **context**) summarizes information about both the user u_t
   and the arm a.
2. Based on observed payoffs from previous trials, the algorithm chooses an
   arm a_t in A_t and receives payoff r_{t,a_t} whose expectation depends on
   both the user u_t and the chosen arm a_t. Crucially, no feedback is
   observed for unchosen arms.
3. The algorithm improves its arm-selection strategy using the new
   observation (x_{t,a_t}, a_t, r_{t,a_t}).

The **payoff of an article** is 1 if it is clicked and 0 otherwise, so the
expected payoff of an article is exactly its **click-through rate (CTR)** —
maximizing expected payoff is equivalent to maximizing CTR / total clicks.

**Regret**: the T-trial regret R_A(T) of algorithm A is the difference
between the expected total payoff of an oracle that always picks the arm with
maximum expected payoff, and the expected total payoff actually achieved by A.

## LinUCB with Disjoint Linear Models (Algorithm 1)

**Linear payoff assumption**: for all t, the expected payoff of arm a given
context x_{t,a} is linear in the context's d-dimensional feature vector, with
an unknown per-arm coefficient vector theta_a*:

  E[r_{t,a} | x_{t,a}] = x_{t,a}^T theta_a*

This model is called **disjoint** because the parameter vectors theta_a are
not shared across arms.

**Ridge regression estimate.** Let D_a be the m x d design matrix whose rows
are the m training contexts observed so far for arm a, and c_a in R^m the
corresponding observed click/no-click rewards. Ridge regression on (D_a, c_a)
gives:

  theta_hat_a = (D_a^T D_a + I_d)^{-1} D_a^T c_a       (Eq. 3)

where I_d is the d x d identity matrix.

**Confidence bound.** If components of c_a are conditionally independent
given the corresponding rows of D_a, then with probability at least 1 - delta,
for any delta > 0 and any x_{t,a}:

  | x_{t,a}^T theta_hat_a - E[r_{t,a} | x_{t,a}] |
      <= alpha * sqrt( x_{t,a}^T (D_a^T D_a + I_d)^{-1} x_{t,a} )    (Eq. 4)

where alpha = 1 + sqrt( ln(2/delta) / 2 ) is a constant. This gives a
reasonably tight **upper confidence bound (UCB)** on the expected payoff of
arm a.

**Arm selection rule.** At each trial t, LinUCB chooses:

  a_t = argmax_{a in A_t} ( x_{t,a}^T theta_hat_a
                            + alpha * sqrt( x_{t,a}^T A_a^{-1} x_{t,a} ) )   (Eq. 5)

where A_a := D_a^T D_a + I_d. The first term is the **predicted payoff**
(exploitation); the second term is the **confidence-interval width**
(exploration bonus) — it is large when arm a has been tried on few contexts
similar to x_{t,a}, and shrinks as more data accumulates for that region of
context space. alpha is the algorithm's only tunable parameter, controlling
the exploration/exploitation trade-off.

**Bayesian interpretation.** Eq. 3's ridge-regression solution can also be
read as the posterior mean of a Gaussian posterior p(theta_a) with mean
theta_hat_a and covariance A_a^{-1} (assuming a Gaussian prior and Gaussian
noise). The predictive variance of the expected payoff x_{t,a}^T theta_a at
context x_{t,a} is x_{t,a}^T A_a^{-1} x_{t,a}, and its square root is the
standard deviation that appears in Eq. 5. The reduction in posterior entropy
from observing x_{t,a} is (1/2) * ln(1 + x_{t,a}^T A_a^{-1} x_{t,a}) — so the
UCB arm-selection criterion can also be read as an additive trade-off between
predicted payoff and expected model-uncertainty reduction.

**Algorithm 1 (LinUCB, disjoint linear models) pseudocode:**

```
Inputs: alpha in R+
for t = 1, 2, 3, ..., T do
    Observe features of all arms a in A_t: x_{t,a} in R^d
    for all a in A_t do
        if a is new then
            A_a <- I_d                 (d x d identity matrix)
            b_a <- 0_{d x 1}
        end if
        theta_hat_a <- A_a^{-1} b_a
        p_{t,a} <- theta_hat_a^T x_{t,a} + alpha * sqrt(x_{t,a}^T A_a^{-1} x_{t,a})
    end for
    Choose arm a_t = argmax_{a in A_t} p_{t,a} (ties broken arbitrarily),
        and observe a real-valued payoff r_t
    A_{a_t} <- A_{a_t} + x_{t,a_t} x_{t,a_t}^T
    b_{a_t} <- b_{a_t} + r_t * x_{t,a_t}
end for
```

**Complexity & practical properties:**
- Computational complexity is linear in the number of arms and at most cubic
  in the number of features (matrix inverse).
- A_{a_t} can be updated incrementally in O(d^2) per step; A_a^{-1} can be
  cached and recomputed periodically instead of every trial.
- The algorithm works for a **dynamic arm set** A_t (arms can be added/removed
  over time, as in news article pools) as long as |A_t| is not too large.
- Theoretical regret bound: O~(sqrt(K d T)) when the arm set is fixed with K
  arms, matching the state-of-the-art regret bound for bandits satisfying the
  linear payoff assumption.

## LinUCB with Hybrid Linear Models (Algorithm 2)

In many applications, some features are **shared across all arms** (e.g., a
user's general preference for "politics" articles, independent of which
specific political article is shown) while others are **arm-specific**. The
hybrid model adds a shared term to the payoff model:

  E[r_{t,a} | x_{t,a}] = z_{t,a}^T beta* + x_{t,a}^T theta_a*       (Eq. 6)

where z_{t,a} in R^k is the shared user/article-interaction feature and beta*
is an unknown coefficient vector **common to all arms**, while theta_a*
remains arm-specific.

Because the shared coefficient beta* couples all arms together, the
disjoint-model algorithm can no longer be used directly — the confidence
intervals of different arms are not independent. The paper derives an
efficient UCB via **block matrix inversion** (Algorithm 2), maintaining global
accumulators A_0, b_0 (for beta) alongside the per-arm A_a, B_a, b_a. The
per-trial cost stays bounded because all building blocks have fixed
dimensions and can be updated incrementally; inverses (A_0^{-1}, A_a^{-1}) can
be cached and refreshed periodically rather than every trial, reducing
amortized cost to O(d^2 + k^2).

## Offline Evaluation Method

Evaluating a bandit policy normally requires live interaction (the policy's
choices affect what feedback it receives). The paper proposes a provably
unbiased **offline policy evaluator**: given a stream of logged events
collected under a **uniformly random logging policy** (each arm chosen
uniformly at random, independent of context), replay the log and, for each
event, only "retain" it (add to the policy's history and total payoff) if the
policy under evaluation *would have chosen the same arm* as the logging
policy did; otherwise discard the event entirely. Theorem 1 proves this
produces a stream of retained events whose distribution is identical to what
the policy would experience by interacting with the real world, requiring
K times T logged events in expectation to evaluate T real interactions with
a K-armed bandit.

## Experiments — Yahoo! Front Page "Today Module"

- **Dataset**: ~4.7M events on May 1, 2009 for model tuning, ~36M events from
  May 3-9, 2009 for evaluation, collected from the "Featured" tab story
  position (F1) of the Yahoo! Front Page Today Module.
- **Features**: user features reduced via logistic-regression-based
  dimensionality reduction + k-means into a 6-dimensional "user group"
  feature (5 cluster memberships + constant 1); article features are an
  83-dimensional categorical vector (URL categories + editor categories,
  binary-encoded, unit-normalized, plus a constant feature). Disjoint LinUCB
  uses the 6-dimensional user feature x_{t,a} per article (separate theta_a
  per article); hybrid LinUCB additionally uses a 36-dimensional shared
  user-article interaction feature z_{t,a} (6 x 6 outer product of user and
  article group features).
- **Compared algorithms**: context-free random and epsilon-greedy baselines,
  context-free UCB1, epoch-greedy, EXP3-style algorithms, and LinUCB
  (disjoint and hybrid).
- **Headline result**: LinUCB achieves a **12.5% click lift (CTR
  improvement)** compared to a standard context-free bandit algorithm on the
  Yahoo! Today Module data, and the advantage **becomes even greater when data
  is more scarce** (i.e., LinUCB's contextual generalization helps most when
  little data is available per arm/article).

## Significance

LinUCB is one of the most widely cited contextual-bandit algorithms: it
combines (1) a closed-form, efficiently-updatable confidence bound derived
from ridge regression, (2) a single tunable parameter (alpha), (3) support
for dynamic arm sets, and (4) a provably unbiased offline evaluation
methodology that made bandit research on logged production data practical.
It is the canonical "contextual bandit" referenced when ad systems describe
per-impression personalized exploration (e.g., creative selection, budget
allocation).
