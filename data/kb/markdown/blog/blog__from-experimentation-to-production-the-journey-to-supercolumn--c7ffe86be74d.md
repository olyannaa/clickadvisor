# From experimentation to production, the journey to Supercolumn


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# From experimentation to production, the journey to Supercolumn

![Nanocorplogo.png](/_next/image?url=%2Fuploads%2FNanocorplogo_e3c5fe8a64.png&w=96&q=75)Florian ThebaultJul 28, 2022 · 11 minutes read*We’d like to welcome NANO Corp. as a guest to our blog. Read on to find out why they are using ClickHouse and their journey from discovery to production.*


**On why exactly NANO Corp. switched to ClickHouse to support its NOC as a Service (NOCaaS) offering and never looked back!**


From the outside, our journey to ClickHouse might not seem groundbreaking. But for a company founded by older gentlemen sporting a wealth of experience in software development fueled by age\-old ideas about tech in general, we didn’t foresee having our convictions shattered in such a fashion ????.


But before we go into details about this journey, let’s have a few words about us, what we are about and what we were, or are, trying to achieve.


## About NANO Corp. [\#](/blog/from-experimentation-to-production-the-journey-to-supercolumn#about-nano-corp)


NANO Corp. is a young French startup founded in 2019 by former defense personnel. We created the company around in\-house technologies we developed ourselves and patented: a groundbreaking dust\-off of what software network probes should be. We made them versatile, lighter than ever before while also being able to easily handle bandwidth of up to 100GBit/s without using any shameful gimmicks like packet slicing or sampling. Lest I forget, it also works entirely on commodity hardware (and cheap ones, at that – you can check our blog for some specs if you want to have a look) on a full CPU basis (once again, no pricy FPGAs or ASICs for us).


What we offer could be summed up in one word: **Observability**. But not the traditional “network monitoring” kind. No *Netflow, sflow, IPFIX* or *SNMP*, and the likes for us. Those technologies work fine, but they lack the breadth and room to grow. They all lack visibility in one way or another and none of them can really do cybersecurity. Based on the absolute unifying link: **the Network**, our core vision is that network performance and cybersecurity are two sides of the same coin, addressing the first without the second makes no sense.


Our main goal is now to analyze complex and changing network traffic at line\-rate high speed. And to do it with asynchronous feed (different probes installed in and around several layers of the network). Pretty challenging, right?
Basically, the database we were looking for had to be:


- Able to deal with fast (and constant) inserts while running periodic queries for alerting and custom queries launched by multiple users,
- Equipped with a hot/cold data buffering system to store data in RAM for alerting queries,
- Easy to maintain and deploy,
- Able to ingest huge volumes of data on one system and still being nimble. Meaning: not having to multicluster / shard too quickly before we hit the 10TB mark (and even after, actually)
- Be very efficient in RAM usage


As you might have guessed, to use the full potential of our network probes and bundle them into products as pervasive as we wished them to be while being able to tackle nowadays’ many hybrid challenges (M/L, cybersecurity, etc...), we needed our probes to be supported with a pretty good database. And that’s where some of our initial hurdles came from. Because we didn’t know it at the time, but what we needed in fact, was a database as groundbreaking as our probe!


## Habits die hard, older habits die even harder [\#](/blog/from-experimentation-to-production-the-journey-to-supercolumn#habits-die-hard-older-habits-die-even-harder)


Traditional RDBMS have long been built around smart transactional management systems. A technology that serves many use cases well and has done that well for ages. Our main engineers successfully used MySQL or PostgreSQL in their previous careers. We knew most of them wouldn’t make the cut, in the long run. Their data schemes are too heavily reliant on update speed and need clustering when overall performance becomes an issue.


But we still tried a couple of those “dad\-a\-base" ????. Mainly because OLTP seemed a prerequisite for some of the queries we had in mind. I am not sure I can mention their names (all good ones, but they just didn’t fit our needs). Let’s say we weren’t expecting much at the time, and even then, we still got disappointed.


To give you a little more context, we had to get successful benchmarks for extracting flow metadata on 1Gb/s networks. In extreme cases, we had to feed as many as 1\.4 million flow/s inside the database (around 30 to 250 columns depending on circumstances). Let’s just say traditional RDBMS or graph databases were not giving us 25% of what we needed on the hardware we had.


And our endgame was to make it run smoothly on 100Gb/s networks... I guess that’s what you get with ***crud*** work ;\-)


But let’s go back a little bit and let me give you more context.


## Best broths are cooked in the oldest pans... or it is said [\#](/blog/from-experimentation-to-production-the-journey-to-supercolumn#best-broths-are-cooked-in-the-oldest-pans-or-it-is-said)


To tell you the truth, dear reader, OLAP was not my first choice of database. And ClickHouse wasn’t either. Coming from Yandex (but Open Source), we had some reservations. First and foremost, I was looking for OLTP hyperscaling databases where sharding or multi\-clustering was the name of the game.


Buzzwords are important. I remember one of my first client, that was pre\-COVID, and in another company (that was literally the Dark Ages). That client was hell\-bent on a Hadoop multi\-clustering infrastructure with TCO in the 7\-digits (euros). All of that to support very basic NLP ETLs expected to handle several hundred MB of data…. monthly. But at the time, Hadoop was all the rage and the CTO of that administration wanted to play with that shiny new toy. Without realizing what it truly entailed. That was my first real true taste of the power of buzzwords in tech. So, when Nano’s story begins, multi\-clustering was already the answer to every problem data storage was rumored to have.


In the end, I too was looking to design and implement multi\-clustering databases. Because it was cool and because with the numbers I had playing in my mind, I was pretty sure no other databases than XXXXXXXX could handle the expected volumes of data. Not without many clustering and replication nodes for speedy querying. Unfortunately, deploying multi\-clustering databases without spending enough time on designing and building robust data schemes is like having your cake and eating it. Unless you are in a hugely profitable company with C\-Suite personnel without knowledge of real prices in tech, you quickly realize there is no free lunch, eh?


Our pre\-requisites were harsh, and we were looking for top\-notch performances over anything else…. The asymptotic quest of the dream world in tech. But then we had to discuss something techies don’t really like to think about: cost. Because in their minds, performance is a pure abstract in a perfect world of numbers and ideals. A world where money is dirty, only meant to be talked about by droning bean\-counters wanting to kill their dreams. Remember, we could spend weeks shaving off 3 to 4 nanoseconds for each network packet managed by the probe… the change we had to make in our mindset was pretty huge.


Early hardware requirements to support the database meant to ingest data from multiple 10Gbit/s probes, for example, were… staggering. And that was without considering the fact using OLTP database meant we would have needed people to maintain such complex architectures. Some would say multi\-clustering is always messy, especially when it’s done right. But… we were (and still are at the time I write those lines) a small company. We wanted cheap, we wanted powerful, scalable and of course, we wanted “easy” at all stages. No mean feat, I can tell you that.


In the end, all our initial tests with traditional OLTP databases were... well... disappointing, to say the least. And it didn’t scale. Even when they said it did. To increase efficiency, we had to spend an inordinate amount on hardware. Which was contrary to all our core beliefs (and those of the procurement desk at any of our clients’ ;\-)


## A fresh breeze from the East [\#](/blog/from-experimentation-to-production-the-journey-to-supercolumn#a-fresh-breeze-from-the-east)


One day, while I was steadily losing hair and sleep, here came my Lead Data Scientist. With a coffee in one hand and his phone in another, telling me quite jokingly: « I want to try out ClickHouse! ».


I can’t tell you enough how much gall that guy had at the time!


We had a client who wanted a sizing and I had been spending days (and weekends) designing an artful data scheme and squeezing through hardware options…. And he was coming to me, asking us to deploy an underdog newcomer into the database community.


In his hunt for a data store running analytical queries over huge volumes of data with interactive latencies, he literally ran across ClickHouse, touted as the fastest data warehouse in the market.


I’m sure you’re already thinking. Fastest data warehouse... we’ve all heard that one, before, right? Spoiler alert: it is the speediest. Actually, it was so fast that I was sure our first benchmarks had to be buggy, and the results had to be fake. I asked my lead data scientist to take a look at those benchmarks. He stopped, watching with curious eyes as he sent query after query and it returned us numbers in a blink of an eye, what normally took several seconds or even minutes with my legacy database, was now done in milliseconds. Wow.


At the time, I thought: “if Cloudflare, a worldwide company specialized and renowned in network, chose ClickHouse, it could only mean they must be onto something ????"


After we ran a bunch of different tests, we were won over. But why exactly? Well, mainly for ClickHouse’s fast multiple inserts, fast indexing, powerful materialized views, its wonderful MergeTree function, and of course, its great documentation supported by an even better community (though that’s a very personal opinion, of course).


Even though later, we had a quick peek at other OLAP databases, like Druid or Pinot, we stayed with ClickHouse. In no small part because data ingestion in ClickHouse is far more efficient than with its alternatives. It doesn’t need to prepare “segments” containing strictly all data falling into specific time intervals and it allows for simpler data ingestion architecture and easier maintenance (remember, we are still a small startup) and it saves computational power. Which is needed because our probes send data for ClickHouse to be ingested constantly while also running constant queries on hot and cold data. ClickHouse’s batch insert philosophy was also especially suited to our technology as we make intermediary batches ourselves for all data to be ingested (a bit like Kafka does, actually, though on a faaaar lower spectrum).


Basically, data ingestion in ClickHouse is much simpler, less taxing on resources, and it lets you do immensely fast lookup queries! The best of both worlds. Now, if only ClickHouse could handle JSON format file natively... what? They do that, now? Wow...


In the end, I can say we stumbled into ClickHouse after being frustrated with all other alternatives and stayed because it was the perfect fit ;\-)


Next time, we will talk about a specific use case: how we dealt with multiple asynchronous data feeds for high\-volume inputs.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
