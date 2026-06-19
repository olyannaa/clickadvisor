# April 2024 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# April 2024 Newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 17, 2024 · 5 minutes readWelcome to the April ClickHouse newsletter where we round up what’s been
happening in real\-time data warehouses over the last month.


This month, we have the 24\.3 release, building a rate limiter, a migration
from MySQL to ClickHouse story, meetup videos, and more!


## Inside this issue [\#](/blog/newsletter-april-2024#inside-this-issue)


- [Featured community member](/blog/newsletter-april-2024#featured-community-member)
- [Upcoming events](/blog/newsletter-april-2024#upcoming-events)
- [24\.3 release](/blog/newsletter-april-2024#243-release)
- [Storing Continuous Profiling Data in ClickHouse](/blog/newsletter-april-2024#storing-continuous-profiling-data-in-clickhouse)
- [Migrating to ClickHouse: Releem's Journey](/blog/newsletter-april-2024#migrating-to-clickhouse-releems-journey)
- [How we Built a 19 PiB Logging Platform with ClickHouse and Saved Millions](/blog/newsletter-april-2024#how-we-built-a-19-pib-logging-platform-with-clickhouse-and-saved-millions)
- [Building a Rate Limiter with ClickHouse](/blog/newsletter-april-2024#building-a-rate-limiter-with-clickhouse)
- [Video Corner](/blog/newsletter-april-2024#video-corner)
- [ClickHouse Cloud Updates](/blog/newsletter-april-2024#clickhouse-cloud-updates)
- [Post of the month](/blog/newsletter-april-2024#post-of-the-month)


## Featured community member [\#](/blog/newsletter-april-2024#featured-community-member)


This month's featured community member is Shivji kumar Jha, a Staff Engineer
for Data Platforms at Nutanix.


![april2024-featuredmember.png](/uploads/april2024_featuredmember_4356cb31d7.png)
Shiv leads a five\-member team, managing and supporting Nutanix's data
platform, which acts as a service for messaging, streaming, event sourcing,
analytics, and time series databases. Shiv actively engages with the
communities of the technologies used at Nutanix, including ClickHouse.


We recently hosted a ClickHouse meetup in Nutanix’s office in Bangalore,
India. Shiv was invaluable in making this event happen, helping organize it,
and acting as an MC for the evening. He recorded all the talks and
[uploaded them](https://www.youtube.com/playlist?list=PLA7KYGkuAD06bXmVPWe6ohM618pVKUZfg) to YouTube afterward. Shiv also participated in [a follow\-up Q\&A session on 15th April](https://clickhouse.com/company/events/2024-05-15-live-q-and-a?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter) to address unanswered questions from the meetup.


Thanks for all your work Shiv and we’ll see you at the next meetup!


[Follow Shivji on LinkedIn](https://www.linkedin.com/in/shivjijha/)


 


## Upcoming events [\#](/blog/newsletter-april-2024#upcoming-events)


- [Copenhagen Meetup](https://www.meetup.com/clickhouse-denmark-meetup-group/events/299629133/) \- April 23rd
- [FREE ClickHouse Training](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter) \- April 24th \& 25th
- [AWS Summit London](https://clickhouse.com/company/events/2024-04-aws-summit-london?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter) \- April 24th
- [v24\.4 ClickHouse Community Call](https://clickhouse.com/company/events/v24-4-community-release-call?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter) \- April 30th
- [Bengaluru Meetup](https://www.meetup.com/clickhouse-bangalore-user-group/events/300405581/)
 \- May 4th
- [AWS Summit Berlin](https://clickhouse.com/company/events/2024-05-aws-summit-berlin?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)
 \- May 15th
- [Stockholm Meetup](https://www.meetup.com/clickhouse-stockholm-user-group/events/299752651/) \- May 22nd
- [Dubai Meetup](https://www.meetup.com/clickhouse-dubai-meetup-group/events/299629189/)
 \- May 28th


 


## 24\.3 release [\#](/blog/newsletter-april-2024#243-release)


![Release blog cover (2).png](/uploads/Release_blog_cover_2_0aff4edfa7.png)
The big feature in the 24\.3 release is the analyzer being enabled by default.
Analyzer is a new query analysis and optimization infrastructure that’s been
in the works for a couple of years and lets you have multiple
ARRAY JOIN clauses in
a query, treats tuple elements like columns, handles queries with nested CTEs
and sub\-queries, and more.


[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-03?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)


 


## Storing Continuous Profiling Data in ClickHouse [\#](/blog/newsletter-april-2024#storing-continuous-profiling-data-in-clickhouse)


![2024-04-15_14-02-36.png](/uploads/2024_04_15_14_02_36_0c5c8f21bf.png)
Coroot is an open\-source tool for observability that turns observability data
into actionable insights. Nikolay Sivko wrote a blog post in which he
describes how they built their own storage system for profiling data based on
ClickHouse. After defining continuous profiling, Nikolay takes us through the
data model and gives examples of queries that check on the performance of a
service.


[Read the blog post](https://coroot.com/blog/storing-continuous-profiling-data-in-clickHouse?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)


 


## Migrating to ClickHouse: Releem's Journey [\#](/blog/newsletter-april-2024#migrating-to-clickhouse-releems-journey)


Releem is a MySQL performance tuning tool that automatically detects
performance degradation and optimizes configuration files. To do this, they
collect metrics from hundreds of database servers across various operating
systems and cloud solutions.


They used to store these metrics in MySQL, which started to struggle once it
reached almost 5 billion records. Enter ClickHouse, which helped shrink the
database size by 20 times, cut aggregation query times from 45 to 2 minutes,
and reduced the page load time of the Releem dashboard by 25%.


[Read the blog post](https://releem.com/blog/migrating-to-clickhouse?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)


 


## How we Built a 19 PiB Logging Platform with ClickHouse and Saved Millions [\#](/blog/newsletter-april-2024#how-we-built-a-19-pib-logging-platform-with-clickhouse-and-saved-millions)


![logging_thumbnail.png](/uploads/logging_thumbnail_f5cabe3803.png)
[Rory Crispin](https://www.linkedin.com/in/rory-crispin/), SRE at ClickHouse, shared his experience building a platform for the logging data generated by ClickHouse Cloud. Rory takes us through key design decisions, including whether to use Kafka and structured vs unstructured logging. He also explains why the team decided to use OpenTelemetry to collect metrics and does a cost comparison of the in\-house solution vs using an off\-the\-shelf product like Datadog. 


[Read the blog post](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)


 


## Building a Rate Limiter with ClickHouse [\#](/blog/newsletter-april-2024#building-a-rate-limiter-with-clickhouse)


![2024-04-15_13-55-49.png](/uploads/2024_04_15_13_55_49_cc7d77b5b5.png)
If you were going to build a rate limiter, the obvious choice for storing the
data would be Redis. But Brad Lhotsky, Systems and Security Administrator at
Craigslist, was curious whether ClickHouse would be fit\-for\-purpose and used
it to build a proof\-of\-concept. Brad shared the slides of a talk explaining
how he imported data from Kafka, built a bridge from the ACL API to
ClickHouse, and tested high availability, all in just one week.


[View the slide deck](https://speakerdeck.com/reyjrar/breaking-the-rules-rate-limiting-with-clickhouse?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)


 


## Video corner [\#](/blog/newsletter-april-2024#video-corner)


- At the New York City meetup, Adam Azzam presented how Prefect
 [uses ClickHouse to enable real\-time event drive orchestration](https://www.youtube.com/watch?v=OKxCrcSWT1g).
- Mark Needham walked us through some of the most common
 [aggregate function combinators](https://www.youtube.com/watch?v=7ApwD0cfAFI)
 and showed how and why we might use them.
- At Kubecon Europe 2024, Manish Gill discussed
 [the challenges of auto\-scaling databases in Kubernetes](https://www.youtube.com/watch?v=AFoMsLMZKik), using ClickHouse Cloud as a case study.


 


## ClickHouse Cloud Updates [\#](/blog/newsletter-april-2024#clickhouse-cloud-updates)


![Cloud Monthly Update Highlights (1).png](/uploads/Cloud_Monthly_Update_Highlights_1_3aa0dcc0fa.png)
- Over the last 9 months, we’ve been rebuilding the UI for ClickHouse Cloud
 and
 [last week, started rolling it out to everybody](https://clickhouse.com/blog/new-clickhouse-cloud-experience?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter).
- Today,
 [ClickPipes](https://clickhouse.com/cloud/clickpipes?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter)
 introduces beta support for continuous data ingestion from S3 and GCS. Let
 us know if you’re interested in giving this a try by replying to this email!
- Tokyo (ap\-northeast\-1\) has been added as a new region for AWS. 
 [Sign up now](https://clickhouse.cloud/signUp?utm_source=clickhouse&utm_medium=website&utm_campaign=202404-newsletter).


 


## Post of the month [\#](/blog/newsletter-april-2024#post-of-the-month)


Our favorite post this month was by
[Divyendu Singh](https://twitter.com/divyenduz) about real\-time
monitoring.


![tweet-1775832353572544681 (1).png](/uploads/tweet_1775832353572544681_1_2db9cd6f7b.png)
[See it here](https://twitter.com/divyenduz/status/1775832353572544681)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
