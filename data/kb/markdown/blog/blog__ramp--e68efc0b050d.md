# “Just OLAP it”: How Ramp rebuilt its analytics platform on ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# “Just OLAP it”: How Ramp rebuilt its analytics platform on ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 20, 2026 · 7 minutes read## Summary


div.w\-full \+ p, 
pre \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

Ramp uses ClickHouse Cloud to power real\-time, customer\-facing analytics like AI\-powered spend insights and proactive budget controls. After struggling to support large enterprise customers, they migrated from Postgres to ClickHouse, turning 40\+ second queries into millisecond responses. They built a Postgres\-to\-Kafka\-to\-ClickHouse pipeline with denormalized enrichers, enabling millisecond\-speed reporting across 50,000 customers.

[Ramp](https://ramp.com/)’s engineers have a saying: “Just OLAP it.” It’s shorthand for what’s become second nature: whenever a route is slow or a dashboard starts to lag, they reach for ClickHouse.


“We’ve done this hundreds of times,” says Ryan Delgado, Director of Engineering and self\-proclaimed “ClickHouse enthusiast.” He leads Ramp’s data platform team, which is focused on building infrastructure and tools to help Ramp realize business value from their data. “We use ClickHouse a bunch. It’s been a game\-changer for us.”


Today, ClickHouse powers a wide range of customer\-facing analytics at Ramp, from AI\-powered spend insights to proactive budget controls. But two years ago, none of that existed.


Ryan joined us at our recent [Open House Roadshow in New York City](https://clickhouse.com/blog/open-house-roadshow-nyc-videos), where he shared how the team built a high\-performance OLAP platform on [ClickHouse Cloud](https://clickhouse.com/cloud), replacing Postgres bottlenecks with real\-time pipelines and helping Ramp scale its analytics.



## Ramp’s journey to ClickHouse Cloud [\#](/blog/ramp#ramps-journey-to-clickhouse-cloud)


With more than 50,000 customers, Ramp offers a modern finance operations platform that helps businesses control spend, automate accounting, and manage vendors from a single place.


“Our goal is to enable companies to reduce spend, while at the same time automating away the tedium that’s historically existed with back\-office finance,” Ryan says.


Today, the company is everywhere. In 2025, it aired its first [Super Bowl ad](https://www.youtube.com/watch?v=p1Tgsy7D0Jg), starring Philadelphia Eagles running back Saquon Barkley. Later that year, Ramp went viral after a [marketing campaign](https://briansoffice.com/) that featured “new CFO” Brian Baumgartner (aka Kevin from *The Office*) sitting in a fishbowl in New York’s Flatiron District filing expense reports “the old\-fashioned way.”


![image2.png](/uploads/image2_c0e288a8a3.png)
The final count: Ramp 600,000 \| Brian 123


“ClickHouse has played a critical role in powering our growth the past two years,” Ryan says.


But back in 2023, Ramp was facing a major problem. The company was growing fast, onboarding larger enterprise customers, each with thousands of cardholders generating huge volumes of transaction data. When those customers tried to run reports on infrastructure powered by Postgres, things started to get slower.


“We had a table that contained every single card transaction,” Ryan says. “When you’re running analytics on that table for a garage\-band startup, Postgres works great. But when a larger company tries to run this report, they’re going to wait longer. Sometimes, quite a bit longer.”


At first, the team tried to optimize what they had. They added indexes. They tuned queries. But that made only isolated and incremental improvements.. “We realized the tools we were using weren’t enough,” Ryan says. “We needed to do something else, and fast.”


In September, he reached out to an engineer in his network. He explained the problem and said he was thinking of switching to Apache Pinot or Druid. The engineer’s advice was simple: “You want ClickHouse.”


That night, Ryan spun up a local ClickHouse instance on his laptop. (“If you can do that locally without signing a vendor contract, that’s a huge green flag for any open\-source product,” he notes.) He loaded around 60 million card transactions into a [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) table partitioned by business ID, then used the ClickHouse SQLAlchemy library to run 16,000 randomized queries across 32 threads. “And then I just let it cook for a little bit,” he says.


“Twelve seconds later, it was done,” he explains. “And it was *fast*. I’ve never seen anything like that in my career. I knew we had something really special here.”


He hopped on a call with the [ClickHouse Cloud](https://clickhouse.com/cloud) team to learn more. “They just answered our questions and casually said, ‘Yeah, we have a cloud product.’ They didn’t try to sell it at all,” he recalls. “Needless to say, a week and a half later, we bought the cloud product.”


Immediately after talking with the ClickHouse team, Ramp formed a specialized “OLAP pod” of “four super cracked engineers hyper\-focused on solving the problem.” They built a process to denormalize in\-flight data, set up a Kafka\-based pipeline, and created Ramp’s first analytics\-ready ClickHouse table: enriched\_spend\_events.


In just four weeks, ClickHouse was in QA. By Thanksgiving, it was live in production for a handful of customers. Charts that once timed out after 40 seconds were returning in milliseconds. “A lot of the performance issues we saw at the enterprise level—we just erased them immediately,” Ryan says.


## Ramp’s ClickHouse\-based architecture [\#](/blog/ramp#ramps-clickhouse-based-architecture)


Today, ClickHouse is a foundational part of Ramp’s OLAP platform, serving backend teams and powering real\-time analytics across a variety of customer\-facing features.


The architecture starts with Ramp’s Postgres monolith, which emits change data capture (CDC) streams via Debezium into Kafka. Each table generates its own Kafka topic, and lightweight, stateless “enrichers” (written in Python) consume those messages, join them with relevant reference data, and emit denormalized records to downstream Kafka topics. The enriched data lands in ClickHouse via a Kafka\-to\-ClickHouse connector.


![Ramp user story Issue 1219.jpg](/uploads/Ramp_user_story_Issue_1219_e39e491b00.jpg)
Ramp’s OLAP pipeline: CDC from Postgres flows through Kafka enrichers into ClickHouse.


Inside ClickHouse, Ramp uses [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) tables to deduplicate incoming data, along with recurring [OPTIMIZE statements](https://clickhouse.com/docs/sql-reference/statements/optimize) and [FINAL query suffixes](https://clickhouse.com/docs/sql-reference/statements/select/from) to ensure consistency. “It works great for online analytics use cases,” Ryan says.


This setup powers features like [Reporting](https://ramp.com/reporting), which enables customers to generate ad hoc and recurring reports in\-app.


In addition, ClickHouse enables Ramp Budgets, a forecasting and spend control feature built for large, complex enterprise customers. “A large customer can forecast how much the engineering department will spend on travel and leisure in month one, two, three, four,” Ryan explains. “Then they can track that spending against the allocated budget from the start of the year.” When teams go over budget, Ramp can automatically trigger alerts or apply spend controls.


And the work isn’t done. Over the next year, Ramp plans to expand its OLAP footprint beyond spend data to include tasks, purchase orders, trips, vendors, and more. “I want enriched\_whatever for every single canonical Ramp data type,” Ryan says. “That’s something we’re really focused on and scaling across our product engineering organization.”


## “A classic Ramp story” [\#](/blog/ramp#a-classic-ramp-story)


Two years into their ClickHouse journey, what began as a scramble to fix slow analytics has become one of Ramp’s most important engineering investments. In just a few weeks, the team built a fast, flexible OLAP platform that underpins some of Ramp’s most advanced features, while scaling effortlessly to support even its largest enterprise customers.


“I’m biased, but I think it’s a great story—a classic Ramp story,” Ryan says. “We love ClickHouse Cloud. It's a great product, a great team, a great slope.”


And if anything’s slow? They just OLAP it.

### Ready to scale your team’s data operations?

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-38-ready-to-scale-your-team-s-data-operations-sign-up&utm_blogctaid=38)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
