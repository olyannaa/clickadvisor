---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"The
topic: the-agentic-analytics-benchmark-measuring-model-accuracy-and-efficiency-in-analytical-agents-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 11
total_chunks_in_doc: 14
---

to 100\. The n column is the number of failures. For example, DeepSeek v4 Pro has 45 failures and 69% (31\) of them are type FM2\. This helps to show the shape of how models fail. ![Figure 12](/_next/image?url=%2Fuploads%2Ffailure_modes_874a272967.png&w=2048&q=75)

*Each model's failures split across the five failure modes. Rows are percentages of that model's failures, not of its questions, and sum to 100; how often a model fails is the leaderboard's job. Turn\-limited runs are excluded here as "ran out of budget."*

FM2 (wrong plan) is by far the most common, at 53 to 82% of failures for every model with a substantial failure count.

FM5 (runtime error) is close to absent. Only four models record any at all, and only Gemma 4 31B exceeds 2%, so modern models rarely write SQL that fails to execute.

FM1 (no attempt) is a different story. It is generally absent, but grows towards the bottom of the board. It reaches 34% for Gemini 2\.5 Flash, 27% for Gemini 2\.5 Pro and 23% for Qwen3\-Coder 30B, all in the bottom third, while seven of the top ten models record none at all. The highest occurrences are with older and/or smaller models, though not exclusively, as GPT\-5\.5 and 5\.6 both have 3 to 5% of failures in this group.

Fable 5\.1 (the board leader) stands out for FM3 (wrong data), at 28% of its failures against 19 to 23% for the models around it. That is the highest rate on the board, and it comes with the lowest FM2 share in the top ten at 57%: it plans well and then picks the wrong field or grain.

These results show that SQL syntax and execution are no longer bottlenecks for modern models. For agentic analytics, data modeling and schema context matter far more.

## The right model for the right task \#

From the results, can we conclude that the frontier models are the best fit for agentic analytics?
