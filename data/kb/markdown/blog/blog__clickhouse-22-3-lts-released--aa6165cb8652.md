# ClickHouse 22\.3 LTS Released


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse 22\.3 LTS Released

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Apr 12, 2022 · 11 minutes read
The new ClickHouse release 22\.3 is ready! This is a long\-term support release (LTS) — it will receive security updates and important bug fixes through March 2023\.


The release includes 1308 new commits from 86 contributors, including 25 new contributors:


1lann, Anish Bhanwala, Eugene Galkin, HaiBo Li, Hongbin, Jianmei Zhang, LAL2211, Lars Eidnes, Miel Donkers, NikitaEvs, Nir Peled, Robert Schulze, SiderZhang, Varinara, Xudong Zhang, Yong Wang, cwkyaoyao, heleihelei, kashwy, lincion, metahys, rfraposa, shuchaome, tangjiangling, zhangyifan27\.


The changes in 22\.3 are mostly focused on feature maturity, security and reliability. A few experimental features have become ready for production usage:


## **ClickHouse Keeper** [\#](/blog/clickhouse-22-3-lts-released#clickhouse-keeper)


ClickHouse Keeper is our replacement for ZooKeeper. It implements the ZooKeeper protocol and data model; and works as a drop\-in replacement of ZooKeeper (up to version 3\.5\) with ClickHouse and with other applications. It can work as a dedicated component or embedded into clickhouse\-server.


We are proud that it is passing Jepsen tests with continuous integration. This includes the tests for ZooKeeper and additional tests for better coverage. In addition, it is passing ClickHouse functional and integration tests, stress tests and fuzzing.


Since version 22\.3 we ensure that it is faster than ZooKeeper on both reads and writes while consuming less memory. Disk usage for logs and snapshots is also lower. The data on disk and in transfer is checksummed to protect from hardware failures. Higher percentiles of request latencies are lower. This has been made possible by contributions of **Zhang Li Star** and **Alexander Sapin**.


As of release 22\.3 ClickHouse Keeper is production ready! In fact, it is already being used in production for more than half a year, so you will not be the first production user.


## **ARM Architecture Support** [\#](/blog/clickhouse-22-3-lts-released#arm-architecture-support)


64bit ARM CPU architecture (AArch64\) has become increasingly popular for server applications in the cloud, as well as for laptops and workstations. Ever considered ClickHouse on network devices and mobile? You know what? ClickHouse runs on all of them and squeezes every bit of performance out of them.


We started porting ClickHouse to AArch64 in Feb 2016, and since that time we have checked 13 different CPU models: APM X\-Gene; Cavium ThunderX 1, 2; Raspberry Pi; Pinebook; Google Pixel; Apple M1, M1 Max; Huawei Taishan; AWS Graviton 1, 2, 3; Ampere Altra. There is a huge diversity among ARM CPU manufacturers and we are happy to support it. We also maintain the collection of [comparative benchmarks of different hardware](https://clickhouse.com/benchmark/hardware/).


Release 22\.3 has two major milestones for AArch64 support:


1. Continuous integration with 100% functional tests passing.
2. Full support for release builds: deb, rpm, apk, tgz, single\-binary and Docker.


This has been made possible by work of **Mikhail Shiryaev**. Since the release 22\.3 ClickHouse on AArch64 is production ready!


ClickHouse has more specific optimizations for x86\_64 instruction set architecture and only a couple AArch64\-specific optimizations, and even despite this fact, it gives better price/performance on AArch64 in the major cloud providers.


Some x86\-specific features are disabled on AArch64: support for Hyperscan, support for hardware metrics from [PMU](https://perfmon-events.intel.com/). Some features are not included in the build, like GRPC API support. Running mixed architecture clusters is not recommended, although there are no known issues as of now.


What to expect next? We have ongoing development for PowerPC 64 little\-endian and for RISC\-V 64\. If you are interested in some other CPU architecture, please let us know.


## **Virtual Filesystem Over S3** [\#](/blog/clickhouse-22-3-lts-released#virtual-filesystem-over-s3)


Experimental support for VFS over S3 exists for around two years. This is the story:


- s3 functions for data import and export by **Vladimir Chebotarev**
- disks, volumes and storage policies by **Igor Mineev** and **Alexander Sapin**
- automatic and user\-triggered movement of data parts between disks by **Vladimir Chebotarev**
- virtual file system interface by **Alexander Burmak**
- implementation of VFS over s3 by **Pavel Kovalenko**, **Grigory Pervakov** and **Anton Ivashkin**
- asynchronous reads by **Alexey Milovidov**, **Kseniia Sumarokova** and **Alexander Sapin**
- full functional test coverage, correctness and reliability by **Alexander Sapin**


As of 22\.3 we ensure maximum query performance on top of s3 and continuous testing for every commit. Support for MergeTree and ReplicatedMergeTree operation over s3 is ready for production.


Although some new features are not production ready: “zero\-copy replication” (ensure one copy of data if there are more than one replica in a region) and the local cache. Testing has been performed for AWS S3 and Minio. There are known issues on GCP.


## **Secure Build Infrastructure** [\#](/blog/clickhouse-22-3-lts-released#secure-build-infrastructure)


For previous versions we have used servers in Yandex Cloud. Since release 22\.3 we have migrated our infrastructure to different locations.


Continuous integration and testing moved to AWS data centers in the US. We also have released all the build and test runners in [open\-source](https://github.com/ClickHouse/ClickHouse/tree/master/.github/workflows). The build process has been made [reproducible](https://reproducible-builds.org/). You can run the build by yourself and get the binaries that are byte\-identical and indistinguishable to the official binaries. The build process is hermetic and does not depend on the OS distribution and the environment. The final release builds are stored in [JFrog Artifactory](https://www.jfrog.com/), and available on [packages.clickhouse.com](https://packages.clickhouse.com/).


The work has been done by **Mikhail Shiryaev**, **Alexander Sapin** and **Alexey Milovidov**.


Please read the [motivation for these changes](https://clickhouse.com/blog/we-stand-with-ukraine/).


## **Security Features** [\#](/blog/clickhouse-22-3-lts-released#security-features)


Authentication with X.509 client certificates has been contributed by **Eungenue**. And two features contributed by **Heena Bansal**: a switch to disable plaintext password or no password for users; filtering outgoing connections in MySQL, PostgreSQL federated queries.


## **More Testing And Fuzzing** [\#](/blog/clickhouse-22-3-lts-released#more-testing-and-fuzzing)


We believe [fuzzing](https://en.wikipedia.org/wiki/Fuzzing) is the absolute need to build reliable software. And the main principle of fuzzing is: there should be more fuzzing. So, we have many fuzzing methods in ClickHouse CI: LLVM’s libFuzzer, AST based query fuzzer, Ad\-hoc SQL function fuzzer, Randomization of thread scheduling order, Randomization of timezones, SQLancer (logical fuzzer), Stress tests, and Jepsen tests.


But this is not enough.


Since version 22\.3 we have added *randomization of query settings in functional tests*. So, we can run the tests under every combination of different settings.


We have also added automated tests for backward compatibility. It is trying to create every possible database, table and dictionary, then install the previous ClickHouse version and check if it will startup successfully. This allows us to be aware if a new feature will prevent version downgrade.


We are so keen on testing that we decided to add automated tests for tests. Whenever someone contributes a bugfix we automatically check that it contains tests and these tests fail on previous ClickHouse versions.


## **Semistructured Data** [\#](/blog/clickhouse-22-3-lts-released#semistructured-data)


Okay, I spent 15 minutes of your time telling about security, reliability, compliance, transparency… but where is **the fun**?


In version 22\.3 we have a new experimental feature — support for dynamic subcolumns and semistructured data!


Suppose you have a bunch of JSON and want to analyze it — without specifying the data types in your table. And you want your table to automatically adapt for the schema changes, to automatically add new columns. And everything with hierarchical objects and arrays with deep nesting! Now it is possible and it works like magic.


Let me demonstrate it with an example using GitHub API.


I obtained the list of GitHub repositories ordered by the number of stars from [GH Explorer](https://ghe.clickhouse.tech/). Then I started querying the metadata of the most popular repositories from GitHub API with the following script:



```
cut -f1 repos.tsv | while read repo; do 
    [ -f "${repo/\//@}.json" ] && continue; 
    echo $repo; 
    while true; 
        do curl -sS -u 'alexey-milovidov:***' "https://api.github.com/repos/${repo}" > ${repo/\//@}.json; 
        grep -F 'API rate limit exceeded for user' ${repo/\//@}.json && sleep 60 || break; 
    done;
done

```

(Sometimes I have a guilty pleasure writing shell scripts)


The data contains the details like the main repository language, the actual number of stars, forks and subscribers. The response JSON objects also have a high amount of redundancy.


I can load all of them into ClickHouse without caring of data types and nesting levels:



```
SET allow_experimental_object_type = 1;
CREATE TABLE repositories (data JSON) ENGINE = MergeTree;
INSERT INTO repositories FROM INFILE '*.json' FORMAT JSONAsObject;

```

And then calculate something interesting:



```
SELECT
    1 + rowNumberInAllBlocks() AS n,
    *
FROM
(
    SELECT DISTINCT
        data.full_name,
        data.stargazers_count,
        data.license.name
    FROM repositories
    WHERE data.language = 'C++'
    ORDER BY data.stargazers_count DESC
)
LIMIT 20

Query id: 175ccd7e-d689-493b-b0bc-57a584f09590

┌──n─┬─data.full_name────────────────────────┬─data.stargazers_count─┬─data.license.name───────────────────────┐
│  1 │ tensorflow/tensorflow                 │                164038 │ Apache License 2.0                      │
│  2 │ electron/electron                     │                101133 │ MIT License                             │
│  3 │ microsoft/terminal                    │                 82110 │ MIT License                             │
│  4 │ opencv/opencv                         │                 60681 │ Other                                   │
│  5 │ apple/swift                           │                 59164 │ Apache License 2.0                      │
│  6 │ pytorch/pytorch                       │                 55051 │ Other                                   │
│  7 │ protocolbuffers/protobuf              │                 53704 │ Other                                   │
│  8 │ x64dbg/x64dbg                         │                 38319 │ GNU General Public License v3.0         │
│  9 │ BVLC/caffe                            │                 32370 │ Other                                   │
│ 10 │ nlohmann/json                         │                 29284 │ MIT License                             │
│ 11 │ google/leveldb                        │                 28826 │ BSD 3-Clause "New" or "Revised" License │
│ 12 │ topjohnwu/Magisk                      │                 24989 │ GNU General Public License v3.0         │
│ 13 │ microsoft/calculator                  │                 24045 │ MIT License                             │
│ 14 │ CMU-Perceptual-Computing-Lab/openpose │                 23777 │ Other                                   │
│ 15 │ huihut/interview                      │                 23490 │ Other                                   │
│ 16 │ cmderdev/cmder                        │                 23453 │ MIT License                             │
│ 17 │ ClickHouse/ClickHouse                 │                 22957 │ Apache License 2.0                      │
│ 18 │ facebook/rocksdb                      │                 22198 │ Other                                   │
│ 19 │ mongodb/mongo                         │                 21409 │ Other                                   │
│ 20 │ apache/incubator-mxnet                │                 19938 │ Apache License 2.0                      │
└────┴───────────────────────────────────────┴───────────────────────┴─────────────────────────────────────────┘

```

So, ClickHouse is the 17th most popular C\+\+ repository on GitHub. Not bad.


Let me explain how dynamic subcolumns work:


There is the new `JSON` data type. You can also write it as `Object('JSON')`. This data type can parse arbitrary JSON and it contains dynamic subcolumns. You can have both regular types and `JSON` types in the same table. Dynamic subcolumns are created on insertion and are stored in column\-oriented format just like regular columns, so querying these subcolumns is as efficient as regular columns. The data types are inferred automatically and can be converted during background merges, so you can have different schemas in different INSERTs. Queries are using natural syntax like `data.license.name[1]` instead of `JSONExtractString(data, 'license', 'name', 1)` or `JSON_QUERY(data, '$.license.name[1]')`.


This feature is implemented by **Anton Popov**. It is available for preview in version 22\.3\. We will be happy to hear your feedback.


## **Performance Improvements** [\#](/blog/clickhouse-22-3-lts-released#performance-improvements)


There are so many performance optimizations in ClickHouse and every new release ClickHouse becomes even faster.


**Maksim Kita** has improved performance of insertion into MergeTree tables up to two times by sorting optimizations (if the order key is represented by several numeric columns).


If you have SELECT queries with a huge list in WHERE IN, these queries will work up to 3 times faster in ClickHouse 22\.3:



```
SELECT * FROM table
WHERE key IN (111, 222, ... a megabyte of something)

```

## **Local Cache For Remote Filesystem** [\#](/blog/clickhouse-22-3-lts-released#local-cache-for-remote-filesystem)


When ClickHouse is reading from the local filesystem, the data is cached by the OS in the page cache. Typical performance of reading from page cache from multiple threads on a server with multi\-channel memory is around 50 GB/sec, so the hot queries are really fast.


But if ClickHouse is reading from a remote filesystem, the OS does not see these reads and cannot use page cache. So, we need our own page cache in ClickHouse. Since version 22\.3, ClickHouse has a cache for remote filesystem, implemented by **Ksenia Sumarokova**. This feature is available for preview.


It gives [tremendous improvements in performance](https://youtu.be/GzeANZzPras?t=389). The cache is hybrid — it is using both the local disks and RAM.


## **What Else?** [\#](/blog/clickhouse-22-3-lts-released#what-else)


Read the [full changelog](https://github.com/ClickHouse/ClickHouse/blob/master/CHANGELOG.md) for the 22\.3 release and follow [the roadmap](https://github.com/ClickHouse/ClickHouse/issues/32513).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
