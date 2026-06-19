# How Anthropic is using ClickHouse to scale observability for the AI era


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Anthropic is using ClickHouse to scale observability for the AI era

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 7, 2025 · 7 minutes readIn just a few short years, [Anthropic](https://www.anthropic.com/) has built a reputation not only for pushing the boundaries of what AI can do, but for doing so safely and responsibly. As the company behind the [Claude](https://www.anthropic.com/claude) series of frontier language models, that commitment extends deep into their infrastructure, where [observability](https://clickhouse.com/engineering-resources/best-open-source-observability-solutions) plays a key role in both performance and protection.



> "ClickHouse played an instrumental role in helping us develop and ship Claude 4\."
> 
> Maruth Goyal, Member of Technical Staff at Anthropic


When Claude usage skyrocketed in 2024, Anthropic's observability team found themselves managing a deluge of telemetry, metrics, and logs. And with every new model, the stakes grew higher. They needed to catch issues in real time, prevent sensitive data from leaking, and keep everything running inside a tightly controlled, secure compute environment.



## With great power comes great responsibility [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#with-great-power-comes-great-responsibility)


When Anthropic launched Claude 3 in March 2024, "people started taking notice," Maruth Goyal, Member of Technical Staff at Anthropic says. But it was Claude 3\.5's release a few months later when, as he puts it, "things hit the fan."


### Learn about ClickStack [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#test)

Explore the ClickHouse\-powered open source observability stack built for OpenTelemetry at scale.

[Learn more](https://clickhouse.com/use-cases/observability?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
Usage soared. Models grew more sophisticated. And the supporting infrastructure had to scale fast. The compute footprint ballooned, and with it, the volume of data needed to monitor, troubleshoot, and fine\-tune increasingly complex training and inference workloads. All of a sudden, their existing observability system struggled to keep up.


![anthropic-1.jpg](/uploads/anthropic_1_0d480442af.jpg)
"What happens when you have a whole lot of data?" Maruth asks. "Your database catches fire. Queries start timing out. Engineers start getting frustrated. Money catches fire."


At the same time, Anthrophic's security and safety standards were only becoming more stringent. With the release of Claude Opus 4 in May 2025, the company [activated AI Safety Level 3 precautions](https://www.anthropic.com/news/activating-asl3-protections), a set of internal guardrails designed to reduce the risk of misuse. A key part of that effort, Maruth explains, was locking down data access.


"We're worried that extremely capable model weights can be used by bad actors to achieve extremely bad outcomes," he says. "To prevent that, we very aggressively monitor any egress from our clusters. No data should leave Anthropic's secure computing environment."


## Choosing ClickHouse to scale observability [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#choosing-clickhouse-to-scale-observability)


In late 2024, Maruth and the Anthropic team set out to find a better database solution. Their wishlist was ambitious: "We need to ingest a huge amount of data in real time. We need fast, interactive, feature\-rich analytics over semi\-structured data. We need it to be deployed in Anthropic's secure computing environment. And we need a [scalable cost structure](/blog/breaking-free-from-rising-observability-costs-with-open-cost-efficient-architectures)."


On top of all that, they wanted a database that played nicely with industry\-standard observability tools, and that wouldn't require constant babysitting. "My team had three people until January," Maruth says. "We don't want to go crazy."


In true Anthropic fashion, he knew he didn't have to search the ends of the Earth for the right solution. "It would be great if I could go ask a superintelligence what I should be using," he jokes. "That would be convenient if I had one lying around."


He asked Claude for its recommendation, and it suggested ClickHouse. As he took a closer look, he liked what he saw. "It supports real\-time ingest at scale," he says. "It offers fast analytics, flexible deployment, and cost\-effective scaling."


He brought it to the team, and they agreed: "This sounds great." Now they just had to figure out how to run it in an air\-gapped, tightly controlled environment.


![anthropic-1.png](/uploads/anthropic_1_f8a40f8682.png)
## Deploying ClickHouse, the Anthropic way [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#deploying-clickhouse-the-anthropic-way)


ClickHouse was the right technical fit, but the default deployment options didn't quite match Anthropic's needs. The open\-source version had clear benefits \- "It's quick to get started, it's tried and tested, you get great performance" \- but it also meant managing disks, replicas, re\-sharding, "the whole hoopla," as Maruth puts it. "Life is not fun \- or, well, it's fun because you have ClickHouse, but the operational cost is high," he adds.


[ClickHouse Cloud](https://clickhouse.com/cloud) came with its own advantages. "You have dynamic scaling, and it's backed by cost\-efficient and reliable blob storage," Maruth says. "But it's only available on ClickHouse Cloud." That was a dealbreaker, since Anthropic needed everything to run inside its own secure compute environment.


So they took a hybrid approach. Working with the ClickHouse team, they deployed a custom, air\-gapped version of the ClickHouse Cloud architecture within Anthropic's infrastructure. Everything, from the control plane to the data plane, is operated internally.


![anthropic-3.png](/uploads/anthropic_3_7c4662a981.png)
*Anthropic's ClickHouse deployment*


The cluster runs on Kubernetes, orchestrated by the ClickHouse Operator. It includes three ZooKeeper replacements ("keepers"), one per availability zone, and uses horizontally scalable servers with object storage as the backing layer. Prometheus handles monitoring, while Vector manages ingestion, stitching together observability pipelines cleanly and efficiently.


As Maruth explains, the setup meets all of Anthropic's needs. It scales with demand, without burdening engineers with constant maintenance. "And everything, critically, is deployed in Anthropic's secure environment and operated by us entirely," he says.


## Speed, security… and sanity [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#speed-security-and-sanity)


Anthropic's new observability setup has already delivered major improvements. As Maruth puts it, "The database is green, queries are lightning\-fast, and money is not on fire."


"With our prior solution," he explains, "our database operators would lose sleep and get frustrated because they couldn't work on what they really wanted to. They were spending all their time going out of the database, contacting support, asking for help with things like re\-sharding and fixing write replication."


And now? "None of that," Maruth says. One engineer even told him, "I haven't noticed the database running for a while." Which is exactly how it should be.


With ClickHouse, fast, reliable queries over massive datasets are the new normal. The team can stop worrying about infrastructure and focus on what matters: building better tools, shipping faster models, and pushing the boundaries of what Claude can do.


## From Claude 4 to agentic analytics [\#](/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era#from-claude-4-to-agentic-analytics)


In addition to scaling observability, Maruth says, "ClickHouse played an instrumental role in helping us develop and ship Claude 4\." Training advanced models, he explains, requires constant visibility into performance metrics and system behavior. ClickHouse gives them the speed and flexibility to analyze that data in real time. "It's already delivered significant value helping create state\-of\-the\-art language models," he says.


Today, the team is looking to the next frontier: agentic analytics. With the [introduction of ClickHouse's MCP server](https://clickhouse.com/blog/integrating-clickhouse-mcp), Anthropic can connect its models \- like [Claude Code](https://www.anthropic.com/claude-code), an agentic coding tool \- directly to ClickHouse. That means agents can query metrics programmatically, ask questions, and get answers, without needing to write traditional query languages.


"I'm really excited about this because, in my mind, observability is not about SQL or PromQL," Maruth says. "It's about questions. You want to be able to ask a question and get back the answers you need. Fundamentally, that's what it's all about."


With ClickHouse, Anthropic has the scalable, secure foundation it needs to support today's AI workloads, while building toward a more dynamic, agent\-driven future.


To learn more about ClickHouse and see how it can bring speed and scalability to your team's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
