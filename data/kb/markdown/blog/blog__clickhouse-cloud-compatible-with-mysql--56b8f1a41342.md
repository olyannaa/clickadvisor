# ClickHouse Cloud now Compatible with the MySQL Protocol


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud now Compatible with the MySQL Protocol

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Oct 5, 2023 · 3 minutes readClickHouse's compatibility with third\-party business intelligence tools and data visualization platforms is crucial for deriving insights from the stored data. Tools like Superset, Metabase, and Grafana can connect natively to ClickHouse and help users create fast and meaningful dashboards and reports, leveraging ClickHouse’s unbeatable performance and versatility.


However, some of our users deploy tools that do not yet provide a native ClickHouse connector. Often, these tools are also proprietary solutions and don’t offer easy ways for us to contribute a native integration. To address this requirement, we are thrilled today to announce that compatibility can be achieved leveraging the [MySQL interface for ClickHouse](https://clickhouse.com/docs/en/interfaces/mysql), now available in ClickHouse Cloud. As of the time of writing this, compatibility allows our users to use Looker Studio and Tableau online with ClickHouse with support for Amazon QuickSight under active development.



## A concrete example with ClickHouse Cloud and Google Looker Studio [\#](/blog/clickhouse-cloud-compatible-with-mysql#a-concrete-example-with-clickhouse-cloud-and-google-looker-studio)


We designed an opt\-in experience for the MySQL interface in ClickHouse Cloud in order to limit the network exposure of Cloud services by default. Using the connection string screen, you can now access the MySQL tab and decide to enable the MySQL interface for your service.


![mysql_protocol_enable.png](/uploads/mysql_protocol_enable_918aa8a730.png)
Once enabled, your ClickHouse Service will expose port 3306 and prompt you with your MySQL connection string that includes your unique MySQL username. The password will be the same as the service's default user password.


With these settings, you can now go to your [Looker Studio](https://lookerstudio.google.com/) interface,declare a new MySQL Data Source, and provide the provided credentials.


![looker_mysql.png](/uploads/looker_mysql_53e2568b78.png)
In the Looker Studio UI, you’ll need to check the "Enable SSL" option. ClickHouse Cloud's SSL certificate is signed by LetsEncrypt. You can download this root cert [here](https://letsencrypt.org/certs/isrgrootx1.pem) and upload it in Looker Studio.


![enable_ssl_mysql.png](/uploads/enable_ssl_mysql_42acf992ac.png)
That’s it! In a few steps, you now have a working connection in place between Looker Studio and ClickHouse Cloud that is using the MySQL interface. Alternatively, you can also leverage this interface to accelerate the migration of your custom applications built for MySQL to ClickHouse Cloud for faster analytics capabilities at scale.


![hackernews_looker.png](/uploads/hackernews_looker_5ab1e4313d.png)
## What’s next? [\#](/blog/clickhouse-cloud-compatible-with-mysql#whats-next)


We tested this feature extensively with Google Looker Studio and Tableau online and improved the overall compatibility of the MySQL interface in ClickHouse by addressing [numerous issues](https://github.com/ClickHouse/ClickHouse/issues?q=is%3Aissue+%22MySQL%22+author%3Aslvrtrn+) (shoutout to Serge Klochkov and Robert Schulze for the great work!). For a detailed description of the work done and efforts made by Serge and the team, see [here](https://clickhouse.com/blog/mysql-support-in-clickhouse-the-journey). We’ll be continuing this evaluation and continuous improvement on different platforms, prioritized based on user feedback. As of now, we are already exploring Microsoft PowerBI and Amazon QuickSight.


As always, user feedback is extremely valuable. If you experience limitations with this functionality for a specific tool or platform or you’d like to see support for another tool, please don’t hesitate to reach out to us ([contact form](https://clickhouse.com/company/contact), [new issue](https://github.com/ClickHouse/ClickHouse/issues/new/choose)).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
