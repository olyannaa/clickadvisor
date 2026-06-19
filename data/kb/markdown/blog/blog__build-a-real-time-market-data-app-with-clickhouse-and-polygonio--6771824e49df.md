# Build a real\-time market data app with ClickHouse and Massive


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Build a real\-time market data app with ClickHouse and Massive

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Jul 1, 2025 · 14 minutes readReal\-time tick data applications are a classic example of real\-time analytics. Like tracking user behavior in web apps or monitoring metrics from IoT devices, they involve high\-frequency event streams that need to be ingested, stored, and queried with low latency.


In financial markets, the difference is the urgency. Even a few seconds of delay can turn a profitable trade into a loss. Every trade and quote update generates a new [tick](https://en.wikipedia.org/wiki/Tick_size), and these can number in the thousands per second across multiple symbols.


ClickHouse is a strong fit for this type of workload. It handles high\-frequency inserts, time\-based queries, and low latency queries. Built\-in compression helps reduce storage overhead, even with billions of rows per symbol. Materialized views can be used to pre\-aggregate or reorganize data as it's written, optimizing query performance without needing a separate processing layer.


In this post, we'll walk through how to build a real\-time tick data application using [Massive](https://massive.com/) to access market data and ClickHouse to store and query ticks in real time. We'll put that together using NodeJS for the backend operation and React for the live visualization. Let's dive in.


## What is a tick? [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#what-is-a-tick)


Before we begin, it helps to understand what a quote is and what a trade is. A quote represents the current prices at which market participants are willing to buy or sell a security. Specifically, it includes the best bid (the highest price someone is willing to pay) and the best ask (the lowest price someone is willing to sell for). These are continuously updated as new orders enter or exit the market.




| sym | bx | bp | bs | ax | ap | as | c | i | t | q | z | inserted\_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPY | 12 | 602\.73 | 2 | 11 | 602\.74 | 6 | 1 | \[1,93] | 1749583478206 | 63152225 | NYSE | 1749583479396 |


A trade, on the other hand, is an actual transaction between a buyer and a seller. It occurs when someone agrees to the current ask or bid price and an order is matched and executed. Trades are recorded with the executed price, the size of the trade, and a timestamp.




| sym | i | x | p | s | c | t | q | z | trfi | trft | inserted\_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPY | 52983525034825 | 11 | 607\.26 | 1 | \[12,37] | 1750842255972 | 22126 | NYSE | 0 | 0 | 1750842257842 |


Tick data typically comes in two streams. One contains quote updates, and the other contains trade executions. Both are essential for understanding market behavior, but they serve different purposes in analysis and strategy development.


## Access to real\-time market data [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#access-to-real-time-market-data)


Now we understand the type of data we're going to ingest, let's have a look at how to access it. We first need to find and subscribe to a stock market API. There are many available, the one we picked to build this demo is [Massive](https://massive.com/). Their paid plan provides an unlimited call to their API, access to real\-time data and support for Web sockets. 


[WebSockets](https://en.wikipedia.org/wiki/WebSocket) are essential for streaming market data because they eliminate the latency and overhead of polling REST APIs. Instead of establishing new connections for each data request and potentially missing ticks between calls, WebSockets maintain a persistent connection that pushes data the moment it's available which is critical for high\-frequency market data where milliseconds matter.


Starting to ingest data using [Massive](https://massive.com/) API is fairly straightforward, simply establish a connection with the /stocks endpoint, authenticate using your Massive API key and start processing messages.


Below is a code snippet implementation using NodeJS.



```

```
1this.authMsg = JSON.stringify({
2  action: "auth",
3  params: process.env.MASSIVE_API_KEY,
4});     
5
6this.ws = new WebSocket("wss://socket.polygon.io/stocks");
7
8this.ws.on("open", () => {
9  console.log("WebSocket connected");
10  this.isConnected = true;
11  this.reconnectAttempts = 0;
12  this.lastMessageTime = Date.now();
13  this.connectionStartTime = Date.now();
14  this.statusMessage = "Connected - Authenticating...";
15  this.logConnectionEvent("connected");
16  this.ws.send(this.authMsg);
17});
18
19this.ws.on("message", (data) => {
20  if (!this.isPaused) {
21    this.handleMessage(data);
22  }
23});
```

```

## Ingesting Data into ClickHouse [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#ingesting-data-into-clickhouse)


### Modeling Tick Data in ClickHouse [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#modeling-tick-data-in-clickhouse)


Tick data is relatively straightforward to model since it consists of just two event types, one for [trade](https://polygon.io/docs/websocket/stocks/trades) and another one for [quote](https://polygon.io/docs/websocket/stocks/quotes), each with a small set of mostly numeric fields. Below is the DDL for creating two separate tables.



```

```
1CREATE TABLE quotes
2(
3    `sym` LowCardinality(String),
4    `bx` UInt8,
5    `bp` Float64,
6    `bs` UInt64,
7    `ax` UInt8,
8    `ap` Float64,
9    `as` UInt64,
10    `c` UInt8,
11    `i` Array(UInt8),
12    `t` UInt64,
13    `q` UInt64,
14    `z` Enum8('NYSE' = 1, 'AMEX' = 2, 'Nasdaq' = 3),
15    `inserted_at` UInt64 DEFAULT toUnixTimestamp64Milli(now64())
16)
17ORDER BY (sym, t - (t % 60000));
18
19CREATE TABLE trades
20(
21    `sym` LowCardinality(String),
22    `i` String,
23    `x` UInt8,
24    `p` Float64,
25    `s` UInt64,
26    `c` Array(UInt8),
27    `t` UInt64,
28    `q` UInt64,
29    `z` Enum8('NYSE' = 1, 'AMEX' = 2, 'Nasdaq' = 3),
30    `trfi` UInt64,
31    `trft` UInt64,
32    `inserted_at` UInt64 DEFAULT toUnixTimestamp64Milli(now64())
33)
34ORDER BY (sym, t - (t % 60000));
```

```

The data volume can grow quickly.


For example, tracking trades on the Nasdaq alone can generate [around 50 million records per day](https://www.nasdaqtrader.com/Trader.aspx?id=DailyMarketSummary). Choosing an [effective order key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key) is essential for performance. In this case, rows are ordered first by sym (the stock symbol), grouping all events for the same symbol. Within each symbol group, rows are ordered by `t - (t % 60000)`, which creates 1\-minute time buckets. This approach works well in our case, as we aggregate data by symbol to generate the visualization. Grouping by minute improves the efficiency of time\-based filtering and aggregation.


### Ingestion strategy [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#ingestion-strategy)


There are several ways to design an ingestion pipeline for this type of application, including using a message queue like [Kafka](https://kafka.apache.org/). However, to minimize latency, it's often better to keep the system simple and push data directly from the WebSocket connection into ClickHouse when possible.


Once that setup is in place, the next step is to choose the [right ingestion method](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy). ClickHouse supports both synchronous and asynchronous inserts.


With synchronous ingestion, data is batched on the client side before being sent. The [batch size](https://clickhouse.com/docs/optimize/bulk-inserts) should strike a balance between memory usage, latency, and system overhead. Larger batches reduce the number of insert requests and improve throughput, but they can increase memory usage and delay individual records. Smaller batches reduce memory pressure but may create more load on ClickHouse by generating too many small data parts.


With asynchronous ingestion, data is sent to ClickHouse continuously, and batching is handled internally. Incoming records are first written to an in\-memory buffer, which is then flushed to storage based on configurable thresholds. This method is useful when client\-side batching isn't practical, such as when data comes from many small clients.


In our case, synchronous ingestion is a better fit. Since there's only one client pushing data from the WebSocket API, batching can be managed on the client side for better control over performance and resource usage.


Code snippet to ingest data from the NodeJS application.



```

```
1handleMessage(data) {
2    try { 
3        const trades = payload.filter((row) => row.ev === "T").map(({ ev, ...fields }) => fields);
4        const quotes = payload.filter((row) => row.ev === "Q").map(({ ev, ...fields }) => fields);
5        this.addToBatch(trades, "trades");
6        this.addToBatch(quotes, "quotes");
7} catch (error) {
8        console.error("Error handling message:", error);
9        console.error("Message data:", data.toString().substring(0, 200));
10}
11
12addToBatch(rows, type) {
13    if (rows.length === 0) return;
14    const batch = type === "trades" ? this.tradesBatch : this.quotesBatch;
15    batch.push(...rows);
16    if (batch.length >= this.maxBatchSize) {
17        this.flushBatch(type);
18    }
19 }
20
21flushBatch(type) {
22    const batch = type === "trades" ? this.tradesBatch : this.quotesBatch;
23    if (batch.length === 0) return;
24    const dataToInsert = [...batch];
25    if (type === "trades") {
26         this.tradesBatch = [];
27    } else {
28         this.quotesBatch = [];
29    }
30    await this.client.insert({
31      table: table,
32      values: data,
33      format: "JSONEachRow",
34    });
35 }
```

```

### Visualize live market data [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#visualize-live-market-data)


Once the data is stored in ClickHouse, building the visualization layer is straightforward. The main challenge lies in writing the right SQL queries. Let’s have a look on how to achieve this.
We’ll focus on the queries needed to power two key visualizations.
The first is a real\-time table that updates continuously to show the latest trading data for a specific stock.


![tick-table.png](/uploads/tick_table_f21d502995.png)
To build this visualization, one query is enough, the data can be formatted using ClickHouse's powerful SQL query language and custom functions.



```

```
1WITH
2    {syms: Array(String)} as symbols,
3    toDate(now('America/New_York')) AS curr_day,
4    trades_info AS
5    (
6        SELECT
7            sym,
8            argMax(p, t) AS last_price,
9            round(((last_price - argMinIf(p, t, fromUnixTimestamp64Milli(t, 'America/New_York') >= curr_day)) / argMinIf(p, t, fromUnixTimestamp64Milli(t, 'America/New_York') >= curr_day)) * 100, 2) AS change_pct,
10            sum(s) AS total_volume,
11            max(t) AS latest_t
12        FROM trades
13        WHERE (toDate(fromUnixTimestamp64Milli(t, 'America/New_York')) = curr_day) AND (sym IN (symbols))
14        GROUP BY sym
15        ORDER BY sym ASC
16    ),
17    quotes_info AS
18    (
19        SELECT
20            sym,
21            argMax(bp, t) AS bid,
22            argMax(ap, t) AS ask,
23            max(t) AS latest_t
24        FROM quotes
25        WHERE (toDate(fromUnixTimestamp64Milli(t, 'America/New_York')) = curr_day) AND (sym IN (symbols))
26        GROUP BY sym
27        ORDER BY sym ASC
28    )
29SELECT
30    t.sym AS ticker,
31    t.last_price AS last,
32    q.bid AS bid,
33    q.ask AS ask,
34    t.change_pct AS change,
35    t.total_volume AS volume
36FROM trades_info AS t
37LEFT JOIN quotes_info AS q ON t.sym = q.sym;
```

```

Let's break down what this query does.


First, it defines two variables: `symbols`, which holds the list of stock tickers to analyze, and `curr_day`, which captures the current date in the New York timezone.


The query then retrieves trade data, including:


- `last_price`: The most recent trade price, using `argMax(p, t)` to get the price at the latest timestamp
- `change_pct`: The percentage change from the day's opening price.
- `total_volume`: Total volume for the day


It also fetches quote data:


- `bid`: Most recent bid price using `argMax(bp, t)`
- `ask`: Most recent ask price using `argMax(ap, t)`


Finally, the trade and quote results are joined to produce the final output.




| ticker | last | bid | ask | change | volume |
| --- | --- | --- | --- | --- | --- |
| NVDA | 151\.2099 | 151\.2 | 151\.21 | 2\.17 | 65269276 |


The second visualization we’re going to analyze is a candlestick visualization that shows the price evolution and volume for a given stock.


![tick-candlestick.png](/uploads/tick_candlestick_d9e922fa60.png)
Let’s have a look at the SQL query to power this visualization.



```

```
1SELECT
2 toUnixTimestamp64Milli(toDateTime64(toStartOfInterval(fromUnixTimestamp64Milli(t), interval 2 minute), 3)) as x,
3    argMin(p, t) as o,
4    max(p) as h,
5    min(p) as l,
6    argMax(p, t) as c,
7    sum(s) as v
8FROM trades
9WHERE x > toUnixTimestamp64Milli(now64() - interval 1 hour) AND sym = {sym: String}
10GROUP BY x 
11ORDER BY x ASC;
```

```

This query is simpler, as it only computes the trading volume, along with the highest and lowest prices, over a specified time window.


To visualize the query result, we use [click\-ui](https://github.com/ClickHouse/click-ui) components for the table display and [Chart.js](https://www.chartjs.org/) for the candlestick visualization.


## Scaling and practical tips [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#scaling-and-practical-tips)


Handling high\-frequency market data in production requires more than just a fast database. The following tips and techniques help ensure your system remains performant and reliable as data volume grows.


### Scaling ingestion [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#scaling-ingestion)


When dealing with tick\-level data across many symbols, sustained throughput can easily exceed tens of thousands of records per second.


To handle this there are different things to look for: 


- Use [client\-side batching](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy#batch-inserts-if-synchronous) with insert sizes optimized for your system's memory and latency constraints.
- Use [compression](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy#use-compression): Compressing insert data reduces the size of the payload sent over the network, minimizing bandwidth usage and accelerating transmission.
- Monitor the number of parts created in ClickHouse to prevent excessive merging. This [blog](https://clickhouse.com/blog/monitoring-asynchronous-data-inserts-in-clickhouse#part-creations) talks about asynchronous insert, but the part creation section can be applied for a synchronous ingestion. You can also use [advanced dashboards](https://clickhouse.com/docs/operations/monitoring) to [monitor](https://clickhouse.com/blog/common-issues-you-can-solve-using-advanced-monitoring-dashboards#unbatched-inserts) the number of data parts.
- [Massive](https://massive.com/) also provides [performance tips](https://polygon.io/docs/websocket/quickstart#performance-&-latency-considerations) to handle high volume data consumption.


### Monitoring ingest latency [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#monitoring-ingest-latency)


As discussed earlier, having the freshest data is critical for a financial application. So it does make sense to monitor it.


You can easily calculate and track the difference between the event timestamp (when the tick occurred) and the ingestion timestamp (when it was stored). This “ingest delay” is key to detecting backpressure or performance bottlenecks.



```

```
1SELECT
2    sym,
3    count() AS trade_count,
4    argMax(inserted_at, t) - argMax(t, t) AS ingest_latency
5FROM trades
6GROUP BY sym
7ORDER BY trade_count DESC
8LIMIT 100;
```

```

Visualizing this metric in a dashboard helps you catch slowdowns early.


### Take advantage of materialized views [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#take-advantage-of-materialized-views)


[Materialized views](https://clickhouse.com/docs/materialized-views) are useful when you want to pre\-aggregate data as it arrives. This helps optimize specific query patterns that rely on time\-based summaries. A typical example is computing [OHLCV](https://en.wikipedia.org/wiki/Open-high-low-close_chart) (Open, High, Low, Close, Volume) metrics for financial data at fixed intervals, such as 1\-minute windows. By generating these aggregates during ingestion, you can serve results quickly without recalculating them each time.


Start by creating a destination table to store the 1\-minute OHLCV aggregates. This table will receive the output from the materialized view and provide a structured way to access precomputed results.



```

```
1-- Create destination table
2CREATE TABLE trades_1min_ohlcv
3(
4    `sym` LowCardinality(String),
5    `z` Enum8('NYSE' = 1, 'AMEX' = 2, 'Nasdaq' = 3),
6    `minute_bucket_ms` UInt64,
7    `open_price_state` AggregateFunction(argMin, Float64, UInt64),
8    `high_price_state` AggregateFunction(max, Float64),
9    `low_price_state` AggregateFunction(min, Float64),
10    `close_price_state` AggregateFunction(argMax, Float64, UInt64),
11    `volume_state` AggregateFunction(sum, UInt64),
12    `trade_count_state` AggregateFunction(count)
13)
14ENGINE = SummingMergeTree
15ORDER BY (sym, minute_bucket_ms);
```

```

The next step is to create the materialized view.



```

```
1-- Create view
2CREATE MATERIALIZED VIEW trades_1min_ohlcv_mv TO trades_1min_ohlcv
3AS SELECT
4    sym,
5    z,
6    intDiv(t, 60000) * 60000 AS minute_bucket_ms,
7    argMinState(p, t) AS open_price_state,
8    maxState(p) AS high_price_state,
9    minState(p) AS low_price_state,
10    argMaxState(p, t) AS close_price_state,
11    sumState(s) AS volume_state,
12    countState() AS trade_count_state
13FROM trades
14GROUP BY
15    sym,
16    z,
17    minute_bucket_ms;
```

```

Now as each trade insert hits the trades table, the materialized view automatically processes it and updates the corresponding 1\-minute bucket in the destination table.


To view the data, execute this query.



```

```
1-- Query the table
2SELECT
3    sym,
4    z,
5    minute_bucket_ms,
6    fromUnixTimestamp64Milli(minute_bucket_ms) as minute_timestamp,
7    argMinMerge(open_price_state) AS open_price,
8    maxMerge(high_price_state) AS high_price,
9    minMerge(low_price_state) AS low_price,
10    argMaxMerge(close_price_state) AS close_price,
11    sumMerge(volume_state) AS volume,
12    countMerge(trade_count_state) AS trade_count
13FROM trades_1min_ohlcv
14GROUP BY sym, z, minute_bucket_ms
15ORDER BY sym, z, minute_bucket_ms;
```

```

## Conclusion [\#](/blog/build-a-real-time-market-data-app-with-clickhouse-and-polygonio#conclusion)


In this post, we explored how to build a real\-time tick data application using Massive for market data and ClickHouse for fast ingestion and querying. We covered how to stream and structure tick data, manage ingestion performance, and build efficient queries and visualizations.


In this Github [repository](https://github.com/ClickHouse/examples/tree/main/stock-data-demo), you will find a working example of this using React for the visualization layer. While this is a simple example, the same principles would apply when building a production ready application at scale.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
