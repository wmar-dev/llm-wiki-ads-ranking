---
title: "Does Google Shopping Ads Have a Vertical Classification?"
type: "synthesis"
sources:
  - "web/google-merchant-center-product-category.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Does Google Shopping Ads Have a Vertical Classification?

**Yes.** Google Shopping Ads uses a hierarchical **Google Product Taxonomy** — a predefined, versioned classification system with ~6,000+ categories organized into a multi-level tree of 20+ top-level verticals and up to 7+ levels of depth.

## How It Works

![synthesis-google-shopping-vertical-classification-diagram-1](/assets/synthesis-google-shopping-vertical-classification-diagram-1.svg)

Every product submitted to Google Merchant Center is **automatically** assigned a category from this taxonomy. The merchant can override with the `[google_product_category]` attribute (must be from the predefined list) or use a custom `[product_type]` attribute for their own categorization scheme.

## Taxonomy Structure

| Level | Example |
|-------|---------|
| Top-level vertical | `Apparel & Accessories` (ID: 166) |
| Level 2 | `Apparel & Accessories > Clothing` |
| Level 3 | `Apparel & Accessories > Clothing > Dresses` (ID: 2271) |
| Level 4+ | `Apparel & Accessories > Clothing > Outerwear > Coats & Jackets` |

Each category has a **numeric ID** (e.g., `2271`) and a **breadcrumb path** (e.g., `Apparel & Accessories > Clothing > Dresses`). Merchants submit either.

## Top-Level Verticals (20+)

- Animals & Pet Supplies
- Apparel & Accessories
- Arts & Entertainment
- Baby & Toddler
- Business & Industrial
- Cameras & Optics
- Electronics
- Food, Beverages & Tobacco
- Furniture
- Hardware
- Health & Beauty
- Home & Garden
- Luggage & Bags
- Mature
- Media
- Office Supplies
- Religious & Ceremonial
- Software
- Sporting Goods
- Toys & Games
- Vehicles & Parts

## Role in Ranking & Bidding

The taxonomy is used for:

1. **Product group organization** in Shopping campaigns — bid management is per-category
2. **Enforcing category-specific attribute requirements** (e.g., Apparel requires `size`, Software requires subscription flags)
3. **Campaign targeting** — category-based ad group structure in Google Ads
4. **Automatic categorization** by Google's ML from product signals (title, description, GTIN, brand, price)
5. **Versioned evolution** — Google continuously updates the taxonomy and auto-translates older submissions to the latest version for bidding purposes

## Learn More

- Full taxonomy: `google.com/basepages/producttype/taxonomy-with-ids.en-US.txt` *(official_documentation)*
- Merchant Center Help: [Google product category attribute](https://support.google.com/merchants/answer/6324436) *(official_documentation)*
- Related: For how Google's search ad ranking works (non-Shopping), see [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
