# Internet Advertising and the Generalized Second-Price Auction: Selling Billions of Dollars Worth of Keywords

**Authors:** Benjamin Edelman (Harvard), Michael Ostrovsky (Stanford), Michael Schwarz (UC Berkeley / NBER)

**Published:** American Economic Review, Vol. 97, No. 1, March 2007, pp. 242–259

**DOI:** 10.1257/aer.97.1.242

**Source URL:** https://www.nber.org/papers/w11765

---

## Abstract

Examines the generalized second-price (GSP) auction mechanism employed by search engines for online advertising. While GSP structurally resembles the Vickrey-Clarke-Groves (VCG) mechanism, it operates under fundamentally different principles. GSP generally does not have an equilibrium in dominant strategies, and truth-telling is not an equilibrium of GSP. The authors analyze the corresponding generalized English auction format and establish that it achieves a unique equilibrium with equivalent payoff outcomes to the VCG dominant strategy equilibrium.

---

## Key Sections

### The Structure and Evolution of Sponsored Search Auctions

Search engines sell keyword-linked advertising slots through sealed-bid auctions. Advertisers submit cost-per-click (CPC) bids; slots are allocated by ranking advertisers on bid × quality score. The mechanism evolved from a naive first-price auction to the GSP format.

### The Rules of GSP

- Each advertiser bids a CPC.
- Slots are ranked by bid (or bid × quality score).
- The winner of slot *k* pays the bid of the advertiser ranked one position below them (i.e., the "next" bidder's adjusted bid divided by the winner's quality score).
- Unlike a true second-price auction, each slot has its own "price" determined by the next competitor's bid.

### GSP and Locally Envy-Free Equilibria

GSP lacks dominant-strategy truthfulness. A counterexample shows the highest-value bidder can end up in the worst slot under truthful bidding. Bidders can profit from strategic shading.

The authors use stable matching theory (Roth and Sotomayor) to identify **locally envy-free equilibria**: states where no advertiser would prefer to swap positions with an adjacent bidder at that bidder's current price. These equilibria are the relevant solution concept for the dynamic, repeated bidding environment.

### Main Result: GSP and Generalized English Auction

The generalized English auction corresponding to GSP has a **unique locally envy-free equilibrium** with payoffs identical to the VCG dominant-strategy equilibrium. This provides a theoretical foundation for why GSP equilibria approximate efficient outcomes despite lacking dominant-strategy truthfulness.

### Revenue Implications

Locally envy-free GSP equilibria generate **higher revenue than VCG** for the platform. This explains the practical adoption of GSP over VCG by search engines.

---

## Subject Classification

- D44 — Auctions
- L81 — Retail and e-Commerce
- M37 — Advertising

---

## Source credibility

`peer_reviewed` — published in American Economic Review (top-5 economics journal); DOI present; institutional affiliations (Harvard, Stanford, UC Berkeley).
