---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-inverted-indices-in-clickhouse-clickhouse
ch_version_introduced: '0.006'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 10
---

2, 3 | | Wait | 1 | | wind | 0, 3 | As we can see, the inverted index associates each term with "postings", i.e., the row positions of the documents which contain the corresponding term.

The dictionary in inverted indexes is usually organized in a way that terms can be found quickly. The simplest method to achieve that is to store the terms in alphabetical sort order and to use binary search for lookups. In contrast to that, ClickHouse stores dictionaries as finite state transducers (FSTs). We will discuss FSTs in more detail below. Their main advantage is that redundancies, e.g., shared prefixes between adjacent terms, can be easily removed. This reduces the memory footprint of the dictionary and improves the overall throughput.

Further interesting extensions of dictionaries that are currently not supported but might be added in the future include the following:

- a removal of stop words that carry no semantic weight like "a", "and", "the" etc., and
- lemmatization and stemming as language\-specific techniques to reduce words to their linguistic word root, e.g., "walking" becomes "walk", "went" becomes "go", "driving" becomes "drive" etc.

ClickHouse also stores the posting lists in a compressed format (more specifically as "roaring bitmap") with the goal of reducing their memory consumption. We will dig a bit deeper into posting list compression below. In the initial inverted index version, posting lists refer to the row positions of the documents which contain the corresponding term. This might be extended in the future with additional metadata, for example:

- A document frequency count stored with each posting indicating how often the term occurs in the document. Such information will allow us to calculate the term frequency / inverse document frequency (TF\-IDF), which is useful for [ranking search results](https://monkeylearn.com/blog/what-is-tf-idf/).
- Word\-level postings, i.e., the exact positions of terms inside documents. Such data allows to answer phrase queries where the user does not search for a single term but for multiple consecutive terms (a "phrase").

If we rerun our query, it will automatically use the index:
