# pg\_clickhouse is the fastest Postgres extension on ClickBench


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# pg\_clickhouse is the fastest Postgres extension on ClickBench

![](/_next/image?url=%2Fuploads%2FImage_512x512_1_8bc569c360.png&w=96&q=75)[David Wheeler](/authors/david-wheeler)Feb 18, 2026 · 4 minutes readIn December 2025, we launched [pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse), a PostgreSQL extension to query ClickHouse directly from Postgres. Its primary goal is to minimize the application migration effort required to move analytics workloads from Postgres to ClickHouse. In designing pg\_clickhouse, we made deliberate architectural choices to ensure that you can continue to use the familiar Postgres interface for both transactional and analytical queries, while harnessing the full power of ClickHouse for analytics.


In this blog post, we examine those design choices and highlight their performance impact by benchmarking pg\_clickhouse in [ClickBench](https://benchmark.clickhouse.com/).

## Query pushdown vs. shoehorning analytics into Postgres [\#](/blog/pg_clickhouse-fastest-analytics-for-postgres#query-pushdown-vs-shoehorning-analytics-into-postgres)


We designed **pg\_clickhouse** to minimize load on Postgres by offloading analytic execution as much as possible to ClickHouse. Instead of running heavy analytics inside Postgres and consuming its resources, it rewrites queries for execution in ClickHouse and only the results are returned, on a best\-effort basis.


This architecture contrasts with most analytic extensions that embed columnar storage and analytic execution engines directly within Postgres. While those approaches can accelerate analytics, they still rely on Postgres resources and are ultimately constrained by a single shared node. As data volumes grow into the terabyte or tens\-of\-terabytes range, analytics workloads begin to compete with transactional workloads for the same system resources.


By delegating execution to ClickHouse, pg\_clickhouse enables independent scaling and avoids resource contention within Postgres. This model especially enhances aggregation\-heavy queries that scan millions or billions of rows. In this context, effective **query pushdown** is the central challenge, not just for filtering, but for aggregation in particular.


## pg\_clickhouse is the fastest Postgres extension on ClickBench [\#](/blog/pg_clickhouse-fastest-analytics-for-postgres#pg_clickhouse-is-the-fastest-postgres-extension-on-clickbench)


To evaluate the impact of these design choices, we recently added pg\_clickhouse to ClickBench, a standard benchmark for analytical DBMS.


As of the end of January, the results are in: ***pg\_clickhouse is [the fastest PostgreSQL extension](https://benchmark.clickhouse.com/#system=+gkus%7C_b%7Cpnc%7CsaB&type=-&machine=-ca2l%7C6t%7Cg4e%7C6ax%7Cae-l%7C6ale%7Cg-l%7C3al&cluster_size=-&opensource=-&hardware=+c&tuned=+n&metric=combined&queries=-), outperforming all other Postgres analytics extensions, performing only slightly slower than native ClickHouse itself.*** Across all 42 ClickBench queries, on both ARM64 (c8g) and AMD64 (c6a) instances, performance closely tracks ClickHouse.


![Screenshot comparing the ClickBench performance of pg_clickhouse to ClickHouse on both arm64 (c8g) and amd64 (c6a) servers.](/uploads/clickbench_2026_02_02_c689143402.png)
These results confirm that pg\_clickhouse pushes down full query execution to ClickHouse. The only measurable overhead comes from rewriting queries, the network round\-trip, and converting the results to Postgres. Postgres does not execute the analytical workload itself; it acts purely as a routing and result layer.


## Comprehensive aggregate and expression pushdown [\#](/blog/pg_clickhouse-fastest-analytics-for-postgres#comprehensive-aggregate-and-expression-pushdown)


ClickBench relies a relatively simple schema: a single denormalized table with no `JOIN`s. While this avoids join pushdown complexity, it highlights something equally important: *comprehensive aggregate and expression pushdown.*


The benchmark exercises a broad range of operations that pg\_clickhouse fully entrusts to ClickHouse, including:


- `COUNT()`, `SUM()`, `AVG()`, `COUNT(DISTINCT)`
- `MIN()`, `MAX()`
- `GROUP BY`
- `ORDER BY` (including `ORDER BY COUNT()`)
- `HAVING`
- `EXTRACT()`, `DATE_TRUNC`
- Date comparisons
- `LIKE`, `REGEXP_REPLACE()`
- `CASE WHEN`


These represent only a subset of the aggregates, functions, and expressions currently supported. We continue to expand coverage, document supported patterns, and close remaining gaps, most recently in [yesterday's 0\.1\.4 release](https://github.com/ClickHouse/pg_clickhouse/releases/tag/v0.1.4).


And we're not stopping here. Work is already underway to support more complex query shapes, including subqueries and [CTEs](https://www.postgresql.org/docs/current/queries-with.html). We'll share more on these improvements in the coming months.


## Get Started [\#](/blog/pg_clickhouse-fastest-analytics-for-postgres#get-started)


To start using **pg\_clickhouse**, you can try the open\-source version through [this quickstart guide](https://github.com/ClickHouse/pg_clickhouse/blob/main/doc/tutorial.md). **pg\_clickhouse** also comes included in our [managed Postgres service](https://clickhouse.com/cloud/postgres).

### Try Postgres managed by ClickHouse

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-67-try-postgres-managed-by-clickhouse-get-access&utm_blogctaid=67)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
