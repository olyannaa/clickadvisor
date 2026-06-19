# Building ClickHouse BYOC (Bring Your Own Cloud) on AWS


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building ClickHouse BYOC (Bring Your Own Cloud) on AWS

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_5_330c6e9bbc.png&w=96&q=75)[Jianfei Hu](/authors/jianfei-hu) and [Yiyang Shao](/authors/yiyang-shao)Mar 12, 2025 · 17 minutes read![Blog_BYOC_202502_V1.0-02.png](/uploads/Blog_BYOC_202502_V1_0_02_6b231bf877.png)
In this blog post, we’ll discuss in detail how we built this new product offering, including the challenges we faced, and how we worked through them.


## Introduction to BYOC [\#](/blog/building-clickhouse-byoc-on-aws#introduction-to-byoc)


The concept of Bring Your Own Cloud (BYOC) is becoming increasingly popular as organizations seek greater control over their cloud environments, while also benefiting from the flexibility and scalability that cloud platforms provide. At ClickHouse, we recognized this trend and saw an opportunity to offer our customers a way to deploy ClickHouse in their own cloud infrastructure, specifically on AWS.


BYOC allows customers to deploy ClickHouse Cloud in their own Virtual Private Cloud (VPC) , thereby they are in control of networking, security, and compliance, while still leveraging the benefits of a fully managed offering. This deployment model provides a balance between the autonomy of self\-managed infrastructure and the convenience of a fully managed database service.


When designing this offering, we tackled a few interesting challenges to ensure a seamless integration of ClickHouse with the customer’s cloud environment. These challenges included setting up and managing the VPC, ensuring network connectivity, implementing auto\-provisioning mechanisms for cloud resources, and providing the right level of abstraction to make the solution both user\-friendly and flexible.


## Key challenges [\#](/blog/building-clickhouse-byoc-on-aws#key-challenges)


Implementing a BYOC model introduces several challenges that must be addressed to ensure a seamless and secure experience for customers.


- **Infrastructure Automation:** Automating the deployment of ClickHouse instances within customer\-managed cloud environments while maintaining reliability and security.
- **Data Residency \& Compliance:** Ensuring that customer data remains fully within their environment and meets compliance requirements.
- **Network Security \& Isolation:** Ensuring secure communication between the management and data planes while preventing unauthorized access to ClickHouse clusters.
- **Resource Management:** Providing customers with fine\-grained control over resource allocation while enabling automatic scaling and monitoring.
- **Reduce Operational Complexity:** Simplifying Kubernetes and infrastructure management for customers who may not have extensive expertise in cloud\-native technologies.


## Auto\-provisioning of Cloud Resources [\#](/blog/building-clickhouse-byoc-on-aws#auto-provisioning-of-cloud-resources)


### Easy onboarding [\#](/blog/building-clickhouse-byoc-on-aws#easy-onboarding)


A core component of the BYOC offering is the ability to automatically provision all necessary cloud resources (like VPC, EKS Clusters, IAM Roles, security groups, etc.) within the customer’s cloud account. This presented several challenges around resource management and ensuring that these resources were appropriately configured and secured.


To address this, we leveraged AWS CloudFormation and Crossplane to automate the creation and management of these resources, allowing our customers to quickly set up and deploy ClickHouse within their cloud environment without having to manually configure each resource. This automation also ensures that all resources are consistently deployed with the correct settings, reducing the likelihood of misconfigurations.


The customer is able to create a BYOC setup via several simple steps.


1. **IAM Role Creation:** The customer uses a ClickHouse\-provided CloudFormation template to create an IAM role, granting ClickHouse access to their cloud account.
2. **Configuration and Provisioning:** The customer specifies region, VPC CIDR range, and availability zones. ClickHouse then automatically provisions the cloud components and installs necessary cloud services.
3. **ClickHouse Service Creation:** Once cloud components are ready, the customer can create their first ClickHouse service, similar to the ClickHouse managed cloud experience.


### Cloud infrastructure separation [\#](/blog/building-clickhouse-byoc-on-aws#cloud-infrastructure-separation)


A central design goal of the ClickHouse BYOC offering was the clear separation between the ClickHouse management services and the data plane EKS cluster. This separation ensures that customers maintain full control over their cloud infrastructure while allowing ClickHouse to handle operational tasks, such as provisioning, monitoring, and scaling of the ClickHouse clusters.


![Blog_BYOC_architecture_202502_V1.0-02.png](/uploads/Blog_BYOC_architecture_202502_V1_0_02_c92ad04457.png)
- **Management Services** handle tasks like orchestration, configuration management, monitoring, and backups etc. Management services reside in the ClickHouse VPC, and do not have direct access to customer data, but interact with customer resources through secure private endpoints.
- **Data Plane** is where ClickHouse runs. It resides within the customer’s VPC, ensuring that all data storage, processing, and querying happen on infrastructure they control. The data plane is customizable, allowing the customer to configure EC2 instances, VPC settings, and security groups to meet their specific needs.


By decoupling the management and data planes, we give customers complete control over their cloud environment while abstracting away much of the operational complexity of managing ClickHouse.


## Data isolation and compliance [\#](/blog/building-clickhouse-byoc-on-aws#data-isolation-and-compliance)


### Data storage [\#](/blog/building-clickhouse-byoc-on-aws#data-storage)


Keeping your data safe and sound is our top priority! With our BYOC model, all your data, including metrics, logs stays in your very own VPC.


- Your logs are stored locally on EBS.
- Metrics, which are also stored locally, use the Prometheus/Thanos stack.


We also aim to maintain the stability and reliability of ClickHouse services. Data transfer is limited to essential telemetry for service status visibility and billing. In case of service failure, alerts will be sent to ClickHouse PagerDuty, and our engineers will be promptly notified to resolve the issue and minimize service disruptions.


### Access for troubleshooting [\#](/blog/building-clickhouse-byoc-on-aws#access-for-troubleshooting)


One of the key differences between BYOC and our managed cloud is that in the BYOC model, our engineers will have limited access to the ClickHouse services, since they are located in the customer’s VPC.


Kubernetes access is needed for troubleshooting issues such as EBS mount failure, and node level network issues. When ClickHouse services in a customer account are experiencing issues, a ClickHouse on\-call engineer may need access to the customer's EKS for troubleshooting.


We began designing with the following goals in mind:


- Access must be approved and audited.
- Access permissions must be separated for each BYOC setup.
- Permissions must be limited and controlled. For example, reading secrets and executing into a pod will not be allowed.


Our solution follows a controlled escalation process:


1. Engineers request access through an internal approval system.
2. A designated approvers group reviews and grants access if necessary.
3. The system temporarily enables access for the approved engineer, which automatically expires after a set time.


Both ClickHouse and customers can audit access activity. ClickHouse monitors access requests and logs, while customers can track activity from ClickHouse engineers within their own systems.


The above process allows support engineers to access EKS clusters, but does not provide access to the ClickHouse instances. For this a separate certificate based mechanism is required.


#### Certificate based auth for system table access [\#](/blog/building-clickhouse-byoc-on-aws#certificate-based-auth-for-system-table-access)


In situations where on\-call engineers need to connect to the ClickHouse service for debugging and improving query performance, they will establish a private connection through Tailscale and authenticate using a temporary certificate. This connection will only grant access to system tables, specifically for diagnostic purposes.


The process is as follows:


1. On\-call engineers within the designated Okta group make a request to access the customer ClickHouse instance system table. This also generates a time bound certificate.
2. The ClickHouse operator configures ClickHouse to accept the certificate.
3. On\-call engineers access the instance via Tailscale using the certificate.


In the BYOC environment, all ClickHouse support access will be cert based. We have shut down password based access for any human access. The setup is only able to access system tables such as [`query_log`](https://clickhouse.com/docs/operations/system-tables/query_log), not customer data. It is enforced via a ClickHouse user profile, which grants only access to system tables. Customers can also identify such accesses in the same `query_log`.


#### Tailscale connection [\#](/blog/building-clickhouse-byoc-on-aws#tailscale-connection)


![Blog_BYOC_architecture_202502_V1.0-03.png](/uploads/Blog_BYOC_architecture_202502_V1_0_03_dce981ef4e.png)
We use Tailscale to provide ClickHouse engineers access to endpoints hosted in customer EKS clusters. For each endpoint/service we want to be accessed via Tailscale, we have:


1. One tailnet address registered. For example `k8s.xxxx.us-east-1.aws.byoc.clickhouse-prd.com` for the k8s API server.
2. A tailscale agent container responsible for coordinating network setup. An agent would send requests to its corresponding Nginx pod.
3. The Nginx pod terminates TLS traffic and then routes traffic to corresponding IPs within the EKS cluster.


The secure network communication setup takes a few steps:


1. The Tailscale agent on both the ClickHouse engineers work environment and the BYOC EKS cluster connect to the Tailscale [coordination server](https://tailscale.com/kb/1155/terminology-and-concepts#coordination-server).  

a. The Tailscale agent from EKS cluster registers the K8s service to let it be discoverable.
b. The employee tailscale agent may or may not have the access to this service, and needs to escalate internally to gain visibility.
2. After the K8s service information becomes visible to the engineer's machine, agents on both ends try to establish Direct Mode via a NAT traversal tunnel.
3. If this fails, Tailscale falls back to relay mode: communication goes through a [DERP server](https://tailscale.com/kb/1232/derp-servers) from Tailscale.


Regardless of direct or relayed mode, communication is encrypted end\-to\-end [as each Tailscale agent](https://tailscale.com/blog/how-tailscale-works#the-control-plane-key-exchange-and-coordination) generates their own public private key pair similar to PKI.


Tailscale agents in the EKS cluster initiate connections to the relay server/coordination server. There’s no SecurityGroups to allow inbound connection to tailscale agents.


In conclusion, we guarantee that all remote access activities are permission\-controlled, audited, and established through private connections. Most importantly, our engineers have no means to access any customer data stored in ClickHouse services.


#### Management services access to Kubernetes [\#](/blog/building-clickhouse-byoc-on-aws#management-services-access-to-kubernetes)


![Blog_BYOC_architecture_202502_V2.0.png](/uploads/Blog_BYOC_architecture_202502_V2_0_0ca4cc99bb.png)
By default our management services access the BYOC Kubernetes cluster via an EKS [API server](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) public IP address. We configure an EKS cluster to ensure that API server only allows IP addresses from our NAT gateway IP list.


If needed, we can also configure EKS API server to only have a private endpoint. In this case, management services access API servers via the [Tailscale](https://tailscale.com/) zero trust network, similar to human access above. We keep the public access only as a backup mechanism in case of Tailscale issues for emergency investigation and support needs.


### VPC Peering and PrivateLink [\#](/blog/building-clickhouse-byoc-on-aws#vpc-peering-and-privatelink)


To enhance security and isolation, we recommend hosting ClickHouse BYOC services in a dedicated VPC separate from other VPCs running different applications. This approach minimizes risks and ensures better traffic management.
By default, ClickHouse BYOC provides a public endpoint with a configurable IP allowlist to restrict access. However, for better security and performance, we strongly recommend using private connectivity options such as [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html) or [AWS PrivateLink](https://aws.amazon.com/privatelink/).


- **VPC Peering:** Customers can [establish VPC Peering connections](https://clickhouse.com/docs/en/cloud/reference/byoc#optional-setup-vpc-peering) for low\-latency, private communication between their application VPC and the ClickHouse BYOC VPC.
- **AWS PrivateLink:** PrivateLink is another alternative to secure connections, allowing customers to access ClickHouse BYOC services without exposing traffic to the public internet. PrivateLink can be easily enabled through the **ClickHouse Cloud Console**, simplifying the setup process.


![vpc_cloud_byoc.png](/uploads/vpc_cloud_byoc_e1781e8cd6.png)
## Resource management [\#](/blog/building-clickhouse-byoc-on-aws#resource-management)


In ClickHouse Cloud, we have invested significant effort into tackling resource contention and "noisy neighbor" issues within our Kubernetes clusters, enhancing resource utilization and overall efficiency. However, the BYOC model presents a unique challenge as customers own and manage their EKS clusters, and these clusters are solely dedicated to their ClickHouse services. This led us to focus our efforts towards resource utilization on each node, ensuring optimal use with no wasted resources. Specifically, this means ensuring replicas are assigned to nodes such that resources are not wasted e.g. assigning a small replica exclusively to a large node.


First, we reduced the overhead of running non\-ClickHouse services (proxy, operator, and monitoring stacks). Because these services are no longer shared among multiple customers, we were able to decrease both the number of replicas and the overall resource allocation.
Next, we tackled the challenge of scheduling ClickHouse server pods. Initially, we created node pools with all instance types in the m7gd family, each with a minimum size of 0, and relied on the Kubernetes default scheduler and the AWS cluster autoscaler to manage them. However, we encountered several challenges with this approach:


- Determining resource allocation for the ClickHouse server was difficult due to DaemonSets (such as Cilium and Observability components) occupying a certain amount of resources. This sometimes caused our pre\-defined resource allocation to fail scheduling on the corresponding node group. The pre\-defined resource allocation shared with our managed cloud is not easily changed.
- During scale\-in operations, the ClickHouse server was not reallocated to a node group with a smaller instance type due to the behavior of the cluster autoscaler, leading to wasted resources.


To solve these issues, we introduced **Custom Profiles**, enabling the customization of resource allocation and configuration (e.g., SSD cache) for different instance types. This approach optimizes performance by ensuring that workloads are scheduled on the most suitable hardware, reducing inefficiencies caused by misallocated resources. Each node group is assigned a corresponding label, and a node selector is used in the ClickHouse server pod during creation or scaling.


Additionally, the web console dynamically displays all available custom profiles and node groups on a specific BYOC setup, allowing users to:


- Custom configure available instance sizes.
- Select different CPU/Memory ratios (e.g., 1 or 1) based on workload needs.
- Optimize ClickHouse deployments for cost efficiency and performance.


This approach ensures customers get maximum value from their AWS resources while maintaining full flexibility over instance types and configurations.


## Easy maintenance [\#](/blog/building-clickhouse-byoc-on-aws#easy-maintenance)


To simplify Day 2 operations and ongoing maintenance, we aim to provide maximum flexibility and control for our BYOC customers. One critical aspect of this is managing upgrades efficiently to minimize disruptions while ensuring security and performance improvements.


### Scheduled upgrades [\#](/blog/building-clickhouse-byoc-on-aws#scheduled-upgrades)


We give BYOC customers full control over upgrades by allowing them to define a [scheduled upgrade time window](https://clickhouse.com/docs/en/manage/updates#scheduled-upgrades). Customers can specify a preferred maintenance window to ensure that updates happen at a time that minimizes impact on their workloads.


### Managed Kubernetes upgrade [\#](/blog/building-clickhouse-byoc-on-aws#managed-kubernetes-upgrade)


Secondly, EKS serves as a core cloud component and needs long term maintenance such as upgrading versions, and node group updates. Regularly updating your Amazon Elastic Kubernetes Service (EKS) clusters is essential to maintain security, access to new features, and ensure compatibility with the broader Kubernetes ecosystem. Also, operating on a version in extended support results in additional charges.


Using the CSP console to upgrade K8S is one of the choices. However, to achieve greater control over the upgrade process, minimize service interruptions, and ensure scalability across multiple cloud providers, ClickHouse has developed a self\-managed solution called **Kubernetes Upgrader**. This engineered approach provides fine\-grained control over the upgrade workflow, allowing for better coordination, reduced downtime, and seamless operation across different cloud environments.


The upgrade process is designed to **separate the EKS control plane upgrade from the Node Group upgrade**, ensuring minimal disruption and maintaining stability. Additionally, the **scheduled upgrade window** set by users is fully respected throughout the process.


- The first step in the upgrade process is upgrading the **Kubernetes Control Plane**. This ensures that API server, controller manager, and scheduler components are upgraded before worker nodes.
- After the control plane is upgraded, the **Node Group upgrade** process begins. The workflow involves:


	- **Node group duplication**: A new group of nodes is created with the upgraded configuration.
	- **Applying taints to old nodes**: Prevents new workloads from being scheduled on outdated nodes.
	- **Cordon \& drain process**: Workloads on old nodes are safely migrated to upgraded nodes.
	- **Skipping ClickHouse pods with an active upgrade window**: Ensures that pods continue to respect maintenance schedules and are not disrupted.
	- **Old Node Removal**: Once the migration is complete, outdated nodes are deleted.
- If additional **Kubernetes Addons** require upgrades (e.g. monitoring, networking, or logging components), they are upgraded in this final step.


The entire workflow follows an **idempotent flow**, meaning it can be re\-executed without causing duplicate or unintended side effects.


This structured approach enables safe, controlled, and scalable Kubernetes upgrades, minimizing service disruptions while providing full flexibility and control.


## Future Improvements [\#](/blog/building-clickhouse-byoc-on-aws#future-improvements)


While our BYOC implementation is robust, there are still areas we are looking to enhance:


- **Multi\-Cloud Support** – Our current BYOC implementation is optimized for AWS, but we are considering expanding to GCP and Azure to give customers more flexibility in their infrastructure choices.
- **ClickPipes support**– We would like to offer the same ClickPipe ingestion capabilities for BYOC while keeping the data in customers’ own VPC.
- **Self\-Service Capabilities** – We are working on enhancing the ClickHouse Cloud Console to give customers more control over their BYOC setup, including better customization of infrastructure and real\-time insights into their deployments.
- **Advanced Security Model** – Security is a top priority for BYOC, and requirements can vary among customers. We will continuously refine our security posture. This includes strengthening identity and access management (IAM),refining audit logging, and improving network isolation strategies.
- **More Flexibility** \- We aim to support a wider range of deployment configurations, including the ability to run BYOC within an existing customer\-managed VPC.


As we continue to iterate on our BYOC offering, we are committed to making it more secure, performant, and user\-friendly, ensuring that customers can get the best of ClickHouse while maintaining full control over their cloud environment.


## Conclusion [\#](/blog/building-clickhouse-byoc-on-aws#conclusion)


Building ClickHouse BYOC (Bring Your Own Cloud) on AWS has been an exciting journey, enabling our customers to deploy ClickHouse within their own cloud environments while benefiting from our fully managed service. We tackled key challenges, such as infrastructure automation, network security, data isolation, and resource management, to ensure a seamless and secure deployment experience.


Through auto\-provisioning mechanisms, customers can quickly and efficiently set up their ClickHouse instances within their VPCs. The separation of management and data planes ensures security and compliance, while our approach to network access via Tailscale and IAM role\-based permissions provides both security and flexibility for troubleshooting.


In addition, we focused on optimizing resource management within customer\-owned EKS clusters, ensuring efficient resource utilization while maintaining performance. With scheduled upgrade support and a Kubernetes Upgrader for managed EKS maintenance, we provide customers with control over their infrastructure while minimizing operational overhead.


BYOC empowers customers with flexibility, security, and scalability, giving them complete control over their cloud infrastructure while offloading operational complexities to ClickHouse.


## Get started now [\#](/blog/building-clickhouse-byoc-on-aws#get-started-now)


If ClickHouse BYOC on AWS is the right fit for your needs, please [contact us](/cloud/bring-your-own-cloud) to get started.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
