# ClickHouse® Monitoring \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. ClickHouse® Monitoring
# ClickHouse® Monitoring

Tracking potential issues in your cluster before they cause a critical errorWhat to read / watch on the subject:

- Altinity webinar “ClickHouse Monitoring 101: What to monitor and how”. [Watch the video](https://www.youtube.com/watch?v=W9KlehhgwLw)
or [download the slides](https://www.slideshare.net/Altinity/clickhouse-monitoring-101-what-to-monitor-and-how)
.
- [The ClickHouse docs](https://clickhouse.com/docs/en/operations/monitoring/)

## What should be monitored

The following metrics should be collected / monitored

- For Host Machine:


	- CPU
	- Memory
	- Network (bytes/packets)
	- Storage (iops)
	- Disk Space (free / used)
- For ClickHouse:


	- Connections (Number of queries running)
	- DDL queue length
	- RWLocks
	- Read / Write / Return (bytes/rows)
	- Merges (queue length, memory used)
	- Mutations
	- Query duration (optional)
	- Replication queue length and lag
	- Read only tables
	- ZooKeeper latencies
	- Zookeeper operations (count)
	- S3 errors (if used)
- For Zookeeper:


	- [See separate article](../altinity-kb-zookeeper/zookeeper-monitoring/)

## ClickHouse monitoring tools

### Prometheus (embedded exporter) \+ Grafana

- Enable [embedded exporter](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-prometheus)
- Grafana dashboards <https://grafana.com/grafana/dashboards/14192>
or <https://grafana.com/grafana/dashboards/13500>

### Prometheus (embedded http handler with Altinity Kubernetes Operator for ClickHouse style metrics) \+ Grafana

- Enable [http handler](../monitoring-operator-exporter-compatibility/)
- Useful, if you want to use the dashboard from the Altinity Kubernetes Operator for ClickHouse, but do not run ClickHouse in k8s.

### Prometheus (embedded exporter in the Altinity Kubernetes Operator for ClickHouse) \+ Grafana

- exporter is included in the Altinity Kubernetes Operator for ClickHouse, and enabled automatically
- see instructions of [Prometheus](https://github.com/Altinity/clickhouse-operator/blob/eb3fc4e28514d0d6ea25a40698205b02949bcf9d/docs/prometheus_setup.md)
and [Grafana](https://github.com/Altinity/clickhouse-operator/blob/eb3fc4e28514d0d6ea25a40698205b02949bcf9d/docs/grafana_setup.md)
installation (if you don’t have one)
- Grafana dashboard [https://github.com/Altinity/clickhouse\-operator/tree/master/grafana\-dashboard](https://github.com/Altinity/clickhouse-operator/tree/master/grafana-dashboard)
- Prometheus alerts [https://github.com/Altinity/clickhouse\-operator/blob/master/deploy/prometheus/prometheus\-alert\-rules\-clickhouse.yaml](https://github.com/Altinity/clickhouse-operator/blob/master/deploy/prometheus/prometheus-alert-rules-clickhouse.yaml)

### Prometheus (ClickHouse external exporter) \+ Grafana

- [clickhouse\-exporter](https://github.com/ClickHouse/clickhouse_exporter)
- Dashboard: <https://grafana.com/grafana/dashboards/882>

(unmaintained)

### Dashboards querying ClickHouse directly via vertamedia / Altinity plugin

- Overview: <https://grafana.com/grafana/dashboards/13606>
- Queries dashboard (analyzing system.query\_log) <https://grafana.com/grafana/dashboards/2515>

## Dashboard querying ClickHouse directly via Grafana plugin

- [https://grafana.com/blog/2022/05/05/introducing\-the\-official\-clickhouse\-plugin\-for\-grafana/](https://grafana.com/blog/2022/05/05/introducing-the-official-clickhouse-plugin-for-grafana/)
- <https://gist.github.com/filimonov/271e5b27c085356c67db3c1bf2204506>

### Zabbix

- <https://www.zabbix.com/integrations/clickhouse>
- [https://github.com/Altinity/clickhouse\-zabbix\-template](https://github.com/Altinity/clickhouse-zabbix-template)

### Graphite

- Use the embedded exporter. See [docs](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-graphite)
and config.xml

### InfluxDB

- You can use embedded exporter, plus Telegraf. For more information, see [Graphite protocol support in InfluxDB](https://docs.influxdata.com/influxdb/v1.7/supported_protocols/graphite/)
.

### Nagios/Icinga

- <https://github.com/exogroup/check_clickhouse/>

### Commercial solution

- Datadog [https://docs.datadoghq.com/integrations/clickhouse/?tab\=host](https://docs.datadoghq.com/integrations/clickhouse/?tab=host)
- Sematext <https://sematext.com/docs/integration/clickhouse/>
- Instana [https://www.instana.com/supported\-technologies/clickhouse\-monitoring/](https://www.instana.com/supported-technologies/clickhouse-monitoring/)
- site24x7 [https://www.site24x7\.com/plugins/clickhouse\-monitoring.html](https://www.site24x7.com/plugins/clickhouse-monitoring.html)
- Acceldata Pulse [https://www.acceldata.io/blog/acceldata\-pulse\-for\-clickhouse\-monitoring](https://www.acceldata.io/blog/acceldata-pulse-for-clickhouse-monitoring)

### “Build your own” ClickHouse monitoring

ClickHouse allows to access lots of internals using system tables. The main tables to access monitoring data are:

- system.metrics
- system.asynchronous\_metrics
- system.events

Minimum necessary set of checks



| **Check Name** | **`Shell or SQL command`** | **`Severity`** |
| --- | --- | --- |
| ClickHouse status | `$ curl 'http://localhost:8123/'``Ok.` | `Critical` |
| Too many simultaneous queries. Maximum: 100 (by default) | `select value from system.metrics``where metric='Query'` | `Critical` |
| Replication status | `$ curl 'http://localhost:8123/replicas_status'``Ok.` | `High` |
| Read only replicas (reflected by `replicas_status` as well) | `select value from system.metrics``where metric='ReadonlyReplica'` | `High` |
| Some replication tasks are stuck | `select count()``from system.replication_queue``where num_tries > 100 or num_postponed > 1000` | `High` |
| ZooKeeper is available | `select count() from system.zookeeper``where path='/'` | `Critical for writes` |
| ZooKeeper exceptions | `select value from system.events``where event='ZooKeeperHardwareExceptions'` | `Medium` |
| Other CH nodes are available | `$ for node in `echo "select distinct host_address from system.clusters where host_name !='localhost'" | curl 'http://localhost:8123/' --silent --data-binary @-`; do curl "http://$node:8123/" --silent ; done | sort -u``Ok.` | `High` |
| All CH clusters are available (i.e. every configured cluster has enough replicas to serve queries) | `for cluster in `echo "select distinct cluster from system.clusters where host_name !='localhost'" | curl 'http://localhost:8123/' --silent --data-binary @-` ; do clickhouse-client --query="select '$cluster', 'OK' from cluster('$cluster', system, one)" ; done` | `Critical` |
| There are files in 'detached' folders | `$ find /var/lib/clickhouse/data/*/*/detached/* -type d | wc -l; \ 19.8+``select count() from system.detached_parts` | `Medium` |
| Too many parts: \\ Number of parts is growing; \\ Inserts are being delayed; \\ Inserts are being rejected | `select value from system.asynchronous_metrics``where metric='MaxPartCountForPartition';``select value from system.events/system.metrics``where event/metric='DelayedInserts'; \ select value from system.events``where event='RejectedInserts'` | `Critical` |
| Dictionaries: exception | `select concat(name,': ',last_exception)``from system.dictionaries``where last_exception != ''` | `Medium` |
| ClickHouse has been restarted | `select uptime();``select value from system.asynchronous_metrics``where metric='Uptime'` |  |
| DistributedFilesToInsert should not be always increasing | `select value from system.metrics``where metric='DistributedFilesToInsert'` | `Medium` |
| A data part was lost | `select value from system.events``where event='ReplicatedDataLoss'` | `High` |
| Data parts are not the same on different replicas | `select value from system.events where event='DataAfterMergeDiffersFromReplica'; \ select value from system.events where event='DataAfterMutationDiffersFromReplica'` | `Medium` |
|  |  |  |

The following queries are recommended to be included in monitoring:

- `SELECT * FROM system.replicas`
	- For more information, see the ClickHouse guide on [System Tables](https://clickhouse.tech/docs/en/operations/system_tables/#system_tables-replicas)
- `SELECT * FROM system.merges`
	- Checks on the speed and progress of currently executed merges.
- `SELECT * FROM system.mutations`
	- This is the source of information on the speed and progress of currently executed merges.

## Monitoring ClickHouse logs

[ClickHouse logs](/altinity-kb-setup-and-maintenance/logging/)
can be another important source of information. There are 2 logs enabled by default

- /var/log/clickhouse\-server/clickhouse\-server.err.log (error \& warning, you may want to keep an eye on that or send it to some monitoring system)
- /var/log/clickhouse\-server/clickhouse\-server.log (trace logs, very detailed, useful for debugging, usually too verbose to monitor).

You can additionally enable system.text\_log table to have an access to the logs from clickhouse sql queries (ensure that you will not expose some information to the users who should not see it).


```
$ cat /etc/clickhouse-server/config.d/text_log.xml
<yandex>
    <text_log>
        <database>system</database>
        <table>text_log</table>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
        <level>warning</level>
    </text_log>
</yandex>

```
## OpenTelemetry support

See <https://clickhouse.com/docs/en/operations/opentelemetry/>

## Other sources

- [https://tech.marksblogg.com/clickhouse\-prometheus\-grafana.html](https://tech.marksblogg.com/clickhouse-prometheus-grafana.html)
- [Key Metrics for Monitoring ClickHouse](https://sematext.com/blog/clickhouse-monitoring-key-metrics/)
- [Monitor ClickHouse with Datadog](https://www.datadoghq.com/blog/monitor-clickhouse/)
- [Unsorted notes on monitor and Alerts](https://docs.google.com/spreadsheets/d/1K92yZr5slVQEvDglfZ88k_7bfsAKqahY9RPp_2tSdVU/edit#gid=521173956)
- <https://intl.cloud.tencent.com/document/product/1026/36887>
- [Tinybird experience (scroll to monitoring section)](https://www.tinybird.co/blog/what-i-learned-operating-clickhouse-part-ii)

Last modified 2026\.01\.06: [Revise ClickHouse and Zookeeper monitoring metrics (17460fa)](https://github.com/Altinity/altinityknowledgebase/commit/17460fa0d0fc4d77ecf3802f28e77c22f27f0e80)
