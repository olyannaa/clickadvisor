---
source: blog
url: https://github.com/ClickHouse/aspire-clickhouse-gateway-analytics-demo
topic: building-a-net-api-gateway-with-clickhouse-and-aspire
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 10
---

Layer [\#](/blog/dotnet-api-gateway-aspire#the-gateway-logging-layer) The core middleware pattern is straightforward: - Start a stopwatch - Call the next delegate - Normalize the route - Capture the current trace id - Emit gateway metrics - Enqueue a row for background ingestion

That last step is worth dwelling on. The proxied request must not wait on ClickHouse; if the database is slow or briefly unavailable, we want the gateway to keep serving traffic. So the middleware does not insert anything itself, it simply hands off the row to a bounded in\-memory queue:

```

```
1if (!requestLogQueue.TryEnqueue(logEntry))
2{
3    GatewayMetrics.LogDrops.Add(1, tags);
4}
```

```

The queue uses a bounded `System.Threading.Channels` channel with `FullMode = DropWrite`:

```

```
1Channel.CreateBounded(new BoundedChannelOptions(Capacity)
2{
3    FullMode = BoundedChannelFullMode.DropWrite,
4    SingleReader = true,
5    SingleWriter = false,
6});
```

```

`DropWrite` is the part that keeps the request path safe. If the queue fills up, `TryEnqueue` returns `false` immediately. The middleware increments a `gateway.log_drops` counter (tagged the same way as the rest of the gateway metrics) and moves on. The proxied request never waits on the database, and the dropped\-row counter becomes a first\-class signal you can alert on.

A background `IHostedService` drains the channel. Its loop is small: wait for one row, drain whatever else is immediately available into a capped batch, bulk\-insert, repeat:

```

```
1while (!stoppingToken.IsCancellationRequested)
2{
3    batch.Add(await queue.Reader.ReadAsync(stoppingToken));
4
5    while (batch.Count < MaxBatchSize && queue.Reader.TryRead(out var more))
6    {
7        batch.Add(more);
8    }
9
10    try
11    {
12        await client.InsertBinaryAsync("request_logs", batch, InsertOptions, stoppingToken);
13    }
14    catch (Exception ex)
15    {
16        logger.LogError(ex, "Failed to write {Count} request log rows to ClickHouse.", batch.Count);
17    }
18    finally
19    {
20        batch.Clear();
21    }
22}
```

```

Each `InsertBinaryAsync` call takes a list of POCOs and the driver streams them in ClickHouse's native `RowBinary` format. Values like `Guid`, `DateTime`, and `uint` round\-trip in their native binary representation with no string conversions.

The mapping from .NET property names to snake\_case column names is declared on the record itself:

```

```
1internal sealed record RequestLogRow(
2    [property: ClickHouseColumn(Name = "request_id")] Guid RequestId,
3    [property: ClickHouseColumn(Name = "trace_id")] string TraceId,
4    [property: ClickHouseColumn(Name = "timestamp")] DateTime Timestamp,
5    // ... remaining columns
6    [property: ClickHouseColumn(Name = "error_message")] string? ErrorMessage);
```

```
