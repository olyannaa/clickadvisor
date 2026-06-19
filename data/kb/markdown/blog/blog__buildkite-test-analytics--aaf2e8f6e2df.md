# How Buildkite transformed test analytics and cut costs with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Buildkite transformed test analytics and cut costs with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 27, 2026 · 11 minutes read## Summary


div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Buildkite uses ClickHouse Cloud to power real\-time test analytics, allowing customers to tag, filter, and analyze billions of test executions instantly. By shifting from Flink\-based pre\-aggregations to on\-demand ClickHouse queries, they cut infrastructure costs by five figures per month, even as ingestion quadrupled. ClickHouse Cloud simplified their stack—retiring DynamoDB, reducing Aurora and Flink spend—and now easily handles 12B monthly events and 25K/second ingestion.

If you build software at scale, there’s a good chance you already know [Buildkite](http://Buildkite). The company's CI/CD platform sits behind the pipelines of engineering organizations like Slack, Reddit, Canva, Airbnb, Shopify, and Uber. Teams use it to ship code confidently, coordinate complex CI flows, and even orchestrate AI model\-training workloads.


Within that platform, Buildkite Test Engine helps teams speed up builds by understanding their test suite. It aggregates results from thousands of builds, flags flaky tests, and splits large suites across fleets of machines. As staff software engineer Gordon Chan puts it, “That’s a lot of data that we have to store and present back to customers in a UI and dashboard.”


This year, at ClickHouse meetups in [Wellington](https://clickhouse.com/videos/wellington-meetup-buildkite-clickhouse-test-analytics) and [Melbourne](https://clickhouse.com/videos/melbourne-meetup-buildkite-20sep25), Gordon told the story of how Test Engine went from a simple Rails app to a streaming architecture—and why the team ultimately reached for [ClickHouse Cloud](https://clickhouse.com/cloud) to power customer\-facing analytics.


## From Rails app to streaming overload [\#](/blog/buildkite-test-analytics#from-rails-app-to-streaming-overload)


Test Engine first launched with a traditional architecture using Ruby on Rails backed by Postgres. “It was great at the time, just to get started,” Gordon says. “But as more customers wanted to use the product, we realized the architecture couldn’t serve information at the speed and scale required by our customers. We needed to scale the platform.”


So in 2024, over six months, the team re\-architected ingestion, introducing Kafka to propagate test events and Flink to handful stateful processing and pre\-aggregations. Data flowed into multiple stores: Postgres for some aggregates, DynamoDB for fast key\-value lookups, and Iceberg tables in S3 queried via Athena (and later Trino) for flexible analysis. For a while, it looked like a success. “We unlocked the platform for large enterprise customers,” Gordon says. “They could onboard onto Test Engine, and everyone was happy.”


But as customers saw what was possible, they wanted more. “Our customers had a really strong demand to leverage the data in a way that’s intuitive to them,” Gordon says. They wanted to tag each test execution with arbitrary metadata—instance type, architecture, language version, cloud provider, feature flag—and then slice, dice, and group on the fly.


The existing tools weren’t built for that level of interactive, high\-cardinality analytics. Flink was great for “rule\-based actions” like detecting flaky tests, but “not very good for aggregations across lots of arbitrary user\-specified tags.” DynamoDB was “good for fast retrieval of individual records, but not really capable of doing real\-time analytics.” Iceberg plus Athena or Trino offered flexible querying, but it wasn’t nearly fast enough. And Kafka, Gordon says, was “never designed for the type of querying or aggregation we wanted to do.”


In short, Test Engine had the data, but not the interactive analytics experience customers were asking for. The team knew they needed a different kind of engine.


## Why ClickHouse Cloud was the perfect fit [\#](/blog/buildkite-test-analytics#why-clickhouse-cloud-was-the-perfect-fit)


By late 2024, Buildkite was on the hunt for a “magical database for tagging”—a system that could power real\-time analytics across billions of test executions without relying on heavy pre\-aggregations. While they evaluated several OLAP options, including Apache Druid and Pinot, it didn’t take long for ClickHouse to emerge as the best fit.


The first reason was obvious: “ClickHouse is blazingly fast,” Gordon says. Beyond that, they wanted something highly available, battle\-tested, and capable of scaling without too much maintenance. ClickHouse checked all those boxes. Gordon had watched talks by ClickHouse creator Alexey Milovidov and came away “really impressed” with his bottom\-up, hardware\-aware approach. That reinforced what he was hearing from “friends and other companies in the industry, who all had good things to say about ClickHouse.”


Another big draw was how easy it was to get started. It took minutes for the team to download the binary, run it locally, and push a sample of production data through. “It was really easy for us to test this locally and actually prove it was really fast, really quickly,” Gordon recalls. ClickHouse’s [SQL compatibility](https://clickhouse.com/docs/sql-reference) contributed to that developer\-friendliness. “It made it very familiar and easy for our engineers who are not data engineers to use it.”


ClickHouse’s new [JSON data type](https://clickhouse.com/docs/sql-reference/data-types/newjson) sealed the deal. Test Engine’s vision depended on arbitrary tags: customers should be able to attach whatever metadata they care about and query it efficiently. “The ability to just send metadata into this JSON data type and then have ClickHouse create individual columns for each key was amazing,” Gordon says.


After validating ClickHouse locally, the team spun up a self\-hosted instance in AWS and even built a ClickHouse\-backed prototype for AWS re:Invent. “Our customers were pretty excited, so we had to look at productionizing that solution,” Gordon says. That pushed them to think about how much operational overhead they wanted to take on. “We didn’t want to do a lot of database operations,” he explains. “We don’t want to worry about updates, patching, scaling. And so [ClickHouse Cloud](https://clickhouse.com/cloud) was a good solution.”


They connected with the ClickHouse team in December, and a month later, after getting the green light from legal, risk, and finance, they became a paying customer. From there, the team quickly moved from prototyping to rolling out their first ClickHouse\-powered features—marking the start of a transformation in how Test Engine handled analytics.


## Six months later: From pilot to production [\#](/blog/buildkite-test-analytics#six-months-later-from-pilot-to-production)


The first production use case was narrow but powerful: enable real\-time analytics over tagged test events without relying on pre\-computed reports. With ClickHouse Cloud, customers could do things like group P50 test durations by instance type, architecture, or cloud provider and identify patterns like “this newer VM family runs 25% faster for the same price.”


“We were amazed by the query performance,” Gordon says. “That success gave us confidence to shift more of our workloads to ClickHouse, to unlock more analytical capability for our customers, and to bring more consistency to our back end.”


By the time of [Gordon’s Melbourne talk in September 2025](https://clickhouse.com/videos/melbourne-meetup-buildkite-20sep25), ClickHouse had become the analytical backbone of Test Engine’s operation, replacing a patchwork of pre\-aggregations and storage systems with a single, real\-time analytics layer.


![Buildkite User Story Issue 1214.jpg](/uploads/Buildkite_User_Story_Issue_1214_a6c8e7b420.jpg)
Test results flow from customer CI/CD pipelines into ClickHouse Cloud for real\-time analytics.


In the current setup, customers send test results from their CI/CD pipelines, Kafka buffers and propagates those events, Flink handles stateful processing, and the majority of that data lands in ClickHouse Cloud. The Test Engine UI still runs inside Buildkite’s monolithic Ruby on Rails application backed by Postgres, but almost every analytical query now targets ClickHouse.


The numbers tell the story. When Gordon first spoke in February, Test Engine was ingesting around 3 billion test executions per month. Six months later, that had quadrupled to 12 billion, with sustained peaks above 25,000 events per second. “At the moment, we have about 70 billion records in ClickHouse, and that’s just since the beginning of this year,” he says, noting they haven’t even needed [TTL\-based pruning](https://clickhouse.com/docs/guides/developer/ttl) yet.


Importantly, ClickHouse handles both sides of the equation. On the write path, ingesting 25,000 events per second into Postgres was “just not possible really, unless you did a lot of tuning,” Gordon says. “With ClickHouse, it was pretty easy.”


On the read path, ClickHouse Cloud distributes queries across multiple nodes—“so things can scale when needed,” he says. “And if we find that customers want more complexity, we have more tools to optimize read performance—things like [choosing the correct primary key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key), using [materialized views](https://clickhouse.com/docs/materialized-views), using [skipping indexes](https://clickhouse.com/docs/optimize/skipping-indexes), stuff like that.”


## A healthier cost sheet and happier customers [\#](/blog/buildkite-test-analytics#a-healthier-cost-sheet-and-happier-customers)


For Buildkite, ClickHouse’s impact has been massive. As Gordon puts it, “Shifting workloads to ClickHouse Cloud has simplified our backend systems and reduced costs, unlocked more possibilities for analytics, and enabled the team to rapidly deliver new functionality.”


He shared screenshots from a team Slack channel called \#social\-salmon, where engineers celebrate GitHub pull requests with more red (deleted) lines than green. As workloads moved to ClickHouse, that channel lit up. “The code base is healthier for it,” Gordon says.


Previously, Flink jobs ran around the clock, pre\-aggregating metrics like daily test duration for every test in existence and syncing them into DynamoDB, Postgres, and Iceberg tables, with Kafka topics and ETL glue in between. “This was quite expensive, and it ran constantly, regardless of whether customers needed that data or not,” Gordon says.


Today, much of that machinery is gone. Test splitting data, flaky test analytics, build\-level insights, and general search and filtering now run as on\-demand queries against ClickHouse. “It was actually really satisfying to tear down the old implementation,” Gordon says. “We deleted a lot of code, dropped many Postgres tables, deleted a lot of Kafka topics, retired a lot of jobs, and managed to completely retire our usage of DynamoDB.”


![image2.png](/uploads/image2_917cd801ae.png)
Buildkite engineers celebrate code deletions as workloads shift to ClickHouse Cloud.


Financially, the impact has been just as huge. Over the same period that event volume quadrupled, Test Engine’s net infrastructure spend dropped by five figures per month. According to Gordon’s napkin math, for every dollar spent on ClickHouse, the team is saving eight dollars elsewhere—“a 1:8 ratio,” as he puts it. Most of that came from scaling down Flink workloads by more than 60%, retiring DynamoDB, and cutting Aurora Postgres capacity in half.


“Thanks to ClickHouse Cloud, we’re doing way more with less, and delivering greater tool capabilities to our customers than ever before,” Gordon says.


That last point about customers is what matters most. The teams who rely on Test Engine now get more speed, more flexibility, and far more control. “ClickHouse has enabled us to deliver on\-demand, real\-time analytics to our customers, who can now leverage data in ways that are intuitive to them, without having to rely on canned reports,” Gordon says. “It’s given them the freedom to slice and dice the data as needed.”


## Built for speed, designed with sympathy [\#](/blog/buildkite-test-analytics#built-for-speed-designed-with-sympathy)


Gordon closed his Melbourne talk with a quote from racing legend Jackie Stewart: “You don’t have to be an engineer to be a racing driver, but you do have to have mechanical sympathy.”


For Buildkite and the Test Engine team, ClickHouse rewards that kind of sympathy. It’s fast enough to keep up with world\-class engineering teams, flexible enough to express the questions they actually want to ask, and simple enough that a small product team can operate it without becoming full\-time database admins.


“Migrating to ClickHouse has simplified our tech stack, reduced costs, and unlocked way more capabilities and possibilities,” Gordon says. “Our customers are delighted with the new features we’ve delivered recently and the accelerated delivery speed of those features.”


At the end of the day, as Gordon puts it, “It’s all about helping teams build and deploy as fast as they can.”

### Looking to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-45-looking-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=45)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
