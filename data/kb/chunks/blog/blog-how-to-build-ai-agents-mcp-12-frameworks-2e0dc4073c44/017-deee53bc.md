---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-to-build-ai-agents-with-mcp-12-framework-comparison-2025-clickhouse
ch_version_introduced: '3.10'
last_updated: '2026-09-07'
chunk_index: 17
total_chunks_in_doc: 22
---

that go beyond just MCP tools. Its extensive documentation and large community also mean you'll find examples and solutions for almost any integration challenge. 📄 [View the full LangChain example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/langchain) 🧪 [Try the LangChain notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/langchain/langchain.ipynb) ## LlamaIndex \#

[LlamaIndex](https://github.com/run-llama/llama_index/) (formerly GPT Index) specializes in **data\-aware AI applications**, particularly those involving retrieval\-augmented generation (RAG). While other frameworks focus on general agent capabilities, LlamaIndex is optimized for scenarios where agents need to work with large amounts of structured and unstructured data.

LlamaIndex's MCP integration is designed to work seamlessly with its data indexing and retrieval capabilities. This makes it particularly powerful when combined with analytical databases like ClickHouse \- you can use MCP tools to query structured data, then combine those results with LlamaIndex's document retrieval and synthesis capabilities to provide comprehensive answers.

Available in both Python and TypeScript:

```
1pip install llama-index llama-index-mcp
```
Copy command
And the code:

```
1from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
2
3mcp_client = BasicMCPClient(
4    "uv",
5    args=[
6        "run",
7        "--with", "mcp-clickhouse",
8        "--python", "3.13",
9        "mcp-clickhouse"
10    ],
11    env=env
12)
13
14mcp_tool_spec = McpToolSpec(
15    client=mcp_client,
16)
17
18tools = await mcp_tool_spec.to_tool_list_async()
19
20from llama_index.core.agent import AgentRunner, FunctionCallingAgentWorker
21
22agent_worker = FunctionCallingAgentWorker.from_tools(
23    tools=tools,
24    llm=llm, verbose=True, max_function_calls=10
25)
26agent = AgentRunner(agent_worker)
27
28from llama_index.llms.anthropic import Anthropic
29llm = Anthropic(model="claude-sonnet-4-0")
30
31response = agent.query("What's the most popular repository?")
```
Copy command

The framework's **query engine abstraction** is what sets it apart. Rather than thinking about individual tool calls, LlamaIndex lets you define complex query patterns that can automatically orchestrate multiple MCP servers, retrieve relevant documents, and synthesize responses. This is particularly useful for building agents that need to answer complex analytical questions by combining data from multiple sources.

📄 
[View the full LlamaIndex example](https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/llamaindex)
  

🧪 
[Try the LlamaIndex notebook](https://github.com/ClickHouse/examples/blob/main/ai/mcp/llamaindex/llamaindex.ipynb)

## PydanticAI \#

[PydanticAI](https://github.com/pydantic/pydantic-ai) launched in December 2024 by the team behind the popular Pydantic validation library. It brings Pydantic's philosophy of **type safety and data validation** to the world of AI agents. If you've ever struggled with agents returning inconsistently formatted data or making type errors when calling tools, PydanticAI aims to solve these problems.
