---
source: kb.altinity.com
url: https://github.com/Altinity/clickhouse-operator/blob/master/docs/quick_start.md
topic: using-the-altinity-kubernetes-operator-for-clickhouse-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '0.0'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 8
---

connect to the same ip even when there is a new Kafka pod running and the old one is deprecated. Is there some setting where we could refresh the connection `<disable_internal_dns_cache>1</disable_internal_dns_cache>` in config.xml ### ClickHouse init process failed

It’s due to low value for env `CLICKHOUSE_INIT_TIMEOUT` value. Consider increasing it up to 1 min.
[https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/docker/server/entrypoint.sh\#L120](https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/docker/server/entrypoint.sh#L120)

---

##### [Istio Issues](/altinity-kb-kubernetes/altinity-kb-istio-user-issue-k8s/)

Working with the popular service mesh

Last modified 2024\.12\.03: [Removed Zendesk link (6328eab)](https://github.com/Altinity/altinityknowledgebase/commit/6328eab05a21aa2395d643a993d7ab7eb6cd7704)
