# Open House observability announcements: MCP server, AI Notebooks, and ClickStack Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Open House observability announcements: MCP server, AI Notebooks, and ClickStack Cloud

![](/_next/image?url=%2Fuploads%2Fmike_shi_5b7145e7d7.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2FImage_512x512_15_b10c118c8e.jpeg&w=96&q=75)[Mike Shi](/authors/mike-shi) and [Brandon Pereira](/authors/brandon-pereira)May 27, 2026 · 13 minutes readOpen House brought the ClickHouse community together for three days of workshops, technical deep dives, product announcements, demos, and conversations about what’s next for real\-time data. We were glad to meet so many users, customers, and members of the observability community throughout the event.


For those who couldn’t join us in person, here’s a recap of the observability announcements we shared at Open House.


We announced three major updates across ClickStack and observability: ClickStack Cloud, AI Notebooks in beta, and a new ClickStack MCP server.


## ClickStack Cloud [\#](/blog/observability-mcp-server-ai-notebooks#clickstack-cloud)


The biggest announcement, and one that deserved its own [blog post](https://clickhouse.com/blog/clickstack-cloud-private-preview), was the introduction of ClickStack Cloud in private preview.


ClickStack Cloud is a fully managed, serverless observability platform built on ClickHouse. Instead of managing collectors, infrastructure sizing, scaling policies, or schema tuning directly, users simply send OpenTelemetry data to a managed endpoint and immediately start exploring logs, metrics, and traces through the ClickStack UI.


ClickStack Cloud is aimed at reducing that operational work while still keeping the performance characteristics people love about ClickHouse.


For more details, we recommend the [dedicated post](https://clickhouse.com/blog/clickstack-cloud-private-preview).


### Managed ClickStack is generally available [\#](/blog/observability-mcp-server-ai-notebooks#managed-clickstack-is-generally-available)


In addition to ClickStack Cloud entering private preview, our existing Managed ClickStack offering is now generally available.


Managed ClickStack is designed for teams that want direct operational control over their observability stack, including ingestion pipelines, compute sizing, workload isolation, schema design, and datastore tuning. Users manage their own OpenTelemetry collectors and ingestion architecture while using ClickHouse Cloud as the underlying observability datastore. For many large\-scale deployments, that control is essential for optimizing performance and achieving market\-leading cost efficiency.


Managed ClickStack and ClickStack Cloud are designed for different operational models.


As discussed above, ClickStack Cloud will provide a fully managed, serverless observability experience where teams send telemetry to a managed endpoint and immediately begin exploring logs, metrics, and traces without managing infrastructure directly. Conversely, Managed ClickStack is intended for organizations that want deeper control over scaling strategy, ingestion architecture, and workload optimization while still running on ClickHouse Cloud infrastructure. Together, the two offerings give teams a choice between a turn\-key observability experience and a more configurable platform for operating observability at scale.


![](/uploads/clickstack_cloud_may2026_image4_d8d0f91b43.png)
## AI Notebooks in Beta [\#](/blog/observability-mcp-server-ai-notebooks#ai-notebooks-in-beta)


We also announced AI Notebooks entering beta for Managed ClickStack.


Over the last year, nearly every observability platform has added some form of AI chat experience, but we increasingly felt that chat alone does not match how real incident investigations actually unfold. Production debugging is messy, and engineers jump between logs, traces, dashboards, deployments, and hypotheses. They backtrack, split into parallel investigations, and revisit earlier assumptions as new signals appear. Incidents are rarely single\-threaded conversations, so we did not want the interface to force them into one.


![](/uploads/clickstack_cloud_may2026_image5_4095d770f0.png)

> Investigations are rarely single\-threaded. SREs typically need to explore multiple branching hypotheses before reaching a resolution.


AI Notebooks are designed as a persistent investigative workspace rather than a transient chat session. Each investigation becomes a structured sequence of prompts, queries, charts, reasoning steps, and findings that remain visible and editable throughout the process.


Engineers can branch from any point in the notebook to explore alternative theories without losing previous work or context. In practice, the workflow feels more like a collaborative debugging experience.

Loading video...We were also pretty opinionated about transparency while building this. In a production incident, engineers need to understand what the system is actually doing, especially if AI is involved in the investigation loop. Every query, chart, reasoning step, and intermediate result is visible inside the notebook. You can edit queries manually, insert your own searches, or ignore the suggested path entirely and take the investigation somewhere else. We wanted the AI to behave more like a collaborator sitting beside the engineer than a system producing black\-box conclusions in the background.


![](/uploads/clickstack_cloud_may2026_image6_02f1301f8d.png)
Underneath the interface, Notebooks are built directly on top of ClickStack’s observability primitives and optimized ClickHouse workflows. The system is not simply attaching an LLM to a SQL console. The model operates against structured investigative tools that already power ClickStack itself, allowing it to execute optimized searches, aggregations, and visualizations while still exposing the generated queries for inspection and refinement. Notebooks can also be shared across teams, turning investigations into persistent collaborative artifacts instead of disposable chat histories that disappear once the incident ends.


For users already running Managed ClickStack, AI Notebooks are now available directly from the left navigation panel inside the ClickStack UI.


![](/uploads/clickstack_cloud_may2026_image7_ae16f00c1f.png)
Finally, the Notebook experience also naturally led us to our third observability announcement at Open House. As part of building structured investigative workflows inside ClickStack, we also introduced a new ClickStack MCP server, allowing external AI systems and agents to integrate directly with the same observability primitives that power Notebooks internally.


## ClickStack MCP Server [\#](/blog/observability-mcp-server-ai-notebooks#clickstack-mcp-server)


Alongside Notebooks, we also spent time at Open House discussing a broader shift we think is underway in AI and observability tooling.


While AI\-assisted investigation inside ClickStack matters, we think teams will want to leverage the same powerful tools we expose within ClickStack in their own agents. Increasingly, users are building their own agents, prompts, workflows, and automation around observability data. Some are doing this inside Cursor or Claude Code. Others are wiring together SDKs and running agents locally against internal systems. In many cases, the teams building these workflows already have strong operational knowledge baked into how they debug incidents, and they want their tooling to reflect that.


Our view is that observability platforms should meet users where they already work instead of forcing them into a single AI experience, and we want to build based on a “Bring your own agents” philosophy.


The first step is to expose the same investigative building blocks that power ClickStack Notebooks internally and make them available to external agents and workflows. For this, we are pleased to announce the ClickStack MCP server in open source ClickStack.


### Why a specialized ClickStack MCP? [\#](/blog/observability-mcp-server-ai-notebooks#why-a-specialized-clickstack-mcp)


There is already a generic ClickHouse MCP server available today, and it works well for broad analytical tasks and SQL\-driven exploration. But while building AI Notebooks, we repeatedly found that observability workflows behave differently from general BI workloads. Models perform much better when they operate against structured investigative tools rather than generating raw SQL queries over and over again.


![](/uploads/clickstack_cloud_may2026_image8_e7cbc93a2a.png)

> AI for observability with ClickHouse combines collaborative notebook experiences and MCP tools delivered through ClickStack, integrations with external agents such as Claude and Codex, and ClickHouse as the high\-performance analytics engine enabling full\-fidelity investigations with sub\-second query performance and high concurrency at scale.


Raw SQL is powerful, but many observability investigations are awkward to express as one\-off queries. Tasks like mining recurring log patterns, comparing behavior across time windows, root causing trace outliers, or following an investigation across logs, metrics, and traces require multi\-step analysis and domain\-specific logic. Leaving all of that to the model means it has to reconstruct the required query patterns and analysis logic from scratch each time, spending context on query mechanics instead of the problem itself.


The ClickStack MCP server gives agents higher\-level semantic tools for observability work. Instead of exposing only a raw SQL interface, it provides stable tools for finding trends in patterns of logs, correlating attributes with outliers, inspecting slow traces, and moving through an investigation with repeatable workflows. Under the hood, those tools still execute optimized ClickHouse queries, but the agent interacts with intent\-level operations rather than hand\-assembling complex analysis every time.


This is the same approach used inside AI Notebooks. The model is not manually stitching together large SQL statements for every step of an investigation. Instead, it works against specialized tools that already understand the underlying observability workflows and ClickStack optimizations.


In our internal benchmarks, investigations completed with 25% fewer tool calls, showed a 2\.5x increase in consistency and improved evaluation scores by almost 20% vs the standard ClickHouse MCP. A large part of that came from giving the model high\-leverage semantic investigation tools instead of forcing it to generate every workflow from raw SQL alone.


### Retaining flexibility [\#](/blog/observability-mcp-server-ai-notebooks#retaining-flexibility)


At the same time, we do not think structured investigative tools should completely replace direct SQL access.


One of the reasons ClickHouse works so well for agentic workloads and observability is that SQL remains an incredibly powerful exploratory language. Sometimes an incident eventually reaches a point where there is no higher\-level abstraction that helps anymore, and you simply need direct access to the underlying data. The structured tools handle many of the repetitive and common investigation paths efficiently, but SQL remains the escape hatch when engineers or agents need to go deeper, test unusual hypotheses, or answer questions the system was never explicitly designed around.


In practice, the workflows end up complementing each other quite naturally: use optimized investigative primitives for the majority of the investigation, then drop into native queries when the situation calls for it.


### Orchestration, not just investigation [\#](/blog/observability-mcp-server-ai-notebooks#orchestration-not-just-investigation)


While some engineers are perfectly happy working directly in the terminal or inside an agent harness like Claude Code, investigations eventually need to be shared with other people. SREs need to collaborate, preserve context, and present evidence once they reach a conclusion.


That is why we do not think observability MCP servers should only expose investigative primitives. Real operational workflows also require orchestration primitives for creating dashboards, persisting searches, managing alerts, and sharing findings across teams.


This becomes especially important for local agent workflows. If an agent investigates an incident locally, the resulting evidence needs to be persisted somewhere for sharing and review by the larger team. Copying raw chat output into documents or generating static reports quickly breaks down during real incidents, leading to inconsistencies.


For that reason, the ClickStack MCP server exposes bi\-directional management tools directly inside ClickStack itself. Agents can not only investigate incidents, but also create dashboards, persist searches, and validate that the resulting artifacts contain the required evidence and visualizations.


In practice, investigations naturally evolve into persistent operational artifacts rather than disposable chat histories.


### Using the MCP [\#](/blog/observability-mcp-server-ai-notebooks#using-the-mcp)


Getting started with the ClickStack MCP server is straightforward. The easiest way to try the full stack locally is to [use the ClickStack all\-in\-one container](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started/oss), which includes ClickHouse, the ClickStack UI (HyperDX), an OpenTelemetry ingestion endpoint, and the MCP server.



```

```
1docker run --name clickstack \
2  -p 8123:8123 \
3  -p 8080:8080 \
4  -p 4317:4317 \
5  -p 4318:4318 \
6  clickhouse/clickstack-all-in-one:latest \
7  clickstack
```

```

Once the container is running, the ClickStack UI will be available at <http://localhost:8080>. Create a user and log\-in.


For a sample dataset, you can modify your local data source to point to our demo server by following steps (1\) and (2\) in [this guide](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started/remote-demo-data#connect-to-the-demo-server).


To use the MCP server, you will also need a Personal API Access Key. Inside the ClickStack UI, navigate to: `Team Settings` → `Integrations` → `API Keys` → `Personal API Access Key`.


![](/uploads/clickstack_cloud_may2026_image9_be45abcb79.png)
The MCP endpoint is exposed at <http://localhost:8080/api/mcp>.


From there, you can connect whichever MCP\-compatible client or agent framework you already use.


For example, to connect Claude Code:



```

```
1claude mcp add --transport http clickstack http://localhost:8080/api/mcp \
2  --header "Authorization: Bearer <your-api-key>"
```

```


```
Added HTTP MCP server clickstack with URL: http://localhost:8080/api/mcp to local config
Headers: {
  "Authorization": "Bearer &lt;your-api-key&gt;"
}
File modified: /Users/demo_user/.claude.json [project: /Users/demo_user]

```

Once connected, the agent can begin interacting directly with ClickStack’s observability primitives. For example, you can ask questions like:


“Show me the services with the highest error rate over the last hour”


![](/uploads/clickstack_cloud_may2026_image10_ad26cd5f59.png)
Underneath, the MCP server routes these requests through the same optimized investigative tools used by AI Notebooks rather than relying entirely on ad hoc SQL generation.


Suppose we investigate elevated latency in a payment service and eventually determine, through Claude, that the root cause is a cache eviction issue.


![](/uploads/clickstack_cloud_may2026_image11_d6a8f4ef67.png)
At that point, we need a way to persist and share the investigation. We could copy the raw Claude output into a document or ask the model to generate a static HTML report, but neither workflow feels particularly natural.


Below, we use the MCP server to generate a dashboard summarizing the investigation and to persist the findings directly in ClickStack, with a validation step confirming that the dashboard presents the required evidence.


![](/uploads/clickstack_cloud_may2026_image12_68ca0875fc.png)
![](/uploads/clickstack_cloud_may2026_image13_a6ed816b79.png)
Our resulting dashboard provides a persisted artifact summarizing the incident and presenting evidence for any RCA document.


## Conclusion [\#](/blog/observability-mcp-server-ai-notebooks#conclusion)


These announcements all reflect the same broader direction: observability tooling should help engineers investigate systems without locking them into predefined workflows. ClickStack Cloud reduces much of the operational burden, AI Notebooks make investigations easier to document and share, and the MCP server lets teams integrate the same capabilities into their own agents and internal tooling. We’re still at the beginning of this shift, but we expect observability systems to become far more collaborative and programmable than the tooling most teams rely on today.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-700-get-started-today-sign-up&utm_blogctaid=700)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
