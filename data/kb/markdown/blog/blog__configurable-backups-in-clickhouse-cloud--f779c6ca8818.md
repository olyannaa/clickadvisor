# Configurable Backups in ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Configurable Backups in ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U05_ARHHQT_7_U_d759fe8fcc74_512_b2a5bc4535.jpg&w=96&q=75)[Aashish Kohli](/authors/aashish-kohli)May 15, 2024 · 5 minutes read[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. To learn more about our volume\-based discounts, [contact us](/company/contact?loc=blog-cta-header) or visit our [pricing page](/pricing?loc=blog-cta-header).

## Introduction [\#](/blog/configurable-backups-in-clickhouse-cloud#introduction)



We’re excited to announce configurable backup controls are now available in ClickHouse Cloud in private preview.




The ability to take backups of your data is table stakes for any database offering. Backups provide a safety net by ensuring that if data is lost for any unforeseen reason \- whether it be accidental deletion, corruption, and so on \- the service can be restored to the previous state of the last successful backup. This minimizes downtime and prevents business\-critical data from being permanently lost. Backups are critical to any disaster recovery (DR) plan by ensuring that the business can quickly recover from disruptive events, maintain continuity, and resume normal operations, thus minimizing financial and reputational impact. Additionally, backups also help enterprises satisfy their compliance and legal requirements around data retention and are evidence that they have policies in place to prevent loss of data.



## How it works [\#](/blog/configurable-backups-in-clickhouse-cloud#how-it-works)



All ClickHouse Cloud services come with default backup policies. For Production services, backups are taken daily and retained for two days. This ensures that if data is lost for any unforeseen reason, the service can be restored to the last successful backup. Backups are a combination of full and incremental backups that constitute a sequence of backups utilized together to restore data to a new service if needed.




ClickHouse Cloud default backups (with a 24\-hour backup frequency, and 48\-hour retention) satisfy the business needs for some customers. However, certain customers need the additional ability to take backups more frequently and retain them for a longer duration to meet their Business Continuity, or in some cases, compliance requirements. 




Additionally, some customers prefer that backups happen at a certain time during the day. This prevents the backup process from competing with compute resources allocated to the service during critical hours, and importantly, it gives customers control over the backups being taken at a time when most of their daily data changes have been committed.




To address these needs, we are making our backup process more flexible by giving customers the ability to configure the start time, retention, and frequency for backups of their Production and Dedicated tier services. We will continue to provide the two default backups at no cost. However, changes to the backups schedule that require retention for a longer duration, or more frequent backups that require additional copies of the data to be retained, may incur additional charges.



## Let’s walk through an example [\#](/blog/configurable-backups-in-clickhouse-cloud#lets-walk-through-an-example)



To configure backups for your service and set the schedule to be different from the default, go to the service settings page and navigate to the **Backups** section. Click the “Change backup configuration.”






![1conf.png](/uploads/1conf_634d82f134.png)


The **Backup configuration** page lets you modify the retention, frequency, or start time of the backups for your service. You can choose any start time over a 24\-hour window, and backups will start within an hour of the scheduled time. Backups can be set up to happen as frequently as every 6 hours, and as infrequently as every 24 hours, with several intermediate values supported within that range. Retention ranges from 1 day and goes up to 30 days, which refers to the ability to roll back to a certain point in time.






![2conf.png](/uploads/2conf_d03c87f980.png)


**NOTE:** Frequency and start time (Scheduled) are mutually exclusive settings for backups. For example, if you select 2 AM UTC as the start time for your backups, you won’t be able to simultaneously set a frequency of backing up the data every 6 hours.



**Available backups, usage, and cost**


All available backups for your service are displayed on the backups page in the Cloud Console. In the example below, backups have been configured to happen every 6 hours, with a 5\-day retention. From here (under Actions) you can also select a particular backup and choose to restore it to a new service. Details of restoring a backup to a service are covered in our [public docs](https://clickhouse.com/docs/en/manage/backups).






![3conf.png](/uploads/3conf_4cd7309f93.png)


To understand the cost impact of your backup configuration, you can look at the usage breakdown for your service under the “Organization” section on the Cloud Console. If there are costs associated with the backup configuration you’ve selected, they will be displayed on this page under the column “Backups.”






![unnamed.png](/uploads/unnamed_a38262a70a.png)

## Looking ahead [\#](/blog/configurable-backups-in-clickhouse-cloud#looking-ahead)



We plan to make ClickHouse Cloud backups even more seamless and flexible. We will soon enable on\-demand backups, so you can kick off a backup at any point in time from the UI, or programmatically via APIs.




We will also soon support the ability to export backups cross\-region. This gives you the ability to fulfill your DR (disaster recovery) requirements in situations where the primary region has an interruption in service. 




Additionally, we are looking to enable the capability to export backups to your own cloud service account. This will allow for more control over the backup lifecycle, as well as data retention for data residency or other compliance purposes.




Finally, in the coming months, we also plan to improve our backup capability to support continuous backups and point\-in\-time restores (PITR). This will make it possible to have even more granular [RPO](https://www.druva.com/glossary/what-is-a-recovery-point-objective-definition-and-related-faqs) for data stored in ClickHouse Cloud.


[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
