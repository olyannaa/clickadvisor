# Data Hive: The story of beehiiv’s journey from Postgres to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Data Hive: The story of beehiiv’s journey from Postgres to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Aug 21, 2024 · 8 minutes read[beehiiv](https://www.beehiiv.com/) is a newsletter platform that helps creators, publishers, and businesses build and grow their email audiences. Founded in 2022 by three Morning Brew engineers, it offers tools for creating, sending, and monetizing newsletters, with billions of emails sent each month and millions of dollars paid out to creators.


Behind beehiiv’s success is its sophisticated data infrastructure, which allows it to personalize content, track user engagement, and optimize performance. Handling vast amounts of data in real\-time is essential as the platform scales, providing creators with up\-to\-the\-minute insights they can use to make informed decisions.


“In the newsletter world, we generate a lot of email data,” says Eric Abis, beehiiv’s Head of Data Infrastructure and Engineering. “Every time an email is processed, every time it lands in an inbox, every time it’s deferred, every time it’s bounced, every time you open it, every time you click a link — all of these things add up to millions and billions of events.”


Eric joined beehiiv in August 2023\. At a [recent meetup in New York City](/videos/transistion-from-postgres-to-clickhouse), he shared how the team moved beehiiv’s data operations from Postgres to ClickHouse Cloud, driving major improvements in efficiency, scalability, and overall system reliability.


## Buzzy beginnings [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#buzzy-beginnings)


In 2020, Tyler Denk, Ben Hargett, and Jake Hurd were working as engineers at Morning Brew, a daily business newsletter. As the company scaled, they saw other newsletter operators struggling to achieve similar success. They asked themselves, “How do we take what we’ve built and make it so that anybody can create their own newsletter and monetize it?”


They wrote the initial beehiiv product using Ruby on Rails, a framework they knew well. The original database management system, which they called Honeycomb, ran on Postgres using a Ruby queueing system, powering in\-app analytics and internal dashboards. Initially, their focus was on bootstrapping the startup and proving they had a viable business.


“The founding team did tremendous feats of engineering, scaling the system to handle hundreds of millions of events a week,” Eric says.


However, as the platform grew, the system’s limitations became clear. Postgres, while effective at first, struggled with the increasing data demands, leading to occasional performance issues and requiring more engineering resources. The team realized that to continue growing and ensure a top\-notch user experience, they needed a more scalable solution.


## Choosing ClickHouse [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#choosing-clickhouse)


When Eric joined beehiiv in 2023, he proposed an all\-new data infrastructure. He envisioned a system that was highly scalable, fast, and capable of handling [real\-time analytics](https://clickhouse.com/resources/engineering/how-to-choose-a-database-for-real-time-analytics-in-2026) without the need for cumbersome job queues or batch processing. Resilience was also key; the new system had to be fault\-tolerant, disaster\-recoverable, and secure. His broader goal was to move towards a microservices\-based architecture and an event\-driven framework, offering greater flexibility as the company grew.


“The objective was to build a new system from the ground up, to scale not only beehiiv’s data platform, but ideally the business as a whole,” Eric says.


Eric decided to move from an OLTP (Online Transaction Processing) system to an OLAP (Online Analytical Processing) system. While OLTP databases like Postgres can be great for managing transactional data with high consistency and quick updates, they struggle with the high\-volume, complex queries needed for analytics. OLAP systems, on the other hand, are built for speed and scalability, making them ideal for beehiiv’s requirements.


ClickHouse Cloud emerged as the clear choice for its unmatched performance as an OLAP database. It excels at handling billions of rows with lightning\-fast query speeds, thanks to its columnar storage format and real\-time analytics capabilities. The ability to perform automatic materialized aggregations also eliminates the need for batch processing. Additionally, as an open\-source product with a growing ecosystem of integrations, ClickHouse offers the flexibility and adaptability to support beehiiv as it continues to grow and evolve.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## A new architecture [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#a-new-architecture)


In beehiiv’s new setup, the data platform is built around a distributed, microservices\-based architecture focused on scalability and efficiency. At its core is Kafka, a distributed streaming platform that manages data flow in real\-time. Data is ingested into Kafka, processed, and then streamed to ClickHouse Cloud for storage and analysis. This approach decouples data ingestion from processing, so that high\-volume event streams are handled smoothly without bottlenecks.


ClickHouse acts as the backbone of beehiiv’s data processing and analytics. As an OLAP database, it’s designed to handle the massive data volumes generated by beehiiv’s millions of users and subscribers. By moving data into ClickHouse after it’s streamed through Kafka, beehiiv ensures that their analytics are not only delivered in real\-time but are also highly scalable, supporting the platform’s growth.


In his presentation at the meetup in New York, Eric highlighted several ClickHouse features the team is leveraging in the new architecture. They include:


### ReplacingMergeTree Table Engine [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#replacingmergetree-table-engine)


This feature ensures data integrity by allowing idempotency, meaning the same row can be inserted multiple times without creating duplicates. This is important when handling data from multiple sources or replaying events, as it prevents data duplication.


### Dictionaries [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#dictionaries)


These make joining metadata to large fact tables instantaneous, which allows for the quick materialization of columns. “Without dictionaries, every insert into the raw email data table would require a join query, slowing down the process,” Eric says.


### Ephemeral Columns [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#ephemeral-columns)


This feature allows beehiiv to calculate values to use in other materialized columns without needing to store the calculated data forever. It’s efficient for managing intermediate data that doesn’t need to be kept long\-term but is necessary for certain calculations.


### Materialized Views [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#materialized-views)


beehiiv uses materialized views to store pre\-aggregated data in “shadow tables” with different sort keys, optimizing the system for specific types of queries. This approach speeds up query performance, allowing for faster analytics and insights.


### Window Functions [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#window-functions)


Eric says the new system “relies heavily” on window functions to power various analytics. These functions allow the platform to perform complex calculations across data sets.


## Sweet success [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#sweet-success)


The move from Postgres to ClickHouse has delivered improvements across beehiiv’s organization. Engineers, who used to spend their days fighting scalability fires and managing data availability, can now focus on real engineering work, like building new features. The change has also sparked new ideas and innovation, allowing the team to think broadly about system design without feeling constrained by data limitations.


For business leaders and product managers, the impact has been huge. They now have direct access to raw data and can generate their own metrics without depending on engineers. The shift has opened doors to advanced analytics, which can be delivered to end users via the web app, dashboards, and APIs. It has also laid the groundwork for future machine learning initiatives, such as fraud detection, spam filtering, and ad network optimization.


Users, too, are seeing benefits firsthand. Unlike the old system, where delays of several hours were common, today’s users can send email blasts and view performance data within a few seconds. “That’s really awesome,” Eric says.


Overall, ClickHouse has proven to be “ridiculously fast,” Eric says. Despite running many queries on raw data, the median query time is just 22 milliseconds, with an average query time of 85 milliseconds (a figure Eric says is skewed by a handful of large users and heavy queries, which the team is currently optimizing).


At the time of Eric’s presentation, the system had stored over 33 billion raw events in six months, totaling 1\.5 TiB of compressed data (13 TiB uncompressed). Compared to Postgres, which couldn’t even store the raw data, the new system’s capacity is in a different league, empowering beehiiv to scale and innovate like never before.


## Looking ahead [\#](/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse#looking-ahead)


beehiiv’s transition to ClickHouse Cloud marks a massive transformation, enabling the company to efficiently manage and make use of vast amounts of data. The new architecture not only resolves the scalability issues of the past, it empowers the entire organization to innovate and grow without being held back by technical constraints.


With ClickHouse at the core of their data infrastructure, Eric and the team can deliver real\-time analytics, improve the user experience, and look ahead to implementing even more new features. As the platform grows, beehiiv is well\-positioned to lead in the newsletter industry, giving creators the tools they need to build and monetize their email audiences.

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
