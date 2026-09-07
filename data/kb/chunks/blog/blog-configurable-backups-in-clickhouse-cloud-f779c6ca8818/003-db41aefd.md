---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Configurable
topic: configurable-backups-in-clickhouse-cloud-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 4
---

as every 24 hours, with several intermediate values supported within that range. Retention ranges from 1 day and goes up to 30 days, which refers to the ability to roll back to a certain point in time. ![2conf.png](/_next/image?url=%2Fuploads%2F2conf_d03c87f980.png&w=2048&q=75)

**NOTE:** Frequency and start time (Scheduled) are mutually exclusive settings for backups. For example, if you select 2 AM UTC as the start time for your backups, you won’t be able to simultaneously set a frequency of backing up the data every 6 hours.

**Available backups, usage, and cost**

All available backups for your service are displayed on the backups page in the Cloud Console. In the example below, backups have been configured to happen every 6 hours, with a 5\-day retention. From here (under Actions) you can also select a particular backup and choose to restore it to a new service. Details of restoring a backup to a service are covered in our [public docs](https://clickhouse.com/docs/en/manage/backups).

![3conf.png](/_next/image?url=%2Fuploads%2F3conf_4cd7309f93.png&w=2048&q=75)

To understand the cost impact of your backup configuration, you can look at the usage breakdown for your service under the “Organization” section on the Cloud Console. If there are costs associated with the backup configuration you’ve selected, they will be displayed on this page under the column “Backups.”

![unnamed.png](/_next/image?url=%2Fuploads%2Funnamed_a38262a70a.png&w=2048&q=75)

## Looking ahead \#

We plan to make ClickHouse Cloud backups even more seamless and flexible. We will soon enable on\-demand backups, so you can kick off a backup at any point in time from the UI, or programmatically via APIs.

We will also soon support the ability to export backups cross\-region. This gives you the ability to fulfill your DR (disaster recovery) requirements in situations where the primary region has an interruption in service. 

Additionally, we are looking to enable the capability to export backups to your own cloud service account. This will allow for more control over the backup lifecycle, as well as data retention for data residency or other compliance purposes.

Finally, in the coming months, we also plan to improve our backup capability to support continuous backups and point\-in\-time restores (PITR). This will make it possible to have even more granular [RPO](https://www.druva.com/glossary/what-is-a-recovery-point-objective-definition-and-related-faqs) for data stored in ClickHouse Cloud.
