---
source: blog
url: https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws
topic: clickhouse-byoc-on-google-cloud-now-generally-available
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 3
---

account or project boundaries. ClickHouse BYOC is already available across all public ClickHouse Cloud Google regions. Over time we will expand support to additional Google Cloud regions. ## **Initial Set up** [\#](/blog/byoc-gcp-ga#initial_set_up) Onboarding uses a three\-step Terraform\-based setup:

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
