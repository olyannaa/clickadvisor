---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Training
topic: training-machine-learning-models-with-clickhouse-clickhouse
ch_version_introduced: '23.3'
last_updated: '2026-09-07'
chunk_index: 19
total_chunks_in_doc: 20
---

variants to version data sources, transformations, features, labels, and training sets. Each of these resources is immutable by default, ensuring you can confidently utilize versioned resources created by others without the risk of disruption due to upstream modifications.

For each resource, a variant parameter exists that can be configured either manually or automatically. Recognizing that later variants of features are not necessarily improvements over previous ones (Machine Learning isn't a linear journey of improvement, unfortunately), the term "[variant" is preferred over "version"](https://docs.featureform.com/concepts/versioning-and-variants#setting-all-variants-in-a-run). In our examples, we've simply relied on automatic versioning. If we changed any resource in our flow (e.g., change the features used for our entity), this would create a new variant of the resource and trigger the recreation of all dependency resources. This tracking of [lineage requires Directed Acyclic Graphs (DAG)](https://docs.featureform.com/concepts/immutability-lineage-and-dags) and employs techniques similar to tools such as dbt that users may be familiar with.

## Conclusion \#

In this post, we've explored how ClickHouse can be used as a feature store to train machine learning models using Featureform. In this role, ClickHouse acts as both a transformation engine and an offline store. We have transformed and scaled a fraud dataset using only SQL and used the subsequent data to incrementally train both Logistic regression and Decision tree\-based models to predict whether transactions are fraudulent or not. In the process, we have commented on how using an SQL database with feature stores allows a collaborative approach to feature engineering, improving the usability of features, which in turn reduces model iteration time. In future posts, we will explore how we can take this model to production and integrate with tooling such as AWS Sagemaker for model training.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

---

Share this post

- Copy URL
- [![Y Combinator icon](/_next/static/immutable/media/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/_next/static/immutable/media/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/_next/static/immutable/media/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/_next/static/immutable/media/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/_next/static/immutable/media/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")
### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts
