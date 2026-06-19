# Announcing the official ClickHouse Connector for Microsoft Power BI


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing the official ClickHouse Connector for Microsoft Power BI

![](/_next/image?url=%2Fuploads%2FLuke_Gannon_NE_4_J_5562a05272.jpeg&w=96&q=75)Luke Gannon \& Bentsi LeviavNov 19, 2024 · 3 minutes readWe’re excited to announce that ClickHouse is now available as an official data source for Microsoft Power BI. Power BI is one of the leading business intelligence platforms in the world, and our users frequently ask how they can leverage it with ClickHouse.


Working closely with Microsoft, the ClickHouse team built the Power BI Connector to make it easy for you to query the data in your ClickHouse instances, regardless of whether you use ClickHouse Cloud or self\-manage your own instances.


## ClickHouse Connector availability [\#](/blog/official-microsoft-power-bi-connector#clickhouse-connector-availability)


As the de facto data visualization software for Microsoft users, our Power BI connector makes it super easy to create interactive dashboards and charts based on the data housed in ClickHouse. There are several flavors of Power BI that you can use to visualize your data:


- Power BI Desktop: a Windows desktop application
- Power BI Service: available within Azure as a SaaS
- Power BI Mobile: available on Windows, iOS and Android devices


![powerbi-1.png](/uploads/powerbi_1_1a9ef7d4f3.png)
## Ready to get started? [\#](/blog/official-microsoft-power-bi-connector#ready-to-get-started)


Before you can use the ClickHouse Power BI connector, you need to make sure you have the ClickHouse ODBC driver installed. You can get the latest version from the [official GitHub repository](https://github.com/ClickHouse/clickhouse-odbc) and run the `.msi` installer. For more information on how to verify the installation, view our [Power BI documentation](https://clickhouse.com/docs/en/integrations/powerbi).


Once the ODBC driver has been installed, you can now use the `Get Data` menu item, search for `ClickHouse,` and the connector will be installed to your Desktop application.


![powerbi-2.png](/uploads/powerbi_2_ee198c1b1d.png)
Note: you will be prompted to enter your connection details, which you can do on the left\-hand side in the ClickHouse Cloud UI. You’ll need to copy the following information:


- Host
- Port
- Database name
- Database username
- Password


![powerbi-3.png](/uploads/powerbi_3_837ce57201.png)
We recommend using DirectQuery. This will enable you to query ClickHouse instead of import mode which will load the entire dataset into your application.


To use Microsoft’s Power BI Service, you’ll need to create your report in Power BI Desktop and publish the report.


## Get in touch! [\#](/blog/official-microsoft-power-bi-connector#get-in-touch)


We’re excited to hear what dashboards and visualizations you’ll be creating with Power BI. If you have any questions or want to provide future enhancement requests, please feel free to [raise an issue on GitHub](https://github.com/ClickHouse/power-bi-clickhouse/issues/new/choose).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
