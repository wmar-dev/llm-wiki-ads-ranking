---
title: "What Does Code for a Simple Ads Auction System Look Like in Python?"
type: "synthesis"
sources:
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/google-ad-rank-briefing-paper.md"
status: "current"
created: "2026-06-12"
last_updated: "2026-06-12"
---

# What Does Code for a Simple Ads Auction System Look Like in Python?

The wiki's auction pages describe the *rules* of ad auctions — ranking by
`bid x quality`, second-price payment, Ad Rank's LTV formula. This page makes
those rules concrete with small, runnable Python implementations, building up
from the simplest case (a single item, second-price) to the realistic
multi-slot case used by search ads.

## 1. The Simplest Case: Single-Item Second-Price (Vickrey) Auction

[[wiki/synthesis/second-price-auction.md]] describes the Vickrey auction: the
highest bidder wins, but pays the *second-highest* bid. This is the
foundation everything else builds on.

```python
from dataclasses import dataclass


@dataclass
class Bid:
    bidder: str
    amount: float


def run_vickrey_auction(bids: list[Bid]) -> dict:
    """Single-item second-price auction: highest bidder wins,
    pays the second-highest bid."""
    ranked = sorted(bids, key=lambda b: b.amount, reverse=True)
    winner = ranked[0]
    price = ranked[1].amount if len(ranked) > 1 else 0.0
    return {"winner": winner.bidder, "price": price}


bids = [Bid("Acme", 5.00), Bid("Globex", 3.50), Bid("Initech", 4.20)]
print(run_vickrey_auction(bids))
# {'winner': 'Acme', 'price': 4.2}
```

Acme wins (highest bid, $5.00) but only pays $4.20 — Initech's bid, the
second-highest. This single property makes truthful bidding a dominant
strategy [[wiki/synthesis/second-price-auction.md]].

## 2. The Realistic Case: Multi-Slot GSP Ad Auction

Real ad auctions allocate *multiple* slots (search results page positions) and
rank by **`bid x quality`**, not bid alone — a low-quality high bidder can lose
to a high-quality lower bidder
[[wiki/concepts/generalized-second-price-auction.md]]. The Generalized
Second-Price (GSP) auction generalizes Vickrey's "pay second price" rule to
"pay the minimum price needed to keep your slot":

```python
@dataclass
class AdBid:
    advertiser: str
    bid_cpc: float   # max price per click the advertiser will pay
    quality: float   # quality score, e.g. predicted CTR

    @property
    def score(self) -> float:
        """GSP ranking signal: bid x quality."""
        return self.bid_cpc * self.quality


def run_gsp_auction(bids: list[AdBid], num_slots: int) -> list[dict]:
    """Generalized Second-Price auction.

    Slots are awarded in order of score = bid x quality. The winner of
    slot k pays the minimum CPC needed to keep score above the
    next-ranked competitor: price_k = next_score / own_quality.
    """
    ranked = sorted(bids, key=lambda b: b.score, reverse=True)
    results = []
    for i, winner in enumerate(ranked[:num_slots]):
        next_score = ranked[i + 1].score if i + 1 < len(ranked) else 0.0
        price_cpc = next_score / winner.quality if winner.quality > 0 else 0.0
        results.append({
            "slot": i + 1,
            "advertiser": winner.advertiser,
            "score": round(winner.score, 4),
            "price_cpc": round(price_cpc, 4),
        })
    return results


bids = [
    AdBid("Acme", bid_cpc=2.00, quality=0.05),
    AdBid("Globex", bid_cpc=1.50, quality=0.08),
    AdBid("Initech", bid_cpc=3.00, quality=0.02),
]
for row in run_gsp_auction(bids, num_slots=2):
    print(row)
# {'slot': 1, 'advertiser': 'Globex', 'score': 0.12, 'price_cpc': 1.25}
# {'slot': 2, 'advertiser': 'Acme', 'score': 0.1, 'price_cpc': 1.2}
```

Note the ranking flip: Initech has the highest raw bid ($3.00) but the lowest
quality (0.02), so its score (0.06) ranks *last* — it wins no slot at all.
Globex's combination of a moderate bid and high quality wins the top slot, and
pays $1.25/click — just enough to outscore Acme (the next-ranked bidder),
not its full $1.50 bid
[[wiki/concepts/generalized-second-price-auction.md]].

![simple-ads-auction-python-diagram-1](/assets/simple-ads-auction-python-diagram-1.svg)

## 3. Extending to Ad Rank: LTV-Based Eligibility and Pricing

Google's production system replaces the simple `quality` term with a full
**LTV (Long-Term Value)** score: `LTV = eCPM - (impression_cost +
click_cost)`, where `eCPM = bid x pCTR`, and the cost terms are functions of
predicted creative quality (pCQ) and landing page quality (pLQ). Only bids
with `LTV > 0` are eligible to show at all
[[wiki/synthesis/what-is-ad-rank.md]].

```python
@dataclass
class AdRankBid:
    advertiser: str
    bid_cpc: float    # max CPC the advertiser will pay
    pctr: float       # predicted click-through rate
    pcq: float        # predicted creative quality, in [0, 1]
    plq: float        # predicted landing page quality, in [0, 1]
    cost_per_unit: float = 0.05  # converts (1 - quality) into eCPM-like units

    @property
    def ecpm(self) -> float:
        return self.bid_cpc * self.pctr

    @property
    def ltv(self) -> float:
        """LTV = eCPM - (impression_cost + click_cost)."""
        impression_cost = self.cost_per_unit * (1 - self.pcq)
        click_cost = self.cost_per_unit * (1 - self.plq)
        return self.ecpm - impression_cost - click_cost


def run_ad_rank_auction(bids: list[AdRankBid], num_slots: int) -> list[dict]:
    """Rank by LTV; bids with LTV <= 0 are ineligible (Ad Rank style)."""
    eligible = [b for b in bids if b.ltv > 0]
    ranked = sorted(eligible, key=lambda b: b.ltv, reverse=True)
    results = []
    for i, winner in enumerate(ranked[:num_slots]):
        next_ltv = ranked[i + 1].ltv if i + 1 < len(ranked) else 0.0
        impression_cost = winner.cost_per_unit * (1 - winner.pcq)
        click_cost = winner.cost_per_unit * (1 - winner.plq)
        # Second price in LTV-space: the eCPM that would push this
        # winner's LTV down to the next bidder's LTV.
        ecpm_at_price = next_ltv + impression_cost + click_cost
        price_cpc = max(ecpm_at_price, 0.0) / winner.pctr if winner.pctr > 0 else 0.0
        results.append({
            "slot": i + 1,
            "advertiser": winner.advertiser,
            "ltv": round(winner.ltv, 4),
            "price_cpc": round(price_cpc, 4),
        })
    return results


bids = [
    AdRankBid("Acme", bid_cpc=2.00, pctr=0.05, pcq=0.9, plq=0.8),
    AdRankBid("Globex", bid_cpc=1.50, pctr=0.08, pcq=0.6, plq=0.5),
    AdRankBid("Initech", bid_cpc=0.50, pctr=0.02, pcq=0.95, plq=0.95),
]
for row in run_ad_rank_auction(bids, num_slots=2):
    print(row)
# {'slot': 1, 'advertiser': 'Acme', 'ltv': 0.085, 'price_cpc': 1.8}
# {'slot': 2, 'advertiser': 'Globex', 'ltv': 0.075, 'price_cpc': 0.625}
```

Here Acme overtakes Globex despite a lower `bid x pCTR` score (0.10 vs. 0.12),
because its much higher creative/landing-page quality (0.9/0.8 vs. 0.6/0.5)
reduces its cost terms enough to win on LTV. Initech is filtered out entirely
— its LTV would be negative at `cost_per_unit=0.05`, so it never enters the
ranking, matching the `LTV > 0` eligibility rule
[[wiki/synthesis/what-is-ad-rank.md]].

*Inference: the `cost_per_unit` constant above is a stand-in for the real
cost functions `f(1-pCQ)` and `f(1-pLQ)`. The wiki does not specify what `f()`
actually is in production — this is the open question already noted in
[[wiki/synthesis/what-is-ad-rank.md]]. The code uses a simple linear function
purely to illustrate how the eligibility and pricing *logic* works once such a
function exists; it is not a claim about the real `f()`.*

## Comparing the Three Auctions

| | Single-item Vickrey | Multi-slot GSP | Ad Rank (LTV) |
|---|---|---|---|
| Ranking signal | bid alone | `bid x quality` | `LTV = bid x pCTR - costs(pCQ, pLQ)` |
| Eligibility filter | none | none (any positive score) | `LTV > 0` |
| Payment rule | pay 2nd-highest bid | pay min. CPC to hold rank: `next_score / own_quality` | pay min. CPC for `LTV == next_LTV` |
| Source | [[wiki/synthesis/second-price-auction.md]] | [[wiki/concepts/generalized-second-price-auction.md]] | [[wiki/synthesis/what-is-ad-rank.md]] |

Each step is a strict generalization of the one before it: GSP with
`quality = 1` for everyone reduces to ranking by bid alone (close to Vickrey
for a single slot), and Ad Rank with `pcq = plq = 1` for everyone (zero cost
terms) reduces to plain GSP's `bid x pCTR` ranking. Production systems also
layer in **rGSP** — randomizing the winner among near-tied LTVs and pricing at
the next-highest bid plus a small increment
[[wiki/synthesis/what-is-ad-rank.md]] — which is a small modification to the
ranking step above (sample from the top-`k` near-ties instead of always
picking the single highest).

## Related Pages

- [[wiki/synthesis/second-price-auction.md]] — Vickrey auction mechanics and incentive compatibility
- [[wiki/concepts/generalized-second-price-auction.md]] — GSP ranking and pricing rules
- [[wiki/synthesis/what-is-ad-rank.md]] — full LTV formula, eligibility, rGSP, and Meta's Total Value comparison
- [[wiki/synthesis/what-is-vcg.md]] — VCG mechanism (the truthful alternative GSP approximates)
- [[wiki/synthesis/why-ads-have-auctions.md]] — why auctions are used at all
