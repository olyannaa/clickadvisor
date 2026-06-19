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


UDFs (user defined functions) in ClickHouse take a few forms. In a recent post, we shared [how you can use a ClickHouse SQL\-defined function](https://clickhouse.com/blog/query-analyze-hugging-face-datasets-with-clickhouse) to query an externally hosted dataset in Hugging Face. While SQL\-defined functions like these are extremely useful for generalizing common SQL tasks, sometimes users need the full functionality of a programming language with which they are familiar. For this, ClickHouse supports [Executable User Defined Functions](https://clickhouse.com/docs/en/sql-reference/functions/udf). These give developers the flexibility to invoke any external executable program or script to process data. In our simple examples below, we’ll use this capability to invoke simple Bash and Python scripts that will query an OpenAI API. We’ll show how the API response can automatically enrich data being inserted or queried by ClickHouse.


![open_ai_udfs.png](/uploads/open_ai_udfs_53eefe62df.png)
## Using OpenAI [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#using-openai)


Most users are familiar with OpenAI through its popular ChatGPT service, which has already revolutionized working behaviors and day\-to\-day tasks. OpenAI offers a REST API for businesses to access the models that power ChatGPT in existing services and automated processes. These services provide everything from chat completion and [embedding generation](https://clickhouse.com/blog/vector-search-clickhouse-p1) to image generation and speech\-to\-text. In our examples, we focus on chat completion, which can be repurposed for more generic tasks, such as entity extraction and sentiment labeling.


*Note: All requests to the OpenAI service require a token \- passed as the environment variable OPENAI\_API\_KEY in the examples below. Users can sign up for a trial and get sufficient free credits for the examples here.*


As well as being able to act as a chatbot, OpenAI’s completion service also supports tasks such as sentiment analysis and the extraction of structure. For these tasks, the developer has to provide the OpenAI service with relevant instructions to describe the expected behavior via a [system role](https://platform.openai.com/docs/guides/gpt/chat-completions-api). An example REST API request to perform a sentiment analysis on some text might look like the following. Here, we ask the service to classify a forum post. Notice how we need to provide explicit instructions to return only a single token specifying sentiment:



```
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
  "model": "gpt-3.5-turbo",
  "messages": [
	{
  	"role": "system",
  	"content": "You are an AI language model trained to analyze and detect the sentiment of forum comments."
	},
	{
  	"role": "user",
  	"content": "Analyze the following hackernews comment and determine if the sentiment is: positive, negative or neutral. Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: I can say for BigQuery and Databricks from personal experience.<p>BigQuery is much slower and is much more expensive for both storage and query.<p>Databricks (Spark) is even slower than that (both io and compute), although you can write custom code&#x2F;use libs.<p>You seem to underestimate how heavily ClickHouse is optimized (e.g. compressed storage)."
	}
  ],
  "temperature": 0,
  "max_tokens": 256
}'

{
  "id": "chatcmpl-7vOWWkKWGN7McODMXJzQB6zzDcx0r",
  "object": "chat.completion",
  "created": 1693913320,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
	{
  	"index": 0,
  	"message": {
    	"role": "assistant",
    	"content": "NEGATIVE"
  	},
  	"finish_reason": "stop"
	}
  ],
  "usage": {
	"prompt_tokens": 147,
	"completion_tokens": 2,
	"total_tokens": 149
  }
}

```

*Note we use the more cost\-effective `gpt-3.5-turbo` model here and not the latest `gpt-4` model. The former is sufficient for example purposes. We leave it to readers to determine its performance levels.*


The same service can also be used to extract structure. Suppose we wished to extract the mentioned technologies from the above text as a list of string values. We need to modify the instructions a little:



```
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
  "model": "gpt-3.5-turbo",
  "messages": [
	{
  	"role": "system",
  	"content": "You are an AI language model trained to extract entities from forum comments"
	},
	{
  	"role": "user",
  	"content": "From the following text extract the many technologies mentioned as a comma seperated list: I can say for BigQuery and Databricks from personal experience.<p>BigQuery is much slower and is much more expensive for both storage and query.<p>Databricks (Spark) is even slower than that (both io and compute), although you can write custom code&#x2F;use libs.<p>You seem to underestimate how heavily ClickHouse is optimized (e.g. compressed storage)."
	}
  ],
  "temperature": 0,
  "max_tokens": 20
}'

{
  "id": "chatcmpl-7vOdLnrZWeax3RxjeUNelCTdGvr8q",
  "object": "chat.completion",
  "created": 1693913743,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
	{
  	"index": 0,
  	"message": {
    	"role": "assistant",
    	"content": "BigQuery, Databricks, Spark, ClickHouse"
  	},
  	"finish_reason": "stop"
	}
  ],
  "usage": {
	"prompt_tokens": 122,
	"completion_tokens": 11,
	"total_tokens": 133
  }
}

```

A few notes on the above request parameters:


- We set [`temperature`](https://platform.openai.com/docs/api-reference/chat/create#temperature) to 0 to remove any randomness from the responses. For these use cases, we don’t need creative text \- only deterministic text analysis.
- In both cases, we set [`max_tokens`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens) to determine the length of the response. A [token is around ¾ of a word](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them). Hence, we adapted our request.


## Dataset [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#dataset)


For our example dataset, we use Hacker News posts. This dataset, which is available in our public play environment, consists of all posts and comments on the popular Hacker News forum from 2006 to August 2023: around 37 million rows. The table schema is shown below.


We’re interested in the `title` and `text` columns for our purposes. We leave exploring this dataset as an exercise for the reader, who can follow the instructions [here](https://github.com/ClickHouse/ClickHouse/issues/29693) if they wish to load the latest version of this dataset into their own ClickHouse instance. Alternatively, we have provided a [Parquet file on S3](https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/2023-08-18.parquet), which can be loaded using the [s3 function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3), as shown below:



```
CREATE TABLE hackernews
(
	`id` UInt32,
	`deleted` UInt8,
	`type` Enum8('story' = 1, 'comment' = 2, 'poll' = 3, 'pollopt' = 4, 'job' = 5),
	`by` LowCardinality(String),
	`time` DateTime,
	`text` String,
	`dead` UInt8,
	`parent` UInt32,
	`poll` UInt32,
	`kids` Array(UInt32),
	`url` String,
	`score` Int32,
	`title` String,
	`parts` Array(UInt32),
	`descendants` Int32
)
ENGINE = MergeTree
ORDER BY id

INSERT INTO hackernews SELECT * FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/2023-08-18.parquet')

```

## Adding sentiment [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#adding-sentiment)


For our example, let's assume we want to add sentiment analysis to our Hacker News data stored in ClickHouse. To do so, we need to invoke the earlier OpenAI REST API via a ClickHouse UDF. The simplicity of this request means even a straightforward bash script may be sufficient, as seen below (the below requires [jq](https://jqlang.github.io/jq/)). Further along, we demonstrate how to do this in Python directly.



```
#!/bin/bash

while read read_data; do
  sentiment=$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <insert>" \
  -d "{
  \"model\": \"gpt-3.5-turbo\",
  \"messages\": [
    	{
    	\"role\": \"system\",
    	\"content\": \"You are an AI language model trained to analyze and detect the sentiment of forum comments.\"
    	},
    	{
    	\"role\": \"user\",
    	\"content\": \"Analyze the following Hacker News comment and determine if the sentiment is: positive, negative or neutral. Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: ${read_data}\"
    	}
  ],
  \"temperature\": 0,
  \"max_tokens\": 2,
  \"temperature\": 0
}" | jq -r '.choices[0].message.content')
  printf "$sentiment";
done

```

This script should be saved in the `user_scripts` directory of ClickHouse as `sentiment.sh` and made executable. The following entry should also be added to a file `openai_functions.xml` and saved to the ClickHouse configuration directory (typically `/etc/clickhouse-server/`).



```
<functions>
       <function>
           <name>sentiment</name>
           <type>executable</type>
           <format>TabSeparated</format>
           <return_type>String</return_type>
           <argument>
             <type>String</type>
           </argument>
           <command>sentiment.sh</command>
           <command_read_timeout>10000</command_read_timeout>
           <command_write_timeout>10000</command_write_timeout>
           <max_command_execution_time>10000</max_command_execution_time>
       </function>
</functions>

```

This configuration makes the UDF available to ClickHouse. Other than modifying the timeouts here to allow for the latency of OpenAI requests, we provide a function name, `sentiment`, and specify the input and return types.


With the above configuration, users can request sentiment for a snippet of text via a simple function call e.g.



```
SELECT sentiment('Learn about the key differences between ClickHouse Cloud and Snowflake and how ClickHouse Cloud outperforms Snowflake across the critical dimensions for real-time analytics: query latency and and cost.') AS sentiment

┌─sentiment─┐
│ POSITIVE  │
└───────────┘

1 row in set. Elapsed: 0.433 sec.

```

While the above gets us started, a more robust solution with error handling will likely be required. For this, we may wish to convert the above to Python. The Python script below adds basic error handling and retries with a backoff. The latter here is to specifically address the challenge of OpenAI rate limits \- see [Handling latency \& rate limits](/blog/clickhouse-open-ai-user-defined-functions-udfs#handling-latency--rate-limits) for more details.


Note the need for the [openai](https://github.com/openai/openai-python) and tenacity libraries for handling API requests and rate limiting.



```
#!/usr/bin/python3
import sys
import openai
from tenacity import (
   retry,
   stop_after_attempt,
   wait_random_exponential,
)

openai.api_key = "<INSERT>"
request_timeout = 3

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(20))
def completion_with_backoff(**kwargs):
   return openai.ChatCompletion.create(**kwargs)

def extract_sentiment(text):
   if text == "":
       return "NEUTRAL"
   messages = [{"role": "system",
                "content": "You are an AI language model trained to analyze and detect the sentiment of hackernews forum comments."},
               {
                   "role": "user",
                   "content": f"Analyze the following hackernews comment and determine if the sentiment is: positive, negative or neutral. "
                              f"Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: {text}"
               }]
   try:
       response = completion_with_backoff(model="gpt-3.5-turbo", messages=messages, max_tokens=30, temperature=0, request_timeout=request_timeout)
       return response.choices[0].message.content
   except:
       return "ERROR"

for size in sys.stdin:
   # collect a batch for performance
   for row in range(0, int(size)):
       print(extract_sentiment(sys.stdin.readline().strip()))
   sys.stdout.flush()

```

*The chat\-based nature of the service makes evaluating multiple pieces of text for sentiment in a single request challenging. In order to keep these examples simple, we have made a request per row. A more optimized solution may batch requests and ask the endpoint to evaluate a set of text.*


The above assumes that any input passed from ClickHouse includes a prefix for the number of rows. This is used to determine the number of times to iterate on the subsequent input. This can allow operations within the Python script to be batched for higher performance.


Our configuration for the above function has a few additional settings other than defining a unique name, `setiment_p`. We set the `type` to an executable pool to improve throughput performance. This will start the command N times (10 below), allowing multiple simultaneous invocations. The setting `send_chunk_header` ensures a numeric heading indicating the number of rows to be processed precedes any input. We increase timeout settings in case large blocks of rows are passed.



```
<functions>
    <function>
    <name>sentiment_p</name>
   	 <type>executable_pool</type>
   	 <pool_size>10</pool_size>
   	 <send_chunk_header>true</send_chunk_header>
   	 <format>TabSeparated</format>
   	 <return_type>String</return_type>
   	 <argument>
   	   <type>String</type>
   	 </argument>
   	 <command>sentiment.py</command>
   	 <command_read_timeout>10000000</command_read_timeout>
         <command_write_timeout>10000000</command_write_timeout>
         <max_command_execution_time>1000000</max_command_execution_time>
    </function>
</functions>

```

We can apply either of the above functions to a set of rows for a column. In the example below, we request sentiment for the title and text of 10 rows containing the word ClickHouse.



```
SELECT text, sentiment_p(text) AS sentiment
FROM hackernews WHERE text LIKE '%ClickHouse%' OR title LIKE '%ClickHouse%'
ORDER BY time DESC
LIMIT 2
FORMAT Vertical
Row 1:
──────
text:  	Yeah ClickHouse is definitely the way to go here. Its ability to serve queries with low latency and high concurrency is in an entirely different league from Snowflake, Redshift, BigQuery, etc.
sentiment: POSITIVE

Row 2:
──────
text:  	There are other databases today that do real time analytics (ClickHouse, Apache Druid, StarRocks along with Apache Pinot).  I&#x27;d look at the ClickHouse Benchmark to see who are the competitors in that space and their relative performance.
sentiment: POSITIVE

2 rows in set. Elapsed: 2.763 sec. Processed 37.17 million rows, 13.30 GB (13.46 million rows/s., 4.82 GB/s.)

```

The UDF is only executed here once the final results have been collated \- meaning only two requests are required. This approach is ideal since the latency of a request to OpenAI is typically much higher than the time for ClickHouse to evaluate the query.


Taking this further, we can compute the number of positive and negative posts for ClickHouse with a simple aggregation. This incurs more overhead, as we need to make over 1600 invocations of the OpenAI API. This is reflected in the final timing.



```
SELECT
	count(),
	sentiment
FROM hackernews
WHERE (text LIKE '%ClickHouse%') OR (title LIKE '%ClickHouse%')
GROUP BY sentiment_p(text) AS sentiment
FORMAT PrettyCompactMonoBlock

┌─count()─┬─sentiment─┐
│ 	192 │ NEGATIVE  │
│ 	628 │ NEUTRAL   │
│ 	857 │ POSITIVE  │
└─────────┴───────────┘

3 rows in set. Elapsed: 203.695 sec. Processed 37.17 million rows, 13.28 GB (182.48 thousand rows/s., 65.21 MB/s.)

```

### Handling latency \& rate limits [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#handling-latency--rate-limits)


The usefulness of the OpenAI API is limited by two factors: its latency and the rate limits it imposes. Note that these variables will differ depending on the “plug and play” model chosen. In our examples, we use OpenAI. There are many others to choose from, each with their own tradeoffs.


Latency will impact the minimum response time of a query. While OpenAI allows multiple concurrent queries to ensure this does not impact throughput, rate limiting will prove more restrictive. We thus recommend users use these APIs either for ad hoc analysis where the function is used on a small subset of results (e.g. our earlier 2 row example), or for enriching data at insert time. Prior to showing an example of the latter, let’s explore the latency and rate limiting limitations.


We can assess the latency of a response by modifying our sentiment curl request to use a [simple format file](https://pastila.nl/?1385630d/57a537ca8c6249111eb201f59f72616a#n7YL5DBm6zQBeBOW57i3rw==):



```
curl -w "@curl-format.txt" -o /dev/null -s  https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
  "model": "gpt-3.5-turbo",
  "messages": [
    	{
    	"role": "system",
    	"content": "You are an AI language model trained to analyze and detect the sentiment of forum comments."
    	},
    	{
    	"role": "user",
    	"content": "Analyze the following hackernews comment and determine if the sentiment is: positive, negative or neutral. Return only a single word, either POSITIVE, NEGATIVE or NEUTRAL: I can say for BigQuery and Databricks from personal experience.<p>BigQuery is much slower and is much more expensive for both storage and query.<p>Databricks (Spark) is even slower than that (both io and compute), although you can write custom code&#x2F;use libs.<p>You seem to underestimate how heavily ClickHouse is optimized (e.g. compressed storage)."
    	}
  ],
  "temperature": 0,
  "max_tokens": 256,
  "temperature": 0
}'

time_namelookup:  0.081196s
time_connect:  0.084907s
time_appconnect:  0.095853s
time_pretransfer:  0.095937s
time_redirect:  0.000000s
time_starttransfer:  0.095942s
----------
time_total:  0.650401s


```

The total latency here of 0\.65s limits our query response times, but is mitigated by the fact we have a command pool (10 above) which ClickHouse’s parallelized execution pipeline can exploit. However, this parallelization is in turn restricted by OpenAPI’s rate limits.


OpenAI is both limited by requests per minute as well as tokens per minute. For our `gpt-3.5-turbo` model, this is 90k Tokens per Minute (TPM) and 3500 Requests per Minute (RPM). Rate limits vary per model and account type \- further details [here](https://platform.openai.com/docs/guides/rate-limits/what-are-the-rate-limits-for-our-api).


To address this, we added basic rate limiting to our UDF. The API [returns rate limiting](https://platform.openai.com/docs/guides/rate-limits/rate-limits-in-headers) information (i.e. how many tokens and requests are left in the next minute) in headers. While we could develop a rate limiting function to use this information, OpenAI suggests several libraries designed to address this with [exponential backoff](https://platform.openai.com/docs/guides/rate-limits/retrying-with-exponential-backoff). This has the advantage of us not needing to track request and token usage across multiple threads.


The above timing for our aggregation query (203\.695s) suggests either we weren’t fully exploiting our pool of 10 UDF commands, or are being rate limited. Assuming an average latency of 0\.65\*, fully parallelized, we would expect our total execution time to be closer to 100s here (1600/10 \* 0\.65 \= 104s).


*\*We assume the Open AI API can maintain this latency irrespective of factors such as variable content length (some comments will be longer than others).*


This performance of 100s isn’t achieved because the query is being restricted by rate limiting on the OpenAI API \- specifically, the token limit. Each Hacker News comment is on average around 330 words as shown below, or about [around 80 tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) (\~4 chars to a token). This does not include our prompt and system text however, which adds an additional 60 tokens. Our ClickHouse related subset also has a higher average token length at 136\.



```
SELECT
	round(avg(length(text))) AS num_chars,
	round(num_chars * 0.25) AS num_tokens
FROM hackernews

┌─num_chars─┬─num_tokens─┐
│   	333 │     	83 │
└───────────┴────────────┘

1 row in set. Elapsed: 1.656 sec. Processed 37.17 million rows, 12.72 GB (22.44 million rows/s., 7.68 GB/s.)

SELECT
	round(avg(length(text))) AS num_chars,
	round(num_chars * 0.25) AS num_tokens
FROM hackernews
WHERE (title LIKE '%ClickHouse%') OR (text LIKE '%ClickHouse%')

┌─num_chars─┬─num_tokens─┐
│   	546 │    	136 │
└───────────┴────────────┘

1 row in set. Elapsed: 1.933 sec. Processed 37.17 million rows, 13.28 GB (19.23 million rows/s., 6.87 GB/s.)
Peak memory usage: 73.49 MiB.

```

While each comment requires one request, resulting in a total of 1600 requests (below the 3500 limit per minute), we have a total of [900k chars or 229k tokens](https://pastila.nl/?00e8b05d/192338b365fd6bbf7654d0457e05cc55#N2cUeyk0TLRXe++EwxyAWg==). When considering our prompt text, this increases to [329k tokens](https://pastila.nl/?0539f3bd/ac17ecf5cded417d2706c678bd8ec230#R1nC2mlEmU38XbOLJNtMrw==) (60 extra per request). This is well above the 90k per minute limit. Despite this, if this work was scheduled perfectly, we would expect this request to complete in the 200 secs (329/90 \~ 3\.65mins \~ 200s) we experienced.


***While a better rate limiting implementation (e.g. based on the [generic cell rate algorithm](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm)) might make more optimal use of Open AI API resources, the request latency will ultimately be limited by our token limits. We could only use the first N tokens, with N selected based on a limit which would ensure the full request limits of 3500/min can be exploited i.e. 90000/3500 \~25 tokens. This was unlikely to be sufficient to establish mentioned technologies on sentiment in our examples however.***


### Extraction at insert time [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#extraction-at-insert-time)


Given rate limiting and latency, a more preferable means to using the API for querying is to assign a sentiment column at the time of data insertion. With its pool of commands, the Python function is more suited for this type of batch processing. Below, we extract a sentiment when loading rows via an `INSERT INTO`. In this example, we insert all ClickHouse\-related rows into a dedicated table computing a sentiment column for each. This type of processing is ideal as new rows are inserted, with the Hacker News dataset receiving about 8\-10 new rows per minute. Once the column is assigned we enjoy ClickHouse query speeds on our sentiment column, without needing to make API requests.



```
INSERT INTO hackernews_v2 SELECT
	*,
	sentiment_p(text) AS sentiment
FROM hackernews
WHERE (text LIKE '%ClickHouse%') OR (title LIKE '%ClickHouse%')

0 rows in set. Elapsed: 185.452 sec. Processed 37.17 million rows, 13.54 GB (200.44 thousand rows/s., 73.00 MB/s.)

SELECT count(), sentiment
FROM hackernews_v2
GROUP BY sentiment

┌─count()─┬─sentiment─┐
│ 	193 │ NEGATIVE  │
│ 	850 │ POSITIVE  │
│ 	634 │ NEUTRAL   │
└─────────┴───────────┘

3 rows in set. Elapsed: 0.003 sec. Processed 1.68 thousand rows, 1.68 KB (531.10 thousand rows/s., 531.10 KB/s.)
Peak memory usage: 72.90 KiB.

```

## Extracting structure [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#extracting-structure)


For completeness, let's also convert our earlier OpenAI request to extract technologies from our post. The bash Python is shown below.



```
#!/usr/bin/python3
import sys
import openai
from tenacity import (
   retry,
   stop_after_attempt,
   wait_random_exponential,
)

openai.api_key = "<INSERT>"
request_timeout = 3

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(20))
def completion_with_backoff(**kwargs):
   return openai.ChatCompletion.create(**kwargs)

def extract_topics(text):
   if text == "":
       return ""
   messages = [{
                   "role": "system",
                   "content": "You are an AI language model trained to extract entities from Hacker News forum comments."},
               {
                   "role": "user",
                   "content": f"From the following text extract the technologies mentioned as a comma separated list with no spaces. Return an empty string if there are no technologies: {text}"
               }]
   try:
       response = completion_with_backoff(model="gpt-3.5-turbo", messages=messages, max_tokens=30, temperature=0,
                                          request_timeout=request_timeout)
       return response.choices[0].message.content.strip()
   except Exception as e:
       return f"ERROR - {e}"

for size in sys.stdin:
   # collect a batch for performance
   for row in range(0, int(size)):
       print(",".join([tech.strip() for tech in extract_topics(sys.stdin.readline().strip()).split(",")]))
   sys.stdout.flush()

```

After configuring this function using the same parameters as the sentiment UDF, except with the name `extract_techs`, we can identify the top technologies mentioned with ClickHouse on Hacker News.



```
WITH results AS (
   	 SELECT extract_techs(text) as techs
   	 FROM hackernews
   	 WHERE (text LIKE '%ClickHouse%') OR (title LIKE '%ClickHouse%')
)
SELECT
    arrayJoin(splitByChar(',', techs)) AS tech,
    count() AS c
FROM results
GROUP BY tech
HAVING tech NOT ILIKE '%ClickHouse%' AND tech != ''
ORDER BY c DESC
LIMIT 5

┌─tech────────┬───c─┐
│ Postgres	│  78 │
│ PostgreSQL  │  65 │
│ SQL     	│  63 │
│ TimescaleDB │  54 │
│ MySQL   	│  51 │
└─────────────┴─────┘

5 rows in set. Elapsed: 211.358 sec. Processed 37.17 million rows, 13.28 GB (175.87 thousand rows/s., 62.85 MB/s.)
Peak memory usage: 931.95 MiB.

```

## Conclusion [\#](/blog/clickhouse-open-ai-user-defined-functions-udfs#conclusion)


This blog post has shown how ClickHouse can be integrated directly with model providers to enrich and add structure to existing data, using UDFs. While we have used OpenAI for our examples, similar “plug and play” model services should be equivalently simple to integrate.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
