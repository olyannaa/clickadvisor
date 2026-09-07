---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Cisco
topic: cisco-talos-empowers-threat-researchers-while-reducing-tco-by-75-with-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 5
---

and our threat hunters use them to look for low prevalence hashes that might be signals for malware campaigns. In both cases, they, and by extension, our customers need fast, accurate answers." — Senay Goitom, Software Engineer, Cisco

But delivering those answers is, as Senay puts it, like searching for a needle in a haystack. In production, the dataset holds nearly 2 trillion rows, with 27 billion new rows ingested daily. On disk, that's around 192 TB of compressed data, or around 2 PB uncompressed. Because these systems power threat intelligence services for Cisco customers, latency and accuracy directly impact the company's security products.

At our [2026 Open House SF user conference](https://clickhouse.com/openhouse/san-francisco), Senay shared how he and the team moved this workload from OSS ClickHouse to [ClickHouse Cloud](https://clickhouse.com/cloud) on AWS and how it helped Cisco dramatically reduce costs with zero downtime.

## Outgrowing the old architecture \#

In the original design, data originated in a Databricks Delta table stored as Parquet files in S3\. A custom, event\-driven serverless ingestion pipeline fed a self\-managed Kubernetes (EKS) cluster, where a staging table rolled up into an aggregated table behind an API endpoint. Under the old retention policy, the team kept about a petabyte of compressed, replicated data on 32 high\-compute nodes, each with seven EBS volumes attached.

![](/_next/image?url=%2Fuploads%2Fciscotalos_jun2026_image1_63d917b06b.jpg&w=2048&q=75)

*Cisco Talos's original self\-managed architecture: a custom ingestion pipeline feeds an EKS cluster, with data flowing from a staging table to an aggregated table behind an API endpoint.*

"It worked," Senay says, "but we started experiencing some challenges." As a small team inside a threat research organization, they found that running a cluster of that size pulled them away from their actual mission. "We were spending time on upgrades, backups, and troubleshooting," he explains, "instead of building new products for our threat researchers."

That setup also tied the team's storage to compute in a costly way. "Query performance needs meant we had to tie our ever\-increasing storage needs to expensive compute nodes," Senay says. "Scaling up or down, depending on traffic, was a costly process and risked service disruption for our consumers. We have to ensure customer trust, so it ultimately meant that we had to over\-provision."
