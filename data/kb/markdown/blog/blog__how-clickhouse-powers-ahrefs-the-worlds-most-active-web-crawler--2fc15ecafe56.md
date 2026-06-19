# Singapore Meetup Report: How ClickHouse Powers Ahrefs, the World's Most Active Web Crawler


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Singapore Meetup Report: How ClickHouse Powers Ahrefs, the World's Most Active Web Crawler

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Jul 27, 2023 · 5 minutes read![Ahrefs_photo.png](/uploads/Ahrefs_photo_85bd1c256b.png)
On July 27th, 2023, Alibaba Cloud hosted the ClickHouse community meetup in Singapore. We had the pleasure of hearing from Yasunari (Yasu) Watanabe from Ahrefs, who shared their journey with ClickHouse on a massive scale.


Founded in 2010, [Ahrefs](https://ahrefs.com/) is renowned for processing immense volumes of web analytics data to provide valuable SEO metrics. They have the most active crawler in the industry, with the world’s largest index of live backlinks.


![Ahrefs1.png](/uploads/Ahrefs1_7df5bcab84.png)
## Early Data Storage Solutions [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#early-data-storage-solutions)


Yasu shared Ahrefs' journey over the years working with various data storage solutions.
“We tried all the available solutions out there, including Cassandra and Hypertable, but none of them really met our requirements. So we ended up developing a custom solution that was optimized for crawling the web with limited resources,” Yasu explained.


As part of their own customer storage solution for the web crawler, they used the Quantcast File System (QFS), alongside Elasticsearch for other non\-crawler tasks. While this combination served them well for some time, it soon revealed its limitations due to an inflexible query engine, the absence of advanced features, and scaling challenges. Yasu shared, “Times change, feature requirements become more complex, the size of the web is growing and our infrastructure keeps on scaling up, so we went looking for some alternative solutions”.


## Migration to ClickHouse [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#migration-to-clickhouse)


In 2019, Ahrefs discovered ClickHouse. They were initially drawn to the ClickHouse architecture which resembled their custom system. ClickHouse offered superior performance, a SQL interface, versatile I/O support, and a column\-oriented approach. This made querying highly efficient for their growing datasets.


Currently, Ahrefs has embedded ClickHouse deeply into their system. They operate multiple ClickHouse clusters on their hardware, with the main cluster being geo\-replicated for both redundancy and task\-specific efficiency. Yasu shared the massive scale at which they operate, “We have multiple clusters deployed on our hardware with hundreds of hosts. Our main cluster is now geo\-replicated, and we designate some replicas for read\-heavy operations and others for write\-heavy operations. Many of our tables are quite large, with trillions and trillions of rows, as well as tens of columns.”


![Ahrefs2.png](/uploads/Ahrefs2_99b947590b.png)
## Advanced Interactions with ClickHouse [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#advanced-interactions-with-clickhouse)


Yasu revealed Ahrefs' strategies for advanced interaction with ClickHouse. To handle their large scale data insertions, Ahrefs uses a buffering technique, grouping data for fewer insert operations, which reduces subsequent merging tasks. Yasu explained "We also use extensive use of fetch and [attach commands to move parts efficiently](https://clickhouse.com/docs/en/sql-reference/statements/alter/partition) across different servers. This one, it's a really, really nice feature that’s handled by ClickHouse."


![Ahrefs3.png](/uploads/Ahrefs3_6b163950fe.png)
## Internal Monitoring Tools [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#internal-monitoring-tools)


Ahrefs developed tools including the "Birdseye View Tool" for a complete overview of ClickHouse clusters and the "Query Analyzer" to understand and optimize query performance. Yasu hinted at the possibility of these tools being open\-sourced, which would be a great contribution to the broader tech community.


![Ahrefs4.png](/uploads/Ahrefs4_e71ac490b3.png)
![Ahrefs5.png](/uploads/Ahrefs5_1a1adb6654.png)
## Mark Compression: Ahrefs' Contribution to ClickHouse [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#mark-compression-ahrefs-contribution-to-clickhouse)


Discussing an upstream patch Ahrefs proposed to ClickHouse, Yasu explained the issue with marks, which help locate rows in compressed data files. Large\-scale queries can strain the cache of these marks, affecting performance. Ahrefs' solution involved compressing these marks for efficiency. After using their solution for a year, Ahrefs discussed its potential with the ClickHouse team. The final accepted solution divided marks into blocks with a custom compression scheme, which eliminated the need for mutexes, reducing memory consumption by three to six times.


![Ahrefs6.png](/uploads/Ahrefs6_6f39c3d04f.png)
## Summary [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#summary)


Ahrefs' switch to ClickHouse has brought significant improvements in data handling and performance. This transition has allowed them to manage massive data volumes more efficiently. Their innovations, like the mark compression solution, have enhanced query performance, saving memory and time. Yasu concluded “I would say that our decision to start using CickHouse in Ahrefs is not without its hurdles, but, overall it's been a great success. We're happy with the performance that is able to keep up with our usage demands. And we really appreciate the active feature development and bug fixes that go on in the regular monthly releases.”


Ahrefs continues to work on new features, promising further advancements in their collaboration with ClickHouse.


## More Details [\#](/blog/how-clickhouse-powers-ahrefs-the-worlds-most-active-web-crawler#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-singapore-meetup-group/events/294428050/) in Singapore on July 27th, 2023
- The presentation materials are available [on GitHub](https://github.com/ClickHouse/clickhouse-presentations/tree/master/meetup80)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
