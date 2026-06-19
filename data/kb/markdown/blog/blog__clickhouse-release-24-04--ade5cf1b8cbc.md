# ClickHouse Release 24\.4


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.4

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)May 5, 2024 · 18 minutes readAnother month goes by, which means it’s time for another release!



ClickHouse version 24\.3 contains **13 new features** 🎁 **16 performance optimisations** 🛷 **65 bug fixes** 🐛



## New Contributors [\#](/blog/clickhouse-release-24-04#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.4! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:


*Alexey Katsman, Anita Hammer, Arnaud Rocher, Chandre Van Der Westhuizen, Eduard Karacharov, Eliot Hautefeuille, Igor Markelov, Ilya Andreev, Jhonso7393, Joseph Redfern, Josh Rodriguez, Kirill, KrJin, Maciej Bak, Murat Khairulin, Paweł Kudzia, Tristan, dilet6298, loselarry*


Hint: if you’re curious how we generate this list… [click here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.4/).


## Recursive CTEs [\#](/blog/clickhouse-release-24-04#recursive-ctes)


### Contributed by Maksim Kita [\#](/blog/clickhouse-release-24-04#contributed-by-maksim-kita)


[SQL](https://en.wikipedia.org/wiki/SQL:1999) introduced recursive common table expressions (CTEs) for [hierarchical queries](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL), making SQL a [Turing\-complete](https://en.wikipedia.org/wiki/Turing_completeness) programming language.


So far, ClickHouse has supported hierarchical queries by utilizing [hierarchical dictionaries](https://clickhouse.com/docs/en/sql-reference/dictionaries#hierarchical-dictionaries). With our new query analysis and optimization infrastructure, now [enabled](https://clickhouse.com/blog/clickhouse-release-24-03#analyzer-enabled-by-default) by default, we finally have everything in place to introduce long\-awaited and powerful features like recursive CTEs.


ClickHouse recursive CTEs [have](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL) the standard SQL syntax and [pass](https://www.youtube.com/live/dtUqgcfOGmE?si=Dzg93iQE3a5XCutn&t=2813) all PostgreSQL tests for recursive CTEs. Furthermore, ClickHouse now has better support for recursive CTEs than PostgreSQL. Inside the CTE’s UNION ALL clause’s bottom part, multiple (arbitrarily complex) queries can be specified, the CTE base table can be referenced multiple times, etc.


Recursive CTEs can solve hierarchical problems elegantly and simply. For example, they can easily answer reachability questions for [hierarchical data models](https://en.wikipedia.org/wiki/Hierarchical_database_model) (e.g. trees and graphs) .



> Specifically, recursive CTEs can calculate [transitive closures](https://en.wikipedia.org/wiki/Transitive_closure) of relations. With the [London Underground](https://en.wikipedia.org/wiki/London_Underground)'s tube connections as a binary relation example, you can imagine the set of all directly connected tube stations: `Oxford Circus -> Bond Street`, `Bond Street -> Marble Arch`, `Marble Arch -> Lancaster Gate`, and so on. The transitive closure of those connections includes all possible connections between these stations, e.g. `Oxford Circus -> Lancaster Gate`, `Oxford Circus -> Marble Arch`, and so on.


To demonstrate this, we use an adapted version of a [data set](https://github.com/nicola/tubemaps/blob/master/datasets/london.connections.csv) modeling all London Underground connections where each entry represents two directly connected stations. Then, we can use a recursive CTE to answer questions like this easily:


**When starting at [Oxford Circus station](https://tfl.gov.uk/tube/stop/940GZZLUOXC/oxford-circus-underground-station) on the [Central Line](https://www.london-tube-map.info/central-line/), which stations can we reach with a maximum of five stops?**


We visualize this with a screenshot of the Central Line station map:


![unnamed2.png](/uploads/unnamed2_16f66d4149.png)
We create a ClickHouse table for storing the London Underground connections data set:



```
CREATE OR REPLACE TABLE Connections (
    Station_1 String,
    Station_2 String,
    Line String,
    PRIMARY KEY(Line, Station_1, Station_2)
);

```


> An attentive reader will have recognized that we didn’t specify a table engine in the DDL statement above (this is possible since ClickHouse [24\.3](https://clickhouse.com/docs/en/whats-new/changelog#improvement-1)) and used PRIMARY KEY syntax in the column definition (possible since ClickHouse [23\.7](https://clickhouse.com/docs/en/whats-new/changelog/2023#new-feature-5)). With that, not just recursive CTEs but also our ClickHouse table DDL syntax is standard\-compliant with SQL.


By utilizing the [url table function](https://clickhouse.com/docs/en/sql-reference/table-functions/url) and [automatic schema inference](https://clickhouse.com/docs/en/interfaces/schema-inference), we load the data set directly into our table:



```
INSERT INTO Connections
SELECT * FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/london_underground/london_connections.csv')

```

This is how the loaded data looks like:



```
SELECT
    *
FROM Connections
WHERE Line = 'Central Line'
ORDER BY Station_1, Station_2
LIMIT 10;

    ┌─Station_1──────┬─Station_2────────┬─Line─────────┐
 1. │ Bank           │ Liverpool Street │ Central Line │
 2. │ Bank           │ St. Paul's       │ Central Line │
 3. │ Barkingside    │ Fairlop          │ Central Line │
 4. │ Barkingside    │ Newbury Park     │ Central Line │
 5. │ Bethnal Green  │ Liverpool Street │ Central Line │
 6. │ Bethnal Green  │ Mile End         │ Central Line │
 7. │ Bond Street    │ Marble Arch      │ Central Line │
 8. │ Bond Street    │ Oxford Circus    │ Central Line │
 9. │ Buckhurst Hill │ Loughton         │ Central Line │
10. │ Buckhurst Hill │ Woodford         │ Central Line │
    └────────────────┴──────────────────┴──────────────┘

```

Now, we use a recursive CTE to answer the above question:



```
WITH RECURSIVE Reachable_Stations AS
(
    SELECT Station_1, Station_2, Line, 1 AS stops
    FROM Connections
    WHERE Line = 'Central Line'
      AND Station_1 = 'Oxford Circus'
    UNION ALL
    SELECT rs.Station_1, c.Station_2, c.Line, rs.stops + 1 AS stops
    FROM Reachable_Stations AS rs, Connections AS c
    WHERE rs.Line = c.Line
      AND rs.Station_2 = c.Station_1
      AND rs.stops < 5
)
SELECT DISTINCT (Station_1, Station_2, stops) AS connections
FROM Reachable_Stations
ORDER BY stops ASC;

```

This is the result:



```
    ┌─connections────────────────────────────────┐
 1. │ ('Oxford Circus','Bond Street',1)          │
 2. │ ('Oxford Circus','Tottenham Court Road',1) │
 3. │ ('Oxford Circus','Marble Arch',2)          │
 4. │ ('Oxford Circus','Oxford Circus',2)        │
 5. │ ('Oxford Circus','Holborn',2)              │
 6. │ ('Oxford Circus','Bond Street',3)          │
 7. │ ('Oxford Circus','Lancaster Gate',3)       │
 8. │ ('Oxford Circus','Tottenham Court Road',3) │
 9. │ ('Oxford Circus','Chancery Lane',3)        │
10. │ ('Oxford Circus','Marble Arch',4)          │
11. │ ('Oxford Circus','Oxford Circus',4)        │
12. │ ('Oxford Circus','Queensway',4)            │
13. │ ('Oxford Circus','Holborn',4)              │
14. │ ('Oxford Circus','St. Paul\'s',4)          │
15. │ ('Oxford Circus','Bond Street',5)          │
16. │ ('Oxford Circus','Lancaster Gate',5)       │
17. │ ('Oxford Circus','Tottenham Court Road',5) │
18. │ ('Oxford Circus','Notting Hill Gate',5)    │
19. │ ('Oxford Circus','Chancery Lane',5)        │
20. │ ('Oxford Circus','Bank',5)                 │
    └────────────────────────────────────────────┘

```

A recursive CTE has a simple iterations\-based execution logic that behaves like a recursive self\-self\-...\-self\-join that stops self\-joining once no new join partners are found or an abort condition is met. For this, our CTE above starts with executing the `UNION ALL` clause’s top part, querying our `Connections` table for all stations directly connected to the `Oxford Circus` station on the `Central Line`. This will return a table that is bound to the `Reachable_Stations` identifier and looks like this:



```
 Initial Reachable_Stations table content
 ┌─Station_1─────┬─Station_2────────────┐
 │ Oxford Circus │ Bond Street          │
 │ Oxford Circus │ Tottenham Court Road │
 └───────────────┴──────────────────────┘

```

From now on, only the CTE’s `UNION ALL` clause’s bottom part will be executed (recursively):


`Reachable_Stations` is joined with the `Connections` table to find the following join partners within the `Connections` table whose `Station_1` value matches the `Station_2` value of `Reachable_Stations`:



```
Connections table join partners

┌─Station_1────────────┬─Station_2─────┐
│ Bond Street          │ Marble Arch   │
│ Bond Street          │ Oxford Circus │
│ Tottenham Court Road │ Holborn       │
│ Tottenham Court Road │ Oxford Circus │
└──────────────────────┴───────────────┘

```

Via the `UNION ALL` clause, these join partners are added to the `Reachable_Stations` table (with the `Station_1` column replaced by `Oxford Circus`), and the first iteration of our recursive CTE is complete. In the next iteration, by executing the CTE’s `UNION ALL` clause’s bottom part, `Reachable_Stations` is again joined with the `Connections` table to identify (and add to `Reachable_Stations`) all NEW join partners within the `Connections` table whose `Station_1` value matches the `Station_2` value of `Reachable_Stations`. These iterations continue until no new join partners are found or a stop condition is met. In our query above, we use a `stops` counter to abort the CTE’s iteration cycle when our specified number of allowed stops from the start station is reached.


Note that the result lists `Oxford Circus` as a reachable station from `Oxford Circus` with 2 and 4 stops. That is theoretically correct but not very practical, and caused by the fact that our query doesn’t mind any directions or cycles. We leave this as a fun exercise for the reader.


As a bonus question, we are interested in how many stops it takes from the `Oxford Circus` station on the `Central Line` to reach the `Stratford` station. We visualize this again with the Central Line map:


![ (5).png](/uploads/5_406bc6cf00.png)
For this, we just need to modify our recursive CTE’s abort condition (stopping the CTE’s join iterations once a join partner with `Stratford` as the target station got added to the CTE table):



```
WITH RECURSIVE Reachable_Stations AS
(
    SELECT Station_1, Station_2, Line, 1 AS stops
    FROM Connections
    WHERE Line = 'Central Line'
      AND Station_1 = 'Oxford Circus'
  UNION ALL
    SELECT rs.Station_1 c.Station_2, c.Line, rs.stops + 1 AS stops
    FROM Reachable_Stations AS rs, Connections AS c
    WHERE rs.Line = c.Line
      AND rs.Station_2 = c.Station_1
      AND 'Stratford' NOT IN (SELECT Station_2 FROM Reachable_Stations)
)
SELECT max(stops) as stops
FROM Reachable_Stations;

```

The result shows that it would take 9 stops, which matches the Central Line’s map plan above:



```
   ┌─stops─┐
1. │     9 │
   └───────┘

```

A recursive CTE could easily answer more interesting questions about this data set. For example, the relative connection times in the [original version](https://github.com/nicola/tubemaps/blob/master/datasets/london.connections.csv) of the data set could be used to discover the fastest (and across tube lines) connection from `Oxford Circus` station to `Heathrow Airport` station. Stay tuned for the solution to this in a separate follow\-up post.


## QUALIFY [\#](/blog/clickhouse-release-24-04#qualify)


### Contributed by Maksim Kita [\#](/blog/clickhouse-release-24-04#contributed-by-maksim-kita-1)


Another feature added in this release is the `QUALIFY` clause, which lets us filter on the value of window functions.


We will see how to use it with help from the [Window Functions \- Rankings](https://github.com/ClickHouse/examples/tree/main/LearnClickHouseWithMark/WindowFunctions-Ranking) example. The dataset contains hypothetical football players and their salaries. We can import it into ClickHouse like this:



```
CREATE TABLE salaries ORDER BY team AS
FROM url('https://raw.githubusercontent.com/ClickHouse/examples/main/LearnClickHouseWithMark/WindowFunctions-Aggregation/data/salaries.csv')
SELECT * EXCEPT (weeklySalary), weeklySalary AS salary
SETTINGS schema_inference_make_columns_nullable=0;

```

Let’s have a quick look at the data in the `salaries` table:



```
SELECT * FROM salaries LIMIT 5;

```


```
   ┌─team──────────────┬─player───────────┬─position─┬─salary─┐
1. │ Aaronbury Seekers │ David Morton     │ D        │  63014 │
2. │ Aaronbury Seekers │ Edwin Houston    │ D        │  51751 │
3. │ Aaronbury Seekers │ Stephen Griffith │ M        │ 181825 │
4. │ Aaronbury Seekers │ Douglas Clay     │ F        │  73436 │
5. │ Aaronbury Seekers │ Joel Mendoza     │ D        │ 257848 │
   └───────────────────┴──────────────────┴──────────┴────────┘

```

Next, let’s compute the salary rank by position for each player. I.e., how much are they paid relative to people who play in the same position?



```
SELECT player, team, position AS pos, salary,
       rank() OVER (PARTITION BY position ORDER BY salary DESC) AS posRank
FROM salaries
ORDER BY salary DESC
LIMIT 5

```


```
   ┌─player──────────┬─team────────────────────┬─pos─┬─salary─┬─posRank─┐
1. │ Robert Griffin  │ North Pamela Trojans    │ GK  │ 399999 │       1 │
2. │ Scott Chavez    │ Maryhaven Generals      │ M   │ 399998 │       1 │
3. │ Dan Conner      │ Michaelborough Rogues   │ M   │ 399998 │       1 │
4. │ Nathan Thompson │ Jimmyville Legionnaires │ D   │ 399998 │       1 │
5. │ Benjamin Cline  │ Stephaniemouth Trojans  │ D   │ 399998 │       1 │
   └─────────────────┴─────────────────────────┴─────┴────────┴─────────┘

```

Let’s say we want to filter `posRank` to return only the top 3 paid players by position. We might try to add a `WHERE` clause to do this:



```
SELECT player, team, position AS pos, salary,
       rank() OVER (PARTITION BY position ORDER BY salary DESC) AS posRank
FROM salaries
WHERE posRank <= 3
ORDER BY salary DESC
LIMIT 5

```


```
Received exception:
Code: 184. DB::Exception: Window function rank() OVER (PARTITION BY position ORDER BY salary DESC) AS posRank is found in WHERE in query. (ILLEGAL_AGGREGATION)

```

We can’t do this as the `WHERE` clause runs before the window function has been evaluated. Before the 24\.4 release, we could work around this problem by introducing a CTE:



```
WITH salaryRankings AS
    (
        SELECT player, 
               if(
                 length(team) <=25, 
                 team, 
                 concat(substring(team, 5), 1, '...')
               ) AS team, 
               position AS pos, salary,
               rank() OVER (
                 PARTITION BY position 
                 ORDER BY salary DESC
               ) AS posRank
        FROM salaries
        ORDER BY salary DESC
    )
SELECT *
FROM salaryRankings
WHERE posRank <= 3

```


```
    ┌─player────────────┬─team────────────────────┬─pos─┬─salary─┬─posRank─┐
 1. │ Robert Griffin    │ North Pamela Trojans    │ GK  │ 399999 │       1 │
 2. │ Scott Chavez      │ Maryhaven Generals      │ M   │ 399998 │       1 │
 3. │ Dan Conner        │ Michaelborough Rogue... │ M   │ 399998 │       1 │
 4. │ Benjamin Cline    │ Stephaniemouth Troja... │ D   │ 399998 │       1 │
 5. │ Nathan Thompson   │ Jimmyville Legionnai... │ D   │ 399998 │       1 │
 6. │ William Rubio     │ Nobleview Sages         │ M   │ 399997 │       3 │
 7. │ Juan Bird         │ North Krystal Knight... │ GK  │ 399986 │       2 │
 8. │ John Lewis        │ Andreaberg Necromanc... │ D   │ 399985 │       3 │
 9. │ Michael Holloway  │ Alyssaborough Sages     │ GK  │ 399984 │       3 │
10. │ Larry Buchanan    │ Eddieshire Discovere... │ F   │ 399973 │       1 │
11. │ Alexis Valenzuela │ Aaronport Crusaders     │ F   │ 399972 │       2 │
12. │ Mark Villegas     │ East Michaelborough ... │ F   │ 399972 │       2 │
    └───────────────────┴─────────────────────────┴─────┴────────┴─────────┘

```

This query works, but it’s pretty clunky. Now that we have the `QUALIFY` clause, we can filter the data without needing to introduce a CTE, as shown below:



```
SELECT player, team, position AS pos, salary,
       rank() OVER (PARTITION BY position ORDER BY salary DESC) AS posRank
FROM salaries
QUALIFY posRank <= 3
ORDER BY salary DESC;

```

And we’ll get the same results as before.


## Join Performance Improvements [\#](/blog/clickhouse-release-24-04#join-performance-improvements)


### Contributed by Maksim Kita [\#](/blog/clickhouse-release-24-04#contributed-by-maksim-kita-2)


There are also some performance improvements for very specific JOIN use cases.


The first is better predicate pushdown, when the analyzer works out when a filter condition can be applied to both sides of a JOIN.


Let’s look at an example using [The OpenSky dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/opensky), which contains air traffic data from 2019\-2021\. We want to get a list of ten flights that go through San Francisco, which we can do with the following query:



```
SELECT
    l.origin,
    r.destination AS dest,
    firstseen,
    lastseen
FROM opensky AS l
INNER JOIN opensky AS r ON l.destination = r.origin
WHERE notEmpty(l.origin) AND notEmpty(r.destination) AND (r.origin = 'KSFO')
LIMIT 10
SETTINGS optimize_move_to_prewhere = 0

```

We’re disabling `optimize_move_to_prewhere` so that ClickHouse doesn’t perform another optimization, which would stop us from seeing the benefit of the JOIN improvements. If we run this query on 24\.3, we’ll see the following output:



```
    ┌─origin─┬─dest─┬───────────firstseen─┬────────────lastseen─┐
 1. │ 00WA   │ 00CL │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 2. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 3. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 4. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 5. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 6. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 7. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 8. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 9. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
10. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
    └────────┴──────┴─────────────────────┴─────────────────────┘

10 rows in set. Elapsed: 0.656 sec. Processed 15.59 million rows, 451.90 MB (23.75 million rows/s., 688.34 MB/s.)
Peak memory usage: 62.79 MiB.

```

Let’s have a look at 24\.4:



```
    ┌─origin─┬─dest─┬───────────firstseen─┬────────────lastseen─┐
 1. │ 00WA   │ 00CL │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 2. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 3. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 4. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 5. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 6. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 7. │ 00WA   │ ZGGG │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 8. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
 9. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
10. │ 00WA   │ YSSY │ 2019-10-14 21:03:19 │ 2019-10-14 22:42:01 │
    └────────┴──────┴─────────────────────┴─────────────────────┘

10 rows in set. Elapsed: 0.079 sec.

```

So that’s about 8 times quicker. If we return all the columns via `SELECT *`, the time taken for this query in 24\.3 goes up to over 4 seconds and in 24\.4 it’s 0\.4 seconds, which is a 10x improvement.


Let’s see if we can understand why it’s faster. The two lines of interest are these:



```
INNER JOIN opensky AS r ON l.destination = r.origin
WHERE notEmpty(l.origin) AND notEmpty(r.destination) AND (r.origin = 'KSFO')

```

The last predicate of our `WHERE` clause is `r.origin = 'KSFO'`. In the previous line we said that we only want to do the join if `l.destination = r.origin`, which means that `l.destination = 'KSFO'` as well. The analyzer in 24\.4 knows this and can therefore filter out a bunch of rows much earlier.


In other words, our `WHERE` clause effectively looks like this in 24\.4



```
INNER JOIN opensky AS r ON l.destination = r.origin
WHERE notEmpty(l.origin) AND notEmpty(r.destination) 
AND (r.origin = 'KSFO') AND (l.destination = 'KSFO')

```

The second improvement is that the analyzer will now automatically convert an `OUTER JOIN` to an `INNER JOIN` if the predicate after the JOIN filters out any non\-joined rows.


For example, let’s say we initially wrote a query to find flights between San Francisco and New York, capturing both direct flights and ones that have a layover.



```
SELECT
    l.origin,
    l.destination,
    r.destination,
    registration,
    l.callsign,
    r.callsign
FROM opensky AS l
LEFT JOIN opensky AS r ON l.destination = r.origin
WHERE notEmpty(l.destination) 
AND (l.origin = 'KSFO') 
AND (r.destination = 'KJFK') 
LIMIT 10

```

We later add an extra filter that only returns rows where `r.callsign = 'AAL1424'`.



```
SELECT
    l.origin,
    l.destination AS leftDest,
    r.destination AS rightDest,
    registration AS reg,
    l.callsign,
    r.callsign
FROM opensky AS l
LEFT JOIN opensky AS r ON l.destination = r.origin
WHERE notEmpty(l.destination) 
AND (l.origin = 'KSFO') 
AND (r.destination = 'KJFK') 
AND (r.callsign = 'AAL1424')
LIMIT 10
SETTINGS optimize_move_to_prewhere = 0

```

Since we now require the `callsign` column on the right\-hand side of the join to have a value, the `LEFT JOIN` can be converted to an `INNER JOIN`. Let’s examine the query performance in 24\.3 and 24\.4\.


24\.3



```
    ┌─origin─┬─leftDest─┬─rightDest─┬─reg────┬─callsign─┬─r.callsign─┐
 1. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 2. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 3. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 4. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 5. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 6. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 7. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 8. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 9. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
10. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
    └────────┴──────────┴───────────┴────────┴──────────┴────────────┘

10 rows in set. Elapsed: 1.937 sec. Processed 63.98 million rows, 2.52 GB (33.03 million rows/s., 1.30 GB/s.)
Peak memory usage: 2.84 GiB.

```

24\.4



```
    ┌─origin─┬─leftDest─┬─rightDest─┬─reg────┬─callsign─┬─r.callsign─┐
 1. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 2. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 3. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 4. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 5. │ KSFO   │ 01FA     │ KJFK      │ N12221 │ UAL423   │ AAL1424    │
 6. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 7. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 8. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
 9. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
10. │ KSFO   │ 01FA     │ KJFK      │ N87527 │ UAL423   │ AAL1424    │
    └────────┴──────────┴───────────┴────────┴──────────┴────────────┘

10 rows in set. Elapsed: 0.762 sec. Processed 23.22 million rows, 939.75 MB (30.47 million rows/s., 1.23 GB/s.)
Peak memory usage: 9.00 MiB.

```

It's a little bit under three times quicker in 24\.4\.


If you’d like to learn more about how the JOIN performance improvements were implemented, [read Maksim Kita’s blog post](https://www.tinybird.co/blog-posts/clickhouse-joins-improvements) explaining everything.


That’s all for the 24\.4 release. We’d love for you to join us for the 24\.5 release call on 30 May. Make sure you [register so that you’ll get all the details for the Zoom webinar](https://clickhouse.com/company/events/v24-5-community-release-call).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
