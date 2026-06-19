---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/url.md)#
topic: url-clickhouse-docs
ch_version_introduced: '127.0'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 3
---

**Empty**: returns the base URL without fragment. - **Absolute URL**: passed through unchanged; `url_base` is ignored. **Example** ``` SET url_base = 'https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/'; SELECT * FROM url('tests/queries/0_stateless/data_csv/data.csv', CSV) LIMIT 3; ``` ## Storage Settings[​](#storage-settings "Direct link to Storage Settings")

- [engine\_url\_skip\_empty\_files](/docs/operations/settings/settings#engine_url_skip_empty_files) \- allows to skip empty files while reading. Disabled by default.
- [enable\_url\_encoding](/docs/operations/settings/settings#enable_url_encoding) \- allows to enable/disable decoding/encoding path in uri. Enabled by default.
- [url\_base](/docs/operations/settings/settings#url_base) \- base URL for resolving relative URLs passed to the `url` function.

## Permissions[​](#permissions "Direct link to Permissions")

`url` function requires `CREATE TEMPORARY TABLE` permission. As such \- it'll not work for users with [readonly](/docs/operations/settings/permissions-for-queries#readonly) \= 1 setting. At least readonly \= 2 is required.

## Related[​](#related "Direct link to Related")

- [Virtual columns](/docs/engines/table-engines#table_engines-virtual_columns)
[PreviousarrowFlight](/docs/sql-reference/table-functions/arrowflight)[NexturlCluster](/docs/sql-reference/table-functions/urlCluster)- [Syntax](#syntax)- [Parameters](#parameters)- [Returned value](#returned_value)- [Examples](#examples)- [Globs in URL](#globs-in-url)- [Virtual Columns](#virtual-columns)- [use\_hive\_partitioning setting](#hive-style-partitioning)- [Resolving relative URLs](#resolving-relative-urls)- [Storage Settings](#storage-settings)- [Permissions](#permissions)- [Related](#related)
Was this page helpful?
