# Rill and ClickHouse: real\-time operational BI for a metered world


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Rill and ClickHouse: real\-time operational BI for a metered world

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 1, 2026 · 9 minutes readModern business is becoming increasingly granular. Cloud providers record usage down to individual operations. Payment platforms track transactions in real time. AI systems meter tokens, requests, and compute consumption. What started as observability inside IT systems has spilled outward, turning the rest of the business into a living stream of events.


"We have this sort of mirror digital universe, where everything we do is an event," says Mike Driscoll, co\-founder and CEO of [Rill](https://www.rilldata.com/), an operational BI\-as\-code tool focused on [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics). "And when we have this data, we want to make sense of it."


As Mike puts it, the challenge isn't collecting data so much as understanding how it fits together. A company might see cloud costs in AWS or Google Cloud, revenue in Stripe, and product usage tracked somewhere else entirely, yet none of these systems explain how the business is doing as a whole. "You can't rely on another company's dashboard to make sense of your business," he says. "Ultimately, you have to integrate all of that data yourself."


BI tools like Rill have emerged as a way to bridge that gap, bringing operational and financial data together so teams can understand what they're spending and why. But that approach requires analytics systems capable of aggregating huge volumes of data quickly and efficiently. "ClickHouse is amazing at doing aggregation at massive scale," Mike says.


At a [December 2025 ClickHouse meetup in San Francisco](https://clickhouse.com/videos/meetupsf_dec_20253), Mike shared how Rill combines declarative ingestion with dlt, high\-performance aggregation in ClickHouse, and a metrics\-first operational BI layer to build a system designed to make sense of a metered world.



## A fast BI tool for real\-time databases [\#](/blog/rill#a-fast-bi-tool-for-real-time-databases)


Rill's approach to analytics grew out of more than a decade spent working on real\-time event data at scale. In 2010, Mike co\-founded Metamarkets, the company behind Apache Druid, one of the first databases built for interactive analytics on streaming data. After Metamarkets was acquired by Snap in 2017, Mike and Nishant Bangarwa founded Rill in 2020, applying what they had learned building analytics infrastructure to rethink BI for a real\-time world.


Today, Rill processes more than 100 billion daily events across thousands of users, serving digital media giants such as Bloomberg and Comcast, large enterprises like AT\&T, and a growing number of fintech and ecommerce companies. "A lot of our customers look like the kinds of customers that love and use ClickHouse," Mike says. "So it's no accident that we found a great fit using ClickHouse as our database."


Rill takes a BI\-as\-code, developer\-friendly, and agent\-first approach. Data sources, transformations, and business logic are defined as code, allowing teams to develop with modern tools like Cursor, version changes through Git, and deploy analytics the same way they ship software. "We really are proponents of this declarative data stack," Mike says. "Between SQL and YAML, you can build [data applications](https://clickhouse.com/resources/engineering/data-application), not just dashboards."


That philosophy extends into Rill's metrics\-first design. Teams declare metrics using SQL expressions, creating a shared semantic layer from which dashboards are generated, not created. As Mike says, this becomes increasingly relevant as AI and conversational analytics enter the workflow. "SQL is valuable," he explains, "but it turns out agents do a lot better when they've got something like a semantic layer to interact with."


Underneath it all is real\-time performance. Traditional BI tools often treat heavy queries as something to be avoided, relying on caching to keep dashboards responsive. "But when you're using something like ClickHouse," Mike says, "there's no need to avoid hitting the dashboard hundreds or thousands of times." For Rill's customers, that translates into instant drilling, slicing, and dicing, alongside fast conversational agents that operate directly on live data.


As Mike puts it, "Because we've built around a real\-time database like ClickHouse, we're able to do things other dashboards wouldn't even attempt to do."


## Inside Rill's ClickHouse\-based architecture [\#](/blog/rill#inside-rills-clickhouse-based-architecture)


Rill's architecture keeps analytics close to the database while defining everything else as code. Instead of introducing new layers between ingestion, modeling, and analysis, the system connects them into a single workflow built around declarative configuration.


![](/uploads/Rill_User_Story_Issue_1250_0_7064f28ae6.png)
*Rill's architecture: declarative data ingestion, ClickHouse\-powered aggregation, and operational BI.*


Data ingestion is orchestrated using software like dlt (data load tool), an open\-source Python framework for declarative data loading. Operational databases, object stores, data lakes, and warehouses are extracted through reusable connectors, with transformations and source credentials defined in SQL and YAML. Rather than maintaining custom pipelines, teams describe how data should move, and dlt handles extraction and loading into ClickHouse automatically.


Once loaded, ClickHouse serves as the [analytical engine](https://clickhouse.com/resources/engineering/what-is-columnar-database), with queries executing directly against large\-scale event data. Business logic is expressed through measure expressions and dimension metadata, compiled into SQL models that power aggregations at query time. These definitions form the shared metrics layer, ensuring dashboards, APIs, and programmatic access all rely on the same logic.


Atop this foundation sits Rill's operational BI layer, where role\-based security policies and dashboard configurations are also defined as code. Because dashboards are generated from metric definitions rather than built manually, analytics applications remain lightweight interfaces querying ClickHouse in real time.


The result is a composable system where data flows from source systems into ClickHouse, delivering interactive analysis to product, operations, and finance teams, as well as external partners, without duplicating business logic across tools.


## How BI\-as\-code works in practice [\#](/blog/rill#how-bi-as-code-works-in-practice)


At the meetup in San Francisco, Mike fired up his laptop and walked through a live demo. "We were inspired by how easy it is to launch ClickHouse on your local machine," he said, noting that, like ClickHouse, Rill lets developers start a local instance that runs in the browser, connecting to either a local ClickHouse database or [ClickHouse Cloud](https://clickhouse.com/cloud).


The demo centered around three core building blocks inside Rill: sources, metrics, and dashboards. Mike began by loading roughly a million rows of Google Cloud usage data from a Parquet file. He then used an agent\-assisted workflow to generate the YAML configuration needed to ingest the dataset into ClickHouse.


Once connected, Rill analyzed the table structure and generated metric definitions and dashboards automatically. Within seconds, he could explore cloud spending trends—drilling into services, zooming across time ranges, and slicing costs by dimension—all backed by ClickHouse queries. "What's great is how easy and fast it is," Mike says.


With Rill, developers can use AI\-assisted coding tools to define configurations as code. In his demo, Mike used Cursor to generate ingestion syntax, adjust formatting, and modify dashboards. Tasks that once required extensive UI configuration, like changing currency formatting across dashboards, can be done in seconds. "That's the difference between BI\-as\-clicks and BI\-as\-code," he says.


As Mike explained, development happens locally first. Teams iterate against small data partitions, validate metrics, and commit changes to Git before deploying to the cloud. Once deployed, the same definitions power conversational analytics layered on top of the data.


Mike demonstrated this by asking natural\-language questions about cost increases across cloud providers. While conversational BI, he notes, has become relatively common ("everyone's seen a demo of a chatbot slapped over some data"), he emphasized two constraints that determine whether it actually works in practice.


First, text\-to\-SQL approaches don't always scale in real production environments. "If you've got hundreds of tables, you just see the agent get lost," Mike says. "It's like throwing a data engineer at a problem and saying, 'Hey, figure out why our cloud costs are up.'"


Second, interaction speed matters as much as correctness. "You've got to have high performance in the back end," he says. "If you were to throw Rill at [Snowflake or Redshift or BigQuery](https://clickhouse.com/resources/engineering/top-5-cloud-data-warehouses), the answers would just take forever to come back."


At the end of the day, trust comes from traceability as much as intelligence. In Rill, each generated insight links back to the underlying dashboard and query results, allowing users to verify conclusions rather than treating AI responses as opaque outputs. "You've got to have trustworthy results," Mike says. "You've got to have verifiability."


## Analytics for a fully metered world [\#](/blog/rill#analytics-for-a-fully-metered-world)


Imagine the workflow Mike described running continuously inside a real organization. Cloud billing exports land in object storage, operational data flows in from APIs, and declarative pipelines stream everything into ClickHouse, where aggregations happen in real time. Metrics defined once become dashboards automatically, and teams across product, operations, and finance explore the same underlying data through a shared analytical layer.


What once required a patchwork of ETL jobs, semantic layers, and dashboard tooling converges into a unified workflow, defined and maintained largely as code.


![](/uploads/Rill_User_Story_Issue_1250_1_59c5095254.png)
*FinOps in practice: declarative ingestion, real\-time aggregation, and operational BI in Rill.*


Taken together, Rill and ClickHouse point toward a new model for analytics, built for a world where every business process generates events. Teams can stay on top of operations by querying live systems, iterating locally, and deploying analytical logic the same way they ship software.


As organizations become increasingly measured in real time, analytics shifts from retrospective reporting to operational decision\-making. Declarative data movement, high\-performance aggregation, and metrics\-first design make it possible to treat analytics not as a separate destination, but as infrastructure running alongside the business itself.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-297-get-started-today-sign-up&utm_blogctaid=297)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
