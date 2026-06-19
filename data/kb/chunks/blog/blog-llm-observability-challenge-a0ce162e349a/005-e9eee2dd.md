---
source: blog
url: https://en.wikipedia.org/wiki/Site_reliability_engineering
topic: can-llms-replace-on-call-sres-today
ch_version_introduced: '34.118'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 51
---

not, we ask follow up questions either based on the response it provided, or if it is completely off track, we provide additional context to help it get to a resolution. Then for each anomaly, we report on:

- What the model finds
- How accurate it is
- How much guidance it requires
- How many tokens it uses getting there
- How long it takes to run the investigation

This gives us a sense of how efficient and reliable each model is when dropped into a real\-world SRE task.

## Experiment walkthrough [\#](/blog/llm-observability-challenge#experiment-walkthrough)

In this section, we go through each anomaly and first document the manual investigation, then for each model we start with our simple prompt and document the model's finding. If the model is not successful at diagnosing the issue right away, we provide additional prompts to guide it. 

### Anomaly 1: Payment service failure [\#](/blog/llm-observability-challenge#anomaly-1-payment-service-failure)

Users are reporting issues during the checkout process, after filling in all the information related to the order, clicking on place order leads to an error. 

#### Manual investigation [\#](/blog/llm-observability-challenge#manual-investigation-1)

This is a simple issue to diagnose manually in ClickStack. We start by looking at one of the client sessions containing an error.

![anomaly-1-manual-1.png](/uploads/anomaly_1_manual_1_8d6ff13aa5.png)
From that specific session, we look at the trace view, where we can see an error message on the payment service. The message indicates that there is an invalid token for the loyalty level gold, which causes the payment request to fail.

![anomaly-1-manual-2.png](/uploads/anomaly_1_manual_2_ffa9a04df4.png)
We navigate to the traces explorer view, and filter the dashboard for the payment service.

![anomaly-1-manual-3.png](/uploads/anomaly_1_manual_3_fe0cbdef27.png)
This validates our finding, **the payment service has issues when processing requests from clients with a Gold loyalty status.**

#### LLM investigation [\#](/blog/llm-observability-challenge#llm-investigation)

##### Claude Sonnet 4 model [\#](/blog/llm-observability-challenge#claude-sonnet-4-model)

The model managed to find the RCA after the first prompt.

Expand below to see the full interaction.

Claude Sonnet 4 anomaly 1 full interaction
Prompt 1:

```
You're  an  Observability  agent  and  have  access  to  OpenTelemetry  data  from  a  demo  application.  Users  have  reported  issues  using  the  application,  can  you  identify  what  is  the  issue,  the  root  cause  and  suggest  potential  solutions?

```

LLM response 1 (snippet):
