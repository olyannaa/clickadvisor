# ClickHouse Release 25\.5


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 25\.5

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 2, 2025 · 13 minutes readAnother month goes by, which means it’s time for another release!


ClickHouse version 25\.5 contains 15 new features 🌸 23 performance optimizations 🦋 64 bug fixes 🐝


This release sees the vector similarity index move into beta, support for the Hive metastore catalog for Iceberg tables, the ability to track when new functions were added to ClickHouse, implicit table in clickhouse\-local, and more.


## New Contributors [\#](/blog/clickhouse-release-25-05#new-contributors)


A special welcome to all the new contributors in 25\.5! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.


Below are the names of the new contributors:


*Andrian Iliev, Colerar, Dasha Wessely, Denis, KovalevDima, Kyamran, Marta Paes, Mojtaba Ghahari, Sachin Singh, YjyJeff, andrei tinikov, caicre, codeworse, gvoelfin, morsapaes, samay\-sharma, shanfengp, tdufour*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/2025-release-25.5/).


## Hive metastore catalog for Iceberg [\#](/blog/clickhouse-release-25-05#hive-metastore-catalog-for-iceberg)


### Contributed by scanhex12 [\#](/blog/clickhouse-release-25-05#contributed-by-scanhex12)


ClickHouse continues to add more functionality for querying Lakehouses. Previous versions added support for the [Unity](https://clickhouse.com/docs/use-cases/data-lake/unity-catalog) and [AWS Glue](https://clickhouse.com/docs/use-cases/data-lake/glue-catalog) [data catalogs](https://clickhouse.com/engineering-resources/data-catalog), and this version sees support added for the Hive metastore catalog.


We can connect to the catalog by first creating a table with the `DataLakeCatalog` table engine:



```

```
1SET allow_experimental_database_hms_catalog=true;
2CREATE DATABASE hive
3ENGINE = DataLakeCatalog('thrift://hive:9083', '', '')
4SETTINGS
5  catalog_type = 'hive',
6  warehouse = 'demo',
7  storage_endpoint = 'http://minio:9000/warehouse';
```

```

We can then query the tables in that catalog as if they were any other tables:



```

```
1SELECT count()
2FROM default.`iceberg.hits`;
```

```

## Implicit table in clickhouse\-local [\#](/blog/clickhouse-release-25-05#implicit-table-in-clickhouse-local)


### Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-25-05#contributed-by-alexey-milovidov)


When using [clickhouse\-local](https://clickhouse.com/docs/operations/utilities/clickhouse-local), you can omit the `FROM` and `SELECT` clauses when processing files from standard input.


For example, imagine we want to parse [a file](https://github.com/openfootball/football.json/blob/master/2024-25/en.1.json) from the [football.json repository](https://github.com/openfootball/football.json/blob/master/2024-25/en.1.json). We can write the following query to explore the properties in the file:



```

```
1curl -sS 'https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/en.1.json' | 
2./clickhouse -q "JSONAllPathsWithTypes(json)" --input-format JSONAsObject
```

```


```
{'matches':'Array(JSON(max_dynamic_types=16, max_dynamic_paths=256))','name':'String'}

```

From this output, we can see two properties: `name` and `matches`. Let’s write another query to explore what’s in `matches`:



```

```
1curl -sS https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/en.1.json | 
2./clickhouse -q "arrayJoin(json.matches::Array(JSON)) LIMIT 5" --input-format JSONAsObject
```

```


```
{"date":"2024-08-16","round":"Matchday 1","score":{"ft":["1","0"],"ht":["0","0"]},"team1":"Manchester United FC","team2":"Fulham FC","time":"20:00"}
{"date":"2024-08-17","round":"Matchday 1","score":{"ft":["0","2"],"ht":["0","0"]},"team1":"Ipswich Town FC","team2":"Liverpool FC","time":"12:30"}
{"date":"2024-08-17","round":"Matchday 1","score":{"ft":["2","0"],"ht":["1","0"]},"team1":"Arsenal FC","team2":"Wolverhampton Wanderers FC","time":"15:00"}
{"date":"2024-08-17","round":"Matchday 1","score":{"ft":["0","3"],"ht":["0","1"]},"team1":"Everton FC","team2":"Brighton & Hove Albion FC","time":"15:00"}
{"date":"2024-08-17","round":"Matchday 1","score":{"ft":["1","0"],"ht":["1","0"]},"team1":"Newcastle United FC","team2":"Southampton FC","time":"15:00"}

```

If we want to query the `matches` array further, we’d need to update our query to use the `FROM table` syntax, as shown below:



```

```
1curl -sS https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/en.1.json |
2./clickhouse -q \
3"m.date, m.team1, m.team2, m.score.ft::Array(String)[1] || '-' || m.score.ft::Array(String)[2] AS score
4FROM table
5ARRAY JOIN json.matches::Array(JSON) AS m
6LIMIT 5" \
7--input-format JSONAsObject \
8--output-format Pretty \
9--output_format_pretty_row_numbers=0
```

```

We’ve also provided an output format so that the column names will be included in the output:



```
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ m.date     ┃ m.team1              ┃ m.team2                    ┃ score ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ 2024-08-16 │ Manchester United FC │ Fulham FC                  │ 1-0   │
├────────────┼──────────────────────┼────────────────────────────┼───────┤
│ 2024-08-17 │ Ipswich Town FC      │ Liverpool FC               │ 0-2   │
├────────────┼──────────────────────┼────────────────────────────┼───────┤
│ 2024-08-17 │ Arsenal FC           │ Wolverhampton Wanderers FC │ 2-0   │
├────────────┼──────────────────────┼────────────────────────────┼───────┤
│ 2024-08-17 │ Everton FC           │ Brighton & Hove Albion FC  │ 0-3   │
├────────────┼──────────────────────┼────────────────────────────┼───────┤
│ 2024-08-17 │ Newcastle United FC  │ Southampton FC             │ 1-0   │
└────────────┴──────────────────────┴────────────────────────────┴───────┘

```

## Track function origin with `introduced_in` field [\#](/blog/clickhouse-release-25-05#track-function-origin-with-introduced_in-field)


### Contributed by Robert Schulze [\#](/blog/clickhouse-release-25-05#contributed-by-robert-schulze)


The `system.functions` table has a new field called `introduced_in,` which tracks when a function was added to ClickHouse. This field contains values for recently added functions, but we are incrementally adding this information for older functions.


Let’s have a look at the list of functions added in the 25\.5 release:



```

```
1SELECT name, introduced_in, returned_value
2FROM system.functions
3WHERE introduced_in = '25.5'
4FORMAT PrettySpace;
```

```


```
 name                   description

 icebergBucket          Implements logic of iceberg bucket transform: https://iceberg.apache.org/spec/#bucket-transform-details.
 icebergHash            Implements logic of iceberg hashing transform: https://iceberg.apache.org/spec/#appendix-b-32-bit-hash-requirements.
 mapContainsValue       Checks whether the map has the specified value.
 mapContainsValueLike   Checks whether map contains value LIKE specified pattern.
 mapContainsKey         Checks whether the map has the specified key.
 mapExtractValueLike    Returns a map with elements which value matches the specified pattern.
 stringBytesEntropy     Calculates Shannon's entropy of byte distribution in a string.
 stringBytesUniq        Counts the number of distinct bytes in a string.

```

## Geo types in Parquet [\#](/blog/clickhouse-release-25-05#geo-types-in-parquet)


### Contributed by scanhex12 [\#](/blog/clickhouse-release-25-05#contributed-by-scanhex12-1)


ClickHouse’s Parquet reader now supports Geo types. To see how this works, we can run the following query against one of the [Overture Maps datasets](https://docs.overturemaps.org/getting-data/):



```

```
1SELECT id, geometry, bbox, 
2       COLUMNS('^id|geometry|bbox') APPLY(toTypeName)
3FROM s3('s3://overturemaps-us-west-2/release/2025-04-23.0/theme=places/type=place/*')
4WHERE categories.primary = 'pizza_restaurant'
5LIMIT 1
6SETTINGS schema_inference_make_columns_nullable = 0;
```

```


```
Row 1:
──────
id:                   08f95008132998a6036bed7d0b7e7661
geometry:             (119.4407421,-5.15814)
bbox:                 (119.44073,119.44074,-5.15814,-5.158139)
toTypeName(id):       String
toTypeName(geometry): Tuple(Float64, Float64)
toTypeName(bbox):     Tuple(
    xmin Float32,
    xmax Float32,
    ymin Float32,
    ymax Float32)

```

The `geometry` field is being parsed correctly, which wasn’t the case before. In previous versions, the `geometry` field would have displayed as binary, as shown below:



```
Row 1:
──────
id:                   08ff2a1b744f064403498c7aa7fce7a1
geometry:             (-149.069345,-83.5991503)
bbox:                 (-149.06935,-149.06932,-83.59915,-83.599144)
toTypeName(id):       String
toTypeName(geometry): Point
toTypeName(bbox):     Tuple(
    xmin Float32,
    xmax Float32,
    ymin Float32,
    ymax Float32)

```

You can now use ClickHouse to query all of your favorite GeoParquet datasets! We’re always looking for fun datasets to play around with, so let us know if you come across any good ones.


## Vector search is beta [\#](/blog/clickhouse-release-25-05#vector-search-is-beta)


### Contributed by Shankar Iyer [\#](/blog/clickhouse-release-25-05#contributed-by-shankar-iyer)


The [vector similarity index](https://clickhouse.com/docs/engines/table-engines/mergetree-family/annindexes#approximate-nearest-neighbor-search) has moved from experimental to beta. It also has support for pre and post\-filtering when doing hybrid search.


Let’s look at how to use it with a subset of [Cohere’s Wikipedia dataset](https://huggingface.co/datasets/Cohere/wikipedia-22-12-en-embeddings). First, let’s enable the similarity index:



```

```
1SET allow_experimental_vector_similarity_index=1;
```

```

And now we’ll create a table along with an HNSW index on the `emb` field:



```

```
1CREATE TABLE wikiEmbeddings (
2  id Int32,
3  title String,
4  text String,
5  url String,
6  wiki_id Int32,
7  views Float32,
8  paragraph_id Int32,
9  langs Int32,
10  emb Array(Float32),
11  INDEX emb_hnsw emb TYPE vector_similarity('hnsw', 'L2Distance', 768)
12)
13ORDER BY id;
```

```

We’ll import the data from Hugging Face:



```

```
1INSERT INTO wikiEmbeddings
2select *
3FROM url('https://huggingface.co/datasets/Cohere/wikipedia-22-12-en-embeddings/resolve/main/data/train-00000-of-00253-8d3dffb4e6ef0304.parquet')
4SETTINGS max_http_get_redirects=10;
```

```

Now we’re ready to query the data. The following query returns one row from the dataset:



```

```
1SELECT * EXCEPT emb
2FROM wikiEmbeddings
3WHERE id = 120356;
```

```


```
Row 1:
──────
id:           120356
title:        Germany national football team
text:         The Germany national football team () represents Germany in men's international football and played its first match in 1908. The team is governed by the German Football Association ("Deutscher Fußball-Bund"), founded in 1900. Between 1949 and 1990, separate German national teams were recognised by FIFA due to Allied occupation and division: the DFB's team representing the Federal Republic of Germany (commonly referred to as West Germany in English between 1949 and 1990), the Saarland team representing the Saar Protectorate (1950–1956) and the East Germany team representing the German Democratic Republic (1952–1990). The latter two were absorbed along with their records; the present team represents the reunified Federal Republic. The official name and code "Germany FR (FRG)" was shortened to "Germany (GER)" following reunification in 1990.
url:          https://en.wikipedia.org/wiki?curid=250204
wiki_id:      250204
views:        3271.844
paragraph_id: 0
langs:        98


```

As we can see, this entry is from the page about the German national football team. Let’s find the most similar rows to this one:



```

```
1WITH (SELECT emb FROM wikiEmbeddings WHERE id = 120356) AS lookup
2SELECT id, title, text, url, L2Distance(emb, lookup) AS dist
3FROM wikiEmbeddings
4ORDER BY dist
5LIMIT 3
6FORMAT Vertical;
```

```


```
Row 1:
──────
id:    120356
title: Germany national football team
text:  The Germany national football team () represents Germany in men's international football and played its first match in 1908. The team is governed by the German Football Association ("Deutscher Fußball-Bund"), founded in 1900. Between 1949 and 1990, separate German national teams were recognised by FIFA due to Allied occupation and division: the DFB's team representing the Federal Republic of Germany (commonly referred to as West Germany in English between 1949 and 1990), the Saarland team representing the Saar Protectorate (1950–1956) and the East Germany team representing the German Democratic Republic (1952–1990). The latter two were absorbed along with their records; the present team represents the reunified Federal Republic. The official name and code "Germany FR (FRG)" was shortened to "Germany (GER)" following reunification in 1990.
url:   https://en.wikipedia.org/wiki?curid=250204
dist:  0

Row 2:
──────
id:    120367
title: Germany national football team
text:  The Federal Republic of Germany, which was referred to as West Germany, continued the DFB. With recognition by FIFA and UEFA, the DFB maintained and continued the record of the pre-war team. Switzerland was the first team that played West Germany in 1950, with the latter qualifying for the 1954 World Cup and the former hosting it.
url:   https://en.wikipedia.org/wiki?curid=250204
dist:  5.537961

Row 3:
──────
id:    120366
title: Germany national football team
text:  After World War II, Germany was banned from competition in most sports until 1950. The DFB was not a full member of FIFA, and none of the three new German states – West Germany, East Germany, and Saarland – entered the 1950 World Cup qualifiers.
url:   https://en.wikipedia.org/wiki?curid=250204
dist:  6.296622

```

The results here aren’t interesting \- they’re just chunks from the same Wikipedia article. We can make things more interesting by adding a `WHERE` clause to filter out results that have the same `wiki_id` as our lookup row:



```

```
1WITH (SELECT emb FROM wikiEmbeddings WHERE id = 120356) AS lookup,
2     (SELECT wiki_id FROM wikiEmbeddings WHERE id = 120356) AS lookup_wiki_id
3SELECT id, title, text, url, L2Distance(emb, lookup) AS dist
4FROM wikiEmbeddings
5WHERE wiki_id <> lookup_wiki_id
6ORDER BY dist
7LIMIT 3
8FORMAT Vertical;
```

```


```
Row 1:
──────
id:    6420
title: Germany
text:  Football is the most popular sport in Germany. With more than 7 million official members, the German Football Association ("Deutscher Fußball-Bund") is the largest single-sport organisation worldwide, and the German top league, the Bundesliga, attracts the second-highest average attendance of all professional sports leagues in the world. The German men's national football team won the FIFA World Cup in 1954, 1974, 1990, and 2014, the UEFA European Championship in 1972, 1980 and 1996, and the FIFA Confederations Cup in 2017.
url:   https://en.wikipedia.org/wiki?curid=11867
dist:  6.9714794

Row 2:
──────
id:    6336
title: Germany
text:  Formal unification of Germany into the modern nation-state was commenced on 18 August 1866 with the North German Confederation Treaty establishing the Prussia-led North German Confederation later transformed in 1871 into the German Empire. After World War I and the German Revolution of 1918–1919, the Empire was in turn transformed into the semi-presidential Weimar Republic. The Nazi seizure of power in 1933 led to the establishment of a totalitarian dictatorship, World War II, and the Holocaust. After the end of World War II in Europe and a period of Allied occupation, Germany as a whole was organized into two separate polities with limited sovereignity: the Federal Republic of Germany, generally known as West Germany, and the German Democratic Republic, East Germany, while Berlin continued its Four Power status. The Federal Republic of Germany was a founding member of the European Economic Community and the European Union, while the German Democratic Republic was a communist Eastern Bloc state and member of the Warsaw Pact. After the fall of communism, German reunification saw the former East German states join the Federal Republic of Germany on 3 October 1990—becoming a federal parliamentary republic.
url:   https://en.wikipedia.org/wiki?curid=11867
dist:  6.98255

Row 3:
──────
id:    7767
title: FIFA World Cup
text:  After FIFA was founded in 1904, it tried to arrange an international football tournament between nations outside the Olympic framework in Switzerland in 1906. These were very early days for international football, and the official history of FIFA describes the competition as having been a failure.
url:   https://en.wikipedia.org/wiki?curid=11370
dist:  7.5603456
dist:  7.736428

```

As mentioned earlier, the `WHERE` clause can be evaluated using a [post\-filtering or pre\-filtering strategy.](https://clickhouse.com/docs/engines/table-engines/mergetree-family/annindexes#using-a-vector-similarity-index)


Post\-filtering means that the vector similarity index is evaluated first, followed by the filter(s) specified in the WHERE clause. Pre\-filtering means that the filter evaluation order is the other way round.


You can control the filtering strategy using the [`vector_search_filter_strategy`](https://clickhouse.com/docs/operations/settings/settings#vector_search_filter_strategy) setting. By default, this is set to `auto`, which means the query engine will use a heuristic to determine when to apply the filter. We can also set it to `postfilter` or `prefilter` to explicitly choose the strategy.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
