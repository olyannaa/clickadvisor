# How Rapid Delivery Analytics tracks real\-time CPG performance with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Rapid Delivery Analytics tracks real\-time CPG performance with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 6, 2025 · 7 minutes readIn recent years, the rise of rapid delivery (also known as quick commerce or “q\-commerce”) has changed how people shop for groceries and convenience goods. Apps like Uber Eats, Flink, and DoorDash now deliver everything from cereal to shampoo in under two hours.


But while shoppers love the convenience, consumer packaged goods (CPG) brands have struggled to keep up. With dozens of apps and hundreds of thousands of delivery zones, it’s hard to know where products are showing up, let alone how they’re performing.


[Rapid Delivery Analytics](https://rda.team/) (RDA) is out to change that. The Paris\-based startup offers a digital shelf analytics platform built specifically for rapid delivery, giving brands real\-time visibility into stock levels, search rankings, pricing, promotions, and more. With coverage across more than 40 delivery apps in over 100 countries, it helps global CPG brands like PepsiCo and Unilever stay on their game in a frenetic, fragmented channel.


We caught up with RDA co\-founder and CEO Andrey Dyatlov to talk about the role of data in rapid delivery, why his team chose ClickHouse to power their analytics engine, and how [ClickHouse Cloud](https://clickhouse.com/cloud) on AWS has become core to their platform as they scale.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Built for speed from day one [\#](/blog/rda-tracks-real-time-cpg-performance-with-clickhouse#built-for-speed-from-day-one)


For nearly a decade, Andrey and his co\-founder Vlad Gafarov have worked with the world’s biggest CPG brands, helping them navigate the evolving world of ecommerce. But when COVID\-19 hit, everything changed. Traditional sales and merchandising models no longer applied. “We had to find a new way to work with them,” Andrey recalls. “We needed to rethink what to build, and how we could keep supporting them based on our experience.”


In early conversations with clients, one theme kept coming up: a new wave of ecommerce was taking shape around ultra\-fast, mobile\-first delivery. New platforms were launching overnight, promising groceries and convenience goods in just a few hours. At the same time, traditional retailers were racing to establish their own presence in the space. “But for the brands—our customers—it was all a black box,” Andrey says.


From the start, the team understood that rapid delivery was unlike any other ecommerce channel. While most analytics tools were built for traditional ecommerce or brick\-and\-mortar channels, RDA focused on the unique challenges of q\-commerce: extreme geographic granularity, fast\-changing assortments, and the need to monitor everything from pricing and promotions to search performance in near real time. “We saw a huge opportunity to create a solution for this particular side of ecommerce,” Andrey says.


They began building with Postgres, a familiar choice. But as Andrey puts it, “It didn’t take long to realize something had to change.” As data volumes grew and customer expectations rose, the team needed an architecture that could scale with them over the long run.


## ClickHouse Cloud enters the chat [\#](/blog/rda-tracks-real-time-cpg-performance-with-clickhouse#clickhouse-cloud-enters-the-chat)


The team began to rethink the fundamentals of their stack. Postgres had worked “quite well” early on, Andrey says, especially when paired with TimescaleDB. But it was ultimately built for transactional (OLTP) workloads, not the kind of analytical (OLAP) queries RDA needed to run across billions of rows. “We needed a better way to run OLAP queries,” he says.


Several team members were already familiar with ClickHouse, so they started with a self\-hosted deployment. The results were positive: faster queries, better compression, and a structure that fit their high\-volume, time\-based metrics. They also tested Amazon Redshift as part of the evaluation, but it didn’t stick. “We didn’t find anything that caught our eye,” Andrey says.


While ClickHouse met their performance needs, running it themselves introduced new challenges. Their workloads weren’t static: some jobs required short bursts of intense compute, while others needed to stay lean. “That’s where ClickHouse Cloud entered the chat, so to speak,” Andrey says. “We needed the API to upscale and downscale really fast, so we could run a lot of aggregations, then downscale again.”


ClickHouse Cloud’s flexibility helped unlock new efficiencies. “It’s about cost savings,” Andrey explains. “And it’s about having the extra capacity available anytime, which is really, really helpful when we have something important to do with this amount of data.”


## Real\-time analytics at scale [\#](/blog/rda-tracks-real-time-cpg-performance-with-clickhouse#real-time-analytics-at-scale)


Today, ClickHouse Cloud powers the core of RDA’s analytics engine, from data ingestion and aggregation to the dashboards brands rely on for daily decisions. The platform ingests more than 500 GB of raw data per day, covering 40\+ apps, hundreds of thousands of delivery zones, and billions of product listings. “The amount of data is insane, to be honest,” Andrey says.


ClickHouse plays a central role in processing and aggregating that data efficiently. RDA uses it to calculate key metrics on a daily basis, storing the results in a format optimized for fast access by both internal teams and external users. For clients who need direct access, RDA exports data from ClickHouse to S3, Postgres, or other downstream systems.


Performance has been impressive. Aggregations that span billions of rows complete in under an hour, and search queries typically return in less than a second. As Andrey explains, that kind of speed matters, especially for clients with real\-time alerting or transactional workflows tied to data. “Some of our clients have a transactional model where they need to pull something from the table quickly, as part of an alerts pipeline or similar use case,” he says. “That low\-latency access is important for them and for us.”


## Growing without slowing down [\#](/blog/rda-tracks-real-time-cpg-performance-with-clickhouse#growing-without-slowing-down)


Currently, RDA is adopting one of ClickHouse Cloud’s newest features: [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud). The team is isolating ingestion from analytics, giving each workload its own dedicated resources. That means keeping a lightweight service running continuously for ingesting data, while scaling up compute only when needed for heavy aggregations or client\-facing queries. “This will save us a lot of time and money,” Andrey says.


For a data\-heavy startup in a fast\-moving space, that kind of flexibility is essential. ClickHouse Cloud has already helped RDA ingest, aggregate, and query billions of rows daily without performance trade\-offs or infrastructure complexity. Now, with features like workload isolation and autoscaling, the team has even more control as they grow, onboard new customers, and expand globally, without needing to operate like a large enterprise.


“We’re still a startup, but we work with very big companies,” Andrey says. “ClickHouse Cloud is the core of our solution. It gives us the kind of capabilities and infrastructure you’d expect from a much bigger, better\-known corporation, while still letting us stay lean.”

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
