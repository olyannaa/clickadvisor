# Trade secrets: How Coinhall uses ClickHouse to power its blockchain data platform


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Trade secrets: How Coinhall uses ClickHouse to power its blockchain data platform

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 14, 2024 · 7 minutes read
  



[Coinhall](https://coinhall.org) is an omnichain trading terminal that delivers real\-time price charts and optimizes trading opportunities by aggregating swap data from 23 different blockchain networks. Founded in 2021, the platform provides users with comprehensive trading tools and the best possible swap rates across decentralized exchanges.


To manage vast amounts of blockchain data from multiple sources, Coinhall requires top\-tier performance and scalability. Speed enables real\-time analytics and ensures users can make timely trading decisions, while cost\-efficiency keeps operating costs low, helping the company stay competitive, allocate resources effectively, and support future growth.


Two years ago, Coinhall co\-founder and CTO Aaron Choo led a transformation of Coinhall’s data architecture. At a recent [meetup in Singapore](/videos/powering-coinhalls-real-time-blockchain-data-platform), Aaron detailed the transition, including the impressive results they’ve seen since implementing ClickHouse.


## In the beginning [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#in-the-beginning)


Aaron started Coinhall as what he calls a “solo weekend project” in August 2021\. At the time he was still a computer science student at the National University of Singapore, with little professional experience, let alone knowledge of database management systems.


He initially built the platform around BigQuery, since he had used Google Cloud Platform at university, and it offered a reasonable free tier. It worked well for a while, Aaron says, but eventually the team ran into issues, most noticeably around performance and cost.


“Queries took on average around two seconds to run,” Aaron says. “This might not be a problem for other use cases, but because we’re a consumer\-facing trading product, if you’re waiting a few seconds just to load data, that’s problematic.”


They also quickly eclipsed BigQuery’s free tier, running two million queries and scanning more than 150 terabytes of data each day. Finding themselves spending thousands of dollars per month for subpar performance, they knew it was time to make a change.


### Choosing ClickHouse [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#choosing-clickhouse)


Aaron quickly Googled “time series database” and found a few options, migrating the platform to QuestDB in October 2021\. Part of the reason he chose QuestDB was that he wanted a solution he could self\-manage. It was an improvement over BigQuery, but by mid\-2022 he had become frustrated with the database’s lack of developer resources and features.


This time, wanting to find a proper long\-term solution, he did a more comprehensive search, comparing online reviews and external benchmarks to find the best fit for Coinhall’s needs. In this early evaluation phase, he saw that ClickHouse had an advantage in every aspect other than complexity, but even that was something he knew he could control.


“As a developer, you can always learn, improve, and make your experience better,” he says.


As part of his evaluation, Aaron focused on how well each database could handle candlestick queries. Candlestick charts are essential for trading platforms like Coinhall, as they visually represent price movements over time, showing the open, high, low, and close prices for each trading period. For Coinhall to deliver real\-time trading insights, it needed a database that could perform these queries quickly and at scale.


Aaron narrowed his choices to Rockset, SingleStore, Snowflake, and ClickHouse. In terms of performance, ClickHouse was the clear winner, executing candlestick queries in 20 milliseconds, compared to 400 milliseconds or more for the other databases. It ran latest\-price queries in 8 milliseconds, outpacing the next\-best performance (SingleStore) which came in at 45 milliseconds. Finally, it handled ASOF JOIN queries in 50 milliseconds, while Snowflake took 20 minutes and Rockset timed out.


ClickHouse also easily won on cost\-efficiency. While the other three managed services cost up to $2,000 per month, self\-hosting ClickHouse was by far the most cost\-effective option, with a monthly cost of only $50\. It delivered these results with just 4 vCPUs and 16 GB of RAM, making it an ideal choice for a small but growing company like Coinhall, who needed to keep operational costs low while ensuring high performance.


![coinhall-img1.png](/uploads/coinhall_img1_ac81e33cc1.png)
### Learnings and optimizations [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#learnings-and-optimizations)


Aaron and the team began migrating the platform to ClickHouse in July of 2022\. As Aaron says, “It wasn’t easy, because we had three or four services running.” But by October, they had fully transitioned to ClickHouse as their primary database management system.


As they’ve gotten more comfortable using ClickHouse, Aaron and the team have made a number of optimizations aimed at boosting speed and efficiency:


### Performance tuning [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#performance-tuning)


As Aaron says, “A database is only as fast as its slowest query.” Early in the implementation, as the team adjusted to some of the differences between ClickHouse and other databases, they encountered performance bottlenecks that slowed certain queries.


Aaron turned to ClickHouse’s documentation, and in particular its [guide on sparse primary indexes](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes), which he calls the “best resource if you’re thinking of using ClickHouse.” By following best practices and fine\-tuning their queries, Aaron and the team have reduced query times, ensuring that even their most complex operations are executed efficiently.


### Efficient data retrieval [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#efficient-data-retrieval)


One of the main challenges the team faced was the inefficiency of the “Limit By” clause, which was necessary for retrieving the latest prices of each asset but inherently scanned the entire table, leading to performance bottlenecks.


To address this, they incorporated two ClickHouse features: AggregatedMergeTree and materialized views. The former is designed for efficient storage of aggregated data, allowing the system to store only the most recent data points, reducing the number of rows scanned during queries. Materialized views automatically update whenever new data is inserted into the table. By creating materialized views that pull only the most recent data, Aaron and the team ensure that only relevant rows are scanned during query execution.


As Aaron notes, this combination boosted query performance by reducing the computational load required to retrieve the latest prices. The result is a much faster and more efficient data retrieval process, which is important for maintaining real\-time analytics.


### Managing complex joins [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#managing-complex-joins)


A third challenge the Coinhall team faced was managing complex join operations, specifically sort\-merge joins, where tables are individually sorted and then merged. Since ClickHouse manages merge joins differently than other databases, Aaron has taken an alternative approach, either avoiding joins where possible or reducing their complexity.


By redesigning their data queries to minimize reliance on joins, they can maintain high performance without compromising on data accuracy or completeness.


## Into the future [\#](/blog/trade-secrets-how-coinhall-uses-clickhouse-to-power-its-blockchain-data-platform#into-the-future)


After trying multiple databases, Aaron and the team found an ideal long\-term solution in ClickHouse that lets them deliver a first\-class trading experience based on real\-time analytics. Looking ahead, they plan to continue to optimize and expand their use of ClickHouse, leveraging even more of its features to add new trading tools, improve the user experience, and position Coinhall for growth as a data platform for years to come.


From Coinhall’s CTO, Aaron Choo: "At Coinhall, managing vast amounts of blockchain data efficiently is crucial for our consumer\-facing trading platform. Initially, we used BigQuery, but as our data grew, so did its costs and performance issues. After exploring several alternatives, we found ClickHouse to be the clear winner. ClickHouse significantly outperformed other databases we tested like Snowflake, Rockset, and SingleStore, and delivered at 40x cost savings.”


Access Aaron Choo’s slides from the meetup [here](https://aaroncql.github.io/clickhouse-presentation-110724/1).


To learn more about ClickHouse and how it can make your data operations faster and more efficient, [join our open\-source community](/slack) or [try ClickHouse Cloud free for 30 days](https://clickhouse.cloud/signUp?loc=coinhall-blog).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
