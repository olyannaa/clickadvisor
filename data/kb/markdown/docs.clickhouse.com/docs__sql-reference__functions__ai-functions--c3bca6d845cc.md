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


### Query\-level settings[​](#query-level-settings "Direct link to Query-level settings")


All AI\-related settings are listed in [Settings](/docs/operations/settings/settings) under the `ai_function_` prefix.


### Restricting endpoint hosts[​](#restricting-endpoint-hosts "Direct link to Restricting endpoint hosts")


The `endpoint` URL in an AI named collection is an outbound destination the server connects to under its own identity, carrying the named collection's `api_key` in the request headers. By default, ClickHouse permits any host. To restrict functions to a specific set of providers, configure [`remote_url_allow_hosts`](/docs/operations/server-configuration-parameters/settings#remote_url_allow_hosts) in the server config, e.g.:



```
<remote_url_allow_hosts>
    <host>api.openai.com</host>
    <host>api.anthropic.com</host>
</remote_url_allow_hosts>

```

Note that this setting is server\-wide and applies to all HTTP\-using features.


## Supported providers[​](#supported-providers "Direct link to Supported providers")




| Provider `provider` value Chat functions Notes| OpenAI `'openai'` Yes Default provider.| Anthropic `'anthropic'` Yes Uses `/v1/messages` endpoint. | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Observability[​](#observability "Direct link to Observability")


AI function activity is tracked through ClickHouse [ProfileEvents](/docs/operations/system-tables/query_log):




| ProfileEvent Description| `AIAPICalls` Number of HTTP requests made to the AI provider.| `AIInputTokens` Total input tokens consumed.| `AIOutputTokens` Total output tokens consumed.| `AIRowsProcessed` Number of rows that received a result.| `AIRowsSkipped` Number of rows skipped (quota exceeded, or error with `ai_function_throw_on_error = 0`). | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Query these events:



```
SELECT
    ProfileEvents['AIAPICalls'] AS api_calls,
    ProfileEvents['AIInputTokens'] AS input_tokens,
    ProfileEvents['AIOutputTokens'] AS output_tokens
FROM system.query_log
WHERE query_id = 'query_id'
AND type = 'QueryFinish'
ORDER BY event_time DESC;

```

## aiClassify[​](#aiClassify "Direct link to aiClassify")


Introduced in: v26\.4\.0


Classifies the given text into one of the provided categories using an LLM provider.


The function sends the text together with a fixed classification prompt and a JSON\-schema response format
constraining the model to return exactly one of the supplied labels. When the response is returned as a JSON
object of the form `{"category": "..."}`, the label is unwrapped and the label string is returned.


The first argument is a named collection that specifies the provider, model, endpoint, and API key.


**Syntax**



```
aiClassify(collection, text, categories[, temperature])

```

**Aliases**: `AIClassify`


**Arguments**


- `collection` — Name of a named collection containing provider credentials and configuration. [`String`](/docs/sql-reference/data-types/string)
- `text` — Text to classify. [`String`](/docs/sql-reference/data-types/string)
- `categories` — Constant list of candidate category labels. [`Array(String)`](/docs/sql-reference/data-types/array)
- `temperature` — Sampling temperature controlling randomness. Default: `0.0`. [`Float64`](/docs/sql-reference/data-types/float)


**Returned value**


One of the provided category labels, or the default value for the column type (empty string) if the request failed and `ai_function_throw_on_error` is disabled. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Classify sentiment**



```
SELECT aiClassify('ai_credentials', 'I love this product!', ['positive', 'negative', 'neutral'])

```


```
positive

```

**Classify a column**



```
SELECT body, aiClassify('ai_credentials', body, ['bug', 'question', 'feature']) AS kind FROM issues LIMIT 5

```


## aiExtract[​](#aiExtract "Direct link to aiExtract")


Introduced in: v26\.4\.0


Extracts structured information from unstructured text using an LLM provider.


The third argument may be either a free\-form natural\-language instruction (e.g. `'the main complaint'`) or a
JSON\-encoded schema of the form `'{"field_a": "description of field a", "field_b": "description of field b"}'`.


In instruction mode, the function returns the extracted value as a plain string, or an empty string if nothing was found.
In schema mode, the function returns a JSON object string whose keys match the requested schema; missing fields are `null`.


The first argument is a named collection that specifies the provider, model, endpoint, and API key.


**Syntax**



```
aiExtract(collection, text, instruction_or_schema[, temperature])

```

**Aliases**: `AIExtract`


**Arguments**


- `collection` — Name of a named collection containing provider credentials and configuration. [`String`](/docs/sql-reference/data-types/string)
- `text` — Text to extract information from. [`String`](/docs/sql-reference/data-types/string)
- `instruction_or_schema` — Free\-form extraction instruction, or a constant JSON object describing the fields to extract. [`const String`](/docs/sql-reference/data-types/string)
- `temperature` — Sampling temperature controlling randomness. Default: `0.0`. [`const Float64`](/docs/sql-reference/data-types/float)


**Returned value**


A single extracted value (instruction mode) or a JSON object string (schema mode). Returns the default value for the column type (empty string) if the request failed and `ai_function_throw_on_error` is disabled. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Free\-form instruction**



```
SELECT aiExtract('ai_credentials', 'The package arrived late and was damaged.', 'the main complaint')

```


```
late and damaged package

```

**Schema extraction**



```
SELECT aiExtract('ai_credentials', review, '{"sentiment": "positive, negative or neutral", "topic": "main topic of the review"}') FROM reviews LIMIT 5

```


## aiGenerate[​](#aiGenerate "Direct link to aiGenerate")


Introduced in: v26\.4\.0


Generates free\-form text content from a prompt using an LLM provider.


The function sends the prompt to the configured AI provider and returns the generated text.
An optional system prompt can be provided to guide the model's behavior (e.g. tone, format, role).
If no system prompt is given, the default system prompt is: `You are a helpful assistant. Provide a clear and concise response.`


The first argument is a named collection that specifies the provider, model, endpoint, and API key.


**Syntax**



```
aiGenerate(collection, prompt[, system_prompt[, temperature]])

```

**Aliases**: `AIGenerate`


**Arguments**


- `collection` — Name of a named collection containing provider credentials and configuration. [`String`](/docs/sql-reference/data-types/string)
- `prompt` — The user prompt or question to send to the model. [`String`](/docs/sql-reference/data-types/string)
- `system_prompt` — Optional constant system\-level instruction that guides the model's behavior (e.g. persona, output format), sent along with each prompt. [`String`](/docs/sql-reference/data-types/string)
- `temperature` — Sampling temperature controlling randomness. Default: `0.7`. [`Float64`](/docs/sql-reference/data-types/float)


**Returned value**


The generated text response, or the default value for the column type (empty string) if the request failed and `ai_function_throw_on_error` is disabled. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Simple question**



```
SELECT aiGenerate('ai_credentials', 'What is 2 + 2? Reply with just the number.')

```


```
4

```

**With system prompt**



```
SELECT aiGenerate('ai_credentials', 'Explain ClickHouse', 'You are a database expert. Be concise.')

```


**Summarize column values**



```
SELECT article_title, aiGenerate('ai_credentials', concat('Summarize in one sentence: ', article_body)) AS summary FROM articles LIMIT 5

```


## aiTranslate[​](#aiTranslate "Direct link to aiTranslate")


Introduced in: v26\.4\.0


Translates the given text into the specified target language using an LLM provider.


Additional style or dialect instructions may be passed as a fourth argument (e.g. `'keep technical terms untranslated'`).


The first argument is a named collection that specifies the provider, model, endpoint, and API key.


**Syntax**



```
aiTranslate(collection, text, target_language[, instructions[, temperature]])

```

**Aliases**: `AITranslate`


**Arguments**


- `collection` — Name of a named collection containing provider credentials and configuration. [`String`](/docs/sql-reference/data-types/string)
- `text` — Text to translate. [`String`](/docs/sql-reference/data-types/string)
- `target_language` — Target language name or BCP\-47 code (e.g. `'French'`, `'es-MX'`). [`String`](/docs/sql-reference/data-types/string)
- `instructions` — Optional constant additional instructions for the translator. [`String`](/docs/sql-reference/data-types/string)
- `temperature` — Sampling temperature controlling randomness. Default: `0.3`. [`Float64`](/docs/sql-reference/data-types/float)


**Returned value**


The translated text, or the default value for the column type (empty string) if the request failed and `ai_function_throw_on_error` is disabled. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Translate to French**



```
SELECT aiTranslate('ai_credentials', 'Hello, world!', 'French')

```


```
Bonjour le monde!

```

**Translate to Japanese with style instructions**



```
SELECT aiTranslate('ai_credentials', body, 'Japanese', 'Use polite form (desu/masu)') FROM articles LIMIT 5

```

[PreviousOverview](/docs/sql-reference/functions/overview)[NextArithmetic](/docs/sql-reference/functions/arithmetic-functions)- [Configuration](#configuration)
	- [Named collection parameters](#named-collection-parameters)- [Query\-level settings](#query-level-settings)- [Restricting endpoint hosts](#restricting-endpoint-hosts)- [Supported providers](#supported-providers)- [Observability](#observability)- [aiClassify](#aiClassify)- [aiExtract](#aiExtract)- [aiGenerate](#aiGenerate)- [aiTranslate](#aiTranslate)
Was this page helpful?
