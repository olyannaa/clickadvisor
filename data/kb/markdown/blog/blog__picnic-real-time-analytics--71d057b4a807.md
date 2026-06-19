# How Picnic uses ClickHouse for real\-time analytics across 20\+ fulfillment centers and 1 million unique stores


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Picnic uses ClickHouse for real\-time analytics across 20\+ fulfillment centers and 1 million unique stores

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 16, 2026 · 10 minutes read## Summary


div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Picnic uses ClickHouse Cloud to power real\-time analytics across 20\+ highly automated fulfillment centers and millions of unique shopping journeys. They migrated from TimescaleDB, reducing operational complexity and enabling widespread adoption through self\-service dbt models and SQL\-based dashboards. Today, the platform supports thousands of Grafana views, continuous event ingestion, and rapid dbt model growth across both warehouse and application analytics.

If you've been to the Netherlands, Germany, or France lately, you’ve probably seen [Picnic](https://picnic.app/)’s little electric trucks zipping through neighbourhoods. The company calls itself an “online everything store,” but in practice it behaves like a million tiny supermarkets—one for every customer.


As software engineer Max Sumrall explains, people don’t come to Picnic once a year to buy a new laptop or TV. They show up every week, often for just a few minutes, to order the exact mix of diapers, vegetables, snacks, and treats that fits their life at that moment. “Someone might only want to order vegan food, or maybe someone really likes hamburgers,” he says. “You need to customize this ecommerce experience for everyone individually.”


Not only is that a lot of customer data to parse, the entire experience runs on a tightly orchestrated supply chain. Picnic is a fully integrated operation with highly automated fulfillment centres, each with kilometers of conveyor belts and robot arms picking orders, not to mention a fleet of more than 5,000 trucks handling the last mile. And they don’t just say “we’ll be there in the afternoon.” As Max says, “We promise a specific 20\-minute delivery slot. There’s a lot of data we need to keep track of to make sure we’re there on time.”


At our Open House Roadshow in Amsterdam, Max walked through how Picnic coordinates all of this information across 20\+ fulfillment centers—and how they use [ClickHouse Cloud](https://clickhouse.com/cloud) to power a real\-time analytics platform that keeps the entire operation running on schedule.


## Why real\-time matters for Picnic [\#](/blog/picnic-real-time-analytics#why-real-time-matters-for-picnic)


Picnic’s fulfillment centers are unique ecosystems, each with their own layout, product assortment, staffing structure, and quirks. But one thing they all share is *pressure*. Orders need to be picked, packed, loaded, and dispatched fast enough to fit within those specified delivery windows. On the warehouse floor, there’s no shortage of questions: Are we on time or running behind? What products are in stock? What’s out of stock? Who’s working where? Which orders are already in progress, and which ones need attention now?


“You have all these people working to get your orders fulfilled,” Max says. “We need real\-time analytics to make sure that process happens on time.”


For Picnic, the major challenge was scale and variability. From Utrecht to Oberhausen, each warehouse has its own requirements, particularly when it comes to data. “You need a lot of customization to get every warehouse running,” Max says. “It’s not going to be sustainable for a team of engineers to build custom solutions for every single warehouse. Because we’re not working on the warehouse floor, we don’t know exactly what they need.”


So Max and the team built a self\-service platform that provides real\-time information on supply chain operations. They call it the real\-time insights (RTI) platform—a system that ingests operational events from across the business and turns them into metrics and dashboards that warehouse teams can use without developer support.


Analysts and floor teams can define the views they need themselves, tracking everything from progress against forecasted order volumes to zone\-level performance in chilled and ambient areas. These dashboards give teams immediate, shift\-by\-shift feedback on whether they’re ahead or behind schedule and what needs attention next.


## Picnic’s ClickHouse\-based architecture [\#](/blog/picnic-real-time-analytics#picnics-clickhouse-based-architecture)


The RTI platform’s architecture is “not exactly rocket science,” Max says. Even so, it gives Picnic a scalable, reliable foundation for turning a continuous stream of operational events into real\-time insight across the entire fulfillment network.


![Picnic User Story Issue 1220 (2).jpg](/uploads/Picnic_User_Story_Issue_1220_2_56adc0da5a.jpg)
Picnic’s real\-time data pipeline, with events processed in ClickHouse and visualized in Grafana.


It starts with the event sourcing layer. This includes Java backend services emitting operational events, mobile apps sending clickstream data, and slow\-moving dimensional data tracking things like product assortment, vehicle information, and warehouse layout.


Next is a transport layer built on RabbitMQ and Apache Kafka, with the occasional direct HTTP call when that’s the simplest operation. Rather than wiring every application directly to ClickHouse, Picnic runs a dedicated Java ingestion service (“essentially our own version of [ClickPipes](https://clickhouse.com/cloud/clickpipes),” Max calls it, adding, “maybe we’ll switch one day”) that knows how to read from each queue, topic, or endpoint and land data consistently in ClickHouse.


Once data is inside ClickHouse, the event processing layer transforms and aggregates the raw events. As Max explains, [materialized views](https://clickhouse.com/docs/materialized-views) act like “database triggers”—data lands in a source table, and the view immediately inserts a parsed, query\-ready version into a downstream table. “Every event always comes first through a [materialized view](https://clickhouse.com/docs/materialized-views),” he says. Because this system predates ClickHouse’s [JSON data type](https://clickhouse.com/docs/sql-reference/data-types/newjson), raw payloads are stored as strings for now. For more complex transformations and aggregates, Picnic uses [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view).


ClickHouse also acts as the serving layer, with different [table engines](https://clickhouse.com/docs/engines/table-engines) tailored for different jobs. Given the team’s familiarity with Postgres and Snowflake, they were able to ramp up quickly. “ClickHouse is written in SQL, so it’s really easy for analysts to get up to speed,” Max says. “It works really well for experimental use cases and people trying new queries on the fly, while also being there for all of the use cases we’ve developed that are operationally crucial.”


On top of that sits the visualization layer. Grafana connects directly to ClickHouse, and teams build panels using SQL. “We use Grafana for our operational dashboards to keep track of what’s going on,” Max says. “It’s pretty capable, and the [integration with ClickHouse](https://clickhouse.com/docs/observability/grafana) works well.”


To keep the platform self\-service, Picnic treats all data models as code. Analysts define new models in dbt, submit them through GitHub pull requests, and automated checks validate schemas, business rules, and downstream dependencies. “We wanted something a business analyst can use themselves, not something an engineer has to maintain,” Max says. He adds that [dbt and ClickHouse](https://clickhouse.com/docs/integrations/dbt) “work really well together,” allowing the team to redeploy models or even replay the entire pipeline from Kafka retention when needed. Slack notifications close the loop, alerting analysts when models are deployed or when data quality issues arise.


## The advantages of ClickHouse [\#](/blog/picnic-real-time-analytics#the-advantages-of-clickhouse)


Picnic’s RTI platform actually didn’t start with ClickHouse. The first version ran on TimescaleDB, which Max calls “very fast with good query performance.” But, he says, “it’s very complex to get going and can be hard to use as a platform because you need a lot of expertise.”


ClickHouse offered the combination of performance, cost\-efficiency, and usability they needed. As Max puts it, “ClickHouse is very easy to operate. It’s very cost\-effective, with things like TTLs. Scaling is really simple with ClickHouse Cloud. We’re very happy with it.”


Since rebuilding around ClickHouse two years ago, adoption has surged. “It basically unhooked adoption from needing developer support,” Max says. “You can see that with the amount of data we store in ClickHouse versus Timescale, which really took off once we switched.”


![Picnic User Story Issue 1220.jpg](/uploads/Picnic_User_Story_Issue_1220_5730066c08.jpg)
Picnic’s dbt model count accelerated sharply after adopting ClickHouse for real\-time analytics.


![Picnic User Story Issue 1220 (1).jpg](/uploads/Picnic_User_Story_Issue_1220_1_edea0aa714.jpg)
ClickHouse unlocked rapid dbt model growth across warehouse and app analytics workloads.


ClickHouse’s flexibility has also proved to be an advantage. When Picnic needed fine\-grained access control to support GDPR, for example, the team used the [getClientHTTPHeader function](http://getClientHTTPHeader) alongside Grafana’s Keycloak integration and ClickHouse [row\-level policies](https://clickhouse.com/docs/sql-reference/statements/create/row-policy). User identity flows in via HTTP headers; [dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries) and policies translate it into table\-level and row\-level permissions. It’s an unusual pattern, but one ClickHouse already had the pieces to support.


“What’s cool about ClickHouse is there are lots of random little things they’ve built over the years,” Max says. “If you need something, you can always start searching GitHub pull requests and issues, and you’ll see some long discussion from 10 years ago with Alexey and other engineers, and then you find out, ‘Oh, there’s a tool for that.’”


## What’s next for Picnic’s real\-time platform [\#](/blog/picnic-real-time-analytics#whats-next-for-picnics-real-time-platform)


Today, ClickHouse ingests and aggregates events; tomorrow, it may also act as a stream processor. The Picnic team is currently experimenting with [RabbitMQ](https://clickhouse.com/docs/engines/table-engines/integrations/rabbitmq) and [Kafka table engines](https://clickhouse.com/docs/engines/table-engines/integrations/kafka) hooked up to [materialized views](https://clickhouse.com/docs/materialized-views) that transform events and write their outputs into downstream Kafka topics. In that model, ClickHouse becomes both the brain of the analytics platform and an active participant in event\-driven workflows. “If this takes off, we might have some future requests to the ClickHouse team,” Max says with a smile.


The team is also exploring how AI can support developers and analysts inside Picnic’s workflow. A new experiment combines dbt’s rich metadata (e.g. models, dependencies, examples) with ClickHouse data using the [ClickHouse MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp) and a GitHub action powered by Claude Code. As Max explains, “You can give the context of all your dbt models to the AI and see if it can help you generate new models, validate the models you want to create, or suggest answers to queries.”


These new initiatives, he says, are a “natural step forward” from what Picnic has already built: a powerful real\-time analytics platform that keeps operations running smoothly across 20\+ fulfillment centers, with ClickHouse at its core.

### Ready to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-590-ready-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=590)**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.


![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
