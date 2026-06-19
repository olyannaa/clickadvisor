---
source: blog
url: https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library
topic: we-built-a-vector-search-engine-that-lets-you-choose-precision-at-query-time
ch_version_introduced: '0.99105519'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 14
---

# We built a vector search engine that lets you choose precision at query time

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# We built a vector search engine that lets you choose precision at query time

![](/_next/image?url=%2Fuploads%2FImage_from_Slack_f18e0d24a5.png&w=96&q=75)Raufs DunamalijevsOct 28, 2025 · 27 minutes read
> **TL;DR**  
> 
> We added **QBit** to ClickHouse, a column type that stores floats as bit planes. It lets you choose how many bits to read during vector search, tuning recall and performance without changing the data.

Vector search is everywhere now. It powers [music recommendations](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library), [retrieval\-augmented generation (RAG) for large language models](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts) where external knowledge is fetched to improve answers, and even googling is [powered by vector search](https://en.wikipedia.org/wiki/RankBrain) to some extent. Many specialised databases are built to handle vector search very well. Nevertheless, these systems are rarely ideal for storing and querying structured data. As a result, we often see [users preferring regular databases](https://youtu.be/jmVxfGEN0QQ?si=utgs-siTTUjAhYoV&t=1069) with ad\-hoc vector capabilities over fully specialised vector stores.

In ClickHouse, brute\-force vector search has been supported for [several years](https://clickhouse.com/blog/vector-search-clickhouse-p1) already. More recently, we added methods for approximate nearest neighbour (ANN) search, including **HNSW** – the current standard for fast vector retrieval. We also revisited quantisation and built a new data type: **QBit**.

Each vector search method has its own parameters that decide trade\-offs for recall, accuracy, and performance. Normally, these have to be chosen up\-front. If you get them wrong, a lot of time and resources are wasted, and changing direction later becomes painful.

With QBit, no early decisions are needed. You can adjust precision and speed trade\-off directly at query time, exploring the right balance as you go.

## Vector search primer [\#](/blog/qbit-vector-search#vector-search-primer)

Let’s start with the basics. Vector search is used to find the most similar document (text, image, song, and so on) in a dataset. First, all items are converted into high\-dimensional vectors (arrays of floats) using embedding models. These embeddings capture **the meaning** of the data. By comparing distances between vectors, we can see how close two items are in meaning.
