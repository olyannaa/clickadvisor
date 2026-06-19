# November 2024 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# November 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 21, 2024 · 7 minutes readWelcome to the November ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.


The big news is that Refreshable Materialized Views are production\-ready, and we have an official Docker image!


Alexey Milovidov was a guest on Data Talks on the Rocks, we learn how to simplify queries with dictionaries, and there’s a deep dive on the new JSON data type.


 


## Inside this issue [\#](/blog/202411-newsletter#inside-this-issue)


- [Featured community member](https://clickhouse.com/blog/202411-newsletter#featured-community-member)
- [Upcoming events](https://clickhouse.com/blog/202411-newsletter#upcoming-events)
- [24\.10 Release](https://clickhouse.com/blog/202411-newsletter#2410-release)
- [Alexey Milovidov on Data Talks on the Rocks](https://clickhouse.com/blog/202411-newsletter#alexey-milovidov-on-data-talks-on-the-rocks)
- [Simplifying queries with ClickHouse dictionaries](https://clickhouse.com/blog/202411-newsletter#simplifying-queries-with-clickhouse-dictionaries)
- [Building a financial data pipeline with Alpha Vantage and ClickHouse](https://clickhouse.com/blog/202411-newsletter#building-a-financial-data-pipeline-with-alpha-vantage-and-clickhouse)
- [How we built a new powerful JSON data type for ClickHouse](https://clickhouse.com/blog/202411-newsletter#how-we-built-a-new-powerful-json-data-type-for-clickhouse)
- [ClickHouse Cloud Live Update: November 2024](https://clickhouse.com/blog/202411-newsletter#clickhouse-cloud-live-update-november-2024)
- [Quick reads](https://clickhouse.com/blog/202411-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202411-newsletter#post-of-the-month)


 


## Visit us at AWS re [\#](/blog/202411-newsletter#visit-us-at-aws-re)


![aws-reinvent-202411.png](/uploads/aws_reinvent_202411_0edd3daa88.png)
Are you heading to re:Invent? We are too, and would love to connect with you!


Book a meeting with us beforehand by emailing sales@clickhouse.com, or stop by our booth \#1737 for:


- A chance to meet all three of [our founders](https://clickhouse.com/company/our-story): Aaron, Alexey, and Yury
- Live demos
- Exclusive swag
- And a chat with ClickHouse experts


Don’t miss out – we’re also hosting a ClickHouse House Party with the Chainsmokers. It’ll be one epic night you won’t want to miss! 



![house-party-202411.png](/uploads/house_party_202411_ba778b3256.png)

[Register for the Chainsmokers party](https://clickhouse.com/houseparty/vegas-2024)



 


## Featured community member [\#](/blog/202411-newsletter#featured-community-member)


This month's featured community member is Lukas Biewald, co\-founder and CEO at [Weights \& Biases](https://wandb.ai?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter).


![featured-202411.png](/uploads/featured_202411_c82ec62b60.png)

Lukas has worked in machine learning for 20 years, previously co\-founding Figure Eight with Chris Van Pelt, where they specialized in data labeling for machine learning applications. Appen acquired the company in March 2019\. 



In 2018, Lukas co\-founded Weights \& Biases, an MLOps platform designed to assist machine learning practitioners in tracking experiments, managing datasets, and collaborating on model development.



Lukas [presented](https://clickhouse.com/videos/ai-developer-platform?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) at the ClickHouse San Francisco meetup in September, where he shared his experience building AI applications and how they use ClickHouse as part of their Weave application. This was also written up in [a blog published last week](https://clickhouse.com/blog/weights-and-biases-scale-ai-development?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter).


[Follow Lukas on LinkedIn](https://www.linkedin.com/in/lbiewald?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter)


 


## Upcoming events [\#](/blog/202411-newsletter#upcoming-events)


**Global events**


- [Release call 24\.11](https://clickhouse.com/company/events/v24-11-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Nov 28


**Free training**


- [Migrating from Postgres to ClickHouse Workshop](https://clickhouse.com/company/events/202411-emea-postgres-to-clickhouse-migration?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Virtual \- Nov 27
- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Virtual\- Dec 4
- [In\-Person ClickHouse Training in Sweden](https://clickhouse.com/company/events/202412-emea-stockholm-inperson-clickhousetraining?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Sweden\- Dec 9
- [In\-Person ClickHouse Training in Denmark](https://clickhouse.com/company/events/202412-emea-copenhagen-inperson-clickhousetraining?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Denmark \- Dec 9
- [ClickHouse Developer In\-Person Training in New York](https://clickhouse.com/company/events/202412-amer-manhattan-inperson-clickhouse-developer?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Manhattan, NY \- Dec 11\-12
- [ClickHouse Developer Training](https://clickhouse.com/company/events/202412-global-training-clickhouse-developer?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Virtual \- Dec 18\-19


**Events in AMER**


- [Microsoft Ignite](https://clickhouse.com/company/events/202411-amer-microsoft-ignite?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Chicago \- Nov 19\-22
- [AWS re:Invent 2024](https://clickhouse.com/company/events/202412-amer-reinvent-meetingrequests?utm_source=clickhouse&utm_medium=email&utm_campaign=202411-newsletter) \- Las Vegas \- Dec 2\-6
- [Meetup in New York](https://www.meetup.com/clickhouse-new-york-user-group/events/304268174) \- Dec 9
- [Meetup in San Francisco](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/304286951) \- Dec 12


**Events in EMEA**


- [Meetup in Dubai](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/) \- Nov 21
- [Meetup in Paris](https://www.meetup.com/clickhouse-france-user-group/events/303096434) \- Nov 26
- [Meetup in Amsterdam](https://www.meetup.com/clickhouse-netherlands-user-group/events/303638814/) \- Dec 3
- [Meetup in Stockholm](https://www.meetup.com/clickhouse-stockholm-user-group/events/304382411/) \- Dec 9


  

## 24\.10 release [\#](/blog/202411-newsletter#2410-release)


![release-24.10.png](/uploads/release_24_10_988ee5facb.png)
Refreshable Materialized Views are production\-ready! That’s the big news in the 24\.10 release, but we’ve also simplified table cloning with the CLONE AS clause, and there’s remote file caching, which is super helpful when querying S3 buckets.


[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-10)


 


## Alexey Milovidov on Data Talks on the Rocks [\#](/blog/202411-newsletter#alexey-milovidov-on-data-talks-on-the-rocks)


![alexey-data talks-202411.png](/uploads/alexey_data_talks_202411_ffc0bfdf7c.png)
Data Talks on the Rocks is a series of interviews with thought leaders and founders discussing the latest trends in data and analytics. Michael Driscoll, CEO and Co\-founder of Rill Data, hosts it.



In episode 4, his guest was none other than Alexey Milovidov, the CTO and Co\-founder of ClickHouse. In a wide\-ranging conversation, they discussed the importance of hashing functions in database design, how AI might impact database technologies in the future, the development of ClickHouse's new analyzer, and more.



[Watch the interview](https://www.rilldata.com/blog/rill-clickhouse-alexey-milovidov-interview)


 


## Simplifying queries with ClickHouse dictionaries [\#](/blog/202411-newsletter#simplifying-queries-with-clickhouse-dictionaries)


[Jeffrey Needles](https://www.linkedin.com/in/jeffreyneedles/), founder of Aggregations.io, has written a blog post explaining how to simplify queries using dictionaries.


Jeffrey takes us through why you’d want to use a dictionary, where data is sourced from, and how to choose the right type of key before demonstrating the performance gain from using them in a query.



[Read the blog post](https://aggregations.io/blog/clickhouse-dictionaries)


 


## Building a financial data pipeline with Alpha Vantage and ClickHouse [\#](/blog/202411-newsletter#building-a-financial-data-pipeline-with-alpha-vantage-and-clickhouse)


![correlation returns-202411.png](/uploads/correlation_returns_202411_b71341e433.png)
Craig Dickson builds a high\-performance data pipeline using Alpha Vantage for data acquisition and ClickHouse for data storage and analytics. 



After querying the Alpha Vantage API data, Craig cleans it up in Pandas before ingesting it into ClickHouse Cloud. He then shows how to create various data visualizations using Vega\-Altair.



[Read the blog post](https://medium.com/@thecraigdickson/building-a-financial-data-pipeline-with-alpha-vantage-and-clickhouse-5860d1e5a4be)


 


## How we built a new powerful JSON data type for ClickHouse [\#](/blog/202411-newsletter#how-we-built-a-new-powerful-json-data-type-for-clickhouse)


![json-data-type-202411.png](/uploads/json_data_type_202411_7b2068bbc1.png)
The new JSON data type was introduced in version 24\.8 in August, and we showed some examples [in the release post](https://clickhouse.com/blog/clickhouse-release-24-08) but didn’t explore it in depth.



That all changes with this blog post, where Tom Schreiber and Pavel Kruglov explain how it works under the hood. They explain how the new data type overcomes challenges like having values of multiple data types in the same JSON path, how to avoid pushing work to query time, and how to prevent an avalanche of column data files on disk. 



There are lots of diagrams explaining how it all works. One to read for ClickHouse enthusiasts!


[Read the blog post](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse)


 


## ClickHouse Cloud Live Update: November 2024 [\#](/blog/202411-newsletter#clickhouse-cloud-live-update-november-2024)


Krithika Balagurunathan and Zach Naimon joined us on our latest ClickHouse Cloud live update call. They taught us about [Bring Your Own Cloud](https://clickhouse.com/cloud/bring-your-own-cloud) and [Compute\-compute separation](https://clickhouse.com/docs/en/cloud/reference/compute-compute-separation), respectively. 



After giving an overview of the features and a brief demo, Zach and Krithika hosted a detailed Q\&A, which included the following questions:



Does BYOC meet FedRAMP requirements? Can horizontal autoscaling be automated based on resource consumption? How do you migrate an existing cluster to BYOC? Can you have powerful instances for read/write nodes and less powerful instances for read\-only nodes?



Check out the full recording below to hear the answers to these questions and more!



[Watch the recording](https://clickhouse.com/videos/clickhouse-cloud-live-november-2024-byoc-compute-compute-separation)


 


## Quick reads [\#](/blog/202411-newsletter#quick-reads)


- It's not really a quick read, but ClickHouse now has [an official Docker image](https://hub.docker.com/_/clickhouse)!
- Carl Lindesvärd posted [a Twitter thread about the things he’s learned from six months of working with ClickHouse](https://x.com/CarlLindesvard/status/1848706279293763917).
- Ravindra Elicherla [stores tick\-by\-tick Webscocket data in ClickHouse](https://ravindraelicherla.medium.com/storing-tick-by-tick-webscocket-data-into-clickhouse-f4bbd29d0d65).
- I came across [Trench](https://github.com/FrigadeHQ/trench), an event\-tracking system built on Apache Kafka and ClickHouse. It powers  [Frigade's](https://github.com/FrigadeHQ/trench) real\-time event\-tracking pipeline, handles large event volumes, and provides [real\-time analytics](https://clickhouse.com/engineering-resources/what-is-real-time-analytics)
- The MetricFire team explains [how to monitor ClickHouse with Telegraf and MetricFire](https://medium.com/@MetricFire/how-to-monitor-clickhouse-with-telegraf-and-metricfire-6b4aef886c49).
- Jesse Grodman, Software Engineer at [Triple Whale](https://www.triplewhale.com/), shares how to [move data from an unsharded ClickHouse cluster to a sharded one](https://medium.com/@jgrodman/migrating-clickhouse-data-without-adding-load-to-the-db-031d6a868b0e) without adding load to the existing cluster.


 


## Post of the month [\#](/blog/202411-newsletter#post-of-the-month)


Our favorite post this month was by [Steven Tey](https://x.com/steventey/status/1855669066817839116) about ClickHouse’s arrayIntersect function.


![tweet-202411.png](/uploads/tweet_202411_301f2111e1.png)

[Read the post](https://x.com/steventey/status/1855669066817839116)


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
