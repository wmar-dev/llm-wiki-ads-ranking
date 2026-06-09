---
status: current
sources: 1
source_type: official_documentation
ingest_count: 1
---

# Google Product Taxonomy for Shopping Ads

Google Shopping Ads uses a hierarchical product taxonomy — the **Google Product Taxonomy** — to classify every product in the feed. This taxonomy is hosted at `www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt` and contains ~6,000+ categories organized in a multi-level tree (depth up to 7+ levels). Each node has both a numeric ID and a breadcrumb-style full path.

## Source

- [Google product category `[google_product_category]` — Google Merchant Center Help](https://support.google.com/merchants/answer/6324436)

## How It Works

| Aspect | Detail |
|--------|--------|
| Automatic assignment | All products are *automatically* assigned a category from Google's evolving taxonomy based on title, description, price, brand, and GTIN |
| Manual override | `[google_product_category]` attribute lets merchants override the automatic category in specific cases: enforcement of category-specific fields, Ads campaign targeting, and alcohol compliance |
| Custom categories | `[product_type]` attribute lets merchants submit their own categorization (unlike `google_product_category` which must be from the predefined taxonomy) |
| Bidding usage | In Shopping campaigns, the taxonomy drives product group organization for bid management and reporting (available in AU, BR, FR, DE, IT, NL, NO, SE, TR, UK, US) |
| Format | Submit either the numeric ID (e.g., `2271`) or the full path (e.g., `Apparel & Accessories > Clothing > Dresses`) |

## Top-Level Categories

The taxonomy has 20+ top-level nodes and ~6,000+ leaf nodes across:

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

## Example Paths

| ID | Full Path |
|----|-----------|
| 1 | Animals & Pet Supplies |
| 4990 | Animals & Pet Supplies > Pet Supplies > Bird Supplies > Bird Food |
| 2271 | Apparel & Accessories > Clothing > Dresses |
| 233 | Electronics > Audio > Audio Players & Recorders > MP3 Players |
| 267 | Electronics > Communications > Telephony > Mobile Phones |
| 313 | Software > Computer Software |
| 53 | Arts & Entertainment > Party & Celebration > Gift Giving > Gift Cards & Certificates |

## Key Design Details

- The taxonomy is versioned (latest: 2021-09-21) and continuously updated; Google translates older submissions to the latest version for bidding
- Bidding in Shopping campaigns uses the **latest** category version, not the submitted one
- Only the first `product_type` value is used for bidding/reporting in Google Ads
- Taxonomy is available in multiple languages; if not available, English values or numeric IDs must be used
- Certain categories impose extra required fields (e.g., Apparel requires `size`/`color`, Software requires subscription flags)
