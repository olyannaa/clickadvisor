---
source: blog
url: https://clickhouse.com/blog/clickhouse-cloud-is-now-generally-available-on-microsoft-azure
topic: agent-facing-analytics-data-lake-support-and-more-a-year-of-clickhouse-cloud-on-azure
ch_version_introduced: '1.1147851049'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 9
---

modes of ingestion: **one\-time loads** and **continuous ingestion** as new files are added to the storage containers. [You can sign up for the private preview here.](https://clickhouse.com/cloud/clickpipes/azure-blob-storage-connector) This connector is built to support enterprise\-grade workloads with the following capabilities:

1. **Built for reliability** – Under the hood, it leverages the native `[azureBlogStorageCluster](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorageCluster)` table function in ClickHouse, but enhances it with improved reliability and a fully managed experience. Loading billions (or even trillions) of rows from object storage can be error\-prone due to transient network issues—retries aren’t trivial, and handling duplicates is tricky. The connector handles retries automatically and ensures **exactly\-once ingestion**, so you don’t have to worry about data consistency or partial loads.
2. **Secure by design** – It supports ingestion from private buckets, with authentication through connection string, which includes account name and key, or can be specified using the storage account URL. You can also use our Shared Access Signature (SAS) within the connection string for time\-limited access without sharing your storage account key.
3. **Optimized for performance** – The connector dynamically tunes ingestion based on your workload and the size of your ClickHouse instance—for example, by adjusting ingestion parallelism, tuning ClickHouse\-specific settings, and more.
4. **Fully managed experience** – The connector is fully integrated into the ClickHouse Cloud experience. It offers high availability, built\-in metrics and monitoring, including throughput, detailed logs for error diagnosis and debugging, in\-place pipe editing (e.g., adding columns), and more.

**Note:** Continuous ingestion may have some caveats, such as limits on the number of files in the bucket. We'll work with you during the private preview to assist with the implementation.

![Azure Blob Storage.gif](/uploads/Azure_Blob_Storage_8df8563bb7.gif)
### AzureQueue and azureBlobStorage [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azurequeue-and-azureblobstorage)

In addition to the fully managed ClickPipes connector to Azure Blob Storage, it is possible to access Azure Blob storage directly from ClickHouse via the [azureBlobStorage table function](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorage) for ad\-hoc queries and the [AzureQueue Table Engine](https://clickhouse.com/docs/engines/table-engines/integrations/azure-queue) for continuous data imports. Introduced in the ClickHouse [24\.7 release](https://github.com/ClickHouse/ClickHouse/pull/65458), AzureQueue will periodically check object storage for new files and load the data into ClickHouse automatically for you. It supports all the formats that ClickHouse supports and will simplify your data loading procedures.

### Azure Flexible Server (Postgres CDC) [\#](/blog/a-year-of-clickhouse-cloud-on-azure#azure-flexible-server-postgres-cdc)
