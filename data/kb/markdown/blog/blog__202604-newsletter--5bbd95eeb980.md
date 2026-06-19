# April 2026 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# April 2026 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Apr 16, 2026 · 10 minutes readHello, and welcome to the April 2026 ClickHouse newsletter!


This month, we have a new CLI for ClickHouse local and cloud, agentic coding at ClickHouse, materialized CTEs in our latest release, building a SIEM, and more!


## Featured community member: Nazarii Piontko [\#](/blog/202604-newsletter#featured-community-member)


This month's featured community member is Nazarii Piontko, Solutions Architect at Future Processing.


![](/uploads/newsletter_apr2026_image2_c4a00ae7d0.png)
He leads technical presales and architecture, translating complex requirements into solutions for clients across trading, mobility, and logistics. He stays hands\-on through open\-source contributions to distributed data systems, mentors engineers, and has taught at universities.


Nazarii contributed two features to ClickHouse 26\.3 LTS: the [`naturalSortKey`](https://github.com/ClickHouse/ClickHouse/pull/90322) function, which enables intuitive sorting of strings containing numbers (so "file10" sorts after "file9", not "file1"), and support for the [ALP compression codec](https://github.com/ClickHouse/ClickHouse/pull/91362), which brings efficient lossless compression for floating\-point data.


➡️ [Connect with Nazarii on LinkedIn](https://www.linkedin.com/in/piontko/)


## Open House 2026 [\#](/blog/202604-newsletter#open-house)


It's just over a month until the second edition of [Open House](https://clickhouse.com/openhouse/san-francisco), a free three\-day ClickHouse user conference running May 26–28 in San Francisco.


Kick things off on May 26 with hands\-on workshops covering real\-time analytics, observability, database administration, and data warehousing, then head into two days of keynotes, technical sessions, and networking.


Hear from ClickHouse CEO Aaron Katz and CTO Alexey Milovidov, plus industry guests including Bret Taylor (Sierra) and Guillermo Rauch (Vercel). Admission is free!


➡️ [Register now](https://clickhouse.com/openhouse/san-francisco)


## 26\.3 release [\#](/blog/202604-newsletter#26-3-release)


![](/uploads/newsletter_apr2026_image1_ce952c56f3.png)
26\.3 sees the experimental introduction of materialized Common Table Expressions (CTEs) and WebAssembly User\-defined functions (UDFs).


This release also makes asynchronous inserts the default, enables JOIN reordering for ANTI, SEMI, and FULL, and improves the internal storage of the ClickHouse Map data type.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-26-03)


## Introducing clickhousectl: the CLI for ClickHouse local and cloud (beta) [\#](/blog/202604-newsletter#introducing-clickhousectl)


![april_2026_clickhouse-ctl.png](/uploads/april_2026_clickhouse_ctl_e3d28f3583.png)
Alasdair Brown announced clickhousectl, a CLI for managing both local ClickHouse installations and cloud deployments, built with AI agents in mind alongside human developers.


Designed for agentic development, it handles local version management, project scaffolding, and server lifecycle, while also supporting cloud infrastructure commands with authentication safeguards like read\-only OAuth and permissioned API keys.


➡️ [Read the blog post](https://clickhouse.com/blog/introducing-clickhousectl-official-cli-for-clickhouse-local-and-cloud)


## How Goldsky made historical blockchain data backfills 12x faster [\#](/blog/202604-newsletter#how-goldsky-made-historical-blockchain-data-backfills-12x-faster)


![](/uploads/newsletter_apr2026_image6_7949daf91e.png)
Goldsky sped up historical blockchain backfills by 12x by replacing their Kafka/Avro pipeline with direct ClickHouse reads using the Apache Arrow format.


Eliminating deserialization overhead by reading data in the format closest to its physical storage proved extremely efficient, boosting throughput from \~50K to \~600K rows/second.


➡️ [Read the blog post](https://goldsky.com/blog/making-historical-blockchain-backfills-faster)


## Agentic coding at ClickHouse [\#](/blog/202604-newsletter#agentic-coding-at-clickhouse)


![](/uploads/newsletter_apr2026_image7_ffb09aaaf1.png)
Our CTO, Alexey Milovidov, argues that agentic coding has crossed the threshold into genuine usefulness for professional software development, driven by recent model improvements such as Claude Opus 4\.5\.


He walks through how we've achieved productivity gains by using AI agents across a wide range of tasks \- fixing flaky tests, investigating bugs, code reviews, security research, and more.


The key takeaway: As of today, agents work best as pair programmers under an engineer's direction, not as autonomous replacements.


➡️ [Read the blog post](https://clickhouse.com/blog/agentic-coding)


## Building a SIEM with ClickHouse and Clickdetect [\#](/blog/202604-newsletter#building-a-siem-with-clickhouse-and-clickdetect)


![](/uploads/newsletter_apr2026_image3_f7c3e467cd.png)
Vinicius Morais walks through building a SIEM architecture using ClickHouse and Clickdetect, an open\-source detection engine that runs SQL\-based security rules against your log data.


He uses Wazuh (an open\-source security platform) solely as a log collector and decoder, forwarding parsed alerts to a ClickHouse table with compression codecs, TTLs, bloom filter indexes, and S3 storage support.


From there, Clickdetect schedules detections and fires alerts to a webhook — giving you a lightweight, cost\-effective SIEM that scales from a single node to a distributed ClickHouse cluster.


➡️ [Read the blog post](https://medium.com/@souzo/building-a-powerful-siem-with-clickhouse-and-clickdetect-ae68a4495a76)


## Building high\-performance full\-text search for object storage [\#](/blog/202604-newsletter#building-high-performance-full-text-search-for-object-storage)


![](/uploads/newsletter_apr2026_image8_39f30f112c.png)
Last month, we announced that Full\-text search was generally available. We now have a blog post written by the engineering team explaining how they redesigned the FTS index to work efficiently with object storage, where random reads are expensive.


The new index uses front\-coding compression, a sparse lookup index, and adaptive posting lists, allowing many queries to be answered from the index alone without touching the underlying text columns.


➡️ [Read the blog post](https://hookdeck.com/blog/how-we-made-payload-search-60x-faster-in-clickhouse)


## Quick reads [\#](/blog/202604-newsletter#quick-reads)


- Marcin Kulakowski explains [why ClickHouse is becoming the data control plane](https://mkulakowski2-73849.medium.com/the-rise-of-real-time-data-why-clickhouse-is-becoming-the-control-plane-77b59bf85399).
- Divyanshu shares what he [learned about observability (and ClickHouse) in 10 days](https://medium.com/@shekdivyanshu/what-i-learned-about-observability-in-10-days-a370c143d2ee).
- Alexandra Petra Berger [draws parallels](https://medium.com/towards-data-engineering/poyekhali-what-1961-soviet-space-tech-teaches-us-about-modern-data-engineering-1549445a054f) between Sergei Korolev's space engineering principles \- precision, redundancy, and military\-grade quality checks \- and modern data engineering practices, using ClickHouse compression codecs like Gorilla and DoubleDelta to illustrate how the same rigor applies to building reliable data systems.


## Upcoming events [\#](/blog/202604-newsletter#upcoming-events)


### Global virtual events [\#](/blog/202604-newsletter#global-virtual-events)


- [Combining Postgres \& ClickHouse to Build a Unified Data Stack](https://clickhouse.com/company/events/202604-APJ-Webinar-Unified-Data-Stack-ClickHouse-Postgres) \- Apr 22, 2026
- [CDC ClickPipes Webinar](https://clickhouse.com/company/events/202604-EMEA-Webinar-CDC-ClickPipes) \- Apr 23, 2026
- [Analisando bilhões de registros em tempo real](https://clickhouse.com/company/events/202604-LATAM-Real-Time-Analytics) \- Apr 16, 2026
- [Analizando miles de millones de registros en tiempo real](https://clickhouse.com/company/events/202605-LATAM-Real-Time-Analytics-ES) \- May 14, 2026


### Virtual training [\#](/blog/202604-newsletter#virtual-training)


- [ClickHouse Fundamentals](https://clickhouse.com/company/events/202605-AMER-ClickHouse-Fundamentals) \- May 5, 2026
- [Data Warehousing with ClickHouse: Level 1](https://clickhouse.com/company/events/202605-AMER-EMEA-data-warehousing-Level1) \- May 13, 2026
- [Data Warehousing with ClickHouse: Level 2](https://clickhouse.com/company/events/202605-AMER-EMEA-data-warehousing-Level2) \- May 14, 2026
- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202605-AMER-EMEA-Observability-with-ClickStack-Level1) \- May 19, 2026
- [Data Warehousing with ClickHouse: Level 3](https://clickhouse.com/company/events/202605-AMER-EMEA-data-warehousing-Level3) \- May 20, 2026
- [ClickHouse Fundamentals](https://clickhouse.com/company/events/202605-EMEA-ClickHouse-Fundamentals) \- May 21, 2026


### Events in AMER [\#](/blog/202604-newsletter#events-in-amer)


- [Meetup in Sunnyvale](https://clickhouse.com/company/events/202504164) \- Sunnyvale \- Apr 16, 2026
- [Google Cloud Next 2026](https://clickhouse.com/company/events/google-cloud-next-2026) \- Las Vegas \- Apr 22, 2026
- [House Party, Google Cloud Next](https://clickhouse.com/company/events/2026-houseparty-google-next) \- Las Vegas \- Apr 22, 2026
- [Sao Paulo 2\-day In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202605-LATAM-SaoPaulo-Real-time-Analytics-w-ClickHouse) \- Sao Paulo \- May 12, 2026
- [Open House](https://clickhouse.com/company/events/202605-global-open-house) \- San Francisco \- May 26, 2026


### Events in EMEA [\#](/blog/202604-newsletter#events-in-emea)


- [Paris In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-EMEA-Paris-Real-time-Analytics-w-ClickHouse) \- Paris \- Apr 15, 2026
- [GrafanaCON](https://grafana.com/events/grafanacon/) \- Barcelona \- Apr 20\-22, 2026
- [Barcelona In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-EMEA-Barcelona-Real-time-Analytics-w-ClickHouse) \- Barcelona \- Apr 20, 2026
- [AWS Summit London](https://aws.amazon.com/events/summits/london/) \- London \- Apr 22 \- Booth G18
- [Rise of AI Berlin](https://riseof.ai/conference-2026/) \- Berlin \- May 5\-6, 2026
- [AWS Summit Tel Aviv](https://aws.amazon.com/events/summits/tel-aviv/) \- Tel Aviv \- May 6, 2026
- [Data Innovation Summit](https://datainnovationsummit.com/) \- Stockholm \- May 6\-8, 2026
- [Gartner Data \& Analytics](http://gartner.com/en/data-analytics) \- London \- May 11\-13, 2026
- [Revolution Banking](https://www.revolutionbanking.es/) \- Madrid \- May 12, 2026
- [London 2\-day In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202605-EMEA-London-Real-time-Analytics-w-ClickHouse) \- London \- May 19, 2026
- [ClickHouse Meetup London](https://www.meetup.com/clickhouse-london-user-group/events/313759007/) \- London \- May 19, 2026
- [Platforma 2026](https://www.platfor-ma.com/) \- Tel Aviv \- May 20, 2026
- [AWS Summit Hamburg](https://aws.amazon.com/events/summits/hamburg/) \- Hamburg \- May 20, 2026
- [Google Summit Madrid](https://cloudonair.withgoogle.com/events/cloud-ai-live-madrid-2026) \- Madrid \- May 28, 2026


### Events in APAC [\#](/blog/202604-newsletter#events-in-apac)


- [Data Streaming World Tour \- Mumbai](https://clickhouse.com/company/events/202604-APJ-3P-Mumbai-ConfluentStreamingTour) \- Apr 13, 2026
- [Taiwan In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-APJ-Taiwan-Real-time-Analytics-with-ClickHouse) \- Taiwan \- Apr 16, 2026
- [Taipei Open Source Meetup](https://clickhouse.com/company/events/taipei-open-source-meetup) \- Taipei \- Apr 16, 2026
- [Data Streaming World Tour \- Bangalore](https://clickhouse.com/company/events/202604-APJ-3P-Bangalore-ConfluentStreamingTour) \- Apr 16, 2026
- [PagerDuty on Tour Tokyo](https://clickhouse.com/company/events/202604-APJ-3P-Tokyo-PagerDutyTour) \- Tokyo \- Apr 16, 2026
- [Bangalore Meetup with Alexey Milovidov](https://www.meetup.com/clickhouse-bangalore-user-group/events/313739871/) \- Apr 18, 2026
- [Data Streaming World Tour \- Jakarta](https://clickhouse.com/company/events/202604-APJ-3P-Jakarta-ConfluentStreamingTour) \- Apr 21, 2026
- [Ho Chi Minh In\-Person Training: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202604-APJ-HoChiMinh-Real-time-Analytics-with-ClickHouse) \- Ho Chi Minh \- Apr 22, 2026
- [AWS Summit Bengaluru](https://aws.amazon.com/events/summits/bengaluru/) \- Apr 22\-23, 2026
- [Microsoft AI Tour \- Sydney](https://clickhouse.com/company/events/202604-APJ-3P-Sydney-MicrosoftAITour) \- Apr 23, 2026
- [AWS Summit Singapore](https://clickhouse.com/company/events/202605-APJ-3P-Singapore-AWSSummit) \- Singapore \- May 6, 2026
- [AWS Summit Sydney](https://clickhouse.com/company/events/202605-APJ-AWSSummit-Sydney) \- Sydney \- May 13, 2026
- [Data Engineering Summit](https://clickhouse.com/company/events/202605-APJ-3P-Bangalore-DataEngineeringSummit) \- Bangalore \- May 14, 2026
- [AWS Summit Seoul](https://clickhouse.com/company/events/202605-APJ-3P-Seoul-AWSSummit) \- Seoul \- May 20, 2026
- [Findy VPoE Summit](https://clickhouse.com/company/events/202605-APJ-3P-Tokyo-FindyVPoESummit) \- Tokyo \- May 22, 2026
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-395-get-started-today-sign-up&utm_blogctaid=395)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
