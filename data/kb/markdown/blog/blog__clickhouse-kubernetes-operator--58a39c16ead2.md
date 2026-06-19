# Introducing the Official ClickHouse Kubernetes Operator: Seamless Analytics at Scale


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing the Official ClickHouse Kubernetes Operator: Seamless Analytics at Scale

![](/_next/image?url=%2Fuploads%2FScreenshot_2026_01_29_at_7_29_42_AM_c2dfdb8b4e.png&w=96&q=75)Grisha PervakovJan 29, 2026 · 5 minutes readAt ClickHouse, our mission has always been to make real\-time analytics accessible and lightning\-fast. As more of our community moves toward cloud\-native architectures, the need for a robust, automated way to manage Open Source ClickHouse distribution on Kubernetes has become clear.


Today, we are thrilled to announce the release of the Official ClickHouse Kubernetes Operator \- available now, open\-source (under Apache\-2\.0 licence), and free for everyone.


## **Why a Kubernetes Operator?** [\#](/blog/clickhouse-kubernetes-operator#why-a-kubernetes-operator)


Running a stateful, high\-performance database like ClickHouse on Kubernetes presents unique challenges: horizontal and vertical scaling, ensuring data persistence during pod restarts, and executing seamless upgrades.


The ClickHouse Operator simplifies these tasks by extending the Kubernetes API. It allows you to manage complex ClickHouse clusters using convenient Custom Resource Definitions (CRDs). Instead of manually configuring Pods and Services, you simply describe your desired state, and the Operator handles the rest.


## **Key Features** [\#](/blog/clickhouse-kubernetes-operator#key-features)


- **Automated Cluster Provisioning:** Deploy a production\-ready, multi\-node cluster with sharding and replication in minutes.
- **ClickHouse Keeper Support:** Deploy and manage ClickHouse Keeper.
- **Vertical \& Horizontal Scaling:** Easily adjust CPU / Memory resources or add new shards to your cluster with minimal downtime.
- **Configuration Management:** Safely update your configuration and ClickHouse version in a single manifest change. The Operator manages the sequence, ensuring that new configuration parameters are rolled out only to updated pods, eliminating the risk of service disruptions caused by version\-config mismatches.
- **Seamless Upgrades:** Perform rolling updates to new ClickHouse versions without dropping queries.


## **Design choices** [\#](/blog/clickhouse-kubernetes-operator#design-choices)


When implementing the operator, we wanted to reuse the ClickHouse Cloud production experience and build on bulletproof, reliable features. That's why we:


- We rely on ClickHouse Keeper for coordination — it’s built in, so you don’t need to run ZooKeeper separately, and there’s no “Keeper\-less” mode to worry about. This [post](https://clickhouse.com/blog/clickhouse-keeper-a-zookeeper-alternative-written-in-cpp) covers the benefits.
- Make the Replicated a default database engine. DatabaseReplicated has been powering ClickHouse Cloud since the beginning of our business and has proved its reliability and convenience. That’s why it was an obvious choice for us to use it in the Operator as well. It eliminates the need to write the ON CLUSTER clause in every DDL query you issue to the database.
- Have a StatefulSet per replica. This key decision allows us to implement different upgrade strategies and have fine\-grained control over each replica (e.g., the version they run, their configuration, etc.).
- TLS/SSL encryption for ClickHouse \<\-\> Keeper and Client \<\-\> ClickHouse communication.
- Configuration overrides for both ClickHouse and Keeper.


In general, our key principle is keeping things simple. If something can be implemented on the ClickHouse side in C\+\+, it has to be there. That made the Operator a very thin layer on top of what ClickHouse already can do.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## **Getting Started: Your First Cluster** [\#](/blog/clickhouse-kubernetes-operator#getting-started-your-first-cluster)


Getting up and running is as simple as applying a few YAML files.


**1\. Install the cert\-manager**


The operator uses defaulting and validating webhooks to ensure the validity of Custom Resource (CR) objects. It requires cert\-manager to issue a certificate.



```

```
1# Using kubectl
2kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.2/cert-manager.yaml
```

```


```

```
1# Or using helmchart
2helm install cert-manager --create-namespace --namespace cert-manager oci://quay.io/jetstack/charts/cert-manager --set crds.enabled=true --version v1.19.2
```

```

**2\. Install the Operator**



```

```
1# Using kubectl
2kubectl apply -f https://github.com/ClickHouse/clickhouse-operator/releases/latest/download/clickhouse-operator.yaml
```

```


```

```
1# Or our helmchart
2helm install clickhouse-operator --create-namespace -n clickhouse-operator-system oci://ghcr.io/clickhouse/clickhouse-operator-helm
```

```

**3\. Deploy a Simple Cluster** Below is a basic example of a Custom Resource (CR) to deploy a two\-node cluster:


YAML CR



```

```
1apiVersion: clickhouse.com/v1alpha1
2kind: KeeperCluster
3metadata:
4  name: sample
5spec:
6  replicas: 3
7  dataVolumeClaimSpec:
8    accessModes:
9      - ReadWriteOnce
10    resources:
11      requests:
12        storage: 10Gi
13---
14apiVersion: clickhouse.com/v1alpha1
15kind: ClickHouseCluster
16metadata:
17  name: sample
18spec:
19  replicas: 2
20  dataVolumeClaimSpec:
21    accessModes:
22      - ReadWriteOnce
23    resources:
24      requests:
25        storage: 10Gi
26  keeperClusterRef:
27    name: sample
```

```

## **Our Commitment to Open Source** [\#](/blog/clickhouse-kubernetes-operator#our-commitment-to-open-source)


We believe that the tools used to manage ClickHouse should be as open as the database itself. This Operator is free to use. We invite the community to contribute, report bugs, and help us shape the roadmap for cloud\-native ClickHouse.


## **Join the Conversation** [\#](/blog/clickhouse-kubernetes-operator#join-the-conversation)


We’d love to hear your feedback!


- **Submit feature requests to GitHub issues:** [https://github.com/ClickHouse/clickhouse\-operator/issues](https://github.com/ClickHouse/clickhouse-operator/issues)
- **Slack:** Join the operator slack channel <https://clickhousedb.slack.com/archives/C0ABN03GJA1>
- **Documentation:** [https://clickhouse.com/docs/clickhouse\-operator/overview](https://clickhouse.com/docs/clickhouse-operator/overview)
- **Mailing list:** [operator@clickhouse.com](mailto:operator@clickhouse.com)


Happy scaling!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
