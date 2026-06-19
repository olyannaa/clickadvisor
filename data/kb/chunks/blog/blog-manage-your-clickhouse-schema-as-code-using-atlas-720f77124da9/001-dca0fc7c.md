---
source: blog
url: https://ariga.io/
topic: manage-your-clickhouse-schema-as-code-using-atlas
ch_version_introduced: '23.11'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# Manage your ClickHouse Schema\-as\-Code using Atlas

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Manage your ClickHouse Schema\-as\-Code using Atlas

![](/_next/image?url=%2Fuploads%2Frotem_90bcd87c4f.png&w=96&q=75)Rotem TamirMar 12, 2024 · 7 minutes read
> Today, we welcome Rotem Tamir from [ariga](https://ariga.io/), who maintains the open\-core tool [atlas](https://atlasgo.io/) for managing database schemas as code. Rotem dives into the details and shows the value of the recent support for ClickHouse.

## The Rise and Fall of Schema\-less Technologies [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#the-rise-and-fall-of-schema-less-technologies)

In the early 2010s, dynamically typed languages like Python and Javascript, and NoSQL databases like MongoDB and Elasticsearch marked the trend of departing from rigid, upfront schema planning. All of these technologies, with less verbose syntax and greater flexibility, promised quicker development cycles and easier prototyping, making them the languages of choice for startups and new projects aiming for rapid market entry.

However, as projects and organizations grew larger in size and complexity, the initial advantages of these technologies began to reveal significant trade\-offs. The lack of schema enforcement led to inconsistencies in data, making it harder to ensure data quality and integrity as applications evolved. The absence of strict type systems and the flexible nature of schema\-less databases made debugging and maintaining large codebases increasingly difficult.

The increasing interest in relational storage technology such as ClickHouse signifies a nuanced shift in our industry’s approach to data management. While modern data systems need to process diverse datasets that sometimes require an unstructured approach, there is a growing appreciation for the efficiency and organization that comes with strongly typed, structured data processing methods.

## Managing Schemas is still a Pain [\#](/blog/manage-your-clickHouse-schema-as-code-using-atlas#managing-schemas-is-still-a-pain)

One of the drivers of the NoSQL movement was that many developers wanted to avoid the pains of managing database schemas at all costs. Schema changes, also called migrations, require technical expertise to be done safely and efficiently. Modern databases provide a limited, *imperative*, way of changing schemas called DDL statements.
