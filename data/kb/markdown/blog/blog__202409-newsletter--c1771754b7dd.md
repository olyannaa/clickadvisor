# September 2024 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# September 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Sep 19, 2024 · 6 minutes readWelcome to the September ClickHouse newsletter, which will round up what’s
happened in real\-time data warehouses over the last month. This month, we have
the much\-awaited JSON data type, our 1st ClickHouse research paper, a Private
Preview of BYOC on AWS, better PyPi stats with Ibis, and more!


 


## Inside this issue [\#](/blog/202409-newsletter#inside-this-issue)


- [Featured community member](https://clickhouse.com/blog/202409-newsletter#featured-community-member)
- [Upcoming events](https://clickhouse.com/blog/202409-newsletter#upcoming-events)
- [VLDB 2024: First ClickHouse research paper](https://clickhouse.com/blog/202409-newsletter#vldb-2024-first-clickhouse-research-paper)
- [How Reco leverages advanced analytics to detect sophisticated SaaS threats](https://clickhouse.com/blog/202409-newsletter#how-reco-leverages-advanced-analytics-to-detect-sophisticated-saas-threats)
- [24\.8 LTS release](https://clickhouse.com/blog/202409-newsletter#248-lts-release)
- [Better PyPI stats with Ibis, ClickHouse, and Shiny](https://clickhouse.com/blog/202409-newsletter#better-pypi-stats-with-ibis-clickhouse-and-shiny)
- [ClickHouse Cloud: BYOC AWS in Private Preview](https://clickhouse.com/blog/202409-newsletter#clickhouse-cloud-byoc-aws-in-private-preview)
- [Quick reads](https://clickhouse.com/blog/202409-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202409-newsletter#post-of-the-month)


 


## Featured community member [\#](/blog/202409-newsletter#featured-community-member)


![sep2024featuredmember.png](/uploads/sep2024featuredmember_eec8525999.png)

 beehiiv is a newsletter platform that helps creators, publishers, and
 businesses build and grow their email audiences. They collect events capturing
 every time an email is processed, every time it lands in an inbox, every time
 it’s deferred, every time it’s bounced, every time you open it, every time you
 click a link, and so on.




 Eric has worked at beehiv for just over a year and was responsible for moving data operations from Postgres to ClickHouse Cloud. There’s [a user story on the work he and his team did](https://clickhouse.com/blog/data-hive-the-story-of-beehiivs-journey-from-postgres-to-clickhouse?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter), and he also presented at the
 [New York meetup in the summer](https://clickhouse.com/videos/transistion-from-postgres-to-clickhouse?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter).




 Eric previously worked as a Tech Lead at Arthur.ai, where he architected and built the company's data ingestion pipeline, storage, and much of the backend infrastructure.




[Follow Eric on LinkedIn](https://www.linkedin.com/in/eric-abis-30a03a13?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## Upcoming events [\#](/blog/202409-newsletter#upcoming-events)


**Global events**


- [ClickHouse Cloud Live Update](https://clickhouse.com/company/events/202409-cloud-update-live?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter) \- Sep 24
- [24\.9 release community call](https://clickhouse.com/company/events/v24-9-community-release-call?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Sep 26


**Free training**


- [Query optimization with ClickHouse workshop](https://clickhouse.com/company/events/202409-amer-query-optimization?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Sep 25
- [In\-Person ClickHouse Workshop](https://clickhouse.com/company/events/202410-apj-singapore-inperson-training?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Singapore \- Oct 3


**Events in EMEA**


- [Meetup in Tel Aviv](https://www.meetup.com/clickhouse-meetup-israel/events/303095121)
 \- Sep 22
- [Meetup in Madrid](https://www.meetup.com/clickhouse-spain-user-group/events/303096564)
 \- Oct 22
- [Meetup in Barcelona](https://www.meetup.com/clickhouse-spain-user-group/events/303096876/?eventOrigin=network_page)
 \- Oct 29
- [Meetup in Oslo](https://www.meetup.com/open-source-real-time-data-warehouse-real-time-analytics/events/302938622/)
 \- Oct 31
- [Meetup in Ghent](https://www.meetup.com/clickhouse-belgium-user-group/events/303049405)
 \- Nov 19
- [Meetup in Dubai](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/)
 \- Nov 21
- [Meetup in Paris](https://www.meetup.com/clickhouse-france-user-group/events/303096434)
 \- Nov 26


**Events in Asia Pacific**


- [DataEngBytes \- Sydney](https://clickhouse.com/company/events/202409-dataengbytes-sydney?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Sep 24
- [DataEngBytes \- Perth](https://clickhouse.com/company/events/202409-dataengbytes-perth?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Sep 27
- [DataEngBytes \- Melbourne](https://clickhouse.com/company/events/202410-dataengbytes-melbourne?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Oct 1
- [DataEngBytes \- Auckland](https://clickhouse.com/company/events/202410-dataengbytes-auckland?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Oct 4
- [Big Data \& AI World Asia](https://www.bigdataworldasia.com/2024-conference-programme/how-open-source-is-re-shaping-the-cloud-data-warehouse-landscape?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Oct 10
- [Cloud Excellence Summit NSW](https://clickhouse.com/company/events/202410-cloudexcellence-summit-sydney?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Oct 17
- [Data \& AI Summit VIC](https://clickhouse.com/company/events/202410-dataai-summit-vic-melbourne?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 \- Oct 22


 


## VLDB 2024: First ClickHouse research paper [\#](/blog/202409-newsletter#vldb-2024-first-clickhouse-research-paper)


![vldbpaper.png](/uploads/vldbpaper_2172677f18.png)

 It’s been almost a year in the making, and at the end of August, we presented
 our first research paper at VLDB 2024\. 




 VLDB—the international conference on very large databases—is widely regarded
 as one of the leading conferences in data management. VLDB generally has an
 acceptance rate of \~20% among the hundreds of submissions.




 The paper concisely describes ClickHouse's most interesting architectural and
 system design components, which make it so fast. We’ve embedded the PDF of the
 paper in the blog post linked below.




[Read the blog post](https://clickhouse.com/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## How Reco leverages advanced analytics to detect sophisticated SaaS threats [\#](/blog/202409-newsletter#how-reco-leverages-advanced-analytics-to-detect-sophisticated-saas-threats)



 Reco is a full\-lifecycle SaaS security solution that uses ClickHouse as the
 foundation of its advanced analytics system. Nir Barak explains how ClickHouse
 gives them a holistic view of data across multiple layers and allows them to
 detect outliers and anomalies.




[Read the blog post](https://www.reco.ai/blog/how-reco-leverages-advanced-analytics-to-detect-sophisticated-saas-threats?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## 24\.8 LTS release [\#](/blog/202409-newsletter#248-lts-release)


![release24.8.png](/uploads/release24_8_346c30e897.png)

 The 24\.8 release is here, and it has an exciting feature that I (and many of
 you) have been waiting for \- the new JSON data type! 




 It’s in experimental mode, but that didn’t stop us from taking it through its
 paces while exploring structured data of events in football/soccer matches.




 This release also introduces the TimeSeries table engine, which can store
 Prometheus data, and a new Kafka table engine that supports exactly\-once event
 processing.




[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-08?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## Better PyPI stats with Ibis, ClickHouse, and Shiny [\#](/blog/202409-newsletter#better-pypi-stats-with-ibis-clickhouse-and-shiny)


![pypistats.png](/uploads/pypistats_67a959ca27.png)

[ClickPy](https://clickpy.clickhouse.com?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 is a ClickHouse\-backed application that analyzes the download of Python
 packages published on PyPI. In addition to the front\-end application, you can
 also query the underlying data, which is exactly what Cody Peterson has
 done. 




 Cody shows how to connect to ClickPy using
 [Ibis](https://clickhouse.com/blog/introduction-to-ibis?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 and then explores the seasonality of downloads of the clickhouse\-connect
 package by day of the week and month. The results are visualized using
 [plot.ly](http://plot.ly?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter), and Cody then puts everything together into a [Shiny](https://shiny.posit.co/py?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)
 application. 




[Read the blog post](https://ibis-project.org/posts/better-pypi-stats?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## ClickHouse Cloud: BYOC AWS in Private Preview [\#](/blog/202409-newsletter#clickhouse-cloud-byoc-aws-in-private-preview)


![byoc.png](/uploads/byoc_943e12d96d.png)

 ClickHouse Cloud has been
 [running for almost two years](https://clickhouse.com/blog/clickhouse-cloud-generally-available?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter) and supports all the major cloud platforms, AWS, Azure, and GCP. So far, it’s
 been a SaaS offering that runs entirely on ClickHouse’s cloud account, which
 made it a non\-starter for users with strict data residency and compliance
 requirements. 




 We’re therefore happy to announce the Private Preview release of Bring Your
 Own Cloud (BYOC) on AWS. BYOC is a fully managed ClickHouse Cloud service
 deployed to your AWS account.




 The waiting list is now open, so be sure to sign up, and we’ll contact you to
 set you up.




[Join the waitlist](https://clickhouse.com/cloud/bring-your-own-cloud?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter)



 


## Quick reads [\#](/blog/202409-newsletter#quick-reads)


- Heng Ma shows how to
 [build a system that enriches shopping cart events with product details](https://risingwave.com/blog/real-time-data-enrichment-and-analytics-with-risingwave-and-clickhouse?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter). Using Rising Wave, a Kafka event data stream is joined with a product
 catalog, and the enriched events are written to ClickHouse using the Rising
 Wave\-ClickHouse connector.
- Auxten released
 [a new version of chDB](https://clickhouse.com/blog/chdb-pandas-dataframes-87x-faster?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter), the in\-process embedded version of ClickHouse, that can query Pandas DataFrames 87 times faster than the initial version.
- I loved
 [this video](https://www.youtube.com/watch?v=_jjvaFWWKqg)
 from Jess Archer’s talk at Laracon US 2024\. It is an excellent introduction
 to ClickHouse and shows where it’s better than MySQL.
- Sai Srirampur
 [shares his tips for ClickHouse data modeling aimed at Postgres users](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips?utm_source=clickhouse&utm_medium=web&utm_campaign=202409-newsletter). He explains various strategies to handle duplicates when using the
 ReplacingMergeTree table engine, how to handle null values, and the
 importance of ordering keys


 


## Post of the month [\#](/blog/202409-newsletter#post-of-the-month)



 Our favorite post this month was by
 [Michael Driscoll](https://x.com/medriscoll) about
 the new JSON data type:



![tweet_1831900730254582115_20240919_134823_via_10015_io.png](/uploads/tweet_1831900730254582115_20240919_134823_via_10015_io_b20a8a502c.png)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
