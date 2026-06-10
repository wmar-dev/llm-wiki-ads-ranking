# First-Price vs Second-Price Auction in Programmatic Advertising

**Source:** Setupad Blog — "First-Price vs Second-Price Auction | Differences Explained"
**URL:** https://setupad.com/blog/first-price-vs-second-price-auction/
**Date:** accessed 2026-06-09

## Summary (fetched)

Explains the two dominant auction-clearing rules used in programmatic
real-time bidding (RTB) and the industry-wide shift from second-price to
first-price auctions.

## How Each Works

- **First-price auction**: the highest bidder wins and pays the *exact* CPM
  bid (the "clearing price"). Example: bids of $3, $5, $4 → the $5 bidder
  wins and pays $5.00.
- **Second-price auction**: the highest bidder wins but pays only $0.01 above
  the second-highest bid. Same example → the $5 bidder wins but pays $4.01.

## Historical Shift to First-Price

- Google Ad Manager (display/video inventory, not initially AdSense)
  transitioned from second-price to first-price auctions in **2019**.
- Driven by "shady buy-side tactics" and the rise of **header bidding**:
  multiple ad exchanges now bid on the same impression simultaneously, which
  made second-price auctions hard to optimize (an SSP's internal second-price
  auction would discard less-competitive bids before they ever reached the
  publisher's final auction, depressing win rates).
- In a first-price header-bidding auction, the buyer's submitted bid IS the
  competing bid in the final auction — more compatible with multi-exchange
  competition.

## Implications

- **For publishers**: 78% reported higher revenue after switching to
  first-price; greater cross-exchange transparency; better visibility into
  true inventory value.
- **Bid shading**: in first-price auctions, advertisers/DSPs deliberately
  submit bids below their true valuation to avoid "paying their full bid" —
  estimated to be able to divert up to 20% of publisher revenue if
  unmitigated. Floor prices help mitigate this.
- **Transparency**: first-price removes inconsistencies in how different ad
  exchanges historically applied "second price" logic (some exchanges charged
  closer to the first price even while calling it "second price").

## Significance

This is the **programmatic/RTB display counterpart** to the GSP
(generalized second-price) auctions used in search (Google) and feed ads
(Meta, Reddit) already covered in the wiki. Search/social platforms still use
second-price-style (GSP) mechanisms with quality-score weighting, while
open-exchange programmatic display has largely moved to first-price due to
header bidding dynamics.
