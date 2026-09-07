---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-external-backups-on-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 6
---

ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits. [Sign up](https://console.clickhouse.cloud/signUp?loc=blog-global-cta&utm_blogctaid=1) #### ClickHouse Cloud Configuration \# On the ClickHouse Cloud console, you will need to configure the external bucket.

1. On the Settings page, click on “Set up external backup”

![Image 2.png](/_next/image?url=%2Fuploads%2FImage_2_75696b2c9e.png&w=2048&q=75)

2. On the subsequent screen, provide the AWS IAM Role ARN you just created and the S3 bucket URL in the following format

![Image 3...png](/_next/image?url=%2Fuploads%2FImage_3_7c0b7df0fb.png&w=2048&q=75)

That’s it, and the first external backup will start within an hour!

By default, backups will then be taken daily (as specified [here](https://clickhouse.com/docs/cloud/manage/backups/overview#default-backup-policy)). However, for additional control, we also support [configurable](https://clickhouse.com/docs/cloud/manage/backups/configurable-backups) backups to your own cloud account to set a custom schedule. You are able to set a start time and frequency (with daily being the most frequent option) for backing up to external buckets.

Up until now, external backups may appear quite similar to the default backups within ClickHouse Cloud. However, there are two important distinctions that set external backups apart:

The first key difference is in lifecycle management. Unlike ClickHouse Cloud backups, which are automatically lifecycled (i.e., deleted once a defined TTL is past, given there are a sufficient number of newer backups), external backups are not managed by ClickHouse Cloud once they are written to the external storage location e.g., S3 bucket. This decision was made because:

1. ClickHouse cloud cannot be certain that it knows where the backup is after it is written to the external storage (for example, the backups could be moved to cold storage to save costs), and
2. External backups can be stored as long as you want and according to whatever conditions you want. Lifecycling the backups yourself gives you the most freedom to implement any desired retention logic.

The fact that ClickHouse Cloud does not lifecycle backups means that this responsibility falls entirely on you, the user. If backups are not deleted manually or programmatically, they will persist indefinitely, potentially leading to unnecessary storage costs and clutter. To address this, users are encouraged to automate backup deletion using tools like bucket TTL policies (which can automatically remove objects from cloud storage after a set period) or through custom scripts.
