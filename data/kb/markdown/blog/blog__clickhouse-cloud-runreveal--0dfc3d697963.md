# How our security team uses ClickHouse Cloud \+ RunReveal


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How our security team uses ClickHouse Cloud \+ RunReveal

![](/_next/image?url=%2Fuploads%2Fjulio_223fe1a141.png&w=96&q=75)Julio Jimenez \& Evan JohnsonSep 25, 2024 · 8 minutes read## Introduction [\#](/blog/clickhouse-cloud-runreveal#introduction)


Security logging is a fundamental component of ClickHouse’s robust enterprise security program. It involves the systematic collection, storage, and analysis of log data from various systems, applications, and devices within the organization's IT environment. These logs provide a chronological record of activities, which is essential for monitoring, detecting, and responding to security incidents or general troubleshooting inquiries.


## ClickHouse as a SIEM (CHaaS?) [\#](/blog/clickhouse-cloud-runreveal#clickhouse-as-a-siem-chaas)


Choosing ClickHouse as the underlying technology for [security information and event management (SIEM)](https://clickhouse.com/engineering-resources/siem) was an obvious choice for the ClickHouse security team.


- Our team already has basic to intermediate knowledge of ClickHouse.
- ClickHouse supports any data format from any of our security log sources.
- Alerts and visualizations are made possible by the official ClickHouse Grafana Plugin.
- The enormous scale of many security logs means we needed a solution which would effectively compress logs while preserving fast query access times, thus allowing us to respond to security incidents quickly and efficiently. We knew that ClickHouse, from both [internal](https://.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog) and [external use cases](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse/?glxid=221f642c-dad8-4e0f-a197-cbe5d6666984&pagePath=%2Fuser-stories&origPath=%2Fblog%2Fbuilding-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog/), is an excellent storage engine for this data and would meet these requirements.
- As a managed ClickHouse offering, ClickHouse Cloud as a SIEM is a low headache solution that is faster and more reliable than traditional SIEMs.
- As with our community and customers, quick online support is just a click away.


With a strong set of customer references, including Temporal and Lumos, testifying as to their ease of use, deployment and cost effectiveness, we were convinced RunReveal with ClickHouse would address our existing challenges and be the perfect combination.



> “RunReveal \[powered by ClickHouse] enabled Temporal to get up and running quickly with a solution that easily scales with our data size, and aligns with similar tooling used elsewhere in our observability stack. This allows us to focus on writing detections and automating our responses”
> 
> 
> Dave Green, Security Engineer @ Temporal


## Legacy ETL [\#](/blog/clickhouse-cloud-runreveal#legacy-etl)


Our original architecture using ClickHouse Cloud as an SIEM consisted of creating explicit ETL (Extract Transform Load) lambda functions from each data source to ClickHouse, as shown in the following image.


![runreveal_arch.jpg](/uploads/runreveal_arch_5403c8ce36.jpg)
Each function was unique to the data source being extracted and loaded to ClickHouse, and as one can quickly discern from this diagram. As a result, scaling up the number of data sources had a proportional impact on costs and engineering complexity. While Lambda functions had the benefit of being scalable and quick to set up, but they quickly became unwieldy and difficult to maintain. Adding new data sources was not a turnkey process, as the data that was collected wasn’t consistently normalized. This made developing good detections an exercise in threat modeling in its own right.


Despite the ClickHouse Cloud service never being a bottleneck, we needed a different solution to collect and normalize logs if we wanted to be able to focus on detections.


## Enter RunReveal [\#](/blog/clickhouse-cloud-runreveal#enter-runreveal)


RunReveal is a security data platform designed to collect raw logs from SaaS and Cloud Services, ingest them into ClickHouse Cloud, and automatically detect anomalies and compromises in your environment. They make collection, detection, enrichment, and search easier than any traditional SIEM while also overcoming the challenges we had with implementing much of the functionality ourselves with lambda functions.


We felt we had found a kindred spirit in our approach to cloud security as soon as we started working with RunReveal. They continue to be a partner who value technical collaboration and view security as data and detection as code.


We migrated our entire in\-house security logging program and added several high\-valued data sources while still in the POC phase. RunReveal’s Destinations feature allowed us to use our own ClickHouse Cloud service, ensuring we have complete ownership of our data.


The most significant mission multiplier for our team was how incredibly easy it was to add new data sources. We went from n \+ many ETL pipelines to a singular and abstracted ingestion engine in RunReveal (ETLaaS?), with health checks and notifications to boot!


![explore_runreveal.png](/uploads/explore_runreveal_1cd7e7c9d9.png)
The ease and speed of deploying new data sources allowed the security team incredible visibility into our infrastructure’s VPC flow logs. To optimize for cost, the team had to maximize the signal\-to\-noise ratio of the network traffic it intended to monitor. This inevitably led to a large number of distinct flow log configurations. This was not a problem with infrastructure\-as\-code and RunReveal.


![runreveal_alerts_sources.jpg](/uploads/runreveal_alerts_sources_e204341544.jpg)
RunReveal made connecting to each individual data source simple, by integrating tightly with each log provider we cared about. When RunReveal integrates with a log source, they normalize the raw logs and enrich the logs with helpful security context making the setup a breeze. RunReveal alerts us if any data sources become unhealthy and keeps track of every byte that we log. Importantly, RunReveal integrates with the tools we care about so we can get alerts in Slack, manage our detections with GitHub, and build out automated responses with Security Orchestration, Automation and Response (SOAR) tools.


## Detections [\#](/blog/clickhouse-cloud-runreveal#detections)


As a data detection platform, the next generation of SIEM, RunReveal is uniquely positioned to outperform competitors that are using slower analytical or OLTP databases. By building on top of ClickHouse, RunReveal is able to exploit its speed advantages as a query engine by exposing SQL through the web UI and the CLI.


Out of the box, RunReveal comes with a large and growing number of detections for all of its supported data sources. Users can view and edit the SQL queries that ultimately run on ClickHouse and make up the detection to better fit their specific requirements.


Using a holistic approach, RunReveal looks across all logs stored in ClickHouse and identifies attack patterns as well as individual signals. We are only notified when something urgent is found, otherwise we receive a daily configurable report.


Detection authoring is just as easy as adding data sources. A detection is written in SQL, and can be created from scratch or from any query in the Explore interface. They can also be generated from other artifacts in the platform, such as Sources. For example, if you have a problematic data source, you can query the errors for that source and create a detection on the fly.


The following was our very first detection used to alert us when an Okta app failed to push a profile to an application. Not exactly 1337c0d3 security stuff, but it has shortened the time it takes to pinpoint and debug access management issues when the root cause is a simple profile push error.


![runreveal_detection.png](/uploads/runreveal_detection_4c6c4a616d.png)
RunReveal’s out\-of\-the\-box detections helped us stand up our security monitoring program quickly and easily, allowing us to focus on building detections that match the security boundaries that are unique to ClickHouse’s business.


To achieve this we are leveraging RunReveal’s correlation functionality to collect and group signals, and beginning to maintain our detections in git with detection as code workflows. ClickHouse Cloud and RunReveal work together seamlessly to manage our security data and operationalize it without headaches.


## Conclusion [\#](/blog/clickhouse-cloud-runreveal#conclusion)


The security applications of ClickHouse may be less well known compared to its observability use cases, yet it has undeniably become a crucial component of our security program. The addition of RunReveal has asserted our path of using ClickHouse in security and has improved how we work with logs and detections in a scalable manner. The security team at Lumos captures our experience with RunReveal perfectly.



> “RunReveal \[on ClickHouse] has been instrumental in allowing our small security team to easily create actionable detections across our entire infrastructure and SaaS stack”
> 
> 
> Ethan Houston, Senior Security Engineer @ Lumos

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
