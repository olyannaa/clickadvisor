# SIEM made simpler: How Huntress improved performance and slashed costs with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# SIEM made simpler: How Huntress improved performance and slashed costs with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 19, 2024 · 8 minutes read
[Huntress](https://www.huntress.com/) is on a mission to make enterprise\-level security accessible to everyone. Founded in 2015 by a team of ex\-NSA cyber operators, the managed security platform offers a range of solutions designed to keep small and mid\-sized businesses safe from cyber threats.




But while Huntress positions itself as a security company, co\-founder and CTO Chris Bisnett admits — only half\-joking — that “secretly we’re a big data company.” With more than 3 million endpoints, data from over a million Microsoft 365 identities, and logs flowing in from around half a million data sources, Huntress’s ability to analyze and act on this massive volume of information is central to its success.




At a [ClickHouse meetup in New York](https://www.youtube.com/watch?v=lhsWNofOcdk), Chris explained how switching to ClickHouse Cloud has helped Huntress optimize performance, address scaling challenges, and simplify their big data workflows, all while saving tens of thousands of dollars each month.




## The SIEM dilemma [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#the-siem-dilemma)



A [SIEM (Security Information and Event Management)](https://clickhouse.com/engineering-resources/siem) system is designed to collect, process, and analyze logs and security data from various sources within an organization’s network. It acts as a centralized hub, pulling in information from firewalls, cloud infrastructure, identity providers, and other devices to detect and respond to potential threats in real time.




But managing a SIEM is tricky at the best of times. The challenge, as Chris describes it, is twofold: volume and variety. SIEMs must handle huge amounts of data coming from diverse sources, each in its own format — syslog, JSON, plain text, and more. This requires companies like Huntress to develop custom parsers and schemas to standardize and make the data usable. As data volumes surge, the costs associated with processing and storing it also increase, making it difficult to maintain efficiency and affordability.




For Huntress, the standard SIEM challenges are amplified by the needs of their customers — SMBs with limited IT resources. “They don’t have big budgets or internal security teams, and yet they need a lot of the same things as larger enterprises,” Chris says of Huntress’s customers. “So there’s gotta be a trade\-off somewhere. It’s our job to figure that part out.”




To provide customers with the same level of 24/7 monitoring and proactive threat protection as enterprise companies, Huntress needed a more efficient database management system that could process logs from millions of endpoints while keeping costs in check. Adding to the pressure was an ambitious timeline of improving their SIEM solution in 6\-8 months.




“A lot of people said it couldn’t be done,” Chris says. “But we did it anyway.”



## In search of a better database [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#in-search-of-a-better-database)



Chris and the team kicked off a search for a database that could handle their growing data volumes without driving costs through the roof. They began by exploring familiar options, including Elasticsearch, which they had used before. But while Elasticsearch offered strong search capabilities, scaling it for Huntress’s workload was, in Chris’s words, “super expensive,” costing upwards of $70,000 per month. They also considered Postgres, but as Chris explains, “The problem there is, if you want to scale it, you’ve got to have multiple individual Postgres databases,” which added unwanted complexity and increased costs.




Microsoft Sentinel, another contender, was briefly evaluated for its ability to manage large data volumes. For Huntress, however, building their SIEM on an existing solution like Sentinel offered little opportunity for differentiation. It was important to keep a competitive edge by creating a unique system tailored to their needs, rather than relying on a pre\-built solution.




Around this time, they noticed [ClickHouse Cloud](https://clickhouse.com/cloud) gaining popularity. They decided to give it a try and found that the managed service offered a scalable solution that met Huntress’s data needs at a fraction of the cost of Elasticsearch — around $5,000 per month for a comparable workload. ClickHouse’s support for [materialized views](https://clickhouse.com/docs/en/materialized-view) and advanced query capabilities, without requiring extensive configuration, made it an ideal fit for powering their SIEM, balancing performance, affordability, and the specific needs of their customers.




“The best part is, there’s zero maintenance required,” Chris says. “We just ingest a ton of data in there; it’s super efficient and way cheaper than other solutions. It checks all the boxes.”



## Huntress’s new data infrastructure [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#huntresss-new-data-infrastructure)



Huntress’s implementation of ClickHouse is defined by its simplicity. “To me, simple generally means cheaper and more reliable,” Chris says. “It means fewer parts to go wrong.”




As a Ruby on Rails shop, they use Vector.dev (a tool open\-sourced by Datadog) to batch and transform data before it reaches ClickHouse. According to Chris, Vector allows Huntress to handle large\-scale inserts — up to 200,000 records per second — which ClickHouse manages “without batting an eye.” This architecture reflects Chris’s philosophy of keeping infrastructure lean to minimize points of failure and reduce costs and maintenance requirements.






![386382601-f9fcb272-9d89-4c88-b29b-6a1900aad069.png](/uploads/386382601_f9fcb272_9d89_4c88_b29b_6a1900aad069_b49ad86b4c.png)


Huntress’s data pipeline: Rails and Vector process data before integration into ClickHouse for optimal performance.




Data sources are funneled through Vector, which batches and routes the data directly into ClickHouse. The team uses HTTP as the insert method, taking advantage of Vector’s templating language to dynamically map data fields to ClickHouse tables. This setup has allowed Huntress to scale their data ingestion seamlessly, without adding complexity or overhead.



## Lessons learned along the way [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#lessons-learned-along-the-way)



For the Huntress team, implementing and scaling ClickHouse wasn’t without its challenges. During his presentation in New York, Chris shared a few key lessons learned:



### Partitioning [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#partitioning)



Initially, Huntress tried to partition data by tenants and days, following a common pattern in other databases like Postgres. However, they quickly ran into limitations, as ClickHouse restricts the number of partitions per insert. As Chris explains, they learned that partitions in ClickHouse are best used for lifecycle management, such as time\-to\-live (TTL) configurations, rather than for primary data sharding.



### Table ordering [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#table-ordering)



Defining a proper sorting key was important for optimizing performance. Huntress found that ordering tables by tenant ID and other common fields dramatically improved query speeds. As Chris explains, “The ordering of your data, your primary key, and your sorting key is super important. This is maybe the biggest thing that drives performance in ClickHouse.” 




ClickHouse’s ability to skip over irrelevant data based on sorting keys is a powerful feature, but it requires precision from the outset. Chris notes that fixing the table order after the fact can be complex and time\-consuming — something the Huntress team experienced firsthand.



### Data skipping indexes [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#data-skipping-indexes)



While ClickHouse’s [data skipping indexes](https://clickhouse.com/docs/en/optimize/skipping-indexes) can improve query performance by ignoring non\-relevant granules, they “aren’t magic,” Chris says. The team found that these indexes function differently from secondary indexes in Postgres; in order to be effective, the data must be ordered correctly, and the indexes should be applied strategically. When not set up properly, the Huntress team saw little to no performance improvement. “The real performance issue was having to visit multiple parts to find the data we needed,” Chris says.



## Building a scalable, efficient future [\#](/blog/how-huntress-improved-performance-and-slashed-costs-with-clickHouse#building-a-scalable-efficient-future)



By switching to ClickHouse Cloud, Huntress has transformed its approach to data management, cutting costs by more than 90% while improving performance. The new setup easily processes up to 200,000 records per second, allowing Huntress to scale as its customer base grows. ClickHouse’s features, like materialized views and advanced query capabilities, have given the team the foundation and framework needed to create a streamlined, low\-maintenance system that meets their needs now and in the future.




Not only has the move to ClickHouse strengthened Huntress’s ability to deliver fast, accurate threat detection, it has reinforced their mission of making enterprise\-level security accessible to everyone. With a scalable and efficient data infrastructure in place, Huntress is poised to keep expanding its services, ensuring that comprehensive, affordable protection remains within reach for small and mid\-sized businesses around the world.





> To learn more about how ClickHouse can help you improve performance and scalability while reducing costs, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
