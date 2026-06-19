---
source: blog
url: https://clickhouse.com/blog/enhancing-google-analytics-data-with-clickhouse
topic: building-a-rag-pipeline-for-google-analytics-with-clickhouse-and-amazon-bedrock
ch_version_introduced: '0.5078125'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 18
---

# Building a RAG pipeline for Google Analytics with ClickHouse and Amazon Bedrock

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building a RAG pipeline for Google Analytics with ClickHouse and Amazon Bedrock

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Nov 21, 2023 · 31 minutes read## Introduction [\#](/blog/retrieval-augmented-generation-rag-with-clickhouse-bedrock#introduction)

In [a recent blog post](https://clickhouse.com/blog/enhancing-google-analytics-data-with-clickhouse), we explored how users can supercharge their website analytics by using ClickHouse and Superset to deliver a fast and flexible means of querying raw data from Google Analytics for minimal cost.

Superset's easy learning curve prompted me to explore how LLMs could offer an even simpler approach to exploring Google Analytics data for less technical users. Amidst the widespread use of acronyms like RAG, ML, and LLM in technical blogs, I seized this chance to delve into an area of Computer Science where my experience is admittedly limited. This post serves as both a record of my journey and experiments in using LLMs and RAG to simplify application interfaces.

Armed with a rather generous set of AWS account permissions granting me access to Amazon Bedrock, I set about trying to build a natural language interface to my raw Google Analytics data. The objective here was simple: to allow users to ask a question in natural language and the appropriate SQL be generated, that ultimately answers their question with the underlying data. If successful, this could form the basis of a simple interface from which a user could ask a question and a sensible chart be rendered.

[![](/uploads/proposed_app_bc63d14983.png)](/uploads/proposed_app_bc63d14983.png)

## Google Analytics with concepts [\#](/blog/retrieval-augmented-generation-rag-with-clickhouse-bedrock#google-analytics-with-concepts)

From our [previous blog](https://clickhouse.com/blog/enhancing-google-analytics-data-with-clickhouse), recall we proposed the following schema to hold Google Analytics data in ClickHouse:
