# Trace similarity systems on top of ClickHouse to analyze crash stack traces from our CI


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Trace similarity systems on top of ClickHouse to analyze crash stack traces from our CI

![](/_next/image?url=%2Fuploads%2Fmisha_3ac4306654.png&w=96&q=75)[Misha Shiryaev](/authors/misha-shiryaev)Sep 24, 2025 · 12 minutes read## Problem [\#](/blog/trace-similarity-stack-traces#problem)


Our CI system is very good at catching bugs, and sometimes it catches crash logs during AST Fuzzing, Stress, and Functional tests. However, the crash reports are often very similar, and it is hard to understand which bugs are actually new and which ones are already known.


Quoting the [TraceSim: A Method for Calculating Stack Trace Similarity](https://arxiv.org/pdf/2009.12590) article:



> Many contemporary software products have subsystems for automatic crash reporting. However, it is well\-known that the same bug can produce slightly different reports.


This paper's methodology is based on the idea that similar stack traces are likely to be caused by the same bug. The authors propose a method for calculating stack trace similarity, which can be used to group similar crash stack traces together.


The system to analyze and group traces from the ClickHouse Cloud was first built by our Infrastructure Engineer, Michael Stetsyuk. It groups crash reports by their stack traces and allows them to be tracked in the issue tracker.


Similar to that system, we wanted to build a trace similarity system on top of ClickHouse to analyze crash stack traces from our CI. The system should be able to:


- Parse crash reports and extract stack frames.
- Calculate similarity between stack traces.
- Group similar new stack traces together with known.
- Create and update issues on GitHub to track the bugs.


I'll describe below each step of the process in detail, so you can build a similar system for your own needs.


## How do we do it? [\#](/blog/trace-similarity-stack-traces#how-do-we-do-it)


The high\-level architecture of the system is as follows:


![trace-blog-diagram.jpg](/uploads/trace_blog_diagram_4819d96174.jpg)
### Step zero: collect crash reports, create all the necessary tables [\#](/blog/trace-similarity-stack-traces#step-zero-collect-crash-reports-create-all-the-necessary-tables)


We need to collect crash reports from our CI system. Luckily, the system already works for a few years.


Briefly described, the system creates [Materialized views](https://clickhouse.com/docs/materialized-view/incremental-materialized-view), inserting new rows into the remote ClickHouse cluster's tables, where the destination tables' names are calculated from the current table structures \+ additional columns. It allows us to have historical data in tables with different structures and the same tables for different CI jobs. The script, managing these tables, is located in our [ci](https://github.com/ClickHouse/ClickHouse/blob/b499c8df1f091cbba234bbf23ce8473a5834e8aa/ci/jobs/scripts/functional_tests/setup_log_cluster.sh#L74) directory.


We need the data from [system.crash\_log](https://clickhouse.com/docs/operations/system-tables/crash-log) tables. That's how tables on the CI Logs cluster look now:



```

```
SHOW TABLES LIKE 'crash_log_%';

    ┌─name───────────────────────────┐
 1. │ crash_log_12587237819650651296 │
 2. │ crash_log_12670418084883306529 │
 3. │ crash_log_1527066305010279420  │
 4. │ crash_log_15355897847728332522 │
 5. │ crash_log_15557244372725679386 │
 6. │ crash_log_18405985218782237968 │
 7. │ crash_log_2288102012038531617  │
 8. │ crash_log_3310266143589491008  │
 9. │ crash_log_6802555697904881735  │
10. │ crash_log_9016585404038675675  │
11. │ crash_log_9097266775814416937  │
12. │ crash_log_9243005856023138905  │
13. │ crash_log_9768092148702997133  │
14. │ crash_logs                     │
    └────────────────────────────────┘
```

```


```

```
SHOW CREATE TABLE crash_logs;

CREATE TABLE default.crash_logs
(
    `repo` String,
    `pull_request_number` UInt32,
    `commit_sha` String,
    `check_start_time` DateTime,
    `check_name` String,
    `instance_type` String,
    `instance_id` String,
    `hostname` LowCardinality(String),
    `event_date` Date,
    `event_time` DateTime,
    `timestamp_ns` UInt64,
    `signal` Int32,
    `thread_id` UInt64,
    `query_id` String,
    `trace` Array(UInt64),
    `trace_full` Array(String),
    `version` String,
    `revision` UInt32,
    `build_id` String
)
ENGINE = Merge('default', '^crash_log_')
```

```

Here is an example of the data we store there

```

```
SELECT *
FROM crash_logs
WHERE event_date = today()
LIMIT 1

Row 1:
──────
repo:                ClickHouse/ClickHouse
pull_request_number: 85843
commit_sha:          41215391373ad2e277230939e887c834edeb16ce
check_start_time:    2025-08-19 10:07:50
check_name:          Stateless tests (arm_binary, parallel)
instance_type:       c8g.8xlarge
instance_id:         i-0b53d7dc362ab4cd8
hostname:            16ffef362c03
event_date:          2025-08-19
event_time:          2025-08-19 10:09:04
timestamp_ns:        1755598144624168055
signal:              6
thread_id:           6359
query_id:            5ce98be8-f4cb-4950-82a8-cc2720669cad
trace:               [280796479681009,280796479399548,280796479320368,188029769003464,188029769005984,188029769006680,188029679339096,188029679337384,188029679380404,188029836833040,188029837238400,188029837230992,188029837232044,188029915248680,188029915247868,188029915340828,188029915297288,188029915294080,188029915293160,…]
trace_full:          ['3. ? @ 0x000000000007f1f1','4. ? @ 0x000000000003a67c','5. ? @ 0x0000000000027130','6. ./ci/tmp/build/./src/Common/Exception.cpp:51: DB::abortOnFailedAssertion(String const&, void* const*, unsigned long, unsigned long) @ 0x000000000e33b1c8','7. ./ci/tmp/build/./src/Common/Exception.cpp:84: DB::handle_error_code(String const&, std::basic_string_view>, int, bool, std::vector> const&) @ 0x000000000e33bba0','8. ./ci/tmp/build/./src/Common/Exception.cpp:135: DB::Exception::Exception(DB::Exception::MessageMasked&&, int, bool) @ 0x000000000e33be58','9. DB::Exception::Exception(String&&, int, String, bool) @ 0x0000000008db8658','10. DB::Exception::Exception(PreformattedMessage&&, int) @ 0x0000000008db7fa8','11. DB::Exception::Exception<>(int, FormatStringHelperImpl<>) @ 0x0000000008dc27b4','12. ./ci/tmp/build/./src/Storages/ObjectStorage/StorageObjectStorageConfiguration.cpp:212: DB::StorageObjectStorageConfiguration::addDeleteTransformers(std::shared_ptr, DB::QueryPipelineBuilder&, std::optional const&, std::shared_ptr) const @ 0x00000000123eb110','13. ./ci/tmp/build/./src/Storages/ObjectStorage/StorageObjectStorageSource.cpp:555: DB::StorageObjectStorageSource::createReader(unsigned long, std::shared_ptr const&, std::shared_ptr const&, std::shared_ptr const&, DB::ReadFromFormatInfo&, std::optional const&, std::shared_ptr const&, DB::SchemaCache*, std::shared_ptr const&, unsigned long, std::shared_ptr, std::shared_ptr, bool) @ 0x000000001244e080','14.0. inlined from ./ci/tmp/build/./src/Storages/ObjectStorage/StorageObjectStorageSource.cpp:412: DB::StorageObjectStorageSource::createReader()','14. ./ci/tmp/build/./src/Storages/ObjectStorage/StorageObjectStorageSource.cpp:265: DB::StorageObjectStorageSource::lazyInitialize() @ 0x000000001244c390','15. ./ci/tmp/build/./src/Storages/ObjectStorage/StorageObjectStorageSource.cpp:274: DB::StorageObjectStorageSource::generate() @ 0x000000001244c7ac','16. ./ci/tmp/build/./src/Processors/ISource.cpp:144: DB::ISource::tryGenerate() @ 0x0000000016eb3828','17. ./ci/tmp/build/./src/Processors/ISource.cpp:110: DB::ISource::work() @ 0x0000000016eb34fc','18.0. inlined from ./ci/tmp/build/./src/Processors/Executors/ExecutionThreadContext.cpp:53: DB::executeJob(DB::ExecutingGraph::Node*, DB::ReadProgressCallback*)','18. ./ci/tmp/build/./src/Processors/Executors/ExecutionThreadContext.cpp:102: DB::ExecutionThreadContext::executeTask() @ 0x0000000016eca01c','19. ./ci/tmp/build/./src/Processors/Executors/PipelineExecutor.cpp:350: DB::PipelineExecutor::executeStepImpl(unsigned long, DB::IAcquiredSlot*, std::atomic*) @ 0x0000000016ebf608',…]
version:             ClickHouse 25.8.1.1
revision:            54501
build_id:            88351121A8340C83AB8A60BA97765ADC4B9B7786
```

```


Perfect, we have the raw data to analyze.


#### Separate collecting and analyzing clusters, create tables for analysis [\#](/blog/trace-similarity-stack-traces#separate-collecting-and-analyzing-clusters-create-tables-for-analysis)


To avoid the performance impact on the CI system, we are using a separate ClickHouse cluster to analyze the crash traces. The following tables and materialized view manage updating the data from the remote CI Logs cluster:



```

```
1-- Create a table to store the raw stack traces with details about where and when they were appeared
2CREATE TABLE default.stack_traces
3(
4    `repo` LowCardinality(String),
5    `pull_request_number` UInt32,
6    `commit_sha` String,
7    `check_name` String,
8    `check_start_time` DateTime('UTC'),
9    `event_time` DateTime,
10    `timestamp_ns` UInt64,
11    `trace_full` Array(String),
12    `Version` UInt32 DEFAULT now()
13)
14ENGINE = ReplacingMergeTree(Version)
15PARTITION BY toYYYYMM(event_time)
16ORDER BY (event_time, timestamp_ns, repo, check_start_time)
17SETTINGS index_granularity = 8192;
18
19-- create a refresheable materialized view to collect the data from the crash_logs table for the last 100 days
20-- https://clickhouse.com/docs/materialized-view/refreshable-materialized-view
21CREATE MATERIALIZED VIEW default._stack_traces_mv
22REFRESH EVERY 30 MINUTE TO default.stack_traces
23AS SELECT
24    repo,
25    pull_request_number,
26    commit_sha,
27    check_name,
28    check_start_time,
29    event_time,
30    timestamp_ns,
31    trace_full,
32    now() AS Version
33FROM remoteSecure('[HOST]', 'default', 'crash_logs', 'username', 'password')
34WHERE event_date >= today() - INTERVAL 100 DAY;
35
36-- Create a table to store the info about the GitHub issues created for the stack traces
37CREATE TABLE default.crash_issues
38(
39    `created_at` DateTime,
40    `updated_at` DateTime,
41    `closed_at` DateTime,
42    `repo` String,
43    `number` UInt32,
44    `state` Enum8('open' = 1, 'closed' = 2),
45    `stack_traces_full` Array(Array(String)),
46    `stack_traces_hash` Array(UInt64)
47)
48ENGINE = ReplacingMergeTree(updated_at)
49PARTITION BY toYYYYMM(created_at)
50ORDER BY (repo, number)
51SETTINGS index_granularity = 8192;
```

```

From this point, we use data on this cluster. The data is refreshed every 30 minutes, ensuring that we have the latest crash events available for analysis.


### Step one: clean crash traces [\#](/blog/trace-similarity-stack-traces#step-one-clean-crash-traces)


Once the traces are on the separate cluster, we need to clean them up. The traces contain a lot of noise that can affect the similarity calculation. The noise can come from, but is not limited to:


- Different compiler versions.
- Different build configurations (e.g., debug vs release).
- Different environments (e.g., different OS, different hardware).
- Different file names and line numbers in the stack traces.


To clean the traces, we define two [User Defined Functions](https://clickhouse.com/docs/sql-reference/functions/udf#sql-user-defined-functions):



```

```
1CREATE FUNCTION cleanStackFrame AS frame -> replaceRegexpOne(
2  replaceRegexpAll(
3    splitByString(
4      -- second, strip the file name and line number, keep the function name
5      ': ', splitByString(
6        -- first, strip the frame address, keep the frame number, file name, line number, and function name
7        ' @ ', frame, 2
8      )[1], 2
9    )[2],
10    -- third, replace all ABI specific information with a placeholder
11    '\\[abi:[^]]+\\]', '[$ABI]'),
12  -- finally, delete all LLVM specific information
13  '(\\s+[(])*[.]llvm[.].+', ''
14);
15
16CREATE FUNCTION cleanStackTrace AS trace -> arrayFilter(
17  frame -> (
18    -- second, keep only meaningful frames
19    frame NOT IN ('', '?')), arrayMap(
20      -- first, clean each frame of the stack trace
21      fr -> cleanStackFrame(fr), trace
22  )
23);
```

```

These functions will be used to clean the stack traces before calculating their similarity on the fly. The `cleanStackFrame` function removes the noise from each frame, and the `cleanStackTrace` function applies it to the whole stack trace.


There's a possibility of using these UDFs to pre\-process the data in the `stack_traces` table; however, we do it on the fly to avoid storing the pre\-cleaned traces in the database. It provides us with more flexibility, enabling us to modify the cleaning logic without reprocessing all the data. It's handy for calculating the weights of frames at the similarity calculation step.


### Step two: group identical traces and distinguish the significant ones among them [\#](/blog/trace-similarity-stack-traces#step-two-group-identical-traces-and-distinguish-the-significant-ones-among-them)


Once the stack traces are cleaned, we can start analyzing them. The already processed traces are in the `crash_issues` table; we use these to find the existing issues.



```

```
1WITH known_hashes AS
2    (
3        SELECT
4            repo,
5            -- Avoid default value of 'open' for state
6            toString(state) AS state,
7            updated_at,
8            closed_at,
9            arrayFlatten(groupArrayDistinct(stack_traces_hash)) AS known_hashes
10        FROM default.crash_issues FINAL
11        GROUP BY ALL
12    )
13SELECT
14    repo,
15    groupArrayDistinct((pull_request_number, commit_sha, check_name)) AS checks,
16    cleanStackTrace(trace_full) AS trace_full,
17    sipHash64(trace_full) AS trace_hash,
18    length(groupArrayDistinct(pull_request_number) AS PRs) AS trace_count,
19    has(PRs, 0) AS is_in_master
20FROM default.stack_traces AS st
21LEFT JOIN known_hashes AS kh ON (st.repo = kh.repo AND has(kh.known_hashes, trace_hash))
22WHERE (st.event_time >= (now() - toIntervalDay(30)))
23    AND (length(trace_full) > 5)
24GROUP BY
25    repo,
26    trace_full
27HAVING
28    groupArrayDistinct(kh.state) = [''] -- new trace, no issues
29    OR (groupArrayDistinct(kh.state) = ['closed'] AND max(st.check_start_time) > max(kh.closed_at)) -- new event after the issue is closed
30ORDER BY max(st.event_time)
```

```

This query groups the stack traces by their cleaned version and calculates the hash of the trace. The hashes are checked against the `crash_issues` table to find out if the trace is already known. If there is an open issue, or the trace is created before the existing issues were closed, it is considered a known trace.


The query also counts the number of unique pull requests that contain the trace and checks if the trace is present in the master branch (pull request number 0\). If the trace appears in fewer than three pull requests and wasn't seen in the master/release branches, it's considered insignificant. Such traces aren't used to create issues, but they can be added to existing issues if they are similar enough to the known traces.


### Step three: calculate similarity between traces [\#](/blog/trace-similarity-stack-traces#step-three-calculate-similarity-between-traces)


Now we have a list of new stack traces from step two. We need to compare them one by one to the known stack traces, linked to GitHub issues.


The following query is the [TraceSim's paper](https://arxiv.org/pdf/2009.12590) implementation of the similarity calculation. ClickHouse has `arraySimilarity` function since version [25\.4](https://clickhouse.com/docs/whats-new/changelog#254), the weights are calculated on the fly. The `new_trace` is one of the new traces from step two.



```

```
1WITH
2    1.97 AS alpha,
3    2.0 AS beta,
4    3.7 AS gamma,
5    0.68 AS threshold,
6    stack_frame_weights AS (
7        WITH
8            (
9                SELECT count()
10                FROM default.stack_traces
11                FINAL
12            ) AS total
13        SELECT
14            arrayJoin(cleanStackTrace(trace_full)) AS frame,
15            countDistinct(trace_full) AS count,
16            log(total / count) AS IDF,
17            sigmoid(beta * (IDF - gamma)) AS weight
18        FROM default.stack_traces
19        FINAL
20        GROUP BY frame
21    ),
22    (SELECT groupArray(weight) AS w, groupArray(frame) AS f FROM stack_frame_weights) AS weights,
23    (trace -> arrayMap((_frame, pos) -> (pow(pos, -alpha) * arrayFirst(w, f -> (f = _frame), weights.w, weights.f)), trace, arrayEnumerate(trace))) AS get_trace_weights,
24    -- one of the new traces from step two
25    ['DB::abortOnFailedAssertion(String const&, void* const*, unsigned long, unsigned long)','DB::handle_error_code(String const&, std::basic_string_view>, int, bool, std::vector> const&)','DB::Exception::Exception(DB::Exception::MessageMasked&&, int, bool)','DB::Exception::Exception(int, FormatStringHelperImpl::type, std::type_identity::type, std::type_identity::type>, String const&, String&&, String const&)','DB::paranoidCheckForCoveredPartsInZooKeeper(std::shared_ptr const&, String const&, StrongTypedef, String const&, DB::StorageReplicatedMergeTree const&)','DB::StorageReplicatedMergeTree::executeDropRange(DB::ReplicatedMergeTreeLogEntry const&)','DB::StorageReplicatedMergeTree::executeLogEntry(DB::ReplicatedMergeTreeLogEntry&)','operator()','decltype(std::declval)::$_1&>()(std::declval&>())) std::__invoke[$ABI])::$_1&, std::shared_ptr&>(DB::StorageReplicatedMergeTree::processQueueEntry(std::shared_ptr)::$_1&, std::shared_ptr&)','bool std::__invoke_void_return_wrapper::__call[$ABI])::$_1&, std::shared_ptr&>(DB::StorageReplicatedMergeTree::processQueueEntry(std::shared_ptr)::$_1&, std::shared_ptr&)','DB::ReplicatedMergeTreeQueue::processEntry(std::function ()>, std::shared_ptr&, std::function&)>)','DB::StorageReplicatedMergeTree::processQueueEntry(std::shared_ptr)','DB::ExecutableLambdaAdapter::executeStep()','DB::MergeTreeBackgroundExecutor::routine(std::shared_ptr)','DB::MergeTreeBackgroundExecutor::threadFunction()'] AS new_trace,
26    get_trace_weights(new_trace) AS new_trace_weights
27SELECT
28    arraySimilarity(
29        new_trace,
30        arrayJoin(stack_traces_full) AS trace_full,
31        new_trace_weights,
32        get_trace_weights(trace_full)
33    ) AS similarity,
34    repo,
35    number,
36    created_at,
37    closed_at,
38    stack_traces_full,
39    stack_traces_hash
40FROM default.crash_issues FINAL
41WHERE repo = 'ClickHouse/ClickHouse'
42    AND state = 'open'
43    AND threshold <= similarity
```

```

In our system, significant traces are collected and processed on an hourly basis, so we can analyze them in a timely manner. If no similar traces are found for a significant new trace, we create a new issue in the GitHub repository and add the row to the `crash_issues` table.


Once a day we process all the traces including insignificant ones, to find out if they are similar to the known significant traces. If a trace with similarity higher the threshold is found, we add it to the existing issue.


A pinch of LLM helps us generating the issue title and generating possible reasons of the crash based on the stack trace.


## What do we have in the end [\#](/blog/trace-similarity-stack-traces#what-do-we-have-in-the-end)


All automatically created issues can be found in the repository with [crash\-ci](https://github.com/ClickHouse/clickhouse/issues?q=state%3Aopen%20label%3Acrash-ci) label. As always, your help is appreciated, so if you find an issue that can be fixed, please feel free to contribute!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
