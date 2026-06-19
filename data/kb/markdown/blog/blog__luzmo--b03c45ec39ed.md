# How Luzmo uses ClickHouse Cloud to power fast end\-user analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Luzmo uses ClickHouse Cloud to power fast end\-user analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 22, 2026 · 6 minutes read## Summary

Luzmo uses ClickHouse Cloud to power fast, embedded analytics for data\-driven companies with highly variable, customer\-defined data. After years on open\-source ClickHouse, Luzmo moved to ClickHouse Cloud to offload infrastructure management and focus on building analytics, not running clusters. ClickHouse now supports embedded analytics, query and plugin log analysis, and vector search, delivering high performance, flexibility, and cost\-efficiency.

[Luzmo](https://www.luzmo.com/) empowers data\-heavy applications to deliver lightning\-fast, accessible analytics to their users. By integrating powerful visualizations and AI\-driven exploration directly into the application, Luzmo helps teams building data\-centric software turn high\-volume information into intuitive, actionable insights for their customers.


Some companies use Luzmo to surface familiar SaaS metrics (e.g. campaign performance, ROI, usage trends) inside marketing or sales platforms. Others, like Belgium's largest telecom provider, Proximus, operate in very different domains, where location intelligence and large\-scale operational data need to be visualized, explored, and monetized. In every case, analytics need to feel instant, even when the underlying data is complex.


From the beginning, delivering that kind of experience meant choosing infrastructure that could keep up. We caught up with Luzmo's co\-founder and CTO, Haroen Vermylen, to chat about why the team originally adopted ClickHouse, what prompted their move from open source to [ClickHouse Cloud](https://clickhouse.com/cloud), and how ClickHouse has since spread across the company, powering everything from end\-user analytics to observability\-related workloads and vector search.



## Why Luzmo originally chose ClickHouse [\#](/blog/luzmo#why-luzmo-originally-chose-clickhouse)


Luzmo was founded (as Cumul.io) in Leuven, Belgium, in 2015\. Two years later, the team discovered ClickHouse. "It's been quite a ride," Haroen says with a smile.


At the time, Luzmo needed a fast internal warehouse to store and analyze data for customers who preferred the platform to host it on their behalf. While Luzmo is federated (many customers keep their data in their own systems), others rely on it to store and query that data efficiently.


Back then, much of the analytics world still equated serious performance with sprawling distributed systems and large clusters. Scaling typically meant spending heavily on infrastructure and taking on significant operational complexity.


ClickHouse, open\-sourced just a year earlier, offered a different set of tradeoffs. Rather than requiring massive infrastructure to unlock speed, it delivered major performance gains even at small scale, while still offering a clear path to grow as needed. "ClickHouse came out, and it worked on my laptop," Haroen recalls. "That was pretty amazing."


The team evaluated a number of alternatives, but none offered ClickHouse's combination of performance, flexibility, and scalability. "We want to make things fast for our customers," Haroen says. "That's why we settled on ClickHouse."


## From open\-source to ClickHouse Cloud [\#](/blog/luzmo#from-open-source-to-clickhouse-cloud)


In late 2022, ClickHouse released [ClickHouse Cloud](https://clickhouse.com/cloud), giving teams a way to run ClickHouse without having to manage clusters themselves. Luzmo was one of the first customers to sign up.


For Haroen and the team, the motivation was simple enough: they never set out to manage infrastructure. "We're in the business of building analytics," he says. "Running clusters isn't really our core business, so that was a task that we wanted to get rid of."


Moving to a managed service allowed the team to offload day\-to\-day operational work and stay focused on building analytics and reporting for customers. It was a "best of both worlds" situation, with ClickHouse Cloud handling provisioning, upgrades, and ongoing maintenance, while still preserving the performance benefits and scalability that attracted Haroen and the team to ClickHouse in the first place.


## One platform, many use cases [\#](/blog/luzmo#one-platform-many-use-cases)


Over the years, Luzmo's use of ClickHouse has evolved well beyond customer\-facing analytics. As Haroen jokes, "ClickHouse has been quite infectious inside our company."


For example, Luzmo now uses ClickHouse for observability\-related workloads, storing query logs and plugin logs so both the team and its customers can understand how queries behave in production. That visibility helps customers identify slow queries, trace issues back to specific data sources, and make informed decisions about how their analytics are powered.


More recently, ClickHouse has become part of Luzmo's work with [vector search](https://clickhouse.com/docs/knowledgebase/vector-search). Rather than introducing a separate system, the team uses ClickHouse to store embeddings, metadata, and related data, extending the platform into what Haroen describes as "non\-obvious use cases."


In practice, ClickHouse has become a kind of default. Once in place, it's often the simplest and most effective choice for the next problem, without adding unnecessary architectural sprawl.


## Engineering for the unknown [\#](/blog/luzmo#engineering-for-the-unknown)


Luzmo's architecture comes with a few unique challenges. As a multi\-tenant platform, the team often doesn't know what data it will receive until it arrives. That leads to tens of thousands of tables, highly variable schemas, and workloads that don't fit neatly into predefined models.


On top of that, many customer queries span multiple systems. To manage that complexity, Luzmo has built its own query engine to optimize and coordinate those requests, ordering and grouping them to reduce load and improve efficiency. In some cases, large volumes of incoming queries can be consolidated into a single, more efficient operation, reducing pressure on ClickHouse while still delivering fast results.


Some of these challenges have required custom engineering. But over time, Haroen says, improvements in ClickHouse itself have smoothed many of the rough edges. New features and data types continue to expand what's possible, even in environments where the data is unpredictable by nature.


## "Fast, versatile, cost\-efficient" [\#](/blog/luzmo#fast-versatile-cost-efficient)


Luzmo bills itself as "the fastest way to embed analytics in your product." For Haroen, that promise goes hand in hand with the role ClickHouse plays under the hood.


Today, ClickHouse Cloud supports everything from end\-user analytics to observability and emerging workloads like vector search. It gives Luzmo the performance it needs, the flexibility to take on new use cases, and the cost profile to scale without friction. And it does all of that while keeping analytics fast and effortless for end users.


Asked to sum up Luzmo's ClickHouse experience in a few words, Haroen thinks for a moment before responding: "extremely fast, extremely versatile, extremely cost\-efficient."

### Need speed and scalability from your database?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-75-need-speed-and-scalability-from-your-database-sign-up&utm_blogctaid=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
