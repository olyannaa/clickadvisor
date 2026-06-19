# How Wix Built AI\-Driven Incident Response at Scale with ClickHouse and Wild Moose


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Wix Built AI\-Driven Incident Response at Scale with ClickHouse and Wild Moose

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 10, 2026 · 10 minutes read[Wix](https://wix.com), a leading global platform for creating, managing, and growing a complete digital presence, operates one of the most complex production environments globally. The platform serves about 300 million users, runs 4,000\+ microservices, and processes billions of requests per day. Any individual user action can traverse long, dynamic chains of services, each with the potential to introduce latency, errors, or cascading failures.


The company is known for its zero\-error tolerance culture, where resilience and error handling are designed into systems from day one. As Wix continued to scale, the engineering team became increasingly committed to finding a way to make incident response faster, more accurate, and less disruptive to developers or the underlying data infrastructure.


This initiative ultimately led Wix to AI\-driven incident response, leveraging Wix’s foundations of handling real\-world production incidents at scale.


## The Challenge: Complexity, Scale, and the Limits of Manual Response [\#](/blog/wix-wild-moose#the-challenge-complexity-scale-and-the-limits-of-manual-response)


To push incident response beyond the limits of manual investigation, Wix experimented with several internal approaches. The team built automation tools and ran early AI experiments that showed promise, but they struggled to scale. Turning these experiments into reliable, production\-grade systems would have required significant ongoing investment and maintenance.


At the same time, any AI\-driven approach posed a new risk of query amplification. Investigating an alert with AI means running many more queries than a human would, often in parallel, while engineers still need full access to logs and dashboards. Without the right data layer, AI would either be too slow to trust or too disruptive to deploy.


Wix needed an approach that matched its zero\-error tolerance culture without compromising system stability.


## ClickHouse and the Data Foundation for Agentic Workloads [\#](/blog/wix-wild-moose#clickhouse-and-the-data-foundation-for-agentic-workloads)


Long before introducing AI agents, Wix had already made a critical architectural decision.


Nearly eight years ago, Alex Ulstein, head of visibility at Wix, set out to support centralized logging at massive scale. As the team began defining requirements, it quickly became clear that conventional approaches would struggle to meet the demands ahead.


Within weeks, Wix needed to ingest roughly one million log events per minute with no sampling, making existing search\-based architectures impractical from both a performance and cost perspective.


Because Wix controls its logging libraries end to end, logs follow a fixed schema. That minimized the need for schema\-on\-read flexibility or full\-text search, shifting the focus instead to raw ingestion speed, compression efficiency, and analytical query performance.


After benchmarking multiple open\-source options, ClickHouse emerged as the clear choice. It delivered the fastest performance and the most complete SQL support among columnar databases. “ClickHouse was by far the fastest,” says Ulstein. “Compression was excellent, and the depth of its SQL feature set exceeded what we needed.”


Today, Wix’s largest application logging cluster runs on 60 machines, handles 300 queries per second, and ingests an average of 300 million events per minute without sampling. Most queries return in sub\-second latency. “Ingestion speed is a really important part, and where ClickHouse shines,” Ulstein adds.


Critically, this architecture gave Wix something many teams lack: full\-fidelity observability data at scale. That foundation would later prove essential for AI\-driven incident response.


## Wild Moose: AI SRE Built from Tribal Knowledge [\#](/blog/wix-wild-moose#wild-moose-ai-sre-built-from-tribal-knowledge)


As alert volumes continued to grow, Wix set out to operationalize AI for incident response by evaluating external, production\-ready solutions. They defined a clear set of requirements:


- AI must work the way engineers investigate, not as a black box
- It must integrate into existing workflows (Slack, Grafana, logs)
- It needs to automate tribal knowledge without replacing human judgment
- And it must scale without disrupting human access to data


Together, these requirements made Wild Moose the right choice \- AI built to work the way engineers do, at production scale.


[Wild Moose](https://wildmoose.ai) is an agentic AI SRE platform designed to codify how experienced engineers debug incidents. Instead of static rules or generic summaries, Wild Moose ingests institutional knowledge and automatically executes investigation workflows. It runs incident analysis the same way engineers do, only faster and in parallel.


“Wild Moose had the most mature approach for automating tribal knowledge. The responsiveness in tuning and adapting the product to our unique needs made it clear this was the right partnership,” Aviva Peisach, head of backend engineering at Wix shares.


When an alert fires, Wild Moose agents query logs, correlate signals across services, examine recent deployments, and compare against historical patterns. Enriched findings are delivered directly to Slack in under a minute, giving engineers high\-confidence starting points instead of raw alerts or noisy summaries.


"With Wild Moose, we’re able to spot the root cause \- whether it’s a recent GA, traffic switch, new experiment, or something environmental. Wild Moose helps pinpoint the actual root cause service causing the problem in a very complex environment with billions of requests coming in through a very long chain of calls between services,” says Peisach.


## How ClickHouse and Wild Moose Work Together [\#](/blog/wix-wild-moose#how-clickhouse-and-wild-moose-work-together)


At Wix, ClickHouse and Wild Moose together formed a system capable of supporting AI\-driven incident response under real production constraints.


### 1\. AI\-driven execution operationalizes incident response [\#](/blog/wix-wild-moose#1-ai-driven-execution-operationalizes-incident-response)


By shifting incident investigations from human\-driven or rule\-based workflows to continuously running AI agents, Wild Moose transforms ClickHouse into a central hotspot for reliability logic at Wix. Unlike human\-driven or rule\-based systems, Wild Moose systematically leverages ClickHouse’s concurrency model by issuing many parallel queries per alert, fully exercising the database’s real\-time analytics capabilities. Wix teams can now compose, test, and iterate on SQL queries directly inside Wild Moose agents, where those queries are executed automatically during incidents.


### 2\. Query performance enables parallel investigations [\#](/blog/wix-wild-moose#2-query-performance-enables-parallel-investigations)


Wild Moose agents are able to run hundreds of queries per alert in parallel to build a complete picture of what's happening. ClickHouse's ability to sustain high query concurrency allows Wild Moose to heavily parallelize investigations without slowing down dashboards or human workflows. "With AI that approaches investigations the same way people do, solutions that work well for humans work well for the AI. Except automating these operations increases the scale and concurrency by orders of magnitude, so the fast and efficient querying that made us choose ClickHouse in the first place becomes even more crucial," Ulstein says.


### 3\. Full\-fidelity retention improves root cause accuracy [\#](/blog/wix-wild-moose#3-full-fidelity-retention-improves-root-cause-accuracy)


Because ClickHouse stores unsampled logs with efficient compression, Wild Moose has access to complete historical context for analysis and comparison. Rare failure patterns, edge cases, and subtle correlations remain detectable, and the AI learns from long\-tail, high\-volume examples that might be filtered out in sampled data. This long\-term retention ensures the agent can draw on rich examples of past incidents that would otherwise be lost, strengthening its ability to reason about and respond to new failures.


### 4\. SQL expressiveness accelerates insight [\#](/blog/wix-wild-moose#4-sql-expressiveness-accelerates-insight)


Wild Moose uses SQL as its native query interface, allowing AI models to generate highly problem\-specific queries without relying on custom query languages. This lets the system reuse and adapt existing queries that Wix engineers already trust. ClickHouse’s rich SQL functions and join support enable Wild Moose to push certain correlations down to the database where they’re optimized, making investigations both faster and more accurate.


This allows Wild Moose to focus its AI on higher\-level guidance that shapes the investigation, rather than on routine query mechanics, preserving valuable context for complex problem\-solving.


### 5\. Decoupled architecture enables flexibility [\#](/blog/wix-wild-moose#5-decoupled-architecture-enables-flexibility)


ClickHouse separates the data layer from the UI layer. AI agents can access raw logs directly while dashboards remain fast and independent, avoiding the “walled garden” constraints of traditional observability platforms.


This decoupling proved essential for rapid iteration and tuning. When Wild Moose needed to adjust investigation strategies or add new correlation techniques, they could do so without worrying about breaking existing dashboards or workflows.


## The Results: Higher Accuracy, Faster MTTR, and Boosted Team Morale [\#](/blog/wix-wild-moose#the-results-higher-accuracy-faster-mttr-and-boosted-team-morale)


Wix’s existing ClickHouse infrastructure meant Wild Moose could be deployed quickly. Logs were structured for ClickHouse queries, full SQL support simplified query translation, and many existing human\-written queries could be reused with minimal optimization. This supported rollout to hundreds of teams in a matter of weeks.


Within weeks, Wix could clearly see how their work with Wild Moose delivered results:


- **90% root cause accuracy** sustained across thousands of alerts
- **50% projected reduction in MTTR**, giving engineers time back
- **30,000\+ alerts enriched per month**, with volume continuing to grow
- **Hundreds of teams supported** across 200\+ Slack channels
- Reduced on\-call stress and improved developer morale


The impact was felt in the day\-to\-day experience of developers on call. Instead of firefighting, engineers now start investigations with context, hypotheses, and likely root causes already surfaced.


"We were able to get to a stage of over 80% accuracy in just three weeks, which is mind\-blowing for a system as complex as ours," Peisach says.


On\-call rotations have become less stressful. Engineers feel more confident knowing they have a system that could guide them quickly to the right answer. And unlike the hard\-coded rules of Wix’s internal automation tools, Wild Moose learns and adapts through natural\-language feedback, automatically improving accuracy over time.


## Looking Forward: A System for AI\-Driven Reliability [\#](/blog/wix-wild-moose#looking-forward-a-system-for-ai-driven-reliability)


Wix's experience highlights what large\-scale engineering teams can achieve when AI, observability, and data infrastructure form a coherent architecture.


Wix designed and operates an AI\-driven reliability system grounded in its own large\-scale production experience. ClickHouse serves as the scalable data backbone for observability and AI workloads, while Wild Moose encodes hard\-won operational knowledge into automated investigations. This architecture allows Wix to sustain a zero\-error tolerance culture while continuing to scale one of the most complex platforms in the world.


What emerged was an investigation engine where AI agents continuously learn, and the data layer continuously scales. As the environment grows more complex, the system becomes more valuable. Tribal knowledge turns into durable institutional knowledge, alert storms become manageable, and developers spend more time building instead of firefighting.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-56-get-started-today-sign-up&utm_blogctaid=56)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
