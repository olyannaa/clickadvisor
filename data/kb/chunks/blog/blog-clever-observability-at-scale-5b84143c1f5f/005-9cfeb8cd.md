---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Clever
topic: clever-ingests-200x-more-logs-at-the-same-cost-with-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 7
---

environments: ClickHouse Cloud services in us\-east and us\-west, with a third service handling dev logs. ClickHouse's [remoteSecure](https://clickhouse.com/docs/sql-reference/table-functions/remote) table function and [merge tables](https://clickhouse.com/docs/engines/table-engines/special/merge) stitch the two production services into a single queryable surface, with reads load\-balanced across both regions.

> "ClickHouse Cloud multi\-region availability gives us the business continuity and disaster recovery we needed. In case of an outage, we can easily stop and redirect all reads or writes to only one of these services, we're much more resilient." — Jake Gutierrez, Sr Software Engineer, Clever

The infrastructure\-as\-code requirement was about making the system easily reproducible. Every ClickHouse service, secret, and KMS key is provisioned with Terraform. Schema changes are managed through Goose using incremental SQL migration files, supplemented by Go\-based migrations for anything that requires dynamic resource creation (e.g. the remote tables that connect the regional services). "The Go functions are also useful for pulling credentials so we don't have to store plaintext passwords in GitHub," Jake says.

## Making ClickHouse feel like home \#

The third area Jake covered was query experience. "We wanted something similar to Datadog, so that it's easy for engineers to ramp up to this new system with no steep learning curve," Jake says. While raw SQL access to ClickHouse is powerful, most of Clever's engineers don't use SQL day\-to\-day. They were familiar with Grafana and wanted to keep using it, but the official ClickHouse Grafana plugin didn't support their non\-standard schema.

So the Clever team built their own query layer. "Q\-Layer," as it's known, is a service that implements a subset of Grafana's LogQL and translates those queries into ClickHouse SQL behind the scenes. Engineers write queries in a familiar, Datadog\-like syntax; Q\-Layer handles the translation. As Jake notes, "More complex queries can still be made in SQL, and engineers can always request improvements to the LogQL implementation." [Projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection) back the log volume chart for fast count queries, while a [materialized view](https://clickhouse.com/docs/materialized-views) powers IntelliSense\-style autocomplete on log labels.

The result, as Jake puts it, is a logging system that engineers can query without having to think about what's running underneath.

## 200x more logs, 0% cost increase \#
