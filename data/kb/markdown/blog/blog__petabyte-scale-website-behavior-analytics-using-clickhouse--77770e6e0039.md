# Seattle Meetup Report: Petabyte\-Scale Website Behavior Analytics using ClickHouse (Microsoft)


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Seattle Meetup Report: Petabyte\-Scale Website Behavior Analytics using ClickHouse (Microsoft)

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jan 18, 2023 · 4 minutes read
  

On January 18th, 2023 Microsoft hosted a ClickHouse community meetup at their office in Redmond. The WebXT team presented two of their analytics products using ClickHouse: Microsoft Clarity and Titan. Microsoft Clarity is a free tool that provides website owners with insights to help them make better business decisions, without the need for a data science team or an instrumentation pipeline.


Narendra Rana, Principal Data Scientist on the Clarity Insights team at Microsoft, explained the architecture of Clarity, the challenges faced by the team when integrating ClickHouse, and how they overcame these challenges to create an efficient, robust, and GDPR\-compliant analytics platform.


## Powering Website Analytics at Petabyte\-Scale [\#](/blog/petabyte-scale-website-behavior-analytics-using-clickhouse#powering-website-analytics-at-petabyte-scale)


Microsoft Clarity is designed to handle billions of page views, petabytes of data, millions of websites, and hundreds of millions of users daily. Clarity is simple to set up and users can visit clarity.microsoft.com, download a JavaScript bundle, and install it on their website. Within 30 minutes, data will begin flowing onto a dashboard dedicated to the user's site. The dashboard offers insights that help website owners improve their website. They can see session recordings, heat maps, scroll maps, and gain deeper insights into their website's performance. The sessions are not sampled, and all data comes in, which is a significant advantage for webmasters.


The presentation included a live demo, where the audience was shown how a webmaster could select a session and see the interaction of their end\-users. Microsoft Clarity provides heat maps that help to aggregate and show the interaction of the end\-users. Rana explained that creating a heatmap is a complex operation that involves a big query, which is well suited for ClickHouse. “A simple operation, like looking at a heat map is basically a big query. And as this is happening lots of data is being ingested at the same time. We looked at a lot of the options out there…we realized that yes, ClickHouse is the stuff that we are going to bet on”, said Rana.


![clarity image 1.png](/uploads/clarity_image_1_636983ff04.png)
*Heat Maps in Clarity, a complex operation involving a big query in ClickHouse.*
## ClickHouse Backup and Recovery on Azure [\#](/blog/petabyte-scale-website-behavior-analytics-using-clickhouse#clickhouse-backup-and-recovery-on-azure)


The team worked with ClickHouse creator Alexey Milovidov to overcome challenges, primarily with backup and recovery on Azure, which is where they invested a significant amount of time. Rana shared that the team's experience in building this system which can be leveraged by other teams, both internal and external, who want to get efficient, robust, and consistent backups without any downtime.


![clarity image 2.png](/uploads/clarity_image_2_53402438bb.png)
*Millions of rows of data are being ingested, while thousands of queries are being executed, at the same time.*
Incremental Snapshots is a feature of Azure that enables incremental backups while data ingestion is still occurring. This is a more cost\-effective solution than the original snapshots that Azure offered. Freeze and Sync commands are used to synchronize cache and disk, and automated validation is used to test the backup and restore processes periodically.


Satish Manivannan, Senior Director of Data and Analytics at Microsoft, expressed his enthusiasm for ClickHouse, stating, "The key point is, we really love ClickHouse and we hope to have more continued collaboration for years to come." Overall, the meetup was an excellent opportunity to learn about Microsoft's use of ClickHouse and its benefits for website analytics.


## More Details [\#](/blog/petabyte-scale-website-behavior-analytics-using-clickhouse#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-seattle-user-group/events/290310025/) at the Microsoft office in Redmond on January 18, 2023
- Learn more about ClickHouse within Titan, the internal data analytics tool that enables self\-serve analytics for Microsoft in our [meetup report](https://clickhouse.com/blog/self-service-data-analytics-for-microsofts-biggest-web-properties).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
