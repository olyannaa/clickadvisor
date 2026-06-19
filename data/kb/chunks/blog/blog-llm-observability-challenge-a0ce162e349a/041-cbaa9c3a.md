---
source: blog
url: https://en.wikipedia.org/wiki/Site_reliability_engineering
topic: can-llms-replace-on-call-sres-today
ch_version_introduced: '34.118'
last_updated: '2026-06-12'
chunk_index: 41
total_chunks_in_doc: 51
---

Failures during either placing an order or charging the payment, not being surfaced in logs, likely due to missing error logging/instrumentation. ``` Prompt 3: ``` Can you further down investigate the payment service ``` LLM response 3 (snippet):

```
Root Cause – Payment Service
	• The root cause of the payment service failure is:
“Visa cache full: cannot add new item.”
	• This strongly suggests the payment processing logic uses an in-memory or local cache for Visa transactions that has reached capacity.
	• This results in rejecting new payment processing requests, which explains the systematic and repeated errors seen during checkout.

```

##### Gemini 2\.5 Pro [\#](/blog/llm-observability-challenge#gemini-25-pro-3)

The test data set contains various repeated, but non\-problematic, errors. This kind of noise is common in observability data. When Gemini investigated this anomaly, it came across one of these errors and got stuck on this incorrect path. It then began to generate a very large table that reproduced a full trace, taking about 30 seconds to generate each row. We let it run for a few minutes, but ended up cancelling the generation.

We gave a follow up prompt with additional context about the user complaint, narrowing the area to the check out process. Gemini discovered one of the OTel demo feature flags (`cartFailure`) which was disabled for this test, and became convinced that this feature flag was the root cause of the problem, instructing us that we should enable the feature flag (enabling the feature flag would introduce a new, simulated failure mode.)

Directing Gemini away from the feature flag resulted in little progress \- it gave up and insisted we needed to implement more logging.

Expand below to see the full interaction.

Gemini 2\.5 Pro demo anomaly full interaction
Prompt 1:

```
You're  an  Observability  agent  and  have  access  to  OpenTelemetry  data  from  a  demo  application.  Users  have  reported  issues  using  the  application,  can  you  identify  what  is  the  issue,  the  root  cause  and  suggest  potential  solutions?

```

LLM response 1 (snippet):
