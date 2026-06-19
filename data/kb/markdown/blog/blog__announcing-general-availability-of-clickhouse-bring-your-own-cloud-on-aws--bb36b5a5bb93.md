# Announcing General Availability of ClickHouse BYOC (Bring Your Own Cloud) on AWS


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing General Availability of ClickHouse BYOC (Bring Your Own Cloud) on AWS

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 20, 2025 · 5 minutes readAs enterprises modernize with cloud\-native architectures on AWS, they can leverage the comprehensive security controls of AWS while meeting their specific compliance requirements and geographic regulations. AWS Virtual Private Cloud (VPC) provides the foundation for secure database deployments, where keeping sensitive data within the customer's own VPC boundary is a critical requirement.


[ClickHouse BYOC](/cloud/bring-your-own-cloud) enables organizations to access the real\-time analytical capabilities of ClickHouse Cloud, while ensuring their data remains entirely within their own AWS VPC environment, simplifying security reviews and compliance processes. In the ClickHouse BYOC architecture, the data plane consisting of storage and compute resources remains in the customer’s own VPC, rather than being transferred to the ClickHouse VPC, and the customer can leverage the extensive security controls of AWS to meet specific governance requirements.


[Request access](/cloud/bring-your-own-cloud)

> "The evolution of ClickHouse Cloud is influenced by the insights we gain from working closely with our users. Our users in banking, healthcare, and cybersecurity must adhere to data governance mandates. With ClickHouse BYOC on AWS, we make all the features of a fully\-managed ClickHouse Cloud available in an operating environment known and trusted by our customers… their own AWS VPC."
> 
> 
> Tanya Bragin, VP Product \& Marketing, ClickHouse


By adopting ClickHouse BYOC, customers can benefit from full compute\-storage separation (powered by the proprietary [SharedMergeTree engine](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates)), seamless vertical and horizontal scaling of compute nodes, and [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud). These capabilities enable granular isolation of workloads in multi\-tenant environments and more targeted, independent allocation of compute resources, resulting in more optimized compute resource usage and lower infrastructure costs.



> “ClickHouse BYOC on AWS has transformed the way we deploy and manage ClickHouse, making it more streamlined and cost\-effective. By moving to shared\-storage architecture and utilizing compute\-compute separation capability, we have significantly optimized our infrastructure costs compared to our self\-managed ClickHouse deployments.”
> 
> 
> Krishna Sai, CTO, SolarWinds.


## ClickHouse BYOC Architecture [\#](/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws#clickhouse-byoc-architecture)


In the BYOC deployment model, all customer data is hosted in the customer VPC on AWS. This includes data stored on disk, data processed via compute nodes (including in memory and local disk cache), and backup data. The only components hosted in the ClickHouse VPC are the web and API interfaces used to manage the organization and services, responsible for operations like user management, service start/stop, and scaling.


Detailed logs and metrics collected by the system are stored in the customer VPC, with only the most critical telemetry and alerts allowed to leave to enable resource utilization and health monitoring.


![ClickHouse_BYOC_Architecture.png](/uploads/Click_House_BYOC_Architecture_bf220960fd.png)
## ClickHouse BYOC Benefits [\#](/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws#clickhouse-byoc-benefits)


The launch of ClickHouse BYOC on AWS is a key milestone in our journey to enable flexible, secure, and high\-performance analytics for verticals and markets that need to adhere to the strictest data governance and residency mandates, including cybersecurity, banking, healthcare, and other businesses that manage sensitive PII.


Businesses no longer need to choose between cloud\-native agility and control; they can achieve both, with the following benefits:


- **Data security and control:** BYOC gives customers complete control over their data, ensuring compliance with internal security policies and regulatory requirements. Sensitive data stays within the customer’s cloud environment, and they have full visibility into system access.
- **Greater operational flexibility:** BYOC offers a hybrid deployment model, allowing customers to control their data, while relying on ClickHouse experts for database management, which includes ongoing software upgrades and patches.
- **Performance predictability:** Deploying ClickHouse Cloud data plane in a dedicated customer account ensures optimal workload isolation and gives customers greater flexibility in selecting instance types to best support their workloads.
- **Cloud spend optimization:** With BYOC, customers can continue to leverage existing cloud provider commitments and discounts, and thus optimize their cloud spending. In addition, this model supports VPC peering, which helps reduce data transfer costs, especially at large data volumes.


[Request access](/cloud/bring-your-own-cloud)
## Part of a broader collaboration [\#](/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws#part-of-a-broader-collaboration)


On December 10, 2024, ClickHouse, Inc. [announced](https://clickhouse.com/blog/clickhouse-announces-strategic-collaboration-agreement-with-aws-to-advance-real-time-data-analytics-and-generative-ai-innovation) a five\-year strategic collaboration agreement with Amazon Web Services (AWS) to enhance real\-time data warehousing, observability, business intelligence, machine learning, and generative AI solutions. This collaboration aims to integrate ClickHouse Cloud more closely with AWS services, facilitating the development of high\-performance analytics and generative AI applications. General availability of ClickHouse BYOC exclusively available on AWS today is a significant milestone in this journey.


## Get started now [\#](/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws#get-started-now)


If ClickHouse BYOC on AWS is the right fit for your needs, please [contact us](https://clickhouse.com/cloud/bring-your-own-cloud) to get started.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
