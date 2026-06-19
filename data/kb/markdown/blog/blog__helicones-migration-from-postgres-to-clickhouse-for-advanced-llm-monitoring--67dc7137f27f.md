# SF Meetup Report: Helicone's Migration from Postgres to ClickHouse for Advanced LLM Monitoring


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# SF Meetup Report: Helicone's Migration from Postgres to ClickHouse for Advanced LLM Monitoring

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Aug 8, 2023 · 4 minutes read
  

On August 8th, 2023, ClickHouse hosted their "ClickHouse and AI \- A Summer Meetup" in San Francisco. We had the pleasure of hearing from Justin Torre, the CEO and co\-founder of Helicone. [Helicone.ai](https://www.helicone.ai/) is an open\-source platform designed for AI observability, offering monitoring, logging, and tracing for Large Language Models (LLMs) applications right out of the box.


Leveraging ClickHouse as a foundational component of their backend, they handle an impressive 3 million requests daily. ClickHouse enables real\-time updates to their dashboards, providing users with immediate visibility into critical metrics like errors and active user counts.


## Helicone’s Rise in the World of LLMs [\#](/blog/helicones-migration-from-postgres-to-clickhouse-for-advanced-llm-monitoring#helicones-rise-in-the-world-of-llms)


Justin spoke about the sudden popularity and surge in LLM usage, with startups rapidly integrating such models into their services. He touched upon Helicone’s inception – initially focusing on a product called TableTalk that allowed users to interact with databases through OpenAI. They quickly realized the need for more extensive monitoring of these LLMs, leading to the creation of Helicone. Its success was driven by an easy integration strategy. By simply adding two lines of code, developers can visualize all their activities in Helicone such as real\-time stats, request logs, and even error details.


![Helicone2.png](/uploads/Helicone2_0ff1e3cc7f.png)
## The Struggle with Scaling Postgres and the Migration to ClickHouse Cloud [\#](/blog/helicones-migration-from-postgres-to-clickhouse-for-advanced-llm-monitoring#the-struggle-with-scaling-postgres-and-the-migration-to-clickhouse-cloud)


Helicone initially launched using Postgres, however this quickly presented a range of challenges, particularly when attempting to scale their dashboard features. Justin explained "we were using Postgres and Postgres just wasn't scaling for those nice dashboards. In order to get these nice dashboards, you need to do all these aggregation calls. Aggregations were taking more than 30 seconds and things were just timing out." AI applications demand flexible data manipulation, where users need the capability to filter, segment, and dissect data dynamically.


Based on a recommendation they decided to try ClickHouse, which immediately gave impressive results. Justin explained "I did a benchmark where I copied a ton of data and then did an aggregation query and I was like… this is fast!" The appeal wasn't just about speed, but also the fact that ClickHouse is open\-source, which aligns with Helicone's core values.


The migration to ClickHouse had its share of complexities, especially around the syncing between Postgres views and ClickHouse tables. They landed on a dual\-insertion approach, populating both ClickHouse and Postgres simultaneously. For newer tables and views, they use pgv2cht, which is an open\-source tool they created.


![Helicone4.png](/uploads/Helicone4_891ec33a4a.png)
After migrating to ClickHouse Helicone experienced a drastic optimization in dashboard query performance. What previously took over 100 seconds was now executed in just 0\.5 seconds. Feedback from their customers was immediate, with many commenting, "Hey, we noticed the dashboard is faster!"


![Helicone3.png](/uploads/Helicone3_1de45e355d.png)
## Conclusion [\#](/blog/helicones-migration-from-postgres-to-clickhouse-for-advanced-llm-monitoring#conclusion)


Justin Torre shared Helicone's transition from its initial product, TableTalk, to its current focus on LLM observability. Their rapid growth led to [scaling challenges with Postgres](https://clickhouse.com/resources/engineering/managed-postgres-for-ai-and-real-time-apps). However, the switch to ClickHouse transformed their performance, slashing dashboard query times. As Justin explained “It was crazy. We went from query times of over 100 seconds to just 0\.5 seconds. We did so many different types of indexes and testing. It was nuts."


This migration not only showcased ClickHouse's efficiency but also aligns with Helicone's commitment to open\-source. Justin appreciated the support from the ClickHouse team, especially via the chat box in ClickHouse Cloud, which helped solve issues efficiently.


## More Details [\#](/blog/helicones-migration-from-postgres-to-clickhouse-for-advanced-llm-monitoring#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/294472987/) in SF on August 8th, 2023
- The presentation materials are available [on GitHub](https://github.com/ClickHouse/clickhouse-presentations/tree/master/meetup81)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
