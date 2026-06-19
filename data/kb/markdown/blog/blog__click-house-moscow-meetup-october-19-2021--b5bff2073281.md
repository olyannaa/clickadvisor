# ClickHouse Moscow Meetup October 19, 2021


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Moscow Meetup October 19, 2021

Rich RaposaNov 11, 2021 · 3 minutes readClickHouse organized an online Meetup on October 19, 2021, hosted by our very own co\-founder and CTO, Alexey Milovidov. There are a lot of new features to discuss in the 21\.10 version of ClickHouse, along with many more new features coming up on the roadmap.


There were over 200 attendees in person for the Meetup and 3,853 viewers online, and we want to thank everyone who attended live. You can watch the recording of the Meetup on YouTube [here](https://www.youtube.com/watch?v=W6h3_xykd2Y).


Alexey Milovidov, Chief Technology Officer, welcomed and updated the community on ClickHouse Inc.'s latest news. Maksim Kita, Sr. Software Engineer at ClickHouse, started with a discussion on the new User Defined Functions (UDFs) available in 21\.10\. UDFs can be defined as lambda expressions using the CREATE FUNCTION command. For example:



```
CREATE FUNCTION a_plus_b AS (a, b) -> a + b

```

In addition to UDFs, there are two new table engines \- Executable and ExecutablePool \- that can stream records via stdin and stdout through custom scripts written in whatever language you prefer. For details, be sure to check out our [new training lesson on What's New in ClickHouse 21\.10](https://clickhouse.com/learn/lessons/whatsnew-clickhouse-21.10/).


You can now encrypt your data stored on S3, HDFS, external disks, or on a local disk. ClickHouse developers Vitaly Baranov and Artur Filatenkov discussed the details and benefits of encrypting your data at rest in ClickHouse. Vitaly presented the new full disk encryption feature and Arthur presented column\-level encryption.


![disk-encryption-performance.jpeg](/uploads/disk_encryption_performance_80c4b61183.jpeg)
![arthur-filatenkov.jpeg](/uploads/arthur_filatenkov_e06321b4f3.jpeg)
Alexey then spent 40 minutes discussing some of the amazing new features on the ClickHouse roadmap, including:


- ClickHouse Keeper: a new C\+\+ coordination system for ClickHouse designed as an alternative to ZooKeeper
- Support for working with semi\-structured data, including JSON objects with arbitrary nested objects
- Asynchronous insert mode \- now you can insert data without batching!


After the talk, Alexey took questions from users on:


- How to parse User\-Agent in ClickHouse
- Is it true that ClickHouse developers have a ClickHouse tattoo


![yaml-configuration.jpeg](/uploads/yaml_configuration_8521694388.jpeg)
- If you are excited about ClickHouse, be sure to join us on [Telegram](https://t.me/clickhouse_en)
- We also have a community Slack workspace be sure to join [here](https://clickhousedb.slack.com/).
- If you are new to ClickHouse and want to see it in action, check out our [Getting Started lesson](https://clickhouse.com/learn/lessons/gettingstarted/).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
