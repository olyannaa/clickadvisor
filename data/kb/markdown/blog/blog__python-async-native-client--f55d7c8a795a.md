# Designing the new async\-native ClickHouse Python client


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Designing the new async\-native ClickHouse Python client

![](/_next/image?url=%2Fuploads%2FImage_from_Slack_2_c9a2dc1d9b.png&w=96&q=75)[Joe Spadola](/authors/joe-spadola)Mar 16, 2026 · 16 minutes read
div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

## Introduction [\#](/blog/python-async-native-client#introduction)


`clickhouse-connect` is the official ClickHouse Python client. It's open source, Apache\-2\.0 licensed, and the code can be found on [GitHub](https://github.com/ClickHouse/clickhouse-connect). It's available on [PyPI](https://pypi.org/project/clickhouse-connect/) and can be installed with `pip install clickhouse-connect`.


Work on the project started in February 2022 and was first published to PyPI at v0\.2\.8 in September 2022\. The original author built it out as a side project, and for the first 2\.5 years the focus was on building out a feature\-rich sync client, which it has become.


An async\-native client had been a popular request for some time, but without a dedicated resource it just wasn't going to happen quickly. As a workaround, in July 2024 we followed the common pattern of wrapping the sync client in a thread pool executor. This was performant enough and unblocked users who needed `clickhouse-connect` in async contexts. It worked well (and still does) for many use cases, but it carries inherent limitations like thread pool exhaustion under high concurrency, threads contending for the GIL ([global interpreter lock](https://wiki.python.org/moin/GlobalInterpreterLock)), and the memory overhead of maintaining OS thread stacks.


According to our cloud usage stats, `clickhouse-connect` is used by nearly 2200 organizations and has run almost 30 billion queries. 13% of `clickhouse-connect` users use it in async mode, but async mode accounts for 24% of all queries. In other words, async users run more than twice as many queries on average, which tells us async is disproportionately used by high\-volume, performance\-sensitive workloads.


## Motivation for the async\-native client [\#](/blog/python-async-native-client#motivation-for-the-async-native-client)


For I/O\-heavy Python workloads, an [event loop](https://en.wikipedia.org/wiki/Event_loop) is significantly more efficient at managing concurrency than OS threads. The GIL limits what threads can do in parallel, and threads can only scale so far. An event loop can efficiently manage hundreds of concurrent I/O operations. Spawning hundreds of OS threads to do the same is simply not practical for this use case.


So while the executor\-based approach provides a usable async client, it is not ideal for high\-concurrency workloads. As load increases, the thread pool saturates, I/O blocks, and tail latencies rise.


![Diagram comparing native-async network I/O with CPU parsing offloaded to a thread versus wrapping a synchronous client in a ThreadPoolExecutor](/uploads/Async_IO_Comparison_2_1_073764f5a3.svg)
Schematic showing the conceptual difference between native\-async network I/O (with offloaded CPU parsing) and wrapping an entire synchronous client operation in a ThreadPoolExecutor. Note that numbers are illustrative. Native async per\-host concurrency is configurable.


## High\-level design choices [\#](/blog/python-async-native-client#high-level-design-choices)


### Choosing an async HTTP library [\#](/blog/python-async-native-client#choosing-an-async-http-library)


The sync client uses the excellent [urllib3](https://urllib3.readthedocs.io/en/stable/) HTTP library, but it's synchronous only. We needed an async replacement. In Python, there are two main production\-grade choices: [aiohttp](https://docs.aiohttp.org/en/stable/) and [httpx](https://www.python-httpx.org/).


`httpx` is known for:


- its [requests](https://requests.readthedocs.io/)\-compatible API
- a clean, modern design
- unified sync and async interfaces
- a pure\-Python protocol stack ([httpcore](https://www.encode.io/httpcore/) \& [h11](https://h11.readthedocs.io/en/latest/))
- built\-in HTTP/2 support


`aiohttp` is known for:


- a longstanding asyncio\-native design
- being both an HTTP client and server framework
- high throughput in async workloads
- compiled accelerators for HTTP parsing and URL/header handling


For a high\-throughput database client, raw speed is the top priority, so `aiohttp` was the natural choice. And despite the client having many methods and helpers, relatively few of them actually touch the HTTP library directly. Most operations flow through a small number of internal methods that make the actual requests. This meant that whatever library we did end up choosing, it would be relatively straightforward to swap out later if needed, though, spoiler alert, we didn’t.


### The core challenge: CPU\-heavy parsing with async I/O [\#](/blog/python-async-native-client#the-core-challenge-cpu-heavy-parsing-with-async-io)


`clickhouse-connect` already has a mature, well\-tested data transformation layer that handles the heavy lifting of parsing [ClickHouse's Native binary format](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient#native-interface) into Python objects like column types, nullability, nested structures, etc. The main problem we faced is that this code is inherently CPU\-bound and synchronous. Rewriting it for async would mean duplicating thousands of lines of battle\-tested logic for no real benefit, since there's no I/O to await during parsing. Reusing the existing parsing machinery was a given from the start. The question was *how*.


#### Naïve approaches [\#](/blog/python-async-native-client#na%C3%AFve-approaches)


One approach is to read the full HTTP response body first, then hand those bytes to the existing parser in an executor thread. This is simple, but it’s a poor fit for a database client where result sets can be hundreds of megabytes or larger. Buffering the entire response before parsing increases peak memory usage and delays time\-to\-first\-row, because parsing cannot begin until the download is complete. Then parsing runs as a separate phase, so network I/O and CPU parsing do not overlap for that query. To be clear, `aiohttp`’s `await response.read()` still yields to the event loop so other coroutines can run but the core issue is loss of pipelining and avoidable memory pressure on large results.


Another approach goes the other direction. We could stream the response and parse it directly on the event loop as chunks arrive. This avoids the memory problem, but now the CPU\-bound parsing blocks the event loop. Parsing ClickHouse's Native format involves deserializing potentially millions of rows of typed columnar data. That takes real CPU time, and every millisecond spent parsing is a millisecond the application can't serve other requests.


Even worse, doing CPU\-heavy parsing on the event loop can throttle the query itself. While the loop is busy parsing, it’s not servicing socket reads. As receive buffers fill, TCP flow control slows the sender, so throughput drops and transfer becomes bursty instead of smooth. For large responses, this is a poor tradeoff, so this approach also doesn’t work for us.


So we're stuck between two bad options. We either block on I/O or block on CPU. What we really need is a way to stream data from the network asynchronously while parsing it synchronously in a separate thread, with the two sides coordinating without either one blocking the other.


#### The half\-sync/half\-async pattern [\#](/blog/python-async-native-client#the-half-synchalf-async-pattern)


This problem isn't uncommon. There's a well\-established concurrency pattern called the "half\-sync/half\-async" pattern. (See [here for the academic treatment](https://www.cs.wm.edu/~dcschmidt/PDF/PLoP-95.pdf), and [here for a more accessible read](https://java-design-patterns.com/patterns/half-sync-half-async/) with Java examples.) The idea is pretty straightforward. We separate the async I/O world from the synchronous processing world and connect them with a bounded queue that provides backpressure in both directions. This pattern shows up across many systems, from [Android's AsyncTask framework](https://www.linux.com/training-tutorials/android-asynctask-internal-half-sync-half-async-design-pattern/) to [ASGI servers](https://github.com/abersheeran/a2wsgi) that bridge async HTTP handling with synchronous WSGI applications.


In our case, the pattern has three parts:


1. First, we have an async producer that runs on the event loop. This is fine since it's pure I/O, just `await`ing socket reads. It reads chunks from the `aiohttp` response stream and pushes them into a bounded queue. The queue has a maximum size, so the producer naturally slows down if the consumer can't keep up. This backpressure is what keeps memory usage predictable.
2. Second, we have the sync consumer which runs in a thread pool executor. It pulls chunks from the queue, decompresses them if needed, and feeds them into the existing synchronous parser. The beauty of this is that as far as the parser is concerned, it's just reading from a byte stream. It doesn't know or care that there's an event loop on the other side feeding it data.
3. Finally, there is the queue itself which serves as the bridge. We built this around an `AsyncSyncQueue` class that exposes both sync and async interfaces to the same underlying buffer. It's bounded at 10 chunks, where each chunk is up to 1MB from the socket read. That means at most \~10MB of response data is buffered at any time, regardless of total response size. Errors are handled across the boundary too. If the server returns an error mid\-stream or the network drops, the producer pushes the exception object through the queue so the consumer sees it and can re\-raise on the parser side.


To be explicit, this is async\-native for network I/O, while CPU\-bound parsing intentionally remains synchronous and runs off the event loop in executor threads. And because the producer and consumer run concurrently, they naturally overlap. So while the parser crunches through chunk `N`, the event loop is already downloading chunk `N+1`. Compare this to the sync client (and the legacy async client, which wraps it), where these operations are strictly sequential:


![Animation showing pipelined read and parse with the half-sync/half-async pattern versus sequential processing in the legacy client](/uploads/Click_House_Python_Client_Animation_1_54f305eb3d.svg)
*Animation showing the difference between a sequential and a pipelined read \& parse design*


The bounded queue is what makes this overlap work well in practice. However, you have to be sensible with the max allowed size of the queue. If it's too small, you end up with ping\-pongy behavior that approaches sequential behavior. If you allow it to be too large, or even unbounded, you end up back with the memory problem if the consumer can't keep up. For large result sets, this pipelining effect meaningfully improves total query time since network I/O and CPU parsing happen in parallel rather than taking turns.


The same pattern works in reverse for inserts. The existing serialization logic builds insert blocks synchronously in an executor thread and pushes them into the queue. The event loop pulls from the other side and streams them over the network via `aiohttp`. It's the same queue primitive, with the same backpressure effect, but the roles are reversed.


## Benchmarks [\#](/blog/python-async-native-client#benchmarks)


Ok, enough theory. Let's see how it actually performs. We benchmarked the new async\-native client against the "legacy" async client (the executor\-based wrapper around the sync client).


### Setup [\#](/blog/python-async-native-client#setup)


We ran the benchmark against a ClickHouse Cloud instance with the following configuration:


- **ClickHouse Cloud instance:**
	- Server version 25\.10\.1\.7462
	- AWS r5ad.2xlarge (fractional pod)
	- us\-west\-2 (Ohio)
	- 4 vCPUs / 8 GiB RAM
	- 30 GiB local NVMe SSD cache \+ S3 storage
- **Client machine:**
	- MacOS Tahoe 26\.3
	- M4 Max
	- 36 GB RAM
	- 14 CPU cores
	- Location, west coast US
- **Network:** 64\.4ms avg latency
- **clickhouse\-connect version:** v0\.12\.0\.rc1
- **Python:** 3\.12\.11


Both clients were configured with 32 connection/thread pool workers. The async client uses `aiohttp` with `connector_limit=32`, while the legacy client uses `urllib3` with a matching pool size and 32 executor threads.


A few notes on methodology. Each scenario executes 50 to 200 individually timed operations per run depending on the scenario, and each scenario runs 5 times. We report mean throughput with standard deviation. P95 latencies are computed per\-run and reported as mean ± standard deviation across runs, giving us a measure of how *stable* tail latency is, not just how fast it is. Scenario execution order is randomized and within each scenario, as is which client goes first. There's a brief cooldown between scenarios to let the server settle. We use geometric mean for the aggregate speedup ratio.


### Results [\#](/blog/python-async-native-client#results)




| Scenario | Concurrency | Async (op/s) | Legacy (op/s) | Async P95 | Legacy P95 | Speedup |
| --- | --- | --- | --- | --- | --- | --- |
| Select 100 rows | 1 | 12\.9 ± 0\.2 | 13\.1 ± 0\.0 | 78\.0 ± 0\.7 ms | 77\.7 ± 0\.4 ms | 0\.99x |
| Filtered query | 16 | 157\.0 ± 17\.4 | 158\.5 ± 12\.5 | 139\.4 ± 28\.9 ms | 135\.2 ± 30\.2 ms | 0\.99x |
| Join query | 16 | 139\.3 ± 15\.7 | 118\.6 ± 51\.0 | 154\.7 ± 68\.0 ms | 439\.2 ± 722\.2 ms | 1\.17x |
| Aggregation | 32 | 290\.4 ± 49\.1 | 258\.5 ± 123\.2 | 191\.9 ± 60\.3 ms | 882\.3 ± 1580\.6 ms | 1\.12x |
| Large result (10k rows) | 4 | 35\.4 ± 3\.0 | 25\.0 ± 3\.4 | 209\.9 ± 164\.1 ms | 330\.3 ± 212\.7 ms | 1\.41x |
| Insert 10 rows | 32 | 28\.1 ± 0\.8 | 26\.9 ± 0\.7 | 1276\.9 ± 70\.6 ms | 1317\.8 ± 11\.6 ms | 1\.05x |
| Insert 100 rows | 32 | 28\.3 ± 2\.0 | 24\.5 ± 5\.8 | 1234\.2 ± 21\.9 ms | 1955\.2 ± 1592\.9 ms | 1\.15x |
| Mixed workload | 32 | 69\.5 ± 15\.1 | 46\.2 ± 10\.5 | 1160\.2 ± 68\.8 ms | 1810\.6 ± 1338\.3 ms | 1\.51x |
|  |  |  |  |  | **Geometric mean:** | **1\.16x** |


### What the numbers tell us [\#](/blog/python-async-native-client#what-the-numbers-tell-us)


The geometric mean across all scenarios is **1\.16x**. We ran this benchmark several times and while individual scenarios do vary between runs (which is natural and expected against a real cloud instance), the geometric mean consistently settles in the 1\.16\-1\.18x range.


A few things worth pointing out:


1. **The async client gets faster as concurrency goes up.** At `concurrency=1`, the two clients are dead even at 0\.99x. That makes sense because with a single concurrent operation, there's nothing for the event loop to manage. At 32 concurrent operations, the differences emerge: 1\.12x on aggregation, 1\.51x on the mixed workload. The event loop is simply better at juggling many concurrent I/O operations than a thread pool, especially in Python where the GIL limits what threads can actually do in parallel.
2. **Tail latency tells an even more interesting story than throughput.** Look at the P95 columns, and not just the values but the ± numbers. The legacy client's P95 standard deviations are enormous: ±722ms on joins, ±1581ms on aggregation, ±1593ms on inserts, ±1338ms on the mixed workload. Its tail latency is essentially a coin flip between "decent" and "terrible" from one run to the next. The async client's worst P95 standard deviation is ±164ms on large results. Across all scenarios, the average P95 is 556ms for async vs 869ms for legacy.


This matters for production workloads. When P95 can swing from sub\-200ms to over 4 seconds between runs, that kind of variance can be problematic. The async client gives you *predictable* tail latency, not just faster tail latency.
3. **Throughput is also more stable.** The legacy client's aggregation throughput has a standard deviation of ±123\.2, which is nearly half its mean of 258\.5\. The async client on the other hand shows ±49\.1 on a mean of 290\.4\. For inserts, the async client varies by ±0\.8 and ±2\.0 op/s while the legacy client swings by ±0\.7 and ±5\.8\. You don't just want fast. You want *consistently* fast.


So where does this improvement come from? At low concurrency, the async client matches the legacy one, which tells us the overhead of the queue bridge is negligible and the underlying HTTP libraries are roughly on par. The gains at high concurrency come from two places: the event loop handles many concurrent connections without OS thread scheduling overhead, and the pipelining effect means network I/O and parsing overlap instead of taking turns. The legacy client's thread pool saturates earlier because each thread holds a connection, occupies a stack, and contends for the GIL.


It's worth noting that this benchmark is deliberately conservative. We capped both clients at 32 connections/threads to create a strict apples\-to\-apples comparison of per\-operation efficiency. In practice, the event loop's advantage grows as concurrency increases. An event loop can comfortably manage hundreds of concurrent connections with negligible overhead because a suspended coroutine is just a small state object in memory. A thread pool doing the same means hundreds of OS threads, each with its own heavy stack, all contending for the GIL and competing for CPU time on the OS scheduler. And eventually we reach a point where the threads aren't doing useful work, they're just waiting. The 1\.16x geometric mean reflects what you gain even when the thread pool isn't being pushed past its comfort zone. At even higher concurrency levels, the gap widens even more.


## Try it out! [\#](/blog/python-async-native-client#try-it-out)


If you've made it this far, you're either genuinely interested in this stuff or you have a vested interest in it. If the former, cool, we're nerds too. If the latter, you can help! `clickhouse-connect` v0\.12\.0rc1 is published and ready to test. The [release notes are on GitHub](https://github.com/ClickHouse/clickhouse-connect/releases/tag/v0.12.0rc1) and you can install it with:



```

```
1pip install clickhouse-connect[async]==0.12.0rc1
```

```

We're actively seeking feedback on how the new async client works for your workloads.


## Conclusion [\#](/blog/python-async-native-client#conclusion)


To be clear, the executor\-based async client served us well for nearly two years and it's still a perfectly valid option. It unblocked a lot of users and handled real production workloads quite well. But having a dedicated resource on the project means we can invest in these kinds of deeper improvements that just weren't feasible before. The result is a ground\-up async\-native client that's faster, more stable under load, and more efficient with resources. It's been one of the most requested features for the project, and we're glad to finally ship it!


As [ClickHouse](https://github.com/clickhouse/clickhouse) grows in popularity, so does the ecosystem of language clients around it. `clickhouse-connect` is the officially supported ClickHouse Python client, maintained by a dedicated team at ClickHouse. If you run into bugs, have feature requests, or want to contribute, we'd love to hear from you. Issues and PRs are always welcome on [GitHub](https://github.com/ClickHouse/clickhouse-connect)!

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-104-get-started-today-sign-up&utm_blogctaid=104)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
