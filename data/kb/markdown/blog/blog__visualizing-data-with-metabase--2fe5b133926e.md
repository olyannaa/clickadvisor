# Visualizing Data with ClickHouse \- Part 3 \- Metabase


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Visualizing Data with ClickHouse \- Part 3 \- Metabase

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Oct 19, 2022 · 10 minutes read![metabase-clickhouse.png](/uploads/metabase_clickhouse_095d5b286e.png)
This blog post is part of a series:


- [Visualizing Data with ClickHouse \- Part 1 \- Grafana](https://clickhouse.com/blog/visualizing-data-with-grafana)
- [Visualizing Data with ClickHouse \- Part 2 \- Superset](https://clickhouse.com/blog/visualizing-data-with-superset)


## Introduction [\#](/blog/visualizing-data-with-metabase#introduction)


In this post, we continue our series on the visualization of data in Clickhouse[\[1]](https://clickhouse.com/blog/visualizing-data-with-grafana)[\[2]](https://clickhouse.com/blog/visualizing-data-with-superset) by exploring Metabase as a popular tool for less technical business users.


## Metabase [\#](/blog/visualizing-data-with-metabase#metabase)


Metabase offers a simpler experience for those less comfortable with writing SQL. Queries can be constructed by simply dragging and dropping fields \- a feature likely to appeal to business users. Focusing on fast data exploration, the breadth of visuals and customizability is less than previous tools we’ve demonstrated, with the benefit of a cleaner and simpler interface and workflow.


Downloading the Metabase jar offers the simplest getting\-started experience. This requires you to have a Java Runtime Environment (JRE) installed on your system. Ensure you download the [ClickHouse driver](https://github.com/enqueue/metabase-clickhouse-driver/releases) (jar file), placing this in a “/plugins” subdirectory. Starting Metabase is then trivial:



```
java -jar metabase.jar

```

The app can take a few minutes to start. The console should redirect you to [http://localhost](http://localhost:3000) once Metabase is ready.


Select ClickHouse as your database during setup and assign a name to the data source. Note the usage of the HTTP port.


[![metabase-1-datasource-v2.gif](/uploads/metabase_1_datasource_v2_3cc6f654ae.gif)](/uploads/metabase_1_datasource_v2_3cc6f654ae.gif)
  

Metabase offers an exploration feature useful for obtaining a quick overview of a particular dataset. The overview statistics such as field cardinality and value changes over time. Below we explore the forex dataset, from an [earlier post](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3), to obtain an overview of the main base and quote columns.


[![metabase-explore.gif](/uploads/metabase_explore_1b683eb74e.gif)](/uploads/metabase_explore_1b683eb74e.gif)
  

Users of Metabase create analytics that can be based on either traditional SQL queries or a “question”. Questions are built with a guided query builder where the user selects a database, table, filter, and summarization field. The summarization can also be split into groups \- effectively using a GROUP BY. This intuitive approach allows users to build simple visualizations quickly.
Below we use the question feature to view the average price for the EUR currency pairs USD, AUD, CAD, CHF, GPB, and NZD from our [forex dataset](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3). Note we assume the bid price represents the average price of the currency pair.


[![metabase-2-simple-viz-v2.gif](/uploads/metabase_2_simple_viz_v2_0f1b8f08a4.gif)](/uploads/metabase_2_simple_viz_v2_0f1b8f08a4.gif)
  

This “question” approach is particularly suited to most simple visualization requirements. For more complex visualizations, Metabase offers a SQL editor. The user simply has to ensure results are returned in a structure appropriate to visualize \- similar to the Grafana approach. With no client\-side transformation logic, all manipulation is deferred to the query itself. With an extensive range of analytical functions, this suits ClickHouse and is typically encouraged even for the largest datasets.
Below we demonstrate using this SQL editor to show the world’s coldest countries, according to our [NOAA dataset](https://clickhouse.com/blog/real-world-data-noaa-climate-data), overlaid on a regional map.


[![metabase-3-country-map.gif](/uploads/metabase_3_country_map_6ad50aa039.gif)](/uploads/metabase_3_country_map_6ad50aa039.gif)
  


```

SELECT
    code,
    min(tempMin) / 10 AS min_temp
FROM blogs.noaa
WHERE date > '1970-01-01'
GROUP BY substring(station_id, 1, 2) AS code
LIMIT 1000
 [✎](https://sql.clickhouse.com?query_id=HNQECUKC2F4GGRKHXWRTGS)

```


As well as region maps, Metabase includes a Grid map. While currently quite simple, this can be useful for plotting points where the color intensity is determined by a metric. We use this capability to plot weather events in the United States where the wind gust speed was greater than 100 kph or approx. 30 MPS (our units of wind gust speed are tenths of meters per second), and significant volumes of rain were involved over the period of a week, i.e., more than 2cm of rain on average per day. We restrict this to the period of July to October, which loosely describes the conditions and time of year for hurricanes. We finally plot the top 2 highest events per year with respect to wind speed and filter out events of high elevation (\>500m) \- as bad weather tends to be a common occurrence on mountain peaks! Note the use of the function [geohashEncode](https://clickhouse.com/docs/en/sql-reference/functions/geo/geohash/#geohashencode) to capture significant events over a wide area, rather than potentially single anomalous stations, as well as the [dictGet](https://clickhouse.com/docs/en/sql-reference/functions/ext-dict-functions/#dictget-dictgetordefault-dictgetornull) function to restrict our analysis to the United States.


[![metabase-hurricanes.gif](/uploads/metabase_hurricanes_48f2f78e1b.gif)](/uploads/metabase_hurricanes_48f2f78e1b.gif)
  

As expected, we capture [hurricanes impacting the east coast](https://en.wikipedia.org/wiki/List_of_United_States_hurricanes) \- including [Katrina in 2005](https://en.wikipedia.org/wiki/Hurricane_Katrina).



```

SELECT
    week,
    toYear(week) AS year,
    lat, lon,
    avg_precipitation,
    max_wind_speed * 10
FROM
(
    SELECT
        geoHash,
        week,
        geohashDecode(geoHash) AS lonlat,
        lonlat.1 AS lon,
        lonlat.2 AS lat,
        max(maxWindSpeed) AS max_wind_speed,
        avg(precipitation)/10 AS avg_precipitation
    FROM blogs.noaa
    WHERE (dictGet(blogs.country_polygons, 'name', location) IN ('United States of America')) AND (elevation < 500) AND toMonth(date) BETWEEN 6 AND 10
    GROUP BY
        geohashEncode(location.1, location.2, 4) AS geoHash,
        toStartOfWeek(date) AS week
    HAVING max_wind_speed > 300  AND avg_precipitation > 20
    ORDER BY
        max_wind_speed DESC
)
ORDER BY
    year ASC,
    max_wind_speed DESC
LIMIT 2 BY year
 [✎](https://sql.clickhouse.com?query_id=T7DVXL4IRQSYDZXUZEMYOL)

```


The waterfall visualization conveys similar information to the [Grafana candlestick](https://clickhouse.com/blog/visualizing-data-with-grafana) shown in our earlier post \- a popular technique for forex datasets. Below we reuse a query from [our earlier forex post](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3) to plot the GBP/EUR currency pair change \- using a [window function](https://clickhouse.com/docs/en/sql-reference/functions/time-window-functions/) over the daily close price. As shown, Metabase also preserves the notion of dashboards to collate multiple visualizations.


[![metabase-4-waterfall.gif](/uploads/meatabase_4_waterfall_83c2b7e296.gif)](/uploads/meatabase_4_waterfall_83c2b7e296.gif)
  


```

SELECT
    base,
    quote,
    day,
    close,
    close - any(close) OVER (PARTITION BY base, quote ORDER BY base ASC, quote ASC, day ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS change
FROM
(
    SELECT
        base,
        quote,
        day,
        argMax(ask, datetime) AS close
    FROM blogs.forex
    WHERE (quote = 'GBP') AND (base = 'EUR')
    GROUP BY
        base,
        quote,
        toStartOfDay(datetime) AS day
    ORDER BY
        base ASC,
        quote ASC,
        day ASC
)
ORDER BY day ASC
 [✎](https://sql.clickhouse.com?query_id=BXNF4KPUROV9QRCS5FAGMD)

```


Similar to Grafana and Superset, Metabase supports combo charts to allow multiple axes to be plotted. For example purposes, we use the [UK house price dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid) used throughout our docs. We plot the average house price and sales per month since 1995, differentiating between [leasehold and freehold](https://www.moneyhelper.org.uk/en/homes/buying-a-home/leasehold-vs-freehold-whats-the-difference) transactions.


[![metabase-5-prices.gif](/uploads/metabase_5_prices_cd9d9a76dc.gif)](/uploads/metabase_5_prices_cd9d9a76dc.gif)
  


```

SELECT
    month,
    countIf(duration = 'leasehold') AS `Leasehold Sold`,
    countIf(duration = 'freehold') AS `Freehold Sold`,
    avgIf(price, duration = 'freehold') AS `Average Freehold Price`,
    avgIf(price, duration = 'leasehold') AS `Average Leasehold Price`
FROM uk_price_paid
GROUP BY toStartOfMonth(date) AS month
ORDER BY month ASC
 [✎](https://sql.clickhouse.com?query_id=5DVCXJZPH77BQJKREMEG8Z)

```


Returning to our NOAA dataset, we were curious as to where might be perfect holiday destination based on climatic conditions. Our rudimentary criteria \- good temperature range, little rain, non\-excessive elevation, and absence of extreme weather events, might be a little contrived, but this allows us to demonstrate the funnel visualization and usage of the [arrayJoin](https://clickhouse.com/docs/en/sql-reference/functions/array-functions/#arrayjoinarr) and [If combinator](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators/#-if) functions for transforming column names to values. We compute our conditions over geo hash regions and months of the year, thereby not just considering a single station recording.


[![metabase-6-funnel.gif](/uploads/metabase_6_funnel_bf9903a805.gif)](/uploads/metabase_6_funnel_bf9903a805.gif)
  


```

SELECT
    values.1 AS labels,
    values.2 AS count
FROM
(
    SELECT arrayJoin([('not_too_cold', countIf(min_temp > 0)), ('not_too_cold_or_cold', countIf((min_temp > 0) AND (max_temp < 40))), ('ideal_temp', countIf((max_temp < 40) AND (min_temp > 0) AND (avg_temp > 10))), ('ideal_temp_min_rain', countIf((max_temp < 40) AND (min_temp > 0) AND (avg_temp > 10) AND (sum_precipitation < 100))), ('ideal_temp_min_rain_not_high', countIf((max_temp < 40) AND (min_temp > 0) AND (avg_temp > 10) AND (sum_precipitation < 100) AND (avg_elevation < 1000)))]) AS values
    FROM
    (
        SELECT
            geoHash,
            month,
            avg(percentDailySun) AS avg_daily_sun,
            geohashDecode(geoHash) AS lonlat,
            lonlat.1 AS lat,
            lonlat.2 AS lon,
            avg(tempAvg) / 10 AS avg_temp,
            max(tempMax) / 10 AS max_temp,
            min(tempMin) / 10 AS min_temp,
            sum(precipitation) AS sum_precipitation,
            avg(elevation) AS avg_elevation
        FROM blogs.noaa
        WHERE date > '1970-01-01'
        GROUP BY
            geohashEncode(location.1, location.2, 4) AS geoHash,
            toMonth(date) AS month
    )
)
 [✎](https://sql.clickhouse.com?query_id=9MFVCCCQDPMXAB6TMG6LQZ)

```


For those curious about the optimal locations, the Pin map allows us to interpret the coordinates quickly. This requires us to move our most restrictive condition to a HAVING clause.


[![metabase-pin-map.gif](/uploads/metabase_pin_map_e070ffb4d8.gif)](/uploads/metabase_pin_map_e070ffb4d8.gif)
  


```

SELECT
    geoHash,
    month,
    avg(percentDailySun) AS avg_daily_sun,
    geohashDecode(geoHash) AS lonlat,
    lonlat.1 AS lon,
    lonlat.2 AS lat,
    avg(tempAvg) / 10 AS avg_temp,
    max(tempMax) / 10 AS max_temp,
    min(tempMin) / 10 AS min_temp,
    sum(precipitation) AS sum_precipitation,
    avg(elevation) AS avg_elevation
FROM blogs.noaa
WHERE date > '1970-01-01'
GROUP BY
    geohashEncode(location.1, location.2, 4) AS geoHash,
    toMonth(date) AS month
HAVING (max_temp < 40) AND (min_temp > 0) AND (avg_temp > 10) AND (sum_precipitation < 100) AND (avg_elevation < 1000)
 [✎](https://sql.clickhouse.com?query_id=DN1SAY1IIIEAWRPF4JHFCG)

```


We’ll leave it to the reader to explore these locations and report if they do make ideal holiday destinations.


## Summary [\#](/blog/visualizing-data-with-metabase#summary)


In this post, we’ve demonstrated how Metabase offers a great getting\-started experience for users not familiar with SQL by providing a simple but effective way to build visualizations for BI via the questions feature. This contrasts with the other tools in this blog series which address other needs. Grafana has a clear strength with respect to time series data and its evolving flexibility in use cases such as geo analysis, requiring users to be comfortable in SQL. Superset meanwhile optimizes for data analysts and BI use cases with an excellent SQL editor and the ability to save any query as a reusable “dataset”, resulting in a highly effective way of building visualizations. Your choice will often depend on your data and personal preference, but all are first\-class citizens within the ClickHouse ecosystem, which we hope to continue to improve.


*If you’re enthusiastic about the latest technologies and are passionate about Open Source, we’re currently hiring for our [integrations team](https://clickhouse.com/company/careers) and would love to hear from you.*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
