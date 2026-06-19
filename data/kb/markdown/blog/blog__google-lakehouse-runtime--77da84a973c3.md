# ClickHouse integrates with Lakehouse Runtime Catalog


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse integrates with Lakehouse Runtime Catalog

![](/_next/image?url=%2Fuploads%2FMelvyn_00a76a1519.PNG&w=96&q=75)[Melvyn Peignon](/authors/melvyn-peignon)Apr 22, 2026 · 6 minutes readWe're excited to announce a new integration between ClickHouse and Google's [Lakehouse Runtime Catalog](https://docs.cloud.google.com/biglake/docs/blms-rest-catalog), enabling direct querying of [Google Cloud Lakehouse Iceberg tables](https://docs.cloud.google.com/biglake/docs/biglake-iceberg-tables-in-bigquery) in ClickHouse via [Apache Iceberg REST Catalog](https://iceberg.apache.org/).


This integration debuts as a beta feature in ClickHouse 26\.2 and will be available shortly after in ClickHouse Cloud.


## **Why Iceberg REST Catalog?** [\#](/blog/google-lakehouse-runtime#why_iceberg_rest_catalog)


A common challenge for data teams is making all their data accessible regardless of where it lives. Discovery, governance, and access control need to work across data lakes, warehouses, and operational stores.


Lakehouse Runtime Catalog solves this by providing a centralized catalog for Apache Iceberg tables in Google Cloud. That enables interoperability with any Iceberg\-compatible engine: BigQuery, Apache Spark, Trino, and now ClickHouse.


By connecting to the REST Catalog, ClickHouse can discover and query Google Cloud Lakehouse Iceberg tables stored in Cloud Storage with no data movement, no proprietary connectors, and no metadata syncing required. Data engineers can write Google Cloud Lakehouse Iceberg tables with Spark or BigQuery, and analysts can immediately query that same data with ClickHouse for fast, complex analytics. Data can also be loaded into ClickHouse's native format in a single query using this integration!


## **How does the integration work?** [\#](/blog/google-lakehouse-runtime#how_does_the_integration_work)


To use this integration, you need two things:


- A ClickHouse instance (ClickHouse and [ClickHouse local](https://clickhouse.com/docs/operations/utilities/clickhouse-local) supported)
- A [Google Cloud project](https://cloud.google.com/) with Lakehouse Runtime Catalog enabled


Lakehouse Runtime Catalog tracks the Iceberg metadata for Iceberg tables and exposes it via the Iceberg REST Catalog API at `https://biglake.googleapis.com/iceberg/v1/restcatalog`. ClickHouse connects to this endpoint to discover and query the underlying tables directly.


For authentication, ClickHouse integrates with Google's [Application Default Credentials (ADC)](https://docs.cloud.google.com/docs/authentication/provide-credentials-adc) mechanism.


## **Getting started** [\#](/blog/google-lakehouse-runtime#getting_started)


Deploy ClickHouse on [Google Cloud](https://clickhouse.com/partners/gcp) or use [ClickHouse local](https://clickhouse.com/docs/operations/utilities/clickhouse-local), ensuring you're on version 26\.2 or later. Once your instance is ready, follow the steps below to connect to the Lakehouse Runtime Catalog. Read more in the [ClickHouse documentation for Lakehouse Runtime Catalog](https://clickhouse.com/docs/use-cases/data-lake/biglake-catalog).


## **Authentication with Google Application default credentials** [\#](/blog/google-lakehouse-runtime#authentication_with_google_application_default_credentials)


ClickHouse supports Google ADC natively, giving you two options to authenticate with the Lakehouse Runtime Catalog.


### **Option 1: Point to your ADC credentials file** [\#](/blog/google-lakehouse-runtime#option-1-point-to-your-adc-credentials-file)


If you already have Application Default Credentials configured on your machine (e.g. via `gcloud auth application-default login`), you can simply point ClickHouse to the JSON credentials file. This is the easiest approach for local development and testing:



```

```
1SET allow_database_iceberg = 1;
2
3CREATE DATABASE Lakehouse_catalog
4ENGINE = DataLakeCatalog('https://biglake.googleapis.com/iceberg/v1/restcatalog')
5SETTINGS
6  catalog_type = 'biglake',
7  google_adc_credentials_file = '/path/to/application_default_credentials.json',
8  warehouse = 'gs://<bucket_name>/<optional-prefix>';
```

```

ClickHouse reads the `client_id`, `client_secret`, `refresh_token`, and `quota_project_id` directly from the JSON file, so you don't need to specify them individually.


### **Option 2: Provide credentials inline** [\#](/blog/google-lakehouse-runtime#option-2-provide-credentials-inline)


For production deployments or environments where a credentials file isn't available, you can provide the OAuth credentials directly in the query settings:



```

```
1SET allow_database_iceberg = 1;
2
3CREATE DATABASE Lakehouse_catalog
4ENGINE = DataLakeCatalog('https://biglake.googleapis.com/iceberg/v1/restcatalog')
5SETTINGS
6  catalog_type = 'biglake',
7  google_adc_client_id = '<client-id>',
8  google_adc_client_secret = '<client-secret>',
9  google_adc_refresh_token = '<refresh-token>',
10  google_adc_quota_project_id = '<gcp-project-id>',
11  warehouse = 'gs://<bucket_name>/<optional-prefix>';
```

```

Both approaches use the same underlying OAuth flow to authenticate with the Iceberg REST Catalog endpoint and authorize access to the data in Cloud Storage.


## **Querying Google Lakehouse Iceberg tables from ClickHouse** [\#](/blog/google-lakehouse-runtime#querying_google_lakehouse_iceberg_tables_from_clickhouse)


Once you've created a connection using either of the authentication methods above, querying your Google Lakehouse Iceberg tables is straightforward.


### **Listing available tables** [\#](/blog/google-lakehouse-runtime#listing-available-tables)


List all tables available in the catalog:



```

```
1SHOW TABLES FROM Lakehouse_catalog;
```

```


```
┌─name─────────────────────────┐
│ public_data.nyc_taxicab      │
│ public_data.nyc_taxicab_2021 │
└──────────────────────────────┘

```

### **Querying tables** [\#](/blog/google-lakehouse-runtime#querying-tables)


Query any Google Cloud Lakehouse Iceberg table directly:



```

```
1SELECT count(*)
2FROM Lakehouse_catalog.`public_data.nyc_taxicab`
3WHERE vendor_id = 1;
```

```

You can also inspect the full schema:



```

```
1SHOW CREATE TABLE Lakehouse_catalog.`public_data.nyc_taxicab`;
```

```

Backticks are required around table names because ClickHouse doesn't support more than one namespace level.


### **Loading data into ClickHouse for faster queries** [\#](/blog/google-lakehouse-runtime#loading-data-into-clickhouse-for-faster-queries)


For use cases that require repeated, low\-latency queries, you can load data from Google Cloud Lakehouse Iceberg tables into a ClickHouse table:



```

```
1CREATE TABLE local_taxi_data
2(
3    `vendor_id` Int64,
4    `pickup_datetime` DateTime64(6),
5    `dropoff_datetime` DateTime64(6),
6    `passenger_count` Int64,
7    `trip_distance` Float64,
8    `total_amount` Float64,
9    `pickup_location_id` Int64,
10    `dropoff_location_id` Int64
11)
12ENGINE = MergeTree
13ORDER BY (pickup_datetime, vendor_id);
14
15INSERT INTO local_taxi_data
16SELECT
17    vendor_id, pickup_datetime, dropoff_datetime,
18    passenger_count, trip_distance, total_amount,
19    pickup_location_id, dropoff_location_id
20FROM lakehouse_catalog.`public_data.nyc_taxicab`;
```

```

You can now query the local\_taxi\_data directly in ClickHouse native format for low query latency.


## **What's next** [\#](/blog/google-lakehouse-runtime#whats_next)


This release is just the first step toward deeper integration with Google Cloud's data ecosystem.


We're already working on several enhancements for upcoming releases, including:


- **Write support:** Adding support for writing data back to Google Cloud Lakehouse Iceberg tables from ClickHouse.
- **Enhanced cloud integration:** Introducing a new user interface in ClickHouse Cloud to easily create connections to the Lakehouse Runtime Catalog and query your data directly from the UI.


![](/uploads/lakehouse_apr2026_image1_c9bdbd90df.png)
With ClickHouse and the Lakehouse Runtime Catalog, you can run fast analytics on all of your Google Cloud Lakehouse Iceberg tables in Google Cloud, without moving data, without duplicating it, and without giving up the tools your teams already use.


## **Get started today** [\#](/blog/google-lakehouse-runtime#get_started_today)


Deploy ClickHouse on [Google Cloud](https://clickhouse.com/pricing?plan=scale&provider=gcp&region=gcp-us-central1&hours=8&storageCompressed=false) or use [ClickHouse local](https://clickhouse.com/docs/operations/utilities/clickhouse-local) once your instance is ready, follow the steps below to connect to the Lakehouse Runtime Catalog. Read more in the [ClickHouse documentation for Lakehouse Runtime Catalog](https://clickhouse.com/docs/use-cases/data-lake/biglake-catalog).

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-464-get-started-today-sign-up&utm_blogctaid=464)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
