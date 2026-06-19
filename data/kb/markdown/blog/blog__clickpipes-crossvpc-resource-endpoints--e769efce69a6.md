# ClickPipes supports cross\-VPC resource access on AWS!


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickPipes supports cross\-VPC resource access on AWS!

![](/_next/image?url=%2Fuploads%2FLuke_Gannon_NE_4_J_5562a05272.jpeg&w=96&q=75)[Luke Gannon](/authors/luke-gannon)Dec 1, 2024 · 5 minutes readToday, we’re proud to announce that [ClickPipes](https://clickhouse.com/cloud/clickpipes) now supports AWS’s new way to provide private, unidirectional connectivity to individual data sources using AWS PrivateLink and VPC Lattice.


Supporting this new PrivateLink feature coincides with our most recent accreditation status as a AWS PrivateLink Service Ready Partner. We went through a stringent validation process with the AWS team to demonstrate our technical capabilities, verification of our solution and security processes, so you can be sure the integration is robust.


ClickPipes is our continuous data ingestion service designed specifically for ClickHouse Cloud. It connects your external data sources like [Amazon MSK](https://aws.amazon.com/msk/getting-started/), [Amazon S3](https://aws.amazon.com/s3/getting-started/), or [Amazon Kinesis](https://aws.amazon.com/kinesis/getting-started/), enabling you to set up robust and scalable data pipelines quickly and efficiently to get data into your ClickHouse service. Since its inception, ClickPipes has provided support for [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to support our customers wanting to avoid their data and network traffic going over the public internet.


![1a_crossvpc.png](/uploads/1a_crossvpc_92f4eb1732.png)
AWS PrivateLink architecture with load balancer
Cross\-VPC resource access with AWS PrivateLink and VPC Lattice gives the added benefit of reducing the amount of resources needed as you no longer require a load\-balancer (ALB/NLB) to take advantage of sharing your data to ClickPipes.


This new capability leverages AWS PrivateLink VPC endpoints and VPC Lattice to share and access resources across VPCs and accounts.


![2_crossvpc.png](/uploads/2_crossvpc_a4d1da0342.png)
AWS PrivateLink architecture without load balancer
A resource owner can share specific resources from their VPC, without exposing any other resources in that VPC to a resource consumer. A resource consumer can access shared resources in another VPC/account privately.


With this capability, you can connect your individual resources across VPC and account boundaries, or even from on\-premise networks\* with the privacy and security benefits of AWS PrivateLink.


![3a_crossvpc.png](/uploads/3a_crossvpc_89d25b655c.png)
ClickPipes using AWS PrivateLink and VPC Lattice for cross\-VPC resource access
## How to share your MSK Resource with ClickPipes? [\#](/blog/clickpipes-crossvpc-resource-endpoints#how-to-share-your-msk-resource-with-clickpipes)


In order to get started using AWS MSK shared through AWS PrivateLink and VPC Lattice, you will need to do the following steps:


1. Create a Resource\-Gateway to allow access into your VPC
2. Provide a Resource\-Configuration to specify which resource should be shared
3. Share the Resource\-Configuration with ClickHouse to use with ClickPipes


### Create a Resource\-Gateway [\#](/blog/clickpipes-crossvpc-resource-endpoints#create-a-resource-gateway)


In order to share resources that are within your VPC, you will need to create a Resource\-Gateway. The following command will create the Resource\-Gateway.



```
aws vpc-lattice create-resource-gateway \ 
--vpc-identifier <VPC_ID> \
--subnet-ids <SUBNET_IDS> \ 
--security-group-ids <SG_IDs> \
--name <NAME> 

```

Before you can proceed, you will need to wait for the Resource\-Gateway to enter into an “Active” state. You can check the state by running the following:



```
aws vpc-lattice get-resource-gateway \
--resource-gateway-identifier <RESOURCE_GATEWAY_ID> 

```

### Create a VPC Resource Configuration [\#](/blog/clickpipes-crossvpc-resource-endpoints#create-a-vpc-resource-configuration)


To share your resource, you’ll need to create a Resource\-Configuration that will be used by the Resource\-Gateway.


You can create a Resource\-Configuration that either shares an IP\-address or a domain\-name that is publicly resolvable.


This simple setup will focus on supplying a single Resource\-Configuration to share, if you would like to configure Group/Child Resource\-Configurations, please refer to our documentation.



```
aws vpc-lattice get-resource-gateway \
--resource-gateway-identifier <RESOURCE_GATEWAY_ID> 

```

The output of the command will provide the “Resource\-Configuration ARN”, you will use this in the next step and replace the \<VPC\_RESOURCE\_CONFIGURATION\_ARN\> variable.


### Share the Resource Configuration with ClickHouse [\#](/blog/clickpipes-crossvpc-resource-endpoints#share-the-resource-configuration-with-clickhouse)


Sharing your resource requires the Resource\-Configuration to be shared with ClickPipes, this is facilitated through the Resource Access Manager (RAM).


The following command will put the Resource\-Configuration into the Resource\-Share, enabling ClickHouse to access your resource when you have shared your Resource\-Owner Account ID with us.



```
aws ram create-resource-share \
--principals 072088201116 \
--resource-arns "<VPC_RESOURCE_CONFIGURATION_ARN>" \
--name "<RESOURCE_SHARE_NAME>"

```

The ClickPipes team will require a resource owner account ID to be shared. You can find this within the [AWS console](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-identifiers.html) or by running the following CLI command:



```
aws sts get-caller-identity \
--query Account \
--output text

```

If data source (e.g. Kafka broker) requires a private DNS setup , please share the host name(s) with ClickPipes team as part of your support request.


## Ready to get set up? [\#](/blog/clickpipes-crossvpc-resource-endpoints#ready-to-get-set-up)


We’re excited to get our users set up with cross\-VPC resource access. If you would like to start utilizing this feature with ClickPipes, please raise a [support ticket](https://console.clickhouse.cloud/support) through the ClickHouse Console with the Resource Owner Account ID.


\* In order to connect PrivateLink Resource Endpoints to an on\-premise resource, a Direct Connect or VPN connection is required

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
