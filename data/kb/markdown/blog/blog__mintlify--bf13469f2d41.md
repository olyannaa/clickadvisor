# Mintlify boosts NPS 30% and saves 60% with real\-time analytics on ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Mintlify boosts NPS 30% and saves 60% with real\-time analytics on ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 14, 2026 · 10 minutes read## Summary

Mintlify uses ClickHouse Cloud to give tens of thousands of companies real\-time visibility into how tens of millions of developers engage with their content. After replacing PostHog with ClickHouse, dashboard load times dropped from tens of seconds to sub\-one\-second, driving an estimated 30% NPS improvement. ClickHouse Cloud requires zero ongoing maintenance and runs at 60% lower cost than PostHog, with an architecture built to scale well beyond Mintlify's current size.

[Mintlify](https://www.mintlify.com/) is the intelligent knowledge platform powering help centers, support centers, and developer documentation sites for companies like Anthropic, Microsoft, Coinbase, and Perplexity, serving tens of millions of developers each month.


Over the past year, the company has seen a major shift in who—or what—is reading those docs. Traffic that was once 90% human and 10% AI crawlers is now split evenly, and Mintlify expects AI agents to account for 90% of all traffic by the end of 2026\.


As tools like ChatGPT, Claude, and Cursor increasingly rely on documentation, Mintlify's customers need fast, reliable insight into how both humans and agents are engaging with their content, so they can make informed decisions about what to improve. But as usage grew, serving that data quickly and reliably turned out to be harder than expected.


"Prior to using ClickHouse, opening the analytics page in the Mintlify dashboard could take tens of seconds to load," says engineering manager Nicholas Khami. "After using ClickHouse, we've gotten that latency down to sub\-one\-second—it's almost instant."


We caught up with Nick to learn why Mintlify migrated from PostHog, what made them choose [ClickHouse Cloud](https://clickhouse.com/cloud), and how it's helping them scale to meet a future dominated by AI agents.


## Outgrowing PostHog [\#](/blog/mintlify#outgrowing-posthog)


Before migrating to ClickHouse, Mintlify initially used PostHog for product analytics, and it was a relatively easy lift to embed it into their dashboard for customer use. The setup worked well at first, but as their customer base grew, it began to show its limits.


The core issue was architectural. "PostHog is a great product," Nick says, "but it just doesn't support [incremental materialized views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view), which was causing really high latency." For a multi\-tenant SaaS platform like Mintlify, where tens of thousands of companies are each querying analytics on their own traffic, that caused serious problems.


Without incremental materialized views, every dashboard triggered raw queries against the full dataset, resulting in sluggish load times and rate limit errors that caused dashboards to fail entirely. "It was very slow and would error out due to those rate limits," Nick says.


At the height of the problem, the limitations of the existing analytics setup became increasingly clear. Dashboard performance and reliability issues began to significantly impact the customer experience and required ongoing attention from the engineering team. The team knew it was time for a more scalable solution.


## Choosing ClickHouse Cloud [\#](/blog/mintlify#choosing-clickhouse-cloud)


Nick wasn't coming to ClickHouse cold. Before joining Mintlify, he had co\-founded [Trieve](https://www.trieve.ai/), a search API startup that used ClickHouse for search analytics at over 100 requests per second. When Mintlify acquired Trieve in 2025, Nick—and ClickHouse—came along with it, effectively powering Mintlify's own search analytics. When the team began evaluating alternatives to PostHog, that positive firsthand experience gave him a strong starting point.


Still, the team did their due diligence, considering two other options. "DuckDB didn't meet our needs, as we had real\-time analytics that needed to horizontally scale to a larger growing customer base," Nick says. "BigQuery was very expensive and difficult to get started with relative to ClickHouse."


Ultimately, Nick and the team's familiarity with ClickHouse, combined with its ease of use, strong open\-source community, and wealth of real\-world examples made the decision easy.


The next question was whether to self\-host it or use [ClickHouse Cloud](https://clickhouse.com/cloud). Nick had self\-hosted at Trieve, so he knew what that entailed. For Mintlify, three things tipped the decision toward the managed service. First was ClickHouse Cloud's [Query Insights](https://clickhouse.com/docs/cloud/get-started/query-insights) tool. "The fact that you can put a query into ClickHouse Cloud and it can tell you whether or not that query is optimal was really huge for our team," Nick says. "It really carries a lot of the burden for us."


Second, the team wanted to use MSK, Amazon's managed Kafka service, to handle data ingestion. At Mintlify's volume, Nick says, "ClickHouse Cloud made it a lot easier to set up MSK with VPC peering than it would have been to do that on our own infrastructure."


Third, Mintlify simply is an ECS rather than Kubernetes shop, so self\-hosting on EKS would have added meaningful overhead to managing their own deployment. "As a result," Nick says, "it just made a lot more sense to use the cloud product."


## A two\-week migration [\#](/blog/mintlify#a-two-week-migration)


The migration took place in the fall of 2025 over a period of about two weeks.


Rather than cutting over all at once, the team dual\-wrote events to ClickHouse and PostHog simultaneously, querying both in parallel to compare results. To minimize disruption, they replicated PostHog's event schema directly in ClickHouse, mapping the same handler functions and API surface area one\-to\-one. "That made our migration super smooth," Nick says. "We didn't have to change much of our API surface area or integration."


Today, all of Mintlify's events flow exclusively through MSK into ClickHouse via [ClickPipes](https://clickhouse.com/cloud/clickpipes), ClickHouse's native ingestion service. Previously unavailable in PostHog, [incremental materialized views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view) are now at the core of how Mintlify serves analytics data to its customers, powering real\-time dashboards without expensive raw queries against the full dataset.


Along with customer\-facing analytics, the data powers an internal AI Slack bot that gives Mintlify's go\-to\-market team read\-only access to customer data, helping them spot high\-growth accounts and make more informed product decisions. "ClickHouse is great for that," Nick says. "These queries happen a lot faster than our previous solution, where we were hitting rate limits."


## Faster analytics, happier customers [\#](/blog/mintlify#faster-analytics-happier-customers)


For Mintlify's customers, ClickHouse delivered benefits right away. Dashboards that took tens of seconds to load in PostHog now return results in under a second. "Migrating to ClickHouse brought latency down and removed all of those rate limits," Nick says. "Now our analytics consistently show up correctly for our customers every single time—and show up quickly—which is just huge for improving satisfaction."


That satisfaction is evident in Mintlify's NPS score, which Nick estimates has increased by roughly 30%. "We went from around 10% of customers raising issues about analytics every week to zero reports per week of analytics bugs," he says. "We no longer get customer support messages about it not working, which was the best outcome."


Perhaps just as impactful from an operational standpoint, ClickHouse Cloud requires zero ongoing maintenance from Mintlify's engineering team. "We set up the thing and the thing runs," Nick says. "No one is full\-time managing it. It's straight\-up zero hours of work a week on average. That's the beauty of using ClickHouse Cloud."


Cost turned out to be a welcome bonus. Nick estimates that ClickHouse Cloud runs at around 60% less than what Mintlify was spending on PostHog for the same workload—though he's quick to note that cost was never the driving factor. "We really wanted product quality over anything else," he says. "Cost savings were just an added benefit."


## Lessons learned along the way [\#](/blog/mintlify#lessons-learned-along-the-way)


Having implemented ClickHouse twice now—first at Trieve, now again at Mintlify—Nick has a few recommendations for teams considering a similar move.


First, if you're dealing with high event volumes, use [ClickPipes](https://clickhouse.com/cloud/clickpipes) for MSK. "It's a lot more efficient than writing data directly, and ClickHouse Cloud with ClickPipes works really well and allows you to scale more smoothly," Nick says. It's a lesson he learned the hard way—Trieve didn't use MSK, and fixing that was one of the first things he did differently at Mintlify.


Second, start with a single events table and build [materialized views](https://clickhouse.com/docs/materialized-views) on top. As Nick explains, materialized views are a first\-class primitive in ClickHouse—essentially tables in their own right—so there's little benefit to managing a sprawl of separate tables. "You'll have a much easier time if you create one giant table for all your events and then create materialized views on top of that," Nick says.


Finally, he suggests using existing migration tooling rather than building your own. "Having migrations as code is important, and ClickHouse has recently invested in more tooling around that, which has been great." Starting from scratch, he adds, isn't worth the effort.


## Scaling for an agentic future [\#](/blog/mintlify#scaling-for-an-agentic-future)


For Nick and the team, the migration to ClickHouse achieved exactly what they set out to accomplish. "There are thousands of companies who are now able to look at traffic statistics for tens of millions of developers every month and figure out what in their product is working well, what's confusing, and where they should polish or spend time improving their documentation," he says. "As a developer myself, I'm super proud of that."


The executive team agrees. "Our CTO and CEO deeply care about the customer experience," Nick adds. "I can tell you they were quite happy and they trust ClickHouse to power our growth."


Looking ahead, the challenge—and the opportunity—is only getting bigger. With AI agent traffic growing exponentially, Mintlify is investing heavily in making sure the experience is as good for agents as it is for humans. That means analytics will only become more important, not less. "I think businesses that use Mintlify will need really fast, reliable analytics on how agents are using their product versus how humans are using it," Nick says. "As we figure out what the best insights are, we're going to continue using ClickHouse to make them easily available."


With ClickHouse Cloud, Mintlify's infrastructure is built for growth. "We've future\-proofed the architecture for many years of scaling beyond where we're at now," Nick says. "We're growing really fast, and it's not even close to the limits of what we see it doing."

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-358-get-started-today-sign-up&utm_blogctaid=358)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
