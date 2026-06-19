---
source: blog
url: https://github.com/ClickHouse/clickhouse-serilog-demo/tree/main
topic: structured-logging-in-net-with-serilog-and-clickhouse
ch_version_introduced: '599.99'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 16
---

stock alert: product 3 (USB-C Hub) has only 3 units remaining [14:23:01 ERR] Order failed — product 4 (Monitor Stand) is out of stock [14:23:02 ERR] Chaos endpoint triggered — TimeoutException ``` ### Structured logging in action [\#](/blog/serilog#structured-logging-in-action)

The key difference between structured and traditional logging is that structured logs preserve data as typed, named fields rather than flattening everything into a string. Numbers stay numbers, dates stay dates, and each property is individually queryable. This makes logs into a queryable dataset and lets a columnar database like ClickHouse store and compress them efficiently.

Here's how the order service logs a successful order:

```
_logger.LogInformation(
    "Order {OrderId} placed by {UserId}: {Quantity}x {ProductName} for {TotalPrice:C}",
    orderId, request.UserId, request.Quantity, product.Name, product.Price * request.Quantity);

```

This produces a log event with named, typed properties, not just a flat string. In ClickHouse, you can then query:

```

```
1SELECT * FROM logs.app_logs
2WHERE properties.UserId = 'user-42'
3ORDER BY timestamp DESC;
```

```

## Exploring your logs [\#](/blog/serilog#exploring-your-logs)

Since your logs are standard ClickHouse tables, you can query them with any SQL client. The fastest way to start is ClickHouse's built\-in Play UI at <http://localhost:8123/play> or the ClickStack interface at <http://localhost:8080>.

In the ClickStack UI, you can see both the rendered log message and the underlying structured properties.

![](/uploads/serilog_2_d1b1d9e189.png)
![](/uploads/serilog_3_8db0641bf2.png)
Our ClickStack instance is pre\-configured with a data source pointing at our `logs.app_logs` table and a pre\-built dashboard that lights up as soon as the demo generates traffic.

![](/uploads/serilog_4_4fa0e50c00.png)
The dashboard includes five tiles that demonstrate what you get out of the box with structured log data in ClickHouse:
