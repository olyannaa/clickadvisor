---
source: blog
url: https://github.com/ClickHouse/clickhouse-odbc
topic: announcing-the-official-clickhouse-connector-for-microsoft-power-bi
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

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
