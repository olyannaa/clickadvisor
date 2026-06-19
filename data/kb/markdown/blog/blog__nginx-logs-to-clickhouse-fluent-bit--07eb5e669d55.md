# Sending Nginx logs to ClickHouse with Fluent Bit


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Sending Nginx logs to ClickHouse with Fluent Bit

![calyptia.png](/_next/image?url=%2Fuploads%2Fcalyptia_3be2a5272f.png&w=96&q=75)[Calyptia](/authors/calyptia)Oct 21, 2022 · 8 minutes read![calypia-blog.png](/uploads/calypia_blog_97dbedcd22.png)
This blog post is part of a series:


- [Sending Kubernetes logs To ClickHouse with Fluent Bit](https://clickhouse.com/blog/kubernetes-logs-to-clickhouse-fluent-bit)


## Introduction [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#introduction)


ClickHouse has become a popular backend for receiving logs after users like [Uber incorporated the blazing\-fast](https://www.uber.com/en-PT/blog/logging/) database into their infrastructure. One common challenge with all data stores is how to ingest data from various sources. Thankfully this is a challenge that the Cloud Native Computing Foundation (CNCF) project Fluent Bit has solved for many backends, such as Amazon. Fluent Bit is a super fast, lightweight, and highly scalable logging and metrics processor and forwarder.


In this blog, we walk through how to set up Fluent Bit to route logs to Clickhouse in under 5 minutes. In our next post, we will showcase an everyday observability use case of collecting and enriching logs from Kubernetes.


## Environment [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#environment)


- Ubuntu 20\.04 LTS running both Clickhouse and [Calypita Fluent Bit](https://calyptia.com/download/) (LTS version of Fluent Bit provided by the creators)
- Fluent Bit v1\.9\.9


For ClickHouse, we recommend trying our serverless [ClickHouse Cloud](https://clickhouse.cloud/signUp), which has a generous free trial that is more than sufficient to follow this blog post. Alternatively, all instructions should be compatible with self\-managed versions greater than 22\.6\.


## Creating the ClickHouse Database and Tables [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#creating-the-clickhouse-database-and-tables)


Our first step is to create a database within ClickHouse where we will store the logs. We can run the following command via the [clickhouse\-client](https://clickhouse.com/docs/en/interfaces/cli/) or via your ClickHouse Cloud console:



```

CREATE DATABASE fluentbit


```


Note that the **[JSON type](https://clickhouse.com/docs/en/sql-reference/data-types/json/) is currently experimental** in ClickHouse core database and not enabled by default in [ClickHouse Cloud](https://clickhouse.cloud/signUp). Should users wish to use this capability in [ClickHouse Cloud](https://clickhouse.cloud/signUp), they can open a support case once they’ve started a service.


After creating the database, we are required to enable the JSON object type via the experimental flag `allow_experimental_object_type`:



```

SET allow_experimental_object_type = 1


```


Once set, we can create the table with the provided structure. This creates a field `log` that contains all the JSON objects.



```

CREATE TABLE fluentbit.jsonlogs
(
    timestamp DateTime,
    log JSON
)
Engine = MergeTree ORDER BY tuple()


```


Once created, we can configure Fluent Bit to send data.


## Configuring Fluent Bit on Ubuntu [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#configuring-fluent-bit-on-ubuntu)


The instructions below use the open source version of Fluent Bit. If you are interested in using an LTS version with additional premium features, you find more information on Calyptia’s offering [here](https://calyptia.com/products/).


For example purposes, we send basic Nginx access logs and assume the user is using an Ubuntu system. For other systems, instructions are available [here](https://docs.fluentbit.io/manual/installation/getting-started-with-fluent-bit#install-on-linux-packages):



```
curl https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh

```

This will install Fluent Bit to /opt/fluent\-bit. If you need some test Nginx Access Logs, you can download a series of mock access logs from [here](https://gist.githubusercontent.com/agup006/b936d299c11b60283bdaf05a12e334eb/raw/b87905c7ea1e21745dba87233666135ee61d0087/apache-access.log) and place them under `/var/log/access.log`.



```
sudo wget -O /var/log/access.log https://gist.githubusercontent.com/agup006/b936d299c11b60283bdaf05a12e334eb/raw/b87905c7ea1e21745dba87233666135ee61d0087/apache-access.log
sudo chmod a+r /var/log/access.log

```

As a high\-level intro to Fluent Bit configuration we designate a set of [Inputs](https://docs.fluentbit.io/manual/pipeline/inputs), [Filters](https://docs.fluentbit.io/manual/pipeline/filters), and [Outputs](https://docs.fluentbit.io/manual/pipeline/outputs). On the Input side, we are going to specify the [`tail`](https://docs.fluentbit.io/manual/pipeline/inputs/tail) plugin which will read the access logs and parse in with a well\-known format.


Once these logs are parsed, we will then use a Fluent Bit [Nest Filter](https://docs.fluentbit.io/manual/pipeline/filters/nest) to nest all fields under a field “log”, allowing ClickHouse to recognize the field where the [JSON object](https://clickhouse.com/docs/en/guides/developer/working-with-json/json-intro) will be housed.


Last but not least, we will use Fluent Bit’s [HTTP output](https://docs.fluentbit.io/manual/pipeline/outputs/http) plugin to route these logs to ClickHouse with a few parameters. You can see from the URI that we are using the database and table that we created earlier.


### Fluent Bit configuration [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#fluent-bit-configuration)


**Note:** We also need to specify the default user’s password for Fluent Bit to make use of HTTP Basic Authentication. For [ClickHouse Cloud](https://clickhouse.cloud/signUp) we specify port 8443 and enable SSL via the `tls on` parameter. Users using self\-managed ClickHouse may need to use the port 8143 if your cluster is not secure. You will also need to explicitly set the use of http, i.e. `tls off` parameter.


Append the following configuration file to `/etc/fluent-bit/fluent-bit.conf`.



```

[INPUT]
    name tail
    path /var/log/access.log
    read_from_head true
    parser nginx_access

[FILTER]
    Name nest
    Match *
    Operation nest
    Wildcard *
    Nest_under log 

[OUTPUT]
    name http
    tls on
    match *
    host 
    port 8443
    URI /?query=INSERT+INTO+fluentbit.jsonlogs+FORMAT+JSONEachRow
    format json_stream
    json_date_key timestamp
    json_date_format epoch
    http_user default
    http_passwd 


```


If using [ClickHouse Cloud](https://clickhouse.cloud/signUp), your credentials will be available when you create your cluster i.e.


![connect_cloud.png](/uploads/connect_cloud_d46c740325.png)
Run Fluent Bit, and send the logs to ClickHouse, with the following command:



```
/opt/fluent-bit/bin/fluent-bit -c /etc/fluent-bit/fluent-bit.conf

```

## Searching the logs in ClickHouse [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#searching-the-logs-in-clickhouse)


Within ClickHouse we can run the following to see our logs in action. Without the [FORMAT](https://clickhouse.com/docs/en/sql-reference/statements/select/format/#default-format) option we only see the values of our JSON.



```

SET output_format_json_named_tuples_as_objects = 1

SELECT * FROM fluentbit.jsonlogs FORMAT JSONEachRow


```


[![logs.png](/uploads/logs_9043688a6c.png)](/uploads/logs_9043688a6c.png)
A benefit with these logs now in ClickHouse is we can run adhoc queries for analysis without having to designate any schema. Using the [DESCRIBE](https://clickhouse.com/docs/en/sql-reference/statements/describe-table/) command, with the setting [`describe_extend_object_types`](https://clickhouse.com/docs/en/guides/developer/working-with-json/json-semi-structured/#json-object-type), we can discover the available fields in our jsonlogs table.



```

DESCRIBE TABLE fluentbit.jsonlogs
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Row 1:
──────
name:               timestamp
type:               DateTime
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:

Row 2:
──────
name:               log
type:               Tuple(agent String, code String, host String, method String, path String, referer String, remote String, size String, user String)
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:

2 rows in set. Elapsed: 0.001 sec.


```


We can run the following command to understand how many error codes are returned \- note how we access the code field via its dot delimited json path.



```

SELECT
    count(log.code) AS count,
    log.code AS code
FROM fluentbit.jsonlogs
GROUP BY log.code

┌─count─┬─code─┐
│    26 │ 301  │
│     9 │ 500  │
│   397 │ 200  │
│    17 │ 404  │
└───────┴──────┘

4 rows in set. Elapsed: 0.003 sec.


```


For users interested in visualizing these logs, we recommend Grafana and the officially supported ClickHouse plugin. Further details can be found [here](https://clickhouse.com/docs/en/connect-a-ui/grafana-and-clickhouse) with an example of visualizing JSON logs at the end of this [earlier post](https://clickhouse.com/blog/visualizing-data-with-grafana). Below we show the above data in the Logs view of Grafana.


[![grafana-logs.png](/uploads/grafana_logs_a00eb90de0.png)](/uploads/grafana_logs_a00eb90de0.png)
Note: ensure your Grafana instance has access to your [ClickHouse Cloud](https://clickhouse.cloud/signUp) service with appropriate IP Access List rules.


## Summary [\#](/blog/nginx-logs-to-clickhouse-fluent-bit#summary)


In this post we have loaded Nginx logs into ClickHouse using Fluent Bit and the JSON type. In the next post in this series, we will explore a common Observability use case of collecting Kubernetes Logs.


*If you’re enthusiastic about the latest technologies and are passionate about Open Source, we’re currently hiring for our [integrations team](https://clickhouse.com/company/careers) and would love to hear from you.*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
