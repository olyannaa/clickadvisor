# Using the ClickHouse MCP server with Google Antigravity


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Using the ClickHouse MCP server with Google Antigravity

![](/_next/image?url=%2Fuploads%2Fdustin_72f62f769f.jpeg&w=96&q=75)[Dustin Healy](/authors/dustin-healy)Apr 22, 2026 · 5 minutes readAt ClickHouse, we’re working toward [our vision of agentic analytics](https://clickhouse.com/blog/agent-facing-analytics) and building the [Agentic Data Stack](https://clickhouse.com/ai). The [ClickHouse MCP server](https://github.com/clickhouse/clickhouse-mcp) is a key part of that vision, and allows ClickHouse to be integrated with the latest and greatest developer tools to bring the fastest analytics experience wherever developers work.


In this post, I’ll show you how to integrate the ClickHouse MCP server with Google [Antigravity](https://antigravity.google/), an agentic development platform


## Adding the ClickHouse MCP server to Antigravity [\#](/blog/google-antigravity#adding_the_clickhouse_mcp_server_to_antigravity)


[Antigravity supports MCP out of the box](https://antigravity.google/docs/mcp#connecting-custom-mcp-servers), so adding the ClickHouse MCP server is straightforward.


Within the Antigravity editor, [open the MCP Store panel within the "..." dropdown at the top of the editor's side panel](https://antigravity.google/docs/mcp#how-to-connect). Select ClickHouse from the list of servers and click Install. You will be redirected via OAuth in your browser to the ClickHouse sign in page to authenticate the connection.


![antigravity_mcp_apr2026_image1.png](/uploads/antigravity_mcp_apr2026_image1_d75a9c1887.png)
Once connected, **the Antigravity agent gains read\-only access to your organizations, services, databases, and tables according to your account permissions**, allowing it to perform high\-speed analytical queries on your behalf.


## Automatic discovery [\#](/blog/google-antigravity#automatic_discovery)


Once the MCP connection is active and authenticated via OAuth the agent will now have the ability to call tools supplied by the ClickHouse MCP server when prompted, allowing it to begin discovering the location and format of your data automatically.


![](/uploads/antigravity_mcp_apr2026_image4_6a8a38eb97.png)
You can use prompts like "What tables are available?" or "Show me the schema for the UK properties price table." and the agent will use tools like `get_services_list` and `list_tables` to orient and ground itself in your data structure.


In this example, we’re working with our `uk_prices_1` example dataset, which has millions of UK property transactions. The agent identifies the relevant columns (`price`, `town`, `district`, `date`) and prepares to help us find meaningful trends.


![](/uploads/antigravity_mcp_apr2026_image5_406c3233d4.png)
## Analyse data in natural language [\#](/blog/google-antigravity#analyse_data_in_natural_language)


The ClickHouse MCP server allows you to use natural language to query your data. The agent will handle translating natural language into functional ClickHouse SQL.


When prompted with something like "Analyze property price trends in London over the last decade and compare them to the national average.", Antigravity converts that prompt into the correct SQL statement and executes it using the `run_select_query` tool.


Because ClickHouse is built for speed, results of queries are fast, and you can have real\-time conversations with your data.


## Generating Antigravity Artifacts [\#](/blog/google-antigravity#generating_antigravity_artifacts)


You’re not limited to just text. Through Artifacts, Antigravity can also generate custom visualizations for your data.


For example, when we asked for a visual breakdown of the data, the agent generated a React\-based interactive chart as an Artifact. The integrated browser renders the Artifact, so we can review it without leaving the IDE.


Antigravity goes a step further than just showing us the Artifact it created: it tests it too. The agent uses the browser to interact with the chart (for example, clicking on tabs) and uses screenshots and screen recordings to watch what happens and validate that the Artifact is displaying and behaving correctly.


![](/uploads/antigravity_mcp_apr2026_image3_10410c758b.png)
## Interactive iteration on Artifacts [\#](/blog/google-antigravity#interactive_iteration_on_artifacts)


Data analysis is rarely a one\-step process.


After Antigravity generated a visualisation, we noticed a peak in the pricing chart and got curious \- what caused this peak? Is the trend consistent across property types? Antigravity’s **Comments on Artifacts** feature allows us to drag a box over the peak, and ask our question with the visual context of the chart.


The agent immediately saw the context of our comment, queried the ClickHouse database again, answered our question and updated the Artifact to include the new breakdown.


For a data analysis workflow, being able to iterate an Artifact by visually interacting with it is a pretty big deal. This kind of iteration has traditionally meant JIRA tickets, hand\-offs between data engineers and business analysts, and a bunch of screenshots.


![](/uploads/antigravity_mcp_apr2026_image2_ce259cda3a.png)
## Conclusion [\#](/blog/google-antigravity#conclusion)


The ClickHouse MCP server makes it possible to integrate ClickHouse with AI\-native IDEs like Google Antigravity. Antigravity brings innovative features like commenting on Artifacts that bring workflow improvements that developers and data analysts have been dreaming about for years. Together, ClickHouse and Antigravity provide a compelling example of the future of agentic analytics.


Are you using ClickHouse with Google Antigravity? We’d love to hear about your use cases! [Come chat with us in our Slack community.](http://clickhouse.com/slack)

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-466-get-started-today-sign-up&utm_blogctaid=466)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
