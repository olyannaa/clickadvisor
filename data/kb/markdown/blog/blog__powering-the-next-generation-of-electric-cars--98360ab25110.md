# Powering the next generation of electric cars: NOVO Energy


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Powering the next generation of electric cars: NOVO Energy

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 8, 2024 · 8 minutes read*In this interview, we had the pleasure of sitting down with [NOVO Energy](https://www.novoenergy.se/) to delve into their experience with ClickHouse and ClickHouse Cloud on AWS. We discussed the challenges they faced before discovering ClickHouse, the impact it has had on their data analytics, and how it has transformed the way their team operates. Their insights offer a firsthand look at how ClickHouse's speed, scalability, and flexibility drive innovation and efficiency in their organization. Enjoy this deep dive into their journey with ClickHouse, and perhaps find inspiration for your own data challenges.*


![NOVOEnergy_quote2.png](/uploads/NOVO_Energy_quote2_b002f9fcc9.png)
## Do you mind introducing yourself? [\#](/blog/powering-the-next-generation-of-electric-cars#do-you-mind-introducing-yourself)


My name is Martin Hardselius and I've been a software engineer for a little more than 12 years. During my career, I've worked in several different companies and industries, including online identity, gambling, telco, consumer electronics, big companies, small startups, etc. I started out as a backend engineer, expanded into infrastructure and site reliability, and now I find myself in the domain of battery research and industrial IoT, which could be viewed as a souped\-up version of home automation, doing work across the entire stack.


I joined NOVO Energy on May 2nd, 2022, as one the very first employees. That is kind of funny considering the only person who knew anything about making batteries in the company at that time was our CTO, Eerik Hantsoo. But he had a vision of how a robust data platform would play a central role in enabling good research, which is why he brought me on before anyone who actually knew anything about batteries. Now, more than two years in, my knowledge of the domain has grown, and I have the privilege of working with some very smart people, solving interesting problems using exciting technology.


![NovoEnergy_image.png](/uploads/Novo_Energy_image_acda265b5b.png)
## What is the origin story of the company or the team within the company? What problem are you solving? [\#](/blog/powering-the-next-generation-of-electric-cars#what-is-the-origin-story-of-the-company-or-the-team-within-the-company-what-problem-are-you-solving)


NOVO Energy is a joint venture between Northvolt and Volvo Cars. Our mission is to develop and produce sustainable batteries, tailored to power the next generation of pure electric Volvo cars. In our R\&D facility, we collect large amounts of data from equipment, research instruments, and assembly machinery. This data feeds into the analysis of the cells we produce.


## What is most important when you tell your, or your team, story? [\#](/blog/powering-the-next-generation-of-electric-cars#what-is-most-important-when-you-tell-your-or-your-team-story)



> The purpose of the software engineering team within NOVO Energy R\&D is to internally democratize access to research data.


The data we collect typically ends up in whatever storage our vendors have picked to back their software. We're writing software that copies that data into our own database, where we are then free to query and analyze using tools that are available to everyone in our organization. We centralize our data so that we can streamline our tooling. We standardize our data to reduce the risk of errors in our calculations. We democratize access to our data to remove unnecessary gatekeeping. We generalize our representations so that data can be compared across different experiments, regardless of which test equipment was used.


## What requirements did you have for the database/store component(s) in your architecture? [\#](/blog/powering-the-next-generation-of-electric-cars#what-requirements-did-you-have-for-the-databasestore-components-in-your-architecture)



> Our primary business requirement for any database/store was that we own and control the data we store \-\- no vendor lock\-in and no walled gardens.


Luckily, that's not the most demanding requirement to fulfill. Regarding performance, we were looking for a solution that allowed us to query for a few million rows out of a dataset of billions of rows in a reasonable time without spending too much time tuning it. Additionally, we wanted a low\-maintenance or managed solution where basic hygiene like backups was part of the package, that's easy to integrate with other tools, such as Grafana or BI solutions, a familiar query language, and good language support for at least Rust and Python.


## Tell us about your discovery of ClickHouse. How did you hear about it, and what made you excited to give it a try? What were your hesitations? [\#](/blog/powering-the-next-generation-of-electric-cars#tell-us-about-your-discovery-of-clickhouse-how-did-you-hear-about-it-and-what-made-you-excited-to-give-it-a-try-what-were-your-hesitations)


We stumbled upon ClickHouse's booth at AWS Summit Stockholm in 2023\. One of the team members had seen the name before on Hacker News so we decided to approach. After a brief discussion with the two gentlemen at the booth, we realized that ClickHouse was highly relevant to our use case.


## How did you evaluate Clickhouse? How did ClickHouse perform against the alternatives considered? [\#](/blog/powering-the-next-generation-of-electric-cars#how-did-you-evaluate-clickhouse-how-did-clickhouse-perform-against-the-alternatives-considered)


Our first evaluation of ClickHouse consisted of taking it on a spin on one of our laptops, seeding it with our current data and then playing around with queries. Already at this stage, we were happy with the performance of ClickHouse because we were seeing 10\-100x performance gains at this stage. From there on we decided to try out ClickHouse Cloud free tier and after further evaluation we quickly upgraded to a paid tier.


## What alternative databases did you consider? [\#](/blog/powering-the-next-generation-of-electric-cars#what-alternative-databases-did-you-consider)


Prior to ClickHouse we were using an on\-premise installation of TimescaleDB, which served us well, but we had not spent any time on right\-sizing the hardware or tuning the database. When considering alternatives to that, we were mainly looking at managed offerings that would fit our architecture. Using AWS RDS to back our analytical queries was not something we wanted to do and we also considered a solution involving AWS S3, AWS Glue and Amazon Redshift, but we felt that it was a bit over engineered for our scale of operation.


## What were the considerations when weighing the use of cloud vs self\-managed ClickHouse? [\#](/blog/powering-the-next-generation-of-electric-cars#what-were-the-considerations-when-weighing-the-use-of-cloud-vs-self-managed-clickhouse)


![NOVOEnergy_quote.png](/uploads/NOVO_Energy_quote_709b8174a3.png)
As previously stated, and since we're a small team with limited time, we were looking for a low\-maintenance or managed solution. Going with ClickHouse Cloud on AWS was an easy decision because it allows us to focus on our primary work without having to worry about maintenance, upgrades, backups, and so on.


## Can you share some quantitative metrics about ClickHouse's performance (e.g., ingest/query latency/overall data volumes/cost efficiency)? [\#](/blog/powering-the-next-generation-of-electric-cars#can-you-share-some-quantitative-metrics-about-clickhouses-performance-eg-ingestquery-latencyoverall-data-volumescost-efficiency)


At the time of writing, we're sitting on just above 400M rows of electrochemical test data. We don't think this is a lot considering we're still in a ramp\-up phase. As we commission new test equipment and push our tester utilization rate up, this number will greatly grow. When we're fully ramped up we might have around 1300 battery cells on test at any given time. The equipment will likely generate new data at roughly 0\.1 Hz. With some auxiliary sensors, sampled at the same frequency, associated with a good portion of the battery cells we're probably looking at around 2000 new records to be inserted every 10 seconds. On top of that, we'll be gathering telemetry data from our process equipment and the BMS (Building Management System). That may be another 200 records at 0\.1 Hz. We're batching our inserts to happen about once per minute, so now we're looking at 12\-13K records per minute. That's not a lot of data, but insert performance was never our highest priority when picking a database. What's more critical is query performance. For every test we're processing, we constantly check the latest record we've already processed. This will tell us when to request new data from our battery cyclers. This query looks something like this



```
SELECT channel, test_id, max(sequence_number), max(observed_at) 
FROM cycler_data GROUP BY channel, test_id

```

With a growing number of tests and every test potentially having months' worth of data, the performance of this query becomes increasingly important. At the moment, this query takes about 0\.1 seconds with just over 4400 (and 4M rows) tests in the database. Without the projection, it takes more than 17 seconds.


## Looking forward, what's next for you (and your use of ClickHouse)? [\#](/blog/powering-the-next-generation-of-electric-cars#looking-forward-whats-next-for-you-and-your-use-of-clickhouse)


At this stage, we have most of the plumbing for our data pipelines in place. We are experimenting with post\-processing pipelines, where we push aggregate results from ClickHouse to either separate ClickHouse tables or PostgreSQL. Of course, we will continue to monitor our system's performance. As the number of tests and test records grows over time, we will likely need to optimize different aspects of our setup.



> Also worth noting is that we're using ClickHouse to store logs from our services.


The amount of data is negligible compared to the lab telemetry we're gathering, but that might grow if we decide to ingest logs from various equipment and machines too. We're using a setup heavily inspired by ([Uber)](https://www.uber.com/en-SE/blog/logging/) and it has served us well as a replacement for CloudWatch. Log analytics is something we haven't explored much, but could potentially be attractive for monitoring our operations.


## How would you describe ClickHouse in 3 words? [\#](/blog/powering-the-next-generation-of-electric-cars#how-would-you-describe-clickhouse-in-3-words)


Simple, pleasant, performant.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
