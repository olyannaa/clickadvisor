---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ai-functions.md)#
topic: ai-functions-clickhouse-docs
ch_version_introduced: '0.0'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

# AI Functions \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- AI
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ai-functions.md)# AI Functions

AI Functions are built\-in functions in ClickHouse that you can use to call AI or generate embeddings to work with your data, extract information, classify data, etc...

NoteAI functions can return unpredictable outputs. The result will highly depend on the quality of the prompt and the model used.

All functions are sharing a common infrastructure that provides:

- **Quota enforcement**: Per\-query limits on tokens ([`ai_function_max_input_tokens_per_query`](/docs/operations/settings/settings#ai_function_max_input_tokens_per_query), [`ai_function_max_output_tokens_per_query`](/docs/operations/settings/settings#ai_function_max_output_tokens_per_query)) and API calls ([`ai_function_max_api_calls_per_query`](/docs/operations/settings/settings#ai_function_max_api_calls_per_query)).
- **Retry with backoff**: Transient failures are retried ([`ai_function_max_retries`](/docs/operations/settings/settings#ai_function_max_retries)) with exponential backoff ([`ai_function_retry_initial_delay_ms`](/docs/operations/settings/settings#ai_function_retry_initial_delay_ms)).

## Configuration[​](#configuration "Direct link to Configuration")

AI functions reference a **named collection** that stores provider credentials and configuration. The first argument to each function is the name of this collection.

Example statement to create a named collection with provider credentials:

```
CREATE NAMED COLLECTION ai_credentials AS
    provider = 'openai',
    endpoint = 'https://api.openai.com/v1/chat/completions',
    model = 'gpt-4o-mini',
    api_key = 'sk-...';

```

### Named collection parameters[​](#named-collection-parameters "Direct link to Named collection parameters")

| Parameter Type Default Description| `provider` String — Model provider. Supported: `'openai'`, `'anthropic'`. See note below.| `endpoint` String — API endpoint URL.| `model` String — Model name (e.g. `'gpt-4o-mini'`, `'text-embedding-3-small'`).| `api_key` String — Authentication key for the provider.| `max_tokens` UInt64 `1024` Maximum number of output tokens per API call.| `api_version` String — API version string. Used by Anthropic (`'2023-06-01'`). | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


NoteAny OpenAI\-compatible API (e.g. vLLM, Ollama, LiteLLM) can be used by setting `provider = 'openai'` and pointing the `endpoint` to your service.
