---
source: blog
url: https://clickhouse.com/blog/query-analyze-hugging-face-datasets-with-clickhouse
topic: using-clickhouse-udfs-to-integrate-with-openai-models
ch_version_introduced: '3.5'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 13
---

# Using ClickHouse UDFs to integrate with OpenAI models

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Using ClickHouse UDFs to integrate with OpenAI models

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Sep 14, 2023 · 21 minutes read![Open AI.png](/uploads/Open_AI_1b9b4742c7.png)
## Introduction [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#introduction)

With ClickHouse, users have the capacity to utilize AI models directly in their SQL workloads. This can take the form of enriching data as it’s being inserted, or at query time, to supplement specific results. While many users are comfortable with training their own domain\-specific models, this can often be impractical for smaller teams or use cases. In these cases, a pre\-built “plug and play” model or service is often sufficient and can deliver good results with minimal effort.

In this post, we demonstrate:

- How ClickHouse can easily be integrated with third\-party APIs using ClickHouse User Defined Functions (UDFs) which provide “AI as a service”
- How these “plug and play” models can be used in ClickHouse directly for tasks such as sentiment analysis, and aggregating against those results for computing metrics like the number of positive and negative posts for a given subject

Given OpenAI’s recent popularity and high\-profile ChatGPT offering, we use OpenAI as an example. However, the simplicity of this approach means it can be easily adapted to competing services.

## User Defined Functions (UDFs) [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#user-defined-functions-udfs)
