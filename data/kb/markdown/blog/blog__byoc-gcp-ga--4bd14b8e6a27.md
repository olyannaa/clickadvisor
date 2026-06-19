# ClickHouse BYOC on Google Cloud now Generally Available


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse BYOC on Google Cloud now Generally Available

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U05_ARHHQT_7_U_d759fe8fcc74_512_b2a5bc4535.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_5_330c6e9bbc.png&w=96&q=75)[Aashish Kohli](/authors/aashish-kohli) and [Yiyang Shao](/authors/yiyang-shao)Mar 31, 2026 · 4 minutes readSince launching [BYOC on AWS](https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws), we've seen organizations adopt it because they want the operational simplicity of a fully managed ClickHouse service, but they need their data to stay inside their own cloud account. With today's announcement, Google Cloud users can now get exactly that : no waitlist, no private preview access request.


## **What is BYOC?** [\#](/blog/byoc-gcp-ga#what_is_byoc)


BYOC splits the control plane and data plane into separate VPCs."


- **ClickHouse\-managed control plane**: Runs in ClickHouse's own VPC. Handles orchestration, scaling, upgrades, monitoring, and billing. It never touches your query data.
- **Your data plane**: Runs entirely inside your Google Cloud project. Your GKE cluster, ClickHouse servers, object storage (Google Cloud Storage), backups, and metrics all live within your account boundary.


The control plane communicates with your environment over a Tailscale zero\-trust tunnel \- outbound\-only, encrypted, and scoped to orchestration traffic only. ClickHouse engineers with support access are restricted to system tables, with time\-bound and audited sessions.


The result: you get a fully managed service without giving up data residency.


## **Why Google Cloud?** [\#](/blog/byoc-gcp-ga#why_google_cloud)


Google Cloud is home to a significant share of enterprise data infrastructure. Organizations running BigQuery, Dataflow, and Pub/Sub pipelines naturally want their high\-performance OLAP layer in the same environment \- with the same IAM primitives, the same VPC controls, and the same compliance perimeter.


BYOC on Google Cloud makes ClickHouse native to that environment. Your service runs on GKE, stores data and backups in your GCS buckets, and connects to the rest of your Google Cloud workloads over private networking \- no data crosses account or project boundaries.


ClickHouse BYOC is already available across all public ClickHouse Cloud Google regions. Over time we will expand support to additional Google Cloud regions.


## **Initial Set up** [\#](/blog/byoc-gcp-ga#initial_set_up)


Onboarding uses a three\-step Terraform\-based setup:


**1\. Account setup:** Run a Terraform module that creates the IAM roles and trust permissions needed for the BYOC controller to manage infrastructure in your Google Cloud project. We follow least\-privilege principles \- the controller gets only what it needs to provision and maintain the cluster.


**2\. Infrastructure provisioning:** In the ClickHouse BYOC console, select your Google Cloud region, configure your VPC CIDR range, and align availability zones. We recommend a dedicated Google Cloud project for BYOC \- this gives you clean cost attribution and a clear resource isolation boundary.


**3\. Service creation:** Specify a service name, select your BYOC environment and region, choose CPU/memory allocation, and configure replica count for high availability. Your GKE cluster, ClickHouse nodes, and monitoring stack are provisioned automatically.


If you have custom networking requirements or want to integrate with an existing VPC, reach out to ClickHouse Support \- we support customized onboarding for those configurations.


## **What's Included** [\#](/blog/byoc-gcp-ga#whats_included)


BYOC on Google Cloud ships with the full set of capabilities you need to run production ClickHouse workloads:


- **SharedMergeTree** for efficient distributed storage
- **Managed backups and restore** : stored in your GCS buckets, never leaving your project
- **Vertical and horizontal scaling** : adjust replica count and node size per workload
- **Auto Idling / Wake up** : automatically idle services during quiet periods to reduce costs
- **Compute\-compute separation** via [Warehouses](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud) \- isolate different query workloads across dedicated compute groups
- **Prometheus / Grafana / AlertManager** monitoring stack
- **Datadog integration** for teams with centralized observability pipelines
- **VPC Peering and Private Service Connect** for enterprise network configurations


## **Upgrades and Maintenance** [\#](/blog/byoc-gcp-ga#upgrades_and_maintenance)


ClickHouse handles both ClickHouse database upgrades and supporting infrastructure upgrades (Kubernetes operator, Istio, monitoring components) in the background via ArgoCD. Database upgrades follow a [make\-before\-break strategy](https://clickhouse.com/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud): updated replicas are added before old ones are removed, minimizing disruption. You can select Fast, Regular, or Slow release channels, with upgrades aligned to your configured maintenance window.

### Get started today

BYOC on Google Cloud is available now. Contact our support team or reach out to your account team for a guided onboarding session. The BYOC documentation covers the full architecture, security model, and configuration options in detail.
[Read the BYOC documentation](https://clickhouse.com/docs/cloud/reference/byoc/overview?loc=blog-cta-320-get-started-today-read-the-byoc-documentation&utm_blogctaid=320)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
