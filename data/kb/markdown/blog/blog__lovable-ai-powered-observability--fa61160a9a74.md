# Lovable \<3 ClickHouse: AI\-powered observability and analytics at the world’s fastest\-growing software company


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Lovable \<3 ClickHouse: AI\-powered observability and analytics at the world’s fastest\-growing software company

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 29, 2026 · 8 minutes read## Summary

Lovable uses ClickHouse Cloud for observability and AI\-powered debugging across millions of AI\-generated apps and highly dynamic LLM workflows. ClickHouse MCP lets engineers investigate billions of logs with natural\-language prompts, reducing debugging time and keeping development velocity high. ClickHouse also powers real\-time analytics for millions of deployed apps, delivering sub\-50ms queries with a simple pipeline built by one engineer in a week.

As growth stories go, it’s literally impossible to find one more impressive than [Lovable](https://lovable.dev/)’s. In just eight months after launching, the Swedish startup surpassed $100 million in subscription revenue, making it the [fastest\-growing software company in history](https://www.forbes.com/sites/iainmartin/2025/07/23/vibe-coding-turned-this-swedish-ai-unicorn-into-the-fastest-growing-software-startup-ever/).


Their mission is simple but profound: to unlock human creativity by enabling anyone to create software. They do that with an AI\-powered platform that lets users build full\-stack apps from scratch using nothing more than natural\-language prompts.


Today, more than 8 million people use the platform. Together they create over 100,000 projects and ship around 25,000 apps into production every day. The company recently crossed 3 million deployed apps, and that number is climbing fast. As technical staff member Tomas Nordström puts it, “This means we definitely need better observability.”


At our [Open House Roadshow in Amsterdam](https://clickhouse.com/openhouse/amsterdam), Tomas shared how Lovable uses [ClickHouse Cloud](https://clickhouse.com/cloud) to keep up with a system that evolves by the minute, including how engineers debug unpredictable AI behavior with [ClickHouse MCP](https://clickhouse.com/blog/integrating-clickhouse-mcp). He also walked through how Lovable powers web analytics for all of its deployed apps, and where the team is expanding next.


## Use case \#1: Observability at scale [\#](/blog/lovable-ai-powered-observability#use-case-1-observability-at-scale)


Lovable runs a deeply distributed, AI\-powered system built from multiple distributed services that power millions of published apps. Every new project triggers a chain of internal API calls, external integrations, and LLM\-driven actions. The result is a “very non\-deterministic system,” Tomas says, in which understanding system behavior is uniquely challenging.


“We have a lot of APIs that we’re exposing internally, and then we’re also communicating with a lot of APIs externally as well,” he adds. “It’s quite a stochastic system.”


To make sense of all that activity, the team built a full OpenTelemetry pipeline that streams directly into ClickHouse. Logs and traces from the Go API backend, Cloudflare Workers, their sandbox environment, Temporal workflows, and Kubernetes clusters all land in one unified ClickHouse schema. From there, the team visualizes everything in Grafana, creating a real\-time view of how traffic moves across every endpoint—“both the ones we’re exposing,” Tomas says, “and also all of the endpoints we’re communicating with externally.”


ClickHouse gives them the high\-volume write throughput they need, plus fast queries across billions of events. And because ClickHouse’s schema model is flexible, the team can evolve their observability pipelines as new services, new models, and new workflows come online, without slowing down development.


## Use case \#2: AI\-powered debugging [\#](/blog/lovable-ai-powered-observability#use-case-2-ai-powered-debugging)


But even with full visibility into their microservices, Lovable still needed a way to understand what happens *between* those services—inside the LLM\-driven logic that can change from one request to the next. When an outgoing request fails or behaves strangely, the root cause often lives in a chain of model\-driven tool calls that didn’t exist a few minutes earlier. As Tomas puts it, “People are using Lovable in very weird ways that we weren’t expecting.” Those edge cases can be incredibly difficult to trace through billions of log entries.


This is where the [ClickHouse MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp) has been a “game\-changer,” Tomas says. With 20\-25 engineers supporting more than 8 million users, Lovable can’t rely on everyone being a SQL expert capable of querying hundreds of billions of log rows during an incident. MCP removes that barrier. Engineers simply describe the issue, and MCP fetches the right traces, recent Git commits, and the current log schema, with no SQL required.


“MCP has really been the best help we could ask for,” Tomas says. “It’s one of the main use cases where we’ve been sticking to ClickHouse and started falling in love with it.”


## Use case \#3: Analytics for 3 million apps [\#](/blog/lovable-ai-powered-observability#use-case-3-analytics-for-3-million-apps)


As more people began deploying apps with Lovable, another need emerged: giving users visibility into how their apps were performing in the real world. With millions of deployed apps and usage patterns ranging “from one visit to several million visits per day,” the team needed an analytics layer that could handle extreme multi\-tenancy at scale.


After a quick conversation with the ClickHouse team, the solution was clear. “We understood, this is actually a great use case for just building this with ClickHouse,” Tomas says.


Today, every time an app renders an HTML page, a lightweight event is sent via Cloudflare Workers straight into ClickHouse. A small service built around four tables and four [materialized views](https://clickhouse.com/docs/materialized-views) handles the rest, powering real\-time dashboards that track visitors, page views, sessions, bounce rates, referrers, devices, and more.


Despite the diversity in traffic, the system is fast and effortless to operate, with queries returning in 50 or so milliseconds. Just as impressive, the pipeline was “created by one engineer in one week,” Tomas says. “It was so easy and really a no\-brainer to set up.”


## Use case \#4: More ClickHouse applications [\#](/blog/lovable-ai-powered-observability#use-case-4-more-clickhouse-applications)


Lovable has continued to expand its ClickHouse usage with new features that benefit from its speed, reliability, and low operational overhead. “There’s a lot of use cases where we can continue using ClickHouse,” Tomas says.


A recent example is [Lovable Cloud](https://lovable.dev/cloud), the company’s native backend hosting environment. It came with a new AI gateway that tracks every LLM call—models, tokens, latency, cost—to support usage\-based billing. Since the team already knew how to structure, materialize, and aggregate data efficiently in ClickHouse, Tomas says integrating it with the gateway was a natural fit.


Security scanning is another new application, driven by the rise of “vibe coding” and security concerns around the apps it produces. “We’ve taken a responsibility to make sure we try our absolute best to make these apps as secure as possible,” he says. Lovable now scans all deployed apps daily for leaked secrets, permission issues, and other vulnerabilities. Any findings are logged into ClickHouse, materialized, and re\-checked every hour via [refreshable materialized views](https://clickhouse.com/docs/materialized-view/refreshable-materialized-view) to determine whether users should be alerted.


## Why ClickHouse matters for Lovable [\#](/blog/lovable-ai-powered-observability#why-clickhouse-matters-for-lovable)


Lovable’s vision of democratizing software comes with a second goal: democratizing the infrastructure behind it. As Tomas puts it, “We want to be able to move really, really fast—and we want to allow our users to move really, really fast as well.”


Part of that, he says, is exposing ClickHouse more and more to Lovable’s users. “You have a lot of options when using ClickHouse, but you can also take, in a sense, a lot of shortcuts as well. You don’t have to be a database expert.” With the right abstractions, both humans and AI can explore data, ask questions, and understand what’s happening without needing to understand every detail of the underlying schema.


That flexibility matters inside the company, too. With more than 200 commits landing in production each day, engineers need quick answers when something looks off. ClickHouse gives them that speed. Instead of digging through opaque logging pipelines, anyone on the team can jump into ClickHouse and instantly see how a change is behaving in the wild, without having to be a SQL expert. It shortens feedback loops, reduces operational drag, and keeps development velocity high.


Tomas closed his talk with a few words from Lovable itself: “At Lovable, we're making it possible for anyone to build software. ClickHouse makes it possible for anyone—human or AI—to understand and analyze that software at scale.”

### Ready to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-591-ready-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=591)**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
