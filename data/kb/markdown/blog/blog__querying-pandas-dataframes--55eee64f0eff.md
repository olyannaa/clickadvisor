# Querying Pandas DataFrames with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Querying Pandas DataFrames with ClickHouse

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Nov 15, 2023 · 5 minutes readIn the world of data analysis, Pandas is considered the starting point for most Python\-based data exploration. But what if we want to query our DataFrames using an OLAP database like ClickHouse to take advantage of its query engine and SQL support?


This is where [chDB](https://github.com/chdb-io/chdb/tree/main), a Python library powered by ClickHouse, comes into play. We’ve already featured chDB [a couple](https://clickhouse.com/blog/welcome-chdb-to-clickhouse) [of times](https://clickhouse.com/blog/chdb-embedded-clickhouse-rocket-engine-on-a-bicycle) already on the blog, but in this post we’re going to focus on its ability to query Pandas DataFrames, join them together, aggregate data, and then export the results back to Pandas.



chDB is available via PyPi, which means we can install it with pip:



```
pip install chdb

```

We’ll also need to install Pandas and PyArrow as the DataFrame functionality of chDB has dependencies on those libraries:



```
pip install pandas pyarrow

```

Ok, now we’re good to go. We’re going to explore [Kaggle’s Canadian house prices for top cities
Dataset](https://www.kaggle.com/datasets/jeremylarcher/canadian-house-prices-for-top-cities), which contains real estate data from the 2021 census.


Once we’ve downloaded the CSV file, we’re going to read it into a Pandas DataFrame.



```
import pandas as pd
house_prices = pd.read_csv(
  filepath_or_buffer="data/HouseListings-Top45Cities-10292023-kaggle.csv", 
  encoding = "ISO-8859-1"
)

```

And then we can have a look at a couple of the records:



```
house_prices.head(n=2).T

```


```
                                          0                      1
City                                Toronto                Toronto
Price                              779900.0               799999.0
Address               #318 -20 SOUTHPORT ST  #818 -60 SOUTHPORT ST
Number_Beds                               3                      3
Number_Baths                              2                      1
Province                            Ontario                Ontario
Population                          5647656                5647656
Latitude                            43.7417                43.7417
Longitude                          -79.3733               -79.3733
Median_Family_Income                97000.0                97000.0

```

## Querying DataFrames with ClickHouse [\#](/blog/querying-pandas-dataframes#querying-dataframes-with-clickhouse)


To query a DataFrame in chDB, we need to import the `chdb.dataframe` module:



```
import chdb.dataframe as cdf

```

This module has a function called query that we can use. We can pass in 1 or more DataFrames as named parameters, which we can then address in the query. The parameter names that we use can be addressed as `__<parameter-name>__`. The following query finds the top 10 cities with the most properties:



```
cdf.query(
    house_prices=house_prices, 
    sql="""
FROM __house_prices__
SELECT City, Province, count(*)
GROUP BY ALL
LIMIT 10
""")

```


```
             City            Province  count()
    b'White Rock' b'British Columbia'     1175
       b'Toronto'          b'Ontario'     1276
       b'Kelowna' b'British Columbia'     1280
      b'Winnipeg'         b'Manitoba'      530
      b'Winnipeg'          b'Ontario'        1
      b'Red Deer'          b'Alberta'      326
   b'Thunder Bay'          b'Ontario'      154
    b'Lethbridge'          b'Alberta'      379
b'St. Catharines'          b'Ontario'     1268
b'Trois-Rivieres'           b'Quebec'      165

```

## Joining DataFrames with ClickHouse [\#](/blog/querying-pandas-dataframes#joining-dataframes-with-clickhouse)


As well as querying individual DataFrames, we can also join them together. So we’re going to bring in another dataset that contains [metadata about Canadian cities](https://simplemaps.com/data/canada-cities). Let’s have a look at that one:



```
cities = pd.read_csv(
    filepath_or_buffer="data/canadacities.csv"
)

cities.head(n=1).T

```


```
                                                               0
city                                                     Toronto
city_ascii                                               Toronto
province_id                                                   ON
province_name                                            Ontario
lat                                                      43.7417
lng                                                     -79.3733
population                                             5647656.0
density                                                   4427.8
timezone                                         America/Toronto
ranking                                                        1
postal         M5T M5V M5P M5S M5R M5E M5G M5A M5C M5B M5M M5...
id                                                    1124279679

```

We can join this DataFrame with the first one via the city\_ascii and province\_name fields.



```
top_cities = cdf.query(
    house_prices=house_prices, 
    cities=cities,
    sql="""
FROM __house_prices__ AS hp
JOIN __cities__ AS c 
ON c.city_ascii = hp.City AND c.province_name = hp.Province
SELECT City, Province, count(*),
       round(avg(Price)) AS avgPrice,
       round(max(Price)) AS maxPrice,
       ranking, density
GROUP BY ALL
LIMIT 10
""")

```

If we view the top\_cities variable, we’ll see similar to the following:



```
           City   Province  count()  avgPrice   maxPrice  ranking  density
   b'Brantford' b'Ontario'      628  955923.0  6495000.0        2   1061.2
    b'Hamilton' b'Ontario'     1289  975543.0 10995000.0        2    509.1
 b'Thunder Bay' b'Ontario'      154  459703.0  5599000.0        2    332.1
     b'Caledon' b'Ontario'     1336 1383366.0  9995000.0        3    111.2
     b'Calgary' b'Alberta'     1322  660046.0  5250000.0        1   1592.4
     b'Windsor' b'Ontario'      720  643019.0  2750000.0        2   1572.8
b'Medicine Hat' b'Alberta'      277  448137.0  1475000.0        3    565.1
    b'Montreal'  b'Quebec'      212  931392.0  4400000.0        1   4833.5
    b'Edmonton' b'Alberta'     1351  425582.0  4463445.0        1   1320.4
     b'Sudbury' b'Ontario'      203  596087.0  7699900.0        2     52.1

```

`top_cities` has the type `<class 'chdb.dataframe.query.Table'>` and we can actually query chDB tables using SQL as well. We can do this using the query function where the underlying table is accessible as `__table__` .


So, if we wanted to get the first 5 rows of top\_cities, we could write the following:



```
top_cities.query("""
FROM __table__ 
SELECT City, maxPrice, ranking, density 
LIMIT 5
""")

```


```
          City   maxPrice  ranking  density
  b'Brantford'  6495000.0        2   1061.2
   b'Hamilton' 10995000.0        2    509.1
b'Thunder Bay'  5599000.0        2    332.1
    b'Caledon'  9995000.0        3    111.2
    b'Calgary'  5250000.0        1   1592.4

```

## Exporting chDB Tables to Pandas DataFrames [\#](/blog/querying-pandas-dataframes#exporting-chdb-tables-to-pandas-dataframes)


And if we’ve done enough querying with ClickHouse, we can always convert that table back to a Pandas DataFrame using the to\_pandas function:



```
top_cities_df = top_cities.to_pandas()

```

And let’s do a bit of querying in Pandas to finish off:



```
(top_cities_df[top_cities_df["Province"] == b"Ontario"]
  .sort_values(["ranking", "density"])
  .drop(["Province"], axis=1)
)  

```


```
          City  count()  avgPrice   maxPrice  ranking  density
    b'Sudbury'      203  596087.0  7699900.0        2     52.1
b'Thunder Bay'      154  459703.0  5599000.0        2    332.1
   b'Hamilton'     1289  975543.0 10995000.0        2    509.1
  b'Brantford'      628  955923.0  6495000.0        2   1061.2
    b'Windsor'      720  643019.0  2750000.0        2   1572.8
    b'Caledon'     1336 1383366.0  9995000.0        3    111.2

```

## In Conclusion [\#](/blog/querying-pandas-dataframes#in-conclusion)


chDB is constantly evolving, but what it can already do is pretty cool. So head over to [the GitHub page](https://github.com/chdb-io/chdb/tree/main) and give it a try!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
