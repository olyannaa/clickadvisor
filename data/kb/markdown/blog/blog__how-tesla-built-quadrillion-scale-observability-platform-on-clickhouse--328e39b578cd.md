# How Tesla built a quadrillion\-scale observability platform on ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Tesla built a quadrillion\-scale observability platform on ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 10, 2025 · 9 minutes readFew companies on Earth operate at the scale of Tesla. From massive Gigafactories to critical energy systems to a global network of connected vehicles, keeping that many moving parts in sync demands real\-time observability into what’s happening, everywhere.


“Tesla isn’t a small operation,” says Senior Staff Software Engineer Alon Tal. “We generate a massive amount of metrics, and we want to use that data for things like long\-term analysis, forecasting, and anomaly detection.”


![unnamed (1).jpg](/uploads/unnamed_1_25d5e12aef.jpg)
When it came time to build a new observability system, Alon and the team looked at the usual suspects. For many growing companies, this re\-evaluation is driven by the limitations of proprietary platforms, from [per\-seat pricing models to vendor lock\-in](https://clickhouse.com/resources/engineering/new-relic-alternatives/). This pivot point is a common architectural challenge, as a direct [comparison of top infrastructure monitoring tools](https://clickhouse.com/resources/engineering/top-infrastructure-monitoring-tools-comparison/) often overlooks the underlying data platform's ability to scale. But while [tools like Prometheus](https://clickhouse.com/engineering-resources/best-open-source-observability-solutions) were great in theory, they weren’t built for Tesla’s scale. “You can’t scale it horizontally, and there's a limit to how much you can scale it vertically,” he explains. “Also, as a single\-server system, it doesn’t meet our availability requirements. If it goes down, you lose your metrics. That’s completely unacceptable.”


They needed something faster, more durable, and more scalable. A system that could ingest tens of millions of rows per second, retain years of data, and stay responsive under heavy load. So they chose ClickHouse and used it to build Comet, a Tesla\-scale platform that delivers Prometheus\-like simplicity backed by ClickHouse\-grade performance and reliability.


This case study explores how Tesla built Comet, why they chose ClickHouse as its foundation, and how a quadrillion\-row load test proved the system could scale far beyond even Tesla's demanding requirements.



> Watch Alon’s talk at ClickHouse’s inaugural 2025 Open House user conference. [Watch the video.](https://clickhouse.com/videos/tesla)


## A slew of non\-negotiables [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#a-slew-of-non-negotiables)


From the outset, the team had a clear list of requirements. First and foremost, Alon says, “it had to scale.” For Tesla, that meant handling massive amounts of data in real time, with confidence that the new system could keep up as volume grew.


Availability was just as important. “At Tesla, losing metrics can have actual, real\-world, physical repercussions,” Alon says. With so much on the line, the system had to be bulletproof.


Retention was another priority. The team needed to look back across months and even years to spot patterns and predict issues. Durability was a given: once a metric is accepted, it has to persist, even through restarts. And speed was non\-negotiable. “Nobody likes a sluggish dashboard, especially when you're troubleshooting an outage,” Alon says.


Flexibility mattered, too. They wanted the freedom to ask complex questions, run custom analyses, and support a wide range of internal use cases. “We want to be able to ask interesting questions about our data and not be limited by a simplistic domain\-specific language.”


Finally, it all had to work with PromQL, Tesla’s query language of choice for metrics analysis. “This is the language our engineers know and prefer,” Alon says. They also had a huge library of existing dashboards and alerting rules. “Nobody wanted to reimplement all that.”


### Learn about ClickStack [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#test)

Explore the ClickHouse\-powered open\-source observability stack built for OpenTelemetry at scale.

[Learn more](https://clickhouse.com/use-cases/observability?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## The case for ClickHouse [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#the-case-for-clickhouse)


As they began their observability journey, there were a few obvious starting points. “When you think about PromQL, the mind immediately goes to Prometheus,” Alon says. It’s the reference system behind the language, widely adopted, and easy to use. But given Tesla’s scale and other requirements, it wasn’t a viable option. “So we set out to build our own,” he says.


The first and “most fundamental” decision was where to put the data. The team looked at several tools, but ClickHouse stood out for its performance and flexibility.



> “In our opinion, data in ClickHouse is better than data anywhere else,” Alon says. “No other system lets you slice and dice your data, ask interesting questions, and get answers in an acceptable amount of time.”
> 
> 
> This approach frames observability as a data analytics problem, which is the core principle detailed in our [playbook for building cost\-effective observability architectures](/resources/engineering/observability-cost-optimization-playbook).


“ClickHouse checks every box,” he adds. “We have availability, speed, durability. We have everything we could want.” It even offers unexpected advantages, like support for [executable user\-defined functions (UDFs)](https://clickhouse.com/docs/sql-reference/functions/udf). That turned out to be especially helpful because, as Alon puts it, “not everything is trivial to express in SQL. Having UDFs was an excellent escape hatch.”


In the end, the choice was obvious. ClickHouse gave Tesla the performance they needed at scale, and the confidence to build something that felt both powerful and familiar. “There’s nothing out there that competes with ClickHouse,” Alon says.


## Inside Comet’s architecture [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#inside-comets-architecture)


With ClickHouse as the foundation, Alon and the team turned to designing an architecture that could meet Tesla’s demands. The result was Comet, a purpose\-built metrics platform with two main pipelines: one for ingesting massive volumes of data, and one for translating and executing PromQL queries on the fly.


On the ingest side, OpenTelemetry collectors deployed across Tesla’s infrastructure send metrics to a Kafka\-compatible queue. From there, a set of custom ETL processes (built entirely in\-house) transforms the data from OTLP format into structured rows, batches them, and writes them into ClickHouse. The architecture is designed to scale out easily and keep performance steady, even as volumes spike. “It’s a very scalable pipeline,” Alon says.


![tesla2.png](/uploads/tesla2_05960a7b2d.png)
Comet’s ingest pipeline uses Kafka and OTLP to batch metrics into ClickHouse.


But the real magic happens in the transpiler. This is the engine that converts PromQL into ClickHouse SQL in real time. It’s what makes Comet so powerful. Tesla’s engineers didn’t have to learn a new query language; they can keep writing PromQL just like they always have, while taking full advantage of ClickHouse’s speed and flexibility.


![tesla3.png](/uploads/tesla3_645ba8ac56.png)
Comet translates PromQL to ClickHouse SQL and maintains compatibility with Grafana and alerting tools.


Once a query runs, Comet formats the results to be byte\-for\-byte identical to Prometheus’s API responses. That means dashboards, alerts, and all the tools Tesla already uses keep working without any rewrites or special connectors. “Nobody has any idea that this wasn’t just a standard Prometheus environment,” Alon says.


To keep things reliable, a dedicated test suite runs identical PromQL queries against both Prometheus and Comet, ensuring the results are an exact match. The alerting layer also supports the same rules and integrations Tesla was using before, with no rework needed.


## Proving the system at scale [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale)



> The final tally: over one quadrillion rows ingested—“with not a single hiccup, not a single issue. Memory was flat, CPU consumption was flat. It was just a thing of beauty to behold.”


Today, Comet is ingesting tens of millions of rows per second. “And the system isn’t yet at full load,” Alon says, noting that they’re still onboarding multiple internal teams.


When it comes to time series, Tesla operates at a scale few systems can handle. Each series represents a stream of related metric samples, and over time, Tesla has accumulated tens of billions of them. Since every series contains many individual data points, the total row count is exponentially higher. “That right there is already a problem for systems that compete with Comet,” Alon says. “They’re super\-sensitive to high\-cardinality time series.”


Comet currently stores tens of trillions of samples, and Alon says the team is “very confident it can scale much higher than this.” He’s not exaggerating. To prove it, they pushed ingestion to one billion rows per second and kept it running for 11 days straight. The final tally: over one quadrillion rows ingested—“with not a single hiccup, not a single issue. Memory was flat, CPU consumption was flat. It was just a thing of beauty to behold.”



> Discover how ClickHouse powers observability at massive scale with [ClickStack.](https://clickhouse.com/use-cases/observability)


![tesla4.jpg](/uploads/tesla4_9b16a90718.jpg)
A count query shows Comet surpassing one quadrillion rows ingested with “not a single hiccup.”


## What’s next for Tesla and ClickHouse [\#](/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#whats-next-for-tesla-and-clickhouse)


With Comet running smoothly at scale, Tesla is already branching out into new use cases, like distributed tracing. Using the same transpiler\-based approach, they’ve added support for TraceQL, letting engineers query trace data just as easily as metrics.


The team is also exploring the idea of open\-sourcing Comet. “If we’re able to do that, everyone could take it for a test drive,” Alon says.


Comet is a great example of the innovation happening at Tesla every day. Built on ClickHouse, delivered through PromQL, and designed to provide real\-time insights across everything from massive factories to millions of connected vehicles, it gives engineers what they need to manage observability at Tesla scale.


“I want to thank everyone working on ClickHouse,” Alon said at Open House. “You’re building a fantastic product, and it makes my project possible.”



  

To learn more about ClickHouse and see how it can transform your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
