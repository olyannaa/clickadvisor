# ClickHouse Release 24\.1


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.1

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 13, 2024 · 14 minutes read
Welcome to our first release of 2024! ClickHouse version 24\.1 contains **26 new features** 🎁 **22 performance optimisations** 🛷 **47 bug fixes** 🐛



As usual, we're going to highlight a small subset of the new features and improvements in this blog post, but the release also includes the ability to generate shingles, functions for Punycode, quantile sketches from Datadog, compression control when writing files, speeds up for HTTP Output and parallel replicas and memory optimizations for keeper and merges.


In terms of integrations, we were also pleased to [announce the GA of v4 of the ClickHouse Grafana plugin](https://clickhouse.com/blog/clickhouse-grafana-plugin-4-0) with significant improvements focused on using ClickHouse for the Observability use case.


## New Contributors [\#](/blog/clickhouse-release-24-01#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.1! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:



> Aliaksei Khatskevich, Artem Alperin, Blacksmith, Blargian, Eyal Halpern Shalev, Jayme Bird, Lino Uruñuela, Maksim Alekseev, Mark Needham, Mathieu Rey, MochiXu, Nikolay Edigaryev, Roman Glinskikh, Shaun Struwig, Tim Liou, Waterkin, Zheng Miao, avinzhang, chenwei, edpyt, mochi, and sunny19930321\.


Hint: if you’re curious how we generate this list… [click here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).


If you see your name here, please reach out to us...but we will be finding you on Twitter, etc as well.



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.1/#).


## Variant Type [\#](/blog/clickhouse-release-24-01#variant-type)


### Contributed by Pavel Kruglov [\#](/blog/clickhouse-release-24-01#contributed-by-pavel-kruglov)


This release sees the [introduction of the Variant type](https://github.com/ClickHouse/ClickHouse/pull/58047), although it’s still in experimental mode so you’ll need to configure the following settings to have it work.



```
SET allow_experimental_variant_type=1, 
   use_variant_as_common_type = 1;

```

The Variant Type forms part of a longer\-term project to add [semi structured columns](https://github.com/ClickHouse/ClickHouse/issues/54864) to ClickHouse. This type is a discriminated union of nested columns. For example, `Variant(Int8, Array(String))` has every value as either `Int8` or `Array(String)`.


This new type will come in handy when working with maps. For example, imagine that we want to create a map that has values with different types:
This release sees the [introduction of the Variant type](https://github.com/ClickHouse/ClickHouse/pull/58047), although it’s still in experimental mode so you’ll need to configure the following settings to have it work.



```
SELECT
    map('Hello', 1, 'World', 'Mark') AS x,
    toTypeName(x) AS type
FORMAT Vertical;

```

This would usually throw an exception:



```
Received exception:
Code: 386. DB::Exception: There is no supertype for types UInt8, String because some of them are String/FixedString and some of them are not: While processing map('Hello', 1, 'World', 'Mark') AS x, toTypeName(x) AS type. (NO_COMMON_TYPE)

```

Whereas now it returns a Variant type:



```
Row 1:
──────
x:    {'Hello':1,'World':'Mark'}
type: Map(String, Variant(String, UInt8))

```

We can also use this type when reading from CSV files. For example, imagine we have the following file with mixed types:



```
$ cat foo.csv
value
1
"Mark"
2.3

```

When processing the file, we can add a schema inference hint to have it use the Variant type:



```
SELECT *, * APPLY toTypeName
FROM file('foo.csv', CSVWithNames)
SETTINGS 
  schema_inference_make_columns_nullable = 0, 
  schema_inference_hints = 'value Variant(Int, Float32, String)'

┌─value─┬─toTypeName(value)───────────────┐
│ 1     │ Variant(Float32, Int32, String) │
│ Mark  │ Variant(Float32, Int32, String) │
│ 2.3   │ Variant(Float32, Int32, String) │
└───────┴─────────────────────────────────┘

```

At the moment, it doesn’t work with a literal array, so the following throws an exception:



```
SELECT
    arrayJoin([1, true, 3.4, 'Mark']) AS value,
    toTypeName(value)


Received exception:
Code: 386. DB::Exception: There is no supertype for types UInt8, Bool, Float64, String because some of them are String/FixedString and some of them are not: While processing arrayJoin([1, true, 3.4, 'Mark']) AS value, toTypeName(value). (NO_COMMON_TYPE)

```

But you can instead use the array function, and the Variant type will be used:



```
select arrayJoin(array(1, true, 3.4, 'Mark')) AS value, toTypeName(value);


┌─value─┬─toTypeName(arrayJoin([1, true, 3.4, 'Mark']))─┐
│ 1     │ Variant(Bool, Float64, String, UInt8)         │
│ true  │ Variant(Bool, Float64, String, UInt8)         │
│ 3.4   │ Variant(Bool, Float64, String, UInt8)         │
│ Mark  │ Variant(Bool, Float64, String, UInt8)         │
└───────┴───────────────────────────────────────────────┘

```

We can also read the individual values by type from the Variant object:



```
SELECT
    arrayJoin([1, true, 3.4, 'Mark']) AS value,
    variantElement(value, 'Bool') AS bool,
    variantElement(value, 'UInt8') AS int,
    variantElement(value, 'Float64') AS float,
    variantElement(value, 'String') AS str;


┌─value─┬─bool─┬──int─┬─float─┬─str──┐
│ 1     │ ᴺᵁᴸᴸ │    1 │  ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │
│ true  │ true │ ᴺᵁᴸᴸ │  ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │
│ 3.4   │ ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │   3.4 │ ᴺᵁᴸᴸ │
│ Mark  │ ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │  ᴺᵁᴸᴸ │ Mark │
└───────┴──────┴──────┴───────┴──────┘

```

## String Similarity functions [\#](/blog/clickhouse-release-24-01#string-similarity-functions)


### Contributed by prashantr36 \& Robert Schulze [\#](/blog/clickhouse-release-24-01#contributed-by-prashantr36--robert-schulze)


Users new to ClickHouse who experiment with the LIKE operator and match operator are often taken aback by its performance. Depending on the expression being matched this can either be mapped to a regular expression or perform a substring search using an efficient implementation of the rather unknown [Volnitsky's string search algorithm](https://clickhouse.com/codebrowser/ClickHouse/src/Common/Volnitsky.h.html). ClickHouse also utilizes the primary key and [skipping indexes](https://clickhouse.com/docs/en/optimize/skipping-indexes) on a best\-effort basis to accelerate LIKE / regex matching.


While string matching has a number of applications, from data cleaning to searching logs in Observability use cases, it is hard to express a "fuzzy" relationship between two strings as a LIKE pattern or regular expression. Real\-world datasets are often more “messy” and need more flexibility than substring searching offers, e.g., to find misspelled strings or mistakes made as the result of [Optical Character Recognition (OCR)](https://en.wikipedia.org/wiki/Optical_character_recognition).


To address these challenges, a number of well\-known string similarity algorithms exist, including [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance), [Damerau Levenshtein](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance), [Jaro Similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro_similarity), and [Jaro Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro%E2%80%93Winkler_similarity). These are widely used in applications such as spell checking, plagiarism detection, and more broadly in the field of natural language processing, computational linguistics and bioinformatics.


All of these algorithms compute a string similarity ([edit distance](https://en.wikipedia.org/wiki/Edit_distance)) between the search string and a target set of tokens. This metric aims to quantify how dissimilar two strings are to one another by counting the minimum number of operations required to transform one string into the other. Each algorithm differs in the operations it permits to compute this distance, with some also weighting specific operations more than others when computing a count.


In 24\.1, we extend our existing support for [Levenshtein distance](https://clickhouse.com/docs/en/sql-reference/functions/string-functions#editdistance) with new functions for [Damerau Levenshtein](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance), [Jaro Similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro_similarity), and [Jaro Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro%E2%80%93Winkler_similarity).


Possibly the most well\-known algorithm that implements this concept (so much so it's often used interchangeably with edit distance) is the Levenshtein distance. This metric computes the minimum number of single\-character edit operations required to change one word into the other. Edit operations are limited to 3 types:


- **Insertions:** Adding a single character to a string.
- **Deletions:** Removing a single character from a string.
- **Substitutions:** Replacing one character in a string with another character.


The Levenshtein distance between two strings is the minimum number of these operations required to transform one string into the other. Damerau\-Levenshtein builds upon this concept by adding **transpositions,** i.e., the swapping of adjacent characters.


For example, consider the difference between Levenshtein and Damerau Levenshtein for “example” and “exmalpe”.


Using Levenshtein distance, we need 3 operations:
![string_similarity_01.png](/uploads/string_similarity_01_b9500423bb.png)


Confirming with ClickHouse:



```
SELECT levenshteinDistance('example', 'exmalpe') AS d
┌─d─┐
│ 3 │
└───┘

```

Using Damerau Levenshtein distance with need only 2, thanks to transpositions:
![string_similarity_02.png](/uploads/string_similarity_02_56d4a494ca.png)


Confirming the the new ClickHouse [damerauLevenshteinDistance](https://clickhouse.com/docs/en/sql-reference/functions/string-functions#dameraulevenshteindistance) function:



```
SELECT damerauLevenshteinDistance('example', 'exmalpe') AS d
┌─d─┐
│ 2 │
└───┘

```

The [Jaro Similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro_similarity) and [Jaro Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro%E2%80%93Winkler_similarity) algorithms have equivalent functions and offer alternative approaches to computing an edit distance metric by considering both transpositions in addition to the number of common characters with a defined distance position.


For an example of this functionality, and its possible application, let's consider the problem of [typosquatting](https://en.wikipedia.org/wiki/Typosquatting) also known as URL hijacking. This is a form of cybersquatting (sitting on sites under someone else's brand or copyright) that targets Internet users who incorrectly type a website address into their web browser (e.g., “gooogle.com” instead of “google.com”). As these sites are often malicious it might be helpful for a brand to know what are the most commonly accessed domains which hijack their domain.


Detecting these typos is a classic application of string similarity functions. We simply need to find the most popular domains from our target site which have an edit distance of less than N. For this, we need a ranked set of domains. The [Tranco](https://tranco-list.eu/) dataset addresses this very problem by providing a ranked set of the most popular domains.


*Ranked domain lists have applications in web security and Internet measurements but are classically easy to manipulate and influence. Tranco aims to address this and provide up\-to\-date lists with a reproducible method.*


We can insert the full list (inc. subdomains) into ClickHouse, including each sites ranking with two simple commands:



```
CREATE TABLE domains
(
	`domain` String,
	`rank` Float64
)
ENGINE = MergeTree
ORDER BY domain

INSERT INTO domains SELECT
	c2 AS domain,
	1 / c1 AS rank
FROM url('https://tranco-list.eu/download/PNZLJ/full', CSV)

0 rows in set. Elapsed: 4.374 sec. Processed 7.02 million rows, 204.11 MB (1.60 million rows/s., 46.66 MB/s.)
Peak memory usage: 116.77 MiB.

```

Note we use 1/rank as [suggested by Tranco](https://tranco-list.eu/list/PNZLJ/1000000) i.e.


*“The first domain gets 1 point, the second 1/2 points, ..., the last 1/N points, and unranked domains 0 points. This method roughly reflects the observation of Zipf's law and the ''long\-tail effect'' in the distribution of website popularity.”*


The top 10 domains should be familiar:



```
SELECT *
FROM domains
ORDER BY rank DESC
LIMIT 10

┌─domain─────────┬────────────────rank─┐
│ google.com 	 │            	     1 │
│ amazonaws.com  │             	   0.5 │
│ facebook.com   │  0.3333333333333333 │
│ a-msedge.net   │            	  0.25 │
│ microsoft.com  │             	   0.2 │
│ apple.com  	 │ 0.16666666666666666 │
│ googleapis.com │ 0.14285714285714285 │
│ youtube.com	 │           	 0.125 │
│ www.google.com │  0.1111111111111111 │
│ akamaiedge.net │             	   0.1 │
└────────────────┴─────────────────────┘

10 rows in set. Elapsed: 0.313 sec. Processed 7.02 million rows, 254.36 MB (22.44 million rows/s., 813.00 MB/s.)
Peak memory usage: 34.56 MiB.

```

We can test the effectiveness of our string distance functions in identifying typosquatting with a simple query using “facebook.com” as an example:



```
SELECT
	domain,
	levenshteinDistance(domain, 'facebook.com') AS d1,
	damerauLevenshteinDistance(domain, 'facebook.com') AS d2,
	jaroSimilarity(domain, 'facebook.com') AS d3,
	jaroWinklerSimilarity(domain, 'facebook.com') AS d4,
	rank
FROM domains
ORDER BY d1 ASC
LIMIT 10

┌─domain────────┬─d1─┬─d2─┬─────────────────d3─┬─────────────────d4─┬────────────────────rank─┐
│ facebook.com  │  0 │  0 │         	    1  │                  1 │ 	   0.3333333333333333 │
│ facebook.cm   │  1 │  1 │ 0.9722222222222221 │ 0.9833333333333333 │   1.4258771318823703e-7 │
│ acebook.com   │  1 │  1 │ 0.9722222222222221 │ 0.9722222222222221 │ 0.000002449341494539193 │
│ faceboook.com │  1 │  1 │ 0.9188034188034188 │ 0.9512820512820512 │ 0.000002739643462799751 │
│ faacebook.com │  1 │  1 │ 0.9743589743589745 │ 0.9794871794871796 │    5.744693196042826e-7 │
│ faceboom.com  │  1 │  1 │ 0.8838383838383838 │ 0.9303030303030303 │   3.0411914171495823e-7 │
│ facebool.com  │  1 │  1 │ 0.9444444444444443 │ 0.9666666666666666 │    5.228971429945901e-7 │
│ facebooks.com │  1 │  1 │ 0.9743589743589745 │ 0.9846153846153847 │   2.7956239539124616e-7 │
│ facebook.co   │  1 │  1 │ 0.9722222222222221 │ 0.9833333333333333 │  0.00000286769597834316 │
│ facecbook.com │  1 │  1 │ 0.9049145299145299 │ 0.9429487179487179 │    5.685177604948379e-7 │
└───────────────┴────┴────┴────────────────────┴────────────────────┴─────────────────────────┘

10 rows in set. Elapsed: 0.304 sec. Processed 5.00 million rows, 181.51 MB (16.44 million rows/s., 597.38 MB/s.)
Peak memory usage: 38.87 MiB.

```

These seem like credible attempts at typosquatting, although we don’t recommend testing them!


A brand owner may wish to target the most popular of these and have the sites taken down or even attempt to obtain the DNS entry and add a redirect to the correct site. For example, in the case of [facebool.com](http://facebool.com) this is already the case.


Developing a robust metric on which to identify the list to target is well beyond the scope of this blog post. For example purposes, we’ll find all domains with a Damerau\-Levenshtein distance of 1 and order by their actual popularity, excluding any cases where the [first significant subdomain](firstSignificantSubdomain) is “facebook”:



```
SELECT domain, rank, damerauLevenshteinDistance(domain, 'facebook.com') AS d
FROM domains
WHERE (d <= 1) AND (firstSignificantSubdomain(domain) != 'facebook')
ORDER BY rank DESC
LIMIT 10

┌─domain────────┬─────────────────────rank─┬─d─┐
│ facebok.com   │  0.000005683820436744763 │ 1 │
│ facbook.com   │  0.000004044178607104004 │ 1 │
│ faceboook.com │  0.000002739643462799751 │ 1 │
│ acebook.com   │  0.000002449341494539193 │ 1 │
│ faceboo.com   │ 0.0000023974606097221825 │ 1 │
│ facebbook.com │  0.000001914476505544324 │ 1 │
│ facebbok.com  │ 0.0000014273133538010068 │ 1 │
│ faceook.com   │     7.014964321891459e-7 │ 1 │
│ faceboock.com │     6.283680527628087e-7 │ 1 │
│ faacebook.com │     5.744693196042826e-7 │ 1 │
└───────────────┴──────────────────────────┴───┘

10 rows in set. Elapsed: 0.318 sec. Processed 6.99 million rows, 197.65 MB (21.97 million rows/s., 621.62 MB/s.)
Peak memory usage: 12.77 MiB.

```

This seems like a sensible list to start with. Feel free to repeat this with your own domain and let us know if it's useful!


## Vertical algorithm for FINAL with ReplacingMergeTree. [\#](/blog/clickhouse-release-24-01#vertical-algorithm-for-final-with-replacingmergetree)


### Contributed by Duc Canh Le and Joris Giovannangeli [\#](/blog/clickhouse-release-24-01#contributed-by-duc-canh-le-and-joris-giovannangeli)


Last month’s release already [came](https://clickhouse.com/blog/clickhouse-release-23-12#optimizations-for-final) with significant optimizations for SELECT queries with the [FINAL](https://clickhouse.com/docs/en/sql-reference/statements/select/from#final-modifier) modifier. Our current release brings some additional optimization when FINAL is used with the ReplacingMergeTree table engine.


As a reminder, FINAL can be used as a query modifier for tables created with the ReplacingMergeTree, AggregatingMergeTree, and CollapsingMergeTree engines in order to apply missing data transformations on the fly at query time. Since ClickHouse 23\.12, the table data matching a query’s WHERE clause is divided into non\-intersecting and intersecting ranges based on sorting key values. Non\-intersecting ranges are data areas that exist only in a single part and thus need no transformation. Conversely, rows in intersecting ranges potentially exist (based on sorting key values) in multiple parts and require special handling. All non\-intersecting data ranges are processed in parallel as if no FINAL modifier was used in the query. This leaves only the intersecting data ranges, for which the table engine’s merge logic is applied on the fly at query time.


As a reminder, the following diagram shows how such data ranges are merged at query time by a [query pipeline](https://clickhouse.com/blog/clickhouse-release-23-12#optimizations-for-final):  

![final_01.png](/uploads/final_01_27361751d7.png)
Data from the selected data ranges is streamed in physical order at the granularity of [blocks](https://clickhouse.com/docs/en/development/architecture#block) (that combine multiple neighboring rows of a data range) and merged using a [k\-way merge sort](https://en.wikipedia.org/wiki/K-way_merge_algorithm#:~:text=In%20computer%20science%2C%20k%2Dway,sorted%20lists%20greater%20than%20two.) algorithm.


The [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) table engine retains only the most recently inserted version of a row (based on the creation timestamp of its containing part) during the merge, with older versions discarded. To merge rows from the streamed data blocks, the algorithm iterates row\-wise over the block’s columns and copies the data to a new block. In order for the CPU to execute this logic efficiently, blocks need to reside in CPU caches, e.g. L1/L2/L3 caches. The more columns that are contained in a block, the higher the chance that blocks need to be repeatedly evicted from the CPU caches leading to [cache trashing](https://en.wikipedia.org/wiki/Thrashing_(computer_science)). The next diagram illustrates this:
![final_02.png](/uploads/final_02_fe27a5a464.png)
We assume that a CPU cache can hold two blocks from our example data at the same time. When the aforementioned merge algorithm iterates in order over blocks from all three selected matching data ranges to merge their data row\-wise, the runtime will be negatively impacted by the worst\-case scenario of one cache eviction per iteration. This requires data to be copied from the main memory into the CPU cache over and over leading to slower overall performance due to unnecessary memory accesses.


ClickHouse 24\.1 tries to prevent this with a more cache\-friendly query\-time merge algorithm specifically for the ReplacingMergeTree, which works similarly to the [vertical](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part1#more-parts--more-background-part-merges) background merge algorithm. The next diagram sketches how this algorithm works:
![final_03.png](/uploads/final_03_e4e011278b.png)
Instead of copying all column values for each row during merge sort, the merge algorithm is split into two phases. In phase 1, the algorithm merges only data from the sorting key columns. We assume that column c1 is a sorting key column in our example above. Additionally, based on the sorting key column merge, the algorithm creates a temporary row\-level filter bitmap for the data ranges indicating which rows would survive a regular merge. In phase 2, these bitmaps are used to filter the data ranges accordingly and remove all old rows from further processing steps. This filtering happens column\-by\-column and only for all non\-sorting\-key\-columns. Note that both phase 1 and phase 2 individually require less space in CPU caches than the previous 23\.12 merge algorithm, resulting in fewer CPU cache evictions and, thus decreased memory latency.


We demonstrate the new vertical query\-time merge algorithm for FINAL with a concrete example. Like in the previous release post, we slightly [modify](https://gist.github.com/tom-clickhouse/26a97634a427a0e67c7bdfce4011f3d5) the table from the UK property prices [sample dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid) and assume that the table stores data about current property offers instead of previously sold properties. We are using a ReplacingMergeTree table engine, allowing us to update the prices and other features of offered properties by simply inserting a new row with the same sorting key value:



```
CREATE OR REPLACE TABLE uk_property_offers
(
    id UInt32,
    price UInt32,
    date Date,
    postcode1 LowCardinality(String),
    postcode2 LowCardinality(String),
    type Enum8('terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4, 'other' = 0),
    is_new UInt8,
    duration Enum8('freehold' = 1, 'leasehold' = 2, 'unknown' = 0),
    addr1 String,
    addr2 String,
    street LowCardinality(String),
    locality LowCardinality(String),
    town LowCardinality(String),
    district LowCardinality(String),
    county LowCardinality(String)
)
ENGINE = ReplacingMergeTree(date)
ORDER BY (id);

```

Next, we [insert](https://gist.github.com/tom-clickhouse/56ec97a75ebe0af7b64262ae34420142) \~15 million rows into the table.


We run a typical analytics query with the FINAL modifier on ClickHouse version 24\.1 with the new vertical query\-time merge algorithm disabled, selecting the three most expensive primary postcodes:



```
SELECT
    postcode1,
    formatReadableQuantity(avg(price))
FROM uk_property_offers
GROUP BY postcode1
ORDER BY avg(price) DESC
LIMIT 3
SETTINGS enable_vertical_final = 0;

┌─postcode1─┬─formatReadableQuantity(avg(price))─┐
│ W1A       │ 163.58 million                     │
│ NG90      │ 68.59 million                      │
│ CF99      │ 47.00 million                      │
└───────────┴────────────────────────────────────┘

0 rows in set. Elapsed: 0.011 sec. Processed 9.29 thousand rows, 74.28 KB (822.68 thousand rows/s., 6.58 MB/s.)
Peak memory usage: 1.10 MiB.

```

We run the same query with the new vertical query\-time merge algorithm enabled:



```
SELECT
    postcode1,
    formatReadableQuantity(avg(price))
FROM uk_property_offers
GROUP BY postcode1
ORDER BY avg(price) DESC
LIMIT 3
SETTINGS enable_vertical_final = 1;

┌─postcode1─┬─formatReadableQuantity(avg(price))─┐
│ W1A       │ 163.58 million                     │
│ NG90      │ 68.59 million                      │
│ CF99      │ 47.00 million                      │
└───────────┴────────────────────────────────────┘

0 rows in set. Elapsed: 0.004 sec. Processed 9.29 thousand rows, 111.42 KB (2.15 million rows/s., 25.81 MB/s.)
Peak memory usage: 475.21 KiB.

```

Note that the second query run is faster and consumes less memory.


## The world of international domains [\#](/blog/clickhouse-release-24-01#the-world-of-international-domains)


And finally, Alexey did some exploration of the debatable quality of international domains using the new punycode functions added in this release. We’ve cut out that segment of the video below for your viewing pleasure.


[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
