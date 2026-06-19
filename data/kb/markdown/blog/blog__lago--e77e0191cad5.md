# A million events per second: How Lago scales usage\-based billing with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# A million events per second: How Lago scales usage\-based billing with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 5, 2026 · 9 minutes read## Summary

- Lago uses ClickHouse Cloud to ingest, store, and query massive volumes of usage events for real\-time, usage\-based billing and complex monetization for large enterprises
- By moving to ClickHouse Cloud and using ClickPipes, Lago scaled from 10K events per second to enterprise workloads of 1M events per second.
- ClickHouse enables Lago to serve larger, more complex customers with accurate, low\-latency billing, without building or operating its own data infrastructure.
## Building the billing backbone [\#](/blog/lago#building-the-billing-backbone)


The team at [Lago](http://www.getlago.com) has a saying: "friends don't let friends build billing systems."


In the late 2010s, the French startup's founders were working at Qonto, one of Europe's fastest\-growing fintechs. Like many product teams, they assumed billing would be a side project—something they could knock out quickly and move on from. Instead, complexity piled up fast, with new pricing models, new customer requirements, and new edge cases to figure out. What started as a handful of scripts turned into a sprawling internal platform supported by a team of 10 to 15 full\-time engineers. They learned that billing is critical infrastructure, and it gets harder the more products, geographies and customers you add to your business.


When they founded Lago in 2021, the goal wasn't just to build another billing tool. It was to change how billing is built: It should neither be a black box nor a homegrown tangle of microservices. Open source was central to that vision, for practical reasons as much as philosophical ones. If billing is the backbone of a company's revenue, it needs to be transparent, extensible, and enable maximum privacy, compliance, and security. Lago was designed so developers could inspect the code, adapt it to their own systems, and avoid being trapped in rigid, black\-box workflows.


It was also a reaction to what they saw in the market. In their words: "Many other billing vendors lock their customers in or offer limited flexibility, leading to the customer having to internally build much of the billing logic." At scale, that model starts to crack. As Lago's Head of Growth, Lisa Bardet, puts it, "Companies have to build a lot of workarounds when they reach a certain size and complexity. That's typically when they come knocking at our door."


Lago was built for complex billing from day one. This means it supports usage\-based pricing, subscriptions, credits, and almost any other pricing model (or hybrids of them). That decision has only become more relevant as AI\-driven products and API\-first businesses reshape how software is sold. Every request, every token, every feature used becomes a billable event. As Lisa says, "That's why it's so important to be able to scale the number of events we ingest, so we can provide the most accurate picture of our customers' margins at any point in time."


## What led Lago to ClickHouse Cloud [\#](/blog/lago#what-led-lago-to-clickhouse-cloud)


As Lago's platform has matured, so has the profile of the companies it serves. What started as a solution for fast\-growing startups is increasingly being adopted by larger, more complex enterprises (like PayPal, CoreWeave, and Mistral, among others) with demanding requirements. With that shift upmarket comes an explosion in data volume. At a certain point, billing stops being an application problem and starts becoming a data problem.


Supporting that new reality meant rethinking Lago's infrastructure from the ground up. The team needed a system that could ingest massive streams of usage events in real time, query them efficiently, and evolve as their customers' needs changed, without forcing Lago into rigid or proprietary constraints. "As an open\-source company, we don't want to be locked in with a solution," says Engineering Lead Jérémy Denquin.


The team evaluated many of the usual candidates: Redshift, Timescale, DuckDB, as well as Postgres\-based approaches. They tested, benchmarked, and pushed each system under real workloads. Some struggled with ingestion. Others required heavy configuration or were too operationally complex to scale. "We tried so many databases," Jérémy says. "The only one that worked really well and that was really easy to understand was ClickHouse."


At the time, million\-event\-per\-second workloads were still a ways off. Lago's initial target was closer to 10,000 to 20,000 events per second—already well beyond what their existing systems could comfortably handle. Even at that level, ClickHouse stood out. It was fast out of the box. It handled high write volumes without drama. And it didn't require weeks of tuning just to get something working. The documentation was clear, the ecosystem was active, and it fit the team's open\-source philosophy, preserving flexibility and control.


If choosing ClickHouse was one decision, choosing how to run it was another. Jérémy was effectively operating solo on the infrastructure side, and the team had no interest in becoming database operators. "I didn't have time," he says. "For me, it was way easier to use ClickHouse Cloud." The managed service offloaded the burden of scaling, upgrades, and maintenance, allowing the team to focus on billing solutions instead of infrastructure.


[ClickHouse Cloud](https://clickhouse.com/cloud) also fit naturally into Lago's existing pipeline. The team relies heavily on Kafka and Redpanda to stream usage events. [ClickPipes](https://clickhouse.com/clickpipes), ClickHouse Cloud's native ingestion service, made it straightforward to move that data into ClickHouse without building and maintaining custom connectors. With private networking, native integrations, and a clear operational model, ClickHouse Cloud gave Jérémy and the team the performance and reliability they needed, without turning infrastructure into a second job.


## Lago's ClickHouse\-based billing engine [\#](/blog/lago#lagos-clickhouse-based-billing-engine)


Today, ClickHouse is at the center of Lago's billing infrastructure. The platform relies on it for three core workloads: high\-volume billing event ingestion, fast [analytical queries](https://clickhouse.com/resources/engineering/oltp-vs-olap) over usage data, and activity and audit logs across the product.


The largest of those is the billing event pipeline. Every time a Lago customer's application generates a billable action—an API call, a feature being used, a unit of compute consumed—that event is streamed through Kafka or Redpanda and ingested into ClickHouse via ClickPipes. For many customers, that means tens of thousands of events per second flowing continuously through the system. And for some, it's far more than that.


A large customer for example, required Lago to support ingestion rates approaching one million events per second. "We did it, and it was a success," Jérémy says. The scale of that workload points to where usage\-based billing is heading as larger enterprises adopt consumption\-driven models. "We're the only one in the market that can provide a million events per second ingestion on the billing side," he adds. "Without ClickHouse, this wouldn't be possible."


Lago also relies on ClickHouse for querying that usage in real time. The platform needs to compute consumption, apply pricing logic, and expose accurate usage data to customers with minimal latency. ClickHouse's [columnar storage](https://clickhouse.com/resources/engineering/what-is-columnar-database) and query performance make it possible to run those analytical workloads directly on raw event data, without pre\-aggregation or complex pipelines, even as data volumes continue to grow.


The most recent addition is activity and audit logging. Every API call to Lago is recorded in ClickHouse, giving the team a complete, queryable history of what's happening across the platform. That data is used internally for debugging and observability, and externally to give customers visibility into their own activity. It's another example of a workload that starts small but scales quickly, and another place where performance and reliability matter.


## What's next for Lago and ClickHouse [\#](/blog/lago#whats-next-for-lago-and-clickhouse)


As Lago continues its move upmarket, ClickHouse's role is only growing. The team is already expanding its use beyond core billing events and logs, pushing deeper into real\-time usage tracking, aggregation, and analytics. The goal is to give customers an even clearer, more immediate view of how their products are being used and how that usage translates into revenue. "I expect we'll use it more and more," Jérémy says of ClickHouse.


That expansion is tightly coupled to the types of customers Lago is serving, who demand the highest billing accuracy, performance, and reliability. "We're moving toward serving larger and larger organizations," Lisa says. "ClickHouse plays a big role in helping us scale and maintain performance at that level. It's a core component of our infrastructure."


Over time, the team expects ClickHouse to take on an even larger share of Lago's data workload. While some analytics and event storage still run on Postgres today, the long\-term direction is clear. "One day in production, we will remove Postgres as an event store," Jérémy says. The goal is to consolidate around a single, high\-performance foundation that can handle everything from raw ingestion to real\-time analytics, while keeping operations simple.


As Lago grows and onboards larger, more complex organizations, that foundation matters more than ever. For a company that started with a vision of making complex billing feel simple, ClickHouse is helping ensure that the hardest parts stay under the hood.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-90-get-started-today-sign-up&utm_blogctaid=90)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
