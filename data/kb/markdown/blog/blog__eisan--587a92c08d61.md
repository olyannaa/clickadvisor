# How Eisan made POS analytics faster, cheaper, and more reliable with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Eisan made POS analytics faster, cheaper, and more reliable with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 8, 2026 · 7 minutes read## Summary

Eisan built a real\-time ID\-POS analytics platform for multiple retail clients, supporting basket analysis, cross analysis, and personalized recommendations at scale They replaced a QlikView\-based BI stack with ClickHouse Cloud to improve reliability and performance while reducing licensing and infrastructure costs. The system now supports hundreds of millions of records per client today, with a clear path toward tens of billions through ongoing optimization.

For nearly four decades, [Eisan System Development](https://eisansystem.jp/) has built highly specialized software in domains where precision matters, from medical and healthcare systems to large\-scale data matching, and more recently, IoT\-enabled platforms. Much of that work runs quietly behind the scenes, supporting mission\-critical workflows for organizations that can't afford mistakes.


That mindset carried into a recent challenge Mamoru Ubukata, Eisan's Representative Director, shared at a [July 2025 ClickHouse meetup in Tokyo](https://www.youtube.com/watch?v=fKP-6-_PiZQ). It started simply, with a client asking for help. Their existing analytics system, built on a traditional BI tool, was starting to strain under growing data volumes and rising expectations for real\-time insight.


"They reached out to see if we could find a better solution," Mamoru explains. What followed was a pragmatic, engineering\-led search for a platform that could scale without sacrificing reliability—one that ultimately led Eisan to [ClickHouse Cloud](https://clickhouse.com/cloud).



## The old system: costly and unreliable [\#](/blog/eisan#the-old-system-costly-and-unreliable)


At the heart of the challenge was ID\-POS data: point\-of\-sale records tied to individual customer IDs, collected from supermarkets and drugstores. For retail clients, this data powers basket analysis and cross analysis, as well as real\-time personalization, where products are recommended as customers identify themselves in\-store. Over time, that data adds up, with some clients accumulating close to 200 million records per year.


The analytics platform Eisan had been using for this workload was built on QlikView and designed for speed—in theory, at least. Because everything was processed in memory, simple aggregations often came back in just a few seconds. "However," Mamoru says, "as the data increased, some processes could take minutes to process." Worse, the system began failing in ways that were hard to anticipate or control. "Recently, we've been seeing more and more cases where we don't even get analysis results back anymore. This is a very serious issue."


As more clients came onto the platform, cost pressures intensified. QlikView's licensing model meant expenses rose with every new deployment—something Mamoru describes as a "real burden and major concern for our users." The system's memory\-heavy design only amplified the problem. "Since QlikView processes everything in memory, it inevitably consumes a huge amount of memory," he says. "As a result, our server costs keep rising as well."


## ClickHouse to the rescue [\#](/blog/eisan#clickhouse-to-the-rescue)


The team's first instinct was to look for an open\-source alternative. The goal was to cut costs while regaining control over performance and scalability. They evaluated familiar options like PostgreSQL and distributed systems such as YugabyteDB. "None of them delivered the results we were looking for," Mamoru says. Discouraged, the team began to wonder if a better solution really existed. "You could call it a defeatist mindset, but we were just about ready to give up."


Then, almost by chance, they discovered ClickHouse. "Its speed was absolutely incredible," Mamoru says. "We thought, 'maybe this could actually work.'" That initial impression was enough to justify a deeper evaluation, and eventually, a move toward production.


At the Tokyo meetup, Mamoru shared a side\-by\-side comparison of the old QlikView\-based system and the new ClickHouse setup. While ClickHouse was clearly faster, the results didn't look dramatic on paper. But context, he says, matters. "QlikView is processing everything in memory. That's not the case with ClickHouse, which is really impressive."


Even compared to so\-called general configurations, ClickHouse produced stable results with fewer resources. "The ClickHouse server actually has slightly lower specs compared to typical setups, and we are running it under high\-load settings. Even so, the performance does not deteriorate and the results are very stable. With conventional products, if you want to do the same thing, you tend to decide to increase the hardware, but with ClickHouse I feel like you can solve the problem before that happens," says Ubukata.


Perhaps most importantly, ClickHouse behaves predictably under pressure. "With QlikView, it's pretty common for results to not come back at all," Mamoru says. "So far, we've never had a case where ClickHouse failed to return a result."


## The subtle art of server balance [\#](/blog/eisan#the-subtle-art-of-server-balance)


Once ClickHouse proved itself, a new question emerged: how to run it efficiently. Mamoru and the team began testing different configurations in [ClickHouse Cloud](https://clickhouse.com/cloud), focusing on the balance between CPU cores and memory. One setup used 30 cores and 120 GB of RAM, following a [1:4 core\-to\-memory ratio](https://clickhouse.com/docs/guides/sizing-and-hardware-recommendations#how-many-cpu-cores-should-i-use) commonly used as a starting point for ClickHouse workloads.


At first glance, the metrics raised questions. CPU utilization looked healthy, but memory usage appeared surprisingly low. "That led to a discussion about whether this balance is actually optimal," Mamoru says. After speaking with the ClickHouse Japan team, the picture became clearer. "That's when I learned that a fair amount of memory is being used for caching."


Once they accounted for that behavior, effective usage was closer to 100 GB, making the setup feel more balanced than it first appeared. The takeaway wasn't a fixed answer, but more of a process. "Of course, there are still a lot of different scenarios to consider," Mamoru says. The team continues to run load tests, adjusting server specs and observing how ClickHouse behaves under different conditions, refining the setup step by step.


## What's next for Eisan and ClickHouse [\#](/blog/eisan#whats-next-for-eisan-and-clickhouse)


Eisan's plans for ClickHouse extend well beyond the current system. "Ultimately, we're expecting the number of users to grow," Mamoru says. "Our goal is to be able to handle data on the scale of 100 billion records." Achieving that scale will take smart architectural decisions, along with continued testing and iteration as workloads evolve.


The team is also taking a closer look at how the system is used day to day. Right now, most analytics jobs run during business hours. "As a result," Mamoru explains, "the system is hardly used at night." To make better use of available capacity, they're exploring ways to shift weekly or monthly processing to off\-hours, smoothing resource usage over time.


[Autoscaling](https://clickhouse.com/docs/manage/scaling) is part of that conversation as well. So is the idea of more intentional, scheduled scaling. "I'm not sure if 'scheduled scaling' is the right term," Mamoru says, "but I think it could be possible to, say, completely shut down operations on Sundays. That could be useful."


For Eisan, ClickHouse is less a finished project than a foundation for what's ahead. Processing times are already improving, and new capabilities continue to expand what's possible. The real challenge is now operational: how to keep large\-scale, real\-time analytics systems running smoothly as both data volumes and expectations continue to grow.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-360-get-started-today-sign-up&utm_blogctaid=360)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
