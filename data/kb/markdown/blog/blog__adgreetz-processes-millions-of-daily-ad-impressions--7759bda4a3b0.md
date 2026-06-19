# How AdGreetz Processes Millions of Daily Ad Impressions with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How AdGreetz Processes Millions of Daily Ad Impressions with ClickHouse Cloud

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Apr 26, 2023 · 5 minutes read[AdGreetz](https://www.adgreetz.com/) is the industry’s leading AdTech and MarTech personalization platform, specializing in the creation and distribution of millions of intelligent, data\-driven, hyper\-personalized ads and messages. With a reach spanning 26 diverse channels including email, app, Meta, Google/YouTube, TikTok, CTV/OTT and programmatic platforms \- AdGreetz processes millions of ad impressions daily. When AdGreetz needed a high\-performance, cost\-effective solution for their data storage and analytics needs, ClickHouse Cloud emerged as the ideal choice, offering impressive query speed, excellent customer support, and affordability.


## AdGreetz's Data Processing Journey: From AWS Athena to Snowflake and Finally ClickHouse [\#](/blog/adgreetz-processes-millions-of-daily-ad-impressions#adgreetzs-data-processing-journey-from-aws-athena-to-snowflake-and-finally-clickhouse)


Initially, AdGreetz was using AWS Athena for their data processing needs, but it struggled to meet their increasing performance and data demands. They then turned to Snowflake and experimented with it for about a month, but the cost proved to be prohibitive for their data volume and query performance. Noor Thabit, a Senior Software Engineer at AdGreetz, explained, “Naturally as an AdTech company, data is the heart of our business, and we have a lot of it. For a small startup budget, the value that we got from Snowflake wasn't great. It's expensive for the performance and features we get. So we went looking for alternatives.”


This search led them to ClickHouse, which delivered high\-performance analytics at a substantially lower cost. AdGreetz was particularly impressed with the query speed, rich features, and the exceptional value they experienced using ClickHouse Cloud. Noor highlighted, "With Snowflake, we were using the standard plan, small compute, which cost nearly six times more than ClickHouse Cloud. We got several seconds query time and no materialized views. With ClickHouse Cloud’s production instance, we are getting sub\-second query time along with materialized views. The decision to switch was a no\-brainer for us.”


Noor also praised the customer support, stating, "What really impressed us, in addition to the great performance, is the customer support. They're fantastic. Every time we had a small issue or a general question, the support team response would be very quick and actually helpful. If it's an incident or a major issue, the support team would take their time to try to replicate the issue and come up with the fix. If necessary, they would schedule a 1 meeting with us. It’s been amazing, and it's been consistently like this so far."


## Seamless Integration of ClickHouse into AdGreetz's High\-Volume Ad Impressions Tech Stack [\#](/blog/adgreetz-processes-millions-of-daily-ad-impressions#seamless-integration-of-clickhouse-into-adgreetzs-high-volume-ad-impressions-tech-stack)


AdGreetz handles 5\-6 million ad impression events daily, with numbers peaking at 20\-30 million during busy periods. These impression events come from ad serving clients around the world, making low latency architecture essential. To manage these events they utilize Cloudflare workers which process the events individually and asynchronously. Each worker handles one event at a time, sending a success response to the client, while simultaneously processing and enriching the event in the background. Once complete, the worker asynchronously inserts data into ClickHouse. Currently, Cloudflare workers only support HTTP connections, not TCP. However, ClickHouse is well\-suited for this, as it accepts HTTP requests and enables the direct insertion of JSON payloads without requiring SQL format conversion. This streamlined compatibility simplifies the architecture and eliminates the need for an aggregating component like Kafka. In addition, the ability to query the database over HTTP using TypeScript reduces adoption time and maintains a simplified architecture. With approximately 1\.25 billion rows of data stored, ClickHouse's data compression feature efficiently manages storage requirements.


![AdGreetz image1v3.png](/uploads/Ad_Greetz_image1v3_b5523899d3.png)
**Overview of AdGreetz's Ad Processing Architecture**


- AdGreetz receives millions of events daily from vast tag serving servers.
- These events are sent to Cloudflare workers, which handle the processing.
- Cloudflare workers parse the event data and enrich it before sending it to ClickHouse.
- ClickHouse uses the [HTTP/REST interface](https://clickhouse.com/docs/en/interfaces/http) and [async inserts](https://clickhouse.com/docs/en/optimize/asynchronous-inserts) to handle the data insertion.


To optimize cost and performance, AdGreetz uses a main table along with [materialized views](https://clickhouse.com/docs/en/guides/developer/cascading-materialized-views) for aggregates in ClickHouse. They partition data by time and use Metabase for dashboards and reports, which they then provide externally to their partners who act as intermediaries for end clients. They use views to filter data by customer, ensuring secure separation between different customers' data. Noor emphasizes the importance of this security layer, stating, "we have a view that filters data by customer, providing a layer of security between different customers, without the need to separate the data into different tables."


![Metabase-ss-1.png](/uploads/Metabase_ss_1_8dea9d2a84.png)
![metabase-ss-2.png](/uploads/metabase_ss_2_724f50c6fb.png)
![Screenshot 2023-03-21 at 2.49.55 PM.png](/uploads/Screenshot_2023_03_21_at_2_49_55_PM_397baefd7e.png)
*User\-facing, real\-time ad performance dashboards for AdGreetz's partners showcasing aggregated impression data*
As a high\-performance, cost\-effective, and scalable analytics solution, ClickHouse has proven to be an essential component of AdGreetz's tech stack. It enables the efficient processing of millions of ad impressions daily, while its scalable architecture can adapt to AdGreetz's future growth and increasing data volumes.The integration of ClickHouse and its features has helped AdGreetz deliver personalized, data\-driven advertising experiences.


Visit: <https://www.adgreetz.com/>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
