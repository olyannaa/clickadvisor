# DeepL’s journey with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# DeepL’s journey with ClickHouse

![DeepLlogo.png](/_next/image?url=%2Fuploads%2FDeep_Llogo_e8d7d2bc31.png&w=96&q=75)Jannik Hoffjann \& Till WestermannJul 26, 2022 · 6 minutes read*We’d like to welcome DeepL as a guest to our blog. Read on to find out how DeepL is using ClickHouse as their central data warehouse.*


At DeepL, we use ClickHouse as our central data warehouse. Today, it serves multiple use\-cases: From analytics for our websites and apps, to making company metrics available to everyone, as well as technical monitoring. In this blog post we would like to tell you about our journey with ClickHouse, how we started, and what we have built.


## How it started [\#](/blog/deepls-journey-with-clickhouse#how-it-started)


Our journey with ClickHouse started in 2020 when we wanted to build up our analytics capabilities in a privacy friendly manner. Back then we evaluated several options to self\-host a solution. The Hadoop world was deemed as too maintenance intense and would have taken too long to set up. With ClickHouse having a single binary deployment from an apt\-repository, it was very easy and quick to set up an MVP (Minimum Viable Product) to see if things would work out on our scale. We started with a single node setup where ClickHouse was running inside of a VM and the hypervisor was even shared with several other services.


The MVP consisted of having an API where the user’s browser would send events to, Kafka as a message broker, a sink writing from Kafka to ClickHouse, ClickHouse itself, and Metabase to visualize the results. The architecture looked something like this:


![DeepLArchitecture.png](/uploads/Deep_L_Architecture_c7545bef5f.png)
The MVP was put together in a couple of weeks and proved that the system was capable of easily handling the amount of data we were throwing at it and query times were excellent.


As a next step we invested heavily in automation. In hindsight this was a very wise decision as the team would have gotten swamped with toil to change table schemas when frontend developers would create new events. We decided to have a combined source of truth for all events and the table schema. When Frontend wants to create a new event, they would need to define this event in protobuf. This protobuf schema file is used for three purposes:


- The APIs validate events and check the data for consistency. This reduces errors and saves the team time to focus on important things
- The sinks compute ClickHouse table schemas, diff them with the status quo and modify the tables as needed
- We create a documentation about all events and what they mean from the protobuf file automatically.


Given the complexity of user interacting with a translator, compared to e.g. an e\-commerce website, ClickHouse allowed us to create complex events and queries that we need to understand how users are interacting with us. This is something that a tool like Google Analytics wouldn’t be able to perform. All of this while having full control over the data itself and keeping the user’s privacy in mind. This enabled us to give everyone at DeepL a complete view of what is happening on every platform and made it the goto system within DeepL.


With this taken care of, the team focused on adding more and more sources to ClickHouse. We added our native apps, Linguee, integrations into 3rd party systems etc..


For DeepL, this was way more than just the introduction of an analytics platform, but the shift towards a data\-driven development of many critical components: main translator page, registration funnel, behavior in the apps; the data collected is used to get insights for Product Managers how our product is used, lets Design discover opportunities, and find bugs that are painful for the user.


We expanded from a single node setup to a cluster of 3 shards with 3 replicas after 16 months of usage. Until then, a single node with a replica was simply enough and performing fine. Currently this setup ingests about half a billion raw rows per day.


Having built our data foundation, it was time to move on to build more things on this platform.


## Experimentation [\#](/blog/deepls-journey-with-clickhouse#experimentation)


Experimentation, also called AB\-testing, is the art of qualifying changes to a website by splitting the traffic into control (A) and test (B) groups and showing them different versions of the page. The architecture of this experimentation framework looks like this:


![DeepLArchitecture2.png](/uploads/Deep_L_Architecture2_bd4e7f3a03.png)
In this framework, ClickHouse takes the role of doing the heavy lifting for the statistical analysis. For every running experiment, ClickHouse goes though 100s of millions of rows to calculate averages, standard deviations, factors for outlier corrections, and so on. As ClickHouse is optimized for this, our Data Scientists had to do very little optimization on indices or data types and could focus on building the actual solution. Especially the array functions were incredibly helpful in building the statistical analysis as it took away the complicated bookkeeping when a user is exposed to many experiments. This allowed us to develop the framework within a couple of months and having the first experiments live. This enabled DeepL to rapidly iterate on frontend or algorithmic backend changes and contributed towards a cultural shift in these areas.


## ML\-Infrastructure of Personalization [\#](/blog/deepls-journey-with-clickhouse#ml-infrastructure-of-personalization)


Not everyone who uses DeepL needs all features and not everyone who uses DeepL knows about all features. To address this problem, we founded a team that personalizes the website. For example, we are hinting some users to certain features if we think they are useful for them. To be be able to do this, we need three things:


- A history of the user
- The capability to retrieve this history and train an ML model on it
- The capability to inference new users on the trained model and tailor the website according to the output


ClickHouse is well suited for this architecture. We aggregate the user’s history in ClickHouse and use it as a data store for training and inference. Even when reading 10s of millions of rows, the performance was very nice and not the bottleneck when training new models.


### The authors [\#](/blog/deepls-journey-with-clickhouse#the-authors)


[Jannik Hoffjann](https://www.linkedin.com/in/hfjn/): Engineering Lead Data Platform


[Till Westermann](https://www.linkedin.com/in/till-westermann-23ab3ba3/): Group Product Manager Data Platform

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
