# GitTrends: A Google Trends style view of the GitHub ecosystem


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# GitTrends: A Google Trends style view of the GitHub ecosystem

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Mar 10, 2026 · 6 minutes readGitHub generates a constant stream of issues, pull requests, and comments. Those are known as GitHub events. Over time, these billions of events capture the complete lifecycle of technology: how frameworks, libraries, and tools rise and fade. But capturing that immense data stream and turning it into a real\-time trends analyzer is a challenge.


**GitTrends** make this possible. It is a new open\-source demo application that works like a **specialized Google Trends for the tech world**, letting you search and compare any topic, technology, or keyword trends across **over 10 billion GitHub events in real time**.


It is now available at <https://gittrends.clickhouse.com>



> GitTrends is a public demo built to showcase ClickHouse's full\-text search capabilities. It is fully functional, but may be missing some features or have the occasional bug.


## How can you use GitTrends? [\#](/blog/gittrends#how-can-you-use-gittrends)


Type a search term into GitTrends and instantly see how many times it was mentioned across issues, pull requests, and comments in every GitHub repository. This gives you an overview of a technology's popularity over time, the repositories driving the conversation, the developers most actively talking about it, and the actual issues and pull requests where the term appears.


![gittrend-1.png](/uploads/gittrend_1_f90a94c48d.png)
But GitTrends gets really interesting when you start comparing.


### Compare tech adoption [\#](/blog/gittrends#compare-tech-adoption)


Search and compare mention trends for any keywords, exactly like Google Trends but built on the world's most relevant data source for open\-source technology. Compare `ClickHouse vs Druid` to see how two analytics databases have traded momentum over time, or track `Claude vs OpenAI` to watch the AI landscape shift in real developer conversations.


![gittrends-21.png](/uploads/gittrends_21_d1284e2bdc.png)
### Identify Ecosystems [\#](/blog/gittrends#identify-ecosystems)


Identify the top repositories driving the conversation around any topic. Is ClickHouse discussed mostly in its own ecosystem, or is it bleeding into data engineering and observability projects? Is OpenAI mentioned across a broad range of repos while Claude is concentrated in a handful?


Knowing where a technology lives tells you as much as knowing how popular it is.


![gittrends-31.png](/uploads/gittrends_31_cca45cbdc2.png)
### Drill into the Source [\#](/blog/gittrends#drill-into-the-source)


Move from a high\-level trend to the actual conversations behind it. Select any repository and explore its underlying activity: the most active contributors, and the most mentioned issues and PRs driving the trend.


![gittrends-41.png](/uploads/gittrends_41_81773597ae.png)
## Full\-Text Search at Scale [\#](/blog/gittrends#full-text-search-at-scale)


GitTrends is built around a simple idea: search any term in real time, across nearly 10 billion GitHub events with no data transformation. Rather than querying pre\-computed answers, you index the raw text and search it directly at query time. That's the all promise behind the [new full\-text search feature](https://clickhouse.com/blog/full-text-search-ga-release) recently released in ClickHouse. [Simply build a text index on a text column](https://clickhouse.com/docs/engines/table-engines/mergetree-family/textindexes) and use full\-text search.


What makes ClickHouse particularly powerful here is that full\-text Search and aggregation live in the same engine. A single query can search raw text and aggregate results in one pass, with no joins across systems, no data movement, and no latency penalty. That combination is what makes the experience feel instant rather than just fast.


The GitHub events dataset, nearly 10 billion rows of issues, pull requests, and comments, is a deliberate stress test. GitTrends still delivers fast search across all of it.


To highlight the performance of the new full\-text search index, GitTrends includes a live query performance comparison. For any search, you can toggle between using full\-text Search, bloom filter and a full table scan and watch the difference play out in real time. 


It is the clearest demonstration of what the right index buys you at scale.


## Look under the hood [\#](/blog/gittrends#look-under-the-hood)


GitTrends is fully open and built to be explored at every layer.


### How is the data ingested? [\#](/blog/gittrends#how-is-the-data-ingested)


We have been ingesting the GitHub events dataset for some time and exposing it in our SQL Playground so anyone can explore it with SQL. We also documented several example queries and analyses on this [page](https://clickhouse.com/demos/explore-github-with-clickhouse-powered-real-time-analytics).


The ingestion script used to load the data into ClickHouse is available [here](https://github.com/ClickHouse/sql.clickhouse.com/blob/main/load_scripts/github_events/ingest.sh).


Note that GitHub introduced changes to the Events API payloads starting in October 2025\. As a result, certain fields differ from earlier data, which can affect analyses and make trend detection across the full history less accurate. More details are available in the GitHub [changelog](https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/).


### What SQL query is running behind each chart? [\#](/blog/gittrends#what-sql-query-is-running-behind-each-chart)


Every chart in GitTrends is backed by a real query. Click the SQL button on any chart to open it in the SQL playground, where you can inspect it, edit it, and run it yourself.



```

```
1SELECT
2  toStartOfDay(created_at) AS bucket,
3  count() AS count
4FROM github.github_events
5WHERE
6  event_type IN ('IssueCommentEvent','IssuesEvent','PullRequestEvent','PullRequestReviewCommentEvent','PullRequestReviewEvent')
7  AND hasAllTokens(body, 'clickhouse')
8  AND created_at >= (now() - toIntervalMonth(1))
9  AND 1=1
10GROUP BY bucket
11ORDER BY bucket ASC
12SETTINGS
13    enable_parallel_replicas = 1,
14    enable_full_text_index = 1,
15    use_skip_indexes = 1,
16    query_plan_direct_read_from_text_index = 1,
17    use_skip_indexes_on_data_read = 1
```

```

Each search type, full\-text search, bloom filter, and full table scan, has its own query so you can see exactly what changes under the hood.


### How is the application built? [\#](/blog/gittrends#how-is-the-application-built)


Interested in running GitTrends locally or adapting the approach to your own dataset?


Most of the demo was developed with Claude Code. The complete source code and step by step deployment instructions are available on [GitHub](https://github.com/ClickHouse/gitTrends).


Give the demo a try at <https://gittrends.clickhouse.com> and share with us [any feedback](https://github.com/ClickHouse/gitTrends/issues/new).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
