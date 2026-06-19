# How ChatFeatured migrated from PlanetScale Postgres to Postgres Managed by ClickHouse to power AI brand discovery


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How ChatFeatured migrated from PlanetScale Postgres to Postgres Managed by ClickHouse to power AI brand discovery

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 18, 2026 · 12 minutes read## Summary

- ChatFeatured helps brands influence how they appear in AI search engines like ChatGPT, Perplexity, and Gemini, from analytics to content execution.
- They were already running ClickHouse for agent analytics with 20x compression, but needed a way to run it alongside Postgres without managing two systems.
- Postgres managed by ClickHouse gave them a single platform for transactional and analytical workloads, cutting analytics query times from 2\.5 minutes to \<1 second.
When someone asks ChatGPT to recommend an [OLAP database](https://clickhouse.com/resources/engineering/what-is-olap), or asks Perplexity what skincare brand works best for their skin, the answer they get isn’t random. It’s shaped by what AI models have read, cited, and learned to associate with authority. For brands, that means a new kind of visibility challenge, and a new kind of platform to solve it.


[ChatFeatured](https://chatfeatured.com/) is one of the fastest\-growing solutions in this space. The Toronto\-based startup helps brands track, optimize, and influence how AI models discover and recommend their brand. Where other tools stop at showing brands how they show up, ChatFeatured closes the loop, telling marketers what content they need and actually helping them produce it.


“We talked to customers, and they told us, ‘The data’s great, everyone’s giving me data… but what do I do with it?” says co\-founder and CTO Nithiiyan Skhanthan. “They said, ‘I don’t know anything about search engine optimization. You guys are the experts… you take care of it.”

Loading video...Nithiiyan and his co\-founder Farris Nasr built what they call an “embedded AEO strategist,” effectively an AI agent that analyzes the sources AI models are citing, identifies what content would improve a brand’s visibility, and guides marketers through producing it. In just a few months, the platform has already attracted customers from all over the world, including billion\-dollar companies like Cooper Consumer Health. “It goes to show how much of a problem this is, and that execution really is the most important part,” Nithiiyan says.


For a fast\-growing, analytics\-first product like ChatFeatured to deliver on its promise, it needs to handle transactional workloads and power complex analytical queries, ideally without the overhead of managing two separate systems. We caught up with Nithiiyan to learn how [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres) gave them the best of both worlds.


## Three providers, same problem [\#](/blog/chatfeatured#three-providers-same-problem)


The recent emergence of tools like Cursor and Claude Code has changed how founders think about technology, prioritizing speed\-to\-market before long\-term scalability. As Nithiiyan puts it, “Most people, especially with the rise of AI coding, aren’t asking, ‘What stack do I need to scale to 1,000 users?’ They’re asking, ‘What stack do I need to get this out as quickly as possible to validate the idea before sinking time into the architecture?’”


ChatFeatured’s story was no different. Like most startups, they began with Postgres. It was quick to get up and running, flexible enough to handle both application and basic analytics needs, and well\-understood. “There’s a lot of talk out there saying you can do anything you need for your first version with Postgres,” Nithiiyan says. “Me being the person who had to put this together, I started with that methodology, and I think it makes sense.”


As they built the first version of the product, the team cycled through three managed Postgres providers, starting with Digital Ocean. “It was cheap and easy… for about 20 dollars, you can get a decent\-sized instance,” Nithiiyan says. While it worked fine at first, once the platform was ingesting around 1,000 prompts a day across six AI models, it became too slow for real users.


With the second provider they tried, performance improved. But as the customer base grew, CPU usage during nightly prompt ingestion windows climbed to 90%, leaving little headroom for growth. As Nithiiyan says, “If I want to add 100 more customers tomorrow, I’d need to scale the database up significantly just to maintain the same performance.”


Having heard good things about PlanetScale, they decided to try that instead. “Once I switched over, though, I wasn’t super impressed with the performance,” Nithiiyan says. On top of that, they were IOPS\-bound, meaning the storage layer was hitting a hard ceiling on read/write operations. Upgrading to PlanetScale’s Metal tier could remove that ceiling, but with how much data the team was ingesting into Postgres, the cost made it a non\-starter.


Even if Metal had been affordable, it was becoming clear to Nithiiyan that there was a more fundamental issue at play. Postgres may be great for transactional workloads, but analytics is at the heart of everything ChatFeatured does, and no managed Postgres service they tried was going to change that. “As you start to scale to more users, you find certain limitations where a different technology would be useful,” he says. “That’s when I started looking into specific analytics databases like ClickHouse.” They needed an architecture where Postgres and ClickHouse worked seamlessly together, with each database handling the workloads it was best suited for, making the platform faster and more cost\-efficient.


## The best of both worlds: Postgres for OLTP and ClickHouse for OLAP [\#](/blog/chatfeatured#the-best-of-both-worlds-postgres-for-oltp-and-clickhouse-for-olap)


In the early days of ChatFeatured, Nithiiyan says the team was “more concerned with being right than fast.” Even so, they knew speed would be core to the customer experience, especially for a product meant to feel like a knowledgeable colleague you can just talk to.


“If analytics queries are taking so long that we can’t access the data in time, it ruins and diminishes the experience,” Nithiiyan says. “People using ChatGPT are used to replies within a couple of seconds. If we have to wait 30 seconds for an analytics query, we’re going to lose the user before our agent can deliver any value.”


Nithiiyan had known for a while that ClickHouse was the right tool for the job. In fact, he was already running a self\-hosted version to power ChatFeatured’s agent analytics. The platform captures AI crawler traffic at the CDN/Server level, tracking when agents visit a customer’s website and using that data to inform content recommendations. Batching thousands of those requests into ClickHouse, he recalls being blown away by the [compression](https://clickhouse.com/resources/engineering/database-compression) numbers: “I remember thinking, ‘There’s no way, this has to be missing data.’ It’s so small and efficient. Even when I need to query that data, it loads instantly."


That experience alone was enough to make him a believer. “I really wanted to use ClickHouse,” he says. “If I could choose one database for my analytics queries, it would be ClickHouse.”


But knowing ClickHouse was the right answer and being able to use it as the backbone of the platform were two different things. ChatFeatured still needed Postgres for the [transactional side of the business](https://clickhouse.com/resources/engineering/oltp-vs-olap) (the application layer, user data, account management). Adopting ClickHouse would mean [running two separate databases](https://clickhouse.com/resources/engineering/unifying-oltp-and-olap), maintaining the pipelines between them, and taking on the operational overhead of both. For a bootstrapped startup also trying to build a product and close customers, that wasn’t a tradeoff he was ready to make.


Then [ClickHouse announced its managed Postgres service](https://clickhouse.com/blog/postgres-managed-by-clickhouse). Unlike other managed Postgres providers, it uses NVMe storage physically colocated with compute, delivering up to 10x faster performance. Crucially for Nithiiyan and the team, it also comes with a native, built\-in path to sync data directly to ClickHouse for analytics, bringing both workloads together under one unified platform.


“When I saw Postgres managed by ClickHouse, I got really excited,” he says. “I thought, ‘That’s perfect. I don’t need to manage two fully separate databases. This will be the one drop\-in solution that lets me take advantage of ClickHouse’s speed and Postgres’s transactional readiness.’”


## A 30\-minute migration from PlanetScale Postgres to Postgres managed by ClickHouse [\#](/blog/chatfeatured#a-30-minute-migration-from-planetscale-postgres-to-postgres-managed-by-clickhouse)


Rather than manually dumping and restoring data, Nithiiyan used the Postgres\-to\-Postgres [ClickPipes](https://clickhouse.com/docs/cloud/managed-postgres/migrations/clickhouse-cloud) connector, a purpose\-built migration tool based on technology battle\-tested across more than 1,000 customers. He simply pointed it at his PlanetScale source, and it took care of the initial load, schema transfer, and continuous sync. From there, all it took was a five\-minute maintenance window to complete the migration. “I’ve migrated between three different Postgres platforms before,” he says, “and this one was by far the simplest.”


What made the difference, he adds, was the ClickHouse team working alongside him: “I love hopping on a call with engineers who really know what they’re doing. Sai and everyone else are experts in doing exactly this. That inspires a lot of confidence that the data we have is not going to suddenly get lost.”


That combination of a productized migration solution and deep, hands\-on expertise from the ClickHouse team was the key to what Nithiiyan describes as an “incredible migration experience” that, from start to finish, took a grand total of 30 minutes.


## Real\-World Customer Impact: From minutes to milliseconds [\#](/blog/chatfeatured#real-world-customer-impact-from-minutes-to-milliseconds)


One of ChatFeatured’s first full\-service customers was [LifestyleRx](https://lifestylerx.com/us). On PlanetScale, a single 30\-day analytics query for LifestyleRx took around two and a half minutes. Denormalizing the data brought that number down to 90 seconds, but that was still far too slow for what was always designed to be a user\-facing product. Nithiiyan knew that if ChatFeatured’s own team couldn’t even work with the product efficiently, they could never claim to offer a better experience than the tools they were trying to replace.


With ClickHouse, he says, that same query now loads in less than a second. “I was so genuinely shocked at how good it was that I remember popping into the chat and saying, ‘Guys, this is incredible, I didn’t realize this sort of performance existed.’ It’s crazy that we exist in a world where this kind of performance is just so readily available and so well integrated.”


It was a feeling he’d experienced before with ClickHouse. When he first started running ChatFeatured’s CDN log data through his self\-hosted ClickHouse instance, he was similarly taken aback to see 20x compression. “Percentage\-wise, it’s incredible,” he says. “As we scale to more customers, that’s going to be a huge unlock for us.”


For ChatFeatured and its users, the real impact goes beyond the numbers. ClickHouse’s performance unlocks features the team previously avoided building, like showing customers their full performance history since joining the platform, queries that would have taken minutes on the old infrastructure. “On ClickHouse, it  takes milliseconds,” Nithiiyan says. “It enhances our roadmap, because I’m no longer worried about performance when it comes to analytics.


In a small but telling sign of how much things have changed, he adds, “I spent so much time making the loading screen look good. Now I don’t need to worry about that anymore.”


## A unified stack that’s built to scale [\#](/blog/chatfeatured#a-unified-stack-thats-built-to-scale)


From day one, Nithiiyan and his co\-founder Farris have been clear about creating a frictionless experience that helps marketers do more, faster. “That was the number\-one reason we were looking into ClickHouse to begin with,” he says. “How do we impress our customers by being faster, and offering a better experience than our competitors?”


Now, with [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres) handling the transactional layer and a path to offloading analytics queries to ClickHouse as the platform scales, Nithiiyan is looking forward to what comes next. “I’m excited for agent performance to be a much smoother experience now that we’re using ClickHouse,” he says. “I think it’s going to be a huge unlock for the experience of using our platform. And experience is our biggest differentiator.”


Less than a year into their journey as a company, ChatFeatured has seen its share of managed service providers. “I’m not going to switch from this one, because I like the team and the product is the best I've used by far”” Nithiiyan says with a smile. That peace of mind is worth a lot. “With ClickHouse, I don’t need to worry about changing my stack or finding a different provider to get the performance I need. I’m in the best place I need to be. That’s just one less thing on my mind as a founder.”

### Try Postgres managed by ClickHouse

Need transactional reliability and blazing\-fast analytical queries in one unified stack? Try Postgres managed by ClickHouse.
[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-818-try-postgres-managed-by-clickhouse-get-access&utm_blogctaid=818)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
