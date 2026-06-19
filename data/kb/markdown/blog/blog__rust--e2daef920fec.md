# A Year of Rust in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# A Year of Rust in ClickHouse

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Apr 1, 2025 · 18 minutes readRust is a great programming language for terminal applications, fantasy consoles, and web3\. If you do an experiment and say "C\+\+" anywhere on the Internet, in a minute someone will chime in and educate you about the existence of Rust. Sadly, ClickHouse is written in C\+\+, not in Rust. If only we had a chance to attract a large army of passionate Rust professionals... So, I decided that we must add Rust to ClickHouse.


The goal was not to rewrite ClickHouse in Rust \- this would be a waste of time. We write ClickHouse in C\+\+ and rewrite some parts [from C\+\+ to a better C\+\+](https://github.com/ClickHouse/ClickHouse/pull/56556). Rewriting is never an end goal, although I know examples when engineers rewrite code [from Rust in Rust](https://db.cs.cmu.edu/events/building-blocks-glaredb-sean-smith/) if they like to rewrite everything in Rust. We should allow writing new system components in Rust. It should be integrated into the build system, so the Rust code interoperates with C\+\+, and it is built and tested together with no complications.


## First Steps [\#](/blog/rust#first-steps)


The first step was to find a small component to kick off the Rust integration. This component should not be in the critical path, it should be something that we can rip off at any time, so if our engineers become too nauseous from Rust poisoning, we just roll it back and forget. At the same time, it should be something large enough to test the integration to the build system. To not risk the mental health of our precious senior C\+\+ developers, I outsourced this task to an undergrad student. To be honest, it's much easier to find Rust experts among undergrad students than inside the company. Rust is prominent in crypto and web3, so the first component to test it was \- the integration of the **BLAKE3** hash function into ClickHouse. At that time, BLAKE3 was only implemented in Rust, so it was at least somewhat reasonable.


## BLAKE3 [\#](/blog/rust#blake3)


In a few months, thanks to **Denis Bolonin**, we had [the first code in Rust in ClickHouse](https://github.com/ClickHouse/ClickHouse/pull/33435). Rust was added to CMake build scripts using the ["corrosion"](https://github.com/corrosion-rs/corrosion) integration; a dedicated directory for Rust code was [added to the project tree](https://github.com/ClickHouse/ClickHouse/tree/master/rust), and we created examples of adding C\+\+ wrappers for Rust libraries. You can read more about this contribution [in the blog post](https://clickhouse.com/blog/more-than-2x-faster-hashing-in-clickhouse-using-rust).


![BLAKE3 vs other hash functions](/uploads/Diagram_ad34f5cbd2_ae41aa9a30.png)
## Skim [\#](/blog/rust#skim)


We have made it possible, and we opened floodgates to let the brilliant Rust developers into the ClickHouse codebase! So now they can write something other than new versions of old terminal applications. I was eagerly checking the list of pull requests for the first external contribution by Rust lovers... So they did come! The [first external pull request with Rust](https://github.com/ClickHouse/ClickHouse/pull/44239) was to improve our terminal application, clickhouse\-client, by adding interactive history navigation. Note: before that, [it was already added by calling a subprocess](https://github.com/ClickHouse/ClickHouse/pull/41730), but thanks to the integration with Rust, now we build and link this code into the ClickHouse binary. However, the Rust library [has a bug and crashed](https://github.com/skim-rs/tuikit/pull/51).


![output.gif](/uploads/output_33afc7028f.gif)
After adding a second Rust library, skim, we found that the BLAKE3 function is already present in the LLVM's C\+\+ codebase, which we also use. After upgrading LLVM, it was found much simpler to use BLAKE3 from there rather than with a Rust library. And to prove that the Rust integration works and is supported in the CI, it is enough to have only one Rust library. So, we [replaced BLAKE3 from Rust to C\+\+](https://github.com/ClickHouse/ClickHouse/pull/57994), and there was no noticeable difference in performance.


## PRQL [\#](/blog/rust#prql)


The third library in Rust that we added to ClickHouse was PRQL. It is a query language, an alternative to SQL, which allows expressing queries in a pipelined, composable form. As a downside, it is more syntax\-heavy than SQL, reminding something like Clojure. It is popular on the Internet \- someone shows PRQL, everyone else thinks "What a wonderful idea, and, also, Rust" and gives this project a star on GitHub. This is, by the way, [how most of Rust projects get their stars on GitHub](https://play.clickhouse.com/play?user=play#U0VMRUNUIGZ1bGxfbmFtZSwgc3RhcmdhemVyc19jb3VudCwgZGVzY3JpcHRpb24gRlJPTSBnaXRodWJfcmVwb3NfaGlzdG9yeSBXSEVSRSBsYW5ndWFnZSA9ICdSdXN0JyBPUkRFUiBCWSBzdGFyZ2F6ZXJzX2NvdW50IERFU0MgTElNSVQgMSBCWSBmdWxsX25hbWUgTElNSVQgMTAwMA==). It doesn't look like someone wants to use this language, but what we want is to ride the hype. Another student [selected](https://github.com/ClickHouse/ClickHouse/pull/50050) the integration of PRQL in ClickHouse as a graduate work.


An example of a SQL query in the ClickHouse dialect:
![SQL example](/uploads/Screenshot_20250401_002936_8a37cc0fea.png)


An example of the same query in PRQL:
![PRQL example](/uploads/Screenshot_20250401_003002_c1b621ac20.png)


After a few months, thanks to **Alexander Nam**, we had [PRQL support merged](https://github.com/ClickHouse/ClickHouse/pull/50686) into the ClickHouse codebase. ClickHouse has support for switchable dialects. Any time, you can write "SET dialect \= 'prql'" or 'kusto', or set it back to 'sql' to switch between different languages. You can specify the dialect in the user's profile, or in the HTTP API's parameter, like any other setting, and pass your queries in the selected dialect. However, there are some downsides of alternative dialects, like the lack of interactive syntax highlighting for all dialects except SQL, and poorer integration with built\-in functions and extensions.


Regardless of questions on its usefulness, PRQL brought us better confidence in Rust. After having two Rust libraries in our codebase, we started to understand that it would be hard to get rid of Rust, and we could tolerate it.


## Delta Kernel [\#](/blog/rust#delta-kernel)


This is the first library we have added not just for the sake of Rust, but for practical needs. Delta Lake is an open data lake format from Databricks. It mimics the operation of [MergeTree](https://clickhouse.com/docs/parts) tables in ClickHouse but is based on Parquet files in object storage. Data lakes and "Lakehouse" (a new term, that sounds surprisingly similar to ClickHouse, but is different) \- are increasingly popular ways for managing data in large organizations, as there is a benefit when the data format is independent of the storage engine. So, one engine (such as Spark) can write into a data lake in the Iceberg or Delta Lake format, and another engine (such as ClickHouse) can run queries on top of the data lake, so the whole architecture is named "data lakehouse".


The problem is that there are no good C\+\+ implementations for either Iceberg or Delta Lake. Either you use Java (which would be a shame for us) or write it from scratch in C\+\+. At first glance, it is not too hard to write Iceberg and Delta Lake implementation in C\+\+, because each format is represented by these components: \- a bunch of Parquet files on object storage; \- a bunch of metadata files, and snapshot descriptions in formats like JSON and Avro; \- a catalog, which is an API to find the tables. We already had C\+\+ implementations of each of the data lake formats: Iceberg v1, v2, Delta Lake, and Apache Hudi. However, these implementations were sketchy, with many corner cases unsupported, and they are not particularly pleasant to write (no C\+\+ engineer can be excited by the task of "read this JSON file and follow the spec precisely").


Here is the area where the increasing popularity of Rust showed in the best way. Recently, Databricks created the [official library for Delta Lake](https://github.com/delta-io/delta-kernel-rs) in Rust, and we used it, replacing our old C\+\+ code. See the [presentation from Oussama Saoudi](https://www.youtube.com/live/1XnA9_s5YOM?si=YIgOs84TiP9RmfvC&t=2115), Software Engineer at Databricks at our release call. We also improved the quality of the library for everyone, as we found and [fixed a bug](https://github.com/delta-io/delta-kernel-rs/pull/656) and [added a feature](https://github.com/delta-io/delta-kernel-rs/pull/659). It was [the most complex and the most real integration](https://github.com/ClickHouse/ClickHouse/pull/74884) of Rust into ClickHouse. So let's review what problems we had to solve...


## Problems [\#](/blog/rust#problems)


## Supply chain [\#](/blog/rust#supply-chain)


The initial integration of Rust was [downloading libraries from the Internet](https://github.com/ClickHouse/ClickHouse/issues/61741) during the build, by running cargo. But our build must be hermetic and [reproducible](https://reproducible-builds.org/). It must work without internet access, and it should not depend on 3rd\-party services, as it could be a supply\-chain problem. Also, we should build everything from the source code \- no binary blobs in the repository.


This problem was solved initially by [suggesting a way to disable Rust](https://github.com/ClickHouse/ClickHouse/pull/61938), then by [stashing dependencies in the docker image](https://github.com/ClickHouse/ClickHouse/pull/52395), and finally, by [vendoring all dependencies](https://github.com/ClickHouse/ClickHouse/pull/62297), although it was [not final](https://github.com/ClickHouse/ClickHouse/pull/77695).


## Complex wrappers [\#](/blog/rust#complex-wrappers)


Rust is a memory\-safe programming language, but to the surprise of our contributors, the first attempt to add Rust code often leads to a [segmentation fault](https://github.com/ClickHouse/ClickHouse/pull/57876). This is because the interop between Rust and C\+\+ requires writing the wrappers, and it has to be done with extra care to not mess up with things like who owns the memory, and in which order it is deallocated. It's not enough to be a Rust engineer to be able to do it properly. Thankfully, we use fuzzing in the CI system, and these types of errors are found before the merge.


## Panic [\#](/blog/rust#panic)


![Okay, Panic](/uploads/OK_panic_c1e0d20a65.gif)
(Airplane!, Paramount Pictures, 1980\)
One of the most visible downsides of Rust is the lack of exceptions (however, it is [possible to hack around it](https://github.com/iex-rs/lithium)). It uses error values instead and implements it fairly well (much better than, say, Go or C). However, it requires an overhead in the code for every possible exceptional situation. You have to do it not only for, say, an error in parsing a JSON from a user, or a socket disconnection, but also for low\-level errors from the operating system. In C\+\+, exceptions will propagate through the stack and could be reported by the server's query processing thread. In Rust, often people use "panic" when they don't want to take the overhead of handling the error, and "panic" will terminate the program. This is okay for batch applications, which cannot meaningfully handle these errors, but not ok for multi\-tenant servers, which have many query\-processing threads.


Fuzzers in our CI automatically [found a problem](https://github.com/ClickHouse/ClickHouse/issues/60511), that certain misformatted [PRQL queries can lead to panic](https://github.com/PRQL/prql/issues/4280) and crash the server. The authors of PRQL promptly [fixed the error](https://github.com/PRQL/prql/pull/4285). This is one of the advantages of having a C\+\+ codebase \- you learn to have so much power in your CI system, that it will easily find bugs inside any Rust code as well, see [1](https://presentations.clickhouse.com/2021-cpp-siberia/index_en.html), [2](https://clickhouse.com/blog/buzzhouse-bridging-the-database-fuzzing-gap-for-testing-clickhouse), and [3](https://clickhouse.com/blog/fuzzing-click-house).


To be honest, this is not different from a problem you find in many C libraries, when they use asserts to catch "impossible" errors, but our CI immediately proves these errors are very much possible. We are fixing Rust libraries in the same way how we fix C libraries. Also, panics in Rust actually work like exceptions by [unwinding the stack](https://github.com/ClickHouse/ClickHouse/pull/59447), and this was also [used as a solution](https://github.com/ClickHouse/ClickHouse/pull/60615).


## Sanitizers [\#](/blog/rust#sanitizers)


When you write in C\+\+ you always use sanitizers. It's important to use four sanitizers: Address Sanitizer (checks invalid memory accesses), Memory Sanitizer (checks for [uninitialized memory usage](https://heartbleed.com/)), Thread Sanitizer (checks for data races), and UB Sanitizer (checks for ill\-formed code leading to undefined behavior), so we do it in our CI. We do it extremely thoroughly, as all sanitizers run for all types of test suites in every pull request and every commit in the master and release branches, and we do it with extra hardening, randomization, for stress tests, and fuzzing.


You might say, [sanitizers are unneeded in Rust](https://github.com/ClickHouse/ClickHouse/issues/50525) because Rust is blazingly safe. But the problem is \- now we have a C\+\+ application with a drop of Rust, and we must continue to use sanitizers for the whole application. What happens if C\+\+ allocates a chunk of memory, then we call a Rust function to fill it with the data, and then C\+\+ code will read from this memory? If we build with MSan, all memory writes have to be instrumented, so next time when someone reads from the memory, MSan can know that the memory was previously initialized. It means that every code, including Rust, has to be [built with the instrumentation by MSan](https://github.com/ClickHouse/ClickHouse/pull/50541) (another option is to call **\_\_msan\_unpoison** manually for the data from Rust).


Instrumentation with sanitizers is supported by Rust, but MSan is available only in the "nightly" (bleeding\-edge) Rust toolchain, so we had to put efforts for specifying this version of the toolchain and [pin it for a particular version](https://github.com/ClickHouse/ClickHouse/pull/51903), so it [does not break over time](https://github.com/ClickHouse/ClickHouse/pull/51721).


For some reason, we also had to [disable](https://github.com/ClickHouse/ClickHouse/pull/55378) Thread Sanitizer for Rust.


## Cross\-compilation [\#](/blog/rust#cross-compilation)


ClickHouse builds with cross\-compilation, which means \- we can use x86\_64 Linux machine (the "host platform" \- where the build is done) to build ClickHouse for AArch64 mac (the "target platform" \- is what we build for), or vice\-versa. In fact, even if the host platform is identical to the target platform, e.g., when we build on x86\_64 Linux for x86\_64 Linux, we still use the cross\-compilation mechanism, to ensure that our build process does not depend on the platform or the environment, but depends entirely on the source code from our repository. This allows hermetic and reproducible builds that anyone can validate.


ClickHouse is very portable. For example, people from IBM want to run ClickHouse on big\-endian s390x systems, so we build it in our CI. My old friend, who lives in a garage with five cats wants to run ClickHouse on FreeBSD, so we build it for FreeBSD (the cats are nice).


![Cats](/uploads/IMG_20250320_102733_a2a8434abd.jpg)
It turns out it is not so easy in Rust. Well, maybe it is easy in Rust, and even easier than in C\+\+, but when you [use Rust and C\+\+ together](https://github.com/ClickHouse/ClickHouse/pull/59309), it is [not easy](https://github.com/ClickHouse/ClickHouse/pull/76921).


## Library linking [\#](/blog/rust#library-linking)


ClickHouse build is restricted from using any libraries from the system \- we isolate the build by making it independent of the operating system distribution. However, delta\-kernel\-rs depends on another library, named "reqwest", and it wants to link OpenSSL from the system, while we require static linking of the in\-tree build of OpenSSL. We [solved this problem](https://github.com/ClickHouse/ClickHouse/pull/74884/files#diff-c4ecba9a35ea888742e435fcf73d8011999e4f586d2c96d9106e1bef1d5e4049R70).


## Symbol sizes [\#](/blog/rust#symbol-sizes)


C\+\+ templates are notorious for slowing down compilation, bloating binary sizes, and generating very long symbol names (symbol name is the name of a piece of code or data in the binary file, used by the linker to bind different libraries together). But Rust can be even worse. It also has compile\-time code generation, and it can go out of control as well. After adding PRQL, I was surprised by the binary size increase and found that symbols from PRQL [approach 85 KB size](https://github.com/PRQL/prql/issues/3768) (which is not the code, just the generated function names!). The author of PRQL promptly [fixed this problem](https://github.com/PRQL/prql/pull/3773). Also, we [disabled debug info](https://github.com/ClickHouse/ClickHouse/pull/59306) for all Rust libraries, because as Rust is safe, who needs to debug it?


![Large symbol names in Rust](/uploads/symbols_b735321de4.png)
An example of a symbol name from Rust. It is about 300 times longer than what fits in the picture.
I found the offending code using my binary visualizer, which is available at the `/binary` handler in ClickHouse.


![Binary Visualizer](/uploads/413521001_a6a05c0d_078d_46ca_91b2_0a2e2ea048b1_597965a2bd.png)
ClickHouse binary code visualized. Try to find Rust here.
Update: While writing this article I found that the problem is not fixed, and it became worse: now some symbols from Rust approach [almost a megabyte in size](https://pastila.nl/?0000abbf/bae03f66ff43f46095c871704539ed44#rpdnTwh42L+Hf42S73NEGg==). I have to fix it urgently.


## Composability [\#](/blog/rust#composability)


There is a problem, when our C\+\+ code uses some conventions to do things like managing connections to external storages, or accounting of allocated memory, and Rust code uses other conventions. We maintain connection pools for S3, we ensure that requests use just the right amount of parallelism, spread across multiple endpoints uniformly, and remain alive just the right time to allow proper rebalancing and avoid slow start, and connections use a proper exponential backoff, proven in practice. When anything in our code allocates memory, we account for it in the query context, to control the memory usage. But it’s hard to expect the level of composability from external libraries to support providing custom memory allocators, custom connection pools, etc. Maybe this is common in Haskell or Julia, but good luck using them. Inevitably, a Rust library will do something slightly differently, and then we will have to patch it. Now it means that we have to sink deeply into the Rust code. The amount of trouble was not evident at the start of the journey.


## Build profiling and caching [\#](/blog/rust#build-profiling-and-caching)


Our build infrastructure supports distributed cache and profiling of the build process. Adding Rust means that we have to [support the caching](https://github.com/ClickHouse/ClickHouse/pull/52865) and profiling of Rust builds as well. In practice, it means that for a long period of time, we work without a build cache for Rust and pay more money for it.


## Dependency management [\#](/blog/rust#dependency-management)


Rust has a highly modular ecosystem, and libraries are composed much better than in C\+\+. As a downside, Rust libraries typically have a large fan\-out of dependencies, much like Node.js. This requires taking care to avoid the [blow\-up of dependencies](https://github.com/ClickHouse/ClickHouse/pull/52316), and to deal with annoyances of dependabot.


## How is Rust going? [\#](/blog/rust#how-is-rust-going)


**Rust is going great!** If your friend is eager to write something in Rust, please invite them to ClickHouse, and we guarantee a warm welcome.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
