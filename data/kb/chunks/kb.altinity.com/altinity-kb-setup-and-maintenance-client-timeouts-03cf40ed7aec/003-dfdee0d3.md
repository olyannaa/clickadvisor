---
source: kb.altinity.com
url: https://clickhouse.com/docs/en/integrations/language\-clients/javascript\#keep\-alive\-nodejs\-only](https://clickhouse.com/docs/en/integrations/language-clients/javascript#keep-alive-nodejs-only
topic: client-timeouts-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 3
---

23\.12 default \`keep\_alive\_timeout\` configured on clickhouse side was 3\. For 23\.8 \`keep\_alive\_timeout\` is not present as a server setting in \`system.server\_settings\` table but if is in the config.xml.- `sync_request_timeout` – timeout for server ping. Defaults to 5 seconds.

In some cases, if the data sync request time out, it may be caused by many different reasons, basically it shouldn’t take more than 5 seconds for synchronous request\-result protocol call (like Ping or TableStatus) in most of the normal circumstances, thus if time out setting too long, eg. 5 minutes or longer than that, then you will run into more overall performance issues. This is not good for any application on the server.

### How to check the current timeouts:

```
SELECT
    name,
    value,
    changed,
    description
FROM system.settings
WHERE (name ILIKE '%send_timeout%') OR (name ILIKE '%receive_timeout%') OR (name ILIKE '%keep_alive%') OR (name ILIKE '%_http_headers') OR (name ILIKE 'http_headers_progres_%') OR (name ILIKE 'http_connection_%')

```
Last modified 2025\.09\.02: [Update client\-timeouts.md (b3f21a0\)](https://github.com/Altinity/altinityknowledgebase/commit/b3f21a08bf0f32327bf5725b06d943ebb9767226)
