# We taught ClickStack to read your logs like a detective novel


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# We taught ClickStack to read your logs like a detective novel

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)Apr 1, 2026 · 5 minutes read## We taught ClickStack to read your logs like a detective novel [\#](/blog/clickstack-read-logs-detective-novel#we-taught-clickstack-to-read-your-logs-like-a-detective-novel)


If you've ever been paged at 3am and stared at a wall of `EmptyCartAsync called with userId=a0cd950c-39ec-11f0-8ddd-a2eca416a8a4` wondering what it means for the business \-\- you're not alone.


Logs are written by machines, for machines. Traces are trees of span with nanosecond timestamps. Log patterns are clusters of identical messages that tell you *something* is happening 113,526 times but won't tell you *why you should care*. The gap between raw telemetry and human understanding is where SRE time goes to die.


Today we're shipping **AI Summarize** \-\- a new feature in HyperDX that generates narrative summaries of your logs, traces, and log patterns. It works on any event in the side panel and on the pattern drawer. One click, and your cryptic span becomes a story.


## What It Looks Like [\#](/blog/clickstack-read-logs-detective-novel#what-it-looks-like)


Open any log entry, trace span, or log pattern in HyperDX. You'll see a new **Summarize** button below the event body. Click it, and after a brief analysis you get something like this:


![april_fools_ai_clickstack_1.png](/uploads/april_fools_ai_clickstack_1_112d4f71ce.png)
Or maybe you'll get David Attenborough narrating your checkout flow:


![april_fools_ai_clickstack_2.png](/uploads/april_fools_ai_clickstack_2_2b7d270393.png)
Or Shakespeare lamenting your latency:


![april_fools_ai_clickstack_3.png](/uploads/april_fools_ai_clickstack_3_01357825e5.png)
Hit **Regenerate** to get a new version. The theme adapts to context \-\- errors get Detective Noir, performance issues get Shakespearean Drama, and normal info events get the Nature Documentary treatment.


## It knows your stack [\#](/blog/clickstack-read-logs-detective-novel#it-knows-your-stack)


The summaries aren't random mad\-libs. AI Summarize understands the OpenTelemetry and Kubernetes attributes already present in your telemetry \-\- service names, versions, HTTP endpoints, database systems, RPC calls, exceptions, pod names, namespaces, durations, and more. It reads what's there and weaves it into the narrative.


A 1ms Redis call gets *"extraordinarily swift \-\- the peregrine falcon of API calls, diving at breathtaking speed."* A checkout span that errors out with a cache exception gets *"Then I found the body \-\- the kind of exception that ends careers and starts postmortems."* A 5\-second database query gets *"an age! Methinks the user doth grow weary, staring at the spinning wheel of fortune."*


The mood adapts too. Errors and exceptions trigger darker themes. Warnings get suspicious. Healthy spans get the nature documentary they deserve.


For **log patterns**, the summary incorporates the repeat count \-\- because a message that appears 113,526 times deserves to be called out:


*"Hark! A refrain most persistent: 'EmptyCartAsync called with \<*\>'. 113,526 times it echoes through the cluster, like a chorus that hath forgotten how to stop."\*


## Zero tokens. Zero data sharing. Zero cost. [\#](/blog/clickstack-read-logs-detective-novel#zero-tokens-zero-data-sharing-zero-cost)


Here's the part we're most proud of: **AI Summarize doesn't use any LLM.** There is no API call to OpenAI, Anthropic, or any other provider. No tokens are consumed. Your data never leaves the browser.


The summaries are generated entirely on the client side using hand\-written phrase pools and OTel\-aware data extraction. The "AI" in "AI Summarize" stands for "Artisanally Improvised."


This means:


- **No cost** \-\- works on every HyperDX deployment, open source or cloud, with no AI API key required
- **No privacy concerns** \-\- event data stays in your browser tab, never sent to a third\-party model
- **No latency** \-\- the \~2 second "analysis" delay is theatrical, not computational
- **No hallucinations** \-\- every fact in the summary comes directly from your event attributes


Click the `(i)` icon next to any summary to see the disclosure. If the feature isn't for you, the same popover has a "Don't show again" link that persists via localStorage.


## Try it [\#](/blog/clickstack-read-logs-detective-novel#try-it)


**AI Summarize** is going live today in HyperDX. Open any log, trace, or pattern and look for the sparkle icon.


After the first week the button is hidden by default to keep the UI clean, but you can bring it back anytime by adding `?smart=true` to your HyperDX URL. It stays active through the end of April 2026\.


We're also evaluating a version that uses actual AI on the backend \-\- the infrastructure is already in place. If you'd like to see real LLM\-powered summaries as a permanent feature, let us know on [GitHub](https://github.com/hyperdxio/hyperdx) in [Slack](https://clickhousedb.slack.com/archives/C09GJFL66FK).


Happy April Fools! The joke is the delivery, not the feature. Every fact in the summary comes from your real OTel attributes. Every Kubernetes pod name is accurate. We just thought your 3am pages deserved better writing.


*"We are such stuff as spans are made on, and our little traces are rounded with a timeout."*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
