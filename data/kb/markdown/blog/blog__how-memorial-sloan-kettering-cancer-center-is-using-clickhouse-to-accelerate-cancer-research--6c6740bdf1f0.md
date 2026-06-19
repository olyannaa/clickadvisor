# How Memorial Sloan Kettering Cancer Center is using ClickHouse to accelerate cancer research


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Memorial Sloan Kettering Cancer Center is using ClickHouse to accelerate cancer research

![](/_next/image?url=%2Fuploads%2Faaron_lisman_017d944d10.jpg&w=96&q=75)Aaron LismanFeb 6, 2025 · 7 minutes read[Memorial Sloan Kettering Cancer Center (MSK)](https://www.mskcc.org/), one of the world's top cancer research and treatment institutions, is known for pushing the boundaries of precision oncology. In 2011, it launched [cBioPortal](https://www.cbioportal.org/), an open\-source platform that makes exploring complex cancer data easier and more accessible. Today, cBioPortal provides researchers all over the world with insights that drive breakthroughs in cancer treatment and personalized care.


Over time, however, as cBioPortal grew to support hundreds of thousands of patient records, its performance started to lag. The platform's reliance on MySQL meant long delays when users filtered or analyzed data. Its architecture wasn't designed for the scale or complexity of modern cancer genomics; as a result, researchers struggled to explore data quickly, slowing down the hypothesis testing and pattern discovery that cBioPortal was built to enable.


"More performance in our application means more insight," says Aaron Lisman, lead software engineer on cBioPortal. "If it's sluggish, people won't use it to test hypotheses. But if it's fast and responsive, they will, and that will lead to more insights and faster progress."


At a [December 2024 ClickHouse meetup in New York City](https://www.youtube.com/watch?v=vrTp3rj0oTk), Aaron shared how MSK turned to ClickHouse to make cBioPortal faster and more scalable — improvements that will help researchers around the world analyze data faster and accelerate cancer research.


## Decoding the mystery of cancer [\#](/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research#decoding-the-mystery-of-cancer)


MSK launched cBioPortal in 2011 to make sense of the growing flood of genomic data driven by advances in DNA sequencing. Initially developed for MSK's own research, the platform quickly grew into an open\-source project supported by leading institutions worldwide, including Dana\-Farber, MD Anderson, Children's Hospital of Philadelphia, and others.


Cancer, at its core, is a disease of the genome. Mutations in DNA, often caused by factors like smoking or sun exposure, disrupt the body's ability to control tissue growth, leading to tumors. With cBioPortal, researchers can analyze these mutations across large cohorts of patients, identifying patterns that reveal how different types of cancer develop and behave.


"Reading this data lets us peer into the root cause of cancer and see biological pathways that are worthy of inquiry," Aaron explains. "Because the mutations are the root cause, we can develop treatments and target them much more specifically and intelligently."


The platform's filtering and visualization tools make complex genomic data more accessible. For example, cBioPortal makes it possible to explore how specific genetic changes — such as mutations in the TP53 gene, a key regulator for DNA damage repair — affect survival rates or treatment outcomes. By transforming raw data into actionable insights, Aaron and his team are helping to advance global cancer research and improve patient care worldwide.


## Cracking the data bottleneck [\#](/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research#cracking-the-data-bottleneck)


Over the past 15 years, the scale of cBioPortal's data has grown dramatically. Today, the platform supports over 140,000 patient records in its internal MSK instance, plus an additional 220,000 records in external databases such as the GENIE consortium. The human genome, meanwhile, consists of around 22,000 genes, with RNA expression data from patient records generating billions of rows. Altogether, these datasets add up to over 4 billion data points. "Our ultimate goal is to support 1 million patients with multiple samples," Aaron says.


This increasing scale, however, took its toll on cBioPortal's old data infrastructure, causing it to become "extremely slow." The MySQL\-based architecture, designed for Online Transaction Processing (OLTP), struggled with the portal's complex analytical queries. Filtering or analyzing patient cohorts often required bringing entire datasets into memory just to filter and count them in Java. "You would have a researcher waiting a minute or more to see the results of their filtering," Aaron says. "We were embarrassed as developers."


Reflecting on the old setup, he adds, "We were doing much too much work in our service layer, exchanging performance for what I call 'developer ergonomics.' It felt easier to do things that way, but what we realized was that it was very unperformant at scale."


As more institutions adopted cBioPortal and contributed genomic and clinical datasets, the MSK team recognized that their OLTP architecture couldn't meet the demands of modern cancer genomics. "We knew we had to do something about this," Aaron says.


## Solving the problem with ClickHouse [\#](/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research#solving-the-problem-with-clickhouse)


In their search for a better database, the cBioPortal team understood that they first needed to find the right solution. "We realized that for doing analytical queries, we should be using an analytical database," Aaron says. "That's how we found ClickHouse."


As Aaron explains, the MSK team chose ClickHouse for its ability to process massive datasets at blazing speed, thanks to its columnar storage and distributed architecture. As an [Online Analytical Processing (OLAP) database](https://clickhouse.com/docs/en/faq/general/olap), ClickHouse is purpose\-built to handle complex analytical queries, making it the ideal choice for cBioPortal's growing needs.


Their first step was proving the concept. "We wanted to get right to business, proving that the optimization concept was viable and reimplementing all of this filtering logic in SQL," Aaron says. Over a six\-month period, the team rebuilt 20 endpoints that filter patients and samples, designing a denormalized schema in ClickHouse tailored to the endpoints' needs. They also used Sling to copy the MySQL schema into ClickHouse for rapid prototyping.


Their mantra during the POC was: "Do not return voluminous data to the web server — keep it in the database and process it there." This led them to create deeply nested SQL queries to push complex filtering and processing directly into ClickHouse. While MyBatis helped structure and modularize their SQL queries, testing and debugging remained a challenge. "A lot of times, when you need to debug something, you just need the whole query," Aaron explains. Without the function\-level unit testing available in Java, the team relied on integration testing with live databases to validate their logic and ensure system performance.


![clickhouse_legacy.png](/uploads/clickhouse_legacy_ab317e58d9.png)
These efforts paid off. By centralizing logic within ClickHouse and optimizing their approach, the team achieved "incredible performance gains" and made queries "10 times faster," Aaron says. The success of the POC showed ClickHouse's potential to transform cBioPortal, supporting near\-real\-time hypothesis testing and accelerating the pace of discovery.


## Scaling cancer research to new heights [\#](/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research#scaling-cancer-research-to-new-heights)


Modern cancer research demands tools capable of keeping pace with the field's growing complexity. With ClickHouse powering key parts of cBioPortal, researchers have a platform that can handle vast amounts of genomic and clinical data with greater speed and efficiency.


"We've proven that the optimization works," Aaron says, noting that Clickhouse is now in production on cBioPortal's internal portals. "In the next few months, we'll be rolling it out to all the many people around the world who use cBioPortal locally at their institutions."


The team is also planning to fully transition the platform's remaining functionalities to ClickHouse, consolidating their data infrastructure and resolving lingering technical challenges like custom binning logic. This will eliminate the need for multiple databases, simplify cBioPortal's architecture, and deliver new and improved capabilities.


As genomic data continues to grow in volume and complexity, the implementation of ClickHouse will ensure that cBioPortal remains a critical tool for researchers across the globe. With their continued focus on innovation and optimization, Aaron and the MSK team are paving the way for even bigger breakthroughs in cancer research.


To learn more about ClickHouse and see how it can improve the speed and scalability of your team's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
