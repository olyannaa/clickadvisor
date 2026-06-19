# ClickHouse at FOSDEM 2026


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse at FOSDEM 2026

![photo-tyler-hannan.jpeg](/_next/image?url=%2Fuploads%2Fphoto_tyler_hannan_250918fdc5.jpeg&w=96&q=75)[Tyler Hannan](/authors/tyler-hannan)Apr 8, 2026 · 7 minutes readFOSDEM 2026 took place on 31 January and 1 February in Brussels, and it was a great weekend for the ClickHouse community, both inside the conference rooms and out.


## Community Dinner [\#](/blog/clickhouse-at-fosdem-2026#community-dinner)


The weekend kicked off with the ClickHouse community dinner at L'Ultime Atome in Ixelles, Brussels. 106 people joined us for dinner, drinks, and some of the best conversations of the conference. ClickHouse founder Alexey was there to chat and answer questions. Thanks to everyone who came out; it was a fantastic evening (some pictures are at the end of this post).


But it wasn’t just a chance to eat and drink; we had multiple presentations at the event itself.


## Our Talks [\#](/blog/clickhouse-at-fosdem-2026#our-talks)


### Planes, Ships, Birds – Building Real\-Time Visualizations with ClickHouse [\#](/blog/clickhouse-at-fosdem-2026#planes-ships-birds--building-real-time-visualizations-with-clickhouse)


**Track:** Geospatial · **Day:** Saturday
**Speaker:** Alexey Milovidov · [Slides](https://presentations.clickhouse.com/2026-fosdem-geospatial/)


This session walked through creating an analytical application from the ground up, covering the entire workflow: data collection, processing, and visualization. The stack uses Leaflet, ClickHouse, and a collection of shell scripts. The finished result is published at [adsb.exposed](https://adsb.exposed/), and the talk uncovered how it was built.





---


### Hotpatching ClickHouse in Production with XRay [\#](/blog/clickhouse-at-fosdem-2026#hotpatching-clickhouse-in-production-with-xray)


**Track:** LLVM · **Day:** Saturday
**Speaker:** Pablo Marcos · [Slides](https://fosdem.org/2026/events/attachments/N7MVZT-hotpatching-clickhouse-with-llvm-xray/slides/266966/hotpatchi_f1nbs5s.pdf)


Ever been debugging a production issue and wished you'd added just one more log statement — only to face a rebuild, a wait for CI, and a full redeploy? The ClickHouse team integrated LLVM's XRay to solve exactly this. It lets you hot\-patch a running production system to inject logging, profiling, and even deliberate delays into any function, with no rebuild required.


XRay reserves space at function entry and exit points that can be atomically patched with custom handlers at runtime. The team built three handler types: LOG to add the trace points you forgot, SLEEP to reproduce or prevent timing\-sensitive bugs, and PROFILE for deterministic profiling to complement the existing sampling profiler. The performance overhead when inactive is negligible.


Control is via a SQL query — `SYSTEM INSTRUMENT ADD LOG 'QueryMetricLog::startQuery' 'message'` — which patches the function instantly, with results appearing in `system.trace_log`. The talk also covered the integration challenges (ELF parsing, thread\-safety, atomic patching), performance numbers (4–7% binary size increase, near\-zero runtime cost), and real production war stories.





---


### Inverted database indexes: The why, the what, and the how. [\#](/blog/clickhouse-at-fosdem-2026#inverted-database-indexes-the-why-the-what-and-the-how)


**Track:** Databbases · **Day:** Saturday
**Speaker:** Elmi Ahmadov · [Slides](https://presentations.clickhouse.com/2026-fosdem-inverted-index/Inverted_indexes_the_what_the_why_the_how.pdf)


Database usage in practice often involves heavy text processing. For example, in "observability" use cases, databases must extract, store, and search billions of log messages daily. Most databases, including many column\-oriented OLAP databases, struggle with such massive amounts of text data. The only way to process text data at scale is by using specialized inverted indexes in databases.


This presentation explains how inverted indexes work and which (text) search patterns they support. Where appropriate, we describe our experience and the gotchas we encountered when adding an inverted index to ClickHouse, one of the most popular open\-source databases for analytics.





---


### ClickHouse's C\+\+ and Rust Journey [\#](/blog/clickhouse-at-fosdem-2026#clickhouses-c-and-rust-journey)


**Track:** Rust · **Day:** Sunday
**Speaker:** Alexey Milovidov · [Slides](https://presentations.clickhouse.com/2025-p99/)


For a large C\+\+ codebase, a full rewrite to Rust is not an option — only gradual integration with Rust libraries is realistic, and even then there are many complications and rough edges. This talk described the experience of integrating Rust and C\+\+ code in ClickHouse, and some of the weird and unusual problems the team had to overcome along the way.





---


### How to Move Bytes Around [\#](/blog/clickhouse-at-fosdem-2026#how-to-move-bytes-around)


**Track:** Software Performance · **Day:** Sunday
**Speaker:** Alexey Milovidov · [Slides](https://presentations.clickhouse.com/2026-fosdem-memcpy/)


If you take a random program and start profiling it, you'll usually find `memcpy` near the top — though that doesn't necessarily mean memcpy is slow. As the abstract puts it: the most hopeless thing a C\+\+/Rust developer can do (while no one is watching) is optimize memcpy to move bytes faster. That's exactly what this talk did.





---


### Contributing to MariaDB \& Postgres [\#](/blog/clickhouse-at-fosdem-2026#contributing-to-mariadb--postgres)


**Track:** Databases · **Day:** Saturday
**Speakers:** Georgi Kodinov, Kevin Biju


A two\-part talk on contributing to major open\-source database projects.


Georgi Kodinov walked through what it actually takes to get a contribution into the MariaDB server codebase, following a real bug fix — two lines of code — through its entire review process, and explaining why the bar is higher than it might seem on a project of this scale.


Kevin Biju traced his own path from setting up a local Postgres build to contributing bug\-fix patches and documentation updates. The talk outlines how the Postgres development process and community operate, with the aim of demystifying the process so more engineers feel confident making their first (or next) patch.





---


## From the Community [\#](/blog/clickhouse-at-fosdem-2026#from-the-community)


We weren't the only ones talking about ClickHouse at FOSDEM. Here are some talks from the community that are worth checking out:


### Dynamic Bot Blocking with Web\-Server Access\-Log Analytics [\#](/blog/clickhouse-at-fosdem-2026#dynamic-bot-blocking-with-web-server-access-log-analytics)


Alexander Krizhanovsky \- [Video](https://fosdem.org/2026/schedule/event/3BMPMU-dynamic_bot_blocking_with_web-server_access-log_analytics/)


Bots generate roughly half of all Internet traffic. Some are clearly malicious (password crackers, vulnerability scanners, application\-level/L7 DDoS), and others are merely unwanted (web scrapers, carting, appointment etc) bots. Traditional challenges (CAPTCHAs, JavaScript checks) degrade user experience, and some vendors are deprecating them. An alternative is traffic and behavior analytics, which is much more sophisticated, but can be far more effective.


Complicating matters, there are cloud services not only helping to bypass challenges, but also mimic browsers and human behavior. It's tough to build a solid protection system withstand such proxy services.


In this talk, we present WebShield, a small open\-source Python daemon that analyzes Tempesta FW, an open\-source web accelerator, access logs and dynamically classifies and blocks bad bots.


You'll learn: \* Which bots are easy to detect (e.g., L7 DDoS, password crackers) and which are harder (e.g., scrapers, carting/checkout abuse). \* Why your secret weapon is your users’ access patterns and traffic statistics—and how to use them. \* How to efficiently deliver web\-server access logs to an analytics database (e.g., ClickHouse). \* Traffic fingerprints (JA3, JA4, p0f): how they’re computed and their applicability for machine learning \* Tempesta Fingerprints: lightweight fingerprints designed for automatic web clients clustering. \* How to correlate multiple traffic characteristics and catch lazy bot developers. \* Baseline models for access\-log analytics and how to validate them. \* How to block large botnets without blocking half the Internet. \* Scoring, behavioral analysis, and other advanced techniques are not yet implemented


## Photos [\#](/blog/clickhouse-at-fosdem-2026#photos)


We wish you could have been there. Here are some images that capture a sense of the experience. Do you want to join the next one? Let us know and we can help with your presentation.

Previous slide\<\-Next slide\-\>![](/_next/image?url=%2Fuploads%2FIMG_2418_278b810aed.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260201_105432126_93a240840f.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2F1000137544_91dc7234e1.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260131_194611228_13bf9b1778.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260201_141128012_622724b026.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260131_194552756_a8aeaf6c81.jpg&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FIMG_2418_278b810aed.jpg&w=384&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260201_105432126_93a240840f.jpg&w=384&q=75)![](/_next/image?url=%2Fuploads%2F1000137544_91dc7234e1.jpg&w=384&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260131_194611228_13bf9b1778.jpg&w=384&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260201_141128012_622724b026.jpg&w=384&q=75)![](/_next/image?url=%2Fuploads%2FPXL_20260131_194552756_a8aeaf6c81.jpg&w=384&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
