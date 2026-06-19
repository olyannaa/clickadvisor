---
source: blog
url: https://clickpy.clickhouse.com/
topic: building-single-page-applications-with-clickhouse
ch_version_introduced: '1.1'
last_updated: '2026-06-12'
chunk_index: 13
total_chunks_in_doc: 15
---

is as responsive as possible. We employ this technique in our [popular ClickPy demo](https://clickpy.clickhouse.com/), which allows users to perform analytics on Python packages. Example views and details on the implementation can be found [here](https://github.com/ClickHouse/Clickpy?tab=readme-ov-file#a-real-example). ### Exploiting compression [\#](/blog/building-single-page-applications-with-clickhouse-and-http#exploiting-compression)

ClickHouse's HTTP endpoint supports both request and response compression. For the text\-based formats described above, we recommend using HTTP response compression. Since read requests are typically small, users typically only need response compression when developing client\-only applications. We recommend only enabling compression when streaming large responses where the network is the bottleneck. Compression may slow response times with a CPU overhead incurred on the server. As always, test and measure.

Provided `enable_http_compression=1` is set for the user (or set in the request), the desired compression method should be specified in the header `Accept-Encoding: compression_method`, with a [number of options supported](https://clickhouse.com/docs/en/interfaces/http#compression).

```
const client = createClient( {
    url: 'https://clickpy-clickhouse.clickhouse.com',
    username: 'play',
     compression: {
       response: true
   }
  }
);

```

If compression is required, we recommend the ClickHouse JS web client, which supports [response compression with gzip](https://clickhouse.com/docs/en/integrations/javascript#compression), as shown above, and automatically sets the required header and settings.

### Predefined HTTP Interfaces [\#](/blog/building-single-page-applications-with-clickhouse-and-http#predefined-http-interfaces)

Open\-source users can abstract SQL away from the client using pre\-defined HTTP interfaces. This feature allows ClickHouse to expose an endpoint to which parameters are provided. These are, in turn, injected into a predefined SQL query, with the response returned to the user. For simple business applications, this can simplify the client code which just communicates with a limited REST API. The same principles described above can be applied to the invoking user to enforce access restrictions and quotas.

### Query Endpoints for ClickHouse Cloud [\#](/blog/building-single-page-applications-with-clickhouse-and-http#query-endpoints-for-clickhouse-cloud)

Pre\-defined HTTP interfaces have their limitations, not least implementing changes or adding endpoints requires modifying the clickhouse.xml configuration.

> Some users may also not feel comfortable exposing their ClickHouse HTTP interface. Query Endpoints help address these concerns by limiting the queries that can be executed, thus reducing the attack surface.
