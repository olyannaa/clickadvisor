# Birds in the cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Birds in the cloud

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Jun 4, 2025 · 9 minutes readI had never heard about birdwatching until the last day when I stumbled upon the Cornell Lab of Ornithology's [eBird project](https://science.ebird.org/en/use-ebird-data). It provides a dataset of bird observations worldwide, with 1\.5 billion records updated monthly.


I immediately loaded this dataset into my [visualization tool](https://adsb.exposed/?dataset=Birds&zoom=5&lat=52.2278&lng=5.0977). The [adsb.exposed](https://adsb.exposed/) website already contains a dataset of [air traffic](https://clickhouse.com/blog/interactive-visualization-analytics-adsb-flight-data-with-clickhouse) with over 130 billion records and a dataset of [Foursquare places](https://clickhouse.com/blog/fsq). There is certainly a larger number of birds than airplanes, but the dataset of bird observations is a hundred times smaller, so it is easy to load and analyze it.


[![Screenshot_20250510_040906.png](/uploads/Screenshot_20250601_185629_ba64647feb.png)](https://adsb.exposed/?dataset=Birds&zoom=5&lat=52.2278&lng=5.0977)


## Dataset [\#](/blog/birds#dataset)


The dataset is located [here](https://hosted-datasets.gbif.org/eBird/2023-eBird-dwca-1.0.zip) in a zip file of 58 GB. It contains a CSV file of 440 GB in size.


### Download the dataset [\#](/blog/birds#download-the-dataset)



```

```
1wget 'https://hosted-datasets.gbif.org/eBird/2023-eBird-dwca-1.0.zip'
```

```

Analyzing local and external datasets is very convenient with [clickhouse\-local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local), a small command\-line tool that provides a full ClickHouse engine.


### Download clickhouse\-local [\#](/blog/birds#download-clickhouse-local)



```

```
1curl https://clickhouse.com/ | sh
2sudo ./clickhouse install # or run it as ./clickhouse without installation
```

```

### Let's preview the dataset structure [\#](/blog/birds#lets-preview-the-dataset-structure)


ClickHouse allows the processing of files inside archives without decompressing.



```

```
1DESCRIBE file('2023-eBird-dwca-1.0.zip :: *.csv');
```

```


```
    ┌─name──────────────┬─type──────────────┐
 1. │ basisofrecord     │ Nullable(String)  │
 2. │ institutioncode   │ Nullable(String)  │
 3. │ collectioncode    │ Nullable(String)  │
 4. │ catalognumber     │ Nullable(String)  │
 5. │ occurrenceid      │ Nullable(String)  │
 6. │ recordedby        │ Nullable(String)  │
 7. │ year              │ Nullable(Int64)   │
 8. │ month             │ Nullable(Int64)   │
 9. │ day               │ Nullable(Int64)   │
10. │ publishingcountry │ Nullable(String)  │
11. │ country           │ Nullable(String)  │
12. │ stateprovince     │ Nullable(String)  │
13. │ county            │ Nullable(String)  │
14. │ decimallatitude   │ Nullable(Float64) │
15. │ decimallongitude  │ Nullable(Float64) │
16. │ locality          │ Nullable(String)  │
17. │ kingdom           │ Nullable(String)  │
18. │ phylum            │ Nullable(String)  │
19. │ class             │ Nullable(String)  │
20. │ order             │ Nullable(String)  │
21. │ family            │ Nullable(String)  │
22. │ genus             │ Nullable(String)  │
23. │ specificepithet   │ Nullable(String)  │
24. │ scientificname    │ Nullable(String)  │
25. │ vernacularname    │ Nullable(String)  │
26. │ taxonremarks      │ Nullable(String)  │
27. │ taxonconceptid    │ Nullable(String)  │
28. │ individualcount   │ Nullable(Int64)   │
    └───────────────────┴───────────────────┘

```

The `DESCRIBE` query gives an automatically inferred schema for the data. The `file` table function allows the processing of files on the local filesystem and the `::` notation allows the processing of files inside archives. All filenames support glob\-expansions with `*`, `?`, `**`, `{0..9}`, `{abc,def}`. For CSV files, ClickHouse automatically detects if there is a header and uses the header if it is present. It also automatically detects data types of columns. With all these conveniences, ClickHouse makes data processing seamless.


### Preview the data [\#](/blog/birds#preview-the-data)



```

```
1SELECT * FROM file('2023-eBird-dwca-1.0.zip :: *.csv') LIMIT 1;
```

```


```
Row 1:
──────
basisofrecord:     HumanObservation
institutioncode:   CLO
collectioncode:    EBIRD_ARG
catalognumber:     OBS602415301
occurrenceid:      URN:catalog:CLO:EBIRD_ARG:OBS602415301
recordedby:        obsr904254
year:              1989
month:             4
day:               23
publishingcountry: AR
country:           Argentina
stateprovince:     Salta
county:            Anta
decimallatitude:   -24.7
decimallongitude:  -64.63333
locality:          PN El Rey
kingdom:           Animalia
phylum:            Chordata
class:             Aves
order:             Pelecaniformes
family:            Threskiornithidae
genus:             Theristicus
specificepithet:   caudatus
scientificname:    Theristicus caudatus
vernacularname:    Buff-necked Ibis
taxonremarks:      ᴺᵁᴸᴸ
taxonconceptid:    avibase-5E393799
individualcount:   ᴺᵁᴸᴸ

1 row in set. Elapsed: 0.008 sec.

```

And this is an [ibis in Argentina](https://adsb.exposed/?dataset=Birds&zoom=5&lat=-16.3623&lng=-60.9525&query=35198a853912e85c5a96e9767ebe7e0c&box=-17.0568,-65.6250,-19.8356,-62.2266)!


[![Screenshot_20250601_181745.png](/uploads/Screenshot_20250601_181745_88f6c3a588.png)](javascript:void(0))


## Loading into ClickHouse [\#](/blog/birds#loading-into-clickhouse)


You can analyze the data with **clickhouse\-local**, but to create an interactive website, we will load it to **clickhouse\-server**. By the way, there is almost no difference between **clickhouse\-local** and **clickhouse\-server** \- it is the same binary executable. The main difference is that **clickhouse\-server** listens to connections.


### Table structure [\#](/blog/birds#table-structure)


I created the following table:



```

```
1CREATE TABLE birds_mercator
2(
3    basisofrecord LowCardinality(String),
4    institutioncode LowCardinality(String),
5    collectioncode LowCardinality(String),
6    catalognumber String,
7    occurrenceid String,
8    recordedby String,
9    year UInt16 EPHEMERAL,
10    month UInt8 EPHEMERAL,
11    day UInt8 EPHEMERAL,
12    publishingcountry LowCardinality(String),
13    country LowCardinality(String),
14    stateprovince LowCardinality(String),
15    county LowCardinality(String),
16    decimallatitude Float32,
17    decimallongitude Float32,
18    locality LowCardinality(String),
19    kingdom LowCardinality(String),
20    phylum LowCardinality(String),
21    class LowCardinality(String),
22    order LowCardinality(String),
23    family LowCardinality(String),
24    genus LowCardinality(String),
25    specificepithet LowCardinality(String),
26    scientificname LowCardinality(String),
27    vernacularname LowCardinality(String),
28    taxonremarks LowCardinality(String),
29    taxonconceptid LowCardinality(String),
30    individualcount UInt32,
31
32    date Date32 MATERIALIZED makeDate32(year, month, day),
33    mercator_x UInt32 MATERIALIZED 0xFFFFFFFF * ((decimallongitude + 180) / 360),
34    mercator_y UInt32 MATERIALIZED 0xFFFFFFFF * ((1 / 2) - ((log(tan(((decimallatitude + 90) / 360) * pi())) / 2) / pi())),
35    INDEX idx_x mercator_x TYPE minmax,
36    INDEX idx_y mercator_y TYPE minmax
37)
38ORDER BY mortonEncode(mercator_x, mercator_y)
```

```

Most of the structure is the same as inferred from the CSV file.


I removed `Nullable` because it is unneeded \- I'd better use empty strings instead of NULLs, and it is generally good practice.


I've replaced `year`, `month`, `day` with `EPHEMERAL` columns and added a `date` column, calculated from them: `date Date MATERIALIZED makeDate(year, month, day)`. `EPHEMERAL` columns are used in `INSERT` queries but are not stored in a table \- they can be used to calculate expressions for other columns to apply transformations on the insertion time. In contrast, `MATERIALIZED` columns are columns that cannot be used in the INSERT query but are always calculated from their expressions.


I've analyzed the number of distinct values in various columns and replaced many of the `String` data types with `LowCardinality(String)` to apply dictionary encoding. For example, the `country` column contains only 253 unique values.


Additionally, I've created two materialized columns, `mercator_x` and `mercator_y` that map the lat/lon coordinates to the [Web Mercator](https://en.wikipedia.org/wiki/Web_Mercator_projection) projection. The coordinates on the Mercator projection are represented by two UInt32 numbers for easier segmentation of the map into tiles. Additionally, I set up the order of the table by a [space\-filling curve](https://en.wikipedia.org/wiki/Space-filling_curve) on top of these numbers, and I created two `minmax` indices for faster search. ClickHouse has everything we need for real\-time mapping applications!


### Data loading [\#](/blog/birds#data-loading)


Then, I loaded the data with the following query:



```

```
1ch --progress --query "
2    SELECT * FROM file('2023-eBird-dwca-1.0.zip :: eod.csv')
3    WHERE decimallatitude BETWEEN -89 AND 89
4      AND decimallongitude BETWEEN -180 AND 180
5    FORMAT Native" \
6| clickhouse-client --host ... --query "INSERT INTO birds_mercator (basisofrecord, institutioncode, collectioncode, catalognumber, occurrenceid, recordedby, year, month, day, publishingcountry, country, stateprovince, county, decimallatitude, decimallongitude, locality, kingdom, phylum, class, order, family, genus, specificepithet, scientificname, vernacularname, taxonremarks, taxonconceptid, individualcount) FORMAT Native"
```

```

Here, I use `clickhouse-local` (which is available under the `ch` alias after installation) to filter out of bound values of latitude and longitude (required by the Mercator projection) and convert the result to the `Native` format, which is optimal for insertion. The result is piped into `clickhouse-client` and inserted into my ClickHouse server in ClickHouse Cloud.


The table took only **16\.8 GB** in ClickHouse, which is much less than the **58 GB** zip file, thanks to ClickHouse compression! This is only **11 bytes** on average per each of the 1\.5 billion bird observations.



```

```
1SELECT name, total_rows, total_bytes FROM system.tables WHERE name = 'birds_mercator'
```

```


```
┌─name───────────┬─total_rows─┬─total_bytes─┐
│ birds_mercator │ 1512208407 │ 16847994349 │
└────────────────┴────────────┴─────────────┘

```

## Visualization [\#](/blog/birds#visualization)


I've added the dataset with this [configuration change](https://github.com/ClickHouse/adsb.exposed/pull/42), and we can instantly explore it!


For example, you can color the map by different orders of birds:


[![Screenshot_20250601_175622.png](/uploads/Screenshot_20250601_175622_72b4e2860f.png)](https://adsb.exposed/?dataset=Birds&zoom=5&lat=40.0949&lng=-98.3936&query=3e17d5bb45e8755d4cd4251592e68645)


We can map only sea birds:


[![Screenshot_20250601_175947.png](/uploads/Screenshot_20250601_175947_63034472a9.png)](https://adsb.exposed/?dataset=Birds&zoom=5&lat=40.0949&lng=-98.3936&query=bb05ddabf821cbe7cec445f9da640ef0)


Interesting to look birds' paths in the south Atlantic near Patagonia:


[![Screenshot_20250601_173052.png](/uploads/Screenshot_20250601_173052_091a856992.png)](https://adsb.exposed/?dataset=Birds&zoom=4&lat=-55.8011&lng=-55.2667&query=3e17d5bb45e8755d4cd4251592e68645&box=-52.7140,-40.0616,-55.9573,-33.5577)


And New Zealand:


[![Screenshot_20250601_173133.png](/uploads/Screenshot_20250601_173133_4b4ddca18a.png)](https://adsb.exposed/?dataset=Birds&zoom=5&lat=-50.4464&lng=167.7278&query=3e17d5bb45e8755d4cd4251592e68645&box=-51.5662,167.7425,-53.4384,171.2581)


Let's filter only penguins:


[![Screenshot_20250601_173836.png](/uploads/Screenshot_20250601_173836_116f64597d.png)](https://adsb.exposed/?dataset=Birds&zoom=4&lat=-50.9351&lng=-68.3380&query=844348dc6ec476336aea65733124908f&box=-59.8664,-65.0227,-65.1026,-48.6165)


Let's show different sorts of Kiwi by adding `AND family = 'Apterygidae'` to the filter:


[![Screenshot_20250601_174117.png](/uploads/Screenshot_20250601_174117_59e5c0b5dc.png)](https://adsb.exposed/?dataset=Birds&zoom=6&lat=-42.1064&lng=169.8710&query=93e36cb2404198e1ddf67f2562c8993d&box=-42.5261,171.1011,-43.1811,172.3169)


If you see this bird, you'll have no regrets!


[![Screenshot_20250601_174318.png](/uploads/Screenshot_20250601_174318_87d5a96f3e.png)](https://adsb.exposed/?dataset=Birds&zoom=6&lat=-42.1064&lng=169.8710&query=93e36cb2404198e1ddf67f2562c8993d&box=-42.5261,171.1011,-43.1811,172.3169)


This crow lives only in Asia:


[![Screenshot_20250601_174438.png](/uploads/Screenshot_20250601_174438_81874b8582.png)](https://adsb.exposed/?dataset=Birds&zoom=4&lat=12.3400&lng=107.8357&query=7ae201133e87a312efe1957075f7e519&box=17.3087,73.0817,3.1625,85.7380)


## Comparison with other tools [\#](/blog/birds#comparison-with-other-tools)


eBird provides its own basic [visualization on a map](https://ebird.org/map), but it is not as interactive and provides no such detail into the data and no direct SQL queries.


## Bottomline [\#](/blog/birds#bottomline)


ClickHouse is a good option for analytics on large\-scale geographical datasets. The eBird dataset has 1\.5 billion records, while the ADS\-B dataset has 130 billion records and counting. ClickHouse customers use the service with datasets over tens of trillions of records. ClickHouse makes large datasets fly!


Reference: eBird. 2021\. eBird: An online database of bird distribution and abundance \[web application]. eBird, Cornell Lab of Ornithology, Ithaca, New York. Available: <https://www.ebird.org>. (Accessed: June 1st, 2025\).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
