# Horizontal Scaling in ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Horizontal Scaling in ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U05_ARHHQT_7_U_d759fe8fcc74_512_b2a5bc4535.jpg&w=96&q=75)[Aashish Kohli](/authors/aashish-kohli)Jun 18, 2024 · 6 minutes read### Introduction [\#](/blog/horizontal-scaling-in-clickHouse-cloud#introduction)


Our mission for ClickHouse Cloud, since its early days, has been to equip our users to develop analytics applications at scale, without having to worry about the operational overhead of infrastructure planning, sizing, and managing complex scaling operations. For this reason, the service has supported vertical autoscaling since its inception, so users never have to overprovision or monitor their usage. Based on memory and CPU usage, the service scales to accommodate the workload within the bounds specified by the user.


Now, we are excited to bring **horizontal scaling** to ClickHouse Cloud in Private Preview. This feature is available for Production instances in ClickHouse Cloud. Horizontal scaling will allow customers to control the number of replicas in their service to match their workload demands.


As part of Private Preview, this feature is available via ClickHouse Cloud APIs. We will also be enabling horizontal scaling via the cloud console very soon. To access horizontal scaling for your service, please contact the ClickHouse Support Team at [support@clickhouse.com](mailto:support@clickhouse.com).


### Why horizontal scaling [\#](/blog/horizontal-scaling-in-clickHouse-cloud#why-horizontal-scaling)


Before we get into the details of horizontal scaling in ClickHouse Cloud, let’s first take a look at how horizontal and vertical scaling are different.


Vertical scaling usually involves increasing the resources available \- adding more memory or CPU \- to a single machine, or a set of machines, in a cluster. Larger machines can handle greater loads, especially ones where you might want all resources to fit in the memory of a single machine \- for instance supporting large joins across tables. There are physical limits to vertical scaling though \- the machines have an upper limit to how large they can get.


Horizontal scaling, on the other hand, involves adding more machines. Usually, these are all of the same size in order to scale out a cluster of homogenous machines (or replicas). The workload is then distributed among a large number of smaller machines (as opposed to a few large machines in case of vertical scaling).


Horizontal scaling provides better fault tolerance as the load is spread over a larger set of replicas. It is usually faster to scale out a service horizontally, by adding smaller machines, than it is to scale vertically by increasing the size of existing replicas. Because of the mechanics of how horizontal scaling works, it can also be less disruptive than vertical scaling, as new replicas are being added (rather than existing replicas being resized, or replaced).


Horizontal and vertical scaling help with different kinds of workloads. Workloads that need lots of resources from a single machine benefit from vertical scaling. For workloads with high concurrency, horizontal scaling can be a great alternative. For instance, you might have the need to ingest a large amount of data into ClickHouse. Adding additional replicas will allow the ingestion to proceed much faster. Horizontal scaling also works much better than vertical scaling in scenarios where the request rate is increasing, and you need to quickly add capacity to the cluster without impacting the existing capacity.


### Horizontal scaling in action [\#](/blog/horizontal-scaling-in-clickHouse-cloud#horizontal-scaling-in-action)


Once horizontal scaling is enabled on the service, you can use ClickHouse Cloud [public APIs](https://clickhouse.com/docs/en/cloud/manage/api/swagger#/paths/~1v1~1organizations~1:organizationId~1services~1:serviceId~1scaling/patch) to scale your service by updating the [scaling settings](https://clickhouse.com/docs/en/cloud/manage/api/swagger#/paths/~1v1~1organizations~1%7BorganizationId%7D~1services~1%7BserviceId%7D~1scaling/patch) for the service.


Let’s see how horizontal scaling works.


1. First, inspect the memory allocated to your cluster as well as the number of replicas. You can do this by looking at the cloud console dashboard as well as the number of replicas from your service settings. Here we have a 3 replica cluster with 16 GiB of memory allocated to each, resulting in a total of 48 GiB memory allocated to the cluster.


![unnamed (3).png](/uploads/unnamed_3_8227247d97.png)
![unnamed (4).png](/uploads/unnamed_4_fe1f1310f3.png)
*Service scaling settings from ClickHouse Cloud console*
2. Let’s say we now want to horizontally scale the cluster to 6 replicas of 16 GiB each. This means that once scaling is complete, we should end up with a total memory of 96 GiB across six replicas.



> **Note**: The API currently assumes that the min and max. total memory is based on 3 replicas, which is the number of replicas in a default production ClickHouse cluster. This means that the `minTotalMemoryGb` and `maxTotalMemoryGb` have values equal to 24 and 96 respectively, which comes out to a per\-node memory minimum of `8GiB` and `32GiB` respectively, as reflected by the UI. If we want to horizontally scale out from 3 to 6 replicas, we need to only change the `numReplicas` in the API, or the `Number of Nodes` in the UI, without changing the min and max memory size. Thus, for an `16GiB` replica size, our total memory will come out to be `96GiB`across 6 replicas


To do so, we issue a patch request, to adjust the number of replicas in a cluster as shown below (screenshots from postman client).


![unnamed (5).png](/uploads/unnamed_5_24d9c7cab6.png)
*PATCH request to update numReplicas*
![unnamed (6).png](/uploads/unnamed_6_9a4ad59745.png)
*Response from PATCH request*
3. Once you issue the PATCH request, you’ll see that the scaling settings screen now displays “6” as the setting for the number of replicas in the cluster. It is important to note that this is not the current number of replicas in the cluster, it is the desired number of replicas.


![unnamed (7).png](/uploads/unnamed_7_d528dc717c.png)
4. Looking back at the monitoring screen for this cluster, we can now see that the cluster has indeed been scaled to a total of 96 GiB memory.


![unnamed (8).png](/uploads/unnamed_8_7700054f43.png)


### Looking to the future [\#](/blog/horizontal-scaling-in-clickHouse-cloud#looking-to-the-future)


As mentioned earlier, we will soon make horizontal scaling available via the cloud console directly. During Private Preview, we will improve the UI and API experience of horizontally scaling a ClickHouse Cloud service based on customer feedback, before making the capability generally available (GA).


Making horizontal scaling self\-service and GA is just the first step. In the near future, we will also enable horizontal autoscaling, whereby a ClickHouse Cloud user is able to set minimum and maximum replica counts on their service as bounds within which their service should autoscale. Based on the load on the cluster, we will automatically horizontally scale the cluster as needed to closely match the actual utilization. Our end goal is to provide a mix of horizontal and vertical autoscaling to achieve the optimal performance for a service based on the workload.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
