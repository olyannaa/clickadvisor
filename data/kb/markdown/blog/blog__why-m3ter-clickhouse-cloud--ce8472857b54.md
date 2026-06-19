# Why m3ter chose ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Why m3ter chose ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FJonathan_Hill_Profile_Image_fefea2ada9.jpeg&w=96&q=75)Jonathan HillJan 14, 2025 · 21 minutes read[Usage\-based pricing](https://www.m3ter.com/guides/usage-based-pricing) is becoming increasingly common, particularly in software as a service (SaaS) companies. Adoption of usage\-based pricing has become mainstream, [increasing from 27% of SaaS companies in 2018 to 61% in 2023](https://openviewpartners.com/blog/state-of-usage-based-pricing/) (as per OpenView Venture Partners).


m3ter is dedicated to addressing significant gaps in automated billing for mid\-size and enterprise companies, providing a service to turn customer usage data into bill line items, supporting the most complex usage based (and hybrid) pricing scenarios.


At [m3ter,](http://www.m3ter.com) we have two categories of data \- a "control" plane which includes all the configuration data (which is relatively small in size) that customers can define to determine how their raw usage data is rated and turned into bill line items, and a "data" plane which contains all of the usage data (which can be very large in size).


The high level architecture diagram below shows how this all links together in the m3ter service:


![m3ter_diagram.png](/uploads/m3ter_diagram_3176e644e0.png)
Handling the control plane data is relatively easy \- due to the relatively low volume of data, and of updates to it, a standard OLTP database can handle this.


The data plane, on the other hand, is more problematic. Customers can send hundreds of millions of usage "events" per month, so the overall data volume is very high.


m3ter offers a variety of powerful features to customers:


- Elimination of duplicate usage data
- Ability to fix configuration errors and recalculate the current bill with the new configuration, without having to re\-ingest all the usage data
- Change pricing, end\-customer plans (e.g. moving from "production" to "enterprise" tier), etc. at any point in time, including midway through a billing period
- Deletion of usage data sent incorrectly by the customer, according to criteria specified by the customer (e.g. time range, type of usage data, etc.)
- Frequent updates of bills to show near\-realtime usage and cost
- Pricing experimentation \- the ability to rate usage against multiple configurations to determine the impact of proposed pricing changes


Many services that deal with large volumes of data will pre\-aggregate the data as it is received, so that later queries against the data actually operate against a smaller dataset. However, pre\-aggregation is not compatible with some of the above features. For example, in order to pre\-aggregate data, you need to know exactly how the data needs to be aggregated prior to any queries being run \- which can prevent changing the configuration and recalculating bills without having to re\-ingest the usage data (so that it can be pre\-aggregated again with the new configuration). In some cases, this is difficult or even impossible for customers (e.g. if the raw data hasn’t been retained) \- whereas with m3ter, it’s always possible because we retain the unaggregated data. When a "retrospective" configuration change is made, there is no need for the customer to re\-send the usage data.


Additionally, at m3ter we don’t want our engineers spending significant time on "undifferentiated heavy lifting" \- where possible, we prefer to use managed services, and that extends to our database and storage solutions.


These features lead to the following key requirements for our data plane storage solution:


- Usage data cannot be pre\-aggregated, i.e. must be stored unaggregated
- Frequent, fast, aggregation of large volumes of data using a variety of "configurations" (i.e. queries, which could change at any point in time for a given customer data set)
- Deletion of usage data according to criteria specified by customers
- Duplicate elimination
- Managed database service


## ClickHouse Cloud [\#](/blog/why-m3ter-clickhouse-cloud#clickhouse-cloud)


We’ll use the majority of this post to explore why we chose ClickHouse Cloud. Performance has been several orders of magnitude better than our previous solution could provide, and we’re achieving this at a significantly lower cost too!


Compared to our previous solution, we are currently achieving:


- 10x more ingested rows per second on average
- 17x more queries per second on average (27x at peak)


ClickHouse also achieves an impressive overall compression ratio of 11\.4x (i.e. every 1 TiB of "raw" data compresses to around 90 GiB on disk), which is significantly better than our previous solution (presumably due to better algorithms combined with columnar storage).


Despite this increased workload, queries run in under 100ms on average. To put this into perspective, our PoC tests showed that for one particular test, ClickHouse Cloud managed an average query duration of 144ms, while RedShift (scaled so that the cost of running it would be roughly the same as the ClickHouse deployment) came in significantly slower at 3927ms, a difference of \~27x. We still believe that RedShift is a fine tool, but it just isn't well\-suited to our particular workload.


This is all being achieved with an average resource usage of 10 vCPUs, and 25 GiB of memory. We can reasonably expect to scale to 10\-100x of our current workload before starting to hit the limits of an "off the shelf" deployment.


In terms of overall cost savings, the headline figure is that we are currently saving \~85% compared to our previous database solution for rating.


We also save additional costs on engineering resources, due to ClickHouse Cloud being a managed service. For example, due to the fact that our ClickHouse Cloud deployment primarily stores data in S3 (providing near\-limitless, relatively cheap storage) we no longer have to spend time adjusting the amount of disk space available to the database.


We’ll now explore in detail how we arrived at choosing ClickHouse Cloud vs other possible solutions.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Comparison [\#](/blog/why-m3ter-clickhouse-cloud#comparison)


In order to choose which database would best fit our requirements, we undertook proof of concept (PoC) projects with several databases, which covered a range of technologies and features. Each of these was assessed against a set of criteria:


- Ability to store large volumes of data easily
- Sustain high rate of data ingest
- Eliminate duplicate data
- Ease of data ingest
- Query performance for highly concurrent, frequent, queries against large volumes of data
- Support for bulk data export
- Support for data deletion
- Ability to monitor both high\-level and low\-level performance
- Easily scalable with zero downtime
- High availability (HA) and Disaster recovery (DR)
- Overall cost of solution
- Miscellaneous other criteria


For some criteria, we defined initial targets to help us make impartial and unbiased comparisons. The targets we defined were minimum targets \- if a database failed to meet these minimums, it was discounted as a possible solution. Where possible, we pushed the database further, in a destructive load test, to see what kind of load we could expect to achieve.


The databases we identified for PoC testing were:


- ClickHouse Cloud
- Snowflake
- Firebolt
- Amazon Redshift
- Amazon Aurora (Postgres)


Note that we included Aurora in order to cover our bases. We didn’t particularly expect great performance from a row\-based OLTP database for the specific type of workload we would be running (which is more analytical in nature). In that sense, comparing the other options to Aurora felt unfair, since it’s targeted at a different use\-case, but we included it to give ourselves confidence that we had covered a range of database choices and technology.


When testing these solutions, we tried various table schemas and tried to take advantage of any unique features that they might offer to improve performance. It’s important to note that in many cases, there is a trade\-off \- for example, adding an index on a table might speed up queries, but slow down ingestion. Similarly, scaling a solution up to provide more hardware oomph can result in better performance, but at a higher cost.


In all cases, we used a fixed set of data and queries, representing our real\-world workloads. The source dataset was identical for all solutions. Queries varied slightly between solutions, due to the different schemas and features available, but in all cases we always queried for the same set of results for a fair comparison.


Let’s look at some of the highlights (and lowlights) of what we found.


## Storage Volume [\#](/blog/why-m3ter-clickhouse-cloud#storage-volume)


All of the above databases were capable of storing large quantities of data, which isn’t a great surprise since they are all (with the exception of Aurora) primarily designed to handle OLAP workloads. Services such as Aurora and Timescale scored lower for this criteria, because data is stored on traditional disks (e.g. SSDs). As the amount of data stored increases, we would have to scale up the service to provide more disk space. In contrast, services such as [ClickHouse Cloud](https://clickhouse.com/cloud) scored more highly, because they don’t carry this operational overhead \- data is offloaded to storage such as S3 automatically, and only the hot dataset is stored on local disks, meaning we wouldn’t have to worry about disks getting full.


We also found that data compression in some solutions was limited \- row\-based solutions didn’t exhibit the same compression ratios as some of the other candidates. Column\-based storage tends to achieve better compression ratios, because you’re compressing a column of data (rather than rows) at a time. Since all the data in a given column is typically similar, higher compression ratios can be achieved.


## Ingest [\#](/blog/why-m3ter-clickhouse-cloud#ingest)


For the configurations we tested, all of the candidates could meet the required target. However, we did note that Aurora started to slow down as the table grew, and internal maintenance operations started to consume more time and resources. We achieved up to \~100k rows per second with the Aurora configuration we tested against, which certainly isn’t bad for a row\-based OLTP database. However, this paled in comparison with some of the other solutions, which were all able to achieve much higher (e.g. 10x) rates. An additional concern here was that Aurora is only scalable (for writes) by scaling a single "writer" node up, whereas other solutions could be scaled horizontally and the workload potentially distributed across multiple nodes, which would allow a higher top\-end cap on this.


We did find that ingesting large batches of data into Firebolt took longer than we initially expected, in the sense that the ingest "query" took quite a long time to return an OK response to the client. This was explained to us as being various data integrity checks that Firebolt perform before the ingest request is deemed to be completed. (It’s also worth noting that we were told this would improve as it was being actively worked on \- so it’s entirely possible that at the time of writing, this has been improved). Whilst this didn’t affect the overall throughput, it did affect how fast data was actually available to be queried, so was a slight concern to us.


One point worth mentioning is that at the time we assessed these services, Snowflake and Redshift offered the best ecosystem in terms of data ingest. For example, Snowflake offered Snowpipes which allow continual ingest from data streams, and Redshift offers similar integration with Kinesis streams. At that time, ClickHouse Cloud didn’t have an equivalent offering, so we had to write our own ETL and ingest pipelines. This has since changed, with the release of Clickpipes \- however, since these were not available at the time we performed our PoC, Snowflake scored highest in this regard.


## Duplicate Elimination [\#](/blog/why-m3ter-clickhouse-cloud#duplicate-elimination)


When customers send data, they can assign a unique ID (UID) to each measurement. This allows us to easily deal with scenarios such as network errors, where the customer isn’t certain if measurements they send were received by m3ter or not. By assigning a UID to each piece of data, it can be resent, safe in the knowledge that m3ter will de\-duplicate the data, and that usage won’t be double\-counted on bills.


Traditional OLTP databases such as Aurora excel at this task \- a simple unique index on the UID field ensures that no duplicates can be inserted into the database. Other databases, such as ClickHouse Cloud, Snowflake, Firebolt and Redshift have limited support for this, due to the way they store and index data. Typically, some features are available to help with this \- for example, ClickHouse Cloud can remove duplicate rows when its [internal "merge" background process](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage) runs. However, until this happens (and there is [no guarantee exactly](https://clickhouse.com/docs/en/guides/replacing-merge-tree#merge-behavior-considerations) when this will happen since it is an internal process), the duplicates exist on the database and would affect query results. (Note that in ClickHouse, a FINAL keyword can be included in the query to ensure deduplication at query time, but comes at the expense of query performance). For these systems, we would need to implement our own row\-level de\-duplication process before data is inserted into the database. This adds complexity and engineering overhead to any potential solution, and meant these systems received a lower score compared to Aurora.


## Query Performance [\#](/blog/why-m3ter-clickhouse-cloud#query-performance)


This was pretty mixed. As expected, row\-based solutions generally performed more poorly, with IO being the major bottleneck, because entire rows of data needed to be read from disk even if not every column of data was needed to fulfil the query.


Solutions such as ClickHouse Cloud and Snowflake performed well here \- we easily achieved our target, with sustained rates of hundreds of queries per second.


Redshift was more of a struggle \- although we did hit our target, we couldn’t get a high degree of confidence that we could continue to scale this in future. Redshift is geared more towards traditional OLAP queries \- that is, a smaller number of very complex queries. Our tests involved a large number of simple queries (where by "simple", I mean that relative to the big beasts I’ve seen before in some OLAP workloads). We also had a concern about the vacuuming process that Redshift uses in the background \- this can result in occasional "blips" in service throughput whilst significant resource is spent on this process. Although all mature databases have some similar or equivalent background processes running, we didn’t experience any performance degradation from ClickHouse Cloud or Snowflake caused by this.


Firebolt similarly achieved the query throughput target, but we found that although scaling the service horizontally did increase the throughput we could achieve, it didn’t scale as well as some other services managed. Although this means we could continue to scale out as our workload grew, we would see diminishing returns on the extra hardware we were paying for. (To be fair, no service scales perfectly, and all of them will exhibit some diminishing returns \- but some services were notably better than others in this particular respect).


## Data Export [\#](/blog/why-m3ter-clickhouse-cloud#data-export)


It was possible to export data (e.g. as the result of a query) from all of the candidates being tested. However, some services made this much easier and more efficient than others. For example, ClickHouse Cloud offers an [S3 table function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3), allowing export of query results directly to files in S3\. Some of the other options would require us to write some export code to achieve the same result, which would mean higher maintenance and operational costs (in terms of human resource).


## Data Deletion [\#](/blog/why-m3ter-clickhouse-cloud#data-deletion)


All of the databases supported data deletion, although some were more performant than others.


Aurora, as a traditional OLTP database, handled data deletion very well, and scored highly. Solutions including ClickHouse Cloud do support data deletions, but due to the column\-store nature of these databases, the deletion can be somewhat more heavy\-weight than for row\-based databases.


Additionally, some features such as aggregated views are only updated by insert triggers, meaning that if we did want to pre\-aggregate data using views to enhance performance, the view would need manually updating for each data deletion. In reality, since we didn’t intend to use these pre\-aggregated views, this wasn’t a problem for us and therefore didn’t affect our scoring, but it was worth bearing in mind in case we ever did find use\-cases for these features.


## Monitoring [\#](/blog/why-m3ter-clickhouse-cloud#monitoring)


All of the candidates offered some monitoring out of the box. Firebolt (at the time of testing) was lacking somewhat in this regard, with no obvious way from the UI to observe CPU, memory, or disk usage. This may well have changed since then, and it may also be possible to obtain this data via SQL queries or similar \- however, this would mean more work for us to implement.


Other services generally offered better out\-of\-the\-box monitoring tooling, and some, allowed detailed metrics to be obtained at a per\-query level. ClickHouse Cloud was the overall winner here, with easy to consume [graphs showing high\-level metrics](https://clickhouse.com/docs/en/operations/monitoring) such as CPU, memory, etc. and their [query\_log table](https://clickhouse.com/docs/en/operations/system-tables/query_log) tracking resources usage at an individual query level, allowing for more detailed analytics and debugging.


![example_monitoring.png](/uploads/example_monitoring_b6887a3a60.png)
*Example ClickHouse monitoring*
## Scaling [\#](/blog/why-m3ter-clickhouse-cloud#scaling)


Many of the services tested offer automatic scaling based on workload. This was attractive to us, since we don’t want to spend our engineers' time monitoring the performance and scaling services up and down regularly.


In practice, sadly, we found that none of these were quite right for our use\-case, and in general are a bit trigger\-happy when scaling up (or out) to larger instances. For example, a workload which is generally fine but contains the occasional "big" query could trigger the service to think it needed more resources, when in reality we were OK with it just taking a little bit longer for 1% of queries. We believe this is a consequence of our fairly unique workload, and auto\-scaling would probably work very well for many people. Just not for us, sadly. Fortunately, ClickHouse Cloud offers a [scaling API](https://clickhouse.com/docs/en/manage/scaling#horizontal-scaling-via-api) meaning that we could easily scale the service based on our own scaling algorithm and requirements.


Some services (such as Aurora) do offer a "serverless" option, where you are charged based on the number/duration of queries rather than by the deployed instance sizes. However, as is typical with these offerings, this becomes quite expensive quite quickly when running heavier workloads, and are better suited to smaller or spikier workloads. Our workload is both large and continuous, so in our particular case, serverless offerings don’t offer the best value for money and were therefore discounted.


## HA/DR [\#](/blog/why-m3ter-clickhouse-cloud#hadr)


There was relatively little to choose between services for this criteria. Nearly all of the candidates offered good HA, with instances deployed as clusters of nodes, into multiple AWS availability zones.


At the time of our testing, Redshift didn’t offer multi\-AZ configurations, although this feature was available in preview. Given we wanted to migrate ASAP, and multi\-AZ wasn’t available for general release at that time, Redshift scored lower on this point.


Similarly, DR was covered by backup strategies offered by all candidate systems, although some services such as ClickHouse Cloud, which stores all of the data in S3 (and copies hot data to fast local disks), have the additional benefit that S3 itself offers high reliability and redundancy out of the box, so the probability of encountering a DR scenario is reduced.


## Overall Cost [\#](/blog/why-m3ter-clickhouse-cloud#overall-cost)


Balancing the competing requirements, e.g. ingest rate vs. query performance, means that it’s difficult to assess which service truly offers the best "value for money". This is where our initial targets proved their worth again. We tested each service at the fixed target rate of ingest and query throughput, and scaled each service down to the smallest configuration which could hit those targets.


When assessing this criteria, we had to account for both compute and storage costs. We calculated storage costs for a fixed data set which represented the amount of data we need to store in our production environment.


ClickHouse Cloud was the clear winner here, being significantly cheaper in terms of raw performance per dollar spent, when scaled to the minimum configuration needed to hit our targets.


## Miscellaneous [\#](/blog/why-m3ter-clickhouse-cloud#miscellaneous)


As well as the above, we also considered criteria such as which regions the service could be deployed to, ease of deployment via infrastructure as code (IaC), SOC accreditation, data encryption, database schema evolution, etc. As expected, different databases scored differently for these criteria, but none fared so badly that we weren’t prepared to accept any additional effort if it turned out to be the best solution otherwise.


For example, AWS services like Aurora and Redshift came out top in areas such as number of regions they supported, and support for IaC (e.g. CloudFormation), but other services offered enough (either in terms of automated deployments, or management APIs so that we could automate it ourselves, or a very simple manual deployment process) that this was acceptable to us.


## Conclusion [\#](/blog/why-m3ter-clickhouse-cloud#conclusion)


Taking everything into account, we found that for our specific workload, ClickHouse Cloud on AWS provided both the best performance, and best value for money. More subjective criteria (where differences between implementations in each service make direct comparisons difficult), such as monitoring, HA/DR, scaling etc. also scored highly for ClickHouse Cloud.


We felt this was a database service we could work with easily on a day\-to\-day basis. The UI for the cloud offering was easy to use, and user management allowed sensible controls to be put in place so that various users/services can only perform the required actions (principle of least privilege).


Additionally, ClickHouse is a mature database that is used by lots of customers, giving us faith that we were unlikely to encounter any unwelcome surprises. In our experience during the PoC, the support and advice we received from them was first class, giving us real confidence that if we did encounter any issues, we wouldn’t be left trying to solve them on our own.


After implementing ClickHouse Cloud as our primary database for usage data, we have been very happy with our choice. We haven’t experienced any particular pain points, and investigating performance (e.g. for new features) has been easy thanks to the detailed monitoring available. The per\-query metrics in the [query\_log table](https://clickhouse.com/docs/en/operations/system-tables/query_log) have been almost invaluable, since we can query that data using standard SQL, just like data in any other table.


ClickHouse Cloud is very much designed for "real\-time analytics" which is exactly what we need at m3ter for our usage data workload. We do use a variety of other databases for different use\-cases, so it’s not a case of "one size fits all". As with most complex services, using a mix of databases and technologies, and choosing the "best in class" for each distinct use\-case, usually yields the best results. In our case, our proof of concept tests determined that ClickHouse Cloud was the current "best in class" for our rating engine.

**ClickHouse Cloud, powered by AWS**

ClickHouse Cloud on AWS uses Amazon Simple Storage Service (Amazon S3\), object storage for scalability, data availability, security, and performance. Amazon Elastic Compute Cloud (Amazon EC2\) is used for high performance and efficiency for data\-intensive workloads. AWS PrivateLink is used for secure connection between ClickHouse Cloud and the customer's VPC. ClickHouse Cloud also integrates with a wide range of other AWS services, including Amazon Managed Streaming for Apache Kafka, Amazon Quicksight, Amazon Relational Database Service, Amazon Glue and Amazon Kinesis.

![](/_next/image?url=%2Fuploads%2Faws_qualified_software_b95bcb6c3e.png&w=1080&q=75)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
