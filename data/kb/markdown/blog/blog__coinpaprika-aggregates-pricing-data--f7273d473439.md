# Coinpaprika Aggregates Pricing Data Across Hundreds of Cryptocurrency Exchanges with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Coinpaprika Aggregates Pricing Data Across Hundreds of Cryptocurrency Exchanges with ClickHouse

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)May 5, 2023 · 5 minutes read[Coinpaprika](https://coinpaprika.com/) is a leading cryptocurrency market data platform that offers users comprehensive insights into price data, historical trends, market capitalization, trading volume, and other relevant metrics for numerous cryptocurrencies across hundreds of exchanges. By connecting directly to almost 370 exchanges using open APIs, and actively working on integrating decentralized exchanges, Coinpaprika aims to provide developers, investors, and businesses with a user\-friendly, transparent, and reliable source of information in the cryptocurrency space.


## Transitioning from InfluxDB to ClickHouse for Improved Performance and Scalability [\#](/blog/coinpaprika-aggregates-pricing-data#transitioning-from-influxdb-to-clickhouse-for-improved-performance-and-scalability)


Before adopting ClickHouse, Coinpaprika was using InfluxDB for their time\-series data alongside MySQL for transactional data. However as their data grew they faced several challenges with InfluxDB. The team struggled to obtain useful metrics from the system, and extending the timeframe for queries often resulted in server overload. Additionally, they experienced issues with response times due to merging data blocks. The open\-source version of InfluxDB lacked built\-in replication and scalability, which were crucial for Coinpaprika's infrastructure.


Radosław Wesołowski, CEO and Co\-founder of Coinpaprika, described their process of evaluating various time\-series databases to enhance their platform's capabilities: “We decided to take a look at different vendors for example, TimescaleDB, CockroachDB and ClickHouse, but after a few initial tests, we decided that ClickHouse was the best choice out of these vendors.”


The decision to choose ClickHouse as their time\-series database was not taken lightly. Coinpaprika evaluated several factors in their decision\-making process, including:


- Number of moving parts and components \- Coinpaprika preferred ClickHouse's single binary architecture over TimescaleDB's multilayer architecture.
- Press coverage on social media \- ClickHouse had been endorsed by big names like Cloudflare and Uber.
- Availability of training materials \- Coinpaprika found ample resources to support their learning.
- Community on Slack \- The ClickHouse community provided valuable assistance and knowledge.
- Storage size and query throughput \- ClickHouse demonstrated impressive performance metrics that fit Coinpaprika's needs.
- Sales team engagement \- Coinpaprika wanted to go as far as possible on their own, while competitors seemed eager to jump to Enterprise solutions.
- Maturity of technology and tooling \- ClickHouse offered a mature, feature\-rich technology stack.


Since making the switch to ClickHouse, the platform has enjoyed significant improvements in performance, query concurrency, and scalability. They managed to develop the initial version of their product using ClickHouse within just three months. Along the way, they experimented with [different codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema) and optimized data structures. After the successful initial setup, they decided to migrate all their data to ClickHouse.


## Coinpaprika's Go and Gorm Integration with ClickHouse [\#](/blog/coinpaprika-aggregates-pricing-data#coinpaprikas-go-and-gorm-integration-with-clickhouse)


One of the essential aspects of Coinpaprika's infrastructure is their choice of programming language and tools. The platform is 99% Go based, and they use an open\-source ORM called Gorm with the [official ClickHouse client](https://github.com/clickHouse/clickHouse-go). This setup allows them to integrate seamlessly with ClickHouse, making it easier for them to build and maintain their solution. The out\-of\-the\-box support provided by Gorm enabled the team to implement their requirements quickly and conveniently.


## Coinpaprika's Architecture: Balancing Public and Private Infrastructure [\#](/blog/coinpaprika-aggregates-pricing-data#coinpaprikas-architecture-balancing-public-and-private-infrastructure)


The Coinpaprika system design consists of many services distributed across public and private infrastructure. For cost optimisation, most CPU and disk intensive parts are hosted on\-premises. Consumer facing interfaces for optimal user experience (low latency) are distributed globally in public cloud infrastructure.


![coinpaprika_image1_ba97a93793.png](/uploads/coinpaprika_image1_ba97a93793_18c7487d6e.png)
## Enhancing Performance and Query Concurrency with ClickHouse at Coinpaprika [\#](/blog/coinpaprika-aggregates-pricing-data#enhancing-performance-and-query-concurrency-with-clickhouse-at-coinpaprika)


ClickHouse’s ability to provide low latency even when subjected to higher query concurrency is essential for Coinpaprika, who need to efficiently handle around 150 requests per second. This level of performance would be challenging to achieve with alternative solutions on the market. ClickHouse's high concurrency ensures that Coinpaprika can consistently deliver accurate, up\-to\-date data to their users. Additionally, materialized views and precomputed aggregations help to optimize data storage and retrieval, enhancing performance for both free and paid users seeking historical information.


![coinpaprika_image2.png](/uploads/coinpaprika_image2_9d9bbc4104.png)
*Grafana dashboard showing the typical query distribution during the day. The average query time is around 7ms which guarantees their clients the best developer experience.*
Coinpaprika's choice to adopt ClickHouse as their time\-series database has significantly improved their platform's capabilities. The advantages of enhanced performance, query concurrency, and scalability have allowed Coinpaprika to offer a reliable and user\-friendly experience for developers, investors, and businesses in the cryptocurrency space. The seamless integration with their existing Go and Gorm infrastructure has further optimized their development process. As the cryptocurrency market continues to evolve, Coinpaprika can confidently depend on ClickHouse's robust and flexible data storage solution to support their growth and maintain their position as a leading market data platform.


Learn more: <https://coinpaprika.com/>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
