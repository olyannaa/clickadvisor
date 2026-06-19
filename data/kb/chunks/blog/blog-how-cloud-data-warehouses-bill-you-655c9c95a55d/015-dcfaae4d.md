---
source: blog
url: https://benchmark.clickhouse.com
topic: how-the-5-major-cloud-data-warehouses-really-bill-you-a-unified-engineer-friendly-guide
ch_version_introduced: '3.64'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 17
---

it with **16 RPUs** (as sketched in the diagram above). If the query’s wall\-clock runtime is **60 seconds**, then the billed compute is simply: **16 RPUs × 60 seconds \= 960 RPU\-seconds** ### Scaling: ML\-driven predictive allocation [\#](/blog/how-cloud-data-warehouses-bill-you#scaling-ml-driven-predictive-allocation)

Redshift Serverless automatically scales the compute assigned to your workgroup within a range you configure. The range has two bounds:

- **Base capacity** — the minimum number of RPUs always available to your workgroup ([default 128 RPUs](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html), configurable from **4 to 512 RPUs**, or up to **1024 RPUs** in select regions).
- **Maximum capacity** — the upper limit that Redshift is allowed to scale to under load.

Scaling is:

- **Automatic** (no clusters or nodes to resize)
- **Predictive** (ML models pre\-allocate RPUs when heavy queries are likely)
- **Constrained** by your configured base and max limits to keep costs predictable

When load drops, Redshift scales down toward the base capacity, releasing unused RPUs. RPUs will drop to zero if you don't run queries in the Redshift serverless environment, and if this remains at zero for an extended period, a cold start will occur (see the Metering granularity section below).

> **How Redshift’s scaling differs from BigQuery’s**  
>   
> BigQuery scales threads dynamically during execution; Redshift scales the entire compute envelope upfront: Compared with BigQuery’s slot\-based model, Redshift Serverless **adjusts the entire query’s compute size (RPUs) upfront**, whereas BigQuery **redistributes many small execution threads (slots) across stages while the query runs**.   
>   
> Once Redshift selects the RPU level, the whole query runs on that fixed amount of compute.

### Compute pricing [\#](/blog/how-cloud-data-warehouses-bill-you#compute-pricing-4)

*(Official pricing, November 2025 → <https://aws.amazon.com/redshift/pricing/>)*

For **US East (N. Virginia)**, the on\-demand price is **$0\.375 per RPU\-hour**.

### Metering granularity [\#](/blog/how-cloud-data-warehouses-bill-you#metering-granularity-4)

*(Metering behavior, November 2025 → AWS docs: [Amazon Redshift Serverless compute pricing details](https://aws.amazon.com/redshift/pricing/))*

Redshift Serverless bills RPU usage per second, with a 60\-second minimum charge.

Redshift automatically manages compute capacity and instantly scales to zero when not in use. There is no manual idle\-timeout setting, the service auto\-pauses internally until new queries arrive.

Redshift Serverless typically resumes quickly when the warm pool is still active. However, after longer idle periods, AWS may de\-allocate resources and a cold start can introduce tens of seconds of delay, even though this behavior is not surfaced explicitly in public documentation.
