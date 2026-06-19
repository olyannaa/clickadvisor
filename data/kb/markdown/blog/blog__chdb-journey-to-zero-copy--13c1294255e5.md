# The Journey to Zero\-Copy: How chDB Became the Fastest SQL Engine on Pandas DataFrame


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The Journey to Zero\-Copy: How chDB Became the Fastest SQL Engine on Pandas DataFrame

![](/_next/image?url=%2Fuploads%2Fauxten_1e039f7a0e.png&w=96&q=75)Xiaozhe Yu Auxten WangJan 9, 2026 · 11 minutes read## The Problem: A Great Engine Trapped Behind Serialization [\#](/blog/chdb-journey-to-zero-copy#the-problem-a-great-engine-trapped-behind-serialization)


If you've worked with data in Python, you know the drill: Pandas is everywhere. It's the lingua franca of data science, the format that bridges your data loading, cleaning, analysis, and visualization. But when datasets grow beyond a few million rows, Pandas starts to struggle. Single\-threaded execution, memory\-hungry operations, and clunky syntax for complex aggregations become real pain points.


Meanwhile, ClickHouse sits there—the fastest open\-source OLAP engine on the planet—waiting to help. But traditionally, using ClickHouse meant setting up servers, loading data into tables, and managing a whole database infrastructure. Not exactly what you want when you just need to run a quick aggregation on a DataFrame.


That's why we built **chDB**: ClickHouse packaged as a simple Python library. `pip install chdb` and you're done.


But here's the thing—our first version had a dirty secret.


![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_5b17faaafe.jpg)
Every query went through four serialization/deserialization steps. The result? **Almost every query took over 100ms**, regardless of complexity. We had the world's fastest engine, but it was choking on data conversion overhead.


## The Vision: What Users Actually Needed [\#](/blog/chdb-journey-to-zero-copy#the-vision-what-users-actually-needed)


From the user's perspective, what they wanted was simple:



> "I have a DataFrame. I want to run SQL on it. Give me back a DataFrame. Fast."


No temp files. No format conversions. No memory explosions. Just seamless, native integration.


More specifically:


- **DataFrame In, DataFrame Out** — Query any Pandas DataFrame with SQL, get results as a DataFrame
- **Zero Configuration** — No registration, no schema definitions, just reference your variable name in SQL
- **ClickHouse Performance** — Multi\-threaded execution, vectorized processing, all the good stuff
- **Memory Efficient** — Handle datasets larger than RAM through streaming


This is what we set out to build with **chDB v2**.


## What We Built: True Native Integration [\#](/blog/chdb-journey-to-zero-copy#what-we-built-true-native-integration)


After months of work, here's what using chDB looks like today:



```

```
1import pandas as pd
2import chdb
3
4# Your data, wherever it comes from
5the_df = pd.DataFrame({
6    'user_id': range(1_000_000),
7    'category': ['A', 'B', 'C'] * 333334,
8    'value': [i * 0.1 for i in range(1_000_000)]
9})
10
11# SQL on DataFrame — just reference the variable name!
12result = chdb.query("""
13    SELECT category,
14           COUNT(*) as cnt,
15           AVG(value) as avg_val
16    FROM Python(the_df)
17    GROUP BY category
18    ORDER BY cnt DESC
19""", "DataFrame")
20
21print(result)
```

```

That's it. No registration. No temp files. The DataFrame variable `df` is automatically discovered and made available as a table. The result comes back as a DataFrame, ready for your next Pandas operation or visualization.


![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240-1.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_1_ac2e1247c8.jpg)
This was a huge leap—**87x faster** than v1\.0! But we weren't done yet.


## Under the Hood: The Technical Journey [\#](/blog/chdb-journey-to-zero-copy#under-the-hood-the-technical-journey)


### Challenge 1: Automatic DataFrame Discovery [\#](/blog/chdb-journey-to-zero-copy#challenge-1-automatic-dataframe-discovery)


When you write `Python(df)` in your SQL, chDB needs to find that variable in your Python environment. We built an automatic discovery mechanism that:


1. **Searches** for the variable name in local and global scope
2. **Validates** it's actually a Pandas DataFrame
3. **Parses** column names and data types
4. **Wraps** it as a ClickHouse table function


No explicit registration required—just name your DataFrame and use it.


![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240-2.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_2_0b69f97121.jpg)
### Challenge 2: The GIL Problem [\#](/blog/chdb-journey-to-zero-copy#challenge-2-the-gil-problem)


Here's where things got interesting. ClickHouse is a massively parallel engine—it wants to use all your CPU cores. Python's Global Interpreter Lock (GIL) says "one thread at a time, please."


If we called Python's C API for every data access, our multi\-threaded engine would degrade to single\-threaded execution. The solution? **Minimize CPython API calls** and batch all Python interactions before the parallel pipeline starts.


![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240-3.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_3_3647a7a3dc.jpg)
### Challenge 3: Python String Encoding Nightmare [\#](/blog/chdb-journey-to-zero-copy#challenge-3-python-string-encoding-nightmare)


Python's `str` type is... complicated. It could be UTF\-8, UTF\-16, UTF\-32, or something else entirely. Converting to UTF\-8 (what ClickHouse expects) via Python's API? That means acquiring the GIL for every string.


So we did something a bit crazy: **we rewrote Python's string encoding logic in C\+\+**. This let us handle string conversion in parallel, without touching the GIL.


The result? Our test query Q23 (`SELECT * FROM hits WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10`) went from **8\.6 seconds to 0\.56 seconds**—a 15x improvement from this single optimization.



```
┌─────────────────────────────────────────────────────────────────┐
│              String Encoding Performance Impact                 │
│                                                                 │
│   Q23 Query Time (seconds)                                      │
│                                                                 │
│   Python API Encoding:  ████████████████████████████████ 8.6s   │
│   C++ Native Encoding:  ██ 0.56s                                │
│                                                                 │
│   15x faster! 🚀                                                │
└─────────────────────────────────────────────────────────────────┘

```

## Semi\-Structured Data: Beyond Simple Columns [\#](/blog/chdb-journey-to-zero-copy#semi-structured-data-beyond-simple-columns)


Real\-world DataFrames often contain messy `object` columns with nested dictionaries. chDB handles these automatically:



```

```
1import pandas as pd
2import chdb
3
4# DataFrame with nested JSON-like data
5data = pd.DataFrame({
6    'event': [
7        {'type': 'click', 'metadata': {'x': 100, 'y': 200}},
8        {'type': 'scroll', 'metadata': {'x': 150, 'y': 300}},
9        {'type': 'click', 'metadata': {'x': 200, 'y': 400}}
10    ]
11})
12
13# Query nested fields directly with ClickHouse JSON syntax
14result = chdb.query("""
15    SELECT
16        event.type,
17        event.metadata.x as x_coord,
18        event.metadata.y as y_coord
19    FROM Python(data)
20    WHERE event.type = 'click'
21""", "DataFrame")
```

```

![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240-4.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_4_b9f40ca068.jpg)
chDB samples `object` columns, detects dictionary structures, and automatically maps them to ClickHouse's native JSON type—giving you full access to ClickHouse's powerful JSON functions.


## Performance: The Numbers [\#](/blog/chdb-journey-to-zero-copy#performance-the-numbers)


We benchmarked chDB against native Pandas operations using the in\-mem DataFrame ClickBench dataset (1M rows, \~117MB in Parquet).


### Simple Aggregation: COUNT(\*) [\#](/blog/chdb-journey-to-zero-copy#simple-aggregation-count)


**chDB SQL Statement**:



```

```
1SELECT COUNT(*) FROM Python(df);
```

```

**Corresponding Pandas Operation**:



```

```
1df.count()
```

```

By fully utilizing multi\-core CPUs through ClickHouse's multi\-threaded execution engine, chDB's speed in executing `COUNT(*)` aggregation is far beyond Pandas, with performance improved by nearly 247x.




| Engine | Time | Speedup |
| --- | --- | --- |
| Pandas | 0\.8643s | 1x |
| **chDB** | **0\.0035s** | **247x** |


### Complex Query: GROUP BY \+ Multiple Aggregations [\#](/blog/chdb-journey-to-zero-copy#complex-query-group-by--multiple-aggregations)


**chDB SQL Statement**:



```

```
1SELECT
2    RegionID,
3    SUM(AdvEngineID),
4    COUNT(*) AS c,
5    AVG(ResolutionWidth),
6    COUNT(DISTINCT UserID)
7FROM Python(df)
8GROUP BY RegionID
9ORDER BY c DESC
10LIMIT 10
```

```

**Corresponding Pandas Operation**:



```

```
1df.groupby("RegionID")
2  .agg(
3      AdvEngineID=("AdvEngineID", "sum"),
4      ResolutionWidth=("ResolutionWidth", "mean"),
5      UserID=("UserID", "nunique"),
6      c=("RegionID", "size")
7  )
8  .sort_values("c", ascending=False)
9  .head(10)
```

```

Thanks to the refined and optimized Group By operations by ClickHouse's query execution engine, chDB still outperforms Pandas native operations in complex scenarios involving "grouping \+ sorting \+ multi\-aggregation".




| Engine | Time | Speedup |
| --- | --- | --- |
| Pandas | 0\.0623s | 1x |
| **chDB** | **0\.0219s** | **2\.8x** |


## Streaming: Breaking Memory Limits [\#](/blog/chdb-journey-to-zero-copy#streaming-breaking-memory-limits)


What if your query result is too large to fit in memory? chDB supports streaming results:



```

```
1import chdb
2
3# Initialize chDB connection
4conn = chdb.connect()
5
6# Construct query (generate 500,000 rows of data)
7query = "SELECT number FROM numbers(500000)"
8
9# Stream query: retrieve results by block and process
10with conn.send_query(query, "DataFrame") as stream_result:
11    for chunk_df in stream_result:
12        # Custom business logic
13        print(chunk_df)
14
15# Close connection
16conn.close()
```

```

![The Journey to Zero-Copy_ How chDB Became the Fastest SQL Engine on Pandas DataFrame #1240-5.jpg](/uploads/The_Journey_to_Zero_Copy_How_ch_DB_Became_the_Fastest_SQL_Engine_on_Pandas_Data_Frame_1240_5_46732f7a49.jpg)
No more OOM errors. Process terabytes of data on your laptop.


## v4\.0: Closing the Zero\-Copy Loop [\#](/blog/chdb-journey-to-zero-copy#v40-closing-the-zero-copy-loop)


With v2\.0, we achieved zero\-copy on the input side—reading DataFrames directly without serialization. But the output path still went through Parquet serialization. In **chDB v4\.0**, we completed the circle.


![Journey to Zero-Copy Blog Image.jpg](/uploads/Journey_to_Zero_Copy_Blog_Image_3135686cb4.jpg)
### How Output Zero\-Copy Works [\#](/blog/chdb-journey-to-zero-copy#how-output-zero-copy-works)


When ClickHouse produces query results, instead of serializing to Parquet and deserializing back, we now:


1. **Direct Type Mapping**: Map ClickHouse column types directly to NumPy dtypes
2. **Memory Sharing**: Share underlying memory buffers where possible
3. **Batch Conversion**: Convert result chunks directly to NumPy arrays using SIMD\-optimized routines


Here's the complete type mapping we implemented:




| ClickHouse Type | Python/NumPy Type |
| --- | --- |
| Int8/16/32/64 | numpy.int8/16/32/64 |
| UInt8/16/32/64 | numpy.uint8/16/32/64 |
| Float32/64 | numpy.float32/64 |
| String | Python str |
| Date/DateTime | numpy.datetime64 |
| Array | numpy.ndarray |
| Map | Python dict |
| JSON | Python dict (recursive) |
| Nullable(T) | numpy.ma.MaskedArray |


### Benchmark: v4\.0 Output Performance [\#](/blog/chdb-journey-to-zero-copy#benchmark-v40-output-performance)


We benchmarked chDB’s performance in exporting query results to Pandas DataFrames against DuckDB, a similar embedded analytics engine, using the ClickBench hits dataset.


**Test Environment**


- **Dataset**: ClickBench hits dataset (1 million rows, Parquet format, file size \~117MB)
- **Hardware Environment**: AWS EC2 c6a.4xlarge instance
- **Test Method**: Execute a single query 3 times and take the best result
- **Comparison Scenario**: chDB exporting to DataFrame vs. DuckDB exporting to Pandas DataFrame


**Test Code:**



```

```
1# chDB: Query Parquet file and export to Pandas DataFrame
2import chdb
3chdb.query("SELECT * FROM file('hits_0.parquet')", "DataFrame")
4
5# DuckDB: Query Parquet file and export to Pandas DataFrame
6import duckdb
7duckdb.query("SELECT * FROM read_parquet('hits_0.parquet')").df()
```

```

**Export Time**


- chDB: **2\.6418** seconds
- DuckDB: **3\.4744** seconds


Test results show that in the scenario of exporting 1 million rows of data to Pandas DataFrame, chDB's time consumption is reduced by about 24% compared to DuckDB, demonstrating superior data conversion performance.


### Benchmark for daily Pandas usage [\#](/blog/chdb-journey-to-zero-copy#benchmark-for-daily-pandas-usage)


To provide everyone with a relatively complete performance comparison of libraries that can directly read and write Pandas DataFrames, we selected 14 common operations and conducted benchmarks on chDB, Pandas, and DuckDB across three different data sizes. The testing hardware was MacBook M4 Pro \+ 48G memory. We can clearly see several facts:


1. For slicing operations like Head/Limit, Pandas itself has always been the fastest
2. As data volume increases, the advantages of chDB and DuckDB begin to emerge, with chDB maintaining a lead in most 1M and 10M row challenges
3. In most cases, chDB and DuckDB performance is very close, and thanks to v4\.0\.0 improvements, chDB maintains a certain advantage, achieving 7:3 comparing with Pandas and DuckDB with 10M data volume


![Zero-Copy Benchmark.webp](/uploads/Zero_Copy_Benchmark_149b01780c.webp)
Benchmark and the chart code in [github.com/auxten/chdb\-ds](https://github.com/auxten/chdb-ds/blob/main/refs/benchmark_pandas_vs_sql.py).


## Where We Started, Where We Are [\#](/blog/chdb-journey-to-zero-copy#where-we-started-where-we-are)


![Journey to Zero-Copy Blog Post (1).jpg](/uploads/Journey_to_Zero_Copy_Blog_Post_1_2ed9008b31.jpg)
## What You Get as a User [\#](/blog/chdb-journey-to-zero-copy#what-you-get-as-a-user)


Let's summarize what chDB \+ Pandas integration means for you:




| Capability | What It Means |
| --- | --- |
| **DataFrame In** | Query any Pandas DataFrame with SQL, no registration needed |
| **DataFrame Out** | Results come back as DataFrames, ready for visualization |
| **ClickHouse Speed** | Multi\-threaded, vectorized execution on your data |
| **Zero Config** | Just `pip install chdb` and you're ready |
| **JSON Support** | Query nested dictionaries naturally |
| **Streaming** | Process datasets larger than your RAM |
| **80\+ Formats** | Also query CSV, Parquet, S3, MySQL, PostgreSQL... |


## Getting Started [\#](/blog/chdb-journey-to-zero-copy#getting-started)


chDB v4 is now in beta!


We welcome everyone to test chDB v4 and share feedback. pip install "chdb\>\=4\.0\.0b2"



```

```
1#pip install chdb
2
3import pandas as pd
4import chdb
5
6# Load your data however you want
7df = pd.read_csv("your_data.csv")
8
9# Query with SQL
10result = chdb.query("""
11    SELECT column_a, SUM(column_b)
12    FROM Python(df)
13    GROUP BY column_a
14""", "DataFrame")
15
16# Use the result with any Pandas-compatible tool
17result.plot(kind='bar')
```

```

## Join the Community [\#](/blog/chdb-journey-to-zero-copy#join-the-community)


We're always looking to make chDB better. Here's how to connect:


- 📧 **Email**: [auxten.wang@clickhouse.com](mailto:auxten.wang@clickhouse.com)
- 💬 **Discord**: [Join our community](https://discord.com/invite/D2Daa2fM5K)
- 🐛 **Issues**: [GitHub Issues](https://github.com/chdb-io/chdb/issues)
- ⭐ **Star us**: [github.com/chdb\-io/chdb](https://github.com/chdb-io/chdb)


The journey from 30 seconds to 0\.5 seconds was long, but we're just getting started. What will you build with chDB

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
