# Retail data, reimagined: How Increff rebuilt its BI platform with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Retail data, reimagined: How Increff rebuilt its BI platform with ClickHouse

![](/_next/image?url=%2Fuploads%2Fincreff_f087885315.png&w=96&q=75)IncreffJan 14, 2025 · 6 minutes read
  



Retail is a high\-stakes game where the margin for error is razor\-thin. For global brands like Puma, Adidas, and Calvin Klein, staying ahead means managing complex supply chains and optimizing inventory, all in real time. That’s where [Increff](https://www.increff.com/), a retail SaaS company, shines.


With flagship products like Merchandising Software and Omni Solution, Increff helps the world’s leading retail brands simplify their operations and make smarter, faster decisions. Whether it’s automating order fulfillment or fine\-tuning inventory, Increff gives companies the tools to navigate the complexities of modern retail.


But behind every smart decision lies a mountain of data, and managing it isn’t always easy. Increff’s platform integrates with over 90 data sources, from CRP systems to cloud storage, allowing businesses to connect and analyze their data wherever it resides. As Increff expanded their client base, serving larger brands with massive catalogs and millions of customers, their BI platform began to struggle under the weight of billions of data points.


At a [September 2024 ClickHouse meetup in Bangalore](https://clickhouse.com/videos/scalable-bi-with-clickhouse-at-increff), lead data analyst Navaneet Krishna shared how Increff reimagined their BI platform, turning to ClickHouse Cloud to create a data architecture that’s scalable, high\-performing, and ready for future growth.


## The BI breaking point [\#](/blog/how-increff-rebuilt-bi-platform-with-clickhouse#the-bi-breaking-point)


Increff’s previous BI system relied on Pandas for data transformations, a serverless SQL database for warehousing, and Superset for visualization. The system worked well for what Navaneet calls “small\-scale BI workloads,” handling datasets of up to 200 million records, but that was about as far as it could go.


![increff.png](/uploads/incerif_4a1bacf290.png)
*Increff’s old BI architecture was functional but struggled with growing datasets and scalability.*
Things took a turn when Increff onboarded a major fashion retailer with data needs five times larger than anything the platform had seen before. Suddenly, the system began to falter. "Query performance dropped and we started to hit concurrency limits, which created a bottleneck," Navaneet recalls. “With our old architecture, we just couldn’t handle that scale.”


The team recognized that if they wanted to keep growing and ensure a good experience for global retail brands, they needed an architecture that could handle massive datasets without sacrificing speed or reliability. Their search for a better BI solution began.


## Rebuilding with ClickHouse [\#](/blog/how-increff-rebuilt-bi-platform-with-clickhouse#rebuilding-with-clickhouse)


As Navaneet explains, he and the Increff team had been "following ClickHouse for a while," and this was the perfect opportunity to put it to the test. A two\-week proof of concept was all it took to prove its value. [ClickHouse Cloud](https://clickhouse.com/cloud) efficiently handled their largest datasets with sub\-second query latencies. "It was a successful implementation," Navaneet says.


Confident in ClickHouse’s capabilities, the team began rearchitecting their BI platform. They replaced most of their Pandas\-based data transformations with DuckDB, implemented managed ClickHouse instances for warehousing, and added Redis caching to speed up dashboard responsiveness. The revamped system was designed to scale, and it delivered.


![increff_v2.png](/uploads/increff_v2_f40989caf1.png)
*Increff’s old BI architecture was functional but struggled with growing datasets and scalability.*


"With ClickHouse Cloud, we’re handling around a billion records, and we’ve maintained the same performance benchmarks we achieved with smaller datasets," Navaneet says. "We’ve also been able to reduce data preparation times by 70 to 80%."


## Taking it up a notch [\#](/blog/how-increff-rebuilt-bi-platform-with-clickhouse#taking-it-up-a-notch)


Since implementing the new architecture, Navaneet and the team have been busy fine\-tuning the BI system to push efficiency and performance even further.


First, they revamped their data modeling, adopting a star schema with a fact constellation design. By creating aggregated fact tables for daily, weekly, and monthly data, they’ve lightened the server load while keeping the granularity needed for analysis. This helps optimize storage and ensures queries run consistently, no matter the scale.


Next up was partitioning and primary keys. Navaneet and the team analyzed their query patterns and set up partitions using time dimensions like days or weeks — columns they knew would get frequent use. This keeps data distribution balanced and avoids the pitfalls of skewed partitions, maximizing the efficiency of ClickHouse’s columnar storage.


Data types played an important role as well. [LowCardinality](https://clickhouse.com/docs/en/sql-reference/data-types/lowcardinality) types were used for categorical data to improve compression and speed up queries, while unsigned integers provided small but meaningful performance boosts for columns with only positive values.


Finally, Navaneet and the team have introduced several query optimizations, including using Jinja templating in Superset to make queries more flexible and strip out unnecessary joins. They also explicitly applied ClickHouse’s [PREWHERE clause](https://clickhouse.com/docs/en/sql-reference/statements/select/prewhere) where execution plans needed fine\-tuning, shaving precious time off query execution.


## The BI of tomorrow [\#](/blog/how-increff-rebuilt-bi-platform-with-clickhouse#the-bi-of-tomorrow)


With the new BI system humming along and improving every day, the Increff team is already looking ahead. They’re exploring advanced ClickHouse features like [projections](https://clickhouse.com/docs/en/sql-reference/statements/alter/projection) and [materialized views](https://clickhouse.com/docs/en/materialized-view) to improve performance further by streamlining query execution and reducing resource consumption. [Dictionaries](https://clickhouse.com/docs/en/sql-reference/dictionaries) for efficient joins are also on their radar.


AI\-driven tools are another area of focus. Navaneet and the team are working on prompt\-based data extraction and visualization, aiming to simplify how users interact with and visualize data. Imagine typing a question and getting a fully formed dashboard in response — that’s the kind of innovation they're working toward.


To maximize flexibility, Increff is moving toward cloud\-agnostic implementations. This will give them greater control over deployments while reducing reliance on specific cloud providers. A self\-service ETL tool is also in development, which would let clients upload and analyze custom datasets directly within Increff’s platform.


## Driving smarter retail decisions [\#](/blog/how-increff-rebuilt-bi-platform-with-clickhouse#driving-smarter-retail-decisions)


Not long ago, Increff faced a mounting challenge: how to scale their BI platform to meet the demands of the world’s largest retail brands. By partnering with ClickHouse, they turned that challenge into an opportunity.


Today, Increff’s BI system, powered by ClickHouse Cloud, delivers sub\-second query speeds and streamlined data preparation, even with massive datasets. By reimagining their data architecture, they’ve built a scalable foundation for future growth. Most importantly, the global retail brands who rely on Increff’s inventory optimization and supply chain management solutions can make faster, smarter decisions with confidence.


To learn more about ClickHouse and see how it can transform your company’s data architecture, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
