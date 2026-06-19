# May 2024 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# May 2024 Newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 23, 2024 · 6 minutes readWelcome to the May ClickHouse newsletter, which will round up what’s been happening in real\-time data warehouses over the last month.


This month, we have recursive CTEs in the 24\.4 release, the launch of ClickHouse developer certification, real\-time fraud detection at Instacart, and more!


## Inside this issue [\#](/blog/newsletter-may-2024#inside-this-issue)


- [Featured community member](/blog/newsletter-may-2024#featured-community-member)
- [Upcoming events](/blog/newsletter-may-2024#upcoming-events)
- [24\.4 release](/blog/newsletter-may-2024#244-release)
- [Become a ClickHouse Certified Developer](/blog/newsletter-may-2024#become-a-clickhouse-certified-developer)
- [Real\-time Fraud Detection at Instacart](/blog/newsletter-may-2024#real-time-fraud-detection-at-instacart)
- [K\-Means Clustering with ClickHouse](/blog/newsletter-may-2024#k-means-clustering-with-clickhouse)
- [Simplified Kubernetes Logging with Fluentbit and ClickHouse](/blog/newsletter-may-2024#simplified-kubernetes-logging-with-fluentbit-and-clickhouse)
- [The New Building Blocks of Observability](/blog/newsletter-may-2024#the-new-building-blocks-of-observability)
- [Using ClickHouse for Financial Charts](/blog/newsletter-may-2024#using-clickhouse-for-financial-charts)
- [Post of the Month](/blog/newsletter-may-2024#post-of-the-month)


## Featured community member [\#](/blog/newsletter-may-2024#featured-community-member)


This month's featured community member is Dan Goodman, Co\-Founder and CEO of Tangia, a service for hosting interactive live streams.


![featured-member-may2024.png](/uploads/featured_member_may2024_7babf3516a.png)
Dan has been part of the ClickHouse community for at least 18 months and frequently gives the engineering team feedback on both missing features and how existing features can be improved.


Dan writes a blog about distributed systems, where he’s previously written about topics like range partitioning and building a Fly.io scheduler.


A few weeks ago he wrote a blog post titled [Finding Trends With Approximate Embedding Clustering](https://www.aspiring.dev/instant-embeddings-clustering-with-k-means-and-clickhouse?utm_source=clickhouse&utm_medium=web&utm_campaign=202405-newsletter). In the post, he explains the importance of approximation techniques when working with big datasets and walks through how to implement the Dynamic K\-Means\+\+ algorithm with ClickHouse.


[Follow Dan on LinkedIn](https://www.linkedin.com/in/daniel-goodman-7a813214a/)


 


## Upcoming events [\#](/blog/newsletter-may-2024#upcoming-events)


- [Dubai Meetup](https://www.meetup.com/clickhouse-dubai-meetup-group/events/299629189/) \- May 28th
- [AWS Summit Dubai](/company/events/2024-05-aws-summit-dubai?loc=newsletter-april2024) \- May 29th
- [v24\.5 Community Call](/company/events/v24-5-community-release-call?loc=newsletter-april2024) \- May 30th
- [San Francisco Meetup](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/300523061/) \- June 4th
- [AWS Summit Stockholm](/company/events/2024-06-aws-summit-stockholm?loc=newsletter-april2024) \- June 4th
- [Tokyo Meetup](https://www.meetup.com/clickhouse-tokyo-user-group/events/300798053/) \- June 5th
- [AWS Summit Madrid](/company/events/2024-06-aws-summit-madrid?loc=newsletter-april2024) \- June 5th
- [ClickHouse Fundamentals](/company/events/clickhouse-fundamentals?loc=newsletter-april2024) \- June 26th \& 27th
- [AWS Summit D.C.](/company/events/2024-06-aws-summit-dc?loc=newsletter-april2024) \- June 26th
- [Amsterdam Meetup](https://www.meetup.com/clickhouse-netherlands-user-group/events/300781068/) \- June 27th
- [Paris Meetup](https://www.meetup.com/clickhouse-france-user-group/events/300783448/) \- July 9th
- [New York Meetup](https://www.meetup.com/clickhouse-new-york-user-group/events/300595845/) \- July 9th


 


## 24\.4 release [\#](/blog/newsletter-may-2024#244-release)


![24.4-release.png](/uploads/24_4_release_2b721e4021.png)
The standout feature in the 24\.4 release is recursive CTEs (Common Table Expressions), and we made a London Underground\-themed example to show you how they work. This release also sees improvements to JOIN performance and the QUALIFY clause to filter the values of window functions.


[Read the release post](/blog/clickhouse-release-24-04?loc=newsletter-april2024)


 


## Become a ClickHouse Certified Developer [\#](/blog/newsletter-may-2024#become-a-clickhouse-certified-developer)


![certified-developer.png](/uploads/certified_developer_c745754b9a.png)
Rich Raposa [recently announced](/blog/first-official-clickhouse-certification?loc=newsletter-april2024) the launch of the official ClickHouse Developer Certification Program, the only certification directly from ClickHouse.


This certification program validates developers’ proficiency in using ClickHouse to build robust, high\-performance data solutions. This certification will showcase your mastery of ClickHouse and help you distinguish yourself as a trusted database management and analytics expert.


[Learn more about certification](/learn/certification?loc=newsletter-april2024)


 


## Real\-time Fraud Detection at Instacart [\#](/blog/newsletter-may-2024#real-time-fraud-detection-at-instacart)


![instacart.png](/uploads/instacart_73a07488a3.png)
Nick Shieh, Shen Zhu, and Xiaobing Xia have written a blog post where they walk us through Yoda, a decision platform service they built at Instacart to detect fraudulent activities and take action quickly. ClickHouse was chosen as the primary real\-time datastore for this system because it can both ingest and query large amounts of data in real time. I especially liked the part of the post where they describe how real\-time features fed into the service are derived from ClickHouse SQL queries.


[Read the blog post](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4?utm_source=clickhouse&utm_medium=web&utm_campaign=202405-newsletter)


 


## K\-Means Clustering with ClickHouse [\#](/blog/newsletter-may-2024#k-means-clustering-with-clickhouse)


![K-means clustering.png](/uploads/K_means_clustering_392356d0bb.png)
Recently, when helping a user who wanted to compute centroids from vectors held in ClickHouse, we realized that the same solution could be used to implement K\-Means clustering. They wanted to do this at scale across potentially billions of data points while ensuring memory could be tightly managed. In this post, we show how to implement K\-means clustering using just SQL and show that it can scale to billions of records while running significantly faster than the same code in scikit\-learn.


[Read the blog post](/blog/kmeans-clustering-with-clickhouse?loc=newsletter-april2024)


 


## Simplified Kubernetes Logging with Fluentbit and ClickHouse [\#](/blog/newsletter-may-2024#simplified-kubernetes-logging-with-fluentbit-and-clickhouse)


Logging is one of the hot ClickHouse use cases of the moment, so I was excited to come across this blog post by Muthukumaran. Fluentbit is a lightweight logging and metrics processor and forwarder designed for containerized environments. Muthukumaran walks us through the steps to setup a metrics server to monitor resource utilization in Kubernetes and then shows how to configure Fluentbit to get those metrics into ClickHouse.


[Read the blog post](https://blog.devops.dev/simplified-kubernetes-logging-with-fluentd-and-clickhouse-9c620ec2dfa9?utm_source=clickhouse&utm_medium=web&utm_campaign=202405-newsletter)


 


## The New Building Blocks of Observability [\#](/blog/newsletter-may-2024#the-new-building-blocks-of-observability)


![obs-building-blocks-3.png](/uploads/obs_building_blocks_3_c64383af8e.png)
This article focuses on what the author coins the three new elements in the observability period table: OpenTelemetry, eBPF, and ClickHouse. OpenTelemetry has emerged as the de facto standard for telemetry data, eBPF makes it possible to generate traces and metrics with zero instrumentation, and ClickHouse is used to ingest and query all this data. The article also covers a series of Observability startups that are using ClickHouse \- Groundcover, SigNoz, and DeepFlow.


[Read the blog post](https://observability-360.com/article/ViewArticle?id=observability-building-blocks&utm_source=clickhouse&utm_medium=email&utm_campaign=202405-newsletter)


## Using ClickHouse for Financial Charts [\#](/blog/newsletter-may-2024#using-clickhouse-for-financial-charts)


![SCR-20240521-odub.jpeg](/uploads/SCR_20240521_odub_7bf15ea035.jpeg)
After giving a brief crash course into when (and when not) to use ClickHouse, Adis Nezirović demonstrates how to ingest, query, and visualize financial time\-series data. Along the way, he shows how to use the Null table engine to massage data and aggregate states to reduce the amount of data kept around. To conclude, Adis creates a candlestick chart using the Grafana QueryBuilder.


[Read the blog post](https://medium.com/mop-developers/using-clickhouse-for-charts-profits-ad6dc56abf67)


## Post of the Month [\#](/blog/newsletter-may-2024#post-of-the-month)


Our favorite post this month was by [ludwig](https://twitter.com/ludwigABAP) who was impressed by both the speed of ClickHouse queries and the quality of its data compression.


![tweet-1788330168999624920 (1).png](/uploads/tweet_1788330168999624920_1_22d9878e33.png)
After giving a brief crash course into when (and when not) to use ClickHouse, Adis Nezirović demonstrates how to ingest, query, and visualize financial time\-series data. Along the way, he shows how to use the Null table engine to massage data and aggregate states to reduce the amount of data kept around. To conclude, Adis creates a candlestick chart using the Grafana QueryBuilder.


[View the post](https://twitter.com/ludwigABAP/status/1788330168999624920)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
