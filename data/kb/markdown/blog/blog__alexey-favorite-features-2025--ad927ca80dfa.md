# Alexey's favorite features of 2025


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Alexey's favorite features of 2025

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Dec 19, 2025 · 15 minutes read
.contributors {
 max\-height: 250px;
 overflow\-y: scroll;
 padding: 1rem;
 border: 1px solid \#444;
 border\-radius: 4px;
 background: transparent;
 position: relative;
 scrollbar\-gutter: stable; /\* reserves space for scrollbar \*/
}

/\* Force scrollbar to always be visible \*/
.contributors::\-webkit\-scrollbar {
 width: 12px;
 display: block;
}

.contributors::\-webkit\-scrollbar\-track {
 background: \#2a2a2a;
 border\-radius: 4px;
}

.contributors::\-webkit\-scrollbar\-thumb {
 background: \#555;
 border\-radius: 4px;
}

.contributors::\-webkit\-scrollbar\-thumb:hover {
 background: \#666;
}

.contributors::after {
 content: \&\#x27;\&\#x27;;
 position: absolute;
 bottom: 0;
 left: 0;
 right: 0;
 height: 40px;
 background: linear\-gradient(to bottom, transparent, \#1a1a1a);
 pointer\-events: none;
}

.contributors p {
 margin: 0;
 line\-height: 1\.6;
 color: \#ccc;
}

We’ve reached the end of the year, which means we’ve had 12 releases, and I thought I'd recap some of my favorite features.


The ClickHouse versions in 2025 have contained 277 new features 🦃, 319 performance optimizations ⌚, and 1,051 bug fixes 🍄


You can see release posts for every release via the links below:  

[25\.1](https://clickhouse.com/blog/clickhouse-release-25-01), [25\.2](https://clickhouse.com/blog/clickhouse-release-25-02), [25\.3 LTS](https://clickhouse.com/blog/clickhouse-release-25-03), [25\.4](https://clickhouse.com/blog/clickhouse-release-25-04), [25\.5](https://clickhouse.com/blog/clickhouse-release-25-05), [25\.6](https://clickhouse.com/blog/clickhouse-release-25-06), [25\.7](https://clickhouse.com/blog/clickhouse-release-25-07), [25\.8 LTS](https://clickhouse.com/blog/clickhouse-release-25-08), [25\.9](https://clickhouse.com/blog/clickhouse-release-25-09), [25\.10](https://clickhouse.com/blog/clickhouse-release-25-10), [25\.11](https://clickhouse.com/blog/clickhouse-release-25-11)


The 25\.12 release blog post will be coming in early 2026!


## New contributors [\#](/blog/alexey-favorite-features-2025#new-contributors)


A special welcome to all the new contributors in 2025! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.


Below are the names of the new contributors this year:



*0xgouda, AbdAlRahman Gad, Agusti Bau, Ahmed Gouda, Albert Chae, Aleksandr Mikhnenko, Aleksei Bashkeev, Aleksei Shadrunov, Alex Bakharew, Alex Shchetkov, Alexander Grueneberg, Alexei Fedotov, Alon Tal, Aly Kafoury, Amol Saini, Andrey Nehaychik, Andrey Volkov, Andrian Iliev, Animesh, Animesh Bilthare, Antony Southworth, Arnaud Briche, Artem Yurov, Austin Bonander, Bulat Sharipov, Casey Leask, ChaiAndCode, Cheryl Tuquib, Cheuk Fung Keith (Chuck) Chow, Chris Crane, Christian Endres, Colerar, Damian Maslanka, Dan Checkoway, Danylo Osipchuk, Dasha Wessely, David E. Wheeler, David K, DeanNeaht, Delyan Kratunov, Denis, Denis K, Denny \[DBA at Innervate], Didier Franc, Diskein, Dmitry Novikov, Dmitry Prokofyev, Dmitry Uvarov, Dominic Tran, Drew Davis, Dylan, Elmi Ahmadov, Engel Danila, Evgenii Leko, Felix Mueller, Fellipe Fernandes, Fgrtue, Filin Maxim, Filipp Abapolov, Frank Rosner, GEFFARD Quentin, Gamezardashvili George, Garrett Thomas, George Larionov, Giampaolo Capelli, Grant Holly, Greg Maher, Grigory Korolev, Guang, Guang Zhao, H0uston, Hans Krutzer, Harish Subramanian, Himanshu Pandey, Huanlin Xiao, HumanUser, Ilya Kataev, Ilya fanyShu, Isak Ellmer, Ivan Nesterov, Jan Rada, Jason Wong, Jesse Grodman, Jia Xu, Jimmy Aguilar Mena, Joel Höner, John Doe, John Zila, Jony Mohajan, Josh, Joshie, Juan A. Pedreira, Julian Meyers, Julian Virguez, Kai Zhu, Kaviraj, Kaviraj Kanagaraj, Ken LaPorte, Kenny Sun, Konstantin Dorichev, KovalevDima, Krishna Mannem, Kunal Gupta, Kyamran, Leo Qu, Lin Zhong, Lonny Kapelushnik, Lucas Pelecq, Lucas Ricoy, Luke Gannon, László Várady, Manish Gill, Manuel, Manuel Raimann, Mark Roberts, Marta Paes, Maruth Goyal, Max Justus Spransy, Melvyn Peignon, Michael Anastasakis, Michael Ryan Dempsey, Michal Simon, Mikhail Kuzmin, Mikhail Tiukavkin, Mishmish Dev, Mithun P, Mohammad Lareb Zafar, Mojtaba Ghahari, Muzammil Abdul Rehman, NamHoaiNguyen, Narasimha Pakeer, Neerav, Nick, Nihal Z., Nihal Z. Miaji, Nikita Vaniasin, Nikolai Ryzhov, Nikolay Govorov, NilSper, Nils Sperling, Oleg Doronin, Olli Draese, Onkar Deshpande, ParvezAhamad Kazi, Patrick Galbraith, Paul Lamb, Pavel Shutsin, Pete Hampton, Philip Dubé, Q3Master, Rafael Roquetto, Rajakavitha Kodhandapani, Raphaël Thériault, Raufs Dunamalijevs, Renat Bilalov, RinChanNOWWW, Rishabh Bhardwaj, Roman Lomonosov, Ronald Wind, Roy Kim, RuS2m, Rui Zhang, Sachin Singh, Sadra Barikbin, Sahith Vibudhi, Saif Ullah, Saksham10\-11, Sam Radovich, Samay Sharma, Sameer Tamsekar, San Tran, Sante Allegrini, Saurav Tiwary, Sav, Sergey, Sergey Lokhmatikov, Sergio de Cristofaro, Shahbaz Aamir, Shakhaev Kyamran, Shankar Iyer, Shaohua Wang, Shiv, Shivji Kumar Jha, Shreyas Ganesh, Shruti Jain, Somrat Dutta, Spencer Torres, Stephen Chi, Sumit, Surya Kant Ranjan, Tanin Na Nakorn, Tanner Bruce, Taras Polishchuk, Tariq Almawash, Todd Dawson, Todd Yocum, Tom Quist, Vallish, Vico.Wu, Ville Ojamo, Vlad Buyval, Vladimir Baikov, Vladimir Zhirov, Vladislav Gnezdilov, Vrishab V Srivatsa, Wudidapaopao, Xander Garbett, Xiaozhe Yu, Yanghong Zhong, YjyJeff, Yunchi Pang, Yutong Xiao, Zacharias Knudsen, Zakhar Kravchuk, Zicong Qu, Zypperia, abashkeev, ackingliu, albertchae, alburthoffman, alistairjevans, andrei tinikov, arf42, c\-end, caicre, chhetripradeep, cjw, codeworse, copilot\-swe\-agent\[bot], craigfinnelly, cuiyanxiang, dakang, ddavid, demko, dollaransh17, dorki, e\-mhui, f.abapolov, f2quantum, felipeagfranceschini, fhw12345, flozdra, flyaways, franz101, garrettthomas, gvoelfin, haowenfeng, haoyangqian, harishisnow, heymind, inv2004, jemmix, jitendra1411, jonymohajanGmail, jskong1124, kirillgarbar, krzaq, lan, lomik, luxczhang, mekpro, mkalfon, mlorek, morsapaes, neeravsalaria, nihalzp, ollidraese, otlxm, pheepa, polako, pranav mehta, r\-a\-sattarov, rajatmohan22, randomizedcoder dave.seddon.ca@gmail.com, restrry, rickykwokmeraki, rienath, romainsalles, roykim98, samay\-sharma, saurabhojha, sdairs, shanfengp, shruti\-jain11, sinfillo, somrat.dutta, somratdutta, ssive7b, sunningli, talmawash, tdufour, tiwarysaurav, tombo, travis, wake\-up\-neo, wh201906, wujianchao5, xander, xiaohuanlin, xin.yan, yahoNanJing, yangjiang, yanglongwei, yangzhong, yawnt, ylw510, zicongqu, zlareb1, zouyunhe, \|2ustam, Андрей Курганский, Артем Юров, 思维* 



Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).


I recently presented my favorite features at the ClickHouse San Francisco meetup \- you can also [view the slides from the presentation](https://presentations.clickhouse.com/2025-meetupsf-3/top_features/#23).


And now for my favorite features of the year.


## Lightweight updates [\#](/blog/alexey-favorite-features-2025#lightweight-updates)


Standard SQL UPDATE statements at scale, also known as lightweight updates, were [introduced in ClickHouse 25\.7](https://clickhouse.com/blog/clickhouse-release-25-07#lightweight-updates).



They’re powered by a [lightweight patch\-part mechanism](https://clickhouse.com/docs/sql-reference/statements/update), and, unlike classic mutations, which rewrite full columns, these updates write only tiny “patch parts” that slide in instantly with minimal impact on query performance.


If we want to update a row, we can now write a query like this:



```

```
1UPDATE orders
2SET discount = 0.2
3WHERE quantity >= 40;
```

```

Behind the scenes, ClickHouse inserts a compact patch part that will patch data parts during merges, **applying only the changed data**.


![Blog-release-25.7.001.png](/uploads/Blog_release_25_7_001_d9f45d41b0.png)
Merges were already running in the background anyway, but now apply patch parts, updating the base data efficiently as parts are merged.


Updates show up right away \- not\-yet\-merged patch parts are matched and applied independently for each data range in each data stream in a surgical, targeted way, ensuring that updates are applied correctly without disrupting parallelism:


![Blog-release-25.7.002.png](/uploads/Blog_release_25_7_002_ec850c7205.png)
Similarly, you can delete data using standard SQL syntax:



```

```
1DELETE FROM orders
2WHERE order_id = 1001
3AND item_id = 'mouse';
```

```

ClickHouse creates a patch part that sets `_row_exists = 0` for the deleted rows. The row is then dropped during the next background merge.


You can read more about this feature in the [ClickHouse 25\.7 release blog post](https://clickhouse.com/blog/clickhouse-release-25-07#lightweight-updates). And if you want to go even deeper, see Tom Schreiber’s 3\-part blog series on fast UPDATEs in ClickHouse:


- [Part 1: Purpose\-built engines](https://clickhouse.com/blog/updates-in-clickhouse-1-purpose-built-engines)  

Learn how ClickHouse sidesteps slow row\-level updates using insert\-based engines, such as ReplacingMergeTree, CollapsingMergeTree, and CoalescingMergeTree.
- [Part 2: Declarative SQL\-style UPDATEs](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates)  

Explore how we brought standard UPDATE syntax to ClickHouse with minimal overhead using patch parts.
- [Part 3: Benchmarks](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks)  

See how fast it really is. We benchmarked every approach, including declarative UPDATEs, and got up to 1,000× speedups.
- [Bonus: ClickHouse vs PostgreSQL](https://clickhouse.com/blog/update-performance-clickhouse-vs-postgresql)  

We put ClickHouse’s new SQL UPDATEs head\-to\-head with PostgreSQL on identical hardware and data parity on point updates, up to 4,000× faster on bulk changes.


## Data Lake support [\#](/blog/alexey-favorite-features-2025#data-lake-support)


We've known for several years that open table formats, such as Iceberg and Delta Lake, have been gaining significant traction in the data ecosystem.


Support for querying Iceberg directly was introduced in version 23\.2, but by the end of 2024, it was clear that comprehensive catalog layer support was essential for proper integration with these table formats.


Throughout 2025, we’ve rapidly expanded our data lake capabilities. The year started with support for REST and Polaris catalogs , and by the end of the year, ClickHouse has added database engines for major catalog systems:


- [REST](https://clickhouse.com/docs/use-cases/data-lake/rest-catalog) and Polaris catalogs (since [24\.12](https://clickhouse.com/blog/clickhouse-release-24-12#iceberg-rest-catalog-and-schema-evolution-support))
- [Unity catalog](https://clickhouse.com/docs/use-cases/data-lake/unity-catalog) (since [25\.3](https://clickhouse.com/blog/clickhouse-release-25-03#aws-glue-and-unity-catalogs))
- [Glue catalog](https://clickhouse.com/docs/use-cases/data-lake/glue-catalog) (since [25\.3](https://clickhouse.com/blog/clickhouse-release-25-03#aws-glue-and-unity-catalogs))
- Hive Metastore catalog (since [25\.5](https://clickhouse.com/blog/clickhouse-release-25-05#hive-metastore-catalog-for-iceberg))
- [Microsoft OneLake](https://clickhouse.com/docs/use-cases/data-lake/onelake-catalog) (since [25\.11](https://presentations.clickhouse.com/2025-release-25.11/#27))


The transformation in data lake functionality between versions 24\.11 and 25\.8 was substantial. The table below shows how ClickHouse went from minimal data lake support to comprehensive feature coverage:




| Feature | ClickHouse 24\.11 | ClickHouse 25\.8 |
| --- | --- | --- |
| Catalog (Unity, Rest catalog, Polaris, ...) | ❌ | ✅ |
| Partitioning Pruning | ❌ | ✅ |
| Statistics Based Pruning | ❌ | ✅ |
| Cache Improvement | ❌ | ✅ |
| Schema Evolution | ❌ | ✅ |
| Time Travel | ❌ | ✅ |
| Introspection | ❌ | ✅ |
| Positional Deletes | ❌ | ✅ |
| Equality Deletes | ❌ | ✅ |
| Write support | ❌ | ✅ |


## Text index [\#](/blog/alexey-favorite-features-2025#text-index)


The journey to full\-text search in ClickHouse has been a long and winding one. Development kicked off in 2022, with Harry Lee and Larry Luo creating a prototype in 2023\. Work on this feature didn't progress continuously from there \- it happened in fits and starts over the following years.


Eventually, the feature was completely rewritten to make it production\-ready. It was introduced as an experimental feature in [version 25\.9](https://clickhouse.com/blog/clickhouse-release-25-09#a-new-text-index) and will be promoted to beta status in ClickHouse 25\.12\.


The text index can be defined on a column in a table like this:



```

```
1CREATE TABLE hackernews
2(
3    `id` Int64,
4    `deleted` Int64,
5    `type` String,
6    `by` String,
7    `time` DateTime64(9),
8    `text` String,
9    `dead` Int64,
10    `parent` Int64,
11    `poll` Int64,
12    `kids` Array(Int64),
13    `url` String,
14    `score` Int64,
15    `title` String,
16    `parts` Array(Int64),
17    `descendants` Int64,
18    INDEX inv_idx(text)
19    TYPE text(tokenizer = 'splitByNonAlpha')
20    GRANULARITY 128
21)
22ORDER BY time;
```

```

It will then be available to speed up queries that use the following text functions:



```

```
1SELECT by, count()
2FROM hackernews
3WHERE hasToken(text, 'OpenAI')
4GROUP BY ALL
5ORDER BY count() DESC
6LIMIT 10;
```

```


```

```
1SELECT by, count()
2FROM hackernews
3WHERE hasAllTokens(text, ['OpenAI', 'Google'])
4GROUP BY ALL
5ORDER BY count() DESC
6LIMIT 10;
```

```


```

```
1SELECT by, count()
2FROM hackernews
3WHERE hasAnyTokens(text, ['OpenAI', 'Google'])
4GROUP BY ALL
5ORDER BY count() DESC
6LIMIT 10;
```

```

We tested the text index on a 50 TB logs dataset and it performs well at scale. You can see a comparison of using no index, a bloom filter, and the text index to run a query in the animation below:

Loading video...And the following chart shows the relative performance of the three approaches:


![FTS Presentation.png](/uploads/FTS_Presentation_74951aadb9.png)
## Vector index [\#](/blog/alexey-favorite-features-2025#vector-index)


Vector search in ClickHouse has also been years in the making. The first experimental version appeared back in 22\.9, thanks to the work of Arthur Filatenkov, Vladimir Makarov, Danila Mishin, Nikita Vasilenko, Alexander Piachonkin, Nikita Evsiukov, and Hakob Sagatelyan.


A year later, in 23\.8, Davit Vardanyan integrated the USearch library, bringing more robust vector similarity capabilities to the platform.


The real momentum picked up this year. 25\.1 introduced significant performance improvements to vector indices, courtesy of Shankar Iyer, Robert Schulze, and Michael Kolupaev. By 25\.5, the feature hit beta status with the addition of prefiltering, postfiltering, and rescoring \- critical features for production use cases \- developed by Shankar Iyer and Robert Schulze.


Finally, in 25\.8, vector search reached general availability with index\-only reading, fetch multiplier support, and binary quantization for even better performance and efficiency.


At the time of writing, the only supported approximate search method is HNSW, a popular and state\-of\-the\-art technique for approximate vector search based on hierarchical proximity graphs. We can define a vector index on a column like this:



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

We can then write a query that uses the index:



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

Another interesting development in this area is the introduction of [QBit](https://clickhouse.com/blog/clickhouse-release-25-10#qbit-data-type) by Raufs Dunamalijevs, a data type for vector embeddings that enables runtime tuning of search precision.


We can create a column that uses this type:



```

```
1CREATE TABLE vectors (
2    id UInt64, name String, ...
3    vec QBit(BFloat16, 1536)
4) ORDER BY ();
```

```

And at query time, we specify how many (most significant) bits to take:



```

```
1SELECT id, name FROM vectors
2ORDER BY L2DistanceTransposed(vector, target, 10)
3LIMIT 10;
```

```

## Query condition cache [\#](/blog/alexey-favorite-features-2025#query-condition-cache)


Introduced in ClickHouse 25\.3, the [query condition cache](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache) enables ClickHouse to remember which ranges of granules in data parts satisfy the condition in the WHERE clause and reuse this information as an ephemeral index for subsequent queries.



This makes it a valuable addition for real\-world workloads, such as dashboards, alerts, or interactive analytics, which often run the same filters (WHERE conditions) repeatedly against the same data or against continuously growing data, as in observability scenarios.


This cache is [enabled by default](https://clickhouse.com/docs/operations/settings/settings#use_query_condition_cache), and in our experiments, it results in an order of magnitude improvement in query performance.


We ran the following query on a BlueSky dataset of 100 million rows with and without the query condition cache:



```

```
1SELECT count()
2FROM bluesky
3WHERE
4    data.kind = 'commit'
5    AND data.commit.operation = 'create'
6    AND data.commit.collection = 'app.bsky.feed.post'
7    AND data.commit.record.text LIKE '%????%'
```

```

On the first run, the query takes 0\.481 sec, but subsequent runs with the query condition cache enabled take around 0\.037 sec, which is more than 10 times quicker.


## Join reordering [\#](/blog/alexey-favorite-features-2025#join-reordering)


[ClickHouse 25\.9](https://clickhouse.com/blog/clickhouse-release-25-09#join-reordering) introduced a long\-awaited feature for many ClickHouse users \- automatic global join reordering.


ClickHouse can now reorder complex join graphs spanning dozens of tables across the most common join types (inner, left outer, right outer, cross, semi, and anti). Automatic global join reordering uses the fact that joins between more than two tables are [associative](https://en.wikipedia.org/wiki/Associative_property).


Two new settings control the global join reordering:


- [query\_plan\_optimize\_join\_order\_limit](https://clickhouse.com/docs/operations/settings/settings#query_plan_optimize_join_order_limit) \- Value is the max number of tables to apply the reordering to.
- [allow\_statistics\_optimize](https://clickhouse.com/docs/operations/settings/settings#allow_statistics_optimize) \- Allows using statistics to optimize join order


We tested this functionality out on a query that joins six tables from the TPC\-H join benchmark. The query was \~1,450 times faster than before and used \~25 times less memory.


You can read more about join reordering in the [25\.9 release post](https://clickhouse.com/blog/clickhouse-release-25-09#join-reordering).


## Lazy reading/materialization [\#](/blog/alexey-favorite-features-2025#lazy-readingmaterialization)


ClickHouse [25\.4](https://clickhouse.com/blog/clickhouse-release-25-04#lazy-materialization) introduced [lazy materialization](https://clickhouse.com/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization). This means that instead of reading data for a column, we track the information about what data should be read, and then read the data only when needed.


The column values can be carried around, filtered, but not used in calculations before the latest stages of the query pipeline.



We tried this functionality out on a query that finds the Amazon reviews with the highest number of helpful votes, returning the top 3 along with their title, headline, and full text.



```

```
1SELECT helpful_votes, product_title, review_headline, review_body
2FROM amazon.amazon_reviews
3ORDER BY helpful_votes DESC
4LIMIT 3
5FORMAT Null;
```

```

Without lazy materialization, this query took 219 seconds. With lazy materialization, it took 0\.14 seconds. That's a 1,576 times speedup, and it also used 40 times less I/O and 300 times less memory.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
