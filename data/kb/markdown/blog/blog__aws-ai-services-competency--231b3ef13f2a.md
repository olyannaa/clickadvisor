# ClickHouse achieves AWS AI Competency


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Company and culture](/blog?category=company-and-culture)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse achieves AWS AI Competency

![](/_next/image?url=%2Fuploads%2FAditya_45b3f106a9.jpg&w=96&q=75)[Aditya Chidurala](/authors/aditya-chidurala)Jan 23, 2026 · 4 minutes readWe’re excited to announce that ClickHouse has achieved the **AWS AI Competency** in the **Software** partner track, with validated offerings in **Agentic AI Tools** and **Agentic AI Applications**.


As organizations move beyond experimentation toward production\-ready autonomous systems, AWS recently expanded the AWS AI Competency (formerly the AWS Generative AI Competency) with three new agentic categories: Agentic AI Tools, Agentic AI Applications, and Agentic AI Consulting Services, to help customers identify partners with proven expertise in delivering enterprise\-grade autonomous AI solutions.


### **Meeting the unique demands of agentic AI** [\#](/blog/aws-ai-services-competency#meeting-the-unique-demands-of-agentic-ai)


Agentic AI systems don’t just “generate”, they **observe, plan, act, and learn**. That introduces a data problem that looks very different from classic analytics:


- **High\-volume, high\-cardinality telemetry** (tool calls, traces, evaluations, feedback signals, token usage, latency, errors)
- **Real\-time iteration loops** (prompt changes, model rollouts, A/B tests, regression checks)
- **Enterprise governance requirements** (data locality, private networking, predictable cost, operational resilience)


ClickHouse is built for this kind of workload: a fast, scalable real\-time analytics engine that can ingest massive event streams and return interactive query results quickly, so teams can keep humans and agents in the loop without slowing down production systems.


Earning the AWS AI Competency recognizes the work we’ve done (with customers) to bring these capabilities to production on AWS, and it reflects AWS’s bar for partner validation and demonstrated customer success in agentic categories.


### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
### **Customer success across AI tools and agentic applications** [\#](/blog/aws-ai-services-competency#customer-success-across-ai-tools-and-agentic-applications)


We see two consistent patterns in production AI: teams need (1\) a **reliable data backbone** for AI tools (observability, evaluation, iteration), and (2\) a **low\-latency analytics layer** to power agentic applications that interact with real\-world business data. Here are six examples that reflect those requirements:


**LLM observability and evaluation at scale (Agentic AI Tools)**


Platforms like **[Langfuse](https://clickhouse.com/blog/langfuse-and-clickhouse-a-new-data-stack-for-modern-llm-applications)** and **[LangChain’s LangSmith](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain)** rely on ClickHouse to store and analyze the traces, metrics, and feedback that teams use to debug and improve LLM and agent behavior. As these systems scale to production volumes (including self\-hosted environments), ClickHouse enables fast dashboards, drilldowns, and evaluation workflows without the ingestion and query bottlenecks that can emerge in general\-purpose architectures.


**Production\-grade telemetry for AI infrastructure (Agentic AI Tools)**


Modern AI infrastructure generates an immense amount of operational signals. **[Modal](https://clickhouse.com/blog/modal-real-time-observability-ai-workloads)** uses ClickHouse Cloud to power real\-time observability dashboards—ingesting **1–2 million events per minute** while still delivering sub\-second queries. **[Temporal](https://clickhouse.com/blog/building-chronicle-how-temporal-supercharged-their-observability-with-clickhouse)** built Chronicle, an internal observability system powered by ClickHouse, to “embrace cardinality” and keep investigative queries and dashboards fast at multi\-tenant scale.


**AI\-powered analytics experiences and domain applications (Agentic AI Applications)**


On the application side, **[Property Finder](https://clickhouse.com/blog/how-property-finder-migrated-to-clickhouse)** modernized its analytics foundation on AWS with ClickHouse, achieving major performance gains and cost reductions, while also enabling AI\-assisted analytics workflows, including natural language requests translated into SQL using **Amazon Bedrock**, and predictive modeling with **Amazon SageMaker**. In healthcare and life sciences, **[Memorial Sloan Kettering (cBioPortal)](https://clickhouse.com/blog/how-memorial-sloan-kettering-cancer-center-is-using-clickhouse-to-accelerate-cancer-research)** uses ClickHouse to accelerate large\-scale genomic analytics, and the cBioPortal team is also developing an AI\-powered chat experience built on **LibreChat** with **Claude via Amazon Bedrock**, connected to cBioPortal data through **MCP servers**, with queries executed against ClickHouse.


Beyond these six stories, you can also [explore](https://clickhouse.com/user-stories?useCase=4) how teams including **mpathic, SewerAI, RBC Borealis, poolside, Cognitiv, Lens, DENIC, AdMixer, and DeepL** are using ClickHouse for machine learning and GenAI workloads.


### **Looking ahead** [\#](/blog/aws-ai-services-competency#looking-ahead)


Agentic systems raise the bar for data infrastructure, especially as organizations demand stronger governance, lower latency, and clearer observability across increasingly autonomous workflows. We’re continuing to invest in helping teams build and run agentic solutions on AWS, from the ClickHouse core engine and ClickHouse Cloud to the **open\-source Agentic Data Stack** that connects natural language interfaces to large\-scale analytics.


If you’re building agentic AI tools or applications on AWS and want to accelerate from prototype to production, we’d love to work with you.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
