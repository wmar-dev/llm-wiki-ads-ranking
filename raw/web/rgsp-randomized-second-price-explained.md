# What is RGSP? Google's Randomized Generalized Second-Price ad auctions explained

**URL:** https://searchengineland.com/google-rgsp-randomized-generalized-second-price-ad-auctions-explained-433053

**Source:** Search Engine Land (industry trade publication)

**Fetched:** 2026-06-09 (via WebFetch, content summarized by extraction model)

---

## What is RGSP?

RGSP is a practice leveraged by Google that picks the winner of an ad auction at random from the top bidders as long as their long-term values (LTVs — a Google calculation that is essentially the same as Ad Rank) are close enough.

## How the Mechanism Works

The winning bidder pays the price equal to the next-highest bid plus one cent. The highest bidder doesn't automatically win the ad auction — a campaign's long-term value (LTV) is given more weight than raw bid rank.

## What Triggers RGSP

RGSP activates when multiple ads meet Google's minimum Ad Rank thresholds and their long-term values are proximate (close enough to each other). Without this mechanism, ads that meet quality criteria could rank below lower-quality ads in a "messy" deterministic ordering — industry experts cited this as the rationale Google has given.

## Why Google Introduced It

Google introduced RGSP to prevent quality bias / "winner-take-all" dynamics in auctions. According to DOJ trial testimony, the system prevents scenarios where a single large advertiser (e.g., "Amazon always shows up on top") dominates every auction, and is positioned by Google as reducing advertiser anxiety about constantly needing to adjust bids.

## Revenue Impact

Google executive Jerry Dischler testified that RGSP "increases Google's ad revenue," though he expressed uncertainty about whether it directly increases advertiser bids. He confirmed Google frequently changes auction mechanics, and that such changes have raised ad costs by approximately 5% for the average advertiser, with some queries experiencing increases up to 10%. Introduced in 2019, RGSP allowed Google to incrementally raise prices over time — increases the DOJ argued were not associated with better ad quality, contributing to roughly a 10% revenue increase.

## DOJ Antitrust Trial Findings (US v. Google)

The Department of Justice argued at the federal antitrust trial that RGSP creates unfair competition for advertisers, contending the highest bidder should always win an auction. The DOJ highlighted that advertisers must increase bids roughly **3.7x** higher than competitors to reliably avoid being randomized out of the top slot, and that Google provides no transparent guidance on how advertisers can improve their LTV/Ad Rank score.

A Google VP, Adam Juda, wrote in an internal email (cited at trial): "If I have to say, '[W]e randomly disable you if you don't bid high enough,' then I'm going to have another bad year" (the message included a winking emoji, which sparked debate at trial about whether it indicated awareness of the practice's optics).

## Advertiser Response

Advertisers have two practical levers if they want to avoid having a potential winning bid demoted at random to runner-up:
1. Improve their campaign's LTV (quality signals: pCTR, pCQ, pLQ)
2. Increase their bid amount

Because Google has not specified exactly how advertisers can improve LTV, increasing the bid is, in practice, the only lever advertisers can pull directly to avoid RGSP randomization.

The PPC/search-marketing community is divided: critics view RGSP as "auction manipulation" that harms competitors and obscures true price signals, while supporters note it can improve user experience by preventing low-relevance-but-high-bid ads from permanently dominating slots — "Higher quality ads typically lead to lower costs and more advertising success."
