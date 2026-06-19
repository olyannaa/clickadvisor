# More Than 2x Faster Hashing in ClickHouse Using Rust


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# More Than 2x Faster Hashing in ClickHouse Using Rust

![DenisBolonin.jpeg](/_next/image?url=%2Fuploads%2FDenis_Bolonin_6a650936f7.jpeg&w=96&q=75)Denis BoloninOct 25, 2022 · 6 minutes read## Introduction [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#introduction)


At the moment, the ClickHouse DBMS codebase consists of several programming languages, but the main language for the DBMS itself is C\+\+. In this regard, the possibilities of integrating libraries in other compiled languages are quite limited. One such language is Rust. It is similar in performance to C and C\+\+. Rust’s rich type system and ownership model guarantee memory\-safety and thread\-safety. There are a fairly large number of useful libraries written on it, so we considered using them in ClickHouse.


## Integrating Rust into ClickHouse [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#integrating-rust-into-clickhouse)


### Building Rust [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#building-rust)


Rust has its own package manager called Cargo. It is used for downloading dependencies, Rust compilation and package distribution. On the other hand, ClickHouse uses CMake and Ninja build system. These two approaches to project building are not compatible by default, so we needed to implement some kind of integration for Rust build system. Our first approach was to implement our own CMake function, which will launch Cargo and then detect its output. This approach was successful and it allowed us to build ClickHouse with Rust libraries as dependencies, but it also had a big downside: we needed to change and reimplement parts of our function for each new Rust library. After some search we found an utility designed for integrating Rust libraries into CMake projects – Corrosion\-rs. It allowed us to integrate Rust projects much easier – with a simple 3\-line CMake files.


### BLAKE3 [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#blake3)


We decided to integrate BLAKE3 as an example Rust library. BLAKE3 is a high performance secure cryptographic hash function.


It was added as a submodule and connected to ClickHouse build system, but we still couldn’t use its methods in C\+\+ code. For that we needed to fix compatibility issues between Rust data types and C\+\+ data types. The solution was simple: we wrote a shim function in Rust. It takes variables with C data types as input, calls BLAKE3 hashing after casting data to respective Rust types and then returns the resulting hash in C format. We used C for compatibility because Rust Foreign Function Interface provides only C\-compatible types.


Because its input and return types were equal to C types, we created a .h header file with declaration of this function, which allowed us to finally use it in ClickHouse code.


## What about performance? [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#what-about-performance)


We measured BLAKE3 performance on three different inputs. Here is the diagram, comparing BLAKE3 to similar hash functions in ClickHouse:


![Diagram.png](/uploads/Diagram_ad34f5cbd2.png)
As you can see, BLAKE3 performs more than 2x faster than SHA224 or SHA256 and a bit faster than MD5\. Also, BLAKE3 is secure, unlike MD5 and SHA\-1 and protected against length extension, unlike SHA\-2\.


These results meet our expectations and comply with BLAKE3 authors’ results for 1KB input length:


![BLAKE3 orig.png](/uploads/BLAKE_3_orig_fc3b362a7a.png)
But what about shim methods? We used them to cast Rust and C data types before and after BLAKE3 call, so they require some time to do all the conversions. To measure the overhead created from casting we used perf top utility, and presented its data as a flamegraph:


![perf_flame_w_eng.png](/uploads/perf_flame_w_eng_9036f441f1.png)
Here we can see that most consuming part of a shim function is conversion of Rust hash data to C format and it takes about 1,15% of whole query time. Moreover, casting C input char pointer to Rust byte array type in the beginning takes almost no time, because convertion of pointer to string is intended to be 0\-cost and convertion to byte array has a constant cost in Rust.


## Problems [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#problems)


During BLAKE3 integration we encountered some problems. The first was connected with C\+\+ Memory Sanitizer, which wasn’t able to comprehend operations with memory in Rust and flagged them as false positive. It was resolved by using \_*msan*unpoison Memory Sanitizer function on input data and adding a version of shim method with more explicit byte array conversion. After all fixes false positives were gone and Memory Sanitizer was working correctly.


Another problem is connected with multiplatform building and linking. While most platforms supported by ClickHouse were configured easily using Cargo, some required additional configuration via CMake or specific packages/frameworks. For now, only one platform (aarch64\-darwin) remains unsupported, because of some troubles with linkage during build process.


## Conclusion [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#conclusion)


The possibility of integrating libraries in Rust language was implemented, and the BLAKE3 hash function was added as an example library. This allows us to:


1. Add and use other Rust libraries in ClickHouse in the future.
2. Use BLAKE3 in the future along with other hash functions in ClickHouse, taking advantage of its speed and security features.


## A comment from Alexey Milovidov [\#](/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust#a-comment-from-alexey-milovidov)


We want to add support for Rust in the build as an experiment. There is a vibrant community and there are many good, high\-quality libraries in Rust, that we can use in ClickHouse. At the same time, we want to make the integration as unobtrusive as possible. We are using the "you don’t pay for what you don’t use" principle: the Rust integration should not stand in your way and scream about how nice it is.


There were the following requirements for the integration:


- it should be optional \- the code should not require Rust for builds: if cargo is not installed, is should simply build without Rust libraries;
- static linking (no new dynamic libraries); it should not introduce dependencies on [new symbol versions from glibc](https://github.com/ClickHouse/ClickHouse/tree/master/base/glibc-compatibility); the binary should run on ancient Linux systems; [the binary should be monolithic](https://notes.volution.ro/v1/2022/01/notes/fbf3f06c/);
- support for cross\-compiling with the C\+\+ code as we always use cross\-compiling for our code (the hermetic build with custom [sysroot](https://github.com/ClickHouse/sysroot/) is used even if the target platform is the same as the host platform);
- support for build with sanitizers and fuzzing: they are relevant mostly for C\+\+ code, but the binary should link with the Rust code and work as well with sanitizers.


Meeting these requirements was much harder than we thought, but the result is better than I expected. There were no complaints about Rust \- when it is not installed, the project builds as usual, and when it is installed, the build simply works.


We selected one small library for a proof of concept. If the experiment will go alright, we can extend the usage to more libraries. At the same time, we don't have high expectations \- if there will be not enough enthusiasm, we can simply drop it.


I'm highly impressed by the work of Denis Bolonin that made it possible!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
