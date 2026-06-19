# 5 ways to parse Dates and DateTimes in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# 5 ways to parse Dates and DateTimes in ClickHouse

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Mar 12, 2026 · 6 minutes readDates come in all shapes and sizes \- Unix timestamps from event streams, weird looking numeric dates from legacy database exports, ISO 8601 strings from APIs, and more. Lucky for us, ClickHouse has a rich set of functions to handle all of them and that's what we're going to explore in this blog post.


We'll start with the most explicit approaches: converting Unix timestamps with `fromUnixTimestamp`, parsing packed numeric dates with `YYYYMMDDToDate`, and parsing known format strings with `parseDateTime`. Then we'll look at the `parseDateTimeBestEffort` family for when the format is unknown or mixed.


Finally, we'll cover how casting dates with the `cast_string_to_date_time_mode` setting might be a better choice than explicit function calls for some use cases.



## Unix timestamps [\#](/blog/parsing-dates-datetimes#unix_timestamps)


First up, Unix timestamps! Unix timestamps represent the number of seconds since January 1st, 1970\. We can use the [`fromUnixTimestamp`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#fromUnixTimestamp) function to convert them:



```

```
1SELECT
2    fromUnixTimestamp(1704067295) AS val1, toTypeName(val1);
```

```

This returns a `DateTime` type. If you have milliseconds since January 1st, 1970, there's a different function — [`fromUnixTimestamp64Milli`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#fromUnixTimestamp64Milli) — and the type comes back as `DateTime64(3)`, where the `3` means precision up to milliseconds.



```

```
1SELECT
2    fromUnixTimestamp64Milli(1704067295123) AS val2, toTypeName(val2);
```

```

For microseconds, [`fromUnixTimestamp64Micro`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#fromUnixTimestamp64Micro) returns `DateTime64(6)`:



```

```
1SELECT
2    fromUnixTimestamp64Micro(1704067295123456) AS val3, toTypeName(val3);
```

```

## Numeric date formats [\#](/blog/parsing-dates-datetimes#numeric_date_formats)


Sometimes dates are represented as plain numbers encoding the year, month, and day — with no separators or formatting. This is common in legacy database exports or flat files from mainframes. The function [`YYYYMMDDToDate`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#YYYYMMDDToDate) handles this:



```

```
1SELECT
2    YYYYMMDDToDate(20240115) AS val1, toTypeName(val1);
```

```

If the number also includes time information, [`YYYYMMDDhhmmssToDateTime`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions#YYYYMMDDhhmmssToDateTime) handles that too:



```

```
1SELECT
2    YYYYMMDDhhmmssToDateTime(20240115143022) AS val2, toTypeName(val2);
```

```

## Known format strings [\#](/blog/parsing-dates-datetimes#known_format_strings)


APIs often return dates as strings. If you know the format, you can use [`parseDateTime`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTime) with a MySQL date format string:



```

```
1SELECT
2    parseDateTime('15/01/2024 14:30:22', '%d/%m/%Y %H:%i:%s') AS val1,
3    toTypeName(val1);
```

```

This returns a `DateTime` including the timezone.


If you prefer Joda date format strings, there's [`parseDateTimeInJodaSyntax`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTimeInJodaSyntax) which produces the same output:



```

```
1SELECT
2    parseDateTimeInJodaSyntax('15/01/2024 14:30:22', 'dd/MM/yyyy HH:mm:ss') AS val2,
3    toTypeName(val2);
```

```

## Best effort parsing of DateTimes [\#](/blog/parsing-dates-datetimes#best_effort_parsing)


The previous three approaches all assumed we knew the exact date format. But what if we don't? That's where the [`parseDateTimeBestEffort`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTimeBestEffort) family of functions comes in. Imagine we have dates in a mix of different formats:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7)
8SELECT raw, parseDateTimeBestEffort(raw) AS val, toTypeName(val)
9FROM dates;
```

```

We can also convert to `DateTime64` using [`parseDateTimeBestEffort64`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTime64BestEffort), like the earlier functions:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7)
8SELECT raw, parseDateTime64BestEffort(raw) AS val, toTypeName(val)
9FROM dates;
```

```

What happens if we include a completely invalid date?



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7    UNION ALL
8    SELECT 'not a date' AS raw
9)
10SELECT raw, parseDateTime64BestEffort(raw) AS val, toTypeName(val)
11FROM dates;
```

```

ClickHouse throws an exception!


We can work around this with the [`parseDateTimeBestEffort64OrNull`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTime64BestEffortOrNull) variant, which returns `NULL` instead:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7    UNION ALL
8    SELECT 'not a date' AS raw
9)
10SELECT raw, parseDateTime64BestEffortOrNull(raw) AS val, toTypeName(val)
11FROM dates;
```

```

Or if you'd rather get an actual datetime value, [`parseDateTimeBestEffort64OrZero`](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions#parseDateTime64BestEffortOrZero) falls back to January 1st, 1970 at midnight:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7    UNION ALL
8    SELECT 'not a date' AS raw
9)
10SELECT raw, parseDateTime64BestEffortOrZero(raw) AS val, toTypeName(val)
11FROM dates;
```

```

## Casting [\#](/blog/parsing-dates-datetimes#casting)


If you'd rather avoid calling explicit parse functions throughout your queries, you can cast string values directly to date types using `::DateTime`. However, there's an important setting to be aware of: `cast_string_to_date_time_mode`.


By default it's set to `basic`, which handles standard formats like `YYYY-MM-DD` and `YYYY-MM-DD HH:MM:SS`, but anything else will fail. For broader format support, change it to `best_effort`. Note that this setting still throws an exception for completely invalid dates.


You can pass the setting inline per query:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7)
8SELECT raw, raw::DateTime AS val, toTypeName(val)
9FROM dates
10SETTINGS cast_string_to_date_time_mode = 'best_effort';
```

```

Or configure it at the session level so you don't need it in every query:



```

```
1SET cast_string_to_date_time_mode = 'best_effort';
```

```

Then the same query works without the `SETTINGS` clause:



```

```
1WITH dates AS (
2    SELECT '2024-01-15T14:30:22.000Z' AS raw
3    UNION ALL
4    SELECT '2024-01-15' AS raw
5    UNION ALL
6    SELECT '1704067295' AS raw
7)
8SELECT raw, raw::DateTime AS val, toTypeName(val)
9FROM dates;
```

```

Finally, imagine that we have the following file that contains a variety of dates:


*dates.csv*



```
raw
2024-01-15T14:30:22.000Z
2024-01-15
1704067295

```

We can parse the dates in that file using the same approach:



```

```
1SELECT raw, raw::DateTime AS val, toTypeName(val)
2FROM file('dates.csv', CSVWithNames);
```

```


```
┌─raw──────────────────────┬─────────────────val─┬─toTypeName(val)─┐
│ 2024-01-15T14:30:22.000Z │ 2024-01-15 14:30:22 │ DateTime        │
│ 2024-01-15               │ 2024-01-15 00:00:00 │ DateTime        │
│ 1704067295               │ 2024-01-01 00:01:35 │ DateTime        │
└──────────────────────────┴─────────────────────┴─────────────────┘

```
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-100-get-started-today-sign-up&utm_blogctaid=100)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
