---
source: blog
url: https://clickhouse.com/cloud/clickpipes?utm_source=google.com&utm_medium=paid_search&utm_campaign=21862172336_181837693625&utm_content=764403839926&utm_term=clickpipes_g_c&gad_source=1&gad_campaignid=21862172336&gclid=CjwKCAjwisnGBhAXEiwA0zEOR3kM4ZBQO0_NpfRPpYU2YWG5onZqwF-Kf8m845Ol2IJeyN96r0k8DxoCit4QAvD_BwE)**
topic: azure-blob-storage-connector-for-clickpipes-is-now-generally-available
ch_version_introduced: '3.6'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 3
---

# Azure Blob Storage connector for ClickPipes is now Generally Available

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Azure Blob Storage connector for ClickPipes is now Generally Available

![](/_next/image?url=%2Fuploads%2FMarta_Paes_Moreira_no_background_9853166ee2.png&w=96&q=75)[Marta Paes](/authors/marta-paes)Sep 24, 2025 · 5 minutes read![azure-blog-banner.png](/uploads/azure_blog_banner_5fda937064.png)
We're excited to announce that the **Azure Blob Storage connector for [ClickPipes](https://clickhouse.com/cloud/clickpipes?utm_source=google.com&utm_medium=paid_search&utm_campaign=21862172336_181837693625&utm_content=764403839926&utm_term=clickpipes_g_c&gad_source=1&gad_campaignid=21862172336&gclid=CjwKCAjwisnGBhAXEiwA0zEOR3kM4ZBQO0_NpfRPpYU2YWG5onZqwF-Kf8m845Ol2IJeyN96r0k8DxoCit4QAvD_BwE)** is now Generally Available! You can seamlessly load files from Azure Blob Storage into ClickHouse Cloud with even **better performance**, and leverage the new support for **programmatic access** (via OpenAPI and Terraform) to manage your ClickPipes with confidence.

Over the past few months, the connector has gone through an extensive beta phase, with customers moving anywhere between a few GiB to **as much as 60\+ PiB of data** into ClickHouse Cloud — validating its reliability and scalability for both small\- and enterprise\-scale data lake analytics workloads.

> [Sign up for ClickHouse Cloud](https://console.clickhouse.cloud/signup) today to try out the [Azure Blob Storage connector for ClickPipes](https://clickhouse.com/cloud/clickpipes)!

![azure-blog.gif](/uploads/azure_blog_d52244e13f.gif)
## What's new? [\#](/blog/azure-blob-storage-connector-ga#whats-new)

Based on customer feedback, and to align the connector with the product experience for other object storage ClickPipes, the Azure Blob Storage connector has been upgraded with:

### Custom HTTP client for better performance [\#](/blog/azure-blob-storage-connector-ga#custom-http-client-for-better-performance)

From the rollout of ClickHouse v25\.8 to ClickHouse Cloud, the connector will leverage a new, custom HTTP client that delivers more consistent and better performance than the original Azure SDK native client. This brings the connector to parity with object storage ClickPipes for other cloud providers, when it comes to performance.

### Terraform and OpenAPI support [\#](/blog/azure-blob-storage-connector-ga#terraform-and-openapi-support)

For mature ClickPipes deployments using workflow automation and Infrastructure as Code (IaC), a new `azureblobstorage` source type is available in [the ClickPipes OpenAPI specification](https://clickhouse.com/docs/cloud/manage/api/swagger#tag/ClickPipes), as well as the ClickHouse Terraform Provider ([3\.6\.0\-alpha1](https://github.com/ClickHouse/terraform-provider-clickhouse/releases/tag/v3.6.0-alpha1)\+). Here's an example of how you'd configure an Azure Blob Storage ClickPipe resource in Terraform:

> **Note**: ClickPipes resources are only supported in [alpha releases](https://registry.terraform.io/providers/ClickHouse/clickhouse/3.7.0-alpha1/docs/resources/clickpipe) of the ClickHouse Terraform provider. Regardless, support for object storage ClickPipes is considered **stable**.
