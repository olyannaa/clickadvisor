# Announcing the Billing API for ClickHouse Cloud with Vantage support


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing the Billing API for ClickHouse Cloud with Vantage support

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_3226961af3.png&w=96&q=75)The ClickHouse \& Vantage teamsMar 4, 2025 · 7 minutes read![billing_api.png](/uploads/Blog_Scaling_Anaytics_Without_Costs_Vantage_202503_FNL_a28b0c2b70.png)
We’re excited to announce the Billing API for ClickHouse Cloud, now available to all our users. This new API provides programmatic access to your billing and usage data, making it easier than ever to track and manage costs. With this capability, teams can integrate ClickHouse Cloud cost data into observability tools, automate cost reporting for finance teams, and even enable usage\-based billing for downstream customers. Whether you’re looking to optimize your spend, improve financial transparency, or build new cost management workflows, the Billing API gives you the flexibility to do so.


To showcase the impact of this feature, we’re excited to share a guest post from Vantage, a leading cloud cost management platform. Vantage has already integrated the ClickHouse Cloud Billing API, allowing users to seamlessly track and manage ClickHouse costs alongside their broader cloud expenses. By leveraging this API, Vantage has demonstrated the art of the possible—transforming raw billing data into actionable insights that help teams gain deeper cost visibility, optimize analytics spend, and implement smarter financial operations. In the post below, Vantage shares how this integration empowers teams to take control of their cloud costs.


Users looking for specifics of the API can find the docs [here](https://clickhouse.com/docs/cloud/manage/api/usageCost-api-reference).


## Scaling analytics without scaling costs [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#scaling-analytics-without-scaling-costs)


*By: Ben Schaechter, Co\-Founder and CEO of Vantage*


Companies are increasingly moving their data\-intensive workloads to ClickHouse Cloud, as it excels particularly well in cases of [real\-time data processing](https://www.vantage.sh/blog/snowflake-vs-clickhouse-cloud-cost) and cost efficiency. Unlike legacy OLAP systems, ClickHouse processes massive datasets with sub\-second query times, while keeping storage costs low through [advanced compression](https://clickhouse.com/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis#storage-efficiency--compression). At Vantage, we’ve even run our own experiments, benchmarking ClickHouse’s performance against other analytical databases, such as DuckDB. We found that ClickHouse was [3X faster for raw query speed](https://www.vantage.sh/blog/clickhouse-local-vs-duckdb)—especially for cloud cost analytics, which is [why we use it for our analytics projects as well as our own platform](https://clickhouse.com/videos/vantage).


This performance advantage makes ClickHouse Cloud an ideal engine for organizations running data\-intensive workloads at scale. But as companies continue to scale, tracking and optimizing costs becomes a top priority, especially as hidden expenses from inefficient resource planning and a lack of centralized cost visibility can quickly add up.


## Scaling pains and the price of growth [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#scaling-pains-and-the-price-of-growth)


Without the right visibility, teams may struggle with inefficient compute scaling and the potential to under\-utilize resources. Additional hidden costs may arise from new services being started within the organization, high idle time leading to wasted resources, and expensive data egress fees.


This is where FinOps \- or financial operations—comes in to help teams stay on top of costs and make smarter infrastructure decisions. Consider the following scenarios and how cost visibility can help.


### Inefficient compute scaling [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#inefficient-compute-scaling)


ClickHouse Cloud provides both [vertical auto scaling and manual horizontal scaling](https://clickhouse.com/docs/en/manage/scaling), but without proper cost visibility, teams may overspend on compute resources and provision more capacity than necessary. For example, manual horizontal scaling allows teams to adjust replica counts via the API or UI; however, one team member might add more replicas or loosen scaling limits without understanding workload patterns, therefore increasing their costs without improving performance. In this case, FinOps best practices, such as setting up [budget alerts](https://www.vantage.sh/features/budgets) or monitoring [cost anomalies](https://www.vantage.sh/features/cost-anomaly-alerts), can help teams keep these costs in check.


### New services unknowingly spun up [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#new-services-unknowingly-spun-up)


ClickHouse Cloud makes it easy to spin up new resources, such as [services](https://clickhouse.com/docs/cloud/get-started/cloud-quick-start); however, without proper governance, teams may accidentally leave unused services running. For example, a developer testing a new query optimization strategy might provision a high\-replica cluster with a large storage footprint, disabling idling for initial convenience. They intend to shut it down after testing, but as often happens, they forget and the service remains active indefinitely. Compute is only charged when active, but forgetting to either enable idling or turn off these resources can cause teams to rack up compute costs. By adding cost visibility to their workflow, teams can regularly monitor [active resources](https://www.vantage.sh/features/resource-reports) and review usage reports to ensure that any forgotten or underutilized clusters are identified and decommissioned before they result in unnecessary spend.


### Growing data egress fees [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#growing-data-egress-fees)


Data transfer costs can often significantly increase an organization’s overall cloud expenses, especially when dealing with large\-scale datasets. Data egress to the public internet or across regions is significantly more expensive than same\-region [data transfer](https://clickhouse.com/docs/en/cloud/manage/network-data-transfer?). Without proper monitoring, these data transfer costs can accumulate substantial egress fees. Teams need to review reporting that digs into their costs at the [data transfer level](https://www.vantage.sh/blog/how-to-see-aws-data-transfer-pricing-save) to better understand how these charges vary over time. Regularly reviewing these reports enables organizations to implement data transfer policies and then make decisions about how to reduce these costs, either via methods like compression or through filtering data before transferring it.


## Vantage \+ ClickHouse Cloud \= visibility for analytics costs [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#vantage--clickhouse-cloud--visibility-for-analytics-costs)


As a way to help provide teams with cost visibility for all their analytics costs, we’re releasing an integration for ClickHouse Cloud and [Vantage](https://www.vantage.sh/). To create this integration, we used the new ClickHouse Cloud [usageCost API](https://clickhouse.com/docs/en/cloud/manage/api/usageCost-api-reference), which provides cost and usage data at an organization level. Vantage securely ingests and processes daily ClickHouse cost data, allowing users to [filter and group costs](https://docs.vantage.sh/cost_reports#filtering-cost-reports) by organization, usage type, cost category, and other dimensions.


![vantage_dashboard.png](/uploads/vantage_dashboard_a3879c25ef.png)
*Vantage Usage Report showing ClickHouse Cloud usage and costs*
Teams can now automatically ingest and visualize ClickHouse costs directly in Vantage, alongside [multiple cloud provider integrations](https://www.vantage.sh/integrations)—including their primary cloud provider’s costs (e.g., AWS, Azure, Google Cloud). Teams get a full picture of all their cloud costs and can more easily manage their overall infrastructure planning. Along with this integration, teams can also use other existing Vantage features to:


- Enable cost alerts, anomaly detection, and budget notifications for ClickHouse Cloud expenses
- Create [business metrics](https://www.vantage.sh/features/unit-costs) on top of ClickHouse Cloud costs to calculate metrics like unit cost per query
- Include ClickHouse costs in [cost reports](https://www.vantage.sh/features/cost-reports), [active resource reports](https://docs.vantage.sh/active_resources), and [usage\-based reporting](https://www.vantage.sh/features/usage-based-reporting) to monitor any active resources currently generating costs


With this integration, FinOps and engineering teams get full visibility into ClickHouse Cloud costs, helping them to avoid some of the challenges mentioned earlier.


## Getting started with the Vantage and ClickHouse Cloud integration [\#](/blog/announcing-billing-api-for-clickhouse-cloud-with-vantage-support#getting-started-with-the-vantage-and-clickhouse-cloud-integration)


Ready to take control of your analytics costs? Sign up for a [free Vantage account](http://console.vantage.sh/signup) and [start your 30\-day free trial of ClickHouse Cloud](https://clickhouse.com/cloud) today. Connect the two to seamlessly track, manage, and optimize your cloud spend. Check out the [Vantage blog](https://www.vantage.sh/blog/clickhouse-cloud-support) and [Vantage documentation](https://docs.vantage.sh/connecting_clickhouse) to get started.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
