# First ClickHouse research paper: How do you make a modern data analytics database lightning\-fast?


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# First ClickHouse research paper: How do you make a modern data analytics database lightning\-fast?

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Sep 4, 2024 · 6 minutes readWe're thrilled to announce that [the first ClickHouse research paper](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) was accepted and is now [published](https://www.vldb.org/pvldb/volumes/17/#issue-12) at VLDB.


[VLDB](https://en.wikipedia.org/wiki/International_Conference_on_Very_Large_Data_Bases)—the international conference on very large databases—is widely regarded as one of the leading conferences in the field of data management. Among the hundreds of submissions, VLDB generally has an acceptance rate of [\~20%](https://www.openresearch.org/wiki/VLDB).


This year, [VLDB 2024](https://vldb.org/2024/), held in Guangzhou, China, marked the [50th anniversary](https://vldb.org/2024/?program-schedule-panel#:~:text=This%20year's%20conference%20in%20Guangzhou,main%20speaker%20of%20this%20session.) of the conference, making it one of the longest\-running data management conferences.


![VLDB 2024 Research paper.002.png](/uploads/VLDB_2024_Research_paper_002_f28b58cc9b.png)
The conference [featured](https://vldb.org/2024/?program-schedule#A1) 250 paper presentations and 10 accompanying workshops on the latest research and industry trends.


This year’s dominant topic was machine learning in all shapes and forms but also lots of papers in core database areas like query engines, storage, and database theory appeared.


![VLDB 2024 Research paper.003.png](/uploads/VLDB_2024_Research_paper_003_a4e9becc47.png)
## A sneak peek into the ClickHouse paper [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#a-sneak-peek-into-the-clickhouse-paper)


Our publication is the culmination of a months\-long, cross\-functional effort to offer readers a concise description of ClickHouse's most interesting architectural and system design components that make it so fast. And now, for the very first time, it's [available](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf).


In the paper, you'll learn about:


### The history of ClickHouse [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#the-history-of-clickhouse)


When were major features described in this paper introduced to ClickHouse, and what features and enhancements are planned for the future?


![VLDB 2024 Research paper.004.png](/uploads/VLDB_2024_Research_paper_004_77999892f5.png)
### The architecture of ClickHouse [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#the-architecture-of-clickhouse)


Layers, components, and execution modes.


![VLDB 2024 Research paper.005.png](/uploads/VLDB_2024_Research_paper_005_08d9ef44fd.png)
### The storage layer of ClickHouse [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#the-storage-layer-of-clickhouse)


On\-disk format, data pruning techniques, merge\-time data transformations, updates and deletes, idempotent inserts, data replication, and ACID compliance.


![VLDB 2024 Research paper.006.png](/uploads/VLDB_2024_Research_paper_006_5b76bb212d.png)
### The query processing layer of ClickHouse [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#the-query-processing-layer-of-clickhouse)


SIMD parallelization, multi\-core parallelization, multi\-node parallelization, and performance optimization techniques.


![VLDB 2024 Research paper.007.png](/uploads/VLDB_2024_Research_paper_007_eb23af8ea6.png)
### The integration layer of ClickHouse [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#the-integration-layer-of-clickhouse)


Native support for 90\+ file formats and 50\+ integrations with external systems.


![VLDB 2024 Research paper.008.png](/uploads/VLDB_2024_Research_paper_008_0fce478e7d.png)
### Benchmarks [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#benchmarks)


Performance comparison of ClickHouse with other databases frequently used for analytics. Note: lower is better.


![VLDB 2024 Research paper.009.png](/uploads/VLDB_2024_Research_paper_009_513bd42024.png)

We hope this whetted your appetite. If you're interested, you can read the whole paper right here right now (you can scroll through the pages):




@media screen and (max\-width: 600px) {
 iframe.embedded\_pdf, p.embedded\_pdf {
 display: none;
 }
}


  

  

## ClickHouse at VLDB 2024 [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#clickhouse-at-vldb-2024)


### Paper presentation [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#paper-presentation)


![VLDB 2024 Research paper.010.png](/uploads/VLDB_2024_Research_paper_010_7548beb974.png)
Alexey Milovidov, our CTO and the creator of ClickHouse, presented the paper last week in Guangzhou (slides [here](https://github.com/ClickHouse/clickhouse-presentations/blob/325fef8adb9db1c19a29af89436e2cb1fa2913db/2024-vldb/VLDB_2024_presentation.pdf)), followed by a Q\&A (that quickly ran out of time!). You can catch the recorded presentation here:



  

  

### Poster presentation [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#poster-presentation)


In addition to the paper presentation, authors of accepted VLDB papers were asked to give a [poster](https://github.com/ClickHouse/clickhouse-presentations/blob/325fef8adb9db1c19a29af89436e2cb1fa2913db/2024-vldb/VLDB_2024_presentation.pdf) presentation.


![VLDB 2024 Research paper.011.png](/uploads/VLDB_2024_Research_paper_011_0ec6a958d4.png)
![VLDB 2024 Research paper - poster.001.png](/uploads/VLDB_2024_Research_paper_poster_001_6f0309c003.png)
  

  

### Bonus meetup talk [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#bonus-meetup-talk)


And as luck has it, we also hosted a [ClickHouse Guangzhou User Group Meetup](https://mp.weixin.qq.com/s/GSvo-7xUoVzCsuUvlLTpCw) just a few days before VLDB. At that meetup, we presented an extended version (slides [here](https://presentations.clickhouse.com/?path=2024-meetup-guangzhou)) of Alexey’s conference talk:



  

  

## From coast to coast–the journey of our first research paper [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#from-coast-to-coastthe-journey-of-our-first-research-paper)


We conclude with a bonus section for readers curious about the backstory of our first research paper.


After ClickHouse became open source in 2016, its popularity grew while the pace of development accelerated as well. The ClickHouse team has been so focused on building the world’s fastest analytics database in the past eight years that there hasn't been time to publish an academic paper on ClickHouse.


![VLDB 2024 Research paper.012.png](/uploads/VLDB_2024_Research_paper_012_d25461d4b9.png)
However, during a ClickHouse company offsite meeting at the stunning Mediterranean coastline of the French Riviera in October 2023, Tanya Bragin, our VP of Product and Marketing at ClickHouse, raised the idea of finally writing a foundational paper on ClickHouse and submitting it to VLDB taking place this year in Guangzhou, China, in the Guangdong province on the north shore of the South China Sea.


![VLDB 2024 Research paper.013.png](/uploads/VLDB_2024_Research_paper_013_a13bc1c6e6.png)
We quickly put a small team of authors together, and while some of us had already written research papers as PhD students at university, others were new to this. An intensive writing process kicked off in November 2023 with status calls almost daily, as the paper authors live in different locations. We submitted our final version in April 2024\.


![VLDB 2024 Research paper.014.png](/uploads/VLDB_2024_Research_paper_014_98bc5a0104.png)
## Summary [\#](/blog/first-clickhouse-research-paper-vldb-lightning-fast-analytics-for-everyone#summary)


![VLDB 2024 Research paper.015.png](/uploads/VLDB_2024_Research_paper_015_2524140982.png)
We had a blast last week! Apart from feasts of delicious [Cantonese cuisine](https://en.wikipedia.org/wiki/Cantonese_cuisine), the ClickHouse team spent last week at the special 50th\-anniversary VLDB 2024 conference in Guangzhou, China, where our CTO and creator of ClickHouse, Alexey Milovidov, proudly presented our first ClickHouse research paper to the scientific community.


We hope you enjoy reading the paper and watching the recording of Alexey’s presentation. We would love to hear what you think.


Lastly, for your convenience, here is a list with links to the paper and all it's accompanying material mentioned in this post:


- [VLDB 2024 research paper](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) "ClickHouse \- Lightning Fast Analytics for Everyone" \+ [poster](https://raw.githubusercontent.com/ClickHouse/clickhouse-presentations/master/vldb_2024/VLDB_2024_poster.pdf)
- [Recording](https://youtu.be/7QXKBKDOkJE) of Alexey Milovidov's paper presentation at VLDB 2024 \+ [slide deck](https://raw.githubusercontent.com/ClickHouse/clickhouse-presentations/master/vldb_2024/VLDB_2024_presentation.pdf)
- [Recording](https://youtu.be/vyYjKuvnSY0) of extended meetup version of our VLDB 2024 talk \+ [slide deck](https://raw.githubusercontent.com/ClickHouse/clickhouse-presentations/master/meetup121/GZ%20meetup%20by%20Tom%20and%20Robert.pdf)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
