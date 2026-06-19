# ClickHouse at Percona Live 2019


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse at Percona Live 2019

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jun 4, 2019 · 4 minutes readThis year American episode of [Percona Live](https://www.percona.com/live/19/) took place in nice waterfront location in Austin, TX, which welcomed open source database experts with pretty hot weather. ClickHouse community is undeniably growing and it became a common database product to give a talk about or at least compare or refer to, while just [two short years ago](blog/click-house-at-percona-live-2017) it was more like “wth is ClickHouse?”.


Alexey Rubin from VirtualHealth compared two column\-oriented databases: ClickHouse and MariaDB Column Store. Bottom line was no surprise, ClickHouse is noticeably faster and MariaDB is more familiar for MySQL users, details were useful though.
![2019-percona-live-1.jpeg](/uploads/2019_percona_live_1_af335ac04a.jpeg)


Alexey Milovidov from Yandex have demonstrated how exactly ClickHouse became even faster in recent releases.
![2019-percona-live-2.jpeg](/uploads/2019_percona_live_2_65101a2d4b.jpeg)


Alexander Zaitsev and Robert Hodges from Altinity have given an entry level tutorial to ClickHouse, which included loading in demo dataset and going through realistic queries against it with some extra variation demonstrating possible query optimization techniques. [Slides](https://www.percona.com/live/19/sites/default/files/slides/Making%20HTAP%20Real%20with%20TiFlash%20--%20A%20TiDB%20Native%20Columnar%20Extension%20-%20FileId%20-%20174070.pdf). Also Altinity was sponsoring the ClickHouse booth in Expo Hall which became an easy spot for people interested in ClickHouse to chat outside of talks.
![2019-percona-live-3.jpeg](/uploads/2019_percona_live_3_1e5bfcf029.jpeg)


Ruoxi Sun from PingCAP introduced TiFlash, column\-oriented add\-on to TiDB for analytics based on ClickHouse source code. Basically it provides [MergeTree](/docs/en/engines/table-engines/mergetree-family/mergetree/)\-like table engine that is hooked up to TiDB replication and has in\-memory row\-friendly cache for recent updates. Unfortunately, PingCAP has no plans to bring TiFlash to opensource at the moment. [Slides](https://www.percona.com/live/19/sites/default/files/slides/Making%20HTAP%20Real%20with%20TiFlash%20--%20A%20TiDB%20Native%20Columnar%20Extension%20-%20FileId%20-%20174070.pdf).
![2019-percona-live-4.jpeg](/uploads/2019_percona_live_4_16f9e05dec.jpeg)


ClickHouse has also been covered in talk by Jervin Real and Francisco Bordenave from Percona with overview of moving and replicating data around MySQL\-compatible storage solutions. [Slides](https://www.percona.com/live/19/sites/default/files/slides/Replicating%20MySQL%20Data%20to%20TiDB%20For%20Real-Time%20Analytics%20-%20FileId%20-%20187672.pdf).
![2019-percona-live-5.jpeg](/uploads/2019_percona_live_5_3d99984c08.jpeg)


ClickHouse represented columnar storage systems in venture beyond relational by Marcos Albe from Percona.
![2019-percona-live-6.jpeg](/uploads/2019_percona_live_6_7300eeb56b.jpeg)


Jervin Real from Percona have demonstrated real case study of applying ClickHouse in practice. It heavily involved manual partitions manipulation, hopefully audience have understood that it is an option, but not exactly a best practice for most use cases. [Slides](https://www.percona.com/live/19/sites/default/files/slides/Low%20Cost%20Transactional%20and%20Analytics%20With%20MySQL%20and%20Clickhouse,%20Have%20Your%20Cake%20and%20Eat%20It%20Too!%20-%20FileId%20-%20187674.pdf).
![2019-percona-live-7.jpeg](/uploads/2019_percona_live_7_d9aed7c2ba.jpeg)


Evgeny Potapov from ITSumma went through modern options for time\-series storage and once more confirmed ClickHouse is leading the way in this field as well.
![2019-percona-live-8.jpeg](/uploads/2019_percona_live_8_f08808182d.jpeg)


Event location in the center of US provided equal opportunities for people from East and West Coast to show up, but presence of people from other countries was also quite noticeable. The content they all brought in was top notch as usual.
![2019-percona-live-9.jpeg](/uploads/2019_percona_live_9_5cc913c105.jpeg)


Austin after the Event.
![2019-percona-live-10.jpeg](/uploads/2019_percona_live_10_2ce9bb43d8.jpeg)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
