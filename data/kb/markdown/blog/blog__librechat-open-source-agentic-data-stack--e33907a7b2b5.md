# ClickHouse welcomes LibreChat: Introducing the open\-source Agentic Data Stack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse welcomes LibreChat: Introducing the open\-source Agentic Data Stack

![](/_next/image?url=%2Fuploads%2FDanny_Avila_Profile_e70daa05ef.jpeg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fspeaker_ryadh_dahimene_3980a57ceb.png&w=96&q=75)Ryadh Dahimene and Danny AvilaNov 4, 2025 · 11 minutes readWe are excited to announce that ClickHouse has acquired LibreChat, the leading open\-source AI chat platform that offers a unified interface for interacting with a wide range of large language models (LLMs), giving users and organizations full control over their data, agents, and conversations. We couldn't be more thrilled to welcome Danny Avila (the founder of LibreChat) as well as the LibreChat team and community into the ClickHouse family.


LibreChat becomes a core component in our vision for [Agent\-Facing Analytics](https://clickhouse.com/blog/agent-facing-analytics), creating a truly open\-source Agentic Data Stack. By combining LibreChat's powerful user experience and AI agent framework with ClickHouse's analytical capabilities at scale, it has never been easier to build analytics agents that can be leveraged to expose massive datasets to agents operating on behalf of users.


## Who is building agentic analytics already? [\#](/blog/librechat-open-source-agentic-data-stack#who-is-building-agentic-analytics-already)


Usually, in similar announcements, the user quotes are often buried deep into the post. We’ll try to do things a bit differently here and lead with the raw, unfiltered user feedback, then state our thesis right after (you can skip straight to our investment thesis by clicking [here](https://clickhouse.com/blog/librechat-open-source-agentic-data-stack#reducing-time-to-insight)).


### Shopify [\#](/blog/librechat-open-source-agentic-data-stack#shopify)


Shopify, a global e\-commerce leader, has embedded AI across its operations, giving employees access to advanced models through a unified internal platform. Using the [open\-source LibreChat platform](https://www.firstround.com/ai/shopify), Shopify built tools like an RFP assistant that pulls from company data, rates response confidence, and improves over time.



> “LibreChat powers reflexive AI use across Shopify. With near universal adoption and thousands of custom agents, teams use it to solve real problems, increase productivity, and keep the quality bar high. By connecting more than 30 internal MCP servers, it democratizes access to critical information across the company”   
> 
>   
> 
> *Matt Burnett, Senior Engineer at Shopify*




> Shopify runs an internal fork of librechat, and we merge most everything back. I highly recommend other companies give this project a look for their internal LLM system. It works very well for us. <https://t.co/ihExJyXY2i>
> 
> — tobi lutke (@tobi) [June 11, 2025](https://twitter.com/tobi/status/1932846291794510241?ref_src=twsrc%5Etfw)

 

### cBioPortal [\#](/blog/librechat-open-source-agentic-data-stack#cbioportal)


The [cBioPortal for Cancer Genomics](https://www.cbioportal.org/) provides visualization, analysis, and download of large\-scale cancer genomics data sets. The team at cBioPortal recently launched the chat\-based [cBioAgent](https://chat.cbioportal.org/) that allows users to interact with genomics datasets in plain text ([example interaction](https://chat.cbioportal.org/share/s2NZmrgtC7neWPM0L3Vl2)).



> “By leveraging the ClickHouse, MCP, and LibreChat stack, we rapidly delivered a prototype to cBioPortal users that empowered them to ask entirely new questions about cancer genomics and treatment trajectories, get quick answers, and explore data in ways not possible through the existing UI. It puts discovery at cancer researchers' fingertips.”   
> 
>   
> 
> *Ino de Bruijn, Manager Bioinformatics Software Engineering, cBioPortal*


### Fetch [\#](/blog/librechat-open-source-agentic-data-stack#fetch)


[Fetch](https://fetch.com/) is a leading mobile rewards app that allows users to earn points by scanning shopping receipts and redeem them for gift cards. Fetch recently launched [FAST](https://fast.fetch.com/): an AI\-powered tool that turns household purchase behavior into business intelligence, insights, and media activation. Running a custom UX for the FAST portal, this use case is a great illustration of user\-facing agentic analytics.



> “We built our new product, FAST by Fetch, on ClickHouse to help users instantly discover insights and drive efficient activation. We see agentic analytics as the future of data interaction, enabling more intuitive, dynamic, and impactful use of information. With its unmatched speed and scalability, ClickHouse is well\-positioned to power this new generation of agentic experiences, and we’re thrilled to grow our partnership together.”   
> 
>   
> 
> *Sam Corzine, Director of Machine Learning, Fetch*


### SecurityHQ [\#](/blog/librechat-open-source-agentic-data-stack#securityhq)


SecurityHQ is a global Managed Security Service Provider (MSSP) offering 24/7 threat detection, response, and risk management through its worldwide Security Operations Centres.



> "We reached out to ClickHouse to present our use case in building an Agentic AI with ClickHouse MCP and LibreChat similar to what [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) provide. After understanding the implementation strategy used for AgentHouse, we managed to create a robust working prototype of what we wanted. The integration between ClickHouse cloud and the LibreChat using the MCP server has been flawless, making them one of, if not the best use of text\-to\-SQL implementation I have ever seen. Now that ClickHouse and LibreChat has joined forces will provide even more seamless interaction to our use case in building Agentic Analytics. Looking forward for a LibreHouse cloud solution for agentic analytics."   
> 
>   
> 
> *Nidharshanen Selliah, Associate Data Engineer, SecurityHQ*


### Daimler Truck [\#](/blog/librechat-open-source-agentic-data-stack#daimler-truck)


Daimler Truck, one of the world’s largest commercial vehicle manufacturers, has deployed LibreChat internally to give all employees secure access to chat tools and data agents. The system democratizes AI use across the company while protecting data and meeting compliance standards. They published a [detailed story](https://www.daimlertruck.com/en/newsroom/stories/daimler-truck-makes-artificial-intelligence-accessible-to-all-employees-worldwide-with-librechat) about their setup of LibreChat.



> “With LibreChat, Daimler Truck is making the power of modern AI available to all employees. This enables the company to bring innovation and progress into everyday work – simply, transparently, securely, and full of new opportunities.”   
> 
>   
> 
> From: [https://www.daimlertruck.com/en/newsroom/stories/daimler\-truck\-makes\-artificial\-intelligence\-accessible\-to\-all\-employees\-worldwide\-with\-librechat](https://www.daimlertruck.com/en/newsroom/stories/daimler-truck-makes-artificial-intelligence-accessible-to-all-employees-worldwide-with-librechat)


### and … ClickHouse [\#](/blog/librechat-open-source-agentic-data-stack#and--clickhouse)


Finally, we also use LibreChat on top of our ClickHouse data warehouse internally as well. We deployed several agents that range from product analytics to billing data and support cases analysis. We’ll let you guess from the screenshot below which one is which.


![image1.png](/uploads/image1_4a06083ea0.png)

> “Internally, we also use LibreChat for data analysis and it now handles \~70% of our data warehouse queries for 200\+ users. The productivity boost has been remarkable. What impressed me most is LibreChat's vibrant community that continuously contributes and innovates. The synergy between ClickHouse Cloud's blazing\-fast query performance and LibreChat's flexible, multi\-LLM architecture is unlocking a new generation of data analysis agents \- real\-time, secure, powerful, and accessible.”   
> 
>   
> 
> *Dmitry Pavlov, Director of Engineering, ClickHouse*


Now, let’s dive into the motivation behind the Agentic Data Stack.


## Reducing Time to Insight [\#](/blog/librechat-open-source-agentic-data-stack#reducing-time-to-insight)


[We are obsessed with world\-class speed and performance at ClickHouse.](https://benchmark.clickhouse.com/) However, traditional analytics workflows often involve multiple handoffs between data engineers writing queries, analysts building dashboards, and business users interpreting results. Each step introduces latency on the left and right sides of the database, often measured in hours or days.


With agentic analytics, that timeline collapses to seconds or minutes. A product manager can ask "What's driving the spike in churn last week?" and immediately receive not just the answer, but the underlying queries, explorations, visualizations, and potential next questions to explore.


This is closely aligned with our own experience at ClickHouse. Earlier this year, we introduced our first agent, Dwaine (Data Warehouse AI Natural Expert): an internal agent that enables our team to query business data through natural language. Since then, questions like "What's our current revenue?", "How is this customer using our product?", "What issues are customers experiencing?" or "What's our website traffic and conversion rate?" are getting close to instant answers.


Dwaine has transformed how our internal teams access insights, eliminating the bottleneck of hand\-writing SQL queries and data requests. Just one month after rollout, ClickHouse internal users generated more than 15 million LLM tokens in a single day on Dwaine. As of October 2025, this is now up at 33 million tokens per day.


!['The first 3 months of DWAINE - Token Counts per Day'](/uploads/image5_2176472bfd.png)
*The first 3 months of DWAINE \- Token Counts per Day*


If you want to experience the power of agentic analytics first\-hand, try the public [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) demo, which exposes publicly available datasets via the Agentic Data Stack.


!['AgentHouse in use'](/uploads/agent_house_v3_7e163b96ca.gif)
## The open\-source advantage [\#](/blog/librechat-open-source-agentic-data-stack#the-open-source-advantage)


The agentic open\-source landscape is currently centered around developer tooling and SDKs, which makes perfect sense given that developers are typically the earliest adopters of emerging technologies. The main open\-source projects in this space aim to empower builders to create, extend, and customize agentic systems with SDKs, frameworks, orchestration layers, and integrations. This developer\-first focus helps establish the foundational ecosystem and standards needed before broader consumer applications take off.


We see the Agentic Data Stack as one of the first proposals of a composable software stack that focuses on the higher\-level integration story, allowing users to get started and deliver value in no time. Both ClickHouse and LibreChat share the same open\-source software DNA, and joining forces strengthens our commitment to that vision:


- **LibreChat remains 100% open\-source** under its existing MIT license
- **Community\-first development** continues with the same transparency and openness
- **Expanded roadmap** to bring an even more enterprise\-ready analytics experience.


This proven playbook is the same one that we applied when joining forces with [PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) to provide our ClickPipes CDC capabilities, and [HyperDX](https://clickhouse.com/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability), which became the UX of our observability product, ClickStack.


We believe that being good stewards of open\-source means not just maintaining code, but actively investing in and growing the communities that depend on it.


## Limitations [\#](/blog/librechat-open-source-agentic-data-stack#limitations)


Large Language Models can be tricky to use in production. While grounding responses in real\-time data often helps, AI agents are not immune to hallucinations: situations where the model generates incorrect information with high confidence.


Our own experience running internal agents within ClickHouse taught us that the best remediation comes from providing the LLMs with the maximum and most accurate context possible. This can be achieved by commenting the tables using the SQL [COMMENT](https://clickhouse.com/docs/sql-reference/statements/alter/column#comment-column) syntax, for example, or by providing more context in\-line, in the chat, or part of the system prompt of the LLM session.


Finally, robust evaluations are critical for agentic analytics in production because they turn qualitative agent behavior into quantifiable insights, enabling teams to measure effectiveness, detect regressions, and continuously improve system performance.


## What's next for LibreChat and ClickHouse users? [\#](/blog/librechat-open-source-agentic-data-stack#whats-next-for-librechat-and-clickhouse-users)


For existing LibreChat deployments: nothing changes. LibreChat continues to work exactly as it does today, and we are committed to continuing to invest in it and make sure the community thrives.


For ClickHouse users, over the coming months, we'll be releasing tailored integration capabilities that make LibreChat a native part of the ClickHouse experience without sacrificing its generic integration capabilities. Think of it as a “happy path” for agentic analytics in LibreChat. This will include:


- Seamless integration of the LibreChat experience alongside your ClickHouse Cloud instances
- Extended support for data visualizations rendering in LibreChat
- OAuth, end\-to\-end user identification, security, and governance schemes.
- Tailored context providing (aka. semantic layer)


And many more. Please stay tuned for more updates by joining our communities in [Slack](https://clickhouse.com/slack) and [Discord](https://discord.com/invite/librechat-1086345563026489514).


Finally, for users of the [LibreChat Code Interpreter API](https://code.librechat.ai/pricing) (a paid service offered by LibreChat that provides a sandboxed environment for executing code). We are planning to evolve this offering and discontinue this API in its current form. We understand that changes can take time to implement, and for this reason, we decided to set the timeline of this transition for the next 6 months (targeting May 1st, 2026\). We will reach out to all code interpreter users directly to coordinate the transition.


## Get started [\#](/blog/librechat-open-source-agentic-data-stack#get-started)


**For LibreChat users:** Continue using LibreChat as you always have, and join our community on [Discord](https://discord.com/invite/librechat-1086345563026489514) if you haven’t already, to connect with other users building agents.


**For ClickHouse users**: You can already deploy the Agentic Data Stack by following our user guides in our public [documentation](https://clickhouse.com/docs/use-cases/AI/MCP/librechat) and [videos](https://www.youtube.com/watch?v=fuyu-AnfRDA)


**For everyone else**: Experience the power of the open\-source Agentic Data Stack with [AgentHouse](https://llm.clickhouse.com/), and let us know how we can help you succeed!



As always, the ClickHouse team would be honored to partner with you on your journey toward agentic analytics. Whether you're using LibreChat today or are interested in building analytical agents, please [contact us](https://clickhouse.com/company/contact)!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
