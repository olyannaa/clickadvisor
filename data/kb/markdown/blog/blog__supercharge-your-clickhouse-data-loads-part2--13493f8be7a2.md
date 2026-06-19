# Supercharging your large ClickHouse data loads \- Part 2: Tuning a large data load for speed


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Supercharging your large ClickHouse data loads \- Part 2: Tuning a large data load for speed

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Oct 18, 2023 · 16 minutes read![large_data_loads-p2-01.png](/uploads/large_data_loads_p2_01_e9832557ed.png)
This blog post is part of the `Supercharging your large ClickHouse data loads` series:


- [Performance and resource usage factors](/blog/supercharge-your-clickhouse-data-loads-part1)
- [Making a large data load resilient](/blog/supercharge-your-clickhouse-data-loads-part3)


## Going on a race track [\#](/blog/supercharge-your-clickhouse-data-loads-part2#going-on-a-race-track)


In this second part of our three\-part blog series about supercharging large data loads, we will put the theory from the [first](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1) post into practice by demonstrating how you can run a large multi\-billion row insert 3 times faster than with default settings using the same hardware. We outline a formula that you can use to determine the best block size / parallelism ratio for your ingestion use case. And lastly, we will break the speed limit by utilizing ClickHouse Cloud’s new SharedMergeTree table engine combined with easy horizontal cluster scaling.


Note that we only demonstrate a tuning scenario here, where data is pulled by the ClickHouse servers themselves. You can read about a setting where clients push the data to ClickHouse [here](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse).


## The challenge [\#](/blog/supercharge-your-clickhouse-data-loads-part2#the-challenge)



Using ClickHouse for [large data loads](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance) is like driving a high\-performance Formula One car 🏎 .
A copious amount of raw horsepower is available, and you can reach top speed for your large data load. But, to achieve maximum ingestion performance, you must choose (1\) a high enough gear ([insert block size](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#insert-block-size)) and (2\) an appropriate acceleration level ([insert parallelism](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#insert-parallelism)) based on (3\) the concrete amount of available horsepower ([CPU cores and RAM](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#hardware-size)).



Ideally, we would like to drive our race car in the **highest gear** with **full acceleration**:


- Highest gear: The larger we [configure the insert block size](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers), the fewer parts ClickHouse has to create, and the fewer [disk file](https://en.wikipedia.org/wiki/Category:Disk_file_systems) [i/o](https://en.wikipedia.org/wiki/Input/output) and [background merges](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges) are required.
- Full acceleration: The higher we [configure the number of parallel insert threads](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers-1), the faster the data will be processed.


However, there is a conflicting tradeoff between these two performance factors (plus a tradeoff with background part merges). The amount of available main memory of ClickHouse servers is limited. Larger blocks use [more](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#impact-on-performance-and-resource-usage) main memory, which limits the number of parallel insert threads we can utilize. Conversely, a higher number of parallel insert threads requires [more](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#impact-on-performance-and-resource-usage-1) main memory, as the number of insert threads determines the number of insert blocks created in memory concurrently. This limits the possible size of insert blocks. Additionally, there can be resource contention between insert threads and [background merge threads](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges). A high number of configured insert threads (1\) creates more parts that need to be merged and (2\) takes away CPU cores and memory space from background merge threads.


Our challenge is to find a sweet spot with a large enough block size and a large enough number of parallel insert threads to reach the best possible insert speed.


## The experiment [\#](/blog/supercharge-your-clickhouse-data-loads-part2#the-experiment)


In the following sections, we put these block size / parallelism settings to the test and evaluate their effect on ingest speed.


### Test data [\#](/blog/supercharge-your-clickhouse-data-loads-part2#test-data)


The data we experiment with is from the [PyPi dataset](https://clickhouse.com/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis#pypi-dataset) (hosted in a GCS bucket). It consists of **65\.33 billion rows** and has a raw, uncompressed size of \~**14 TiB**. The compressed data size on disk (when stored in a ClickHouse table) is \~**1\.2 TiB**.


### Test table and insert query [\#](/blog/supercharge-your-clickhouse-data-loads-part2#test-table-and-insert-query)


For these tests, we will ingest this data as fast as possible into a [table](https://gist.github.com/tom-clickhouse/50ec22c9cf6a5569c45d1aea958a09d4) in a ClickHouse Cloud [service that c](https://clickhouse.com/pricing)onsists of 3 ClickHouse servers with 59 CPU cores and 236 GiB of RAM per server. We’ll use an [INSERT INTO SELECT query](https://gist.github.com/tom-clickhouse/808dd03d7bc4cf061bf98b7bbb77c3a6) in combination with the [s3Cluster](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#parallel-servers) integration table function (which is compatible with gcs).
![large_data_loads-p2-02.png](/uploads/large_data_loads_p2_02_a34ea2bb28.png)


We’ll start by ingesting our large dataset with the default settings for [insert block size](https://clickhouse.com/docs/en/operations/settings/settings#min-insert-block-size-bytes) and [insert threads](https://clickhouse.com/docs/en/operations/settings/settings#max-insert-threads), and will then repeat this load with different numbers to assess the impact on load time.


### Queries for introspecting performance metrics [\#](/blog/supercharge-your-clickhouse-data-loads-part2#queries-for-introspecting-performance-metrics)


We are using the following SQL queries over [system tables](https://clickhouse.com/blog/clickhouse-debugging-issues-with-system-tables) for introspecting insert performance metrics visualized in our test [results](/blog/supercharge-your-clickhouse-data-loads-part2#top-speed):


- [Number of active parts at ingest finish](https://gist.github.com/tom-clickhouse/5c17431de8716041e10acde1ef379a8a)
- [Time to reach less than 3k active parts](https://gist.github.com/tom-clickhouse/d4df796c10a318a4c95061362e486ab5)
- [Number of initial parts written to storage](https://gist.github.com/tom-clickhouse/beebf6b9f7876b4c100c4e234771b221)
- [Number of initial parts written to storage per cluster node](https://gist.github.com/tom-clickhouse/1435eba5e76701bee00a9145f40aec79)


## Shifting gears [\#](/blog/supercharge-your-clickhouse-data-loads-part2#shifting-gears)


![large_data_loads-p2-03.png](/uploads/large_data_loads_p2_03_dc77564d85.png)
To illustrate how insert block sizes impact the number of parts that get created (and need to be merged), we visualize below various [insert block sizes](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#insert-block-size) (in terms of rows) versus the (uncompressed) average in\-memory size of a single data block and its corresponding ([compressed](https://clickhouse.com/docs/en/about-us/distinctive-features#data-compression)) average on\-disk size of a single data [part](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage). This is overlayed with the average overall number of parts written to storage. Note that we give average values because, as [mentioned](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers) in the first post, the created blocks and parts rarely precisely contain the configured number of rows or bytes, as ClickHouse is [streaming](https://clickhouse.com/company/events/query-performance-introspection) and processing data row\-[block](https://clickhouse.com/docs/en/operations/settings/settings#setting-max_block_size)\-wise. Therefore these settings specify minimum thresholds.


*Also, note that we took these numbers from the [results](/blog/supercharge-your-clickhouse-data-loads-part2#top-speed) of different ingest test runs in the next section.*


![large_data_loads-p2-04.png](/uploads/large_data_loads_p2_04_1b4f466d4f.png)
You can see that the larger we [configure](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#configuration-when-data-is-pulled-by-clickhouse-servers) the insert block size, the fewer parts need to be created (and [merged](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges)) for storing the test data, \~1\.2 TiB of compressed table data. For example, with an insert block size of 1 million rows, 65 thousand initial parts (with an average compressed size of 20 MiB) will be created on disk. Whereas with an insert block size of 80 million rows, only 817 initial parts get created (with an average compressed size of 1\.5 GiB).
## Standard speed [\#](/blog/supercharge-your-clickhouse-data-loads-part2#standard-speed)


The following chart visualizes the [result](https://gist.github.com/tom-clickhouse/6c2bd2b6bd18aca4a1cce665d0c806fe) of ingest runs with the default insert block size of [\~1 million rows](https://clickhouse.com/docs/en/operations/settings/settings#min-insert-block-size-rows) but different numbers of insert threads. We show the peak memory used and the resulting time for the number of parts to reach 3000 (the [recommended](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#parts-to-throw-insert) number for efficient querying):
![large_data_loads-p2-05.png](/uploads/large_data_loads_p2_05_8bcb732865.png)
With the ClickHouse Cloud default setting of 4 ingest threads (default is no parallel ingest threads in OSS), the peak amount of consumed main memory is 7 GiB per server. It takes over 4 hours from the start of the ingest until the [65 thousand initially created parts](/blog/supercharge-your-clickhouse-data-loads-part2#shifting-gears) are merged to a [healthy](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#parts-to-throw-insert) number of less than 3 thousand parts. With its default settings, ClickHouse tries to offer a good balance of resource usage for supporting concurrent tasks from concurrent users. One size doesn’t fit all, though. Our goal here is to tune a dedicated service only used by us for one purpose: Achieving top speed for inserting our dataset.


If we match the amount of utilized parallel insert threads with the number of 59 available CPU cores, the time to 3k active parts is increased compared to lower thread settings.


The lowest time is achieved with 16 insert threads, leaving plenty of the 59 CPU cores available for [background part merge threads](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges) that run concurrently with the data insertion.


Note that the blue horizontal bar on top in the chart above denotes the available memory per server (236 GiB RAM). We can see that there is much room for increasing insert block size and memory usage (blue vertical bars in the chart above), respectively.


Currently, we are pushing the accelerator pedal with full force (up to 59 insert threads) in a very low gear (only 1 million rows per initial part), resulting in a low overall ingestion speed. We will now find a better gear and acceleration combination in the next section.


## Top speed [\#](/blog/supercharge-your-clickhouse-data-loads-part2#top-speed)


![large_data_loads-p2-06.png](/uploads/large_data_loads_p2_06_0ed79d0f98.png)
We tried to identify the perfect combination of insert block size and number of insert threads by running ingestions with different systematic combinations for these insert speed factors. The following chart visualizes the results of these ingest test runs, where we doubled the insert block size a few times (from [1 million](https://gist.github.com/tom-clickhouse/6c2bd2b6bd18aca4a1cce665d0c806fe) to [5 million](https://gist.github.com/tom-clickhouse/bfd88290a696144de9b5f6d4d07f0c08) to [10 million](https://gist.github.com/tom-clickhouse/4cff7a19f89faac96f53f2e3963403b3) to [20 million](https://gist.github.com/tom-clickhouse/174b81144169ae02dcec1c4518839f53) to [40 million](https://gist.github.com/tom-clickhouse/8955d5a57ad4babf84690a10f90da97a), until [80 million](https://gist.github.com/tom-clickhouse/3570f02b38e8b5f11351cd2d446f7d8c)):


![large_data_loads-p2-07.png](/uploads/large_data_loads_p2_07_357c63e939.png)
For each block size, we doubled the number of insert threads (starting at 4\) until the peak memory usage (blue vertical bars) almost reached the available memory per server (blue horizontal bar). The yellow circles indicate the time from the start of the ingest until all initially created parts are merged to a healthy number of less than 3000 parts.


We reached top speed when the 65\.33 billion rows of our dataset were ingested by 32 parallel insert threads with an insert block size of 10 million rows. This is the sweet spot for our server size of 59 CPU cores and 236 GiB RAM. This causes a moderate amount of [6\.5 thousand initial parts](/blog/supercharge-your-clickhouse-data-loads-part2#shifting-gears), that can be quickly merged to less than 3000 parts in the background by the free 27 CPU cores (32 cores are used for reading and ingesting the data in parallel). With 16 insert threads and less, the insert parallelism is too low. With 59 insert threads, a 10 million rows block size doesn’t fit into the RAM.


A 5 million row block size works with 59 insert threads. Still, it creates [13 thousand initial parts](/blog/supercharge-your-clickhouse-data-loads-part2#shifting-gears) without leaving any dedicated CPU cores for an efficient background merging, resulting in resource contention and a long time to reach 3 thousand active parts. With 32 and 16 insert threads, the data is processed slower but merged faster as more dedicated CPU cores are available for background merges. 4 and 8 insert threads don’t create enough insert parallelism with a 5 million row block size.


Insert block sizes of 20 million rows and more cause [low numbers of initial parts](/blog/supercharge-your-clickhouse-data-loads-part2#shifting-gears), but the high memory overhead restricts insertion to a low number of insert threads creating insufficient insert parallelism.


**With our identified sweet spot settings, we sped up the ingest by a factor of almost 3\.** We used exactly the same underlying hardware, but we utilized it more effectively for our data ingestion, without creating too many initial parts by pressing the accelerator pedal in half force (32 insert threads) with the highest possible gear (10 million rows block size).


## Formula One [\#](/blog/supercharge-your-clickhouse-data-loads-part2#formula-one)


We are aware that identifying perfect settings for large multi\-billion row inserts via several test runs is impractical. Therefore we give you this handy formula for calculating approximately the settings for top speed of your large data loads:


`• max_insert_threads: choose ~ half of the available CPU cores for insert threads (to leave enough dedicated cores for background merges)
  
  
• peak_memory_usage_in_bytes: choose an intended peak memory usage; either all available RAM (if it is an isolated ingest) or half or less (to leave room for other concurrent tasks)   
  
Then:  
min_insert_block_size_bytes = peak_memory_usage_in_bytes / (~3 * max_insert_threads)`


With this formula, you can set `min_insert_block_size_rows` to 0 (to disable the row based threshold) while setting `max_insert_threads` to the chosen value and `min_insert_block_size_bytes` to the calculated result from the above formula.


## Breaking the speed limit with ClickHouse Cloud [\#](/blog/supercharge-your-clickhouse-data-loads-part2#breaking-the-speed-limit-with-clickhouse-cloud)


![large_data_loads-p2-08.png](/uploads/large_data_loads_p2_08_ac7345f2e0.png)
The next measure to make the ingestion even faster is to put more horsepower into our engine and increase the number of available CPU cores, respectively, by adding additional servers.


Combined with its [SharedMergeTree table engine](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates), ClickHouse Cloud [allows](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#automatic-cluster-scaling) you to freely (and [quickly](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates#seamless-cluster-scaling)!) either change the size (CPU and RAM) of existing servers or add additional servers. We did the latter with our service and ingested our dataset with different numbers of ClickHouse servers (each with 59 CPU cores and 236 GB RAM). This chart shows the [results](https://gist.github.com/tom-clickhouse/5517b902d3990f7299d747bedbd5fd77):
![large_data_loads-p2-09.png](/uploads/large_data_loads_p2_09_92bb211121.png)
For each ingestion test run, we used the optimal tuning settings (32 parallel insert threads with an insert block size of 10 million rows) identified in the section [above](/blog/supercharge-your-clickhouse-data-loads-part2#top-speed).


We can see that the ingest throughput scales perfectly linearly with the number of CPU cores and ClickHouse servers, respectively. This enables us to run your large data inserts as fast as you want.


### It can be as fast as you want it to be [\#](/blog/supercharge-your-clickhouse-data-loads-part2#it-can-be-as-fast-as-you-want-it-to-be)


ClickHouse Cloud allows you to easily scale ingest duration linearly with additional CPU cores and servers, respectively. Therefore, you can run large ingests as fast as required. The following chart visualizes this:
![large_data_loads-p2-10.png](/uploads/large_data_loads_p2_10_ad4238e5c3.png)
A single ClickHouse Cloud server (with 59 CPU cores and 236 GB RAM) ingests our 65 billion row dataset with a throughput of [\~4 million rows per second](/blog/supercharge-your-clickhouse-data-loads-part2#breaking-the-speed-limit-with-clickhouse-cloud) in \~240 minutes. Based on our ingest test runs [above](/blog/supercharge-your-clickhouse-data-loads-part2#breaking-the-speed-limit-with-clickhouse-cloud) proving linear scalability, we project how the throughput and ingest time can be improved with additional servers.


## Summary [\#](/blog/supercharge-your-clickhouse-data-loads-part2#summary)


In this second part of our three\-part blog series, we gave guidance and demonstrated how to tune the major insert performance factors for drastically speeding up a large multi\-billion row insert. On the same hardware, the top ingestion speed is almost 3 times faster than with default settings. Additionally, we utilized ClickHouse Cloud’s seamless cluster scaling to make the ingest even faster and illustrated how you can run your large data inserts as fast as you want by scaling nodes.


We hope you learned some new ways to supercharge your large ClickHouse data loads.


In the next and last post of this series we will demonstrate how you can load a large dataset incrementally and reliably over a long period of time.


Stay tuned!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
