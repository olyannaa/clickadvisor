# "Confoundingly fast": Inside Attentive’s migration to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# "Confoundingly fast": Inside Attentive’s migration to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 25, 2024 · 8 minutes read[Attentive](https://www.attentive.com/) is an AI\-powered SMS and email marketing platform that helps brands engage customers with timely, personalized messages. Behind that value proposition is a sophisticated targeting system that ensures every message sent is relevant to the customer’s situation and needs.


“We’re all about sending the right message to the right customer at the right time,” says Larry Finn, a Principal Engineer on Attentive’s targeting team. “We ingest a lot of data from brands about their customers so they can reach people who actually care about the message.”


Over the years, however, Attentive’s data infrastructure had become increasingly complex, spread across “nine or ten different databases,” according to Larry. To continue growing, the company needed to simplify operations, improve scalability, and handle larger data loads. The solution was clear: consolidate their data architecture and migrate to a single database.


At a [September 2024 ClickHouse meetup in New York](https://www.youtube.com/watch?v=7lQpUY1qCnQ), Larry told the story of how Attentive transitioned from a fragmented, multi\-database setup to a streamlined, high\-performance solution powered by ClickHouse Cloud — with a few cat pictures along the way. ????


## Understanding the problem [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#understanding-the-problem)


The first step in improving their data architecture, Larry says, was understanding the problem they needed to solve. “Before you undertake a migration like this, you should figure out why you’re doing it,” he says. “If you don’t actually understand the problem you’re solving, you probably aren’t going to solve it correctly.”


He stresses the importance of understanding your data, including the size and shape of it, and having a good observability system to measure success. In Attentive’s case, the company’s rapid growth and their use of machine learning models meant their data was “growing way faster than before.” They needed a “smarter, faster, simpler” system that could account for specific challenges such as mutating data and idempotency, essential for tracking dynamic customer attributes like location and behavior in real time.


“We wanted to simplify our data architecture, make it easier to build product, make it faster — all the good stuff,” Larry says. “We knew that moving to one database would streamline things and make our system more performant and scalable, without breaking the bank.”


## Choosing the right technology [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#choosing-the-right-technology)


With so many options available, choosing a database wasn’t easy. “There’s a lot to consider,” Larry says. “Some databases excel at many things, like ClickHouse, while others don’t.”


He suggests researching solutions and quickly becoming an “expert” by learning from industry trends and tech talks. He also advises against letting emotions drive decisions and warns not to linger too long in the research phase. It’s important to consider your company’s needs, budget, and detractors, and distinguish real constraints from artificial ones.


After exploring ClickHouse’s features and performance, he was impressed. The installation was “super easy,” and his first queries were “confoundingly fast.” He laughs as he recounts his confusion at ClickHouse’s speed: “I kept thinking, ‘Is it caching something? Am I missing something? Is my laptop on steroids?’”


Cost was another factor. “We’re not in ZIRP times anymore,” Larry says. “We can’t just print money.” ClickHouse’s efficiency and lower resource consumption, combined with its speed, scalability, and support for idempotent data, made it ideal for Attentive’s use case. Its ability to handle large result sets for targeting campaigns was also crucial.


ClickHouse’s [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engine was especially helpful, Larry adds, allowing Attentive to replay data multiple times, even out of order, and achieve consistent results. “We can replay data over and over in any order, and every time we get the right result.”


## Evaluating and implementing ClickHouse [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#evaluating-and-implementing-clickhouse)


Before committing to ClickHouse, Larry and the team ran tests to ensure the database could handle Attentive’s real\-world demands. They used a two\-pronged approach, replaying production traffic to assess how well the system handled data insertion under load and using mock datasets to evaluate query performance, retrieval, and updates.


“It’s important to test with data that represents your actual workload,” Larry says. “You’ll hear people say, ‘This system’s so fast,’ but when you dig into it, they’ve used the simplest query possible. That doesn’t tell you the system is actually going to scale or be fast enough for your use case. We needed to see performance on our own data and queries.”


Once they confirmed ClickHouse could handle their specific workload, they moved on to building the infrastructure. They opted for [ClickHouse Cloud](https://clickhouse.com/cloud), a decision that saved Larry and his team the headache of managing their own infrastructure — a big help for a growing company whose main focus is on scaling their product.


“You might enjoy running databases, but once you manage it yourself, you become that expert people call at 3 in the morning when something bad happens,” Larry says. The cloud service, by contrast, was quick and easy to set up. “You sign up, click a few buttons, and you have your database running with endpoints ready to go.”


## Schema design and data ingestion [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#schema-design-and-data-ingestion)


With the new infrastructure in place, Attentive turned its attention to schema design — what Larry calls “super important” for getting the best performance out of ClickHouse.


“The crazy performance you get from ClickHouse is generally based on the sort key,” Larry explains. Sorting the data correctly allowed them to optimize queries, but it wasn’t without its challenges. For example, the team initially underestimated the importance of [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) precision for their use case. “We didn’t think we’d need microsecond\-level precision for timestamps, but we did,” Larry says.


After fine\-tuning their schema, Attentive used ClickHouse’s [materialized views](https://clickhouse.com/docs/en/materialized-view) to optimize query performance for different use cases. This has allowed them to efficiently handle the various ways their clients want to segment customers, reducing the need to repeatedly compute complex queries.


For data ingestion, Attentive developed custom connectors and relied on [bulk inserts](https://clickhouse.com/docs/en/cloud/bestpractices/bulk-inserts) to process large data streams quickly. Larry again emphasizes the value of the ReplacingMergeTree engine for ensuring data accuracy. “We don't have to worry, because it’s idempotent. Our timestamps are always correct, so we’ll just get the right data every time we replay.”


## Migrating without downtime [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#migrating-without-downtime)


Migration is typically one of the hardest parts of any major system overhaul, and Attentive’s database migration was no exception. Instead of switching everything over to ClickHouse in one go, Larry and the team followed the [“strangler fig” pattern](https://en.wikipedia.org/wiki/Strangler_fig_pattern) — a strategy that allowed them to migrate services piece by piece without interrupting operations.


“We didn’t want to cut over everything at once,” Larry explains. “We built a parallel system to our existing one, allowing us to run both in parallel and compare and contrast performance.”


Shadow testing ensured accuracy and consistency between the legacy system and the new ClickHouse\-based system. The team replayed queries on both systems to compare outputs and latency, gradually building confidence in the new architecture.


Of course, not everything went smoothly. Migrating large datasets brings unique challenges, especially with legacy systems and “crazy optimizations and logic that no one remembers.” But by iterating and “eating the elephant one bite at a time,” Larry says, Attentive completed the migration with minimal disruption to their services.


## Faster, simpler, and ready to scale [\#](/blog/confoundingly-fast-inside-attentives-migration-to-clickhouse#faster-simpler-and-ready-to-scale)


The migration to ClickHouse has already delivered improvements for Attentive. The new system is faster, more scalable, and easier to manage than their previous setup. Queries complete faster, and ClickHouse’s efficiency and data compression have reduced costs.


By moving to ClickHouse Cloud, Larry and the team can now focus on building and optimizing features instead of maintaining infrastructure. The database’s performance and advanced capabilities mean they can keep expanding and scaling Attentive’s platform, powering even more sophisticated targeting and segmentation strategies.


Reflecting on the migration, Larry offers his advice for engineers embarking on similar journeys: “Understand your data, don’t rush the technology choices, and be prepared to iterate.” For Attentive, this approach made all the difference in transforming their data architecture — and with ClickHouse, they’re ready for the next stage of growth.


To learn more about ClickHouse and how it can streamline your company’s data architecture, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_partner_advertising_and_marketing_technology_f168923363.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
