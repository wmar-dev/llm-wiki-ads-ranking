# Contextual Relevance of Ads @ Reddit

Source: https://www.reddit.com/r/RedditEng/comments/1r0hyfu/contextual_relevance_of_ads_reddit/
Fetched: 2026-06-08 via old.reddit.com (WebFetch bypass)
Authors: Daniel Peters, Aleksandr Plentsov, Anand Natu

---

## The Why

One of Reddit's core differentiators as a platform is the tremendous variety and depth of authentic human conversations that happen on the site, covering a huge variety of topics ranging from shopping advice to niche media fandoms. Subreddits allow entire communities to organize around individual topics (e.g. r/malefashionadvice), and posts within these subreddits go even deeper on a specific issue or question (e.g. the best men's t-shirt under $50).

From an ads standpoint, contextually relevant ads are naturally aligned to this structure; we can leverage deep, specific context to place ads where they're genuinely valuable to users, and therefore are most likely to be efficient and performant for advertisers. This blog post describes our efforts as a company to implement context-aware ad selection into our delivery systems, and what we've learned along the way, by:
1. Motivating the problem (why and how is contextual advertising good for Reddit users & advertisers?)
2. Defining the solution path (how did we improve the contextual relevance of ads?)
3. Identifying learnings and opportunities for further work

Today, we have three main categories of placements on Reddit: Mixed feeds (e.g. Home feed), Subreddit feeds (e.g. feed for r/espresso), and posts (e.g. an individual conversation page within r/espresso).

Intuitively, it's easy to hypothesize that posts represent the best opportunity for contextual advertising, since the context is very specific (e.g. showing an ad for an espresso grinder on a post asking which one is best). To prove out this hypothesis, we sought to validate the effect of contextual ads on business outcomes - specifically ad performance (e.g. do relevant ads drive better click-through / conversion rates).

## The How: Definition & Ground-Truth

Our first step in proving out the above relationships was to create a ground-truth definition for contextual relevance for posts; given a <post, ad> pair, how relevant is the ad to the context of the post? Our first iteration leveraged existing content understanding artifacts, specifically the IAB taxonomy labels we apply to posts; wherein ads and posts were considered relevant to each other if they had the same IAB taxonomy label, with more granular labels in the 3-tiered taxonomy hierarchy translating to a higher degree of relevance. This let us quickly prove out a promising offline correlation to performance, i.e. <ad, post> pairs with matching IAB categories demonstrated better performance metrics, with a monotonic increase in performance from no match to a Tier 1/2/3 match. This motivated further work to address multiple limitations with the IAB approach, specifically:
- IAB labels are a proxy for contextual relevance, but not an explicit definition of it, making them structurally unsuitable as ground-truth.
- IAB labels often lack granularity for certain relevance assessments, e.g. two different posts about Kubernetes and Twitter both fall within the same IAB Tier 3 category.
- IAB labels are rigid and don't allow us to characterize posts that fall within intermediate / intersectional states (e.g. a post about Auto Insurance could be relevant to Automotive or Insurance IAB categories).

Accordingly, we needed a purpose-built ground-truth labeler for contextual relevance; LLMs were a promising choice for this task, since language models are well-suited to the nuanced semantic analysis and inherent ambiguity of this problem.

We evaluated several variations of models and prompts by measuring agreement against a golden dataset of human labels. We found that using Gemini 1.5 Flash (now Gemini 2.5 Flash Lite) provided the right balance of quality & cost. Our prompt used a few-shot approach, with simple definitions of our relevance criteria (No/Low/Medium/High) and a handful of examples for each. We found that these LLM labels aligned to human labels at a comparable rate to the intrinsic alignment between any two human labelers. We further improved alignment by labeling more golden data and performing SFT (supervised fine-tuning) of the LLM.

Finally, we built an Airflow pipeline to sample a large set of real <ad, post> pairs daily, and label them with the LLM prompt using BigQuery's ML integration. These labels served two purposes:
1. We used them to continuously evaluate the relevance of the ads we were serving.
2. We could also use them to build up a data set for evaluating & training a relevance model.

Assessment of these LLM labels with respect to performance lift also indicated that they were better predictors of relevance than IAB labels.

## The How: Inorganic Experiments

After developing an LLM labeling schema for ground-truth post<>ad relevance labels, we shifted focus to improving the delivery funnel's ability to serve contextually relevant ads. The funnel consists of:
- The targeting layer considers advertisers' criteria to select eligible ads;
- Then, light rankers narrow that list down;
- Heavy rankers predict calibrated probabilities for performance outcomes: CTR / conversion rate;
- The final ad is selected in the Auction to maximize the utility function (roughly, P(outcome) * Value, e.g., p(CTR) * Bid).

Each of these stages represents a possible source of error. The fastest way to prove out a treatment online was to apply an intervention in the auction to systemically induce more relevant ad serves. Using IAB tags as an online relevance proxy, we ran two experiments:
1. A "filter" experiment wherein non-relevant candidates (i.e. w/ no IAB category match) were excluded outright from heavy ranking on the treatment slice.
2. After the filter yielded positive results, we developed a more balanced approach by applying a Utility boost to relevant ad candidates based on their degree of relevance (Tier 1/2/3 IAB category match). This led to more balanced performance improvements, especially for lower-funnel objectives (conversions).

## Selecting for User Intent

The lower-funnel performance bias we observed came with another hypothesis about the relationship between contextual relevance and user intent. Breaking out experiment traffic based on predicted user intent showed non-uniform results, wherein passive / low-intent users showed worse ad engagement, while high-intent users disproportionately benefited. One of the best proxies we have for high user intent is the referral source of the impression; millions of users visit Reddit every day from search engines like Google. That implies both the presence of high intent through search, and the Reddit post context becomes a descriptive proxy for that intent. Accordingly, applying the auction boost conditionally (preferentially for search-referred traffic) helped us further refine the treatment and drive performance.

## The How: Organic Treatments

### Relevance using Embeddings

After proving key relevance hypotheses through the above experiments, we finally set out to tackle the challenge of improving contextual relevance via the core delivery systems. This involved developing a predictive model that could vend relevance scores for <post, ad> pair, while meeting the scale and latency demands of online inference in the auction, while simultaneously addressing the shortcomings of the incumbent approach (using IAB categories).

Embeddings are a classic solution to this problem; we used our large dataset of LLM labels to evaluate several pre-trained embedding models by generating embeddings from post & ad text, and measuring how well post<>ad cosine similarity predicted the underlying LLM relevance labels (using PR AUC). For instance, in one iteration, we found that Stella (stella_en_400M_v5) performed best.

### Fine-Tuning

The generic embedding approach described above met our performance needs for online ad serving, and had better generalizability and representative power than IAB tags. From there, we refined the construction of these embeddings to more explicitly capture elements of contextual relevance:
- Complementary subreddit features: Subreddit context is often a crucial signal to understanding posts, so we used pre-existing subreddit embeddings as an additional feature for the experiment variants.
- Leveraging ad landing pages to enhance the ad representation with an LLM-generated summary of the landing page contents.
- Leveraging product attributes for product-centric ad formats (e.g. Dynamic Product Ads) to improve representational power (e.g. product brand, type etc.)

To implement these improvements, we built a multi-tower model using pre-trained Stella as our encoder for text features, and learning or reusing representations for other features.

Our initial training set consisted of millions of <ad, post/product> pairs, sampled daily from real served impressions. Training on this dataset was suboptimal for two reasons: 1) the relevance label distributions were constrained by the existing level of relevance on the platform, and 2) a small number of posts and ads were over-represented in the set of labeled pairs. To address these gaps, we rebuilt the dataset to include pairs that hadn't actually been served in real impressions. This let us better control the distribution of labels, and ensure every different type of post/ad/product was represented in the training set. We started by sampling N diverse ads/posts/products using embedding similarity as a diversity measure, ensuring adequate representation. We then constructed <ad, post/product> pairs from this set, using embedding similarity to try and build a consistent number of positive and negative samples for each ad & post in the dataset. This new training set was labeled with the same LLM prompt, and performed much better both qualitatively and quantitatively.

### Results & Integration

Using the LLM's labeled data for evaluation:

| Treatment | Normalized PRAUC multiple (Ground truth: LLM relevance) |
|---|---|
| IAB category match | 1x |
| Cosine similarity of pre-trained Stella embeddings | 2.08x |
| Cosine similarity of fine-tuned embeddings v1 | 3.2x (+54% to pretrained) |

Today, these fine-tuned embeddings have been systemically integrated into all of the major modeling steps in the funnel: for targeting and retrieval, and as features in light + heavy rankers for different objectives (clicks, conversions, etc.). This has resulted in online improvement which is directionally consistent with our offline results and hypotheses, incremental to the gains from our inorganic MVP solution (boosting).

Since we can compute this similarity at scale, we also integrated it in our online experiment platform and started to use it as an "FYI" metric in all tests we run.

## What's next

We continue to work on improving guidelines, metrics, and embeddings; look for better ways to integrate them into the funnel and break the feedback loops and biases in the data we train our rankers on; we seek a better understanding of when relevance is a must... stay tuned!

## Acknowledgements

Eng: Ted Ni, Andrea Trianni, Alessandro Tiberi, Clement Wong.
Product: Looja Tuladhar, Lillian Kravitz.
DS: Ryan Sekulic.
