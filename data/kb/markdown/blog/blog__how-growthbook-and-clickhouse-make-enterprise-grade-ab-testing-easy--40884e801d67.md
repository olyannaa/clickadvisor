# How GrowthBook and ClickHouse make enterprise\-grade A/B testing easy


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How GrowthBook and ClickHouse make enterprise\-grade A/B testing easy

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 11, 2025 · 7 minutes readWhen product teams ship new features, they do it with the best intentions. They've identified a user need, designed something they believe is intuitive, and debated the rollout strategy. But there's a problem: many new features don't deliver the impact teams are hoping for.


Industry\-wide, the success rate for product changes hovers around 30%. That means two\-thirds of what gets shipped doesn't meaningfully move the metrics it's meant to improve. "That's an awful lot of time spent on products that don't work" says Graham McNicholl, co\-founder of [GrowthBook](https://www.growthbook.io/), an open\-source feature flagging and experimentation platform.


The problem isn't a lack of effort or creativity. It's a lack of clarity. Without a way to isolate cause and effect, teams risk doubling down on features that aren't working. And even for those that do embrace experimentation, it's often expensive and hard to scale.


At a [March 2025 ClickHouse meetup in San Francisco](https://www.youtube.com/watch?v=pVNxXfVB2cE), Graham laid out the case for a better approach—and showed how GrowthBook, with the help of ClickHouse, makes enterprise\-grade experimentation possible for teams of all sizes.


## Why product teams need A/B testing [\#](/blog/how-growthbook-and-clickhouse-make-enterprise-grade-ab-testing-easy#why-product-teams-need-ab-testing)


Most of the time, product development feels like progress. You release a new feature, usage ticks up, and the charts in your dashboard trend in the right direction. But those aggregate numbers don't tell the full story, and they often lead teams astray.


"The impact of the products we ship is surprisingly non\-obvious," Graham says. "We're all trying to build great products, but even with our best efforts, we actually fail a lot."


In his presentation, he showed an A/B test from Airbnb that may have seemed like a clear win but ended up underperforming, and another from Netflix that appeared risky but turned out to be a success. Without a framework for controlled experimentation, both companies might have made the wrong call based on aggregate trends alone.


That uncertainty only gets worse as your product matures. Once you've optimized your core flows and eliminated low\-hanging fruit, it's harder to find meaningful wins. "The more optimized your product is, the lower your success rate becomes over time," Graham says.


In the face of this uncertainty, A/B testing tells you, with confidence, whether what you built is working. And that clarity is what separates high\-performing product teams—the Airbnbs and Netflixes of the world—from the ones still guessing.


## Scaling A/B testing without starting from scratch [\#](/blog/how-growthbook-and-clickhouse-make-enterprise-grade-ab-testing-easy#scaling-ab-testing-without-starting-from-scratch)


As teams mature, so does their approach to experimentation. Early on, A/B tests are run manually on the most important parts of a product—onboarding flows, pricing pages, checkout steps. As those tests show results, appetite grows. What begins as a handful of experiments becomes dozens, then hundreds. Teams move from "walk" to "run," as Graham puts it, testing across product areas with help from dedicated data and growth leads.


At the highest level—what Graham calls ubiquitous experimentation—A/B testing becomes the default for how you launch anything. "Every change, no matter how small, is an A/B test," he says. At product powerhouses like Microsoft and LinkedIn, there are hundreds of thousands of experiments running each year, often in parallel, "down to the pixel."


But operating at that scale requires a fundamentally different kind of system. "When you're running five tests, the product that you build and how you scale it is entirely different from the product you build for 100,000 tests," Graham says.


To make that level of experimentation work, you need a system that's fast, flexible, and self\-serve—where any team can run tests without one team or one person being the bottleneck. You also need the cost per test to be as close to zero as possible. "If you're running 100,000 tests and you're paying per test," Graham says, "you're probably going to go broke." And the platform needs to support your custom metrics and keep up with your event volume.


Needless to say, that's a big lift. It's why many companies at this stage end up building their own experimentation platforms from scratch. But for teams that can't justify the time, cost, or complexity, GrowthBook and ClickHouse offer another path.


GrowthBook gives teams the flexibility of a homegrown system without the overhead. It's open\-source, warehouse\-native, and designed to work with the data and metrics you already have. ClickHouse, meanwhile, delivers the speed and scale to query raw event data in real time, without complex pipelines, expensive infrastructure, or heavy pre\-aggregation.


"Our goal, together with ClickHouse, is to bend that curve," Graham says, "so you can get really sophisticated, enterprise\-grade experimentation without requiring much effort at all."


## How GrowthBook and Clickhouse work together [\#](/blog/how-growthbook-and-clickhouse-make-enterprise-grade-ab-testing-easy#how-growthbook-and-clickhouse-work-together)


GrowthBook is built to sit on top of your data warehouse—no black boxes, no custom setup. Teams can assign users to experiments using feature flags, track exposure events through their existing analytics tools, and run real\-time queries using their own definitions of success.


"The idea is that it's a self\-hostable A/B testing platform you would build in\-house—only you don't have to build it," Graham says.


While GrowthBook supports a variety of data warehouses, ClickHouse is an ideal fit for teams with real\-time performance and cost\-efficiency needs. "We're huge ClickHouse fans," Graham says. "If you haven't made a decision about where to put your data, it's a great option."


In the below setup, ClickHouse serves as "the center of your data analytics." Event data flows into ClickHouse through pipelines like Kafka and ClickPipes. From there, GrowthBook connects directly to ClickHouse and runs statistical analysis over raw data, without the need for pre\-aggregation or intermediate ETL jobs.


"Once you get your data into ClickHouse," Graham explains, "you just plug GrowthBook on top of that, and we can query that data for you."


![growthbook.png](/uploads/growthbook_fc42a3f59b.png)

*GrowthBook uses ClickHouse to power real\-time A/B testing directly from raw event data.*



This warehouse\-native approach gives teams full visibility into how experiments are defined and analyzed. It's also highly flexible. Whether you use React or Cloudflare Workers, send events through Segment or straight from the edge, the setup can be tailored to fit your stack.


And thanks to ClickHouse's performance, GrowthBook can run complex queries across hundreds of thousands of rows in just seconds. At the [San Francisco meetup](https://www.youtube.com/watch?v=pVNxXfVB2cE), Graham demoed exactly that: querying multiple fact tables, pulling in exposure and conversion events, and running a full experiment analysis using a ClickHouse Cloud instance loaded with real data.


"A lot of the heavy lifting data teams usually have to do, like running DBT or building complex pipelines, you just don't need," Graham says. "You can get really, really far just piping raw event data into ClickHouse and querying it in real time to get great results."


## Test like the best [\#](/blog/how-growthbook-and-clickhouse-make-enterprise-grade-ab-testing-easy#test-like-the-best)


Experimentation at the scale of companies like Airbnb, Netflix, and Microsoft used to require a massive platform team and years of investment. But with GrowthBook and ClickHouse, that enterprise\-level rigor is within reach for teams of all sizes.


GrowthBook's open\-source platform gives teams the tools to run sophisticated A/B tests with flexibility and control. It's warehouse\-native, easy to integrate, and designed to fit into your existing data stack. Paired with ClickHouse, it provides the speed and visibility teams need to experiment fearlessly and build with confidence.


To learn more about ClickHouse and see how it can bring speed and scalability to your team's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
