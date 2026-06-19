# How DoControl delivers real\-time, AI\-driven SaaS security insights with ClickHouse Cloud and MCP


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How DoControl delivers real\-time, AI\-driven SaaS security insights with ClickHouse Cloud and MCP

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 30, 2026 · 8 minutes read## Summary

DoControl uses ClickHouse Cloud to power real\-time analytics for SaaS security, governing file access, permissions, and third\-party apps. After hitting the limits of Postgres, they migrated to ClickHouse Cloud for faster ingestion, complex filtering, and real\-time queries at enterprise scale. They recently launched Dot, an AI\-powered security assistant, using ClickHouse MCP to translate natural\-language queries into real\-time analytics workflows.

The rise of SaaS tools has made it easier than ever for teams to collaborate, but it’s also created a new kind of security challenge. Sensitive files can be shared with a click. Third\-party apps proliferate without oversight. And while workplace productivity might boom as a result, organizations often have no idea how much risk they’ve inherited.


[DoControl](https://www.docontrol.io/) is all about identifying and addressing those blind spots. Founded in 2020 to bring control back to modern SaaS environments, the platform helps organizations govern access, detect misconfigurations, manage third\-party integrations, and automate remediation across tools like Google Workspace, Microsoft 365, Slack, and more.


For many customers, the impact is immediate. “There’s a ‘wow moment’ when they’re finally able to get accurate visibility into their exposure,” says Amit Fidler, Director of Engineering. “They’re in shock when they see both the scale and risk of the exposure across millions of assets and applications—board materials, compensation data, competitive intelligence, former employee access, and more.”


DoControl empowers organizations to uncover, pinpoint, and remediate these risks within seconds, without compromising business productivity. But as adoption grew and the company started onboarding Fortune 500 customers with billions of assets, they ran into a new challenge: scale.


We caught up with Amit and the DoControl team to talk about outgrowing Postgres, migrating to [ClickHouse Cloud](https://clickhouse.com/cloud), and using [ClickHouse MCP](https://clickhouse.com/blog/integrating-clickhouse-mcp) to deliver AI\-powered insights at scale.


## Growing pains with Postgres [\#](/blog/do-control#growing-pains-with-postgres)


Originally, DoControl’s analytics engine ran entirely on Postgres. It worked fine for most use cases, but as the company scaled and began ingesting tens of millions of assets from Google Drive and other SaaS platforms, the limitations quickly became apparent.


“Postgres is a pretty good database,” says Bar Ifrah, Technical Lead. “But the problem is, when you’re trying to build tens of indexes or run aggregations, it just can't do it.”


Even with the indexes they built, the transactional database struggled to keep up with the volume of events and the complexity of the queries. “It’s not just about aggregation,” Bar adds. “Once we started onboarding enterprise\-level customers, we couldn’t ingest all their data at the scale and pace we needed. We just didn’t have a good analytics system.”


Postgres remained the system of record for identity and filtering by ID, but it was no longer viable as the foundation for real\-time analytics. The team began exploring alternatives, and eventually found their answer in [ClickHouse Cloud](https://clickhouse.com/cloud).


“We were super excited to start working with ClickHouse,” Amit says. “It has been a game\-changer in how we serve the world’s largest companies, in a way that no competitive solution can match.”


## A new analytics engine with ClickHouse [\#](/blog/do-control#a-new-analytics-engine-with-clickhouse)


For DoControl, the benefits of ClickHouse Cloud were clear right away.


“It’s much faster than Postgres,” Bar says. “When we added ClickHouse to the architecture, we could remove all the indexes, and ingestion worked much faster than before.”


“Now, we’re able to ingest tens of millions of files quickly and perform complex analytics in real time,” Amit adds. “Even querying a single asset across tens of millions of files and billions of permissions happens in real time, which is fantastic.”


Today, ClickHouse powers every analytics workflow in the product. From customer\-facing dashboards to internal investigations, queries that once pushed Postgres to its limits now run smoothly. Whether it’s application data, audit logs, or sharing events, the team can query it live and surface insights instantly in the product UI.


“This is something we couldn’t do with our previous database,” Amit says.


“The filters we’re allowing customers to run are very complex,” Bar adds. “ClickHouse’s ability to process a lot of data in a short period of time is a game\-changer.”


DoControl currently operates ClickHouse instances across both AWS and GCP, an architecture that supports internal requirements and customer needs. ClickHouse Cloud’s multi\-cloud support gives the team flexibility to run workloads where it makes the most sense.


With instances ranging from 100 GB to several terabytes across both clouds, DoControl has built a real\-time analytics layer that’s sturdy and flexible enough to support its growing user base, while laying the foundation for what comes next.


## Agents, AI, and ClickHouse MCP [\#](/blog/do-control#agents-ai-and-clickhouse-mcp)


As the company looked to the future, the team felt convinced of one thing: the next wave of user interaction wouldn’t happen in a traditional UI. It would happen through conversation, with AI agents acting as the new front end.


So they built [Dot](https://www.docontrol.io/lp/dot), an AI\-powered security assistant that helps users investigate events and answer questions about their environment. Dot uses [ClickHouse MCP](https://clickhouse.com/blog/integrating-clickhouse-mcp) (Model Context Protocol) to interact directly with ClickHouse, translating natural\-language queries into SQL, performing “very interesting and complex aggregations,” and returning results in real time.


“It really opened a whole wide area of use cases and changed how we think about data,” Amit says. “Because once you take all the ClickHouse knowledge in the world, which we get from working with AI, and combine it with our data, you can achieve marvelous things.”


In one example, the team wanted to detect “impossible travel” events—logins from two distant locations within a short window. Rather than build custom logic, they let Dot try to solve the problem on its own. The agent discovered ClickHouse’s built\-in [greatCircleDistance function](https://clickhouse.com/docs/sql-reference/functions/geo/coordinates), which calculates the distance between coordinates. It’s a perfect example of how ClickHouse MCP can open the door to powerful new workflows.


The architecture behind Dot is lightweight and scalable. A supervisor agent interfaces with the UI and routes queries to specialized sub\-agents—one for events, one for identities. Each agent uses ClickHouse MCP to issue queries and return results.


“Working with a lot of indexes, like in Postgres, isn’t feasible for AI, since you don’t really know what filter or aggregation the user wants to run, and just guessing isn’t enough,” Bar explains. “You need a real\-time analytics engine like ClickHouse with very fast filtering capabilities, because the user isn’t going to stay and watch the chat for 10 minutes.”


The team is now experimenting with multi\-agent orchestration, cross\-database querying, and even exposing the system through chat apps. As Amit says, “We believe that in the future, most user interactions will not be in the application itself, but within those chat applications.”


## What’s next for DoControl and ClickHouse [\#](/blog/do-control#whats-next-for-docontrol-and-clickhouse)


With AI use cases expanding and customer demand continuing to grow, the DoControl team is hard at work pushing their infrastructure forward. That includes rolling out [compute\-storage separation](https://clickhouse.com/docs/guides/separation-storage-compute) in ClickHouse Cloud, giving them more flexibility to isolate workloads and support high\-scale ingestion and querying. “It’s one of the best steps we’ve taken,” Amit says.


Looking ahead, they’re focused on enabling new interfaces, scaling to support more enterprise data, and deepening their AI capabilities. As an engineering\-led culture, they’re proud to be early adopters of technologies like the [ClickHouse MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp).


“We’re always looking for ways to use the most advanced technology to achieve our business needs,” says Itai Birenshtok, DoControl’s VP of Research and Development. “That includes being one of the first companies to use ClickHouse MCP in production.”


The team is always exploring what’s next, always finding ways to combine cutting\-edge infrastructure with business value. Whether it’s reducing security risk for customers, ingesting billions of events, or building the next generation of AI\-powered assistants, DoControl is all\-in on modern, real\-time analytics. And ClickHouse is at the heart of it.

### Want to see ClickHouse MCP in action?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-50-want-to-see-clickhouse-mcp-in-action-sign-up&utm_blogctaid=50)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
