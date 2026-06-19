# ClickHouse Cloud is now Generally Available


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud is now Generally Available

![TanyaBragin.jpeg](/_next/image?url=%2Fuploads%2FTanya_Bragin_84bf5232c3.jpeg&w=96&q=75)[Tanya Bragin](/authors/tanya-bragin)Dec 6, 2022 · 9 minutes read![ClickHouse_Cloud_GA.png](/uploads/Click_House_Cloud_GA_6fa98fbc13.png)
It’s the time of year where many of us start thinking about holiday gift\-giving and look ahead to our New Years’ resolutions, and here at ClickHouse we are no different! This year, our gift to you is to let you know that ClickHouse Cloud is Generally Available, and our never\-ending resolution will always be to build the world’s fastest database with the best possible experience for our community and customers.


Before we talk about all of the goodness available in GA, let’s take a look back — in April, we launched a private preview of ClickHouse Cloud, which progressed to our public beta [announcement](https://clickhouse.com/blog/clickhouse-cloud-public-beta) in October. It is thanks to the thousands of users who tried the service and gave us feedback that we’re able to now progress to General Availability. If you haven’t had a chance to try ClickHouse Cloud yet — **you can start a [30\-day trial](https://clickhouse.cloud/signUp?loc=blog) with $300 in free credits to explore the service.**


ClickHouse Cloud makes it simple to use ClickHouse to get the insights you need at incredible speed and scale. Its serverless architecture, powered by a separated storage and compute engine, makes the most efficient use of resources to deliver robust, secure, and scalable performance that adapts to the needs of your workload: no sizing upfront, no rebalancing later, and no resources sit idle as your environment auto\-scales with your usage.


ClickHouse Cloud is fully production\-ready. It is SOC 2 Type II compliant, offers uptime SLAs, and is available in the AWS Marketplace. But we haven’t forgotten about the millions of developers who are looking to experiment and grow — we have also launched services that are purpose\-built for your starter projects. And that’s not all: we’ve added a cloud\-native SQL console for ClickHouse and many other delightful features for both experienced and new users.


Check out the details below!


## SOC 2 Type II compliance [\#](/blog/clickhouse-cloud-generally-available#soc-2-type-ii-compliance)


Security is a top priority here at ClickHouse, and we’ve been working hard to achieve SOC 2 Type II compliance for GA.


This certification demonstrates that we conform to industry standards with regard to security, availability, data processing integrity, and confidentiality. We have always treated your services with the utmost attention and care, but now you can have the peace of mind knowing that independent auditors agree. For more on what this entails, check out our recent [blog post](https://clickhouse.com/blog/clickhouse-cloud-is-now-soc-2-type-ii-compliant) on this subject.


As part of our ongoing commitment to security, we have also launched our [Trust Center](http://trust.clickhouse.com). This is the place to go when you want to dig deeper into our security posture and the various documentation around it.


![GA_trust_center.png](/uploads/GA_trust_center_0ce4694f2d.png)
## Uptime status and SLAs [\#](/blog/clickhouse-cloud-generally-available#uptime-status-and-slas)


It doesn’t matter if your service is secure, if it is down or unreliable. We know that availability and reliability is one of the most important considerations in choosing a cloud service. As a part of GA, ClickHouse Cloud now has a [public status page](https://status.clickhouse.com/). It was important for us to be transparent about the quality and reliability of our service. The status page shows regional availability and incidents (both current and historical), and supports the ability for users to subscribe to alerts on any service disruptions.


Of course, nobody wants to experience a disruption at all, and so ClickHouse also provides an uptime SLA for users running production workloads on ClickHouse Cloud. Please [contact us](/company/contact) to learn more about our SLA policy.


![GA_status_page.png](/uploads/GA_status_page_bb51b6d9e0.png)
\#\#Available in the AWS Marketplace


We know many users rely on the AWS Marketplace to reduce friction between their services and to streamline their billing. We are delighted to share that as part of our GA release, ClickHouse Cloud is also available on the AWS Marketplace.


To get started, go to the [ClickHouse Cloud AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-jettukeanwrfc). When you subscribe to the AWS Marketplace, you get $300 in free credits towards your usage.


![GA_aws_marketplace.png](/uploads/GA_aws_marketplace_8f4c0a08f3.png)
## Development and Production Services designed for your use case [\#](/blog/clickhouse-cloud-generally-available#development-and-production-services-designed-for-your-use-case)


ClickHouse Cloud is always deployed in a redundant manner to ensure that your analytical data is highly available and secure. We run a typical production\-level service across three availability zones and take care to ensure high availability during auto\-scaling, idle/resume, and ClickHouse version upgrade operations.


However, we recognize that for some use cases, users are looking for simplified services that are more cost\-effective. In addition to robust production\-level services, the GA release introduces Development services – still highly available and redundant, but fixed\-capacity, deployed on leaner hardware and across two availability zones instead of three.


Development services cost less than $200/mo for the most widely used AWS regions, and a lot less for intermittent development workloads that are automatically idled by ClickHouse Cloud. With this new offering, ClickHouse Cloud users can now much more effectively architect, model, and experiment with ClickHouse Cloud until they are ready to deploy the solution in production.


Check out our [pricing page](https://clickhouse.com/pricing) or simply spin up a Development service in your cloud console to find out more.


![GA_dev_pricing.png](/uploads/GA_dev_pricing_7082cab390.png)
## Interactive SQL console for ClickHouse Cloud users [\#](/blog/clickhouse-cloud-generally-available#interactive-sql-console-for-clickhouse-cloud-users)


ClickHouse has a great command\-line client used and loved by many. However, we know that many users prefer to use a GUI instead of a terminal.


For the ClickHouse Cloud GA release, we are also launching the new SQL console, a fully\-featured workbench for ClickHouse Cloud. This UI enables database schema browsing, interactive SQL queries, auto\-complete, query history and sharing, basic visualizations, and more!


The new SQL console makes it easy to learn, manage, and use ClickHouse all from your web browser.


![GA_sql_console.png](/uploads/GA_sql_console_4ea474d5a1.png)
## ClickHouse Academy [\#](/blog/clickhouse-cloud-generally-available#clickhouse-academy)


In the spirit of helping even more users learn how to use ClickHouse to unlock the potential of their analytical datasets, we are launching ClickHouse Academy, a self\-paced learning center for ClickHouse. This offering includes courses that are available for free to everyone.


Visit the ClickHouse Academy [catalog](http://learn.clickhouse.com/visitor_class_catalog) to view our free on\-demand courses, and also recordings of previous live deliveries of our onboarding workshops.


![GA_academy.png](/uploads/GA_academy_c379fc9a73.png)
## New and improved integrations [\#](/blog/clickhouse-cloud-generally-available#new-and-improved-integrations)


We launched a curated listing of cloud\-native integrations in Beta, and expanded it in GA.


Most notably, we now have the following new integrations:


- The official [clickhouse\-kafka\-connect](https://github.com/ClickHouse/clickhouse-kafka-connect) sink is now in Beta
- We’ve launched [Metabase](https://clickhouse.com/docs/en/connect-a-ui/metabase-and-clickhouse/) and [Tableau](https://clickhouse.com/docs/en/connect-a-ui/tableau-and-clickhouse/) connectors for BI use cases
- A [HEX](https://hex.tech/integrations/clickhouse) connector for data scientists
- An official [Javascript language client](https://clickhouse.com/docs/en/integrations/language-clients/nodejs/), compatible with Node.js
- Native support for a community [C\# language client](https://github.com/DarkWanderer/ClickHouse.Client/wiki/Quick-start)


In addition to new integrations listed, we also improved ClickHouse Cloud support for most of our core and partner integrations including Airbyte, DBT, Python, Superset and Grafana. Finally, we have also improved the integrations UI for easier navigation, metadata display, and related content listings.


![GA_integrations.png](/uploads/GA_integrations_7dc5bbf6c8.png)
## PostgreSQL and MySQL engines, dictionaries, and SQL UDFs [\#](/blog/clickhouse-cloud-generally-available#postgresql-and-mysql-engines-dictionaries-and-sql-udfs)


We upgrade your ClickHouse services automatically to the latest release version with no downtime or disruptions. ClickHouse Cloud is currently running 22\.11, so be sure to check out the latest features announced in the [last release](https://clickhouse.com/blog/clickhouse-release-22-11), such as support for Apache Hudi and Delta Lake.


However, some features previously released in open\-source ClickHouse are not yet available for self\-service usage in ClickHouse Cloud, either because they are experimental or need to be re\-architected in a cloud\-native way.


In Beta, we worked hard to introduce support for three most\-requested ClickHouse features, and are very happy to share that as of GA, you can now use ClickHouse Cloud with support for:


- [PostgreSQL](https://clickhouse.com/docs/en/engines/database-engines/postgresql) and [MySQL](https://clickhouse.com/docs/en/engines/database-engines/mysql) integration engines for federated queries
- [Local and HTTP dictionaries](https://clickhouse.com/docs/en/sql-reference/statements/create/dictionary) for fast data lookups at query time
- [SQL user\-defined functions](https://clickhouse.com/docs/en/sql-reference/statements/create/function) (or UDFs) for complex analytical queries


And more improvements are on the way! So, check our [Cloud Compatibility](https://clickhouse.com/docs/en/whats-new/cloud-compatibility/) documentation to learn more.


## Many other improvements [\#](/blog/clickhouse-cloud-generally-available#many-other-improvements)


We would like to thank everyone that tried out the ClickHouse Cloud service in Beta and engaged with us to share feedback. We have carefully reviewed all of your suggestions, already started to make improvements, and will continue to listen to your feedback as we iterate on our offering post GA.


See highlights of the feedback we addressed, and check out [cloud changelog](https://clickhouse.com/docs/en/whats-new/cloud/) for more:


- Introduced multi\-factor authentication in cloud console
- Streamlined auto\-scaling policies
- Improved metering granularity and fidelity
- Tuned pricing dimensions and price points
- Added cloud console navigation for mobile devices
- Introduced services in the Mumbai region


## Try it out for free [\#](/blog/clickhouse-cloud-generally-available#try-it-out-for-free)


To get started with ClickHouse Cloud, sign up [here](https://clickhouse.cloud/signUp?loc=blog) for a 30\-day free trial.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
