# The world’s fastest tool for querying JSON files


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The world’s fastest tool for querying JSON files

![pavel.png](/_next/image?url=%2Fuploads%2Fpavel_52fa6ba078.png&w=96&q=75)[Pavel Kruglov](/authors/pavel-kruglov)Oct 14, 2022 · 5 minutes read![racing-cars.jpg](/uploads/large_racing_cars_69dec31eac.jpg)
## Introduction [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#introduction)


At ClickHouse, we’re passionate about [benchmarks and performance](https://benchmark.clickhouse.com/). So when I first saw the Hacker News post “[The fastest tool for querying large JSON files is written in Python](https://news.ycombinator.com/item?id=31004563)”, my first thought was \- "But clickhouse\-local is not written in Python". Let’s look at this benchmark and demonstrate that clickhouse\-local is actually the fastest tool for querying large JSON files.


## clickhouse\-local [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#clickhouse-local)


[clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local/) is a single binary that enables you to perform fast processing on local and remote files using SQL \- effectively database features without a database. As well as supporting the full breadth of [ClickHouse functions](https://clickhouse.com/docs/en/sql-reference/functions), JSON is also one of the many [supported file formats](https://clickhouse.com/docs/en/sql-reference/formats/). Below we try to visualize the differences between a ClickHouse cluster, a single ClickHouse instance, and clickhouse–local:


![clickhouse-local.png](/uploads/clickhouse_local_8d3789c232.png)
## The Benchmark [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#the-benchmark)


Daniel Moura, the creator of SPySQL, posted a [benchmark](https://colab.research.google.com/github/dcmoura/spyql/blob/master/notebooks/json_benchmark.ipynb) as a part of the [SPySQL project](https://github.com/dcmoura/spyql). The benchmark compares several command\-line tools with a focus on querying large files that fit into the disk of a standard machine but might not fit into memory. A 10GB subset of the [Amazon book reviews dataset](http://deepyeti.ucsd.edu/jianmo/amazon) was used as the test dataset. The original list of tools used in the benchmark was SPySQL, jq, trdsql, Miller, OctoSQL, spqrk\-sql, Pandas, and DSQ. The benchmark itself focused on 3 challenges:


- Map: a new column is calculated for all rows (batch input and output are large). This represents a common ETL\-like task required for data cleansing and enrichment.
- Aggregation/Reduce: the average of all rows of a column is calculated (only the input is large). Useful to users who need a quick analytical answer and want to avoid the steps of loading the data into a data store such as ClickHouse.
- Subset/Filter: the first 100 values of a column matching filter criteria are returned (only a part of the input needs to be processed). The objective of this test is to assess the tool's ability to sample files quickly and represents a task users often perform before iterating on a query.


The first set of results for this benchmark showed SPySQL as the fastest tool for querying large JSON files:


![initial_results.png](/uploads/initial_results_cb29f85d92.png)
But Daniel was unaware of the clickhouse\-local. To assist with this task, ClickHouse recently introduced two cool features that make it easy and straightforward to process JSON files and reproduce this benchmark: support for semi\-structured data storage and automatic schema inference. The latter feature allows ClickHouse to infer the types of columns from the data itself so that the user is not required to specify the structure of JSON files and the type of each field: simplifying the syntax and accelerating the getting started experience.


After contacting Daniel, he promptly added clickhouse\-local to his benchmarks and updated the results. To his surprise, clickhouse\-local was faster than all previous tools. One of the developers of OctoSQL (written in Go) also asked to update the benchmark in accordance with the latest improvements with good results. Below we show the updated benchmark results.


### Map challenge [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#map-challenge)


![map.png](/uploads/map_e32a6f03c0.png)
**Results for 1GB of data**


![map-results.png](/uploads/map_results_08327d3dc9.png)
### Aggregation (reduce) challenge [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#aggregation-reduce-challenge)


![reduce.png](/uploads/reduce_b0461ed1d5.png)
**Results for 1GB of data**


![reduce-results.png](/uploads/reduce_results_53b0cd1005.png)
### Filter (subset) challenge [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#filter-subset-challenge)


![subset.png](/uploads/subset_a61734b754.png)
**Results for 1GB of data**


![subset-results.png](/uploads/subset_results_3203932782.png)
## Results summary [\#](/blog/worlds-fastest-json-querying-tool-clickhouse-local#results-summary)


![results.png](/uploads/results_332d851de4.png)
The updated results have been posted [here](https://www.reddit.com/r/programming/comments/u98qtz/the_fastest_commandline_tools_for_querying_large/). As we can see, clickhouse\-local is much faster than most other tools for querying large JSON files, whereas OctoSQL excels on smaller files.


This benchmark is not perfect. Each query is run only once, so fluctuations are possible, and users reproducing the results on local hardware may experience noticeable differences between runs. Results may also vary as a result of hardware and operating system differences. Finally, Daniel was deliberate in his approach to not have ORDER BY clauses in filter queries. Although this might mean results are different between tools, as SQL doesn’t enforce a default order, the objective of the benchmark is users wanting to sample files as quickly as possible and the ability of the tool to avoid a full scan. This test gives an advantage to tools that support early termination once satisfying the LIMIT, and those don’t need to load the entire file into memory.


So next time you need to process large JSON files, you know which tool to use!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
