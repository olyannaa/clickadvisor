# Unordered mode for GCS ClickPipes is now available


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Unordered mode for GCS ClickPipes is now available

![](/_next/image?url=%2Fuploads%2FMarta_Paes_Moreira_no_background_9853166ee2.png&w=96&q=75)[Marta Paes](/authors/marta-paes)Mar 16, 2026 · 7 minutes read
> *Ingest data from Google Cloud Storage into ClickHouse Cloud in **any** **order** for event\-driven, blazing\-fast analytics. Files are no longer required to follow lexicographical order.*


A few months ago, we removed one of the biggest usability wrinkles in S3 ClickPipes by [supporting ingesting files in any order](https://clickhouse.com/blog/clickpipes-s3-unordered-mode) (*aka* unordered mode). We’re now extending that functionality to the Google Cloud Storage (GCS) connector, with a little help from [Google Cloud Pub/Sub notifications for Cloud Storage](https://docs.cloud.google.com/storage/docs/pubsub-notifications).


![gcs-unordered-mode.png](/uploads/gcs_unordered_mode_fd4559c5df.png)
This means that you no longer need to worry about ensuring files land in your bucket in lexicographical order: with unordered mode, we’ll simply listen to notifications for new files and ingest files as they land in the GCS bucket. Whether you’re dealing with backfills, retries, late\-arriving data, or some other source of out\-of\-orderness — this is now covered.

### Get started today

Sign up for ClickHouse Cloud today to try out the GCS connector for ClickPipes![Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-103-get-started-today-sign-up&utm_blogctaid=103)## Why is this a big deal? [\#](/blog/clickpipes-gcs-unordered-mode#why-is-this-a-big-deal)


By default, the GCS ClickPipe assumes files are added to a bucket in lexicographical order, and relies on this implicit order to ingest files sequentially. This means that any new file *must* be lexically greater than the last ingested file, which isn’t always true in the real world. For example, files named `events_2024-12-01.parquet`, `events_2024-12-02.parquet`, and `events_2024-12-03.parquet` will be ingested in order, but if a backfill named `events_2024-11-30.parquet` lands later in the bucket, it will be ignored.


Not cool.


With unordered mode, this limitation no longer applies: instead of polling the bucket every 30 seconds looking for the next file to process, the ClickPipe waits for new file notifications. When a notification arrives, ClickPipes just goes and processes that file regardless of its relative order to previously processed files. Although this requires a little extra configuration, it's a more robust and scalable approach when you’re dealing with millions of objects.


## How does it work? [\#](/blog/clickpipes-gcs-unordered-mode#how-does-it-work)


To configure a GCS ClickPipe to ingest files that don’t have an implicit order, you need to configure notifications from the bucket to a Pub/Sub topic. ClickPipes can then listen for `OBJECT_FINALIZE` events and ingest any new files regardless of the file naming convention.


![564927906-277a62f5-799d-4d30-951d-35ebc8b346f2.jpg](/uploads/564927906_277a62f5_799d_4d30_951d_35ebc8b346f2_56abffa4ed.jpg)
***Unordered mode:** Files land in GCS in **any order** (A) and trigger Pub/Sub notifications (B\-C). ClickPipes polls and processes files in the specified path, using a metadata store to track state (1\-5\). Data is inserted into the target tables with exactly\-once guarantees (6\).*


***“What about failures?”*** Since the steps above span multiple systems and don’t happen in a single transaction, failures can occur at any step — reading from GCS, marking files as processed, inserting data into ClickHouse, and so on. If a failure occurs, ClickPipes automatically reprocesses the batch. ***"But what about duplicates?”*** Even if files are reprocessed multiple times, the GCS ClickPipe guarantees exactly\-once semantics, so no duplicates make it into your target table.


Let’s see it in action!


### Create a Pub/Sub topic [\#](/blog/clickpipes-gcs-unordered-mode#create-a-pubsub-topic)


*The following instructions assume you already have a GCS bucket with some data in it, as well as enough permissions to manage IAM roles and create new resources in your Google Cloud account.*


**1\.** In the Google Cloud Console, navigate to **Pub/Sub \> Topics \> Create topic**. Create a new topic with a default subscription and note the **Topic Name**.


**2\.** Configure a [service account](http://docs.cloud.google.com/iam/docs/keys-create-delete) with the minimum required set of permissions to allow ClickPipes to list and fetch objects in the specified bucket, as well as consume and monitor notifications from the Pub/Sub subscription.


![](/uploads/gcs_unordered_mar2026_image1_5969bf8711.png)
**3\.** Configure your GCS bucket to send notifications to Pub/Sub when a new object lands in the bucket. This step cannot be performed in the Google Cloud Console, so you must use `gcloud` or your preferred programmatic interface.


**3\.1\.** Using `gcloud`, add a notification configuration to your GCS bucket that triggers notifications for the `OBJECT_FINALIZE` [event type](https://docs.cloud.google.com/storage/docs/pubsub-notifications#events):



```

# Create a Pub/Sub notification for new objects in the bucket
gcloud storage buckets notifications create "gs://${YOUR_BUCKET_NAME}" \
--topic="projects/${YOUR_PROJECT_ID}/topics/${YOUR_TOPIC_NAME}" \
--event-types="OBJECT_FINALIZE" \
--payload-format="json"

# List the Pub/Sub notifications in the bucket
gcloud storage buckets notifications describe

```

We strongly recommend configuring a [**Dead\-Letter topic**](https://docs.cloud.google.com/pubsub/docs/dead-letter-topics), too, so it's easier to debug and retry failed notifications. But that’s it — you’re ready to create a ClickPipe to continuously ingest data from your bucket whenever a new file lands!


### Create a ClickPipe [\#](/blog/clickpipes-gcs-unordered-mode#create-a-clickpipe)


**1\.** In the ClickHouse Cloud console, navigate to **Data Sources \> Create ClickPipe**, then choose **Google Cloud Storage**. Enter the details to connect to your GCS bucket, using **Service account** as the authentication method and providing the `.json` service account key.


**2\.** Toggle on **Continuous ingestion**, then select the new **Any order** ingestion mode to enable unordered mode. Enter the path to your Pub/Sub subscription.


![](/uploads/gcs_unordered_mar2026_image5_01fc577707.png)
**3\.** Click **Incoming data**. Define a **Sorting key** for the target table (very important) and make any necessary adjustments to the mapped schema. Finally, configure a role for the ClickPipes database user.


![cp-gcs-unordered.gif](/uploads/cp_gcs_unordered_26a91e8d0f.gif)
**4\.** **Sit back and relax.** ClickPipes will now perform an initial scan of your bucket, then start processing files as new notification events arrive. 🚀


If that seems like a lot of clicking, the good news is that ClickPipes is fully supported in the [ClickHouse Terraform provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest/docs), so you can configure this setup as code from start to finish.


## What’s next? [\#](/blog/clickpipes-gcs-unordered-mode#whats-next)


We’re excited to enable more complex ingestion patterns from object storage into ClickHouse Cloud with the new unordered mode in GCS ClickPipes — you get the same fully\-managed, full\-speed experience with a little extra flexibility! This feature is also available for Amazon S3 as a data source. We plan to extend support to Azure Blob Storage in the near future, to ensure feature parity across **all** Object Storage ClickPipes.


If you have any feedback or run into any snags while setting up ClickPipes, reach out to our team! For step\-by\-step instructions, frequently asked questions, and gotchas, check out the [documentation for GCS ClickPipes](https://clickhouse.com/docs/integrations/clickpipes/object-storage/gcs/get-started).


*Ready to eliminate your ETL complexity and reduce your data movement costs? [Try the GCS ClickPipe connector today](https://clickhouse.com/cloud/clickpipes) and experience a fully managed, native integration experience with ClickHouse Cloud — the world’s fastest analytics database.*

### Ready to eliminate your ETL complexity and reduce your data movement costs?

Try the GCS ClickPipe connector today and experience a fully managed, native integration experience with ClickHouse Cloud — the world’s fastest analytics database.[Try the GCS ClickPipe connector today](https://clickhouse.com/cloud/clickpipes?loc=blog-cta-102-ready-to-eliminate-your-etl-complexity-and-reduce-your-data-movement-costs-try-the-gcs-clickpipe-connector-today&utm_blogctaid=102)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
