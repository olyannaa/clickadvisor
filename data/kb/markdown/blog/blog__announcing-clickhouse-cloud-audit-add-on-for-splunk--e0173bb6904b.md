# Announcing ClickHouse Cloud Audit add\-on for Splunk


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing ClickHouse Cloud Audit add\-on for Splunk

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 22, 2025 · 3 minutes readIn an ongoing effort to grow the ClickHouse ecosystem so that it can easily integrate into any environment, we are excited to announce the recent release of the **ClickHouse Cloud Audit add\-on for Splunk**! 


This new integration lets you easily store and analyze ClickHouse Cloud audit logs directly into [Splunk](https://www.splunk.com/), the data analytics and monitoring platform. 


It uses the [ClickHouse Cloud API](https://clickhouse.com/docs/en/cloud/manage/api/api-overview) to securely pull the audit logs from your ClickHouse Cloud organization.  The add\-on is available for download on [Splunkbase](https://splunkbase.splunk.com/app/7709).


![client-only.png](/uploads/splunk_clickhouse_add_on_1_f053ea4218.png)
## Installation and Configuration [\#](/blog/announcing-clickhouse-cloud-audit-add-on-for-splunk#installation-and-configuration)


Installing the add\-on on your Splunk deployment is straightforward and requires only a few steps. Currently, only Splunk Enterprise deployment is supported. Approval for the Splunk Cloud availability is pending.


1. Download and Install:


- Download the ClickHouse Cloud Audit Add\-on for Splunk from [Splunkbase](https://splunkbase.splunk.com/app/7709).
- In Splunk Enterprise, navigate to Apps \> Manage, click Install app from file, and upload the downloaded file.


2. Gather ClickHouse Cloud Information:


- Log in to your ClickHouse Cloud console.
- Navigate to Organization \> Organization Details to copy your Organization ID.
- Generate an API Key with admin privileges under API Keys and save it securely.


3. Configure Data Input in Splunk:


- Go to Settings \> Data Inputs in Splunk.
- Select ClickHouse Cloud Audit Logs and click New.
- Enter your Organization ID and Admin API Key to complete the setup.


Find a detailed version of the instructions on the [ClickHouse documentation website](https://clickhouse.com/docs/en/integrations/audit-splunk).


## Audit ClickHouse Cloud from Splunk [\#](/blog/announcing-clickhouse-cloud-audit-add-on-for-splunk#audit-clickhouse-cloud-from-splunk)


Once configured, the Cloud organization audit logs start flowing into Splunk and are ready for exploration through Splunk search and analytics tools.


![client-only.png](/uploads/splunk_clickhouse_add_on_2_2f18f68739.png)
  

If you need to centralize audit logs in your Splunk deployment, start using the ClickHouse Cloud Audit Logs for Splunk add\-on today.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
