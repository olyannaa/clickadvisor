# What's new in ClickHouse Cloud: spring 2025 roundup


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What's new in ClickHouse Cloud: spring 2025 roundup

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U02_HHFZ_0874_2cba508d09c4_512_e984252673.png&w=96&q=75)[Mihir Gokhale](/authors/mihir-gokhale)Apr 24, 2025 · 8 minutes read![whast_new_2025.png](/uploads/whast_new_2025_67023db754.png)
If you live in the northern hemisphere, spring is here! As flowers bloom and animals come out of hibernation, we’ve been bringing the power of ClickHouse to ClickHouse Cloud. Over the past few months, we’ve delivered a wave of new features and improvements — all designed to give you the most powerful backend for your real\-time data as you spring into the new season. Here’s a look at what’s new from the [ClickHouse Cloud Changelog](https://clickhouse.com/docs/whats-new/changelog/cloud).


## Bring Your Own Cloud (BYOC) \- now Generally Available for AWS [\#](/blog/whats-new-clickhouse-cloud-spring-2025#bring-your-own-cloud-byoc---now-generally-available-for-aws)


In February, we [introduced a new deployment model](https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws) for ClickHouse by launching Bring Your Own Cloud (BYOC) in GA for AWS. With BYOC, you can deploy ClickHouse Cloud directly into your own AWS account, maintaining full control of your data while we manage the operations. It’s the best of both worlds: the power of ClickHouse with the security and compliance benefits of a single\-tenant environment.


![byoc.png](/uploads/byoc_5942e30172.png)
Learn more about the architecture, onboarding process, and operations about our BYOC offering [here](https://clickhouse.com/blog/building-clickhouse-byoc-on-aws). To request access or add yourself to the waitlist for GCP or Azure, please submit your information [here](https://clickhouse.com/cloud/bring-your-own-cloud).


## Native Postgres Change Data Capture (CDC) \- in public beta [\#](/blog/whats-new-clickhouse-cloud-spring-2025#native-postgres-change-data-capture-cdc---in-public-beta)


After [joining forces with PeerDB](https://clickhouse.com/blog/clickhouse-acquires-peerdb-to-boost-real-time-analytics-with-postgres-cdc-integration), in February we announced the public beta of a native Postgres CDC connector, making it easier than ever to capture and replicate Postgres changes into ClickHouse in near real\-time.



> “ClickPipes for Postgres has made it incredibly easy for us to keep our billing data in Postgres synchronized with ClickHouse for efficient analytics. The CDC experience is blazing fast, ensuring data freshness within seconds while minimizing the load on our production Postgres database. An invaluable solution for seamlessly integrating Postgres with ClickHouse!”
> 
> Mo Abedi, Software Engineer in Billing team, Neon.tech


Learn more about this feature in our [launch blog](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta). During the public beta, if you face issues, have questions, or want to chat with the team working on this feature, please reach out to [db\-integrations\-support@clickhouse.com](mailto:db-integrations-support@clickhouse.com).


## Native MySQL Change Data Capture (CDC) \- in private preview [\#](/blog/whats-new-clickhouse-cloud-spring-2025#native-mysql-change-data-capture-cdc---in-private-preview)


When we launched the Postgres CDC connector, we got overwhelming requests for a similar MySQL connector \- so we developed a ClickHouse native CDC connector purpose built for MySQL which is now in private preview. You can use this connector for both continuous replication and one\-time migration from MySQL, no matter where it's running—whether in the cloud (RDS, Aurora, CloudSQL, Azure, etc.) or on\-premises.


Some key features of this connector include blazing fast backfills during the initial load, continuous replication from MySQL, schema change replication, and more.


Learn more in our [launch blog](https://clickhouse.com/blog/mysql-cdc-connector-clickpipes-private-preview), and sign up for the Private Preview [here](https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector).


## Slack notifications for Cloud events [\#](/blog/whats-new-clickhouse-cloud-spring-2025#slack-notifications-for-cloud-events)


Monitor your ClickHouse Cloud deployment without leaving Slack. ClickHouse Cloud already sends notifications for key events — such as billing, scaling, and ClickPipes. In April, we started allowing users to deliver these notifications directly to your Slack workspace using the ClickHouse Cloud Slack application.


![alert.png](/uploads/alert_b8b6678f95.png)
To get started, admins can configure these notifications via the notification center by specifying slack channels to which notifications should be sent. Learn more [here](https://clickhouse.com/docs/cloud/notifications).


## Monitor ClickHouse with the Resource Utilization Dashboard [\#](/blog/whats-new-clickhouse-cloud-spring-2025#monitor-clickhouse-with-the-resource-utilization-dashboard)


Also in April, we started rolling out a new dashboard to monitor your ClickHouse Cloud deployment without leaving the ClickHouse Cloud console. The new Resource Utilization dashboard gives replica\-level insights into how your cluster is sized, also how much CPU and memory load each replica is experiencing, and how much data is transferred in and out of your service.


We scrape the metrics on this dashboard from [ClickHouse system tables](https://clickhouse.com/docs/operations/system-tables), and serve them via this dashboard to help you diagnose issues of overprovisioned or underprovisioned clusters. For one of our internal ClickHouse Cloud services, we used this dashboard to cut our ClickHouse Cloud costs by 4x!


Questions, comments, or feedback? Reach out to [metrics\-requests@clickhouse.com](mailto:metrics-requests@clickhouse.com).


![resource_util.png](/uploads/resource_util_dc54995e2e.png)
## New region: AWS Middle East (UAE) \- me\-central\-1 [\#](/blog/whats-new-clickhouse-cloud-spring-2025#new-region-aws-middle-east-uae---me-central-1)


In February, we’re announced that ClickHouse Cloud is now available in the AWS Middle East (UAE) region (me\-central\-1\). This expansion helps us better serve customers in the Middle East who require local data residency and low\-latency access. With this expansion, you can now harness the power of ClickHouse in [11 regions on AWS, 4 regions on GCP, and 3 regions on Azure](https://clickhouse.com/docs/cloud/reference/supported-regions). We also support private regions in select geographies, you can find more information or request access [here](https://clickhouse.com/docs/cloud/reference/supported-regions).


## Cross\-Region Private Link \- in public beta [\#](/blog/whats-new-clickhouse-cloud-spring-2025#cross-region-private-link---in-public-beta)


In March, we announced the public Beta of Cross\-Region Private Link \- useful for customers running ClickHouse clusters across multiple AWS regions. This enables secure access between your applications and ClickHouse Cloud, no matter where they live.


Learn more [here](https://clickhouse.com/docs/manage/security/aws-privatelink).


## ClickPipes \- AWS PrivateLink [\#](/blog/whats-new-clickhouse-cloud-spring-2025#clickpipes---aws-privatelink)


Last week, we released the ability to use AWS PrivateLink and ClickPipes to establish secure connectivity between VPCs, AWS services, your on\-premises systems, and ClickHouse Cloud. This can be done without exposing traffic to the public internet while moving data from sources like Postgres, MySQL, and MSK on AWS. It also supports cross\-region access through VPC service endpoints. PrivateLink connectivity set\-up is now fully self\-serve through ClickPipes.


Learn more [here](https://clickhouse.com/docs/integrations/clickpipes/aws-privatelink).


## Usage cost API endpoint [\#](/blog/whats-new-clickhouse-cloud-spring-2025#usage-cost-api-endpoint)


A common ask from users was better monitoring around billing and costs, so in February we started exposing a new API endpoint to allow you to programmatically retrieve usage and cost data for your ClickHouse Cloud organization. Whether you’re building internal dashboards or automating budget tracking, it’s easier than ever to stay on top of your ClickHouse Cloud spend.


![usage_api.png](/uploads/usage_api_225d68d4d9.png)
*Vantage Usage Report showing ClickHouse Cloud usage and costs, powered by the Usage Cost API under the hood.*


## New user roles [\#](/blog/whats-new-clickhouse-cloud-spring-2025#new-user-roles)


We expanded our role\-based access control to give teams more flexibility with access control.


- New Member Role (Organization\-Level): Member is an organization level role that is assigned to SAML SSO users by default and provides sign\-in and profile update capabilities.
- Service\-Level Roles: We also introduced two new roles that can be scoped to services:
	- Service Admin: Full control of assigned services.
	- Service Read Only: View\-only access.


These service roles can be assigned to users who already have a Member, Developer, or Billing Admin role. Refer to [Access control in ClickHouse Cloud](https://clickhouse.com/docs/cloud/security/cloud-access-management/overview) for more information.


## PCI and HIPAA compliance [\#](/blog/whats-new-clickhouse-cloud-spring-2025#pci-and-hipaa-compliance)


Security and compliance are at the core of everything we do. In addition to an already exhaustive list of [security and compliance reports](https://clickhouse.com/docs/cloud/security/security-and-compliance), ClickHouse Cloud began to meet key requirements for PCI DSS and HIPAA in February. If you need to build analytics applications for regulated industries like healthcare and finance, we have you covered. We support PCI and HIPAA in select regions at this time, please refer to the documentation for the list of [supported regions](https://clickhouse.com/docs/cloud/reference/supported-regions#hipaa-compliant-regions). To request access, please review guidelines [here](https://clickhouse.com/docs/cloud/security/security-and-compliance).


## We’re Just getting started: summer is coming [\#](/blog/whats-new-clickhouse-cloud-spring-2025#were-just-getting-started-summer-is-coming)


These updates are part of our commitment to delivering the most powerful, flexible, and user\-friendly ClickHouse backend for your application. As always, we'd love to hear your feedback. You can view the full changelog [here](https://clickhouse.com/docs/whats-new/changelog/cloud), engage with our team directly in our [community Slack](https://clickhousedb.slack.com/ssb/redirect), and [get started with a free trial](https://console.clickhouse.cloud/signUp).


Stay tuned for more.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
