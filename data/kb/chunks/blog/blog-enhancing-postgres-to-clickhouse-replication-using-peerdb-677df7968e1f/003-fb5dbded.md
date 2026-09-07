---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Enhancing
topic: enhancing-postgres-to-clickhouse-replication-using-peerdb-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 4
---

related to the overcommit tracker mentioned earlier. We disabled this setting for our queries by setting it to 0\. 5. [`dial_timeout`](https://clickhouse.com/docs/en/integrations/go#connection-settings-1): Sometimes queries were taking longer than 1 minute, so we [increased the `dial_timeout`](https://github.com/PeerDB-io/peerdb/pull/1772) to a higher value.

These changes drastically reduced memory\-related issues on smaller ClickHouse clusters. We are actively working with the core team to further fine\-tune ClickHouse\-specific settings. Additionally, we are working on a [feature](https://github.com/PeerDB-io/peerdb/pull/1770) that improves the handling of large datasets by breaking them into manageable parts for more efficient processing and storage.

## Row\-level transformations \#

A few months ago, PeerDB shipped [Lua\-based row\-level transformations](https://blog.peerdb.io/row-level-transformations-in-postgres-cdc-using-lua) while replicating data from Postgres to Queues such as Kafka. We have now extended this feature to ClickHouse. With this feature, customers can write simple Lua scripts to perform row\-level transformations, enabling use cases such as masking PII data, generating columns, and more. Below is a quick demo of this feature to mask PII columns while replicating data from Postgres to ClickHouse:

## Improved security on PeerDB Cloud \#

At PeerDB, safeguarding data replication from Postgres to ClickHouse is crucial. To enhance security, we have implemented several key measures around AWS S3, which we use for internally staging data before pushing it to ClickHouse.

### Temporary credentials with IAM roles \#

One significant enhancement is the use of AWS S3 buckets with strict access controls. Instead of traditional, long\-lived user\-generated access keys, which pose a higher risk of compromise, we use IAM roles to generate temporary credentials. These credentials are automatically rotated by AWS, ensuring they are always up\-to\-date and valid for only short periods, thus minimizing the risk of unauthorized access.

Additionally, with the introduction of the AWS\_SESSION\_TOKEN parameter in ClickHouse version 24\.3\.1, our security practices have been further strengthened. This update allows the use of short\-lived credentials, aligning with our approach to secure data replication.

### Attribute Based Access Control (ABAC) \#
