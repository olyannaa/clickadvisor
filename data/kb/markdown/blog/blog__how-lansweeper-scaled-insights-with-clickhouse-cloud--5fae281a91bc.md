# How Lansweeper scaled IT, OT, and IoT insights with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Lansweeper scaled IT, OT, and IoT insights with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 11, 2025 · 8 minutes read[Lansweeper](https://www.lansweeper.com/) has come a long way from its early days as a simple inventory tool. Five years ago, it offered a basic table—searchable, sortable, and little else. Desktop scanners pulled data from devices across networks and sent it to the cloud, where it lived in MongoDB. If a user wanted to know what assets they had, the system could tell them. At the time, that was enough.


But as Lansweeper’s [technology asset intelligence platform](https://www.lansweeper.com/product/) expanded to cover IT, OT, and IoT environments, customer expectations changed. They wanted to go deeper, analyzing not just assets but also users, software, and vulnerabilities. They wanted to customize views, apply complex filters, and surface meaningful, actionable insights in real time.


That brought new technical challenges. As Lansweeper collected more types of data, it also collected more data, period. Today, the company tracks more than 50 million assets, 150 million users, 1\.4 billion pieces of software, and 5\.5 billion vulnerabilities. And customers—names like PepsiCo, Nvidia, and AstraZeneca—expect all of it to be instantly queryable.


At a recent [ClickHouse meetup in Ghent, Belgium](https://www.youtube.com/watch?v=UOPKB4f_BCA), lead developer Juan Carlos Lloret Hernández shared the story of Lansweeper’s evolution—from a basic inventory tool to an Elasticsearch\-based analytics pipeline, then to ClickHouse OSS, and ultimately to a high\-performance architecture powered by [ClickHouse Cloud](https://clickhouse.com/cloud).


## The pains of Elasticsearch [\#](/blog/how-lansweeper-scaled-insights-with-clickhouse-cloud#the-pains-of-elasticsearch)


By early 2023, Lansweeper had outgrown MongoDB for analytics. The database was still their single source of truth, but it just wasn’t built for the kind of fast, flexible queries users were asking for. “It’s not the best solution for real\-time analytics,” Juan Carlos says.


So the team added a new layer: Elasticsearch. It was familiar and fast enough to power new features like customizable views, advanced filtering, and full\-text search. Instead of relying on limited filters or groupings in the UI, they could now show smarter summaries, like how many assets had a certain software installed, or which systems were affected by specific vulnerabilities.


![461489392-29cc9254-328a-474f-8878-b45a06e9e6ad.png](/uploads/461489392_29cc9254_328a_474f_8878_b45a06e9e6ad_21ca6d3a64.png)
Lansweeper’s Elasticsearch pipeline layered on top of MongoDB: incoming asset data flows through Kafka into enrichment services before being indexed and queried for real\-time insights.


For a while, it worked. But as usage grew, Elasticsearch’s cost became hard to justify. “It was very expensive,” Juan Carlos says. “Seventeen percent of our total cloud spend went to Elasticsearch.” They looked into Elastic’s official hosted service, but the price was even steeper: two to three times more expensive for the same hardware.


On top of that, they ran into problems with ingestion and scale. The platform was constantly updating huge documents, and Elasticsearch couldn’t keep up. “We wanted to explore vulnerabilities from different points of view,” Juan Carlos explains. “That required creating new indexes, and it was just something we couldn’t manage to solve.”


And the growing split between Elasticsearch and OpenSearch didn’t help. Diverging licenses and drivers added more complexity to an already strained system. “We just weren’t comfortable with it anymore,” Juan Carlos says. “So we started looking for alternatives.”


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Scaling with ClickHouse [\#](/blog/how-lansweeper-scaled-insights-with-clickhouse-cloud#scaling-with-clickhouse)


The team evaluated a number of OLAP databases. After benchmarking several options, one stood out. “ClickHouse outperformed Elastic in every single test,” Juan Carlos says. “Sometimes it was 10 times faster—even on slower hardware, because we were testing ClickHouse on our laptops and Elastic on production machines.”


That performance opened new possibilities. With ClickHouse, they could finally build the features they’d struggled to implement, like surfacing vulnerabilities from multiple perspectives across assets, users, and software. ClickHouse also gave them the efficiency they needed to keep costs down as data volumes continued to rise.


The team deployed ClickHouse OSS in their Kubernetes environment using the Altinity operator, standing up a three\-replica cluster with fast SSDs and Zookeeper. The architecture didn’t need a major overhaul: data still flowed from Kafka into enrichment services and through to ClickHouse. “The migration was quite smooth,” Juan Carlos says.


![461489391-9bd4ab41-98a4-4df9-a749-c551699e414a.png](/uploads/461489391_9bd4ab41_98a4_4df9_a749_c551699e414a_c869871dea.png)
Lansweeper’s ClickHouse OSS setup: enriched asset data flows through Kafka and Go\-based consumers into ClickHouse, with the same analytics API delivering insights to the user\-facing cloud app.


One challenge remained: real\-time ingestion. “Our assets change really fast, really often, and are really big,” he explains. At the time, ClickHouse didn’t support updates, so the team adopted an insert\-only model. “If something updates, we just insert a new row. If it’s deleted, we insert a new row marked deleted.” The latest version is determined by a sort key and timestamp. “It sounds a bit overkill, but ClickHouse is really fast, so why not?”


With careful schema design—sorting by client and asset key, and partitioning by date—they were able to keep queries fast without sacrificing freshness. Even customers with a million assets could get near\-instant results.


## From self\-managed to ClickHouse Cloud [\#](/blog/how-lansweeper-scaled-insights-with-clickhouse-cloud#from-self-managed-to-clickhouse-cloud)


ClickHouse OSS gave Lansweeper the performance they needed, but not without tradeoffs. Running their own cluster meant extra overhead. The team had opted for fast SSDs to keep performance high, but that made setup expensive. And scaling horizontally wasn’t exactly straightforward. “You can scale ClickHouse on\-prem, but it’s not easy,” Juan Carlos says.


The real trouble, though, was Zookeeper. It became a constant source of issues, from out\-of\-memory errors to disk corruption to nodes falling out of sync. “Kubernetes hates the JVM,” Juan Carlos says with a laugh. “We had incidents where Zookeeper wouldn’t even start.” After one especially painful outage, Juan Carlos and the team decided they “didn’t want to manage ClickHouse infrastructure anymore.”


That’s when [ClickHouse Cloud](https://clickhouse.com/cloud) launched. For Lansweeper, the timing was perfect. It was their first experience as early adopters, and the switch couldn’t have been easier. “We didn’t do anything,” Juan Carlos says. “No rework, no downtime. We just changed connection credentials.” Because their architecture was already Kafka\-based, they spun up a new consumer and started piping data into ClickHouse Cloud without touching the API layer.


The payoff was immediate. With S3\-based storage replacing SSDs, infrastructure costs fell off a cliff. “We’re now paying 30% of the cost of OpenSearch, with 3x more assets,” Juan Carlos says. Even with all the new features they’ve added since, ClickHouse Cloud still costs less than half of what they were paying three years ago. “And performance is the same, with less hardware than the on\-prem,” he adds.



## Building for IT, OT, and IoT insights [\#](/blog/how-lansweeper-scaled-insights-with-clickhouse-cloud#building-for-it-ot-and-iot-insights)


ClickHouse Cloud solved Lansweeper’s infrastructure and performance challenges, but that was just the foundation. The bigger goal was to give users more control over their data. While the old table\-based interface allowed for filters and saved views, it still made it hard to explore relationships across assets, vulnerabilities, and software. Inventory lived on one page, risk insights on another, and reports somewhere else entirely.


Juan Carlos and the team wanted to go further. Recently, they rolled out a new experience powered by Luzmo: an interactive dashboard layer that lets users build their own charts, drill into specific segments, and bring datasets together in one place. “We’re letting customers create their own insights,” Juan Carlos says.


It’s a big step forward. Instead of exporting to external tools like Power BI, users can now explore and answer questions right inside the product. With ClickHouse Cloud as the backbone, Lansweeper is evolving from an inventory tool into a true insights platform, helping customers stay ahead in modern IT environments that can change on a dime.


*See how ClickHouse Cloud can power real\-time analytics at scale—[try it free for 30 days](https://clickhouse.com/cloud).*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
