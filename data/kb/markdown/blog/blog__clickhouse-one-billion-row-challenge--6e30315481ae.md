# ClickHouse and The One Billion Row Challenge


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse and The One Billion Row Challenge

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Jan 23, 2024 · 11 minutes read![1_billion_row_challenge_clickhouse.png](/uploads/1_billion_row_challenge_clickhouse_271f68c94f.png)
Earlier this month [Gunnar Morling](https://www.linkedin.com/in/gunnar-morling-2b44b7229/) from Decodable set a challenge for the month of January, which has garnered significant attention \- write a Java program for retrieving temperature measurement values from a 1 billion row text file and calculating the min, mean, and max temperature per weather station. While we are far from experts in Java, as a company that both loves big data and tests of speed, we thought we'd assemble an official ClickHouse response to the challenge!



> While the original challenge remains in Java, Gunnar has opened a ["Show \& Tell"](https://github.com/gunnarmorling/1brc/discussions/categories/show-and-tell) in the form of a Github discussion to allow broader technology contributions. We would also like to thank our community, who [responded to the challenge also](https://github.com/gunnarmorling/1brc/discussions/80).


## Following the rules [\#](/blog/clickhouse-one-billion-row-challenge#following-the-rules)


In responding to this challenge, we've tried to remain in the spirit of the [original challenge](https://github.com/gunnarmorling/1brc#rules-and-limits). We have, therefore, included any processing time or data loading time in our final submission. For example, providing just a response time for a query once the data is loaded into a table and not considering the insert time feels a little like…well, cheating :)


Gunnar is performing testing on a [Hetzner AX161](https://www.hetzner.com/dedicated-rootserver/ax161), limiting execution to 8 cores. As much as I would have liked to procure a dedicated bare metal server just for an internet challenge, it was decided this might be a little excessive. In the spirit of trying to be comparable, our examples use a Hetzer virtual instance (dedicated CPU) with a CCX33 with 8 cores and 32GB of RAM. Although virtual instances, these instances utilize a later AMD EPYC\-Milan Processor with a Zen3 architecture \- later than AMD's EPYC\-Rome 7502P processor offered by the Hetzner AX161\.


## Generate (or just download) the data [\#](/blog/clickhouse-one-billion-row-challenge#generate-or-just-download-the-data)


Users can follow the original instructions [to generate the 1 billion row dataset](https://github.com/gunnarmorling/1brc#running-the-challenge). This requires Java 21 and requires a few commands.


*In writing this blog I discovered [sdkman](https://sdkman.io/jdks) which simplifies installation of Java for those of you who don’t have an existing installation.*


It is, however, quite slow to generate the 13GB measurements.txt file as shown below:



```
# clone and build generation tool. Output omitted.
git clone git@github.com:gunnarmorling/1brc.git
./mvnw clean verify
./create_measurements.sh 1000000000

Created file with 1,000,000,000 measurements in 395955 ms

```

Curious about how fast ClickHouse Local would compare in generating this file, we explored the [source code](https://github.com/gunnarmorling/1brc/blob/main/src/main/java/dev/morling/onebrc/CreateMeasurements.java#L30). The list of stations and their average temperatures are compiled into the code, with random points produced by sampling a Gaussian distribution with a [mean and variance of 10](https://github.com/gunnarmorling/1brc/blob/main/src/main/java/dev/morling/onebrc/CreateMeasurements.java#L29-L32). Extracting the raw station data to a CSV and hosting this on s3, allow us to replicate this logic with an `INSERT INTO FUNCTION FILE`. Note the use of the s3 function to read our stations into a CTE before sampling these results with random functions.



```
INSERT INTO FUNCTION file('measurements.csv', CustomSeparated)
WITH (
	SELECT groupArray((station, avg)) FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/1brc/stations.csv')
) AS averages
SELECT
    	averages[floor(randUniform(1, length(averages)))::Int64].1 as city,
    	round(averages[floor(randUniform(1, length(averages)))::Int64].2 + (10 * SQRT(-2 * LOG(randCanonical(1))) * COS(2 * PI() * randCanonical(2))), 2) as temperature
FROM numbers(1_000_000_000) 
SETTINGS format_custom_field_delimiter=';', format_custom_escaping_rule='Raw'

0 rows in set. Elapsed: 57.856 sec. Processed 1.00 billion rows, 8.00 GB (17.28 million rows/s., 138.27 MB/s.)
Peak memory usage: 36.73 MiB.

```

At 6\.8x the speed, this seemed worth sharing!



> An experienced ClickHouse user might reach for the [randNormal](https://clickhouse.com/docs/en/sql-reference/functions/random-functions#randnormal) function here. Unfortunately, this requires the mean and variance to be constants currently. We therefore use the [randCanonical](http://randCanonical) function and use this to sample the Guassian distribution using a [Muller transform](https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform).


Alternatively, users can simply download a gzip compressed version of our generated file from [here](https://datasets-documentation.s3.eu-west-3.amazonaws.com/1brc/measurements.txt.gz) :)


## ClickHouse local only [\#](/blog/clickhouse-one-billion-row-challenge#clickhouse-local-only)


While many users are familiar with ClickHouse as a real\-time data warehouse deployed on servers, it can also be used as a local binary "Clickhouse Local" for querying files for ad hoc data analysis. This has become an increasingly popular application of ClickHouse since our [blog described this use case just over a year ago](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local).


ClickHouse Local has either a console mode (accessible by running `clickhouse local`), from which tables can be created and interactive query feedback provided, or a command line interface designed for integration with scripts and external tooling. We use the latter to sample our measurements.txt. The setting \`format\_csv\_delimiter\=';" allows the CSV file delimiter to be specified.



```
clickhouse local --query "SELECT city, temperature FROM file('measurements.txt', CSV, 'city String, temperature DECIMAL(8,1)') LIMIT 5 SETTINGS format_csv_delimiter=';'"
Mexicali    44.8
Hat Yai    29.4
Villahermosa    27.1
Fresno    31.7
Ouahigouya    29.3

```

Computing the min, max, and mean of the temperature for each city requires a simple `GROUP BY` query. We utilize `-t` to ensure timing information is included. The challenge requires the output in a specific format:



```
{Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, Accra=-10.1/26.4/66.4, Addis Ababa=-23.7/16.0/67.0, Adelaide=-27.8/17.3/58.5, ...} 

```

To achieve this, we can use the [CustomSeparated](https://clickhouse.com/docs/en/sql-reference/formats#format-customseparated) output format and [format](https://clickhouse.com/docs/en/sql-reference/table-functions/format) function. This avoids the need to use any functions, such as groupArray, which collapses the rows to a single row. Below, we use the console mode of ClickHouse Local.



```
SELECT format('{}={}/{}/{}', city, min(temperature), round(avg(temperature), 2), max(temperature))
FROM file('measurements.txt', CSV, 'city String, temperature DECIMAL(8,1)')
GROUP BY city
ORDER BY city ASC
FORMAT CustomSeparated
SETTINGS 
  format_custom_result_before_delimiter = '{', 
  format_custom_result_after_delimiter = '}', 
  format_custom_row_between_delimiter = ', ', 
  format_custom_row_after_delimiter = '', 
  format_csv_delimiter = ';'

{Abha=-34.6/18/70.3, Abidjan=-22.8/25.99/73.5, Abéché=-25.3/29.4/80.1, Accra=-25.6/26.4/76.8, Addis Ababa=-38.3/16/67, Adelaide=-33.4/17.31/65.5, …}

413 rows in set. Elapsed: 27.671 sec. Processed 1.00 billion rows, 13.79 GB (36.14 million rows/s., 498.46 MB/s.)
Peak memory usage: 47.46 MiB.

```

27\.6s represents our baseline. This compares to the Java baseline, which takes almost 3 minutes to complete on the same hardware.



```
./calculate_average_baseline.sh

real    2m59.364s
user    2m57.511s
sys    0m3.372s

```

## Improving performance [\#](/blog/clickhouse-one-billion-row-challenge#improving-performance)


We can improve the above performance by observing that our CSV file doesn’t use value escaping. The CSV reader is therefore unnecessary \- we can simply read each line as a string and access the relevant substrings using the separator `;`.



```
SELECT format('{}={}/{}/{}', city, min(temperature), round(avg(temperature), 2), max(temperature))
FROM
(
	SELECT
    	substringIndex(line, ';', 1) AS city,
   	substringIndex(line, ';', -1)::Decimal(8, 1) AS temperature
	FROM file('measurements.txt', LineAsString)
)
GROUP BY city
ORDER BY city ASC FORMAT CustomSeparated
SETTINGS 
  format_custom_result_before_delimiter = '{', 
  format_custom_result_after_delimiter = '}', 
  format_custom_row_between_delimiter = ', ', 
  format_custom_row_after_delimiter = '', 
  format_csv_delimiter = ';'

413 rows in set. Elapsed: 19.907 sec. Processed 1.00 billion rows, 13.79 GB (50.23 million rows/s., 692.86 MB/s.)
Peak memory usage: 132.20 MiB.

```

This reduces our execution time to under 20s!


## Testing alternative approaches [\#](/blog/clickhouse-one-billion-row-challenge#testing-alternative-approaches)


Our ClickHouse Local approach performs a complete linear scan of the file. An alternative approach here might be to load the file into a table first before running the query on the file. Maybe unsurprisingly, this offers no real performance benefit as the query effectively performs a 2nd scan of the data. The total load and query time thus exceeds 19 seconds.



```
CREATE TABLE weather
(
	`city` String,
	`temperature` Decimal(8, 1)
)
ENGINE = Memory

INSERT INTO weather SELECT
	city,
	temperature
FROM
(
	SELECT
    	splitByChar(';', line) AS vals,
    	vals[1] AS city,
    	CAST(vals[2], 'Decimal(8, 1)') AS temperature
	FROM file('measurements.txt', LineAsString)
)

0 rows in set. Elapsed: 21.219 sec. Processed 1.00 billion rows, 13.79 GB (47.13 million rows/s., 650.03 MB/s.)
Peak memory usage: 26.16 GiB.

SELECT
	city,
	min(temperature),
	avg(temperature),
	max(temperature)
FROM weather
GROUP BY city
ORDER BY city ASC
SETTINGS max_threads = 8
413 rows in set. Elapsed: 2.997 sec. Processed 970.54 million rows, 20.34 GB (323.82 million rows/s., 6.79 GB/s.)
Peak memory usage: 484.27 KiB.

```


> Note that we use a Memory table here over a classic MergeTree. Given the dataset fits in memory, with the query containing no filters (and thus not benefiting from MergeTree’s sparse index), we can avoid I/O with this engine type.


The above has the obvious benefit of allowing the user to issue arbitrary queries on the data once it's loaded into a table. 
Finally, if our target query computing the min, max, and average is not sufficiently performant, we can move this work to insertion time using a [Materialized View](https://clickhouse.com/blog/using-materialized-views-in-clickhouse). In this case, a Materialized View `weather_mv` computes our statistics as the data is inserted. More specifically, our previous aggregation query executes on blocks of data as it is inserted with the results (effectively [aggregation states](https://clickhouse.com/docs/en/sql-reference/data-types/aggregatefunction)) sent to a target table "weather\_results" using the [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree) table engine. A query on this table will utilize the fact the results have been precomputed, resulting in a significantly faster execution time.


As an optimization, the `weather` table receiving our data can use the Null engine. This will cause the rows to be discarded, saving memory.



```
CREATE TABLE weather
(
    `city` String,
    `temperature` Decimal(8, 1)
)
ENGINE = Null

CREATE TABLE weather_results(
	city String,
	max AggregateFunction(max, Decimal(8, 1)),
	min AggregateFunction(min, Decimal(8, 1)),
	avg AggregateFunction(avg, Decimal(8, 1))
) ENGINE = AggregatingMergeTree ORDER BY tuple()

CREATE MATERIALIZED VIEW weather_mv TO weather_results
AS SELECT city, maxState(temperature) as max, minState(temperature) as min, avgState(temperature) as avg
FROM weather
GROUP BY city

INSERT INTO weather SELECT
	city,
	temperature
FROM
(
	SELECT
    	splitByChar(';', line) AS vals,
    	vals[1] AS city,
    	CAST(vals[2], 'Decimal(8, 1)') AS temperature
	FROM file('measurements.txt', LineAsString)
)

0 rows in set. Elapsed: 26.569 sec. Processed 2.00 billion rows, 34.75 GB (75.27 million rows/s., 1.31 GB/s.)

```

Our subsequent query on the `weather_results` requires the `merge-` functions to combine our aggregation states.



```
SELECT format('{}={}/{}/{}', city, minMerge(min), round(avgMerge(avg), 2), maxMerge(max))
FROM weather_results
GROUP BY city
ORDER BY city ASC
FORMAT CustomSeparated
SETTINGS format_custom_result_before_delimiter = '{', format_custom_result_after_delimiter = '}', format_custom_row_between_delimiter = ', ', format_custom_row_after_delimiter = '', format_csv_delimiter = ';'

413 rows in set. Elapsed: 0.014 sec.

```

This gives us a nominal execution time, which has been reported [by other experiments](https://github.com/gunnarmorling/1brc/discussions/244). However, when combined with our 26s load time, we still fail to beat our simple ClickHouse Local query.


## Conclusion [\#](/blog/clickhouse-one-billion-row-challenge#conclusion)


We have formalized our response to the one billion row challenge. We’ve demonstrated that ClickHouse Local solves the problem on comparable hardware to the challenge rules in around 19s. While it isn’t competitive with specialized solutions, it requires only a few lines of SQL.
We would like to take the opportunity to thank Gunnar for the thought and time he has invested in this challenge.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
