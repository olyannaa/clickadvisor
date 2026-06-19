# How Poolside is using ClickHouse to build next\-gen AI for software development


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Poolside is using ClickHouse to build next\-gen AI for software development

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 3, 2025 · 7 minutes read![Poolside.png](/uploads/Poolside_ba4fb435be.png)
Everything [poolside](https://poolside.ai/) does revolves around one goal: scaling intelligence. Co\-founders Eiso Kant and Jason Warner are on a mission to redefine software development by [closing the gap between human and machine intelligence](https://poolside.ai/checkpoint/announcing-our-500-million-fundraise-to-make-progress-towards-agi), empowering developers to be more productive and creative, and unleashing a wave of innovation to tackle humanity’s greatest challenges.


"We’re focused on bringing AI to software developers on a daily basis in a way that drives increasingly more productivity and enjoyment in the job," Eiso told ClickHouse recently. "To do that, we build foundation models from the ground up, with our own unique point of view, research, and approach that we think sets us apart from competitors."


But scaling innovation requires more than ambition: it demands infrastructure capable of handling billions of documents and running complex analytics at unprecedented speeds. As Eiso and the team scaled their training clusters to 10,000 GPUs and expanded their research to more than 800,000 real\-world codebases, they realized their existing data pipelines couldn’t keep pace with the scale and speed they required.


Last year, they turned to [ClickHouse Cloud](https://clickhouse.com/cloud), a move that has allowed them to iterate faster, explore new approaches, and refine their AI models with greater precision.



> "ClickHouse gives us the speed to look at the data directly, letting us make faster decisions and iterate quickly, which is core to our mission."
> 
> 
> Eiso Kant, poolslde


## Data growing pains [\#](/blog/poolside-using-clickhouse-to-build-next-gen-ai-for-software-development#data-growing-pains)


Six months ago, poolside’s data operations were a patchwork of ad\-hoc pipelines managed by just two engineers. Today, Eiso says, they have "around a dozen people running data pipelines in different ways, shapes, and forms." This rapid growth has underlined the need for a more advanced database solution to manage their increasingly complex workflows.


At the heart of poolside’s work is an iterative approach to AI development. Their models analyze billions of documents and receive deterministic feedback, allowing them to improve reasoning and coding capabilities. But as the company scaled, poolside’s existing pipelines struggled to keep up with the demands of running large\-scale queries across datasets. These delays slowed the team’s ability to experiment, make decisions, and refine their models.



> "How fast can we go from idea to dataset? That’s the metric that drives everything we do."


Adding to the complexity was the sheer scale of their operations. With massive compute clusters powering their AI training and research, they needed infrastructure that could handle large\-scale data and help their team work faster and smarter. "How fast can we go from idea to dataset? That’s the metric that drives everything we do," Eiso says. Simply put, their existing setup couldn’t keep up with the speed or scalability their vision demanded.


## Choosing ClickHouse Cloud [\#](/blog/poolside-using-clickhouse-to-build-next-gen-ai-for-software-development#choosing-clickhouse-cloud)



> "If you only get to pick one thing, you’re glad you picked ClickHouse."


Eiso was no stranger to ClickHouse. He first encountered the database nearly a decade ago when it was open\-sourced and had used it extensively at his previous companies, source{d} and Athenian. Having witnessed its speed and efficiency firsthand, he knew it could address Poolside’s growing data needs. "Even when you abuse it, you’re happy you did,” he says. “If you only get to pick one thing, you’re glad you picked ClickHouse."


While the familiarity helped, Eiso says the decision to choose ClickHouse was primarily about one thing: speed. "At the end of the day, the only thing we care about is speed," he says. Whether querying billions of records or analyzing the performance of AI models in real time, ClickHouse’s superior performance as a columnar OLAP database meant it could deliver results in seconds. For poolside’s iterative workflows, this translated into tangible advantages — running more experiments, exploring more ideas, and refining their models faster.


[ClickHouse Cloud](https://clickhouse.com/cloud) added another major benefit: simplicity. By choosing a managed service, the poolside team could avoid the burden of maintaining database infrastructure internally, freeing them to focus on scaling AI models and refining research, rather than troubleshooting performance issues or managing servers.


## Turning complexity into efficiency [\#](/blog/poolside-using-clickhouse-to-build-next-gen-ai-for-software-development#turning-complexity-into-efficiency)


The adoption of ClickHouse Cloud has transformed poolside’s data architecture, making it more streamlined, scalable, and efficient. Alongside standardized Spark pipelines to handle data processing, this shift allows the team to manage massive datasets consistently while maintaining the flexibility needed for fast experimentation.


[ClickPipes](https://clickhouse.com/cloud/clickpipes) has been a big part of this transformation. By simplifying the ingestion of datasets from queuing systems and object storage, it ensures each newly enriched dataset flows seamlessly into ClickHouse. This lets poolside analyze and validate data at every stage of their iterative AI workflows, with minimal management and no reliance on third\-party infrastructure.


ClickHouse sits at the core of their analytics workflows, delivering results from billions of records in seconds. Its performance lets poolside’s engineers focus on analyzing data and refining models instead of troubleshooting bottlenecks. For tasks requiring different strengths, the team also incorporates other tools like Dremio, creating a flexible multi\-engine system. This means engineers can choose the best query engine for each workload, whether it’s ClickHouse for lightning\-fast analytics or Dremio for more specialized needs.


Today, ClickHouse is primarily used internally, with around 50 terabytes of compressed data stored in ClickHouse Cloud. This architecture supports billions of documents, delivering real\-time insights that fuel poolside’s iterative workflows. With data bottlenecks eliminated, the team can experiment, innovate, and push the boundaries of AI at scale.


## Building the future of AI [\#](/blog/poolside-using-clickhouse-to-build-next-gen-ai-for-software-development#building-the-future-of-ai)


As they chart the future of AI, poolside is setting their sights on even greater challenges. Their next steps include scaling their models further and pushing the limits of what their infrastructure can achieve. As they expand their research with larger datasets and new reinforcement learning techniques, ClickHouse Cloud will be a big enabler of their mission.


Eiso sees a future where anyone — not just seasoned developers — can use AI to build technology and solve complex problems. As the gap between human and machine intelligence continues to close, poolside’s tools promise to lower the barrier to entry, unlocking innovation for a wider audience as more people access the power of software development.



> "ClickHouse makes a lot of sense for what we’re trying to do. It lets us work faster, think bigger, and focus on what we care about most — scaling intelligence through AI."


As poolside grows, they’re not just building technology. They’re laying the foundation for a future where intelligence is scaled to tackle humanity’s shared challenges. With ClickHouse by their side, they’re redefining what’s possible in AI and software development.


*To see how ClickHouse can scale your company’s data operations, [try ClickHouse Cloud free for 30 days](https://console.clickhouse.cloud/signUp).*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
