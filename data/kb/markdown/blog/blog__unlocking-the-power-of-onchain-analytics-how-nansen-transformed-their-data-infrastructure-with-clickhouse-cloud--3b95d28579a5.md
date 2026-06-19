# Unlocking the power of onchain analytics: how Nansen transformed their data infrastructure with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Unlocking the power of onchain analytics: how Nansen transformed their data infrastructure with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 2, 2024 · 7 minutes read[Nansen](https://www.nansen.ai/) is one of the world’s leading blockchain analytics platforms, empowering top crypto teams and investors with detailed insights and analytics. Serving both individual clients and large enterprises, the platform acts as an information hub in the crypto market, offering real\-time alerts, on\-chain flows, and detailed dashboards.


![5-Integrated-Portfolio-Research.png](/uploads/5_Integrated_Portfolio_Research_23f3bec61e.png)
At the heart of Nansen’s operations lies an enormous amount of blockchain data, continuously ingested and processed to ensure accuracy and relevance. By transforming raw data into actionable insights, Nansen helps investors discover investment opportunities, perform due diligence, and defend their portfolios against market volatility.


In 2022, Anders Aagaard joined Nansen with a clear mandate: “Make the platform faster.” In the short term, he saw the need for a database management system to meet their performance needs without adding complexity. At the same time, he knew the importance of a long\-term solution that could simplify operations while keeping costs in check. After a thorough search, he found everything he needed in [ClickHouse Cloud](https://clickhouse.com/cloud).


## From BigQuery to ClickHouse [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#from-bigquery-to-clickhouse)


When Anders reviewed Nansen’s data operations, he flagged a series of performance issues as the company’s technical requirements had evolved. Their data infrastructure, built primarily around BigQuery, was struggling to keep pace with Nansen’s needs. End users would wait “minutes, hours, or even days” for dashboards to load and display insights. In addition, BigQuery’s costs were quickly becoming unsustainable.


In search of a better alternative, Anders and his team began evaluating other database management systems. They considered several options, including AlloyDB and Apache Druid, but found that while they outperformed BigQuery in some aspects, they often introduced new complexities or failed to deliver the necessary gains in speed and efficiency.



> “We had some basic performance requirements for our queries and had received a lot of feedback that speed was critical for our users,” Anders says. “Internally, we also discussed the trade\-offs between increasing developer complexity and getting the performance we needed. As we looked at different solutions, that balance was hard to find.”


Anders first heard of ClickHouse several years earlier at Schibsted, before the open\-source database became its own independent company. In those early days, Anders says they had a number of good conversations with the ClickHouse team, and he followed their progress as they incorporated in 2021 and released ClickHouse Cloud in 2022\.


When Anders revisited ClickHouse in his new role at Nansen, he saw right away that the columnar database offered exceptional performance. His team conducted rigorous tests, comparing its capabilities against their existing setup and other solutions. The results were impressive: ClickHouse not only outperformed BigQuery in speed and efficiency, but the managed service offered by ClickHouse Cloud on GCP promised reduced complexity and costs.



> “ClickHouse was the winner by a considerable margin,” Anders says. “Compared to other solutions, it offered the best balance of performance improvements without introducing unmanageable complexity.”


## The Benefits of ClickHouse Cloud [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#the-benefits-of-clickhouse-cloud)


After a successful proof of concept in which Anders and the team managed ClickHouse internally, they decided to transition Nansen’s data infrastructure to ClickHouse Cloud fully. Anders says their long\-term vision had always been finding a cloud service to simplify their data operations.



> “We know the pains of managing your own infrastructure, especially when it comes to storage,” Anders says. “We wanted a fully managed service like ClickHouse Cloud to help us avoid that.”
> Today, ClickHouse is in the center of Nansen’s data operations. As Anders explains, the move to ClickHouse Cloud on GCP has provided a range of benefits to Nansen’s team, customers, and the business at large.


### Improved Performance [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#improved-performance)


First and foremost, Anders says, ClickHouse has brought unmatched speed to Nansen’s data operations. This speed upgrade is critical for providing the real\-time, actionable insights Nansen is known for, helping users make faster decisions, capitalize on timely opportunities, and mitigate losses in the face of market volatility.



> “With ClickHouse, we’re running queries we wouldn’t have dreamed of with our old setup,” Anders says.


Specifically, he says they’ve moved from running batch queries hourly, which were both costly and time\-consuming, to real\-time streaming using materialized views in ClickHouse. This shift has offloaded a significant amount of processing to the ClickHouse Cloud infrastructure, allowing for more frequent, less expensive queries with considerably lower data latency.


### Cost Efficiency [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#cost-efficiency)


The move to ClickHouse Cloud has allowed Nansen to manage large data volumes and run complex queries without racking up exorbitant processing fees. The total cost savings, Anders says, have been “orders of magnitude” better than their previous setup.


The BigQuery pricing model is based on the amount of bytes scanned by each query, which can cause costs to quickly spike, especially with many concurrent queries. ClickHouse Cloud offers a more predictable and economical solution. Its efficient columnar storage, advanced compression techniques, and decoupled compute and storage architecture help minimize data processing costs. Meanwhile, ClickHouse Cloud’s pricing based on compute units consumed means that Nansen only pays for the hardware resources they use, which is better aligned with a company growing out of startup mode.


### Scalability [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#scalability)


The massive amounts of blockchain and cryptocurrency data that Nansen deals with on a daily basis — currently more than 100 terabytes of compressed data storage — will only continue to grow as adoption increases across the blockchain ecosystem. As Nansen’s user base expands, with more individual crypto investors and larger chains and funds coming on board, ClickHouse’s distributed architecture and horizontal scaling ensure that Nansen can handle these rising data volumes without a drop in performance.


![3-Personalised-Signals.gif](/uploads/3_Personalised_Signals_d9ce41556c.gif)
### Streamlined Operations [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#streamlined-operations)


The managed service offered by ClickHouse Cloud has simplified Nansen’s data operations, allowing the team to focus more on developing new features and improving their analytics platform, rather than getting bogged down in the day\-to\-day complexities of infrastructure management.



> “ClickHouse Cloud takes away an enormous amount of stuff that we would otherwise need to do manually,” Anders says. “It lets us focus on what we do best: building solutions to empower crypto investors to make better decisions.”


## Better Blockchain Insights [\#](/blog/unlocking-the-power-of-onchain-analytics-how-nansen-transformed-their-data-infrastructure-with-clickhouse-cloud#better-blockchain-insights)


The benefits of moving to ClickHouse have been felt not just by Anders and his team but by everyone in the company and Nansen’s users.



> “Since moving to ClickHouse Cloud, we’ve seen a very large cost decrease,” Anders says. “At the same time we’re running queries that would have been unfeasible with BigQuery, and we have data latency in a completely different category as well.”


Looking ahead, Nansen is well\-positioned to continue growing and scaling their platform, relying on ClickHouse Cloud to handle increasing data volumes and deliver real\-time insights to a growing number of clients. Thanks to ClickHouse’s combination of performance, cost efficiency, scalability, and simplified operations, Nansen remains the market leader in on\-chain analytics, committed to delivering value and innovating on behalf of Web3 investors and institutional clients now and into the future.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
