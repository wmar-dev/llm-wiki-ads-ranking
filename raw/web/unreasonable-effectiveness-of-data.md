# The Unreasonable Effectiveness of Data

**Authors:** Alon Halevy, Peter Norvig, Fernando Pereira (Google)

**Publication:** IEEE Intelligent Systems, vol. 24, no. 2, March/April 2009, pp. 8–12

**DOI:** 10.1109/MIS.2009.36

---

## Abstract / Summary

Eugene Wigner's article "The Unreasonable Effectiveness of Mathematics in the Natural Sciences" (1960) examines why so much of physics can be neatly explained with simple mathematical formulas such as f = ma or e = mc^2. Meanwhile, sciences that involve human beings rather than elementary particles have proven more resistant to elegant mathematics. Economists suffer from physics envy over their inability to neatly model human behavior. An informal, incomplete grammar of the English language runs over 1,700 pages. Perhaps when it comes to natural language processing and related fields, we're doomed to complex theories that will never have the elegance of physics equations. But if that's so, we should stop acting as if our goal is to author extremely elegant theories, and instead embrace complexity and make use of the best ally we have: the unreasonable effectiveness of data.

## Key Points

### The Growth of Data
- The Brown Corpus (1960s): 1 million English words — a milestone at the time
- Several notable corpora ~100x larger followed
- 2006: Google released a trillion-word corpus with frequency counts for all sequences up to five words long
- This trillion-word corpus is "a million times larger than the Brown Corpus"
- Despite being from unfiltered Web pages (containing errors), the sheer scale outweighs these drawbacks
- A trillion-word corpus captures even very rare aspects of human behavior

### First Lesson: Use Available Large-Scale Data
- The biggest successes in NLP have been statistical speech recognition and statistical machine translation
- These tasks have large training sets available naturally (closed-caption broadcasts, EU operations)
- Traditional NLP problems (document classification, POS tagging, named-entity recognition, parsing) are NOT routine tasks, so they have no large corpus available in the wild
- "The first lesson of Web-scale learning is to use available large-scale data rather than hoping for annotated data that isn't available"
- Useful semantic relationships can be automatically learned from search queries and Web-based text patterns without any manually annotated data

### Second Lesson: Memorization Is a Good Policy with Enough Data
- Statistical language models consist primarily of huge databases of n-gram probabilities
- Built by counting occurrences of each n-gram sequence from corpora of billions or trillions of words
- "Simple models and a lot of data trump more elaborate models based on less data"
- Early machine translation relied on elaborate rules; today's statistical translation models consist mostly of large memorized phrase tables
- "Instead of assuming that general patterns are more effective than memorizing specific phrases, today's translation models introduce general rules only when they improve translation over just memorizing particular phrases"

### The Threshold of Sufficient Data
- For scene completion (removing unwanted objects from photos): with thousands of photos, results were poor; with millions of photos, the same algorithm performed quite well
- The number of grammatical English sentences is theoretically infinite, but in practice humans care to make only a finite number of distinctions
- "For many tasks, once we have a billion or so examples, we essentially have a closed set that represents (or at least approximates) what we need, without needing to infer general rules"

### Language Is Inherently Complex
- Hundreds of thousands of vocabulary words and a vast variety of grammatical constructions
- Every day, new words are coined and old usages modified
- Suggests we can't reduce what we want to learn about language to a small set of general rules
- Simple n-gram models or linear classifiers based on millions of specific features perform better than elaborate models that try to discover general rules

### Observations on Scale
- Features are proportional to available data and can often be personalized easily
- The system becomes naturally scalable
- Because of a huge training set, we can afford to have more features and still have enough data to estimate them correctly
- Web-derived corpora of millions, billions, or trillions of links, videos, images, tables, and user interactions capture even very rare aspects of human behavior

## References (from article)
1. E. Wigner, "The Unreasonable Effectiveness of Mathematics in the Natural Sciences," Comm. Pure and Applied Mathematics, vol. 13, no. 1, 1960, pp. 1–14.
2. R. Quirk et al., A Comprehensive Grammar of the English Language, Longman, 1985.
3. H. Kucera, W.N. Francis, and J.B. Carroll, Computational Analysis of Present-Day American English, Brown Univ. Press, 1967.
4. Google Books Ngram Viewer, http://books.google.com/ngrams
5. P. Norvig, "Natural Language Corpus Data," Beautiful Data, O'Reilly Media, 2009.
6. M. Banko and E. Brill, "Scaling to Very Very Large Corpora for Natural Language Disambiguation," Proc. 39th Ann. Meeting Assoc. Computational Linguistics (ACL 01), 2001.
7. J. Hays and A.A. Efros, "Scene Completion Using Millions of Photographs," ACM Trans. Graphics, vol. 26, no. 3, 2007.
8. A. Halevy, "Learning from Text at Web Scale," to be published in IEEE Intelligent Systems, 2009.

## About the Authors
- **Alon Halevy**: Research scientist at Google (halevy@google.com). Previously at University of Washington. Known for work on data integration, semantic web, and large-scale data management.
- **Peter Norvig**: Research director at Google (pnorvig@google.com). Previously at NASA Ames Research Center. Author of "Artificial Intelligence: A Modern Approach." Known for work on NLP, information retrieval, and software engineering.
- **Fernando Pereira**: Research director at Google (pereira@google.com). Previously at University of Pennsylvania and AT&T Labs. Known for work on statistical NLP, machine learning, and speech recognition.
