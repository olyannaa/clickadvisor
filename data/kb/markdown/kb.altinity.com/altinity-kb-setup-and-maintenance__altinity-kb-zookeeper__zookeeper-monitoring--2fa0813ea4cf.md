# ZooKeeper Monitoring \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. [ZooKeeper](/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/)
3. ZooKeeper Monitoring
# ZooKeeper Monitoring

## ZooKeeper

### scrape metrics

- embedded exporter since version 3\.6\.0
	- [https://zookeeper.apache.org/doc/r3\.6\.2/zookeeperMonitor.html](https://zookeeper.apache.org/doc/r3.6.2/zookeeperMonitor.html)
- standalone exporter
	- [https://github.com/dabealu/zookeeper\-exporter](https://github.com/dabealu/zookeeper-exporter)

### Install dashboards

- embedded exporter <https://grafana.com/grafana/dashboards/10465>
- dabealu exporter <https://grafana.com/grafana/dashboards/11442>

See also [https://grafana.com/grafana/dashboards?search\=ZooKeeper\&amp;dataSource\=prometheus](https://grafana.com/grafana/dashboards?search=ZooKeeper&dataSource=prometheus)

### setup alert rules

- embedded exporter [link](https://github.com/Altinity/clickhouse-operator/blob/master/deploy/prometheus/prometheus-alert-rules-zookeeper.yaml)

### See also

- [https://www.datadoghq.com/blog/monitoring\-kafka\-performance\-metrics/\#zookeeper\-metrics](https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics/#zookeeper-metrics)
- [https://dzone.com/articles/monitoring\-apache\-zookeeper\-servers](https://dzone.com/articles/monitoring-apache-zookeeper-servers)
\- note exhibitor is no longer maintained
- [https://github.com/samber/awesome\-prometheus\-alerts/blob/c3ba0cf1997c7e952369a090aeb10343cdca4878/\_data/rules.yml\#L1146\-L1170](https://github.com/samber/awesome-prometheus-alerts/blob/c3ba0cf1997c7e952369a090aeb10343cdca4878/_data/rules.yml#L1146-L1170)
(or [https://awesome\-prometheus\-alerts.grep.to/rules.html\#zookeeper](https://awesome-prometheus-alerts.grep.to/rules.html#zookeeper)
)
- [https://alex.dzyoba.com/blog/prometheus\-alerts/](https://alex.dzyoba.com/blog/prometheus-alerts/)
- [https://docs.datadoghq.com/integrations/zk/?tab\=host](https://docs.datadoghq.com/integrations/zk/?tab=host)
- [https://statuslist.app/uptime\-monitoring/zookeeper/](https://statuslist.app/uptime-monitoring/zookeeper/)

Last modified 2024\.02\.01: [Fixed broken links, other housekeeping (33dff8b)](https://github.com/Altinity/altinityknowledgebase/commit/33dff8b40c62828a1baf7b31d3a22f87a0950e8c)
