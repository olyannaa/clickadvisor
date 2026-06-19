---
source: blog
url: https://clickhouse.com/docs/operations/system-tables/query_log
topic: building-clickhouse-byoc-bring-your-own-cloud-on-aws
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 10
---

providing the right level of abstraction to make the solution both user\-friendly and flexible. ## Key challenges [\#](/blog/building-clickhouse-byoc-on-aws#key-challenges) Implementing a BYOC model introduces several challenges that must be addressed to ensure a seamless and secure experience for customers.

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
