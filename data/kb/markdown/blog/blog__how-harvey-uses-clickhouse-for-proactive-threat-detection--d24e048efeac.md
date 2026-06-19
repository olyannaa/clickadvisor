# One step ahead: How Harvey uses ClickHouse for proactive threat detection


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# One step ahead: How Harvey uses ClickHouse for proactive threat detection

![](/_next/image?url=%2Fuploads%2Fmike_paroswski_6b41517e96.jpg&w=96&q=75)Mike ParowskiMar 24, 2025 · 7 minutes readThe legal industry is notorious for highly manual, labor\-intensive tasks: contract analysis, due diligence, litigation support, regulatory compliance. [Harvey](https://www.harvey.ai/) is a generative AI platform that builds custom LLMs to help law firms automate these workflows, improving efficiency and productivity while allowing lawyers to focus on more complex, high\-value work.


But revolutionizing the legal profession isn’t just about streamlining processes \- it’s also about protecting sensitive client information. When Mike Parowski joined Harvey as the company’s first detection and response (D\&R) hire in April of 2024, he saw the need for a proactive approach to threat detection that could keep client data secure from network threats.


At a [recent meetup in San Francisco](https://www.youtube.com/watch?v=9E2_35TAPGQ), Mike broke down how Harvey’s security team is using network logs for scalable, efficient threat detection \- and how [ClickHouse Cloud](https://clickhouse.com/cloud) is helping Harvey and its customers stay ahead of potential security risks.



## Data overload [\#](/blog/how-harvey-uses-clickhouse-for-proactive-threat-detection#data-overload)


In the world of D\&R, there’s what Mike calls a "standard paradigm," where network logs are viewed as secondary tools — used retrospectively to investigate security incidents. Usually, after an alert from an endpoint detection and response (EDR) system, security teams dig into network logs to uncover the source of the problem.


"I challenge that notion" Mike says. "Not only can network logs be effective primary indicators of compromise, but they may actually beat host EDRs to the punch."


But harnessing network logs for proactive threat detection isn’t always easy. Upon joining Harvey, Mike’s first challenge was managing its massive volume of network data. The platform, powered by Azure NSG flow logs, produces 5\.4 TB of data daily, spanning 1\.5 million unique IP addresses and up to 40 million rows. As Mike notes, "We expect this data to grow proportional to our customer base \- so as Harvey gets more customers, this data will only go up."


Processing this volume in real time was challenging because the logs were stored in "block blob" format, which forced the team to traverse huge chunks of raw data before they could run meaningful queries. Each minute generated hundreds of thousands of log entries for just one service, resulting in a complex web of file paths that had to be navigated.


"At this volume, doing any sort of aggregate statistics and proactive detection becomes nearly impossible," Mike explains. Queries designed to identify potential threats, such as top talkers or traffic anomalies, were difficult to execute. "We just consistently met with timeouts or out\-of\-memory errors, no matter how hard we tried" he says.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## A more scalable solution [\#](/blog/how-harvey-uses-clickhouse-for-proactive-threat-detection#a-more-scalable-solution)


To overcome these challenges, the Harvey AI team turned to [ClickHouse Cloud](https://clickhouse.com/cloud) and partnered with [RunReveal](https://runreveal.com/), a security analytics platform built on ClickHouse. The combination of ClickHouse’s high\-performance columnar database and RunReveal’s expertise allowed Harvey to completely restructure their approach to processing network logs.


As Mike explains, their optimization strategy involved selecting [primary indexes](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes) for key data points \- source IPs, destination IPs, and destination ports \- and using [materialized views](https://clickhouse.com/docs/en/materialized-view) to pre\-compute aggregations. "By really understanding how we would use these logs, and by understanding the domain itself, we could carefully select the indexes we’d use in the materialized views to drive those efficiency gains," he says.


This approach has allowed the team to better track and compare network activity over time. "Combining these fields lets us effectively answer the question of who is doing what, and gives us quantifiable metrics to compare today to yesterday to the day before" Mike adds.


Along with improving query efficiency, ClickHouse's “compression capabilities (which Mike calls "absolutely nuts") played a key role. The 5\.4 TB of daily log data was compressed down to just 4\.55 GB, reducing the data footprint and enabling faster, real\-time processing. "I don’t know if anyone else besides ClickHouse could get us those numbers" Mike says.


With this new architecture in place, Harvey’s security team can run complex queries on network traffic patterns, detect anomalies, and proactively detect threats \- capabilities that would have been impossible before.


## Enrichment for better insights [\#](/blog/how-harvey-uses-clickhouse-for-proactive-threat-detection#enrichment-for-better-insights)


Beyond simply optimizing data storage and querying, the Harvey team has taken further steps to enrich their network logs with more meaningful, human\-readable labels. Tapping into the flexibility of ClickHouse’s query capabilities, they’ve mapped raw IP addresses to recognizable names, making it easier to understand network activity in real time.


"I was actually surprised by how seamlessly this worked with ClickHouse," Mike says. "I’ve tried doing similar enrichment in other systems, but they couldn’t handle the scale or complexity of our data without major slowdowns."


He says the enriched data gives the team a "really clear, high\-level snapshot of what our network looks like and the visibility across Harvey’s environment." By enriching the data, the team can quickly spot suspicious activity, such as unexpected traffic spikes or unusual port activity. The higher level of visibility has allowed the security team to not only monitor their network but also act on anomalies with greater confidence and precision.


This enrichment process has further simplified the task of detecting threats, helping Harvey’s security team move away from sifting through raw, indecipherable logs and focus on key patterns that point to genuine security concerns.


## Real\-time threat detection [\#](/blog/how-harvey-uses-clickhouse-for-proactive-threat-detection#real-time-threat-detection)


In cryptography and cybersecurity, [Alice and Bob](https://en.wikipedia.org/wiki/Alice_and_Bob) are traditionally used as the names of the two parties communicating, while Eve \- shorthand for "evil" or "eavesdropper" \- is the third\-party adversary or hacker trying to listen in or disrupt their communications.



> "On the security team at Harvey, we like to say that if we do our jobs well, and if we protect this perimeter from Evil Eve, we let all the brilliant people at Harvey do their jobs, and at the end of the day, we all get to drink Mai Tais on the beach. ClickHouse helps us do just that."
> 
> Mike Parowski


With the help of ClickHouse Cloud, Harvey has successfully transformed their network threat detection. What once seemed like an overwhelming flood of data is now a manageable, streamlined system capable of running real\-time detections on Harvey’s rapidly expanding network. The improvements in compression and query efficiency mean the team can stay ahead of security threats while maintaining the highest level of data protection.


The impact of these changes goes beyond simply managing data effectively. By optimizing their security operations, Harvey has ensured that their platform can scale securely, giving peace of mind to their internal teams and customers. As Harvey grows, Mike and the team are confident they have the tools to stay ahead of evolving threats, allowing them to focus on their core mission: revolutionizing the legal industry with cutting\-edge AI solutions.


To learn more about ClickHouse and see how it can improve the efficiency and scalability of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
