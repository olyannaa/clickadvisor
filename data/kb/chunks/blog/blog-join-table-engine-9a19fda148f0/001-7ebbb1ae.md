---
source: blog
url: https://en.wikipedia.org/wiki/Dimensional_modeling
topic: clickhouse-cloud-fast-updatable-lookups-with-the-join-table-engine
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# ClickHouse Cloud: Fast, Updatable Lookups with the Join Table Engine

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud: Fast, Updatable Lookups with the Join Table Engine

![](/_next/image?url=%2Fuploads%2FImage_512x512_14_950d86cdef.jpeg&w=96&q=75)[Hellmar Becker](/authors/hellmar-becker)May 12, 2026 · 8 minutes read## Dictionaries in ClickHouse [\#](/blog/join-table-engine#dictionaries-in-clickhouse)

When you move data from your transactional or event\-based data sources to an analytical database like ClickHouse, you will likely consider modeling a dimensional schema according to the [Kimball methodology](https://en.wikipedia.org/wiki/Dimensional_modeling).

> [Dimensional modeling](https://en.wikipedia.org/wiki/Dimensional_modeling) always uses the concepts of facts (measures), and dimensions (context). Facts are typically (but not always) numeric values that can be aggregated, and dimensions are groups of hierarchies and descriptors that define the facts.

It follows that fact tables are typically immutable, and data are appended to them; whereas dimension tables are smaller, and subject to (infrequent) updates ([slowly changing dimensions](https://en.wikipedia.org/wiki/Slowly_changing_dimension)). When you run an analytical query, you have to join those dimensions against the fact table.

One common approach to do this in ClickHouse is to have a copy of the dimension data in memory in a [Dictionary](https://clickhouse.com/docs/engines/table-engines/special/dictionary). This approach enables [Direct Joins](https://clickhouse.com/blog/clickhouse-fully-supports-joins-direct-join-part4#direct-join) and is [recommended for optimizing join performance](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2#optimizing-joins).

A Dictionary is set up by specifying, among others, the `SOURCE` and `LIFETIME` attributes. ClickHouse pulls fresh data from the source and uses `LIFETIME` to determine how often it should refresh the Dictionary. But some customers asked me: Isn't there a way to update a Dictionary like a regular table? And indeed, there is a way to achieve this, using another special table engine.

## The `Join` table engine [\#](/blog/join-table-engine#the-join-table-engine)

The [`Join` table engine](https://clickhouse.com/docs/engines/table-engines/special/join) is just what we need here. It is an in\-memory structure, laying out data for a *specific* type of join that has to be stated in the table definition, and it is backed by a persistence layer. Setting up the `Join` table, you need to configure

- *join strictness*
- *join type*
- the *key column(s)* you want to use in the join.

### Join strictness [\#](/blog/join-table-engine#join-strictness)
