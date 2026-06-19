---
source: blog
url: https://www.reddit.com/r/explainlikeimfive/)*
topic: agent-facing-analytics
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 11
---

triggers the model to get familiar with the datasets. Claude runs the `list_tables` tool on two databases: Forex and Stock then requests data samples by running select queries (note that the previous prompt asked about all available datasets).

![7_agent-analytics.png](/uploads/7_agent_analytics_329cb2753c.png)
Later, we asked about the tech stocks that were hit the worst by the dot com bubble. Note that the question was purposefully vague with no specific dates or field names mentioned, however, the model still managed to understand the scope of the query, propose a relevant methodology, a metric, and a time range, and run the analysis requested. It is interesting to compare the duration of this task to the time needed for an analyst to produce a similar result.

![image (7).png](/uploads/8_agent_analytics_6f4227459e.png)
*Iterative exploration of the data by Claude*

The prompts we submitted for this investigation resulted in a total of 10 SQL queries to the database. The result is a set of insights extracted from raw data, in a few seconds, with supporting visualization and descriptive analysis.

![9_agent-analytics.png](/uploads/9_agent_analytics_1d451ffde6.png)
![10_agent-analytics.png](/uploads/10_agent_analytics_fa7a7e685d.png)
Even if exciting, this approach has known limitations and isn’t a silver bullet. While grounding responses in real\-time data helps, AI agents are not immune to hallucinations: situations where the model generates incorrect information with high confidence. Ensuring data integrity (e.g. with templated queries), setting sensible default settings (e.g. [temperature](https://www.ibm.com/think/topics/llm-temperature)), and implementing safeguards to verify AI\-generated outputs are crucial steps required for minimizing this risk.

### Run it on your laptop! [\#](/blog/agent-facing-analytics#run-it-on-your-laptop)

The best way to grasp this use case is to try it yourself. You’ll find details about how to connect to the ClickHouse public playground service in our [documentation](https://clickhouse.com/docs/en/getting-started/playground). The setup of the ClickHouse MCP Server with Claude desktop is also described in its [README](https://github.com/ClickHouse/mcp-clickhouse/blob/main/README.md) file. Finally, you can also set up a local offline version with an alternative, tools\-compatible model. We experimented with a local setup using the following components:

- Model: [llama3\.2 3B](https://ollama.com/library/llama3.2) running on Ollama
- Client: [mcp\-cli](https://github.com/chrishayuk/mcp-cli)
