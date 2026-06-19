# How Socialpruf built a faster, more reliable data stack by replacing Neon with Postgres managed by ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Socialpruf built a faster, more reliable data stack by replacing Neon with Postgres managed by ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 17, 2026 · 9 minutes read## Summary

Socialpruf leverages Postgres and ClickHouse, fully managed in ClickHouse Cloud, to deliver real\-time social analytics for brands, talent agencies, and sports media companies. Migrating from Neon, a Databricks company, reducing network transfer costs and delivered up to 5x faster Postgres query performance with zero connectivity issues. ClickHouse Cloud powers Socialpruf's customer\-facing analytics, aggregating millions of rows in milliseconds to deliver near\-instant dashboards at scale.

The creator economy generates enormous amounts of performance data, but most of it still gets trapped in screenshots, stale PDFs, and gut instinct. [Socialpruf](https://socialpruf.com/) was built to change that.


The Toronto\-based platform calls itself a "social operating system" for brands, talent agencies, and sports media companies, aggregating performance data across Instagram, TikTok, YouTube, and X into real\-time dashboards, campaign trackers, and shareable reports.


Powering that kind of product at scale is a major infrastructure challenge. Today, Socialpruf ingests hundreds of posts per second. Getting data to customers quickly and reliably is core to what makes the product work.


We caught up with Semyon Khlavich, Founder and CTO, and Evgenii Baldin, Principal Engineer, to learn how Socialpruf built their data stack to maximize speed and reliability—moving their analytics workload to [ClickHouse Cloud](https://clickhouse.com/cloud) for near\-instant query performance, and becoming one of the first teams in production on [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres).


## Solving the analytics problem [\#](/blog/socialpruf#solving-the-analytics-problem)


Socialpruf runs on a modern, event\-driven architecture. A Tanstack Start web app serves as the customer\-facing product, backed by a Node.js pipeline that continuously collects and processes social media data—ingesting posts, analyzing video hooks, extracting demographic data, processing mentions, and aggregating co\-author data across platforms. Python workers handle data collection from external providers and browser\-based collectors, and everything flows into Postgres as the system of record.


"Postgres is a wonderful database with a lot of functionality, and we started building on it because it was easy to stand up and get running," Evgenii says.


As Socialpruf grew, however, the analytics layer struggled to keep up. Customer\-facing dashboards were being computed on the fly from Postgres, and load times were climbing to one, two, sometimes three seconds. "We didn't even have that much data at the time," Semyon adds. "We predicted that as we grew and added more customers, it would only get slower."


In the summer of 2025, they began looking at how larger players in the data space were handling analytical workloads. That led them to ClickHouse, and the impact was immediate. By replicating data from Postgres to ClickHouse via CDC and routing all front\-end analytics queries there, Socialpruf was able to aggregate millions of rows in milliseconds, a huge improvement over what Postgres could deliver at scale.


The effect on the product was tangible. "It gives a real 'wow' effect for customers," Semyon says. "We have a great UX, and combining that with the speed of ClickHouse makes for a great user experience."

Loading video...## Addressing reliability issues and network costs with Neon Postgres [\#](/blog/socialpruf#addressing-reliability-issues-and-network-costs-with-neon-postgres)


From the beginning, Socialpruf had been running Postgres on Neon, a Databricks company. It was an easy choice early on: quick to set up, a good developer experience, and more than capable for their needs at the time. "We used it for a while, and it worked well," Evgenii says. "But then once we started reaching scale, we faced two problems."


The first was stability. They began experiencing occasional connection dropouts and restarts that would disrupt their data processing pipeline. Background jobs would stall, requiring manual intervention to identify and restart affected services. "It's not extremely time\-consuming, but it's a bottleneck you have to keep an eye on and check periodically," Semyon says.


The second problem was cost. With CDC replication now streaming a constant flow of data from Neon to ClickHouse, network transfer charges added up. "Even though they live in the same AWS region, Neon was charging us for network transfer," Semyon explains. "It was more than half of what we were paying for compute and just started racking up our bill."


The team discussed trying another solution. "We considered PlanetScale at one point, but kept putting it off, partly because we thought it could have similar problems to Neon," Evgenii says.


When [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres) was announced, as an existing ClickHouse customer, the value proposition was immediately clear: an enterprise\-grade service built to sit natively alongside ClickHouse, with both systems physically collocated in the same infrastructure, eliminating the network transfer costs and backed by NVMe storage for reliability and performance.


"It aligned with our vision of having both the analytical engine and the transactional engine live together on the same platform," Semyon says. "This architecture would bring the seamless analytical experience we wanted our customers to have."


## Up to 5x faster Postgres performance with zero connection dropouts and restarts [\#](/blog/socialpruf#up-to-5x-faster-postgres-performance-with-zero-connection-dropouts-and-restarts)


It's still early, but the biggest impact of migrating to ClickHouse's managed Postgres service has been stability. "We haven't experienced any connectivity issues or restarts since switching," Semyon says. For a team that prides itself on shipping fast, eliminating those dropouts (and the manual intervention they required) makes a huge difference.


"We value stability and velocity," Evgenii adds. "Keeping that balance is important to us."


On the performance side, the numbers tell a clear story. Query performance on Postgres has improved by around 30% overall, with some queries showing up to 5x gains. Looking at Datadog metrics, specific queries dropped from 42 milliseconds to 22 milliseconds, roughly a 50% improvement. Those gains may also create room to downscale their instance as data volumes grow. With these performance gains, NVMe\-backed Postgres is expected to improve price\-performance, enabling Socialpruf to manage resources much more efficiently.


The image below shows a live dashboard displaying the P50 and P99 latency of Socialpruf’s top queries before and after the migration. As you can observe, all the queries are faster than before, with up to 5× performance gains for some queries.


![Image 565019671 2022x420.jpg](/uploads/Image_565019671_2022x420_457bae3940.jpg)
Meanwhile, the ClickHouse analytics layer—what Semyon calls "the magical part about ClickHouse"—continues to underpin the core product experience. Aggregating millions of rows in milliseconds, it powers dashboards that load near\-instantly regardless of data volume.


"At the end of the day, we want to make the best product for our customer," Semyon says. "The managed Postgres piece is more about operational simplicity and reliability on the tech side—having the analytical and transactional layers together reduces technical overhead, lowers costs, and allows us to work with a single platform. ClickHouse is a key differentiator in the value we deliver to customers."


## A seamless migration from Neon to Postgres managed by ClickHouse [\#](/blog/socialpruf#a-seamless-migration-from-neon-to-postgres-managed-by-clickhouse)


One of the deciding factors in Socialpruf's move to Postgres managed by ClickHouse was the migration itself—specifically, the role ClickHouse's team played in making it work.


"We initially tried using Postgres logical replication to migrate around 0\.5 TB of data, but the process failed after a day," Semyon recalls. "The ClickHouse team then proposed using PeerDB and worked closely with us to make the migration straightforward and reliable."


The migration began by creating the required schema on the target database and initiating a Neon\-to\-Postgres managed by ClickHouse mirror with the necessary tables. The 0\.5 TB dataset was copied within a few hours, after which the target database remained continuously synchronized with the source.


Socialpruf ran this mirrored setup for about a week, testing the application by spinning up forks from the syncing database. Once thoroughly validated, a production cutover window was scheduled. During this phase, the ClickHouse team worked closely alongside Socialpruf to complete the final migration steps.


## Managing connections at scale with PgBouncer [\#](/blog/socialpruf#managing-connections-at-scale-with-pgbouncer)


One unexpected challenge during cutover was connection volume. The number of connections exceeded Postgres's `max_connections` limit. That's when they turned to [PgBouncer](https://clickhouse.com/docs/cloud/managed-postgres/connection#pgbouncer), which comes included with Postgres managed by ClickHouse.


Between the application and ingestion workers, Socialpruf can generate thousands of database connections simultaneously. PgBouncer has handled that load reliably since the migration, without any issues.


A key differentiator of ClickHouse's approach is support for multiple parallel, peered PgBouncer instances, allowing connection handling to scale horizontally while keeping the operational complexity hidden from customers. This enabled Socialpruf to efficiently handle large volumes of connections in production. (We'll cover more on our PgBouncer architecture in future technical blog posts.)


## A future\-proof foundation by bringing OLTP and OLAP together [\#](/blog/socialpruf#a-future-proof-foundation-by-bringing-oltp-and-olap-together)


For Semyon and Evgenii, the decision to migrate to ClickHouse's managed Postgres service wasn't a drawn\-out deliberation. The timing was right, the solution made sense, and they trusted ClickHouse to deliver based on how it had already transformed their analytics.


That pragmatism reflects a broader team philosophy. Socialpruf is a product company first—the infrastructure exists to serve the product, not the other way around. Today, ClickHouse powers a [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics) experience that makes customers say "wow," while the managed Postgres service provides the stable, high\-performance transactional foundation beneath.


Semyon says the team has "big plans" for Socialpruf—and now, with the data infrastructure to match, they can focus on executing them. "We're very satisfied with the combination of Postgres and ClickHouse. It just works and fulfills our needs. As we grow, it'll play a bigger role."


Asked to sum up their experience with Postgres managed by ClickHouse, Semyon and Evgenii look at each other for a moment before answering: "Reliable. Fast. Premium quality."

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-106-get-started-today-sign-up&utm_blogctaid=106)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
