---
source: kb.altinity.com
url: https://github.com/Altinity/clickhouse-operator/blob/master/docs/quick_start.md
topic: using-the-altinity-kubernetes-operator-for-clickhouse-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '0.0'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 10
---

of fast shutdown there is possibility to loss some data(needs to be clarified) 3. Some cloud providers (GKE) can have slow unlink command, which is important for ClickHouse because it’s needed for parts management. (`max_part_removal_threads` setting) Useful commands:

```
kubectl logs chi-chcluster-2-1-0 -c clickhouse-pod -n chcluster --previous
kubectl describe pod chi-chcluster-2-1-0 -n chcluster

```
Q. ClickHouse is caching the Kafka pod’s IP and trying to connect to the same ip even when there is a new Kafka pod running and the old one is deprecated. Is there some setting where we could refresh the connection

`<disable_internal_dns_cache>1</disable_internal_dns_cache>` in config.xml

### ClickHouse init process failed

It’s due to low value for env `CLICKHOUSE_INIT_TIMEOUT` value. Consider increasing it up to 1 min.
[https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/docker/server/entrypoint.sh\#L120](https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/docker/server/entrypoint.sh#L120)

# 1 \- Istio Issues

Working with the popular service mesh## What is Istio?

Per documentation on [Istio Project's website](https://istio.io/latest/docs/overview/what-is-istio/)
, Istio is “an open source service mesh that layers transparently onto existing distributed applications. Istio’s powerful features provide a uniform and more efficient way to secure, connect, and monitor services. Istio is the path to load balancing, service\-to\-service authentication, and monitoring – with few or no service code changes.”

Istio works quite well at providing this functionality, and does so through controlling service\-to\-service communication in a Cluster, find\-grained control of traffic behavior, routing rules, load\-balancing, a policy layer and configuration API supporting access controls, rate limiting, etc.

It also provides metrics about all traffic in a cluster. One can get an amazing amount of metrics from it. Datadog even has a provider that when turned on is a bit like a firehose of information.

Istio essentially uses a proxy to intercapt all network traffic and provides the ability to configured for providing a appliction\-aware features.

## ClickHouse and Istio

The implications for ClickHouse need to be taken into consideration however, and this page will attempt to address this from real\-life scenarios that Altinity devops, infrastructural, and support engineers have had to solve.

### Operator High Level Description

The Altinity ClickHouse Operator, when installed using a deployment, also creates four custom resources:

- clickhouseinstallations.clickhouse.altinity.com (chi)
- clickhousekeeperinstallations.clickhouse\-keeper.altinity.com (chk)
- clickhouseinstallationtemplates.clickhouse.altinity.com (chit)
- clickhouseoperatorconfigurations.clickhouse.altinity.com (chopconf)
