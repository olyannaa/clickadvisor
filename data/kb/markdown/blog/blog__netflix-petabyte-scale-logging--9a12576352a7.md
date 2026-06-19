# How Netflix optimized its petabyte\-scale logging system with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Netflix optimized its petabyte\-scale logging system with ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 23, 2025 · 9 minutes read
div.w\-full \+ p, pre \+ p {
 text\-align: center;
 font\-style: italic;
}


> **TL;DR**  
>   
> Netflix ingests 5 petabytes of logs daily with ClickHouse, serving 10\.6M events/second with sub\-second queries.  
>   
> Three optimizations unlocked this scale: generated lexers for log fingerprinting (8\-10x faster), custom native protocol serialization, and sharded tag maps that cut query times from 3 seconds to 700ms.


“At Netflix, scale drives everything,” says engineer Daniel Muino. He’s not kidding.


In its largest namespace, Netflix’s logging system ingests an eye\-popping 5 petabytes of data every day. On average, it processes 10\.6 million events per second, peaking at 12\.5 million (“unless something weird is happening—then it can go higher,” Daniel says) with each event averaging around 5 KB in size. Depending on the needs of a given microservice—of which there are over 40,000 at Netflix—logs are retained anywhere from two weeks to two years.


And while the system is overwhelmingly write\-heavy, it still fields an impressive 500 to 1,000 queries per second. Those queries are what engineers use to debug issues, monitor microservices, and keep the platform running for 300\+ million subscribers in 190 countries.


Safe to say, this is a scale that would overwhelm most logging platforms. Making that kind of interactivity possible—logs that are searchable within seconds, queries that feel instant—took not just the right database (ClickHouse!) but a series of carefully engineered optimizations.


At a [July 2025 ClickHouse meetup in Los Gatos](https://www.youtube.com/watch?v=LgGNxPl6c9k), Daniel shared how his team made it happen, including the three breakthroughs that made Netflix’s petabyte\-scale logging both fast and cost\-efficient.


## Inside Netflix’s logging architecture [\#](/blog/netflix-petabyte-scale-logging#inside-netflixs-logging-architecture)


Netflix’s logging setup is “fairly straightforward, nothing crazy,” Daniel says. “But in order to make that work, we had to make a lot of choices.”


Logs flow from thousands of microservices through lightweight sidecars, which forward events into ingestion clusters. After a brief buffer, data is written to Amazon S3 and a message is placed in Amazon Kinesis, triggering downstream processing. From there, a central hub application consumes the data, routes it into separate namespaces, and writes it to the appropriate storage tier.


ClickHouse sits at the heart of the system as the hot tier. It stores recent logs where speed is critical, powering fast queries and interactive debugging. “Thanks to ClickHouse, we’re able to serve this data very fresh,” Daniel says. “All the buffering we do along the way doesn’t really affect us much.”


For historical data, Netflix uses Apache Iceberg, which provides cost\-efficient long\-term storage and query capability at larger time scales. On top of both tiers, a query API automatically determines which namespaces to search, so engineers get a unified view without having to think about what’s under the hood.


![Netflix ClickHouse architecture](/uploads/Image_503743030_3300x1808_ce7d291bde.jpg)

Netflix’s logging architecture, combining ClickHouse for hot data and Iceberg for long\-term storage.



The result is a system that feels almost instantaneous. Logs are usually searchable within 20 seconds of being generated, far faster than Netflix’s 5\-minute SLA. In some cases, engineers can even stream live logs with two\-second latency. They can click into events, expand JSON payloads, group millions of messages by fingerprint hash, or drill into surrounding logs, all without waiting for queries to churn.


But as Daniel explains, this level of interactivity didn’t happen overnight. It took three big optimizations—in ingestion, serialization, and queries—to turn the system into what it is today.


### Learn about ClickStack [\#](/blog/netflix-petabyte-scale-logging#test)

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale.

[Learn more](https://clickhouse.com/use-cases/observability?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Optimization \#1: Ingestion \- Fingerprinting [\#](/blog/netflix-petabyte-scale-logging#optimization-1-ingestion---fingerprinting)


To make logs useful, Netflix first needs to group similar messages together. This process, called fingerprinting, helps engineers cut through the noise by collapsing millions of near\-identical entries into a single pattern. Without it, searching through logs at Netflix’s scale would be overwhelming, to say the least.


Early on, the team experimented with machine learning models to classify log messages into groups. It worked in theory, but in practice it was way too resource\-hungry. “It was extremely expensive, very slow, and it made the whole product not work,” Daniel recalls.


Next they turned to regular expressions, matching patterns in log text and swapping out values for generic tokens. That helped, but regex couldn’t keep up with 10 million events per second. “Recognizing entities from raw text is something compilers have been doing for a long time,” Daniel explains. “It’s basically the same problem with the same solution—you need a lexer.”


So the team rebuilt fingerprinting as a generated lexer using JFlex, a Java tool that produces optimized tokenizers. Instead of evaluating complex regex at runtime, the new system compiles patterns into efficient code. The payoff was huge: throughput increased 8\-10x, and average fingerprinting time dropped from 216 to 23 microseconds. Even at the 99th percentile, latency was much lower.


“It was a huge win,” Daniel says. “And it was basically just a rewrite.” That rewrite cleared one of the system’s biggest ingestion bottlenecks, and gave Netflix room to keep scaling.


## Optimization \#2: Hub \- Serialization [\#](/blog/netflix-petabyte-scale-logging#optimization-2-hub---serialization)


Once logs are fingerprinted, they still need to be written into ClickHouse at a rate of millions per second. Here, Netflix hit another bottleneck: serialization.


The team’s first implementation leaned on [JDBC](https://clickhouse.com/docs/integrations/language-clients/java/jdbc) batch inserts. It was simple and familiar, but also inefficient. Every prepared statement forced the client to negotiate schemas and serialization details with the database, adding overhead that scaled poorly. “I thought we could do better,” Daniel says.


So the team dropped down a level in the abstraction stack, using the [RowBinary](https://clickhouse.com/docs/interfaces/formats/RowBinary) format exposed by ClickHouse’s low\-level Java client. This meant manually serializing data column by column—writing map lengths, encoding [DateTime64](https://clickhouse.com/docs/sql-reference/data-types/datetime64) as nanoseconds since the epoch, and handling other quirks. It gave them a “huge performance boost,” Daniel says, but it still wasn’t enough.


“When I looked at the CPU and allocation profiles, it just bothered me so much,” he says. “Why is it doing more work than I want it to do? Why is it using more memory than I want it to use?”


The breakthrough came when Daniel read a [ClickHouse blog post benchmarking input formats](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient). The native protocol consistently outperformed RowBinary, but the Java client didn’t support it. Only the [Go client](https://clickhouse.com/docs/integrations/go) did. “So I just reverse\-engineered the Go client,” Daniel says.


Netflix built its own encoder that generates LZ4\-compressed blocks using the native protocol and ships them directly to ClickHouse. The result is lower CPU usage, better memory efficiency, and throughput equal to (and in some cases even better than) RowBinary.


“It’s not perfect yet, because I’ve only just finished it,” Daniel says. “But we’re on par with where we were before, and there’s a lot of room left for optimizations.”


## Optimization \#3: Queries \- Custom tags [\#](/blog/netflix-petabyte-scale-logging#optimization-3-queries---custom-tags)


If ingestion and serialization were mostly write\-heavy challenges, the third bottleneck came on the read side. Engineers at Netflix rely heavily on tags—dynamic key\-value pairs appended to each log event that let you filter by microservice, request ID, or other custom attributes. As useful as they are, tags also became one of the system’s biggest headaches.


“Custom tags are a huge problem for us,” Daniel says. “They are by far the most expensive query that is commonly used by our users.”


Originally, tags were stored as a simple [Map(String, String)](https://clickhouse.com/docs/sql-reference/data-types/map). Under the hood, ClickHouse represents maps as two parallel arrays of keys and values. Every lookup required a linear scan through those arrays. At Netflix scale, with up to 25,000 unique tag keys per hour and tens of millions of unique values, query performance degraded quickly.


Daniel talked it over with ClickHouse creator Alexei Milovidov, who suggested using [LowCardinality types](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality). That worked for keys, but values were far too numerous, so it only solved half the problem. “LowCardinality values was not an option,” Daniel notes.


The solution turned out to be surprisingly simple: shard the map. By hashing tag keys into 31 smaller maps, queries could jump directly to the right shard instead of scanning every key.


The difference was huge. A filtering query that once took three seconds dropped to 1\.3 seconds. A filter\-plus\-projection query fell from nearly three seconds to under 700 milliseconds. In both cases, the amount of data scanned shrank by five to eight times.


“Now, a query that used to cause us a lot of problems is somewhat okay,” Daniel says. And at Netflix’s scale, he adds, “That’s a big, big win.”


## The beauty of simplicity [\#](/blog/netflix-petabyte-scale-logging#the-beauty-of-simplicity)


Put together, these three optimizations—rethinking fingerprinting, rewriting serialization, and reshaping queries—have cleared bottlenecks and cemented Netflix’s logging system as one of the largest and fastest ClickHouse deployments anywhere.


Instead of slowing engineers down, the system now feels lightweight and interactive, even at Netflix’s otherworldly scale. That kind of responsiveness can be the difference between scrambling to chase outages and keeping the service running smoothly for hundreds of millions of viewers around the world.


In the end, Daniel credits the team’s success less to clever tricks than to disciplined engineering. “The key is more about how you simplify things in order to do the least amount of work,” he says.


Looking to transform your team’s data operations? [Try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
