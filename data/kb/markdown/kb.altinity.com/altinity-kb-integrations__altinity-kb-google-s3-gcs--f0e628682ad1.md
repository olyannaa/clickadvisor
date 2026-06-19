# Google S3 (GCS) \| Altinity® Knowledge Base for ClickHouse®


1. [Integrations](/altinity-kb-integrations/)
2. Google S3 (GCS)
# Google S3 (GCS)

GCS with the table function \- seems to work correctly for simple scenarios.

Essentially you can follow the steps from the [Migrating from Amazon S3 to Cloud Storage](https://cloud.google.com/storage/docs/aws-simple-migration)
.

1. Set up a GCS bucket.
2. This bucket must be set as part of the default project for the account. This configuration can be found in settings \-\> interoperability.
3. Generate a HMAC key for the account, can be done in settings \-\> interoperability, in the section for user account access keys.
4. In ClickHouse®, replace the S3 bucket endpoint with the GCS bucket endpoint This must be done with the path\-style GCS endpoint: `https://storage.googleapis.com/BUCKET_NAME/OBJECT_NAME`.
5. Replace the aws access key id and aws secret access key with the corresponding parts of the HMAC key.

Last modified 2025\.01\.16: [Streamlined page metadata, simplified directory structure (afe0f3c)](https://github.com/Altinity/altinityknowledgebase/commit/afe0f3c3e76e848e6941903e93f05dd41fccfea0)
