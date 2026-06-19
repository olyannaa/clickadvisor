# How Superwall uses WarpStream and ClickHouse Cloud to scale subscription monetization


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Superwall uses WarpStream and ClickHouse Cloud to scale subscription monetization

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)ClickHouse and ConfluentSep 23, 2025 · 9 minutes read[Superwall](https://www.superwall.com/) is a small team doing big things. With only 14 people, the company powers paywall monetization for hundreds of mobile subscription apps that reach billions of end users.


The pitch is straightforward: install Superwall’s SDK once, and you can instantly A/B test checkout flows, adjust pricing globally, and roll out discounts, all without shipping an app store update. As co\-founder and CTO Brian Anglin explains, at the heart of the platform is a focus on continuously balancing supply and demand. “With digital products, usually you have high fixed costs and low variable costs,” he says. “You want to be able to accept any offer without cannibalizing customers who would have paid more.”


But that type of experimentation and optimization at scale is anything but simple. Every paywall view, conversion, and experiment generates an event that must be captured, streamed, and analyzed in near real\-time. Dashboards have to update in seconds so customers can see results. To ingest 100 MB of events per second and store 300\+ TB of data, Superwall needed a stack that was fast, durable, and perhaps most importantly, low maintenance.


We caught up with Brian to learn how they landed on [WarpStream](https://www.warpstream.com/) and [ClickHouse Cloud](https://clickhouse.com/cloud), how their stack has evolved over the past few years, and the missing piece that finally tied it all together.


## Getting started with Apache Kafka® and ClickHouse [\#](/blog/superwall-warpstream-clickhouse-cloud-monetization#getting-started-with-apache-kafka-and-clickhouse)


When Superwall first began building its platform, the team had two main needs: a reliable data streaming backbone to handle the flood of events from its SDK, and an analytical database that could make sense of those events quickly enough to power customer dashboards. “We didn't want to settle for hourly or daily roll ups,” Brian says. “We wanted something near real\-time.”


On the streaming side, Kafka compatibility was important. “It really sucks to lose data, and we also make mistakes,” he says. By turning up retention, the team could replay events if something broke or reprocess data when new use cases emerged. That durability gave the team confidence to move quickly.


For analytics, they chose [ClickHouse](https://clickhouse.com/). Blog posts from PostHog and Cloudflare—including one showing [how Cloudflare processed 6 million requests per second](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse/)—gave Brian confidence it could handle web\-scale workloads. “I was like, ‘If their Kafka\-plus\-ClickHouse stack can do that, it’ll be enough for our piddly little SDK with, like, one customer,” he jokes.


ClickHouse’s [materialized views](https://clickhouse.com/docs/materialized-views), he says, were like “magic.” Instead of writing custom jobs to update counters or roll up metrics, the team could lean on ClickHouse to pre\-aggregate in real time. “When I realized I could do that with SQL, I was like, oh, this is so much easier.”


[Compression](https://clickhouse.com/docs/data-compression/compression-in-clickhouse) was another unexpected win, allowing the team to store huge amounts of data without jacking up costs. “I was shocked by the compression ratios we were able to achieve,” Brian says. “You don’t get that for free in any other database systems.”


The initial production stack was simple: Kafka up front, ClickHouse on a single EC2 instance behind it. “Once we had those two things working,” Brian says, “we started writing queries against it and had everything we needed to deliver a super simple MVP that was more real\-time than anyone else in the space.”


## Evolving with WarpStream and ClickHouse Cloud [\#](/blog/superwall-warpstream-clickhouse-cloud-monetization#evolving-with-warpstream-and-clickhouse-cloud)


Within a few months, however, the limits of that early stack started to show. With ClickHouse running on EC2, disk space was a constant headache. “I’d find myself over and over trying to resize the instance,” Brian recalls. “It became this background task I was always thinking about.”


They turned to a third\-party ClickHouse consulting company, which solved some problems but introduced others, including cost. “When I actually did the math about what we were paying between compute, backups, the managed service, and S3 usage in our own AWS account, it got really, really expensive,” he says.


As they looked for a better long\-term foundation, [ClickHouse Cloud](https://docs.google.com/document/u/0/d/1VZYKrf8OQnYLIywxa1mRR4F7MWSq8O-MBLvux72ZtK0/edit) became the logical next step for analytics. Its [separation of storage and compute](https://clickhouse.com/docs/guides/separation-storage-compute) promised to eliminate the endless disk resizing, while [SharedMergeTree](https://clickhouse.com/docs/cloud/reference/shared-merge-tree) offered elastic scaling that could flex with demand. Just as important, the pricing model aligned with their usage. “Being able to just charge my credit card and have more storage was pretty compelling,” Brian says.


On the streaming side, [WarpStream](https://www.warpstream.com/) (which was [acquired by Confluent](https://www.confluent.io/blog/confluent-acquires-warpstream/) in September 2024\) emerged as the answer. It preserved Kafka compatibility—meaning no rewrites—while introducing a bring\-your\-own\-cloud model that made it cheaper and easier to run at scale. “Unlike trying to run Kafka locally, I ran the little agent demo and it just worked,” Brian says. “It was so refreshing to have a Kafka\-compatible API running out of the box.”


Together, ClickHouse Cloud and WarpStream offered Superwall the scalable, cost\-effective, ops\-light stack it needed to keep up with growth. There was only one missing piece...


## Ingesting from WarpStream to ClickHouse with ClickPipes [\#](/blog/superwall-warpstream-clickhouse-cloud-monetization#ingesting-from-warpstream-to-clickhouse-with-clickpipes)


Before Superwall could fully migrate to the new ClickHouse\-Cloud\-plus\-WarpStream stack, they needed a reliable way to move data between the two without taking on operational overhead. Any break in ingestion risked leaving customer dashboards stale.


They had previously relied on the Kafka table engine in ClickHouse OSS. However, this approach provided limited monitoring, lacked notifications, and coupled scaling to the ClickHouse server—too many gray areas. “Every time something broke, the question was always, did everything stop? Or did reporting just stop?” Brian says. Running connectors themselves wasn’t appealing either. “I just wasn’t confident we could do it perfectly.”


[ClickPipes](https://clickhouse.com/cloud/clickpipes) offered a much better and fully managed way. By streaming data directly from Kafka\-compatible sources like WarpStream into ClickHouse Cloud, it gave Brian and the team both durability and peace of mind. Invalid records, which once threatened to bring pipelines to a halt, now land in a dedicated [errors table](https://clickhouse.com/blog/evolution-of-clickpipes#system-tables-centralization) for review. “If something goes wrong, we can still remain available for valid records, and we have an auditable trail for what didn’t make it,” he says.


Today, ClickPipes reliably moves more than 100 MB of events per second from WarpStream into ClickHouse Cloud, feeding a dataset of over 300 TB of total data that’s growing by 40 TB each month. Instead of adding another system to build and maintain, it takes the ingestion burden off their plates, while removing the gray areas that used to slow them down. That clarity lets them stay focused on building product features and spinning up new integrations quickly, knowing the underlying pipeline is solid.


## Confluent \+ ClickHouse \= “Durable, scalable, powerful” [\#](/blog/superwall-warpstream-clickhouse-cloud-monetization#confluent--clickhouse--durable-scalable-powerful)


Even at Superwall’s scale, customer dashboards still load in seconds. Developers get the immediate visibility they need to measure the success of pricing experiments or checkout flows without delay.


For Brian, the strength of the new stack lies in its balance of durability, scalability, and simplicity. Kafka compatibility ensures no data is lost and makes it easy to reprocess streams when new use cases arise. ClickHouse’s materialized views and indexing strategies give them the performance to support complex breakdowns (like analyzing paywall conversion rates across dozens of attributes) without trade\-offs. And because the stack is fully managed, the team can focus on product innovation instead of operations.


The next diagram shows Superwall’s data stack today, powered by WarpStream and ClickHouse Cloud:


![Superwall Customer Story Diagram.png](/uploads/Superwall_Customer_Story_Diagram_19dec2ecc2.png)
“It's totally elastic,” Brian says of the new stack. “We can increase our volume as much as we want, both on the storage side and on the streaming side. And it's pretty much ops\-free, which is the goal we were trying to get to.”


With Warpstream by Confluent and ClickHouse Cloud, what was once a patchwork of managed services and constant disk resizing has become a cohesive architecture that connects streaming and analytics in a single, resilient pipeline. Asked to sum up the stack in three words, Brian pauses for a moment, and says, “Durable, scalable, powerful.”


## Helping mobile apps monetize smarter [\#](/blog/superwall-warpstream-clickhouse-cloud-monetization#helping-mobile-apps-monetize-smarter)


Today, Superwall is starting to layer on new AI\-driven features like Demand Score, which rolls countless signals into a single metric predicting a user’s likelihood to subscribe. It’s an early example of how the company plans to bring more intelligence and personalization to developers. “There’s a lot more we’ll be doing on top of Confluent and ClickHouse,” Brian says.


That solid foundation gives them the freedom to focus on what matters: building product. “We wanted to make our systems as horizontally scalable, simple, and operationally non\-intensive as possible,” Brian says. “Because for us to be successful, we don’t have to be 10x Kafka engineers or 10x ClickHouse engineers—we need to make a great product.”


Superwall’s ambitions are big, but the team remains grounded. “We’re a small team and we do the best we can,” Brian says. “But we definitely rely on great vendors and partners.” With Confluent and ClickHouse working side by side, they’re ready to keep building, iterating, and helping mobile subscription apps optimize monetization.


Ready to take your data stack to the next level? Get started with a free trial of [ClickHouse Cloud](https://clickhouse.com/cloud) and [WarpStream by Confluent](https://console.warpstream.com/signup) today.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
