---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Trace
topic: trace-and-evaluate-cursor-agents-with-langfuse-powered-by-clickhouse-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 2
total_chunks_in_doc: 5
---

queries. For a Cursor team, this means you can start with a cost trend, find the turns behind it, and inspect the model and tool activity that needs attention. ## Set up the Langfuse plugin in Cursor \#

1. Create a project in [Langfuse Cloud](https://cloud.langfuse.com/) or your [self\-hosted](https://langfuse.com/self-hosting) instance and copy its API keys.
2. Install [**Langfuse Observability** from the Cursor Marketplace](https://cursor.com/marketplace/langfuse/langfuse-observability): open **Customize**, go to **Plugins**, choose **Browse Marketplace**, and search for it.
3. Put your keys in `~/.cursor/langfuse.json`:

```
1{
2  "publicKey": "pk-lf-...",
3  "secretKey": "sk-lf-...",
4  "baseUrl": "https://cloud.langfuse.com"
5}
```
Copy command
This example uses the EU region. For other regions or a self\-hosted instance, use the corresponding base URL from the [integration docs](https://langfuse.com/integrations/developer-tools/cursor).

4. Restart Cursor and send a prompt to the agent.

The plugin is open source under the MIT license. It sends prompts, assistant messages, tool inputs and outputs, token usage, and other trace metadata to your Langfuse project. Capture of file\-read contents is off by default; enabling it requires both `captureFileContent` and `captureToolOutput`. The plugin masks your Langfuse keys and, by default, logs upload failures while keeping Cursor running. Set `enabled` to `false` in the config to disable it. The [integration docs](https://langfuse.com/integrations/developer-tools/cursor) cover every option, the Cursor CLI, and Cloud Agents.

## What a Cursor turn looks like in Langfuse \#

The plugin runs on Cursor hooks and creates one trace per prompt, named `Cursor Turn`. Inside it you find:

- An `LLM` observation for every assistant message, with the conversation history as input and the text, thinking, and requested tool calls as output.
- A tool observation for every tool the agent runs, such as `Shell`, `Read`, `StrReplace`, and MCP tools, with input, output, duration, and error status.
- Nested `Cursor Subagent` observations for subagents, and an event when Cursor compacts the context.

All turns of one conversation are grouped into a [session](https://langfuse.com/docs/observability/features/sessions), and the user defaults to the signed\-in Cursor account’s email unless you override it.

Cursor reports token usage once per turn, not per model call. The plugin records it on the last `LLM` observation of the turn, so read the cost from the trace total.

## Track cost and usage across a team \#
