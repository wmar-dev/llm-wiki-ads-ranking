# About Bid and Budget Pacing (Meta Business Help Center)

**Source URL:** https://www.facebook.com/business/help/571961726580148
**Source type:** official_documentation

**Note:** Direct WebFetch of this page returned only the page title (the page
appears to be JS-rendered / requires authentication). The quotes below were
recovered from web-search result snippets of this official Meta page, which
returned substantive verbatim text.

---

## Pacing is unified with bid strategy, not a separate admission gate

> "In practice, budget pacing and bid pacing are one process. Meta adjusts
> your bid or which auctions they enter based on how much budget and time are
> left for your ad set."

> "...pacing means raising or lowering your bid on an auction-by-auction
> basis, or deciding which auctions to enter and which to skip."

## The pacing multiplier

> "A process in Meta's system called pacing adjusts the ad's total value by
> adjusting what's called the pacing multiplier, which is used in ad auctions
> to help ensure that an advertiser's entire campaign budget is not spent in
> just a few days."

> "The total value of an ad in the auction has three key components: the
> advertiser bid, the estimated action rate, and ad quality. The pacing
> multiplier adjusts an ad's total value in this calculation."

## Spend adjustment based on opportunity

> "Meta may increase how much budget they spend if there's an opportunity to
> get many optimization events with costs aligned with your bid strategy, and
> they may also decrease how much budget they spend if there are few
> available optimization events with costs aligned with your bid strategy."

## Interaction with advertiser-set bid multipliers

Per Sprinklr's documentation of Meta's bid-multiplier feature: "Using bid
multipliers might affect your budget pacing if campaign delivery is limited
by budget. Using multipliers (especially small ones) might make it harder for
Facebook to evenly pace the budget spend throughout the day" — i.e.,
advertiser-set value rules (audience-segment bid multipliers) and Meta's own
pacing multiplier both modify the same "total value" auction term and can
interact.

---

## Takeaway

This is the most architecturally explicit description found for Cluster D-1:
Meta's pacing system is not a separate admission-control layer sitting "in
front of" the auction. It is implemented as a multiplicative adjustment
(the "pacing multiplier") folded directly into the same total-value/bid term
the auction ranks on — alongside the bid strategy's own bid (Cost Cap / Bid
Cap / Lowest Cost), the predicted action rate, and ad quality.
