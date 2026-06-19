# ClickHouse welcomes Langfuse: The future of open\-source LLM observability


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse welcomes Langfuse: The future of open\-source LLM observability

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmarc_9e41a9643d.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmax_e5e9dfa298.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fclemens_db98ee8068.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene), [Marc Klingen](/authors/marc-klingen), [Max Deichmann](/authors/max-deichmann) and [Clemens Rawert](/authors/clemens-rawert)Jan 16, 2026 · 8 minutes readWe are thrilled to announce that ClickHouse has acquired [Langfuse](https://github.com/langfuse/langfuse), the leading open\-source platform for LLM observability, evaluations, and prompt management. We couldn't be more excited to welcome Marc Klingen, Max Deichmann, Clemens Rawert, and the entire Langfuse team and community into the ClickHouse family.


By combining Langfuse's developer\-first approach to AI quality monitoring with ClickHouse's blazing\-fast core analytical capabilities, we offer a comprehensive, open\-source stack for building, monitoring, and optimizing AI applications at scale.


## The rise of AI\-native applications [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#the-rise-of-ai-native-applications)


LLMs are no longer an emerging technology and have seen widespread adoption, powering features and capabilities in almost every modern software. For instance, a majority of new SaaS applications ship with AI\-powered features at the center of their workflows: conversational interfaces, agent\-enhanced workflows, and automation. Developers have become both consumers of AI (through coding agents and co\-pilots) and the primary builders of AI\-powered experiences.


At ClickHouse, we've seen this shift firsthand through our work on the [Agentic Data Stack](https://clickhouse.com/ai). Complex AI workflows need to be grounded in real data and insights: that's where the synergy between LLMs and powerful analytical databases becomes essential.


But there's still a critical “trust” gap: how do you know if your AI application is actually working as intended?


## AI quality monitoring [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#ai-quality-monitoring)


LLM\-powered applications are non\-deterministic black boxes. The same prompt can produce different responses, making debugging and quality assurance fundamentally different from traditional software.


Operating without proper visibility is what some practitioners call "vibe\-checking": essentially placing a bet on output quality without any way to measure it. For consumer applications, this might mean a bad user experience. For enterprise applications dealing with financial decisions, legal or compliance matters, or customer\-facing interactions, the stakes are much higher.


The challenge compounds with complexity. Modern AI applications can involve multi\-step agentic workflows, enrichment pipelines, tool calls, nested reasoning chains, and multi\-agent coordination. When something goes wrong, finding the cause and a remediation becomes nearly impossible without proper tooling.


Traditional observability tools can tell you if your service is up, fast, and error\-free. But it reveals nothing about whether your model's outputs are correct, helpful, safe, or aligned with user intent. An LLM can be perfectly healthy from a systems perspective while consistently producing low\-quality answers.


This is why we believe "AI quality monitoring" is the right framing—it focuses directly on the outcome that matters: how well is your AI actually performing for users?


As always at ClickHouse, we evaluate the solutions on our internal systems first. We've been using Langfuse internally to monitor [DWAINE](/blog/ai-first-data-warehouse), our internal data warehouse AI agent. Having proper observability into our LLM interactions has been invaluable for understanding where our agents succeed and where they need improvement.


![langfuse-screenshot-2.png](/uploads/langfuse_screenshot_2_ae975a0ccc.png)
The ability to trace individual interactions, score them for quality metrics like hallucination detection, and analyze trends over time has fundamentally changed how we think about AI quality in production.


![langfuse-screenshot.png](/uploads/langfuse_screenshot_a76076e363.png)
## Why Langfuse? [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#why-langfuse)


When we evaluated the AI observability landscape, a few things became immediately clear.


**The market is fragmented, but Langfuse is pulling ahead.** While there are dozens of players in this space, ranging from pure\-play startups to MLOps vendors extending into LLM monitoring to traditional observability platforms adding AI features, Langfuse has emerged as a leader in open\-source, developer\-first LLM observability with:


- 20k\+ GitHub stars
- 23\.1M\+ SDK installs per month
- 6M\+ Docker pulls
- Trusted by 19 of the Fortune 50 and 63 of the Fortune 500
- [Enterprise](https://langfuse.com/enterprise) users like Intuit, Twilio, 7\-Eleven, Merck, and numerous others


Check out the [Langfuse Wrapped 2025](https://langfuse.com/wrapped) for a great retrospective of last year's growth.


**Langfuse is already built on ClickHouse.** Langfuse's architecture [runs entirely on ClickHouse](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution), both in the cloud offering and for self\-hosted deployments. The scale and performance requirements of LLM observability demand a database [that can handle](https://www.youtube.com/watch?v=NXYQ5odATrM) high\-volume writes and fast analytical queries. This existing alignment means tighter integration and better performance for everyone.


**Shared Open\-source DNA.** We believe that being good stewards of open\-source means not just maintaining code, but actively investing in and growing the communities that depend on it. Langfuse has built exactly the kind of vibrant developer community we love to support—one where contributors actively shape the product and enterprise adoption follows organic grassroots momentum, embracing open standards like OpenTelemetry. This is the same playbook that made ClickHouse what it is today, and we're excited to bring that same energy to the Langfuse community.


**The product is comprehensive.** Langfuse is a [complete platform](https://langfuse.com/enterprise) covering AI observability, prompt management, evaluations, and experimentation. The data models and SDK layers are thoughtfully designed for the unique challenges of LLM applications.


![observability-image.png](/uploads/observability_image_b64e9276e3.png)

> "Generative AI will only earn enterprise trust when we can see what's happening under the hood. Langfuse enables us to track every prompt, response, cost, and latency in real time, turning black\-box models into auditable, optimizable assets."   
> 
>   
> 
> *Walid Mehanna, Chief Data \& AI Officer at Merck* ([source](https://langfuse.com/customers/merckgroup))


## The synergy [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#the-synergy)


This acquisition follows the same playbook we've used successfully with [PeerDB](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) (for Postgres CDC) and [HyperDX](/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability) (for infrastructure observability). We join forces with category\-leading open\-source projects that are already built on ClickHouse and share our commitment to developer experience and community\-first development.


With Langfuse, we're doing the same for AI observability:


- **Langfuse remains 100% open\-source** under its existing MIT license for core features which allows for self\-hosting at production scale (on top of ClickHouse)
- **Langfuse Cloud continues operating** as a standalone service
- **Community\-first development** continues with the same transparency and openness


The tighter integration between Langfuse and ClickHouse means we can optimize the entire stack together—from data collection through to analysis and action. This creates a feedback loop that benefits both Langfuse users (through better performance) and ClickHouse users (through insights that help us optimize for AI workloads).



> "Langfuse has really enabled our developers to get extremely fast feedback. When building and deploying features, we can quickly watch how those experiences are going. Langfuse is fundamental to how our developers understand their AI implementations."   
> 
>   
> 
> *Walt Wells, Staff Software Engineer at Khan Academy ([source](https://langfuse.com/customers/khan-academy))*


## What this means for the Agentic Data Stack [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#what-this-means-for-the-agentic-data-stack)


The [Agentic Data Stack](/ai) (our vision for AI\-powered applications built on ClickHouse and LibreChat) now gains a critical new capability: the ability to monitor, evaluate, and continuously improve the AI components themselves.


For data analysts and administrators using LibreChat to query their data warehouses, Langfuse provides visibility into how well the agents are performing. For developers building custom agentic workflows with our APIs and MCP servers, Langfuse offers the debugging and optimization tools they need to ship with confidence.


The three main personas of agentic analytics—data professionals operating databases, developers building AI features, and business users consuming insights—all benefit from knowing that their AI interactions are monitored, evaluated, and improving over time.


## What's next? [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#whats-next)


**For existing Langfuse deployments:** Nothing changes. Langfuse continues to work exactly as it does today, and we are committed to continuing to invest in the platform and community.


**For Langfuse Cloud customers:** The service continues operating with the same SLAs and support. The Langfuse team is focused on expanding the roadmap, not disrupting what's working.


**For ClickHouse users:** Over the coming months, we'll be releasing deeper integrations that make LLM observability a native part of the agentic data stack experience. Expect seamless connections between your AI workloads and the tools to understand them.


**For everyone:** Join the communities on [Slack](/slack) to stay connected as we build the future of AI observability together.


## Get started [\#](/blog/clickhouse-acquires-langfuse-open-source-llm-observability#get-started)


**For Langfuse users:** Continue using Langfuse as you always have. Check out the excellent [documentation](https://langfuse.com/docs) if you're new, or explore the latest features if you're already on board.


**For ClickHouse users:** If you're building AI\-powered applications, [try Langfuse](https://langfuse.com) to add observability to your LLM interactions. The integration with ClickHouse as a backend store is already seamless.


**For everyone else:** The AI quality monitoring space is only going to become more important as AI becomes more central to how software works. Now is the time to get serious about understanding your AI systems.


As always, the ClickHouse team would be honored to partner with you on your AI journey. Whether you're using Langfuse today or are just starting to think about LLM observability, please [contact us](/company/contact).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
