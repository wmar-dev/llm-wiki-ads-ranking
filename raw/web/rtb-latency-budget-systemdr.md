# Real-Time Ad Bidding Systems (RTB): Designing for <100ms Responses

**Source URL:** https://systemdr.systemdrd.com/p/real-time-ad-bidding-systems-rtb

**Source type:** blog_post

---

## Overall Latency Budget

Real-time bidding (RTB) prices and serves a digital ad impression in roughly
**80-120ms** total, with the broader industry standard cited as **100-300ms**
including round-trip time (RTT). When a DSP (demand-side platform) receives a bid
request from an exchange, it has on the order of 100ms to receive the request,
evaluate the opportunity, run its bidding algorithm, and return a response. If a
response arrives even 1ms after the cutoff, it is dropped.

## Budget Allocation Across the Auction Pipeline

| Stage | Budget |
|---|---|
| Network transmission (publisher → exchange) | ~10ms |
| Exchange processing + fanout to DSPs | ~15ms |
| **DSP bid calculation** | **~50ms** |
| Response aggregation + auction logic | ~15ms |
| Network return (exchange → publisher) | ~10ms |

The DSP's ~50ms bid-calculation window is identified as the critical
engineering constraint — "where the real engineering challenge lives."

## OpenRTB Timeout Behavior

OpenRTB returns a 408 Timeout status when round-trip time plus auction time
exceeds the configured timeout; bids that arrive after the hard cutoff are
discarded entirely (not scored late).

## Design Strategies for Operating Within the Budget

- **Aggressive pre-computation and caching**: instead of computing signals
  on-the-fly, systems maintain hot caches of user profiles, campaign targeting
  rules, and bid multipliers ahead of the request.
- **Multi-tier cache architecture**: L1 in-memory caches for hot data, L2
  distributed caches (e.g., Redis) for broader rule sets, with strict per-query
  timeout budgets.
- **Skip-on-timeout for auxiliary signals**: if a database lookup would take
  more than ~5ms, it is often better to skip that signal entirely than risk
  missing the overall response deadline.
- **P99 monitoring**: industry guidance (from related search results) is to
  alert when P99 bid latency exceeds ~80ms (risk of timeout) and treat P99
  auction duration above 100ms as lost auctions.
