---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-the-official-clickhouse-kubernetes-operator-seamless-analytics-at-scale-clickhouse
ch_version_introduced: '1.19'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 3
---

manages the sequence, ensuring that new configuration parameters are rolled out only to updated pods, eliminating the risk of service disruptions caused by version\-config mismatches. - **Seamless Upgrades:** Perform rolling updates to new ClickHouse versions without dropping queries.

## **Design choices** \#

When implementing the operator, we wanted to reuse the ClickHouse Cloud production experience and build on bulletproof, reliable features. That's why we:

- We rely on ClickHouse Keeper for coordination — it’s built in, so you don’t need to run ZooKeeper separately, and there’s no “Keeper\-less” mode to worry about. This [post](https://clickhouse.com/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp) covers the benefits.
- Make the Replicated a default database engine. DatabaseReplicated has been powering ClickHouse Cloud since the beginning of our business and has proved its reliability and convenience. That’s why it was an obvious choice for us to use it in the Operator as well. It eliminates the need to write the ON CLUSTER clause in every DDL query you issue to the database.
- Have a StatefulSet per replica. This key decision allows us to implement different upgrade strategies and have fine\-grained control over each replica (e.g., the version they run, their configuration, etc.).
- TLS/SSL encryption for ClickHouse \<\-\> Keeper and Client \<\-\> ClickHouse communication.
- Configuration overrides for both ClickHouse and Keeper.

In general, our key principle is keeping things simple. If something can be implemented on the ClickHouse side in C\+\+, it has to be there. That made the Operator a very thin layer on top of what ClickHouse already can do.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=1)

## **Getting Started: Your First Cluster** \#

Getting up and running is as simple as applying a few YAML files.

**1\. Install the cert\-manager**

The operator uses defaulting and validating webhooks to ensure the validity of Custom Resource (CR) objects. It requires cert\-manager to issue a certificate.

```
1# Using kubectl
2kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.2/cert-manager.yaml
```
Copy command

```
1# Or using helmchart
2helm install cert-manager --create-namespace --namespace cert-manager oci://quay.io/jetstack/charts/cert-manager --set crds.enabled=true --version v1.19.2
```
Copy command
**2\. Install the Operator**

```
1# Using kubectl
2kubectl apply -f https://github.com/ClickHouse/clickhouse-operator/releases/latest/download/clickhouse-operator.yaml
```
Copy command
