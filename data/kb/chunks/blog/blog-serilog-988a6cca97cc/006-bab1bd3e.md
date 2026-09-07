---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Structured
topic: structured-logging-in-net-with-serilog-and-clickhouse-clickhouse
ch_version_introduced: '599.99'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 16
---

request summary event too. ### One event per request \# `UseSerilogRequestLogging()` replaces ASP.NET's verbose per\-middleware logging with a single summary event per request that includes the HTTP method, path, status code, and elapsed time. Cleaner and more efficient.

You can enrich this completion event with additional properties: globally via `EnrichDiagnosticContext` and per\-endpoint via `IDiagnosticContext`. Our demo does both. In the middleware configuration, you can add variables from the `HttpContext`, such as the user agent string:

```
1app.UseSerilogRequestLogging(options =>
2{
3    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
4    {
5        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value ?? "unknown");
6        diagnosticContext.Set("UserAgent", httpContext.Request.Headers.UserAgent.ToString());
7    };
8});
```
Copy command
Then in individual endpoints, you can attach properties specific to that endpoint which will appear on the same completion event:

```
1app.MapPost("/orders", (OrderRequest request, OrderService orders,
2    IDiagnosticContext diagnosticContext) =>
3{
4    diagnosticContext.Set("UserId", request.UserId);
5    diagnosticContext.Set("ProductId", request.ProductId);
6    // ...
7});
```
Copy command
### Health check \#

The `/health` endpoint uses ASP.NET Core's built\-in health check framework to verify ClickHouse connectivity. We use a simple `IHealthCheck` that opens a connection and runs `SELECT 1` (see [`ClickHouseHealthCheck.cs`](https://github.com/ClickHouse/clickhouse-serilog-demo/blob/main/src/DemoApi/Health/ClickHouseHealthCheck.cs)).

### Graceful shutdown \#

Because the sink batches events in memory, you must call `Log.CloseAndFlush()` (or its async counterpart) before the process exits, otherwise the last partial batch is lost. Our demo wraps `app.Run()` in a try/finally:

```
1try
2{
3    app.Run();
4}
5finally
6{
7    await Log.CloseAndFlushAsync();
8}
```
Copy command
This ensures the final in\-memory batch is flushed during normal shutdown.

## Running the demo \#

Start the stack:

```
1docker compose up -d
```
Copy command
After \~15 seconds, the demo API is available at <http://localhost:5000>, the ClickHouse Play UI at <http://localhost:8123/play>, and a dashboard UI at <http://localhost:8080>.

![](/_next/image?url=%2Fuploads%2Fserilog_1_68263c7434.png&w=2048&q=75)

The API includes a built\-in traffic generator that exercises every endpoint:

```
1curl -X POST http://localhost:5000/generate-traffic
```
Copy command
You'll see structured log output in the console:
