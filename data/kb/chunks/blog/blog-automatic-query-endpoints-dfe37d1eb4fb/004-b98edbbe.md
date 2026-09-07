---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Automatic
topic: automatic-query-endpoints-creating-apis-from-sql-queries-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 5
---

prompted to specify which API key(s) should be able to access the endpoint: ![03_share_query.png](/_next/image?url=%2Fuploads%2F03_share_query_f13e8e3e2f.png&w=2048&q=75) After selecting an API key, we’ll be good to go! An example `curl` command demonstrates how we can build requests to the endpoint: ![04_api_endpoint.png](/_next/image?url=%2Fuploads%2F04_api_endpoint_b6a4230117.png&w=2048&q=75)

Now, we can try to curl the endpoint:

![endpoints-curltest.png](/_next/image?url=%2Fuploads%2Fendpoints_curltest_11cc268ccb.png&w=2048&q=75)

Now that we’ve verified that the endpoint works let’s go back to the SQL console. A new button should appear immediately to the right of the ‘share’ button. Clicking it will open a flyout containing monitoring data about the query:

![06_insights.png](/_next/image?url=%2Fuploads%2F06_insights_30915a022a.png&w=2048&q=75)

### How we built it \#

To release an initial version of this feature as quickly as possible, we built upon existing functionality in our Cloud Console:

- Saved Queries
- Query parameterization
- Passwordless DB Authentication using certificates
- Server\-side query execution
- Existing Cloud API keys as the endpoint authentication method

In other words, the foundational elements necessary for building query API Endpoints have already been battle\-tested in production for months to years. Implementation primarily required stringing these components together in a new way and extending our SQL console saved queries UI to give users an easy and seamless way to configure and monitor their endpoints.

### What we’re building next \#

While OpenAPI keys are functional, they are still in Beta—primarily because the current functionality does not provide an optimal solution for direct endpoint calls from a user interface within a webpage. To enhance this user experience, we plan to introduce authentication/authorization via JWT (your own JWT). This will allow these API endpoints to be the building blocks for any developer to construct an analytics application backend.

A frontend developer would only require two key skills to build their next analytics application: the ability to create a query in ClickHouse (with assistance from our copilot/Gen AI if needed) and proficiency in their preferred web framework.

We also plan to add support for a streaming API, letting you pull all your data via API endpoints without memory constraints.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

---

Share this post
