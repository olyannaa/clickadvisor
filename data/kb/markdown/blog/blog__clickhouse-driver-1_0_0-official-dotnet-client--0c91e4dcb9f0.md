# ClickHouse.Driver 1\.0\.0: The Official .NET Client Hits Stable


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse.Driver 1\.0\.0: The Official .NET Client Hits Stable

![](/_next/image?url=%2Fuploads%2FImage_512x512_6_bb7e272a62.jpeg&w=96&q=75)Alex Soffronow PagonidisMar 2, 2026 · 7 minutes read
div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

We are proud to announce the release of ClickHouse.Driver 1\.0\.0, the first stable release of the official .NET client for ClickHouse. This has been a ground\-up effort: new API design, full type coverage, package signing, and OpenTelemetry integration, all built on top of the community project we adopted last year. Starting with 1\.0\.0, the public API is stable. The package follows semver, and we won't break your code between minor versions.


This release also comes bundled with a big [documentation](https://clickhouse.com/docs/integrations/csharp) upgrade and 40\+ [practical usage examples](https://github.com/ClickHouse/clickhouse-cs/tree/main/examples).


## **Road to 1\.0\.0** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#road_to_100)


The 1\.0\.0 release builds on two major pre\-releases:


**0\.8\.0** focused on packaging, configuration, and observability:


- Added support for .NET 10
- NuGet package signing and strong naming
- `ClickHouseClientSettings` for structured configuration
- Logging and diagnostics support via `ILoggerFactory`
- `EnableDebugMode` for low\-level network tracing
- Improved OpenTelemetry/ActivitySource integration


**0\.9\.0** focused on type support:


- Added support for BFloat16, Time/Time64, Geometry types (LineString, MultiLineString, Polygon)
- Reading Dynamic now supports all underlying types
- Improved JSON and FixedString support


## **The New ClickHouseClient API** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#the_new_clickhouseclient_api)


1\.0\.0 introduces `ClickHouseClient`, a new primary API that replaces the [ADO.NET](http://ADO.NET) classes for most use cases. It's thread\-safe, singleton\-friendly, and a lot less ceremony than `ClickHouseConnection`.



```
using var client = new ClickHouseClient("Host=localhost");

// DDL
await client.ExecuteNonQueryAsync("CREATE TABLE logs (ts DateTime, msg String) ENGINE = MergeTree ORDER BY ts");

// Binary bulk insert (replaces ClickHouseBulkCopy)
await client.InsertBinaryAsync("logs", ["ts", "msg"], rows); // rows: IEnumerable<object[]>

// Query
var parameters = new ClickHouseParameterCollection();
parameters.AddParameter("since", DateTime.UtcNow.AddDays(-7));
using var reader = await client.ExecuteReaderAsync("SELECT * FROM logs WHERE ts > {since:DateTime}", parameters);

// Scalar
var count = await client.ExecuteScalarAsync("SELECT count() FROM logs");

```

**Key methods:**




| Method | What it does |
| --- | --- |
| `ExecuteNonQueryAsync` | DDL/DML (CREATE, INSERT, ALTER, DROP) |
| `ExecuteScalarAsync` | Returns a single result |
| `ExecuteReaderAsync` | Stream results via `ClickHouseDataReader` |
| `InsertBinaryAsync` | High\-performance bulk insert |
| `ExecuteRawResultAsync` | Raw result stream in arbitrary format (e.g. save Parquet directly to a file) |
| `InsertRawStreamAsync` | Insert from stream (CSV, JSON, Parquet, etc.) |
| `PingAsync` | Check server connectivity |
| `CreateConnection()` | Get a `ClickHouseConnection` for ORM compatibility |


Per\-query settings (query ID, custom server settings, roles, bearer token) are passed via the new `QueryOptions` and `InsertOptions` classes. The [ADO.NET](http://ADO.NET) layer (`ClickHouseConnection` / `ClickHouseCommand`) remains fully supported for ORM integration with Dapper and linq2db.


**Note:** `ClickHouseBulkCopy` is now deprecated. Use `client.InsertBinaryAsync(table, columns, rows)` instead.


## **What Else is New in 1\.0\.0** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#what_else_is_new_in_100)


### **Automatic parameter type extraction from SQL** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#automatic_parameter_type_extraction_from_sql)


No more specifying the type twice. The driver now extracts parameter types directly from your SQL:



```
// Before: type specified in both the SQL and the parameter
command.CommandText = "SELECT {dt:DateTime('Europe/Amsterdam')}";
command.AddParameter("dt", "DateTime('Europe/Amsterdam')", value);

// After: type extracted from SQL automatically
command.CommandText = "SELECT {dt:DateTime('Europe/Amsterdam')}";
command.AddParameter("dt", value);

```

### **JWT authentication, roles, custom HTTP headers** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#jwt_authentication_roles_custom_http_headers)


JWT authentication, ClickHouse roles, and custom HTTP headers are now supported at the client level, with per\-query overrides via `QueryOptions`. Check out the examples on GitHub: [JWT example](https://github.com/ClickHouse/clickhouse-cs/blob/main/examples/Core/Auth_001_JwtAuthentication.cs), [roles example](https://github.com/ClickHouse/clickhouse-cs/blob/main/examples/Advanced/Advanced_006_Roles.cs), and [custom headers example](https://github.com/ClickHouse/clickhouse-cs/blob/main/examples/Advanced/Advanced_007_CustomHeaders.cs).


### **POCO serialization for JSON columns** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#poco_serialization_for_json_columns)


Write plain C\# objects directly to typed JSON columns. Properties are serialized using the column's type hints, with automatic inference for unhinted properties:



```
client.RegisterJsonSerializationType<UserEvent>();

await client.InsertBinaryAsync("events", ["data"], rows);

```

Control serialization using attributes: use `[ClickHouseJsonPath("custom.path")]` for custom paths and `[ClickHouseJsonIgnore]` to exclude properties. See the [JSON type example](https://github.com/ClickHouse/clickhouse-cs/blob/main/examples/DataTypes/DataTypes_005_JsonType.cs).


### **Mid\-stream exception detection** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#mid_stream_exception_detection)


ClickHouse 25\.11\+ can signal exceptions mid\-stream via the `X-ClickHouse-Exception-Tag` header. The driver now detects these and throws a proper `ClickHouseServerException` with the error message, instead of a generic `EndOfStreamException`.


### **QBit vector type** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#qbit_vector_type)


QBit stores vectors in a compact transposed binary format; quantization granularity is chosen at query time rather than at insert time, letting you trade precision for speed without re\-ingesting data. See the [QBit similarity search example](https://github.com/ClickHouse/clickhouse-cs/blob/main/examples/DataTypes/Vector_001_QBitSimilaritySearch.cs).


### **Query ID auto\-generation** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#query_id_auto_generation)


Every query now gets a unique ID automatically when one isn't explicitly set, making it easier to trace queries in server logs.


### **Additional improvements** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#additional_improvements)


- **Binary data in String/FixedString columns** — write `byte[]`, `ReadOnlyMemory<byte>`, or `Stream`; read back with the `ReadStringsAsByteArrays` setting.
- Full support for Dynamic type binary writing.
- **`AddParameter()` convenience method** on `ClickHouseParameterCollection`.


## **Breaking Changes** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#breaking_changes)


1\.0\.0 includes breaking changes to clean up the API surface. Here's a summary:


**Dropped .NET Framework / .NET Standard.** The library now targets `net6.0`, `net8.0`, `net9.0`, and `net10.0` only. If you're on .NET Framework, stay on the previous version or migrate to .NET 6\.0\+.


**DateTime behavior changed for columns without explicit timezone.** Columns like `DateTime` (without a timezone parameter) now return `DateTime` with `Kind=Unspecified`, preserving the stored wall\-clock time exactly. Writing also changed: `DateTime.Kind` is now respected. `Utc` and `Local` values maintain their instant, while `Unspecified` values are treated as wall\-clock time.


*Migration:* Use explicit timezones in column definitions (`DateTime('UTC')`) or apply timezones after reading.


**Removed `UseServerTimezone`.** No longer needed since timezone\-less columns return `Unspecified` values. `ServerTimezone` moved from `ClickHouseConnection` to `ClickHouseCommand` (extracted from response headers).


**JSON write mode default changed from Binary to String.** JSON data is now serialized via `System.Text.Json` and parsed server\-side. This removes the need for the client to parse JSON structure into binary column format before sending. The server handles parsing directly from the JSON string. Binary writing now only works with POCOs.


*Migration:* JSON string or JsonNode writing still works, but the JSON string will be parsed on the server instead of the client. This could lead to subtle changes in paths without type hints, e.g., values previously parsed as Int32 may be parsed as Int64\.


**Other changes:**


- Removed feature discovery query from `OpenAsync` (no more `SELECT version()` on connect)
- Several helper/extension methods made internal
- See the full [release notes](https://github.com/ClickHouse/clickhouse-cs/blob/main/RELEASENOTES.md) for details and migration guidance


## **Getting Started** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#getting_started)


Install via NuGet:



```
dotnet add package ClickHouse.Driver

```

Quick start:



```
using ClickHouse.Driver;

using var client = new ClickHouseClient("Host=localhost;Port=8123");

// Create a table
await client.ExecuteNonQueryAsync("""
    CREATE TABLE IF NOT EXISTS events (
        timestamp DateTime('UTC'),
        event_type String,
        payload JSON
    ) ENGINE = MergeTree ORDER BY timestamp
    """);

// Insert data
var rows = new List<object[]>
{
	    ([DateTime.UtcNow, "click", """{"page": "/home"}"""]),
	    ([DateTime.UtcNow, "view", """{"page": "/about"}"""]),
};
await client.InsertBinaryAsync("events", ["timestamp", "event_type", "payload"], rows);

// Query
using var reader = await client.ExecuteReaderAsync("SELECT * FROM events");
while (reader.Read())
{
    Console.WriteLine($"{reader.GetDateTime(0)} | {reader.GetString(1)} | {reader.GetString(2)}");
}

```

## **Links** [\#](/blog/clickhouse-driver-1_0_0-official-dotnet-client#links)


- **Documentation:** [clickhouse.com/docs/integrations/csharp](https://clickhouse.com/docs/integrations/csharp)
- **GitHub:** [github.com/ClickHouse/clickhouse\-cs](https://github.com/ClickHouse/clickhouse-cs)
- **Usage examples:** [github.com/ClickHouse/clickhouse\-cs/tree/main/examples](https://github.com/ClickHouse/clickhouse-cs/tree/main/examples)
- **.NET Demo App**: [https://github.com/ClickHouse/dotnet\-demo\-app](https://github.com/ClickHouse/dotnet-demo-app)
- **NuGet:** [nuget.org/packages/ClickHouse.Driver](https://www.nuget.org/packages/ClickHouse.Driver)


We'd love your feedback! [Open an issue](https://github.com/ClickHouse/clickhouse-cs/issues) or find us on [ClickHouse Community Slack](https://clickhouse.com/slack).

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-86-get-started-today-sign-up&utm_blogctaid=86)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
