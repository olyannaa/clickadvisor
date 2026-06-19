# ClickHouse integrates with Microsoft OneLake Table APIs


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse integrates with Microsoft OneLake Table APIs

![](/_next/image?url=%2Fuploads%2FMelvyn_00a76a1519.PNG&w=96&q=75)[Melvyn Peignon](/authors/melvyn-peignon)Nov 18, 2025 · 6 minutes readWe’re excited to announce a new integration between ClickHouse and Microsoft OneLake \- Microsoft Fabric’s unified data lake \- powered by the OneLake [Tables APIs](https://learn.microsoft.com/en-us/fabric/onelake/table-apis/iceberg-table-apis-overview) and [Apache Iceberg](https://iceberg.apache.org/).


This integration will debut as a beta feature in ClickHouse 25\.11 (November release) and will be available shortly after in ClickHouse Cloud.


With this new integration, ClickHouse now supports direct querying of Iceberg tables in OneLake, eliminating friction and unlocking unified, fast analytics across multiple sources.


## **Building a Unified Analytics and AI Platform** [\#](/blog/clickhouse-integrates-with-microsoft-onelake#building-a-unified-analytics-and-ai-platform)


A common challenge for organizations and in particular data teams is being able to use all of their data, regardless of where it’s stored for analytics, GenAI and AI agents. Discovery, governance and access controls are critical to successfully delivering on these projects. Making sure they work with all data assets in various data lakes, data warehouses and operational stores is very difficult.


Microsoft OneLake enables organizations to unify their data into a common store, cataloging and securing it in a single place. They can use [OneLake Shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) to connect external stores like [Amazon S3](https://learn.microsoft.com/en-us/fabric/onelake/create-s3-shortcut) or [Google Cloud Storage](https://learn.microsoft.com/en-us/fabric/onelake/create-gcs-shortcut) to OneLake, moving data only when it is queried. They can also continuously replicate data from popular databases using native [zero\-copy mirroring](https://learn.microsoft.com/en-us/fabric/mirroring/overview) or build their own with [Open Mirroring](https://learn.microsoft.com/en-us/fabric/mirroring/open-mirroring). All of this data is cataloged in the [OneLake catalog](https://learn.microsoft.com/en-us/fabric/governance/onelake-catalog-overview) and secured using [OneLake Security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security) so it can be safely accessed from Microsoft Fabric, [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry) and many popular 3rd party engines like ClickHouse.


OneLake’s Iceberg\-compatible [Tables APIs](https://learn.microsoft.com/en-us/fabric/onelake/table-apis/iceberg-table-apis-overview) make it possible for ClickHouse to discover and query data in OneLake with minimal configuration. The ease of use and ecosystem interoperability enable a unified analytical platform that combines flexibility and control to empower users to build and deliver analytics and AI projects quickly with all of their data \- enterprise, operational, logs, and 3rd party.


## **How does the integration work?** [\#](/blog/clickhouse-integrates-with-microsoft-onelake#how-does-the-integration-work)


To use this new integration, you only need two components:


- A ClickHouse instance (even [ClickHouse local](https://clickhouse.com/docs/operations/utilities/clickhouse-local) will suffice)
- A [Microsoft Fabric account](https://www.microsoft.com/en-us/microsoft-fabric/getting-started)


Tables can be written into OneLake using Fabric managed engines like [Spark](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime) or [Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/) or your tool of choice. You can write tables in either Delta Lake or Apache Iceberg format. OneLake’s format virtualization will automatically convert between formats and keep both in sync at all times, making it easy to bring your engine of choice without converting or migrating your data.


OneLake also exposes an Iceberg REST catalog via OneLake Table APIs, which ClickHouse uses as an interface to discover and query the underlying Iceberg tables directly.


![onelake_image1.png](/uploads/onelake_image1_01d3a18aa2.png)
For security, ClickHouse uses Microsoft Entra ID (formerly Azure Active Directory) to authenticate the user identity with the OneLake Table APIs, ensuring secure and controlled access to data stored in OneLake. Additionally, the same access token received from Entra will be used to allow users the ability to read data from OneLake. Access permissions are managed in Entra as [Service Principals](https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals?tabs=browser) or through Fabric [workspace\-level permissions](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sharing).


## **Getting Started with ClickHouse and OneLake** [\#](/blog/clickhouse-integrates-with-microsoft-onelake#getting-started-with-clickhouse-and-onelake)


Getting started with ClickHouse and OneLake is simple. You can deploy ClickHouse on [Azure](https://clickhouse.com/partners/azure) or directly from the [Azure Marketplace](https://marketplace.microsoft.com/en-us/product/saas/clickhouse.clickhouse_cloud?tab=overview), ensuring you’re using version 25\.11\. Once your service is deployed, you’ll be able to enable the OneLake integration and run the following queries to access your Iceberg tables directly. Read more in the [ClickHouse documentation for OneLake](https://clickhouse.com/docs/use-cases/data-lake/onelake-catalog).


## **Querying OneLake from ClickHouse** [\#](/blog/clickhouse-integrates-with-microsoft-onelake#querying-onelake-from-clickhouse)


It is very simple to start querying OneLake using ClickHouse. [Here](http://learn.microsoft.com/en-us/fabric/onelake/table-apis/table-apis-overview#prerequisites), you’ll find a step\-by\-step guide to obtaining all the information needed to connect ClickHouse to your OneLake Iceberg catalog.


Since this integration is still in beta, you’ll need to also execute the following:



```
SET allow_database_iceberg=1

```

### Creating a connection to OneLake [\#](/blog/clickhouse-integrates-with-microsoft-onelake#creating-a-connection-to-onelake)


Once the prerequisites are met, you can create a connection to your OneLake Iceberg catalog by running the following command in ClickHouse:



```
CREATE DATABASE onelake_catalog   
ENGINE = DataLakeCatalog('https://onelake.table.fabric.microsoft.com/iceberg')   
SETTINGS
  catalog_type = 'onelake',   
  warehouse = 'warehouse_uuid/data_item_uuid',   
  onelake_tenant_id = '<tenant_id>',   
  oauth_server_uri = 'https://login.microsoftonline.com/<tenant_uuid>/oauth2/v2.0/token',   
  auth_scope = 'https://storage.azure.com/.default',   
  onelake_client_id = '<client_id>',   
  onelake_client_secret = '<client_secret>';

```

### Querying OneLake tables [\#](/blog/clickhouse-integrates-with-microsoft-onelake#querying-onelake-tables)


After creating the connection, you can list all the tables available in the catalog:



```
SHOW TABLES FROM onelake_catalog;

```

![onelake_image2.png](/uploads/onelake_image2_6dbbc12201.png)
Then, you can query any table directly from ClickHouse:



```
SELECT count(*)   
FROM onelake_catalog.`year_2017.green_tripdata_2017`   
WHERE VendorID = 2;

```

![onelake_image3.png](/uploads/onelake_image3_9e0ea8ce49.png)
## **What’s next** [\#](/blog/clickhouse-integrates-with-microsoft-onelake#whats-next)


The 25\.11 release is just the first step toward deeper integration with the OneLake ecosystem.


We’re already working on several enhancements that will be introduced in upcoming releases, including:


- **General Availability**: Upgrading the feature from beta to GA by improving the overall quality of life, performance, and incorporating user feedback.
- **Write support:** Adding support for writing data back to your Iceberg tables in OneLake.
- **Enhanced cloud integration:** Introducing a new user interface in ClickHouse Cloud to easily create connections to the OneLake catalog and query your data directly from the UI.


![onelake_image4.png](/uploads/onelake_image4_d309e8af1e.png)
With ClickHouse and Microsoft OneLake, customers can leverage their vast data assets, integrated via OneLake native integrations, Shortcuts and Mirroring, to quickly and easily query, perform complex analytics and drive GenAI and AI Agent initiatives with ease. Get started today at [ClickHouse.com](http://clickhouse.com)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
