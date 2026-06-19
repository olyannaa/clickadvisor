# Trouble will find you: How Cloudflare uses ClickHouse to scale analytics at quadrillion\-row scale


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Trouble will find you: How Cloudflare uses ClickHouse to scale analytics at quadrillion\-row scale

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 18, 2026 · 7 minutes readFor [Cloudflare](https://www.cloudflare.com/en-ca/)’s Jamie Herre, trouble is the engineer’s version of Murphy’s Law: whatever *can* go wrong *will* go wrong, and at scale it’s not a matter of *if* but *when*. A drive fails. A server goes down. A certificate expires. A link breaks. “If you carry a pager, you know what I’m talking about,” he says. “You can always assume something is broken somewhere.”


When Jamie joined Cloudflare as Senior Director of Engineering in 2018, its events pipeline was already “by far” the biggest he’d ever seen. Seven years later, the company has grown to serve roughly one\-fifth of the world’s websites. What once looked enormous now feels modest compared to the quadrillions of events Cloudflare processes daily.


Scaling, Jamie argues, isn’t a milestone or a box to check. It’s a journey of constant adaptation: to more data, more complexity, more failure. Each new ceiling eventually becomes the floor for what comes next. “When we talk about scaling, it’s not a process that ends,” he says. “As you go up in scale, things are going to fail more frequently.”


Trouble and scaling, in this sense, are two sides of the same coin. A sudden surge in traffic can look a lot like losing half your capacity to an outage, and vice versa. In both cases, the system is stretched beyond yesterday’s limits. The challenge for designers and engineers, Jamie says, isn’t to avoid that stress—that’s impossible—but to build infrastructure that bends without breaking, and keeps delivering answers in the face of inevitable failure.


## What good trouble looks like [\#](/blog/cloudflare#what-good-trouble-looks-like)


To show what “bending without breaking” looks like in practice, Jamie demoed his team’s analytics system at an [August 2025 ClickHouse meetup](https://clickhouse.com/videos/meetupsf_august_2025_2) at Cloudflare’s office in San Francisco.



The first results showed the system’s scale. A single query scanned 96 trillion events in an hour and returned in less than two seconds, with a margin of error under one percent. Zooming out to a full day, the same query covered 1\.61 quadrillion events—and still finished in less than two seconds. For Jamie, part of the fun was being able to say “quadrillion” out loud (“it’s a vanity thing,” he jokes) but his point was serious: even at volumes that, for many teams, would defy imagination, the system continued to respond instantly and accurately.


Then came the stress test. What happens when trouble arrives not as a traffic surge, but as a loss of capacity? Jamie simulated disconnecting a major North American data center, and then all of North America at once. Errors spiked, as expected, but the queries kept returning results. Thanks to Cloudflare’s distributed, active\-active design, with more than 300 data centers around the world, European clusters automatically picked up the load, and the results remained consistent within the same tight margin of error.


Even when scaling the query window—from an hour to a day, a week, a month, and even a year—the system’s performance held steady. “No matter how much I ask it for, it will return results in less than two seconds,” Jamie says.


The demo proved that Cloudflare’s analytics system is both resilient and responsive. It can withstand large\-scale outages and changes in scale without collapsing, and return queries in seconds regardless of load, capacity, or volume. In other systems, maintaining that level of responsiveness at extreme scale would require complex coordination, aggressive tuning, and major architectural tradeoffs, but ClickHouse lets Cloudflare operate this way by design. The fundamental assumption may be that “something is always sub\-optimal,” but that doesn’t prevent successful responses.


“At Cloudflare, we’re always scaling,” Jamie says. “There’s always more trouble tomorrow. But we’ve designed our system around ClickHouse to be able to deal with that.”


## Why ClickHouse works for Cloudflare [\#](/blog/cloudflare#why-clickhouse-works-for-cloudflare)


“So what’s so great about ClickHouse?” Jamie asks. It turns out, quite a lot.


Cloudflare has been running on open\-source ClickHouse for nearly 10 years, making it one of the OLAP database’s earliest large\-scale adopters. That long history has shaped how Jamie and his team think about resilience and performance at global scale.


One “underrated feature,” according to Jamie, is the HTTP protocol. Cloudflare’s analytics clients interact with ClickHouse entirely over HTTP, which makes integration simple and universal. “There are all these tools and modes that you can leverage,” he says.


He also highlights the “minimal coordination required.” Unlike systems that rely on constant Raft or Paxos negotiation, ClickHouse nodes don’t need heavy orchestration to keep working. “When I take away a third of the capacity, like we did in the demo, not that much goes wrong, because all of those nodes are still there,” he explains.


That philosophy extends to what Jamie calls “soft clusters”—the ability to interrogate any node and choose dynamic combinations. “This gives us a lot of control and flexibility about how to find the nodes that are working and happy,” he says. There’s also what he calls “optional complexity,” or the ability to turn features on and off as needed. “We’ve tried to leverage the things that work well for our specific use case,” he adds.


Even the SQL dialect has turned out to be a “surprising advantage.” It took some getting used to, but over time Jamie has come to value how expressive and efficient it is for the team’s workloads. “It’s really cool,” he says.


Finally, Jamie emphasizes the value of ClickHouse’s open\-source community and source code. For Cloudflare, being able to understand, contribute to, and rely on the database’s evolution has been valuable. “We’ve gotten a lot over the years by being part of this community,” he says.


## Jamie’s advice—just do it! [\#](/blog/cloudflare#jamies-advicejust-do-it)


Jamie closed his talk with a reminder that scaling is never finished. The best time to prepare is right now. “It’s never too early, and it’s never too late,” he says. “You’ll never be done.”


The important thing, he argues, is to think about scaling *before* trouble forces your hand. “Say your workload suddenly scales 10x or 100x—would it fail in a good way, or would it fail in a bad way? And then the inverse of that is, what if you lose nine\-tenths of the capacity? Would it just keel over? Or would you still be able to use it successfully?”


For Cloudflare, these aren’t hypotheticals. With quadrillions of events a day, hundreds of data centers around the world, and the omnipresent inevitability of failure, the company has to design for explosive growth and catastrophic loss at the same time. ClickHouse gives Jamie and his team the flexibility to handle either scenario without sacrificing speed or resilience.


Your company may not operate at Cloudflare’s scale, but the same design principles apply whether you’re starting with gigabytes or scaling from terabytes to petabytes—the goal is simply to be ready when scale arrives.


The lesson is universal. Trouble is guaranteed. The only question is whether you’ll be ready when it finds you.

### Ready to make your systems more resilient?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-63-ready-to-make-your-systems-more-resilient-sign-up&utm_blogctaid=63)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
