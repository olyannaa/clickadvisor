# BuzzHouse: Bridging the database fuzzing gap for testing ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# BuzzHouse: Bridging the database fuzzing gap for testing ClickHouse

![Pedro Ferreira](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U07_FGC_3_NWC_9_95b20f53eb49_512_7ab325b2fe.jpeg&w=96&q=75)Pedro FerreiraJan 21, 2025 · 11 minutes readFuzzing has become a scorching [research topic](https://www.techscience.com/cmc/v78n1/55370) in the last few years to find issues in software, including crashes, bad output, and security vulnerabilities. Databases are no exception, and many research tools have been developed.


ClickHouse is also actively tested with fuzzers \- over the years, several fuzzers, including SQLancer, SQLsmith, [AST fuzzer](https://clickhouse.com/blog/fuzzing-click-house), and, more recently, [WINGFUZZ](https://clickhouse.com/blog/fuzzing-wingfuzz) fuzzer, have been used to test ClickHouse.


Since I joined ClickHouse, I have been reviewing the existing testing infrastructure in ClickHouse and noticed a notorious gap in their fuzzers. None of them was capable of generating a wide complexity of queries while keeping query correctness in mind.


Therefore, over the past 5 months, I developed BuzzHouse, a new fuzzer to complement the existing gap in the existing testing infrastructure. BuzzHouse already has found about [100 new issues](https://github.com/ClickHouse/ClickHouse/issues?q=is%3Aopen+label%3Afuzz+author%3APedroTadim) in ClickHouse, and in this blog post, I am showing what to consider when fuzzing databases.


![Fuzz_01.png](/uploads/Fuzz_01_2f5ac9f93f.png)
## What is fuzzing or fuzz testing? [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#what-is-fuzzing-or-fuzz-testing)


Before discussing why fuzzing databases is hard, let’s briefly define what fuzzing is. Fuzzing, or fuzz testing, is a software testing technique that involves providing random, unexpected, or invalid inputs to a program to uncover bugs, crashes, or vulnerabilities. By simulating unpredictable user behavior, fuzzing helps identify edge cases that might otherwise go unnoticed during standard testing. It’s widely used to improve the robustness and security of software, from operating systems to compilers and databases.


## Why fuzzing databases is hard [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#why-fuzzing-databases-is-hard)


A database is a complex system encompassing query processing and optimization, data storage, buffer management, and, for cases such as ClickHouse, distributed processing over multiple nodes. With such a level of complexity, building a fuzzer to test a database is no simple task. At the same time, attempting to test all the layers of a database system becomes more challenging because more diversified inputs are required.


### How to generate queries? [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#how-to-generate-queries)


We can start by looking at the top\-most layer, ie input client’s query parsing and processing. Most databases, including ClickHouse, use SQL as their input language, and most database fuzzers are developed to produce SQL queries. The very first design question is how we are going to generate queries. Some fuzzers do it completely randomly, while others use a backlog strategy in mind. While both approaches are correct, depending on the chosen approach, some cases won’t be generated, and some bugs may not be found. Let’s take a look at [TPC\-H](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch) Q5 as an example:



```

```
1SELECT
2    n_name,
3    sum(l_extendedprice * (1 - l_discount)) AS revenue
4FROM
5    customer,
6    orders,
7    lineitem,
8    supplier,
9    nation,
10    region
11WHERE
12    c_custkey = o_custkey
13    AND l_orderkey = o_orderkey
14    AND l_suppkey = s_suppkey
15    AND c_nationkey = s_nationkey
16    AND s_nationkey = n_nationkey
17    AND n_regionkey = r_regionkey
18    AND r_name = 'ASIA'
19    AND o_orderdate >= DATE '1994-01-01'
20    AND o_orderdate < DATE '1994-01-01' + INTERVAL '1' year
21GROUP BY
22    n_name
23ORDER BY
24    revenue DESC;
```


```

When users write such a query, they expect all tables and columns to be valid. However, if the fuzzer only generates valid identifiers, bugs from inexisting tables and columns will never be found.


Another interesting case here is the grouping case. SQL has complex semantics that make random query generation harder. In this case, we must make sure the projection either uses the `n_name` column or any other column inside an aggregate function to be correct. Other rules may also be applied, such as not using aggregates in WHERE clause and window functions cannot be inside aggregate functions. With these semantics in mind, it becomes difficult to generate correct queries randomly. If we take these restrictions, we will decrease the domain of queries generated, plus the number of bugs we can potentially find.


Some statements, such as DROP and DETACH, make tables unavailable. The fuzzer should potentially be aware of this to use valid tables in queries. We can keep track of changes made by these statements, but later, it becomes complex to handle this information when more features are added, such as SQL views that may depend on tables.


As we add more features to be tested, e.g. SQL functions, SQL query clauses, SQL types, number of tables/columns/databases to use, other statements such as INSERT or OPTIMIZE in ClickHouse, or more table engines, the number of combinations will increase sharply. This becomes a relevant issue when we attempt to generate correct queries or test a new feature in the fuzzer. As I said before, we can either try to avoid these errors and restrict the generated domain or ignore them and improve query correctness. In BuzzHouse I try to generate the correct output for most cases while fallbacking to the random case a few times.


### Finding wrong results [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#finding-wrong-results)


With current state\-of\-the\-art research, we can find queries with wrong results in BuzzHouse which is not possible in other fuzzers such as SQLsmith. The strategies include:


- Dump a table and read it back again, so we can test formats as well.
- Run and compare equivalent queries using an oracle. This strategy was pioneered by SQLancer.
- Run the same query with different settings, such as the number of threads, enable/disable external sorting or grouping, or set a different join algorithm.
- Swap tables with a table from another relational database, then push predicates into it, and then compare computation results with either the same ordering clause or a global aggregate query.


The following issue was found after dumping and re\-inserting values into a table. The block order was different after the insert, thus impacting sorting with the `LowCardinality` type.



```

```
1SET allow_suspicious_low_cardinality_types = 1;
2CREATE TABLE t0 (c0 LowCardinality(Nullable(Int))) ENGINE = MergeTree()
3ORDER BY (c0) SETTINGS allow_nullable_key = 1;
4INSERT INTO TABLE t0 (c0) VALUES (1);
5INSERT INTO TABLE t0 (c0) VALUES (0), (NULL);
6SELECT c0 FROM t0 ORDER BY c0 DESC NULLS LAST;
7-- 1
8-- NULL
9-- 0
```


```

### Use code coverage? [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#use-code-coverage)


Current state\-of\-the\-art techniques in fuzzers such as AFL and libFuzzer use code coverage to find new code paths while fuzzing. This sounds promising at first, but with the complexity of databases, finding new paths becomes increasingly more difficult. First, the SQL language has many semantics to follow as explained above. Second, many issues require more inputs, such as multiple clients or server restarts. Third, code coverage fuzzing becomes much slower, and due to each mutation doing a small change to a query at each loop, the diversity of queries generated is much lower. At the same time, it’s advised to backup the generated corpus to continue the same session later. In BuzzHouse, we decided not to use code coverage at the moment to complement existing fuzzers with this feature.


### Frequency of events [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#frequency-of-events)


The next important decision is the randomness of the events. Every decision a fuzzer performs will be based on probabilities. Conforming to the probabilities set, the fuzzer gets restricted to the possibility of events it can generate. Let’s take an example for the case a fuzzer has to choose the next query to generate:


- 10% chance to create a table.
- 50% chance to run a SELECT query (these happen more often in analytical databases so we should generate more).
- 20% chance to insert into a table.
- 5% to drop a table.
- 5% to delete from a table (a lightweight delete in ClickHouse).
- 10% for an ALTER statement.


This probability chart may sound plausible, however, at every 20 queries, one DROP statement will be generated. What is the consequence of this? Due to the number of combinations, a DROP statement has a higher chance of succeeding than a CREATE TABLE. There’s also a possibility to drop all the tables in the catalog, while none is created. Furthermore, it becomes difficult to do long\-term testing on a table that persists on the server while many INSERT/UPDATE/DELETE statements are issued over time. These small decisions may impact what the fuzzer will ever be capable of doing.


## Designing a fuzzer for ClickHouse [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#designing-a-fuzzer-for-clickhouse)


Besides everything mentioned above, there are other design decisions when building a fuzzer. Here are some questions and what was implemented:


- Should many clients run in parallel? If so, how to synchronize between them? At the moment, only a single client in BuzzHouse.
- All the fuzzers run on the client side. What about fuzzing the server? Use a separate fuzzer for the server.
- Not all the issues are about crashes, we have to look for wrong results in queries, the quality of error messages, and performance. BuzzHouse detects some wrong results. For performance, later we can benchmark consecutive query runs and compare them.
- By looking at TPC\-H Q5, what should the size of the queries generated by the fuzzer be? How many tables should we join? Look at cross\-products, they generate large intermediates and turn the fuzzer slower. BuzzHouse has “depth” and “width” parameters that can be tuned for this.
- For how long should a fuzzer keep a table in the catalog on average? What about updating the table metadata? BuzzHouse will always keep at least 3 tables in the catalog. Alter statements run for every table except for the ones with peers in other databases.
- Look at error messages, some bugs output strange error messages instead of crashing the server. Also sometimes an error message may be right or wrong. In the future, we could keep a list of expected error messages to be thrown by the server.
- For slow queries, which ones are legitimately slow and which aren’t? This is a difficult question to answer. However, we can compare the performance with other databases.


Taking all the points above, it becomes very difficult to build a fuzzer that will cover all the cases, and then find all existing issues. Making a simple design decision will impact what the fuzzer will be capable of generating.


BuzzHouse attempts to generate the most correct queries as possible by using syntax assumptions such as:


- Always generate the correct number of arguments for a function.
- Use columns from tables present in queries.
- Back up the catalog with CREATE/ALTER/DROP changes.
- Keep query syntax always correct.


However, the codebase becomes more complex to handle all these assumptions, plus requires to be updated whenever new features are added. Also don’t forget some trivial queries such as `SELECT 1 FROM idontexist;` won’t be generated.


## Summary [\#](/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse#summary)


BuzzHouse was developed to address critical gaps in the fuzzing landscape used for ClickHouse.


By focusing on generating complex yet correct queries and identifying issues beyond simple crashes, it complements the current suite of tools used to test databases:


- Use AFL and libFuzzer for code coverage\-guided fuzzing.
- SQLsmith (<https://github.com/anse1/sqlsmith>) for complex query generation.
- SQLancer (<https://github.com/sqlancer/sqlancer>) for query correctness.
- Pstress ([https://github.com/Percona\-QA/pstress](https://github.com/Percona-QA/pstress)) for heavy load. Planned to possibly integrate it in ClickHouse CI later.
- Sysbench (<https://github.com/akopytov/sysbench>) for a continuous workload (\+1 hour). Also in the plans for CI.
- BuzzHouse for randomly generated catalog\-backed queries.
- AST fuzzer to mutate queries from tests, and possibly other fuzzers.
- A custom script to fuzz the server and plug any other existing fuzzer into it.


BuzzHouse’s ability to uncover already over 100 new issues underscores its value and the importance of diverse fuzzing approaches in improving the robustness and reliability of databases like ClickHouse.


BuzzHouse is set to be merged into the ClickHouse source code soon. If you’re curious, feel free to explore the [pull request](https://github.com/ClickHouse/ClickHouse/pull/71085).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
