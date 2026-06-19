# From Rockset to ClickHouse: How Lens made its database faster and more efficient


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# From Rockset to ClickHouse: How Lens made its database faster and more efficient

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 1, 2024 · 8 minutes read[Lens](https://www.lens.xyz/) is an open social protocol where all content and interactions are stored on the blockchain. Lens provides users ownership and control over their profile, social graph, and data while providing a technology stack that enables developers to build social applications of their choice on Lens.


Like other social networks, Lens Protocol relies heavily on machine learning to create a more relevant, enjoyable, and trustworthy user experience. As the Lens team explains, Lens’ ML systems handle everything from feed ranking algorithms that decide the order in which content is displayed to users, to sophisticated bot detection mechanisms that identify and mitigate malicious activity.


Every day, the Lens team computes and evaluates hundreds of features across various time periods to assess user behavior and content interactions. This includes a mix of heavy batch jobs, which run periodically to update models and features, and lighter, real\-time jobs, such as reply ranking, which require instant processing with lower latencies to provide immediate feedback.


The team initially relied on Postgres and Rockset to support their data needs. However, after struggling with data ingestion delays and query concurrency limits under their old setup they turned to ClickHouse Cloud for a faster, more efficient data operation.


## Hitting the limitations of Postgres [\#](/blog/rockset-migration-to-clickhouse-lens#hitting-the-limitations-of-postgres)


Lens Protocol is built on the [Polygon blockchain](https://en.wikipedia.org/wiki/Polygon_(blockchain)) but is transitioning to the [Lens network](https://x.com/LensProtocol/status/1790458242855751950) in Q4 2024\. Originally, Lens used a simple Postgres database to manage user interactions and content. Instead of traditional RPC endpoints, a GraphQL API was implemented to make it easier for integrators (developers building on Lens Protocol) to interact with the blockchain and build front\-end applications.


According to the Lens team, this worked well initially. But as the platform grew, and as integrators requested more complex features, Postgres’s limitations became apparent. The data science team transitioned to Rockset, which offered better data processing capabilities, particularly for complex queries and aggregations.


## Performance challenges with Rockset [\#](/blog/rockset-migration-to-clickhouse-lens#performance-challenges-with-rockset)


Even after transitioning to Rockset, however, new challenges emerged. To ingest data from Postgres into Rockset, they had to use [AWS Database Migration Service](https://aws.amazon.com/dms/) (DMS) in conjunction with [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/). This process involved capturing changes from Postgres using DMS and then streaming that data through Kinesis to reach Rockset.


The Lens team found that having multiple layers added a lot of latency in terms of synchronization. The process added several seconds, sometimes even minutes of latency. For real\-time jobs, that was a big problem.


Another significant challenge the Lens team describes were the Rockset concurrent query limits. Rockset had predefined limits on the number of queries that could be executed simultaneously; when these limits were reached, Lens could either upgrade to a more expensive plan — which they did several times until costs became unfeasible— or additional queries had to wait, leading to delays in data processing. This was especially problematic for real\-time machine learning tasks, where timely data retrieval and processing are key. They tried custom solutions to work around these limits, but not only did the constraints persist, but they added complexity to the overall architecture, especially as Lens’ data processing demands grew.


Thus, the Lens team found itself in a process of finding a better database management solution.


## Migrating from Rockset to ClickHouse [\#](/blog/rockset-migration-to-clickhouse-lens#migrating-from-rockset-to-clickhouse)


As they explored Rockset alternatives for Lens, the team briefly considered Amazon Aurora, spinning up RDS clusters to manage their immediate data needs. However, Aurora was viewed as insufficient for Lens’ long\-term needs. They knew they needed a database that could handle high\-speed queries and scale efficiently as Lens Protocol grew.


A few weeks earlier, Lens had begun using ClickHouse for a different project. Their main requirement for that project was a database that could do raw queries as fast as possible. As a member of the Lens team said, “If the one metric you’re looking for is query speed, you go to ClickHouse.”


Based on their early experience with ClickHouse, they began exploring using it for Lens Protocol. At first, they looked into deploying it using the Kubernetes operator and managing it themselves. However, after learning more about [ClickHouse Cloud](https://clickhouse.com/cloud) and seeing how cost\-effective and simple it was to get started, they opted for the cloud offering.



> “Databases are never really fun to run,” a team member explains with a laugh. “As a managed service, ClickHouse Cloud takes a lot of the load off our shoulders.”


They developed a quick proof of concept, setting up data synchronization between the existing Postgres database and ClickHouse. They used [PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) to manage the CDC process, efficiently streaming updates from Postgres to ClickHouse without the need for complex custom configurations. By creating data mirrors and configuring the necessary helm charts, they had a fully functional setup in no time.


As a Lens team member said, “The integration was so fast. It only took a day or two to implement.”


The team describes the migration as “seamless.” With most of their data already migrated and operational in ClickHouse, the team is now focused on adapting and rewriting the existing code that previously relied on Rockset’s API to work with ClickHouse’s API.


According to Lens, this went faster than expected because they didn’t have to build a lot of the methods around libraries that were needed with Rockset. They just needed to handle the queries and data insertion, without worrying about scaling the VIs or other complexities. The PeerDB integration made the process even smoother since both systems were built for each other.


![Avara customer story.png](/uploads/Avara_customer_story_11501b204c.png)
## A massive improvement with ClickHouse [\#](/blog/rockset-migration-to-clickhouse-lens#a-massive-improvement-with-clickhouse)


The transition to ClickHouse has already brought major benefits to Lens Protocol’s data operations. By eliminating the multiple layers of data transfer previously required with Rockset, the team has enabled near\-instantaneous data processing. Ingestion times for tables with tens of millions of rows, which clocked in around 24 hours with Rockset, are now just 1\-2 hours with ClickHouse and PeerDB.



> As a team member said, “We’ve reduced friction. Rather than having three tools that kind of work together, we've now got ClickHouse and PeerDB which are purpose\-built for each other. It's made our lives easier, and it fully eliminated the latency issue.”


ClickHouse’s ability to handle a high volume of concurrent queries without performance degradation is another big advantage. Unlike Rockset, where query limits hindered the Lens team’s work and led to frustrating bottlenecks, ClickHouse allows the team to scale their ML operations as Lens Protocol grows. The additional capacity will improve the speed and efficiency of their data processing workflows, allowing the team to support more complex features and improve the overall user experience on the platform.


“We want to serve as many requests as possible,” said a team member. “We are very happy with what ClickHouse gives us.”


## Lessons learned migrating from Rockset to ClickHouse [\#](/blog/rockset-migration-to-clickhouse-lens#lessons-learned-migrating-from-rockset-to-clickhouse)


Looking back on the migration, one big lesson learned was the value of rapid prototyping. It was easy to get started and develop a POC with ClickHouse, which allowed Lens to quickly test and validate its performance.


“Using the product is always better than reading documentation and building architecture diagrams. Using the product is the easiest way to know if something will work.”


The Lens team also reflects on the importance of platform engineering and choosing long\-term, scalable solutions that work well together.


Moving forward, Lens is excited about the possibilities that ClickHouse unlocks for Lens Network and its future social products. This includes developing a [feature store](https://clickhouse.com/blog/powering-featurestores-with-clickhouse) to streamline the management and reuse of features across different machine learning models, enhancing consistency and accelerating the deployment of new ML solutions.


With the migration to ClickHouse Cloud, Lens is well\-positioned to scale data operations as they transition to the Lens network. Along with the value ClickHouse has provided in terms of performance and efficiency, the Lens team recognizes the scalability and sense of assurance the migration has provided.


As a member of the team said, “You get this good gut feeling as a developer when things work and they're easy. We didn’t have to go through a big process, finding weird bugs. ClickHouse gave us confidence that we made the right decision and this can scale.”

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
