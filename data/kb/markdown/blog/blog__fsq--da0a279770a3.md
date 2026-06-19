# Visualizing Foursquare places with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Visualizing Foursquare places with ClickHouse

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)May 8, 2025 · 8 minutes readRecently, we had an all\-company offsite, where most of our company gathered together. I always use this event to organize a hackathon. This time, it was a data visualization hackathon with simple rules: you have two hours, you take a dataset and make a nice demo on top of it with ClickHouse. I also participated in this hackathon, and [here is what I've made](https://adsb.exposed/?dataset=Places&zoom=5&lat=52.3488&lng=4.9219)


![Screenshot_20250506_230316.png](/uploads/Screenshot_20250506_230316_0a16182f12.png)
## Dataset [\#](/blog/fsq#dataset)


The dataset is located [here](https://opensource.foursquare.com/os-places/) and is available for download and free usage under the Apache 2\.0 license. It contains information about places on a map, such as shops, restaurants, parks, playgrounds, and monuments, with additional metadata, such as categories, emails, etc. It is not large from the ClickHouse perspective, just above 100 million records. However, it is probably the largest open\-source dataset of this kind available.


Recently, I made a [visualization tool for air traffic](https://clickhouse.com/blog/interactive-visualization-analytics-adsb-flight-data-with-clickhouse), and it works in real\-time on top of a 1000x times bigger dataset (currently, 130 billion records). So, visualizing a small dataset of Foursquare is a no\-brainer, and I decided to reuse the same tool.


### Taking a look at the data [\#](/blog/fsq#taking-a-look-at-the-data)


To preview the dataset and query it directly, you can use the `s3` table function:



```
:) SELECT * FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*') LIMIT 10

Row 1:
──────
fsq_place_id:        4ed7a0b89adf06cbf6d71fec
name:                Частная Бильярдная
latitude:            55.82704778252206
longitude:           37.44663365528853
address:             ᴺᵁᴸᴸ
locality:            ᴺᵁᴸᴸ
region:              ᴺᵁᴸᴸ
postcode:            ᴺᵁᴸᴸ
admin_region:        ᴺᵁᴸᴸ
post_town:           ᴺᵁᴸᴸ
po_box:              ᴺᵁᴸᴸ
country:             RU
date_created:        2011-12-01
date_refreshed:      2013-01-13
date_closed:         ᴺᵁᴸᴸ
tel:                 ᴺᵁᴸᴸ
website:             ᴺᵁᴸᴸ
email:               ᴺᵁᴸᴸ
facebook_id:         ᴺᵁᴸᴸ
instagram:           ᴺᵁᴸᴸ
twitter:             ᴺᵁᴸᴸ
fsq_category_ids:    ['4bf58dd8d48988d1e3931735']
fsq_category_labels: ['Arts and Entertainment > Pool Hall']
placemaker_url:      https://foursquare.com/placemakers/review-place/4ed7a0b89adf06cbf6d71fec
geom:                @B�+J�`�@K�ܳ��
bbox:                (37.44663365528853,55.82704778252206,37.44663365528853,55.82704778252206)

:) SELECT * FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*')
   WHERE address IS NOT NULL AND postcode IS NOT NULL AND instagram IS NOT NULL LIMIT 10

Row 1:
──────
fsq_place_id:        643c2e2fc5a3b53de7ddfea7
name:                VIBE Nagymaros
latitude:            47.781879
longitude:           18.946042
address:             Szamaras Utca
locality:            Nagymaros
region:              PE
postcode:            2626
admin_region:        ᴺᵁᴸᴸ
post_town:           ᴺᵁᴸᴸ
po_box:              ᴺᵁᴸᴸ
country:             HU
date_created:        2023-04-16
date_refreshed:      2024-10-18
date_closed:         ᴺᵁᴸᴸ
tel:                 ᴺᵁᴸᴸ
website:             http://www.vibenagymaros.hu
email:               ᴺᵁᴸᴸ
facebook_id:         ᴺᵁᴸᴸ
instagram:           vibenagymaros
twitter:             ᴺᵁᴸᴸ
fsq_category_ids:    ['56aa371be4b08b9a8d5734e1']
fsq_category_labels: ['Travel and Transportation > Lodging > Vacation Rental']
placemaker_url:      https://foursquare.com/placemakers/review-place/643c2e2fc5a3b53de7ddfea7
geom:                @2�/���v@G��o6�
bbox:                (18.946042,47.781879,18.946042,47.781879)


```

Analyzing local and external datasets is very convenient with [clickhouse\-local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local), a small command\-line tool that provides a full ClickHouse engine.


The `DESCRIBE` query gives automatically inferred schema for the data:



```
:) DESCRIBE s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*')

    ┌─name────────────────┬─type────────────────────────┐
 1. │ fsq_place_id        │ Nullable(String)            │
 2. │ name                │ Nullable(String)            │
 3. │ latitude            │ Nullable(Float64)           │
 4. │ longitude           │ Nullable(Float64)           │
 5. │ address             │ Nullable(String)            │
 6. │ locality            │ Nullable(String)            │
 7. │ region              │ Nullable(String)            │
 8. │ postcode            │ Nullable(String)            │
 9. │ admin_region        │ Nullable(String)            │
10. │ post_town           │ Nullable(String)            │
11. │ po_box              │ Nullable(String)            │
12. │ country             │ Nullable(String)            │
13. │ date_created        │ Nullable(String)            │
14. │ date_refreshed      │ Nullable(String)            │
15. │ date_closed         │ Nullable(String)            │
16. │ tel                 │ Nullable(String)            │
17. │ website             │ Nullable(String)            │
18. │ email               │ Nullable(String)            │
19. │ facebook_id         │ Nullable(Int64)             │
20. │ instagram           │ Nullable(String)            │
21. │ twitter             │ Nullable(String)            │
22. │ fsq_category_ids    │ Array(Nullable(String))     │
23. │ fsq_category_labels │ Array(Nullable(String))     │
24. │ placemaker_url      │ Nullable(String)            │
25. │ geom                │ Nullable(String)            │
26. │ bbox                │ Tuple(                     ↴│
    │                     │↳    xmin Nullable(Float64),↴│
    │                     │↳    ymin Nullable(Float64),↴│
    │                     │↳    xmax Nullable(Float64),↴│
    │                     │↳    ymax Nullable(Float64)) │
    └─────────────────────┴─────────────────────────────┘

```

## Loading into ClickHouse [\#](/blog/fsq#loading-into-clickhouse)


I created the following table:



```
CREATE TABLE foursquare_mercator
(
    fsq_place_id String,
    name String,
    latitude Float64,
    longitude Float64,
    address String,
    locality String,
    region LowCardinality(String),
    postcode LowCardinality(String),
    admin_region LowCardinality(String),
    post_town LowCardinality(String),
    po_box LowCardinality(String),
    country LowCardinality(String),
    date_created Nullable(Date),
    date_refreshed Nullable(Date),
    date_closed Nullable(Date),
    tel String,
    website String,
    email String,
    facebook_id String,
    instagram String,
    twitter String,
    fsq_category_ids Array(String),
    fsq_category_labels Array(String),
    placemaker_url String,
    geom String,
    bbox Tuple(
        xmin Nullable(Float64),
        ymin Nullable(Float64),
        xmax Nullable(Float64),
        ymax Nullable(Float64)),

    category LowCardinality(String) ALIAS fsq_category_labels[1],
    mercator_x UInt32 MATERIALIZED 0xFFFFFFFF * ((longitude + 180) / 360),
    mercator_y UInt32 MATERIALIZED 0xFFFFFFFF * ((1 / 2) - ((log(tan(((latitude + 90) / 360) * pi())) / 2) / pi())),
    INDEX idx_x mercator_x TYPE minmax,
    INDEX idx_y mercator_y TYPE minmax
)
ORDER BY mortonEncode(mercator_x, mercator_y)

```

Most of the structure is the same as in the source. Additionally, I've created two materialized columns, `mercator_x` and `mercator_y` that map the lat/lon coordinates to the [Web Mercator](https://en.wikipedia.org/wiki/Web_Mercator_projection) projection. The coordinates on the Mercator projection are represented by two UInt32 numbers for easier segmentation of the map into tiles. Additionally, I set up the order of the table by a [space\-filling curve](https://en.wikipedia.org/wiki/Space-filling_curve) on top of these numbers, and I created two `minmax` indices for faster search. ClickHouse has everything we need for real\-time mapping applications!


Then, I loaded the data with the following query:



```
INSERT INTO foursquare_mercator SELECT * FROM s3('s3://fsq-os-places-us-east-1/release/dt=2025-04-08/places/parquet/*')

```

The whole dataset is loaded in **42 seconds** and takes **11 GB**.


## Visualization [\#](/blog/fsq#visualization)


I only [slightly modified](https://github.com/ClickHouse/adsb.exposed/compare/main...foursquare) the [adsb.exposed](https://adsb.exposed/) tool, with 48 lines consisted mostly by replacing a table name and adding new example queries.


When I opened the page, I was amazed at how beautiful it was!


![Screenshot_20250506_025216.png](/uploads/Screenshot_20250506_025216_949653b810.png)
![Screenshot_20250506_230749.png](/uploads/Screenshot_20250506_230749_b4396c9cc5.png)
And it gives a lot of interesting info. For example, try to do rectangular selection over Tokyo, and then filter all the world for [Sake bars](https://adsb.exposed/?dataset=Places&zoom=5&lat=38.4622&lng=135.8789&query=dde166991e51d41998feef29f2c3c409)! Or find countries with a larger and smaller number of [ATM machines](https://adsb.exposed/?dataset=Places&zoom=5&lat=45.0735&lng=9.8877&query=33830e2b3973c97d1c2023234216a9ae).


## Comparison with other tools [\#](/blog/fsq#comparison-with-other-tools)


This visualization is not new \- similar projects have been made a few times.


The visualization in [Foursquare Studio](https://studio.foursquare.com/map/public/32a54c6d-81fb-47b6-a9c7-12fdea15f9a0) looks similar. But it loads much slower and has a low resolution. They aggregate data by [H3 hexagons](https://clickhouse.com/docs/sql-reference/functions/geo/h3) while I do it on a single\-pixel level. The difference in detail is most visible in the Alps.


![Screenshot_20250506_213050.png](/uploads/Screenshot_20250506_213050_da85c5c5e9.png)
![Screenshot_20250506_213010.png](/uploads/Screenshot_20250506_213010_32cd59a735.png)
To be honest, my visualization does not correctly compare the densities of points in regions with different latitudes, while the original visualization does it properly. Another difference is that my tool works fast in the browser by loading rasterized tiles, while the original visualization makes the browser lag.


This visualization by [Simon Wilson](https://simonwillison.net/2024/Nov/20/foursquare-open-source-places/) used DuckDB for a fairly basic visualization.


Here is the visualization from [Mark's blog](https://tech.marksblogg.com/foursquare-open-global-poi-dataset.html). It looks beautiful, much like mine, but it is not interactive.


[Kepler.gl](https://kepler.gl/demo) is a tool for visualizing local datasets in the browser with GPU. When I tried it on a MacBook Pro M3, it worked with only a small subset of the data (a million records), and the browser struggled to render it without lagging. To be honest, Kepler.gl does a lot of cool visualizations, while being limited in the data processing.


## Bottomline [\#](/blog/fsq#bottomline)


ClickHouse is a good option for analytics on large\-scale geographical datasets. The Foursquare dataset has 100 million records, while the ADS\-B dataset has 130 billion records and counting. ClickHouse customers use the service with datasets over tens of trillions of records. ClickHouse processes queries in a blink, and does it with grace!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
