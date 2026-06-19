# The three villains to agentic observability: retention, sampling and rollups


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The three villains to agentic observability: retention, sampling and rollups

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)[Mike Shi](/authors/mike-shi)Apr 8, 2026 · 21 minutes read![banner_3_villians.jpg](/uploads/banner_3_villians_70f00b1ef3.jpg)
*Are you sampling your trace just to keep costs under control?*


*Are you rolling up high\-cardinality metrics to make them queryable?*


*Are you limiting retention of your logs because storing everything simply isn't affordable?*


These patterns have become so common in observability that they are often treated as best practices with vendors marketing these as capabilities just to mask shortcomings. At ClickHouse we believe they are workarounds and reflect the constraints of the systems behind them, not the needs of the engineers using them.


How did we arrive at a world where SREs must police what data to keep, discard, or aggregate? And more importantly, does it need to stay this way?


In this post, we examine retention, sampling, and roll\-ups as the three constraints shaping modern observability. These are not neutral design choices, but limitations imposed by storage engines that struggle with scale, cost, and high\-cardinality data, and by SaaS platforms that pass those constraints on to users.


These trade\-offs were once tolerable. Human operators could compensate for missing data with experience and intuition. But that assumption is breaking down. While at least [90% of practitioners see value in using AI to surface anomalies and assisting with root cause analysis](https://grafana.com/observability-survey/#ai-in-observability-transparency-is-key-autonomy-is-the-next), these systems are not designed to support it. As AI and agent\-driven workflows become central to observability, sampling, aggregation, and short retention become far more damaging. Not only do they remove the context required for automated reasoning, but make it harder for agents to justify their conclusion \- something over [95% of practitioners demand](https://grafana.com/observability-survey/#observability-practitioners-overwhelmingly-want-ai-to-show-i).


What were once acceptable compromises are now active limitations. If we are to build systems that can support automated diagnosis and reasoning, we need to remove these constraints.


If we can, the result is not just fewer trade\-offs, but a fundamentally better model for observability: no blind spots, faster resolution times, and the complete context required for the next generation of agent\-driven workflows.

### Get started today

Interested in seeing how Managed ClickStack works for your observability data? Get started in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?intent=o11y&loc=blog-cta-343-get-started-today-sign-up&utm_blogctaid=343)## Retention: The memory tax [\#](/blog/three-villains-agentic-observability#retention-the-memory-tax)


Retention is one of the first constraints every observability user is asked to think about. It becomes an almost automatic consideration. How long should logs be kept? How far back should traces go? What is affordable?


To some degree, this is reasonable. Not all data needs to be stored indefinitely, and there are valid reasons to expire data over time. But the problem is not whether retention exists, it is that it has become a primary concern \- often forcing teams into extremely short windows. Logs are often only retained for seven to fourteen days, with traces treated even more aggressively due to their volume and/or cardinality.


This is not driven by user needs but by system limitations. Many systems rely on SSD\-backed storage to deliver query performance, and when combined with poor compression, this makes long\-term retention costly. As a result, these costs are either absorbed or passed on, forcing end users to treat retention as a budgeting problem.


![](/uploads/three_villains_apr2026_image12_413776037f.png)
*To extend retention, teams introduce tiers, pushing data into progressively cheaper and poorer performing storage. While allowing longer retention, this adds complexity and means querying historical data requires rehydration or slower queries.*


But this should not be the case. With high compression and object storage, the economics change completely. If we can store on object storage at roughly $0\.025 per GB, and combine this with 50x compression, raw data can be retained for a fraction of typical costs. Retention at 30 days, 60 days, or even a year should be a default. **Data expiry should be driven by compliance or policy, not cost pressure.**



> Object storage should not mean managing storage tiers. Users should not have to decide what data is hot, warm, or archived to object storage. All data should be ingested and treated equally, with frequently accessed data accelerated automatically based on query patterns. Introducing tiers only adds complexity and operational burden, with users constantly needing to think what to store where, without addressing the underlying problem.


Removing this constraint does more than reduce operational burden. It unlocks entirely new ways of working. Long\-term retention enables analysis of seasonal patterns, historical regressions, and previously unseen issues. A single log pattern can be traced back across months of data to understand when a bug first appeared and which users were affected.


![](/uploads/three_villains_apr2026_image6_8bd07c984a.png)
*Cyclic patterns are challenging for an agent to identify if the data is not present.*


As agents become part of the observability workflow, access to historical context becomes critical. Human operators carry implicit knowledge of past incidents and patterns, but agents do not. Without long\-term data, they cannot distinguish anomalies from expected behavior or reason about trends. Limiting retention does not just reduce visibility, it constrains their ability to function.


For these reasons, retention is our first villain. Not because data should never expire, but because the burden of deciding what to keep has been pushed onto the user due to costs imposed by underlying storage systems.


## Sampling: Observability with holes [\#](/blog/three-villains-agentic-observability#sampling-observability-with-holes)


Sampling is where we begin to drop data by design. Unlike retention, which limits how far back we can look, sampling determines what we see at all.


Most commonly applied to traces, sampling works by selectively keeping only a subset of events. This is typically done using either **head sampling** or **tail sampling**. Head sampling makes a decision at the start of a trace, keeping or discarding it before it is fully observed. Tail sampling defers that decision until the trace completes, allowing systems to retain traces that meet certain criteria, such as those with explicitly labelled errors or high latency. While tail sampling is more informed, both approaches ultimately discard data e.g. potentially missing data which illustrates logical issues but is not explicitly labelled as an error. The same pattern appears in logging, where error logs may be retained while higher\-volume info logs are selectively reduced per service.


![](/uploads/three_villains_apr2026_image1_824477d094.png)
*Head\-based sampling selects traces upfront (deterministically or randomly), which can drop traces containing critical errors, while tail\-based sampling waits for all spans and prioritizes keeping those with issues. Although tail sampling is more informed, both approaches still discard data and risk losing important signals.*


The goal is straightforward. Sampling reduces the volume of data written, lowers storage requirements, and minimizes the amount of data scanned at query time. In doing so, it controls cost. But like retention, this is not a user\-driven optimization but rather a constraint imposed by the system \- with the **burden again shifted to the user to decide what is worth keeping.**


In many ways, sampling is even more limiting than retention. With short retention windows, at least the available data is complete within that period. Sampling, by contrast, removes fidelity at the point of ingestion.


This loss of fidelity has broader implications. Modern observability increasingly relies on rich, high\-cardinality events, often combining logs, metrics, and traces into unified "wide events". These enable deeper analysis, trend detection, and more accurate reasoning over time. Sampling breaks this model. By removing events, it distorts aggregates, weakens statistical accuracy, and limits the ability to perform meaningful analysis.



> Sampled metrics can be extrapolated to deliver approximate results. While this works for many simple aggregation types, it's challenging for others and invariably means the user is relying on estimates.


Like retention it again constrains the effectiveness of agents. Without full data, agents cannot reliably detect patterns, correlate signals, or reason about anomalies. Also like retention, what may have once been an acceptable trade\-off becomes a hard limitation.


In an ideal system, every event would be retained with full fidelity, made possible through efficient compression and low\-cost storage. This ensures that when an issue arises, the complete context is available. The result is not just faster resolution for engineers, but a system that can support deeper, more accurate analysis, both by humans and by the next generation of agent\-driven workflows.


## Roll\-ups: The aggregation trap [\#](/blog/three-villains-agentic-observability#roll-ups-the-aggregation-trap)


Roll\-ups emerged as a practical response to one of the problems of metrics systems such as Prometheus: high cardinality.


![](/uploads/three_villains_apr2026_image5_e02e95ff29.png)
*High cardinality causes series explosion.
Credit: Observability Engineering: Achieving Production Excellence, Chapter 16\. Efficient Data Storage*



> It is worth briefly defining that term "high cardinality". In time series databases, cardinality refers to the number of unique time series created by combinations of labels such as `host`. A metric like a count of HTTP GET requests, might have labels like `host`, `service`, `endpoint` or `status_code`. Each unique combination becomes its own series. As those dimensions multiply, the number of series can grow extremely quickly. High cardinality labels such as user ids, as shown above, can single handedly cause series explosions.


This is where the time series model begins to show its limits. Systems like Prometheus work well with a moderate number of long\-lived series, but incur overhead for every unique series in memory, on disk, and at query time. Short\-lived, high\-dimensional labels such as `container_id` or `pod_id` amplify this by constantly creating new series and churn.


That pressure leads directly to roll\-ups. Users either reduce the number of dimensions they collect, which creates blind spots, or they pre\-aggregate metrics into coarser forms that are easier to store and query. Vendors reinforce this dynamic by pricing on active series counts, passing the architectural cost of the datastore directly on to the customer. So **teams are again pushed to think less about what they want to observe** and more about what their metrics backend can tolerate.


![](/uploads/three_villains_apr2026_image14_991d95dda4.png)
*Roll\-ups reduce high\-cardinality data by aggregating many detailed series into fewer, coarser metrics, improving efficiency at the cost of losing granular context.*


Roll\-ups are attractive because they help with both storage and query performance, making higher\-level aggregates easier to answer. But they come with a serious cost: they require you to decide in advance what questions you will want to ask later, based on expected day\-to\-day usage, even though the most important questions during incidents are often unknown and ad hoc.. Once data has been rolled up, the original fidelity is gone. If the aggregation was too coarse, or the wrong dimensions were omitted, there is no way to recover them. The result is another observability blind spot, created not by a lack of instrumentation, but by the need to compensate for the limitations of the storage layer.


This problem is compounded further as agents become part of the workflow. When critical dimensions are missing, such as the ability to break down a metric by customer id, the agent simply reaches a dead end. The signal needed to isolate the issue no longer exists. Unlike a human, there is no intuition or fallback.


And this is what makes roll\-ups a villain. They are often presented as a smart optimization, but in many cases they are a workaround for a backend that cannot cope with full\-fidelity data at scale. Ideally, users would **not need to think so hard about cardinality in the first place**. They would store rich, high\-dimensional telemetry as\-is, and use roll\-ups only where they genuinely help accelerate known queries, not as a prerequisite for making the system usable.


A better model is possible. If the storage engine can handle high\-cardinality data efficiently, then roll\-ups become an optional tool used selectively to accelerate some workflows rather than foundational. That means fewer compromises, fewer blind spots, and a system that preserves the full context needed for debugging, analysis, and increasingly, agent\-driven reasoning.


## When the Villains combine [\#](/blog/three-villains-agentic-observability#when-the-villains-combine)


Individually, retention, sampling, and roll\-ups each remove part of the picture. Together, they compound the loss as data is sampled, aggregated, and eventually discarded, leaving not the original signal, but a heavily filtered version of it. The system has not just lost data, it has lost context.


This layered loss creates a fragile model of observability. Questions that were not anticipated in advance often cannot be answered. Root cause analysis becomes guesswork, constrained by what data happened to survive each stage. For human operators, this results in longer investigations and reliance on intuition and system understanding \- delaying the time to resolution, but manageable.


For agents, it is far more severe. With no residual knowledge to fall back on, missing context becomes a hard stop. The combined effect of these three constraints is not just reduced visibility, but a fundamental limit on how well systems can be understood and operated.


## What Observability should look like [\#](/blog/three-villains-agentic-observability#what-observability-should-look-like)


So should retention, sampling, and roll\-ups disappear entirely? Not necessarily. But their role should fundamentally change. They should not be primary constraints shaping system design or data collection, but optional optimizations applied deliberately, not defaults imposed by cost or architectural limits.


Rollups are valuable when used to accelerate specific queries or provide fast access to common aggregates, but should exist alongside raw data, not instead of it. It should never be a choice between performance and fidelity. Full\-resolution data should always be retained, with roll\-ups acting as an optimization layer rather than the foundation of the system.


The same applies to sampling. There may be cases where certain events or logs are known to add little value and can be reduced. But this should be an informed decision based on the data itself, not a necessity driven by storage or processing constraints. By default, systems should capture complete traces and events, preserving full fidelity so that nothing is lost when it matters most.


Retention follows the same principle. Long\-term storage should be the default, with costs low enough that it does not dominate decision\-making. Retention policies should be driven by compliance or actual business requirements, not by the need to aggressively limit storage.


## Defeating the Villains with columns [\#](/blog/three-villains-agentic-observability#defeating-the-villains-with-columns)


To defeat the villains, we need a storage model that can handle full\-fidelity high\-cardinality data economically in the first place.


This is where column\-oriented storage changes the equation. Observability workloads are fundamentally analytical, requiring the ability to ingest large streams of structured or semi\-structured events, then filter, aggregate, and correlate them across time, services, users, containers, and regions.


![](/uploads/three_villains_apr2026_image7_1e81079a62.png)
*Observability is at its heart an analytical data problem requiring aggregations for charts*


Column stores are built for exactly this pattern. Because each column is stored separately, queries only read the fields they need. This reduces I/O significantly and makes aggregations over large datasets much faster than row\-oriented or search\-first systems.

Loading video...*Columnar databases store each column separately, sorting them for high compression*


Columnar storage compresses observability data extremely well. Repeated values and ordered patterns enable far higher compression than traditional approaches. Combined with object storage, this makes long\-term retention economically viable. Instead of treating retention as a constant budgeting exercise, teams can afford to keep raw data for much longer and use expiry policies for compliance or governance, not because the system forces them to delete context.

Loading video...*By treating each column independently, high cardinality properties are isolated in their impact*


The same architecture helps with high cardinality. Unlike time series systems that create and maintain heavy per\-series structures for every unique label combination, column stores isolate each field independently. High\-cardinality columns such as `userId` may compress less effectively, but that cost is contained within the column itself and does not impact the rest of the dataset. This allows efficient filtering and aggregation across highly dimensional data, where fields like user IDs, request paths, or model versions become just additional dimensions to query rather than constraints to avoid.



> Columnar systems do not eliminate cardinality, they shift some cost to query time. Aggregating over a high\-cardinality dimension such as `container_id` can require creating millions of groups and is computationally expensive, even with techniques like disk spilling. However, this is not a common observability access pattern. In practice, users rarely need to visualize or aggregate across millions of distinct series. Most workflows focus on filtered subsets, top\-N results, or aggregated views, making these worst\-case queries the exception rather than the norm.


This also changes the role of roll\-ups and sampling. Roll\-ups still have value when they accelerate known access patterns, and sampling can still make sense for genuinely low\-value data. But neither needs to be the foundation of the system. Raw, full\-fidelity data can remain available, with roll\-ups and sampling [used only as targeted optimizations](https://clickhouse.com/blog/whats-new-in-clickstack-december-2025#materialized-views-arrive-in-clickstack). That is a fundamentally different model from today's observability stacks, where these techniques are often required just to make the system affordable or usable.


![](/uploads/three_villains_apr2026_image11_ab27782576.png)
## Why ClickHouse makes the most sense [\#](/blog/three-villains-agentic-observability#why-clickhouse-makes-the-most-sense)


ClickHouse is not the only columnar database capable of addressing these challenges. Systems like Apache Pinot and Apache Druid share many of the same architectural advantages, and all have found success powering large analytical workloads. But when it comes to observability, ClickHouse stands out due to its real\-time focus.


Sparse primary indices make filtering efficient, aligning with observability access patterns, while the parallel execution engine scales queries across large datasets. [Skip indices](https://clickhouse.com/docs/optimize/skipping-indexes) and [support for full\-text search](https://clickhouse.com/docs/engines/table-engines/mergetree-family/invertedindexes) extend these capabilities, enabling exploratory workflows.

Loading video...*ClickHouse's sparse primary indices exploit the ordered structure of columns to skip large ranges of data, significantly reducing the amount that needs to be scanned.*


ClickHouse's storage architecture natively supports object storage and separation of compute from storage. Combined with columnar compression, this makes it possible to retain large volumes of data at low cost while scaling compute independently based on demand. Crucially, this model removes the need for storage tiers entirely. All data is treated uniformly, with frequently accessed data automatically accelerated through caching based on query patterns. This ensures that hot data is served efficiently without requiring users to decide what belongs in hot, warm, or archive layers. As a result, users benefit from consistent performance and feature parity across all data, without the operational overhead of managing tiers or moving data between them.


![](/uploads/three_villains_apr2026_image2_75cfc83c74.png)
*Intelligent distributed and node level caching in ClickHouse Cloud automatically accelerates frequently accessed data, ensuring common queries and critical investigation paths are served quickly without requiring manual data tiering based on criteria such as time.*


Users can also provision dedicated compute pools for specific workloads such as ingestion, querying, investigations, or alerting, each sized and optimized independently. This reduces overall cost while ensuring resources are aligned with actual usage rather than peak provisioning. Any unused pools can be idle'd, incurring no cost, and activated only when needed.


![Dedicated compute pools](/uploads/three_villains_apr2026_image8_3a1b38141f.png)
These features have already been validated in large\-scale observability deployments. Companies such as [Tesla](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse), [Anthropic](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era), [OpenAI](https://clickhouse.com/blog/why-openai-uses-clickhouse-for-petabyte-scale-observability), and [Character.AI](https://clickhouse.com/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai) rely on ClickHouse to analyze observability data at petabyte scale, demonstrating its ability to meet the demands of modern workloads.


[ClickHouse played an instrumental role in helping us develop and ship Claude 4\. With ClickHouse, the database is green, queries are lightning\-fast, and money is not on fire. ClickHouse has already delivered significant value in helping us create state\-of\-the\-art language models.](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era)[Previously, querying the last 10 minutes would take 1\-2 minutes. With ClickStack, it was just a case of how fast I could blink. The performance is real. When you're digging into logs during an incident, every second matters.](/blog/scaling-observabilty-for-thousands-of-gpus-at-character-ai)
## The future \- agents with full columnar powered context [\#](/blog/three-villains-agentic-observability#the-future---agents-with-full-columnar-powered-context)


So what does a world look like when retention is long\-term, roll\-ups are selective, and sampling is optional?


Instead of managing what data we can afford to keep, we begin optimizing how we access and use it. High concurrency becomes critical, especially as agents become active participants in observability workflows. These systems issue far more queries than humans, and they expect fast, consistent responses. Crucially, we do not want agents to be bottlenecked by the underlying datastore. Instead, we need systems capable of serving queries at the required concurrency without becoming a bottleneck.


![classic_vs_ai_observability.png](/uploads/Untitled_presentation_5_3be67bb8eb.png)
Latency also takes on a new importance. The agentic loop is only as fast as its slowest step. If queries take seconds to return, the entire reasoning process slows down, making interactions less responsive and less effective. Observability becomes less of an interactive workflow and more of a batch process, which is fundamentally at odds with how both humans and agents want to operate.


At the same time, raw data alone is not enough. Agents cannot simply ingest unbounded logs or traces and reason effectively. They need fast, structured summarization. This makes powerful, low\-latency aggregations essential, along with techniques that push summarization into the database itself. Capabilities like log clustering, pattern detection, and high\-speed grouping become first\-class requirements, allowing systems to distill large volumes of data into meaningful signals quickly.


Equally important is openness. In this context, openness means exposing the full capabilities of the datastore through a standard, expressive interface such as SQL. Rather than relying on proprietary query languages or constrained APIs, users and agents can interact directly with the underlying data model. This matters because LLMs are already highly effective at generating SQL, reducing the need for custom training or additional context to learn domain\-specific grammars.


At the same time, well\-defined endpoints and tools remain important for common workflows, providing stable, efficient access patterns for frequent queries. But these should not be the only interface. The ability for agents to fall back to raw SQL acts as a critical escape hatch, enabling deeper introspection and truly ad hoc investigation.


This is where systems designed for real\-time analytics have an advantage, naturally providing these properties as part of their design. ClickHouse, for example, was built from the outset to serve low\-latency SQL aggregations at high concurrency. Once the constraints of retention, sampling, and roll\-ups are removed, these characteristics form the foundation of the next generation of observability, optimizing for speed, scale, and reasoning over complete data.


## Conclusion [\#](/blog/three-villains-agentic-observability#conclusion)


Observability has been shaped by constraints that force users to trade fidelity for cost and performance. As we move into an agent\-driven future, those trade\-offs are no longer acceptable. By removing these limitations and embracing architectures built for full\-fidelity data, we can shift from managing compromises to enabling true understanding. This is what ultimately unlocks agentic observability, where systems can reason, investigate, and act with complete context.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
