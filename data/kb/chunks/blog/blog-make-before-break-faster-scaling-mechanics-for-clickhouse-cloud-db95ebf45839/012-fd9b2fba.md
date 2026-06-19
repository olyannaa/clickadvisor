---
source: blog
url: https://kubernetes.io/blog/2023/04/28/statefulset-start-ordinal/
topic: make-before-break-faster-scaling-mechanics-for-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 13
---

table data on object storage. Combined with the command to \*\*ATTACH \*\*a table based on its name, uuid and path on object storage, we can now preserve system tables during MBB operations. ![system_tables.png](/uploads/system_tables_045684441a.png) ### System table attachments [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#system-table-attachments)

While attachments seem like a simple enough operation, it requires very fine\-grained tracking of system tables. We modified the clickhouse\-operator to start tracking the tables along with their replica names. This is important because each replica has its own replica\-local copy of say `system.query_log`. Once the old 3 replicas go away, we want the ability to attach the system tables from those 3 replicas to the newly made replicas (ideally preserving the same table distribution).

It is also important for retention purposes. Currently we have a hard\-limit of 30 days. As more and more MBB operations happen in our cloud (for both Upgrades and Scaling), more and more system tables get accumulated. This has an impact on replica startup time. We are currently exploring avenues to improve this.

## Conclusion [\#](/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud#conclusion)

Building MultiSTS, Make Before Break and Live Migrations has been a \~2 year project. This involved a long tail of a lot of customers who had unique challenges. We ended up with a lot of stragglers who took quite some time to migrate due. The typical flow would be to migrate a few customers \-\> encounter issues \-\> fix said issues \-\> continue again. We also had to be very proactive in communicating the impact of these migrations to our customers (via our UI and sending emails to critical customers).

We had to handle some customers with special requirements, and our engineers were hands\-on in managing those cases. Importantly, the principle of “make before break” meant these issues were at no time ever disruptive to customer production workloads.
