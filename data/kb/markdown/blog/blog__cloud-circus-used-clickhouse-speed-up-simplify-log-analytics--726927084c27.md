# How Cloud CIRCUS used ClickHouse to speed up and simplify log analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Cloud CIRCUS used ClickHouse to speed up and simplify log analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 17, 2025 · 8 minutes read[Cloud CIRCUS](https://cloudcircus.jp/) is on a mission to make marketers’ lives easier. The Tokyo\-based SaaS company offers a suite of digital tools designed to help businesses across Japan streamline their marketing. One of those tools is [BlueMonkey](https://bluemonkey.jp/), a CMS platform that makes it easy for anyone to build and manage a professional website.


Today, BlueMonkey supports more than 2,000 customer websites on AWS, each with its own CloudFront distribution. That setup keeps content delivery fast, but it also generates tens of millions of access logs every day. These logs are important for tracking errors and understanding user behavior, but querying them with Amazon Athena was slow, expensive, and hard to scale. The team needed a better way to analyze all those logs without running thousands of separate queries or worrying about unpredictable costs.


At a [January 2025 ClickHouse meetup in Tokyo](https://clickhouse.com/videos/tokyo-meetup-cloudcircus-accelerating-cloudfront-log-analysis), infrastructure engineer Kyurin Shu shared Cloud CIRCUS solved the problem by switching to ClickHouse. What started as an experiment turned into a powerful, self\-managed analytics pipeline—one that’s faster, easier to automate, and far more cost\-efficient than what they had before.


## From Athena to ClickHouse [\#](/blog/cloud-circus-used-clickhouse-speed-up-simplify-log-analytics#from-athena-to-clickhouse)


Originally, Cloud CIRCUS used Athena to analyze CloudFront logs stored in S3\. But as BlueMonkey brought on more customers, performance started to fall off. Each customer site had its own CloudFront distribution, generating millions of new log records every day. “Analyzing all logs with Athena was challenging,” Kyurin says. “There were too many CloudFront instances and records. It took too much time and cost too much money.”


One of the biggest pain points was structure. Athena required a separate table for each CloudFront distribution, which made it hard to run queries across all sites. Performance also dragged: pulling in fresh logs could take hours, and even simple queries were slow to return results. On top of that, because Athena charges per query based on the amount of data scanned, costs were both high and unpredictable.


Kyurin and the team began exploring alternatives. “We thought if we could analyze CloudFront logs on our self\-built ClickHouse environment, that would be great,” he says. They were drawn to ClickHouse’s open\-source model and reputation for fast, large\-scale aggregation. Just as important, it offered a way to consolidate all log data into a single table and break free from Athena’s per\-query pricing model.


Still, they didn’t want to jump in blind. “We thought this could solve the issues of speed and cost to some extent,” Kyurin says. “Of course, we also wanted to conduct a technical evaluation to test ClickHouse’s performance.” So they spun up a proof of concept on EC2 and ran some benchmarks. The results were strong enough to move ahead with a full migration.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Building the new system [\#](/blog/cloud-circus-used-clickhouse-speed-up-simplify-log-analytics#building-the-new-system)


The team kept things simple to start. They created a single EC2 instance running Amazon Linux 2023 with 4 vCPUs and 32 GB of memory, and installed ClickHouse using the [official RPM packages](https://clickhouse.com/docs/install#install-from-rpm-packages). “We started with a small server for technical verification and to keep costs down,” Kyurin says. Both the ClickHouse server and client ran on the same machine, making it easy to manage during the early testing phase.


Next came schema design. To maintain consistency, the team mirrored the table structure Athena used for CloudFront logs. “This ensured we got results similar to those from the queries executed by Athena,” Kyurin explains. It also made comparing the two systems easier. One tweak was necessary: Athena stored the HTTP status code as an integer, but because some CloudFront logs include values like “000,” ClickHouse needed that column to be a string. They used the [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) engine, partitioned the data by day, and sorted it by host\_header and date, a setup well\-suited for the aggregate queries they planned to run.


With the table ready, they moved on to importing logs. CloudFront logs were already being delivered to S3, organized into folders by domain. Using ClickHouse’s [s3 table function](https://clickhouse.com/docs/sql-reference/table-functions/s3), they could pull in logs from a specific date range across many files at once, without listing every file manually. To clean up the data during import, they configured ClickHouse to skip the first two header lines and treat placeholder dashes as null values. The setup was simple and fast enough to get their initial data loaded without any issues.


The bigger challenge was scale. “The data volume of logs from all sites is quite large,” Kyurin explains. “Inserting them all at once would take a lot of time.” To automate the process, they built a pipeline using Amazon EventBridge and ECS. A scheduled batch task scans S3, pulls a list of domains, and loads the relevant logs into ClickHouse for each one. “This lets us automate everything,” he says.


![455025117-34c69730-c6e0-491a-998e-7528c66d8561.png](/uploads/455025117_34c69730_c6e0_491a_998e_7528c66d8561_88b403b054.png)
Cloud CIRCUS’s automated log import pipeline: CloudFront logs flow through S3 and ECS into ClickHouse on EC2\.


To speed things up even more, they parallelized the import using AWS Fargate. Logs are split across 20 tasks, each handling a different group of domains. “What used to take several hours to insert all at once now finishes in under 30 minutes,” Kyurin says. To avoid overloading the system, they capped the number of concurrent tasks to keep memory usage below 80%, striking a solid balance between speed and stability.


With the new architecture in place and automation up and running, Cloud CIRCUS now has a streamlined, self\-managed log analytics pipeline that can keep up with their growing traffic. “By systematizing the log insert process, we were able to continuously and efficiently implement repeated log entries,” Kyurin says.


## Faster queries, lower costs [\#](/blog/cloud-circus-used-clickhouse-speed-up-simplify-log-analytics#faster-queries-lower-costs)


Since implementing the new pipeline, Cloud CIRCUS has seen major improvements in query performance. At the Tokyo meetup, Kyurin demoed a daily access count query that took around 16 seconds in Athena, which now returns in just 0\.043 seconds in ClickHouse.


And that was just for one site. When aggregating across all domains, ClickHouse completed the query in under nine seconds, scanning over 470 million rows. In Athena, that same analysis would mean running 2,000\+ separate queries and could take hours to complete.


“In terms of query speed and convenience, ClickHouse is superior,” Kyurin says.


Performance is only part of the story. Another big win is cost control. With Athena, Cloud CIRCUS was billed per query based on the volume of data scanned, making large\-scale analysis expensive and monthly costs tough to predict. With ClickHouse running on a fixed\-size EC2 instance, costs are relatively flat at around $300 per month.


While Athena may seem cheaper at lower query volumes (around $100/month), Kyurin notes, “With ClickHouse, you pay a fixed amount no matter how many queries you run.” In contrast, he adds, “with Athena, the price depends on the number of queries, and running a few additional queries that aggregate all sites can easily exceed the cost of ClickHouse.”


By consolidating logs into a single table, automating ingestion, and running queries locally on ClickHouse, the team has moved from a fragmented, pay\-per\-query setup to a centralized pipeline that’s faster, easier to manage, and built to handle scale.


## Scaling log analysis with ClickHouse [\#](/blog/cloud-circus-used-clickhouse-speed-up-simplify-log-analytics#scaling-log-analysis-with-clickhouse)


For Cloud CIRCUS, adopting ClickHouse has changed how they think about log analysis at scale. “By migrating from Athena to ClickHouse, we’ve been able to save both time and costs,” Kyurin says. “Most importantly, we no longer have to worry about expenses every time we run a query, which is a huge relief.”


With faster queries, predictable costs, and a fully automated pipeline, Kyurin and the team now have a system that can scale with BlueMonkey’s growth and support thousands of customer websites with ease. By simplifying their own data workflows, they’re better equipped to do the same for the marketers and businesses they serve.


To learn more about ClickHouse and see how it can improve the speed and scalability of your team’s data workflows, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
