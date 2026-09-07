---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Adding
topic: adding-analytics-to-an-application-in-under-10-minutes-with-clickhouse-cloud-query-endpoints-clickhouse
ch_version_introduced: '0.018'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 10
---

into an endpoint, we simply need to click `Share -> API Endpoint`, saving the query with a name and creating an API token to use with "Query Endpoints" permissions. Ensure the endpoint is uses a read\-only only: [![](/_next/image?url=%2Fuploads%2Fcreate_api_endpoint_0d3994f6fc.gif&w=2048&q=75)](https://cms.clickhouse-dev.com:1337/uploads/create_api_endpoint_0d3994f6fc.gif)

> Note how we associate the "Play role" with the endpoint. This is a role that ensures this endpoint can only be used to respond to queries on the required tables, as well as imposing quotas that are [keyed off IP addresses](https://clickhouse.com/docs/en/operations/quotas), thus limiting the number of requests a single user can make. For users wishing to invoke endpoints from browsers, CORS headers can also be configured with a list of allowed domains. A default "Read only" role provides a simpler getting started.

This provides us with a HTTP endpoint we can now execute using curl, with the response returned in JSON:

```
1curl -H "Content-Type: application/json" -X 'POST' -s --user '<key_id>:<key_secret>' 'https://console-api.clickhouse.cloud/.api/query-endpoints/9001b12a-88d0-4b14-acc3-37cc28d7e5f4/run?format=JSONEachRow' --data-raw '{"queryVariables":{"project_name":"boto3","min_date":"2011-01-01","max_date":"2024-06-06"}}'
2
3{"stars":"47739","issues":"3009","forks":"11550","prs":"1657"}
```
Copy command
An astute reader might notice we pass the url parameter `"format":"JSONEachRow"` to control the output format. Users can specify any of the over [70 output formats](https://clickhouse.com/docs/en/interfaces/formats#jsoneachrow) supported by ClickHouse here. For example, for `CSVWithNames`:

```
1curl -H "Content-Type: application/json" -X 'POST' -s --user '<key_id>:<key_secret>' 'https://console-api.clickhouse.cloud/.api/query-endpoints/9001b12a-88d0-4b14-acc3-37cc28d7e5f4/run?format=CSVWithNames' --data-raw '{"queryVariables":{"project_name":"boto3","min_date":"2011-01-01","max_date":"2024-06-06"}}'
2
3"stars","issues","forks","prs"
447739,3009,11550,1657
```
Copy command
## Putting it together \#

The above leaves us with just needing to build our visuals and integrate the API endpoint above.

The React code for components is pretty simple with the most relevant snippets below. More curious readers can find the code [here](https://github.com/ClickHouse/clickpy/blob/main/src/components/GithubStats.jsx).
