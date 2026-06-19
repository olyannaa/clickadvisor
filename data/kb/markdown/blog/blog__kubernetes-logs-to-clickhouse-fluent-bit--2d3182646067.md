# Sending Kubernetes logs To ClickHouse with Fluent Bit


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Sending Kubernetes logs To ClickHouse with Fluent Bit

![calyptia.png](/_next/image?url=%2Fuploads%2Fcalyptia_3be2a5272f.png&w=96&q=75)[Calyptia](/authors/calyptia)Oct 28, 2022 · 11 minutes read![blog_post_kubenetes_calyptia.png](/uploads/blog_post_kubenetes_calyptia_b8c87f8883.png)
This blog post is part of a series:


- [Sending Kubernetes logs To ClickHouse with Fluent Bit](https://clickhouse.com/blog/kubernetes-logs-to-clickhouse-fluent-bit)


## Introduction [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#introduction)


In this post we continue [our series](https://clickhouse.com/blog/nginx-logs-to-clickhouse-fluent-bit) on sending log data to [ClickHouse Cloud](https://clickhouse.cloud/signUp) using Fluent Bit, with a focus on Kubernetes logs. With ClickHouse becoming an increasingly popular backend for receiving logs, and Kubernetes almost a ubiquitous standard for container orchestration and software deployment, Fluent Bit provides a simple and out\-of\-the\-box means of connecting these technologies. We will demonstrate how to deploy FluentBit for Kubernetes log collection, in addition to some simple recommendations on schema design for log data in ClickHouse.


## Environment [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#environment)


- AWS Kubernetes Service v1\.23\.8
- Fluent Bit v1\.9\.9


For ClickHouse, we recommend trying our serverless [ClickHouse Cloud](https://clickhouse.cloud/signUp), which has a generous free trial that is more than sufficient to follow this blog post. Alternatively, all instructions should be compatible with self\-managed versions greater than 22\.6\.


## Kubernetes Logs [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#kubernetes-logs)


In our [previous post](https://clickhouse.com/blog/nginx-logs-to-clickhouse-fluent-bit), we sent raw Nginx logs to ClickHouse. Here we will look at the more advanced use case of Kubernetes Logs. One of the benefits of Fluent Bit is that in addition to parsing the logs into well\-known formats during ingest, we can also enrich logs with context that is useful to operators and practitioners when searching for specific issues.


For example, with Kubernetes, Fluent Bit can talk to the Kubernetes API and enrich each log message with the namespace, pod, and other important information. A diagram showcasing this can be seen below.


![fluent-bit-kubernetes.png](/uploads/fluent_bit_kubernetes_0427f8250b.png)
## Modifying the Helm Chart [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#modifying-the-helm-chart)


To deploy on top of Kubernetes we are going to grab the Fluent Bit Helm charts from the open\-source repository [https://github.com/fluent/helm\-charts](https://github.com/fluent/helm-charts).



```
wget https://github.com/fluent/helm-charts/releases/download/fluent-bit-0.20.9/fluent-bit-0.20.9.tgz
tar -xzvf fluent-bit-0.20.9.tgz
cd fluent-bit

```

We will modify the [values.yaml](https://github.com/fluent/helm-charts/blob/757f8e26184c6bb886950dae7bcda6e2a74a5526/charts/fluent-bit/values.yaml#L309) file, in the root of the `fluent-bit` folder, in two key places. These changes will be used to formulate our Fluent Bit configuration. The Helm chart itself will deploy a [daemonset](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) on each node responsible for log collection.


Under the `filters` key we are going to add the same [nest filter](https://docs.fluentbit.io/manual/pipeline/filters/nest) as our earlier post to move all fields under the `log` column.


While the JSON type is great for the dynamic parts of the logs, we cannot currently use the columns it creates for primary keys. [Primary keys](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-intro) are a key component of accelerating query performance in ClickHouse and should broadly match those columns on which we are most likely to apply filters. For purposes of example, we will later create our table with a primary key on the `host`, `pod_name` and `timestamp` fields \- filtering logs by the host, pod and timestamp seems like a reasonably common usage pattern for Kubernetes logs as a first pass. Obviously, this may vary depending on your use case and typical diagnosis paths, and we encourage users to read about optimizing and configuring primary keys [here](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-design). To use these columns as primary keys we must therefore move them out of the JSON `log` field to the base of the message. To achieve this we use a [lua filter](https://docs.fluentbit.io/manual/pipeline/filters/lua). This is currently necessary as the lift feature of the nest filter is not selective and the [modify filter](https://docs.fluentbit.io/manual/pipeline/filters/modify) is unfortunately [not supported on nested fields](https://github.com/fluent/fluent-bit/issues/2152#issuecomment-1049615508). To achieve this, we set the `luaScripts` key in our [values.yaml](https://github.com/fluent/helm-charts/blob/757f8e26184c6bb886950dae7bcda6e2a74a5526/charts/fluent-bit/values.yaml#L276) file:



```
luaScripts:
  functions.lua: |
    function set_fields(tag, timestamp, record)
          record['host'] = record['log']['kubernetes']['host']
          record['log']['kubernetes']['host'] = nil
          record['pod_name'] = record['log']['kubernetes']['pod_name']
          record['log']['kubernetes']['pod_name'] = nil
          return 2, timestamp, record
    end

```

Our filters configuration thus becomes:



```
## https://docs.fluentbit.io/manual/pipeline/filters
filters: |
  [FILTER]
      Name kubernetes
      Match kube.*
      Merge_Log On
      Keep_Log Off
      K8S-Logging.Parser On
      K8S-Logging.Exclude On

  [FILTER]
      Name nest
      Match *
      Operation nest
      Wildcard *
      Nest_under log

  [FILTER]
    Name lua
    Match *
    script /fluent-bit/scripts/functions.lua
    call set_fields

```

In the [Output section](https://github.com/fluent/helm-charts/blob/757f8e26184c6bb886950dae7bcda6e2a74a5526/charts/fluent-bit/values.yaml#L319) we are going to replace the default Elasticsearch configuration with the ClickHouse HTTP output. Be sure to replace the `host`, `port` and `http_passwd` parameters with your [ClickHouse Cloud](https://clickhouse.cloud/signUp) settings. As a reminder, users can access the HTTP settings from the connection settings of a [ClickHouse Cloud](https://clickhouse.cloud/signUp) service.


![connection-details.gif](/uploads/connection_details_4bf6eb8788.gif)
Note: We’ve used a separate table `kube` for the data vs. the original `jsonlogs` table used in our earlier post. We create this below.



```
## https://docs.fluentbit.io/manual/pipeline/outputs
outputs: |
  [OUTPUT]
    name http
    tls on
    match *
    host <YOUR CLICKHOUSE CLOUD HOST>
    port 8443
    URI /?query=INSERT+INTO+fluentbit.kube+FORMAT+JSONEachRow
    format json_stream
    json_date_key timestamp
    json_date_format epoch
    http_user default
    http_passwd <YOUR PASSWORD>

```

A copy of a full example configuration can be found [here](https://gist.github.com/gingerwizard/7783e1884cb457d7e25cf39f0fe14381).


## Creating the table [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#creating-the-table)


In preparation for the logs, we need to create the table in ClickHouse.


If you haven’t created the database as part of the previous post in this series:



```

CREATE DATABASE fluentbit


```


After creating the database, we are required to enable the JSON object type via the experimental flag `allow_experimental_object_type`, or in [ClickHouse Cloud](https://clickhouse.cloud/signUp) opening a support case:



```

SET allow_experimental_object_type = 1


```


Once set, we can create the table with the provided structure. Note how we specify our primary key via the ORDER BY clause. Explicitly declaring our `host` and `pod_name` columns on the root of the message, rather than relying on ClickHouse to infer them dynamically as simply `String` within the JSON column, allows us to define their types more tightly \- for both we use LowCardinality(String) improving their compression and query performance due to reduced IO. We create the usual `log` column which will contain any other fields in the message.



```

CREATE TABLE fluentbit.kube
(
    timestamp DateTime,
    log JSON,
    host LowCardinality(String),
    pod_name LowCardinality(String)
)
Engine = MergeTree ORDER BY tuple(host, pod_name, timestamp)


```


Once created, we can deploy Fluent Bit to send our Kubernetes logs.


## Applying the Helm Chart [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#applying-the-helm-chart)


We can now deploy the helm chart using the following command in the `fluent-bit` directory:



```
helm install . --generate-name

NAME: chart-1666796050
LAST DEPLOYED: Wed Oct 26 15:54:11 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1

```

To confirm successful installation, list the pods in the default namespace. Note your namespace and response may vary in production environments.:



```
kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
chart-1666796050-fluent-bit-bczgc   1/1     Running   0          65s
chart-1666796050-fluent-bit-mw27h   1/1     Running   0          65s

```

After a few minutes we should begin to see logs start to flow to ClickHouse. From the [clickhouse\-client](https://clickhouse.com/docs/en/interfaces/cli/) we perform a simple SELECT. Note the `FORMAT` option is required to return rows in JSON format and we focus on log messages where a host and pod\_name could be extracted.



```

SET output_format_json_named_tuples_as_objects = 1
SELECT * FROM fluentbit.kube LIMIT 10 FORMAT JSONEachRow


```



```

clickhouse-cloud :) SELECT * FROM fluentbit.kube WHERE host != '' AND pod_name != '' LIMIT 2 FORMAT JSONEachRow

SELECT *
FROM fluentbit.kube
WHERE (host != '') AND (pod_name != '')
LIMIT 1
FORMAT JSONEachRow


```



```
{
  "timestamp": "2022-10-26 15:13:41",
  "log": {
    "kubernetes": {
      "annotations": {
        "checksum/config": "9787019d9ab49da594ab2636487dd89fbe22cc819fa100b97534277015b9a22d",
        "checksum/luascripts": "84ee9e1eee2352af076ebec7a96ff7bcfd6476d4da3aa09c7c02c3b2902a768f",
        "kubernetes.io/psp": "eks.privileged"
      },
      "container_hash": "",
      "container_image": "cr.fluentbit.io/fluent/fluent-bit:1.9.9",
      "container_name": "fluent-bit",
      "docker_id": "80c28b724a3c18e5847c887d5a1d5f7df5bf1335b0b49e50e82fd6a43d4f7131",
      "labels": {
        "app.kubernetes.io/instance": "chart-1666797215",
        "app.kubernetes.io/name": "fluent-bit",
        "controller-revision-hash": "96df88b78",
        "k8s-app": "",
        "pod-template-generation": "1"
      },
      "namespace_name": "default",
      "pod_id": "388d2e57-1239-45cc-9b63-3a69b96050ac"
    },
    "log": "[2022/10/26 15:13:41] [error] [output:http:http.0] qm5u2tm7n9.us-east-2.aws.clickhouse.cloud:8443, HTTP status=404\n",
    "stream": "stderr",
    "time": "2022-10-26T15:13:41.445772997Z"
  },
  "host": "ip-192-168-88-154.us-east-2.compute.internal",
  "pod_name": "chart-1666797215-fluent-bit-blz9c"
}

```

We can now analyze these similarly to our Nginx access logs e.g., the question “how many logs were sent per Kubernetes namespace?” can be answered with a simple GROUP BY:



```

clickhouse-cloud :) SELECT
    count(),
    namespace
FROM fluentbit.kube
GROUP BY log.kubernetes.namespace_name AS namespace

┌─count()─┬─namespace───┐
│      12 │             │
│    2680 │ default     │
│      14 │ kube-system │
└─────────┴─────────────┘

3 rows in set. Elapsed: 0.006 sec. Processed 2.71 thousand rows, 43.27 KB (453.55 thousand rows/s., 7.25 MB/s.)


```


## Visualizing the Kubernetes data [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#visualizing-the-kubernetes-data)


In our [earlier post](https://clickhouse.com/blog/nginx-logs-to-clickhouse-fluent-bit) we used the [Explore feature](https://grafana.com/docs/grafana/latest/explore/) of Grafana to visualize our logs. While useful for an exploratory analysis, users typically prefer to dashboard logs and link these to other sources e.g., tracing and metrics. Using the above dataset, we can build a very simple dashboard to visualize the state of our Kubernetes cluster. This dashboard can be downloaded from [here](https://grafana.com/grafana/dashboards/17284) and [imported into Grafana](https://grafana.com/docs/grafana/v9.0/dashboards/export-import/) as shown below \- note the dashboard id `17284`. A read\-only version is also published [here](https://snapshots.raintank.io/dashboard/snapshot/yz0rOGp68hwiFN5dTz1syFY2Gd2D097z?orgId=2). Feel free to expand and enrich this with your own data and please share your results! Note we equate the host to be the same as the Kubernetes node for the purpose of this dashboard. For further details using the official Grafana plugin for ClickHouse, see [here](https://clickhouse.com/docs/en/connect-a-ui/grafana-and-clickhouse).


![dashboard-grafana-k8-logs.gif](/uploads/dashboard_grafana_k8_logs_238ae799b5.gif)
## Best Practices [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#best-practices)


An initial benefit of the new JSON settings within ClickHouse is we do not have to specify the schema of nested JSON; everything works out of the box. Any new fields which appear in the logs will automatically have new columns created for them within ClickHouse. We encourage users to use this capability for dynamic columns only. For fields which are expected to be on each message, and for which the type is known, we encourage users to lift these out of a JSON field to the root and explicitly define their type. Additionally, remove unused fields to minimize storage where possible and avoid column explosion. Your lua script may therefore be a lot longer in any production setting. As well as allowing more explicit typing e.g., lower precision integer, for better performance, users can also exploit codecs for compression.


**Note: The JSON Object type is experimental and is undergoing improvements. Our advice with respect to this feature is evolving and may therefore change in later versions.**


Finally, by default the Fluent Bit Helm chart configures a [batch to be flushed](https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/classic-mode/configuration-file) [every 1s](https://github.com/fluent/helm-charts/blob/757f8e26184c6bb886950dae7bcda6e2a74a5526/charts/fluent-bit/values.yaml#L248). ClickHouse prefers batches [of at least 1000 records](https://clickhouse.com/docs/en/about-us/performance/#performance-when-inserting-data). You may wish to tune this flush time depending on the volume of logs generated by your Kubernetes cluster to [avoid common issues](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse).


## Conclusion [\#](/blog/kubernetes-logs-to-clickhouse-fluent-bit#conclusion)


In this blog we set up Fluent Bit to route logs from a Kubernetes Environment to ClickHouse for expedited analysis. We have touched on how the new experimental JSON type can be used to assist with storing log data and provided some simple best practices around its usage. In future blog posts, we’ll demonstrate storing log data at scale and building an end\-to\-end Observability solution.


*If you’re enthusiastic about the latest technologies and are passionate about Open Source, we’re currently hiring for our [integrations team](https://clickhouse.com/company/careers) and would love to hear from you.*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
