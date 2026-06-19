# How Electrum is driving Indonesia's net\-zero carbon future with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Electrum is driving Indonesia's net\-zero carbon future with ClickHouse

![](/_next/image?url=%2Fuploads%2FAndi_Pangeran_dfacec1f6a.jpg&w=96&q=75)Andi PangeranJan 31, 2025 · 8 minutes read
  



As Indonesia's leading electric motorcycle company, [Electrum](https://electrum.id) is a major player in the nation’s shift toward low\-carbon, sustainable transport. With a fleet of more than 3,000 electric bikes and 250 battery swap stations, Electrum is redefining urban travel in Jakarta and beyond. By pairing innovative technology with scalable infrastructure, the company is helping Southeast Asia's largest economy move closer to its goal of net\-zero carbon emissions by 2060\.


But a seismic shift like this comes with equally massive data challenges. Electrum gathers a steady flow of information from IoT sensors in its motorcycles and battery swap stations, as well as transactional data from top\-ups, rentals, and fleet management. These two data streams are critical for monitoring operations, improving performance, and providing actionable insights to business teams. As the company expanded its fleet and services, it was clear they needed a more flexible, scalable database solution to keep up with growing demand.


At a [ClickHouse meetup](https://www.youtube.com/watch?v=cYrh0Wasyqo) in Jakarta in October 2024, Principal Software Engineer Andi Pangeran shared how Electrum used ClickHouse to build a powerful data platform from scratch, giving them the speed, cost\-efficiency, and scalability to support their long\-term growth.


## The electric data surge [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#the-electric-data-surge)


Operating in the world's second\-largest electric motorbike market (after India), Electrum's fleet has grown exponentially over the past year, increasing from a few hundred to over 3,000 vehicles, with its drivers collectively traveling over 220,000 kilometers per day. 


"Imagine the carbon offset and sustainability impact of moving from an ICE motorcycle to an electric motorcycle," Andi says. "That's the impact we're trying to offer to Indonesians."


But this rapid expansion has triggered a tidal wave of data demands. The IoT data stream alone is immense, with each battery continuously transmitting key metrics like voltage, current, temperature, state of charge, and health status. GPS location data and vehicle telemetry add another layer of real\-time information to be processed. 


On top of that, transactional data from customer top\-ups, battery swaps, and fleet management operations introduces even more complexity, with thousands of transactions occurring daily across Electrum's growing network of stations and vehicles.


"These two data sets are crucial to supporting our business," Andi says. "We needed a platform that could monitor ongoing activities, support analytics, and generate actionable insights."


## Priorities for a new database [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#priorities-for-a-new-database)


Electrum's search for a new database focused on three main priorities: flexibility, efficiency, and scalability. Flexibility would let business users query raw and aggregated data independently, without help from engineers. This self\-service approach was key to responding quickly to challenges, like investigating swap station performance or analyzing driver behavior.


Efficiency was just as important. With millions of records generated daily, the database needed to handle high volumes of data while minimizing its use of resources. As a startup, Electrum couldn't afford to over\-provision or let infrastructure costs spiral out of control.


Finally, scalability was non\-negotiable. With plans to expand its fleet and add thousands of new bikes and swap stations, Electrum needed a solution that could grow alongside its business. Whether it was doubling CPU capacity or moving to a multi\-server setup, the database had to keep pace with Electrum's rapid expansion.


## ClickHouse: The perfect choice [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#clickhouse-the-perfect-choice)


After considering a range of options, including row\-based databases like Postgres and MySQL, ClickHouse emerged as the clear winner. Its [columnar storage format](https://clickhouse.com/docs/en/faq/general/columnar-database) allows for lightning\-fast queries, processing only the relevant data rather than scanning entire rows. This is especially valuable for Electrum's IoT datasets, where engineers need to quickly analyze performance metrics and spot trends.


ClickHouse's indexing features also stood out. [Sparse primary indexes](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes) allow queries to skip irrelevant data granules, while [skip indexes](https://clickhouse.com/docs/en/optimize/skipping-indexes) filter out unnecessary data blocks, making querying large datasets almost instantaneous. As Andi says, "It's really, really fast."


The database's merging mechanisms, particularly the [MergeTree engine family](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree), add even more efficiency and flexibility. These engines support real\-time aggregation and deduplication during data merges, which is important for managing massive IoT and transactional datasets. By organizing data into manageable parts and merging them in the background, ClickHouse ensures queries remain fast and accurate, even as Electrum's data volumes grow.


## Building the Electrum data platform [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#building-the-electrum-data-platform)


With ClickHouse as the foundation, Andi and the team built a data platform designed for flexibility, efficiency, and scalability. IoT data from batteries and swap stations flows through gateways, where it's converted into event formats and published to Kafka. Transactional data from Postgres is captured via Debezium, which streams changes into Kafka for further processing. Custom workers then consume these Kafka streams, integrating the data into ClickHouse to create a unified pipeline for real\-time analytics and historical analysis.


![Blog_ElectrumDiagram_012025_FNL.png](/uploads/Blog_Electrum_Diagram_012025_FNL_189630e685.png)
Electrum's new architecture relies heavily on [materialized views](https://clickhouse.com/docs/en/materialized-view), which Andi calls the "distinguishing feature of ClickHouse." These views transform and pre\-aggregate data in real\-time as it's ingested, giving business and engineering teams up\-to\-date insights.


For example, when a battery swap station was underperforming, the team analyzed IoT data processed through materialized views. They discovered that prolonged exposure to direct sunlight was causing the station's batteries to overheat, leading to slower charging times. This ability to diagnose and address operational challenges in real time has made Electrum's new data platform a key driver of their success.


"With materialized views, many of our daily transactions and IoT data points can be quickly summarized," Andi says. "Instead of processing all 50 million records, we only need to analyze a much smaller subset in real\-time. It's so much faster — this makes us very happy."


![jakarta_electrum.png](/uploads/jakarta_electrum_27566a34e6.png)
*Geospatial h3 heatmap visualizing trip density across Jakarta.*
Another standout feature of ClickHouse, Andi says, is its geospatial function, which allows Electrum to create hexagonal h3 heatmaps for visualizing trip density and assessing carbon impact. These insights are frequently used by the operational team to drive fleet optimization and advance sustainability efforts.


## Electrifying results [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#electrifying-results)


The impact of Electrum's data transformation can be felt company\-wide. Today, the platform processes over 50 million records daily, with sub\-second query times. This blazing performance means business users can access analytics on their own, removing bottlenecks and enabling faster data\-driven decision\-making.


The company has also seen huge improvements in cost efficiency. Despite managing massive IoT and transactional datasets, Electrum spends less than $500 per month on its single\-server setup. These savings allow the startup to allocate more resources toward scaling operations, developing new products, and improving the customer experience.


Looking ahead, Andi says Electrum plans to scale their ClickHouse implementation to a multi\-server setup, making the system even more performant and reliable. With ClickHouse powering its data strategy, Electrum is in a great position to keep innovating and growing.


## Charging into the future [\#](/blog/electrum-driving-net-zero-carbon-future-with-clickhouse#charging-into-the-future)


Electrum's journey shows the power of the right database when it comes to solving complex challenges at scale. By integrating ClickHouse into their operations, Andi and the team have built a flexible data platform to support their growing fleet, optimize performance, and deliver real\-time business insights, all while keeping costs under control.


As Indonesia sprints toward its goal of net\-zero carbon emissions, Electrum's story offers an inspiring look at how technology and innovation can fuel a greener, more connected future. With ClickHouse as the heart of their data infrastructure, the road ahead looks bright for Electrum and Indonesia’s electric mobility revolution.


To learn more about ClickHouse and see how it can improve the performance and scalability of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
