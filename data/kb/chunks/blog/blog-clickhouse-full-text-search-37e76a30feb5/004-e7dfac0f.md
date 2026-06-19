---
source: blog
url: https://clickhouse.com/blog/full-text-search-ga-release
topic: inside-clickhouse-full-text-search-fast-native-and-columnar
ch_version_introduced: '10.1007'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 15
---

*text index*. Conceptually, this index consists of two key components: 1. **A dictionary**, storing all unique tokens across all documents. 2. **Posting lists**, which record the row numbers of documents that contain each token. Here’s how it works:

- When you search for a token, ClickHouse looks it up in the dictionary.
- If it is found, the dictionary returns the location of the corresponding posting list.
- The **posting list** is simply a list of row numbers — i.e., the documents — that contain that token.

Example:
- The token `wind` might appear in documents 12, 15, 99, 100, and 141\.
- The token `winter` might appear in documents 12, 514, 678, and 2583\.

This index design makes token lookups fast and efficient — even at massive scale.

Below is a simplified diagram of this structure:

![Full-text search 16.png](/uploads/Full_text_search_16_77b912e274.png)
Under the hood, ClickHouse stores and compresses both the dictionary and the posting lists using advanced data structures, which we’ll explore next.

### FSTs: Space\-efficient dictionaries [\#](/blog/clickhouse-full-text-search#fsts-space-efficient-dictionaries)

To find a token quickly, we need an efficient dictionary structure.

The most basic approach for this is a sorted list of (token → posting list) pairs. This lets us do a fast binary search to find a token. Assuming that the documents are written in natural language, this opens up another useful optimization opportunity: **prefix sharing**.

For example, many tokens start with the same prefix:

- "wind", "winter"
- "click", "clickhouse"

A plain list of tokens doesn’t take advantage of this \- but a **Finite State Transducer (FST)** does.

#### **What is an FST?** [\#](/blog/clickhouse-full-text-search#what-is-an-fst)

An FST is a compact automaton—essentially a graph of characters—that encodes the dictionary in a highly compressed manner. It was originally designed to translate strings from one language to another, but it is also a great fit for text indexing. Systems like [Lucene](https://burntsushi.net/transducers/) and ClickHouse use FSTs to represent sorted dictionaries.

Instead of storing each token as a string, an FST:

- Represents shared prefixes and suffixes only once
- Encodes each token as a path through a graph
- Emits an *output* (e.g. the address of a posting list) when a path reaches a final “accepting” state.

This makes the dictionary extremely compact, especially when tokens share common parts.

#### **Mapping tokens to posting lists** [\#](/blog/clickhouse-full-text-search#mapping-tokens-to-posting-lists)
