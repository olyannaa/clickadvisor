---
source: kb.altinity.com
url: https://clickhouse.com/docs/en/integrations/language\-clients/javascript\#keep\-alive\-nodejs\-only](https://clickhouse.com/docs/en/integrations/language-clients/javascript#keep-alive-nodejs-only
topic: client-timeouts-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 3
---

# Client Timeouts \| Altinity® Knowledge Base for ClickHouse®

1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Client Timeouts
# Client Timeouts

How to prevent connection errors.Timeout settings are related to the client, server, and network. They can be tuned to solve sporadic timeout issues.

It’s important to understand that network devices (routers, NATs, load balancers ) could have their own timeouts. Sometimes, they won’t respect TCP keep\-alive and close the session due to inactivity. Only application\-level keepalives could prevent TCP sessions from closing.

Below are the settings that will work only if you set them in the default user profile. The problem is that they should be applied before the connection happens. And if you send them with a query/connection, it’s already too late:

```
SETTINGS
        receive_timeout = 3600,
        send_timeout = 3600,
        http_receive_timeout = 3600,
        http_send_timeout = 3600,
        http_connection_timeout = 2

```
Those can be set on the query level (but in the profile, too):

```
SETTINGS
    tcp_keep_alive_timeout = 3600,
    --!!!send_progress_in_http_headers = 1,
    http_headers_progress_interval_ms = 10000,
    http_wait_end_of_query = 1,
    max_execution_time = 3600

```
[https://clickhouse.com/docs/en/integrations/language\-clients/javascript\#keep\-alive\-nodejs\-only](https://clickhouse.com/docs/en/integrations/language-clients/javascript#keep-alive-nodejs-only)

`send_progress_in_http_headers`  will not be applied in this way because here we can configure the JDBC driver’s client options only ([this](https://github.com/ClickHouse/clickhouse-java/blob/main/clickhouse-client/src/main/java/com/clickhouse/client/config/ClickHouseClientOption.java)
), but there is an option called `custom_settings`  ([this](https://github.com/ClickHouse/clickhouse-java/blob/main/clickhouse-client/src/main/java/com/clickhouse/client/config/ClickHouseClientOption.java#L34C22-L34C37)
) that will apply custom ch query settings for every query before the actual connection is created. The correct JDBC connection string will look like this:

```
jdbc:clickhouse://"${clickhouse.host}"/"${clickhouse.db}"?ssl=true&socket_timeout=3600000&socket_keepalive=true&custom_settings=send_progress_in_http_headers=1

```
### Description
