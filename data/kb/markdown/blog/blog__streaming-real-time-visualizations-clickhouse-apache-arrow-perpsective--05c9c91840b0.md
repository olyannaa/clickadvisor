# Streaming Real\-Time Visualizations with ClickHouse, Apache Arrow and Perspective


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Streaming Real\-Time Visualizations with ClickHouse, Apache Arrow and Perspective

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Oct 2, 2024 · 17 minutes readAs a company founded in open\-source, we love to promote other OSS projects that impress us either because they look technically impressive, resonate with our obsession with performance, or we feel will genuinely help our users. On discovering the UI library [Perspective](https://perspective.finos.org/), we realized this ticked all of these requirements, allowing users to build truly [real\-time visualizations](https://clickhouse.com/engineering-resources/real-time-data-visualization) on top of ClickHouse data! Keen to see if the library could be easily integrated with ClickHouse, we've built a simple demo application that provides rich visualization capabilities by streaming Forex data using Apache Arrow straight to the browser, all in a little more than 100 lines of code!


![forex_demo.png](/uploads/forex_demo_f7a306db18.png)
The example should be easily adapted and allow users to visualize any dataset as it is streamed into ClickHouse. Let us know your thoughts, and shout out to Perspective for building such a cool library!


If you want to run the [example perspective app](https://github.com/ClickHouse/perspective-forex), we've provided a ClickHouse instance for you to use. Alternatively, play with a hosted version [here](https://perspective-clickhouse.vercel.app/). Finally, we'll explore how fast we can stream data and why the current approach isn't ideal, but some ideas for future ClickHouse features that will address these deficiencies.


## What is Perspective? [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#what-is-perspective)


The **[Perspective Library](https://perspective.finos.org/)** is a high\-performance data analytics and visualization tool designed to handle real\-time and streaming datasets efficiently. It offers interactive and customizable visualizations, such as heat maps, line charts, and tree maps. Like ClickHouse, Perspective is built with performance in mind. Its core is written in Rust and C\+\+ and compiled into WebAssembly. This enables it to process millions of data points in the browser and respond to continuous data streams.


Beyond simple rendering, Perspective offers fast operations for pivoting, filtering, and aggregating datasets in the browser or server side and performing expressions [using ExprTK](https://www.partow.net/programming/exprtk/index.html). While this isn't designed for the petabyte scale seen in ClickHouse, it allows a 2nd level of data transformation on rows delivered to the client \- reducing the need for further queries if the required data is already available and requires only a simple transformation to achieve the desired visual.


This makes it ideal for ClickHouse\-powered applications where real\-time insights and smooth interactivity are critical. With its support for both Python and JavaScript, it can be integrated into both backend analytics pipelines and web\-based interfaces.


While Perspective complements ClickHouse perfectly for standard visualization needs, we were particularly interested in its ability to handle streaming data, maintaining a constant memory overhead by only retaining the latest N rows. We were curious how easy it would be to tail a continuously updated dataset, loading only the new delta into the browser where only the latest subset of points were retained and summarized.



> While we focus on the javascript integration with Perspective, users can also use Perspective in Python with a JupyterLab widget and client library for interactive data analysis in a notebook.


## ClickHouse for streaming data? [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#clickhouse-for-streaming-data)


While ClickHouse is not a stream processing engine but rather an OLAP database, it has features that provide functionality such as [Incremental Materialized views](https://clickhouse.com/docs/en/materialized-view), which allow much of the same functionality seen in technologies such as Apache Flink. These views are triggers that execute a query (which can include aggregates) on a block of data as it is inserted, storing the results in a different table for later use.


![mv_simple.png](/uploads/mv_simple_31f168288b.png)
While many simple stream processing capabilities can replicate the simpler transforms and aggregates people perform in engines such as Flink to simplify architectures, we acknowledge these technologies work in unison, with the latter providing additional capabilities for advanced cases. When used for stream processing, ClickHouse has the added benefit of efficiently storing all of your data \- allowing historical data to be queried.


In our case, we wanted to attempt streaming the latest rows in ClickHouse to Perspective for rendering. For our example, we'll crudely simulate the requirement to visualize forex trades as they arrive in ClickHouse. This will likely be most useful to a trader, with rows persisted for future historical analysis if required.


## Dataset \- Forex [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#dataset---forex)


For our example, we'll use a forex dataset. Forex trading is the trading of currencies from different countries against each other, where a trader can either buy a base currency with a quote currency from the broker (at an `ask price`) or sell a base currency and receive the quote in return (at the `bid` price). The dataset tracks the price changes of each currency pair over time—what's important is that they change quickly!


For those not familiar with Forex trading, we recommend reading a [short section from this earlier post](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3#a-little-bit-about-forex), where we summarize the concepts.


The full dataset, available in a [public S3 bucket](https://github.com/ClickHouse/perspective-forex?tab=readme-ov-file#dataset), was downloaded from <www.histdata.com> and covers the years 2000 to 2022\. It has 11\.5 billion rows and 66 currency pairs (around 600GB decompressed).


While simple, the schema for this dataset is ideal for our example. Each row represents a tick. Timestamps here are to ms granularity, with columns indicating the base and quote currency and the ask and bid quotes.



```
CREATE TABLE forex
(
   `datetime` DateTime64(3),
   `bid` Decimal(11, 5),
   `ask` Decimal(11, 5),
   `base` LowCardinality(String),
   `quote` LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (datetime, base, quote)

```


> Ticks record when the price of a stock or commodity changes by a predetermined amount or fractional change, i.e., a tick occurs when the price moves up or down by a specific amount or fractional change. A tick in Forex will happen when the bid or quote price changes.


Since a streaming feed for Forex is not available, we'll simulate this by loading a year's worth of data from parquet format and offsetting it to the current time. You can replicate this dataset if they wish to try the app on a local instance \- see [here](https://github.com/ClickHouse/perspective-forex?tab=readme-ov-file#dataset).



> Note that tick data does not represent an actual trade/exchange. The number of trades/exchanges per second is significantly higher! Nor does it capture the agreed price or the volume of the currency exchanged (logically 0 in the source data and hence ignored). Rather, it simply marks when the prices change by a unit known as [the pip](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3#pips-and-ticks).


## Connecting Perspective to ClickHouse with Arrow [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#connecting-perspective-to-clickhouse-with-arrow)


### Some boilerplate [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#some-boilerplate)


Setting up and configuring perspective requires [importing several packages](https://github.com/ClickHouse/perspective-forex/blob/main/index.html#L6-L8) with a little boilerplate code. The [public examples](https://perspective.finos.org/examples/) are excellent, but in summary, we create a worker and table. A worker represents a web worker process that offloads heavy operations, such as updates, from the browser's main renderer thread \- ensuring that the interface remains responsive, even when streaming large real\-time datasets. The table represents the primary data structure that can be updated dynamically with new data.



```
import perspective from "https://cdn.jsdelivr.net/npm/@finos/perspective@3.0.0/dist/cdn/perspective.js";
const forex_worker = await perspective.worker();
// fetch some rows... 
const forex_table = await market_worker.table(rows, { limit: 20000 })

```


> We've kept our example as simple as possible, importing the package via CDN and avoiding any dependencies apart from perspective. Users integrating Perspective into existing applications or building production applications are recommended to explore the examples for [common JS frameworks and build tooling](https://perspective.finos.org/docs/js/#installation).


Perspective provides a number of [deployment models](https://perspective.finos.org/docs/server/)) that determine how data is loaded and bound, each with its respective pros and cons. For our example, we'll use the [client\-only](https://perspective.finos.org/docs/server/#client-only) approach, with the data streamed to the browser, a few lines of Javascript fetching the data from ClickHouse over HTTP, and the WebAssembly library running all calculations and UI interactions.


### Streaming latest trades [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#streaming-latest-trades)


When creating the table, as shown below, we limit the number of rows retained to restrict the memory overhead.



```
const forex_table = await market_worker.table(rows, { limit: 20000 });

```

For our example, we'll constantly add new rows to this table as new trades become available, relying on Perspective to retain only the latest 20k.


As of the time of writing, ClickHouse doesn't support web sockets or a means to stream changed rows to a client. We, therefore, use a polling approach to fetch the latest rows over HTTP. With Perspective preferring data in Apache Arrow format, we exploit ClickHouse's ability to return data in this format, which has the added benefit of minimizing the data transferred.


Forex ticks occur quickly, with up to 35 per second for the highest volume currency pairs. We want to fetch these as quickly as possible \- ideally every 30\-50ms, to ensure all values are visualized. Our query, therefore, needs to execute quickly, with each connected client issuing 10s of queries per second. Across all connected clients, we'd expect 100s of queries per second \- something ClickHouse, contrary to some misconceptions, is comfortable serving.


Our query simply filters on the timestamp of the event, which is the first entry in our primary key [thus ensuring filtering is optimized](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes). As all clients are issuing requests for approximately the same time period i.e. now, and monotonically increasing, our queries should be cache friendly. Testing showed that while our query executes in less than 10ms even on the full 11 billion row dataset, the HTTP round trip time to a ClickHouse instance is optimistically (same region) 20\-30ms. We therefore just use a simple sliding window from the current time to the previous fetch time. This is continuously executed, retrieving rows as quickly as ClickHouse can serve them.


![sliding_window.png](/uploads/sliding_window_a19e99b1cf.png)
The simplified diagram above assumes that each query execution takes exactly 50ms. Our query fetches all of the columns as well as computing the [spread](https://www.babypips.com/learn/forex/what-is-a-spread-in-forex-trading) (difference between the `ask` and `bid`). Ideally, we'd also like to show the change in the current bid \- this is useful in trading. To ensure the first values for each pair have the correct change value, we need to make sure we have the last price outside of the current window for each currency pair. For this, we query slightly more data than we return, as shown above and in our final query below.



```
SELECT *
FROM
(
   SELECT
       concat(base, '.', quote) AS base_quote,
       datetime AS last_update,
       bid,
       ask,
       ask - bid AS spread,
       ask - any(ask) OVER (PARTITION BY base_quote ORDER BY base_quote ASC, datetime ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS chg
   FROM forex
   WHERE datetime > {prev_lower_bound:DateTime64(3)} AND datetime <= {upper_bound:DateTime64(3)}
   ORDER BY
       base_quote ASC,
       datetime ASC
)
WHERE datetime > {lower_bound:DateTime64(3)} AND datetime <= {upper_bound:DateTime64(3)}
ORDER BY last_update ASC

┌─base_quote─┬─────────────last_update─┬─────bid─┬────────ask─┬──spread─┬──────chg─┐
│ AUD.CAD    │ 2024-09-19 13:25:30.840 │ 0.97922 │    0.97972 │  0.0005 │ -0.00002 │
│ XAG.USD    │ 2024-09-19 13:25:30.840 │  17.858 │   17.90299 │ 0.04499 │  0.00499 │
│ AUD.JPY    │ 2024-09-19 13:25:30.840 │   97.28 │      97.31 │    0.03 │   -0.001 │
│ AUD.NZD    │ 2024-09-19 13:25:30.840 │ 1.09886 │    1.09946 │  0.0006 │  0.00004 │
...
│ EUR.AUD    │ 2024-09-19 13:25:30.840 │ 1.43734 │    1.43774 │  0.0004 │ -0.00002 │
└────────────┴─────────────────────────┴─────────┴────────────┴─────────┴──────────┘

25 rows in set. Elapsed: 0.012 sec. Processed 24.57 thousand rows, 638.82 KB (2.11 million rows/s., 54.98 MB/s.)
Peak memory usage: 5.10 MiB.

```


> Note how we apply a time range filter to the argMax so we don't need to perform a complete scan over all rows where the time \< lower bound (rather `lower bound - 5 mins < time < lower bound`).


Our final function for fetching the next rows can be found [here](https://github.com/ClickHouse/perspective-forex/blob/ffc48caf4b7395f6d02b12f9920b8754f8035d86/index.js#L47-L51). This uses the above query, requesting the data in Arrow format and reading the response into an ArrayBuffer as required by Perspective.



> We don't use the [ClickHouse JS library,](https://clickhouse.com/docs/en/integrations/javascript) mainly to minimize dependencies but also because our code is so simple. We recommend that complex applications use this.


## Initial application [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#initial-application)


Our application, shown below, invokes the above function to fetch rows [in a continuous loop](https://github.com/ClickHouse/perspective-forex/blob/ffc48caf4b7395f6d02b12f9920b8754f8035d86/index.js#L72):


![simple_forex.gif](/uploads/simple_forex_5b63c6b76d.gif)
Our [loop computes also the average fetch time](https://github.com/ClickHouse/perspective-forex/blob/ffc48caf4b7395f6d02b12f9920b8754f8035d86/index.js#L83-L85) (averaged across the latest 10 requests). The performance here will depend on how close you are to the ClickHouse cluster, with the latency dominated by the HTTP fetch time. With reasonable proximity to a ClickHouse service, we were able to reduce this to about 30ms.


While we display the datagrid for the out of the box visualization, users can easily modify the visualization type and apply transformations. In the example below, we switch to a scatter visualization to plot the bid and ask prices for the `EUR-GBP` currency pair.


![forex_simple_line.gif](/uploads/forex_simple_line_78fbb99645.gif)
Curious to test the CPU load for this, we initiated 20 concurrent clients resulting in almost 200 queries per second. Even with this load, ClickHouse uses less than 2 cores.


![cpu.png](/uploads/cpu_df004dba1c.png)
### Not quite streaming, yet [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#not-quite-streaming-yet)


In reality, the above, in a real scenario, could potentially miss rows if tracking the current time due to ClickHouse's eventual consistency model. Even though this can be mitigated with [careful configuration](https://clickhouse.com/docs/en/operations/settings/settings#settings-select_sequential_consistency), it's suboptimal. Rows are also likely to incur some insert latency, so we'd want to offset our query from the current time rather than just using `now()`.


We acknowledge these deficiencies and have begun [exploring the concept of streaming queries](https://github.com/ClickHouse/ClickHouse/pull/63312), which would reliably only return new rows as they match a specified query. This would remove the need for polling, with the client simply opening an HTTP connection with the query and receiving rows as they arrive.


## A speed test \- with Arrow Stream [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#a-speed-test---with-arrow-stream)


While following the ticks in real time is probably the most useful, we were curious to see how fast Perspective could actually handle the data. For this we wanted to stream the entire dataset to Perspective in ascending date order, again only keeping the last N data points. Our query, in this case, becomes:



```
SELECT concat(base, '.', quote) AS base_quote,
	datetime AS last_update,
	CAST(bid, 'Float32') AS bid,
	CAST(ask, 'Float32') AS ask,
	ask - bid AS spread
FROM forex
ORDER BY datetime ASC
FORMAT ArrowStream
SETTINGS output_format_arrow_compression_method='none'

```


> Note how we've dropped the computation of the change per currency pair. This requires a window function that doesn't exploit the [optimize\_read\_in\_order](https://clickhouse.com/docs/en/operations/settings/settings#optimize_read_in_order) and prevents an immediate stream of the results.


For this, you'll notice we don't just use Arrow format. This would require us to download the entire dataset [\>60GB compressed in ClickHouse](https://sql.clickhouse.com?query_id=6B6MXXER1XG8J2QVTY3NMA) and convert it to a table for Perspective. Even in Arrow format, this is a little large for a browser!


Instead we exploit ClickHouse's support for the Arrow Stream format, reading the data in chunks and passing this to perspective. While previously we could do all the work without a dependency, for this we need the [Arrow js lib](https://arrow.apache.org/docs/js/). While this makes consuming Arrow files trivial, to support streaming we need a bit more JS. Our final function which streams the entire dataset a batch at a time is shown below.



```
async function get_all_rows(table, lower_bound) {
   const view = await table.view({ // Create a view with aggregation to get the maximum datetime value
       columns: ["last_update"], // Column you're interested in
       aggregates: { last_update: "max" } // Aggregate by the maximum of datetime
   });
   const response = await fetch(clickhouse_url, {
       method: 'POST',
       body: `SELECT concat(base, '.', quote) AS base_quote, datetime AS last_update, bid::Float32 as bid,  ask::Float32 as ask, ask - bid AS spread
              FROM forex WHERE datetime > ${lower_bound}::DateTime64(3) ORDER BY datetime ASC FORMAT ArrowStream SETTINGS output_format_arrow_compression_method='none'`,
       headers: { 'Authorization': `Basic ${credentials}` }
   });
   const reader = await RecordBatchReader.from(response);
   await reader.open();
   for await (const recordBatch of reader) {  // Continuously read from the stream
       if (real_time) { // set to false if we want to stop the stream
           await view.delete();
           return;
       }
       const batchTable = new Table(recordBatch); // currently required, see https://github.com/finos/perspective/issues/1157
       const ipcStream = tableToIPC(batchTable, 'stream');
       const bytes = new Uint8Array(ipcStream);
       table.update(bytes);
       const result = await view.to_columns();
       const maxDateTime = result["last_update"][0];
       document.getElementById("last_updated").textContent = `Last updated: ${new Date(maxDateTime).toISOString()}`;
       total_size += (bytes.length);
       document.getElementById("total_download").textContent = `Total Downloaded: ${prettyPrintSize(total_size,2)}`;
   }
}

```

This code could be more efficient than it is \- mainly as Perspective currently [requires an array of bytes](https://github.com/finos/perspective/issues/1157) for the update call. This forces us to convert our batch to a table and stream this to an array. We also use a Perspective view, conceptually similar to a materialized view in ClickHouse \- executing an aggregation on the table data as it's loaded. In this case, we use the view to simply compute the maximum streamed date, which we show in the final UI.


With a little additional code to switch between the earlier "real\-time" polling mode and this "streaming mode," we have our final app. Switching to streaming mode shows the performance of Perspective:


![super_fast_forex.gif](/uploads/super_fast_forex_ab5036cd9d.gif)
The line chart on a currency pair shows how we're able to render thousands of data points per second with at least 25MiB/sec streamed to the browser.


You can play with the final application [here](https://perspective-clickhouse.vercel.app/).


## Conclusion [\#](/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective#conclusion)


We've used this blog to explore a popular open\-source visualization library, Perspective, which has useful applications for ClickHouse with synergies in performance and the ability to handle large volumes of data arriving quickly! Thanks to Apache Arrow, we can integrate ClickHouse with Perspective in only a few lines of JavaScript. In the process, we've also identified some of the limitations of ClickHouse's ability to handle streaming data and highlighted current work we hope will address these.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
