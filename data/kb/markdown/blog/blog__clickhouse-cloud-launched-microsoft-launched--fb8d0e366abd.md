# Building ClickHouse Cloud on Microsoft Azure


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building ClickHouse Cloud on Microsoft Azure

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 25, 2024 · 22 minutes readWe’re excited to announce the [General Availability of ClickHouse Cloud on Azure](/blog/clickhouse-cloud-is-now-generally-available-on-microsoft-azure).


In this blog post, we’ll discuss in detail how we built this new service, including the challenges we faced and how we worked through them.


## A brief history of ClickHouse Cloud [\#](/blog/clickhouse-cloud-launched-microsoft-launched#a-brief-history-of-clickhouse-cloud)


We [launched ClickHouse Cloud](https://clickhouse.com/blog/clickhouse-cloud-generally-available) in December 2022 on AWS. Just a few months later, we expanded to support ClickHouse Cloud on [GCP](https://clickhouse.com/blog/clickhouse-cloud-on-google-cloud-platform-gcp-is-generally-available). Our Azure launch marks a meaningful milestone for us, as ClickHouse Cloud is now available on all three major cloud providers.


## The architecture of ClickHouse Cloud [\#](/blog/clickhouse-cloud-launched-microsoft-launched#the-architecture-of-clickhouse-cloud)


In the next few sections, we’ll describe the architecture and components of ClickHouse Cloud before discussing the Azure\-specific differences.


In ClickHouse Cloud, we have a “shared everything” architecture with “separated storage and compute.” This means that storage and compute are decoupled and can be scaled separately. We use object storage (such as Azure Blob storage) as the primary store for the analytical data and local disks only for caching, metadata, and temporary storage.


The architecture is designed to be as Cloud Service Provider (**CSP**) neutral as possible, so that it can be reused across different CSPs, such as AWS, GCP, and Azure.


A diagram describing this is shown below:


![00_azure.png](/uploads/00_azure_d529ca9f37.png)
## ClickHouse Cloud components [\#](/blog/clickhouse-cloud-launched-microsoft-launched#clickhouse-cloud-components)


ClickHouse Cloud’s components are best described as two different and independent logical units:


1. **Control Plane** \- The “user\-facing” layer: This is the UI and API layer that enables users to run their operations on the cloud, grants access to their ClickHouse services, and enables them to interact with the data.
2. **Data Plane** \- The “infrastructure\-facing” part: The functionality for managing and orchestrating physical ClickHouse clusters, including resource allocation, provisioning, updates, scaling, load balancing, isolating services from different tenants, backup and recovery, observability and metering (collecting usage data).


The following diagram illustrates these ClickHouse Cloud components and their interactions.


![01_azure.png](/uploads/01_azure_a166bdca5c.png)
Our Control Plane is built in AWS and interacts with our Data Plane in AWS, GCP, and Azure. We do not have a different control plane for each CSP. For this reason, for the remainder of this blog, we’ll focus on the Data Plane architecture.


## Multi\-cloud \- Azure [\#](/blog/clickhouse-cloud-launched-microsoft-launched#multi-cloud---azure)


We designed ClickHouse Cloud to be CSP agnostic. Broadly, this holds true for all 3 major CSPs (**AWS/GCP/Azure**). However, each individual CSP also has its own quirks and differences. Therefore, there are areas in our architecture where we must adapt to the underlying CSP. In this section, we’ll talk about some of the challenges we faced in adapting our architecture to Azure.


### CSP components in ClickHouse Cloud [\#](/blog/clickhouse-cloud-launched-microsoft-launched#csp-components-in-clickhouse-cloud)


As is illustrated in the diagram above, our Data Plane is made up of a few key components:


1. **Compute**: We use managed Kubernetes such as [AWS EKS](https://aws.amazon.com/eks/)/[GCP GKE](https://cloud.google.com/kubernetes-engine?hl=en)/[Azure AKS](https://azure.microsoft.com/en-us/products/kubernetes-service) as our compute layer for ClickHouse clusters. We use Kubernetes namespaces \+ Cilium to ensure proper tenant isolation for our customers.
2. **Storage**: We use Object storage, such as [AWS S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_st_s3)/[GCP Cloud Storage](https://cloud.google.com/storage?hl=en)/[Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), to store the data in ClickHouse clusters. Each ClickHouse cluster has its own dedicated storage for tenant isolation.
3. **Network**: ClickHouse Cloud infrastructure in each region runs inside a private, logically isolated virtual network, and all our compute in that region is connected via this network. Here, we use CSP\-specific solutions as well, such as [AWS VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)/[GCP VPC](https://cloud.google.com/vpc/docs/overview)/[Azure VNET](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
4. **Identity and Access Management (IAM)**: Lastly, in order for a ClickHouse Cloud cluster compute to be able to talk to corresponding Object Storage, we use the CSP IAM to provide access and to ensure correct authorization. Each ClickHouse Cloud cluster has its own identity and only this identity can access the data. For identity and access management, we leverage CSP offerings such as [AWS IAM](https://aws.amazon.com/iam/)/[GCP IAM](https://cloud.google.com/security/products/iam)/[Microsoft Entra](https://learn.microsoft.com/en-us/entra/) (previously Azure Active Directory).


Although each CSP has its own specific solution, ideally, we should be able to design common interfaces and abstract out most of the complexity. However, in reality, while some components such as compute (Kubernetes) were seamless across CSPs, not all components were so easy.


Object storage is one example. Azure blob storage is fairly different from AWS S3 in terms of both its API and implementation. Blob storage also has different permission\-based access on buckets. This results in differences in the way we organize storage for each cluster. This was one of the easier differences to work around. More complex components like network setup are discussed in detail below.


One problem we didn’t anticipate was the way cloud resources (e.g., VMs, identities, and storage buckets) are organized in Azure. Let’s discuss why that is.


### Cloud resource organization [\#](/blog/clickhouse-cloud-launched-microsoft-launched#cloud-resource-organization)


In AWS, resources are organized under accounts, which serve as the primary container for all resources. At a higher level, AWS Organizations allow you to manage multiple accounts centrally, providing consolidated billing and centralized access control. This creates a two\-level hierarchy: individual accounts and the organization.


Similarly, GCP employs a three\-level hierarchy, starting at the top with Organizations, which contain Projects and, optionally Folders for further organization. Projects are the primary container for resources and represent billing entities, while Folders allow hierarchical grouping of Projects.


Azure, on the other hand, has a more complex resource hierarchy. At the top level are tenants, representing a dedicated Microsoft Entra ID (previously [Azure AD](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)) instance and providing identity management across multiple subscriptions. Under tenants, Management Groups manage access, policies, and compliance across multiple subscriptions. Subscriptions, containers for billing, and resource management sit under Management Groups. Additionally, resources are organized within each subscription into Resource Groups, which are logical containers for related resources. This results in a four\-level hierarchy: **Tenants**, **Management Groups**, **Subscriptions**, and **Resource Groups**.


![Azure Hierarchy last.png](/uploads/Azure_Hierarchy_last_d40f7a28fb.png)
A keen reader might wonder whether we are needlessly complicating things. Since Resource Groups in Azure are usually meant for resources that are created/deleted together, it might make logical sense to create each customer ClickHouse cluster in a different Resource Group and create one subscription per ClickHouse Cloud region in Azure, under which all the Resource groups exist. However, it’s not so straightforward, as we need to keep Resource limits in mind. While AWS/GCP also have resource limits, Azure resource limits are much more extensive and apply to a wider range of resources.


For example, in Azure, there is a limit of [980 resource groups per subscription](https://github.com/MicrosoftDocs/azure-docs/blob/main/includes/azure-subscription-limits-azure-resource-manager.md). Say we have one subscription per region, we could not create more than 980 clusters or have more than 980 customers in that one region. Given our scale, we are very likely to hit this limit quickly.


Similarly, in Azure, there is a limit of [500 storage accounts per](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview#scalability-targets-for-standard-storage-accounts) subscription (by request, the default is 250\). If we create a separate storage account per ClickHouse instance in Azure, we couldn’t support more than 500 customers in a region. Again, this design is not future\-proof. Thus, one subscription per region doesn’t work.


During our design process, we got in touch with architects and engineers from Microsoft Azure and the AKS team, who were very helpful in working through these differences. We discussed design ideas with them to ensure we wouldn’t hit limits like these as we scale. One of our first discussion points with the Azure team was \- should we create one subscription per customer to avoid running into the above resource limits? However, this design is not optimal as subscriptions are meant to be logical containers to hold resources and groupings to help with billing, usage, etc. Creating 1000s of subscriptions under the same tenant is not advisable in Azure.


In collaboration with the Azure team, we designed a solution where we create a **pool of Azure subscriptions for customer ClickHouse clusters**. Whenever a new instance is created by a customer, it is randomly assigned to a subscription picked from the pool and a new resource group is created in this subscription. Subsequently, the storage account, IAM, etc., for the customer instance are created in this Resource Group.


This design works around the resource limit issue we mentioned earlier. Since we now have **\#X** number of subscriptions, all the limits mentioned above are increased **\#X** times, and since **X** is controlled by us, this design is very scalable. Resource groups and storage accounts still have limits on resources, but they largely fall within our requirements since these are per customer, so we are unlikely to hit the limits.


![02_azure.png](/uploads/02_azure_4b8664ad84.png)
Even with this design, there are few hard limits on resources, such as the Kubernetes cluster size (number of nodes), IP limits, etc., which can cause issues at scale.


The next section will explain how we addressed these problems using cellular architecture.


### Scaling ClickHouse Cloud [\#](/blog/clickhouse-cloud-launched-microsoft-launched#scaling-clickhouse-cloud)


Every public cloud provider imposes various limits that must be considered when building services. Additionally, relying on a single, large Kubernetes cluster is generally not advisable.


To ensure our cloud can scale effectively, we can use various approaches:


1. Deploy multiple AKS clusters within a single VNET.
2. Deploy multiple VNETs for different AKS clusters.


Beyond the limits and quotas at the public cloud level, Kubernetes has its own [constraints](https://kubernetes.io/docs/setup/best-practices/cluster-large/).


*As of Kubernetes v1\.30, the following limits apply:*


- *Clusters can have up to 5,000 nodes.*
- *No more than 110 pods per node.*
- *No more than 150,000 total pods.*
- *No more than 300,000 total containers.*


It's crucial that we are prepared to scale our cloud infrastructure to meet demand.


To address this challenge, we utilize a concept called "cells" within each region. This approach is not new to us; we've already employed it to circumvent AWS account limits.


**What is a cell?**


In ClickHouse Cloud, a cell is an independent environment with its own networking and Kubernetes clusters. Cells operate autonomously and do not rely on each other. Think of them as a sharding mechanism. Client connections are directed to the appropriate cell using DNS records, which makes the routing simple.


![03_azure.png](/uploads/03_azure_2473783582.png)
If necessary, we can always deploy a new cell within a region and create new ClickHouse Cloud services in that cell. This process is invisible to end customers.


### Networking [\#](/blog/clickhouse-cloud-launched-microsoft-launched#networking)


The foundation of any cloud infrastructure is its networking stack. In Azure, this is called [VNET](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview). Unlike AWS, where a subnet belongs to a specific availability zone, Azure's subnets do not. This is similar to Google's Cloud Platform (GCP) approach.


This design offers some benefits. For instance, it simplifies the configuration of Azure Kubernetes Service (AKS) node groups. We can create a single AKS node group pinned to multiple availability zones (we use three availability zones to run ClickHouse Cloud services). Kubernetes then manages pod distribution across these zones.


However, despite these advantages, some limitations prevent us from fully utilizing this benefit, which will be explained below.


#### AKS Networking [\#](/blog/clickhouse-cloud-launched-microsoft-launched#aks-networking)


We have been using Cilium as our network CNI since launching our service on AWS in 2022\. We use Cilium due to its utilization of eBPF, which ensures high throughput, reduced latency, and lower resource consumption, particularly when managing many services. You can find more details about this choice in our blog post, "[Building ClickHouse Cloud From Scratch in a Year](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year#network-isolation)." From the start of our Azure project, using Cilium was a no\-brainer. The only decision we needed to make was whether to use the self\-managed version (BYOCNI) or the managed version supported by AKS.


Azure Kubernetes Service (AKS) supports managed Cilium, and it's also possible to install a self\-managed version of Cilium using the [Bring Your Own Container Network Interface (BYOCNI) plugin](https://learn.microsoft.com/en-us/azure/aks/use-byo-cni?tabs=azure-cli).


During our GCP implementation, we decided to use managed Cilium, which helped us reduce the maintenance burden. After a year of running Cilium on GCP, we opted to use the same approach in Azure. You can find details about managed Cilium in Azure [here](https://learn.microsoft.com/en-us/azure/aks/azure-cni-powered-by-cilium).


Another important note about our managed Cilium setup in Azure is that we do not use an overlay network. Instead, pods deployed in AKS use IP addresses from the VNET, which is necessary to support inter\-cluster communication.


#### NAT Gateway story [\#](/blog/clickhouse-cloud-launched-microsoft-launched#nat-gateway-story)


As mentioned earlier, subnets in Azure are not pinned to specific availability zones, simplifying network infrastructure. We started working on NAT gateway implementation but later realized that the simple model offered by Azure would not work for us. We needed to adopt an approach similar to AWS's subnetting strategy, with a subnet per AZ, due to Azure's NAT gateway implementation.


The Azure NAT Gateway handles outbound connections from the VNET. For ClickHouse Cloud, this is a critical component because our clients ingest data from various sources, such as:


- Azure Blob Storage
- S3 buckets
- GCS buckets
- HTTP servers
- MySQL/Postgres databases
- Kafka clusters
- And many more!


If a connection does not belong to a "local" Azure storage account, it will be routed through the NAT Gateway. Efficient and fault\-tolerant data ingestion is essential for ClickHouse Cloud.


Azure NAT Gateway is a zonal resource. If we used just one subnet with a NAT Gateway in AZ 1, an outage in AZ 1 would affect the entire region in ClickHouse Cloud.


![04_azure.png](/uploads/04_azure_6f7ac19995.png)
Therefore, we decided to deploy zonal NAT Gateways to ensure the reliability of ClickHouse Cloud:


![Zones-subnet 2 (1).png](/uploads/Zones_subnet_2_1_2aad6e19c8.png)
*Note: You can find more details about the Azure NAT Gateway deployment model [here](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-availability-zones#zonal-nat-gateway-resource-for-each-zone-in-a-region-to-create-zone-resiliency).*


This setup complicated the AKS node group configuration: instead of having a single node group, we had to create three node groups in AKS. Each node group was pinned to a specific availability zone and subnet.


#### Even more subnets [\#](/blog/clickhouse-cloud-launched-microsoft-launched#even-more-subnets)


In ClickHouse Cloud, we run multiple Kubernetes clusters within a region:


- **Data Plane Cluster(s)**: Hosts ClickHouse/ClickHouse Keeper instances.
- **Data Plane Management Cluster**: Hosts software that manages ClickHouse Cloud and exposes API endpoints for the Control Plane team.
- **Proxy Cluster**: Hosts Istio proxy. All inbound customer connections are terminated in this cluster and then forwarded to the Data Plane Cluster.


In AWS and GCP, it is easy to control network isolation between clusters using security groups. Unfortunately, this was not the case for Azure when ClickHouse Cloud was designed.


While [application security groups](https://learn.microsoft.com/en-us/azure/virtual-network/application-security-groups) could help, they do not work for AKS. To achieve network isolation between clusters, we created three subnets per AKS cluster (one subnet per AZ due to NAT Gateway limitations). This approach increased the complexity of our network infrastructure but allowed us to use [Network Security Groups](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) for network filtering.


![06_azure.png](/uploads/06_azure_08667dce0a.png)
To summarize :


- All traffic between AKS clusters is filtered by VNET Firewall rules.
- Traffic within each cluster is filtered by Kubernetes network policies.


#### Managed Kubernetes ingress [\#](/blog/clickhouse-cloud-launched-microsoft-launched#managed-kubernetes-ingress)


In addition to our proxy cluster, we expose other endpoints for internal needs, such as the Data Plane API service.


In AWS and GCP, we use managed ingress to terminate TLS and filter traffic (WAF). The closest equivalent in Azure is the [Azure Application Gateway v2](https://learn.microsoft.com/en-us/azure/application-gateway/overview-v2), but it requires infrastructure changes, such as a dedicated subnet, which was more than we needed. Therefore, we initially opted for the NGINX ingress controller in Azure. This worked fine until we started implementing advanced traffic filtering configurations. Managing these configurations with NGINX was difficult, and leveraging Istio for this task was much easier, especially since we already had Istio expertise at ClickHouse.


We migrated from NGINX to Istio ingress for our API server, and it performed seamlessly. We plan to migrate from managed ingress solutions to Istio in AWS and GCP as well. [Istio](https://istio.io/), combined with [cert manager](https://github.com/cert-manager/cert-manager) and [external DNS](https://github.com/kubernetes-sigs/external-dns), works great.


## Azure support in ClickHouse [\#](/blog/clickhouse-cloud-launched-microsoft-launched#azure-support-in-clickhouse)


We use the Azure C\+\+ SDK to work with Azure Blob Storage in ClickHouse, and for authentication, we use [Workload Identity](https://azure.github.io/azure-workload-identity/docs/). Workload Identity is the next iteration of Azure AD Pod Identity, which enables Kubernetes applications to access Azure cloud resources securely.


For reading files from Azure Blob Storage, we use the approach of downloading and reading from stream. This makes it efficient, especially for large files, as we don’t have to download the whole file and can continue to read in parts or as much as needed. We also read files in [parallel](https://github.com/ClickHouse/ClickHouse/pull/61503/) when feasible.


For writing to Azure Blob Storage, we use multipart upload for large files and take advantage of single\-part upload whenever possible to make it fast. Combined with our asynchronous and parallel writing, this means we can write files efficiently. For [copying](https://github.com/ClickHouse/ClickHouse/pull/56988) files, we can configure ClickHouse to use native copy, which directly copies files without having to read \& write them. When copying large files using read \+ write, we read the file in parts \& write them to Azure blob storage in order to handle memory efficiently.


One of the major performance boosts was seen when we adjusted the retries. Azure SDK has large backoff delays, and reducing them improved our performance. Now, we have added the option to [configure](https://github.com/ClickHouse/ClickHouse/pull/62608/) them as well.


### OpenSSL [\#](/blog/clickhouse-cloud-launched-microsoft-launched#openssl)


Workload identity credentials were supported only by Azure C\+\+ SDK starting from version 1\.8\. Since ClickHouse used an older version of the SDK (version 1\.3\) at that time, we started to upgrade the SDK. Upgrading up to [version 1\.7](https://github.com/ClickHouse/ClickHouse/pull/58075) was fine.


That said, the [upgrade to version 1\.8](https://github.com/ClickHouse/ClickHouse/pull/62702) broke.


This was because the Azure SDK v1\.8 introduced a dependency on [OpenSSL](https://www.openssl.org/) as an encryption library, which we could not easily patch out. We were also reluctant to make changes in third\-party code, especially in security\-related areas. Prior to that, ClickHouse (and Azure) was compiled against boringssl, Google’s fork of OpenSSL, which was created in the aftermath of the [Heartbleed bug](https://heartbleed.com/) many years ago.


So, we set out to migrate ClickHouse from boringssl to OpenSSL. Being such an important and fundamental library, this migration was rather complex. We will highlight two notable issues that stood out during this transition:


Our initial migration attempt involved OpenSSL in version 3\.0\. After making OpenSSL build on ClickHouse’s platforms (e.g., x86, ARM, PPC, RISC\-V, and others), all functional tests passed except this one test for ClickHouse’s [encrypting codec](https://clickhouse.com/docs/en/sql-reference/statements/create/table#encryption-codecs). It [turned out](https://github.com/ClickHouse/ClickHouse/pull/56398#issuecomment-1937766144) that the codecs were based on modern misuse\-resistant [AES\-GCM\-SIV ciphers](https://en.wikipedia.org/wiki/AES-GCM-SIV), with OpenSSL supporting these ciphers only from [version 3\.2](https://github.com/openssl/openssl/issues/16721). In order to stay compatible with existing user data encoded with encrypting codecs, we had to start from scratch using OpenSSL 3\.2\.


The other class of issue was related to “code sanitization,” a technique which executes code with special instrumentation to find tricky and rare bugs. ClickHouse is notorious for running most of its tests with sanitization and frequently finding bugs in the third\-party libraries it uses. This time was no different \- testing revealed bugs in the venerable OpenSSL codebase! We reported the issues upstream, where they were quickly fixed, for example, [here](https://github.com/openssl/openssl/issues/24629) and [here](https://github.com/openssl/openssl/pull/24295). That’s the power of open source!


## Performance Benchmarking [\#](/blog/clickhouse-cloud-launched-microsoft-launched#performance-benchmarking)


ClickHouse is one of the fastest databases in the world. Performance is sacred to us. So naturally, once we built ClickHouse Cloud on Azure, we couldn’t wait to benchmark it against our product on AWS/GCP. You might’ve heard of our handy open\-source tool called ClickBench, which is widely used for performance benchmarking. Using this tool, we went through multiple rounds of improvements to tune ClickHouse for Azure Blob Storage. Some of the optimizations were mentioned in the section above. Looking at the final results, Azure performs very well in ClickBench. The public ClickBench results can be found here \- <https://benchmark.clickhouse.com/>.


On a hot run, Azure is the fastest of all 3 clouds in ClickBench.


![07_azure.png](/uploads/07_azure_6c0f9e77dc.png)
On a cold run, Azure is faster than GCP and slower than AWS, but overall it performs very well.


![08_azure.png](/uploads/08_azure_285424b668.png)
These results gave us confidence that our Azure offering was on par with the other clouds in terms of performance.


## Azure Marketplace [\#](/blog/clickhouse-cloud-launched-microsoft-launched#azure-marketplace)


Last but not least, let’s discuss billing. You can sign up for [ClickHouse Cloud](https://auth.clickhouse.cloud/u/signup) directly, or you can sign up through the [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/clickhouse.clickhouse_cloud?tab=Overview). Through the Marketplace, you’ll have unified billing along with all your other Azure resources \- your ClickHouse Cloud organization and its resources are bound to your Azure subscription. Our integration with the Azure Marketplace allows you to either pay for your Azure consumption on a PAYG (pay\-as\-you\-go) basis, or sign a committed contract over a specified period.


If your organization has a pre\-committed spend agreement with Azure, you may be able to apply some of that committed spend towards ClickHouse Cloud consumption on Azure.


## Takeaways \& conclusion [\#](/blog/clickhouse-cloud-launched-microsoft-launched#takeaways--conclusion)


When we set out to build ClickHouse Cloud on Azure, we expected that, since we’d already built our service on AWS/GCP, we could apply a lot of the learning and architecture to make it easier for Azure. Although many of these did apply, there were quite a few complications and differences in setup that we didn’t expect. In this blog, we’ve discussed some of the important ones like resource organization, resource limits, network setup etc. We also had great help from the Microsoft Azure team in ensuring that we were able to design for scale while following Azure best practices.


We’re also looking forward to seeing some improvements from the Azure platform. For reliability's sake, each ClickHouse Cloud cluster has pods deployed in 3 AZs. However, not all regions in Azure support 3 AZs yet. In the future, this would be a feature from Azure that would help with reliability.


This blog was contributed by Vinay Suryadevara, Timur Solodovnikov, Smita Kulkarni \& Robert Schulze on the ClickHouse Cloud team.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
