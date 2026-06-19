# IBM Instana’s solution for monitoring ClickHouse performance


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# IBM Instana’s solution for monitoring ClickHouse performance

![](/uploads/ibm_6177497242.svg)IBMJan 17, 2025 · 6 minutes readAs a real\-time observability platform, IBM Instana gives DevOps teams and engineers the tools they need to spot and fix issues in distributed systems before they affect users. At the heart of their platform is ClickHouse, which handles the massive job of storing and querying all the telemetry data that drives Instana’s monitoring capabilities.


But as foundational as ClickHouse is to Instana’s architecture, it posed a unique challenge: how do you monitor the performance of the very system that monitors everything else? And how do you pull that off without adding complexity or slowing anything down?


At a recent [ClickHouse meetup in Toronto](https://clickhouse.com/videos/monitoring-clickhouse-using-opentelemetry), Joshua Hildred, a software developer at Instana, shared how his team tackled this problem with a custom span exporter, a clever solution that has changed the way Instana monitors ClickHouse performance.


## Monitoring the system without overloading it [\#](/blog/ibm-instance-monitoring-clickhouse-performance#monitoring-the-system-without-overloading-it)


One of the keys to understanding system performance is tracing. Tracing captures the flow of requests through distributed systems, breaking them down into spans, or individual units of work that reveal where time and resources are spent. For Instana, whose success depends on providing high\-fidelity, one\-second observability, tracing ClickHouse operations means uncovering insights into performance bottlenecks and system behavior.


"ClickHouse is a fundamental part of our system, so our team really cares about monitoring it," explains Joshua. While processing requests from users was easily handled by ClickHouse, analyzing what happened inside the system presented a bigger challenge. The team needed to trace and monitor ClickHouse's performance in real\-time without disrupting its role as the foundation of Instana's observability platform.


Initially, they explored using ClickHouse's [materialized views](https://clickhouse.com/docs/en/materialized-view) to export telemetry spans. While effective in theory, this approach came with tradeoffs. For one, materialized views added unnecessary overhead that could affect ClickHouse's performance. More importantly, they were "invasive," posing risks for customer systems by introducing additional complexity. "We don't want to be putting unneeded things in customers' systems," Joshua says.


## A custom solution built for efficiency [\#](/blog/ibm-instance-monitoring-clickhouse-performance#a-custom-solution-built-for-efficiency)


Rather than relying on existing tools, Joshua and the Instana team decided to build a custom span exporter to deliver the rich performance insights they needed without burdening the systems it was designed to monitor.


[OpenTelemetry](https://clickhouse.com/docs/en/observability/integrating-opentelemetry), the emerging standard for collecting and transmitting telemetry data, provided the foundation. "ClickHouse supports OpenTelemetry, which is awesome for tracing performance," Joshua says. "It lets us dive into ClickHouse and not only capture flows through our distributed systems but also track how those calls are executed within ClickHouse, giving us clear visibility into what ClickHouse is doing."


As Joshua explains, the custom span exporter was designed with six main goals in mind:


1. **Ease of installation** \- The exporter needed to be simple to deploy, with a one\-liner installation that allowed teams to get up and running quickly.
2. **Automatic reconfiguration** \- It had to adapt to system changes on the fly, minimizing maintenance and staying reliable even in dynamic environments.
3. **Non\-invasiveness** \- To avoid disrupting customer systems or complicating ClickHouse's operations, the exporter had to have a minimal footprint.
4. **Preprocessing spans** \- By performing preprocessing tasks before data reaches the backend, the exporter could offload computational work and improve system efficiency.
5. **Easy configuration updates** \- The ability to seamlessly push updates would allow the exporter to evolve with Instana's needs.
6. **Support for metrics and profiling** \- Beyond tracing, the exporter was designed to capture metrics and profiling data, adding even more value for monitoring teams.


Ultimately, this design would allow Instana to monitor ClickHouse, minimize the impact on system performance, and address the needs of both their internal team and customers.


## From concept to reality [\#](/blog/ibm-instance-monitoring-clickhouse-performance#from-concept-to-reality)


With their goals laid out, the Instana team got to work integrating the custom span exporter into their architecture. One of the benefits of building in a mature ecosystem, Josh says, is the availability of existing tools like the Instana agent, a lightweight monitoring tool capable of automatic discovery. When deployed, the agent identified running ClickHouse instances, fetched the necessary sensors, and began collecting data, all without requiring manual setup.



> "We got all this for free, which was nice," Joshua says.


The exporter itself uses a [sliding window](https://clickhouse.com/docs/en/sql-reference/window-functions) approach to query ClickHouse's `opentelemetry_span` table at regular intervals. This method ensures that no data is missed while keeping the system efficient. Preprocessing tasks, like filtering and formatting spans, are handled before data reaches Instana's backend, reducing the computational load on downstream systems. Once processed, the spans are stitched together in the backend and visualized to give Instana actionable insights into ClickHouse's performance.


## A better system for everyone [\#](/blog/ibm-instance-monitoring-clickhouse-performance#a-better-system-for-everyone)


The addition of the custom span exporter has changed how Instana's teams monitor and optimize ClickHouse. Internal users can trace ClickHouse's performance with newfound clarity, identifying bottlenecks and improving query execution. For customers, better monitoring capabilities mean faster issue resolution and more reliable system performance.


But the benefits go beyond just troubleshooting. The integration has deepened Instana's understanding of how ClickHouse fits into broader distributed systems. By visualizing how ClickHouse interacts with other components, teams can fine\-tune the database while optimizing the entire platform to better serve internal and external stakeholders.


"The custom span exporter helps us make the whole system more reliable, bringing us one step closer to our mission of providing real\-time observability for everyone," Joshua says.


## Pushing the boundaries of observability [\#](/blog/ibm-instance-monitoring-clickhouse-performance#pushing-the-boundaries-of-observability)


Instana's clever solution to the question of monitoring ClickHouse shows how Joshua and the team turned a tricky challenge into an opportunity to innovate. By using ClickHouse's support for OpenTelemetry to build a custom span exporter, they came up with a solution that's simple, effective, and designed to meet their needs. Most importantly, they've improved their ability to deliver the high\-fidelity insights DevOps teams rely on every day.


The success of the custom span exporter speaks to what Instana is all about: giving teams the tools they need to act quickly and confidently. For Instana's engineers, it's made it easier to understand and optimize how ClickHouse fits into their architecture. For customers, it means faster fixes, better performance, and more trust in a world that runs on distributed systems.


To discover more ClickHouse benefits and see how it can transform your company's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
