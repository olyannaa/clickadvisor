---
source: blog
url: https://clickhouse.com/blog/vector-search-clickhouse-p2
topic: building-a-chatbot-for-hacker-news-and-stack-overflow-with-llamaindex-and-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 17
---

old' = 4, '45-54 years old' = 5, '55-64 years old' = 6, '65 years or older' = 7, 'NA' = 8, 'Prefer not to say' = 9), `annual_salary` Nullable(UInt64) ) ENGINE = MergeTree ORDER BY tuple() ```

> The column names here are very descriptive, e.g., `infrastructure_tools_have_worked_with` describes a list of tools a user wants to work with. These column names have been selected for the same reason we’ve also chosen here to liberally use the Enum type over LowCardinality. These choices make the data self\-descriptive. Later, our LLM will need to consider this schema when generating SQL queries. By using Enums and self\-describing column names, it avoids the need to provide additional context with an explanation of the meaning and possible values in each column.

Parsing this data from its original format requires a few SQL functions. While the original commands can be found [here](https://gist.github.com/gingerwizard/d3b32ed801973498e87145ed0c6e4bdb), we again provide the final data in Parquet in the interest of brevity:

```
INSERT INTO surveys SELECT * FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/surveys/2021/surveys-llama.parquet')

```

It is worth noting that data can be inserted into [ClickHouse via LlamaIndex](https://github.com/run-llama/llama_index/blob/main/docs/examples/vector_stores/ClickHouseIndexDemo.ipynb). We chose to do this directly via the ClickHouse client for performance and brevity reasons.

## Building a RAG pipeline in LlamaIndex [\#](/blog/building-hackernews-stackoverflow-chatbot-with-llamaindex-and-clickhouse#building-a-rag-pipeline-in-llamaindex)

LlamaIndex is available in both Python and Typescript. For our examples, we’ll use Python for no other reason than I prefer it :).

Rather than build our RAG flow in one go, we’ll assemble the building blocks first: testing a separate query engine for structured and unstructured queries.

> To install the ClickHouse integration for LlamaIndex, you can simply use `pip install llama-index-vector-stores-clickhouse`

### Generating SQL with LlamaIndex [\#](/blog/building-hackernews-stackoverflow-chatbot-with-llamaindex-and-clickhouse#generating-sql-with-llamaindex)

As mentioned above, we will need to convert some questions to SQL queries against our Stack Overflow data. Rather than building a prompt including our schema, making an HTTP request to ChatGPT, and parsing the response, we can rely on LlamaIndex to do this with a few calls. The following notebook is available [here](https://github.com/ClickHouse/examples/blob/main/blog-examples/llama-index/hacknernews_app/structured_nl_to_sql.ipynb).
