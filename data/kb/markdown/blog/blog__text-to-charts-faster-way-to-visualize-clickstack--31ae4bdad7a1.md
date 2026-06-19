# From text to charts: a faster way to visualize with ClickStack


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# From text to charts: a faster way to visualize with ClickStack

![](/_next/image?url=%2Fuploads%2Fclickhouse_b3f07400ef.png&w=96&q=75)ClickStack TeamOct 22, 2025 · 4 minutes read![clickstack-text-to-chart.png](/uploads/clickstack_text_to_chart_1ec8213e10.png)
ClickStack's new text\-to\-chart feature makes analyzing observability data simpler than ever. Whether you're working with logs or traces, ClickStack lets you create charts just by describing them. No menus, no dropdowns \- just type what you want to see and get instant visualizations that accelerate your path to root cause analysis.


Over the last year, large language models have started finding their way into observability tools, helping users move faster and spend less time on repetitive work. With ClickStack, we're now bringing that same convenience to data visualization.


[ClickStack](https://clickhouse.com/docs/use-cases/observability/clickstack/overview) is a high\-performance observability stack that aims to democratize access to ClickStack for everyone. It brings the power, speed, and flexibility of ClickHouse to logs, metrics, and traces \- all in an open\-source package that anyone can use. This new feature continues that mission by making ClickStack even easier to use.


![simple_text_to_chart.gif](/uploads/simple_text_to_chart_49ec63e8ed.gif)
## Describe your chart, and we'll build it [\#](/blog/text-to-charts-faster-way-to-visualize-clickstack#describe-your-chart-and-well-build-it)


Want to see error rates by service over the last 24 hours? Just type it out. Need a latency breakdown by endpoint? Describe it, and the chart appears.


ClickStack takes your text prompt, converts this to a query using an LLM, and automatically builds the corresponding visualization. It's fast, intuitive, and designed to get you from idea to insight in seconds.


This kind of natural\-language chart generation first emerged in business intelligence tools, but it's now proving just as useful in observability. When you're exploring logs, traces, or metrics, being able to instantly visualize patterns can make it much easier to spot anomalies and understand what's really happening in your systems.


### Get started with ClickStack
 [\#](/blog/text-to-charts-faster-way-to-visualize-clickstack#test)

Ready to explore the world's fastest and most scalable open source observability stack? Start locally in seconds.

[Start exploring](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started?loc=blog-o11y-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
## Trying it out [\#](/blog/text-to-charts-faster-way-to-visualize-clickstack#trying-it-out)


Enabling the text\-to\-chart just requires an Anthropic API key. Set the environment variable `ANTHROPIC_API_KEY`, and ClickStack will enable the feature.


The quickest way to get started and experiment with the feature, is with our [local\-only Docker image](https://clickhouse.com/docs/use-cases/observability/clickstack/deployment/hyperdx-only) specifying the key via the `-e` flag.



```
docker run -p 8080:8080 docker.hyperdx.io/hyperdx/hyperdx-local -e ANTHROPIC_API_KEY='<YOUR KEY>'

```

Note that this Docker image is intended for quick experimentation, not production use. Authentication is disabled in the local image, which makes it perfect for testing new features but unsuitable for live environments.


For feature testing, connect to our [public demo environment](https://play-clickstack.clickhouse.com/). Launch HyperDX locally at localhost, click `Connect to Demo Server` and you'll automatically have access to a live stream of logs, traces, and metrics for our OTel demo environment.


![hyperdx_demo.png](/uploads/hyperdx_demo_f562ea040d.png)
Once you're connected, head over to the **Chart Explorer**. At the top, you'll find the **AI Assistant** ready to help you describe and generate charts instantly. Just select a data source and try a few prompts, and see how fast you can go from text to visualization.


In the example below, we generate charts for the logs and traces based only on some simple text prompts.


![text_to_chart.gif](/uploads/text_to_chart_6b73d46e08.gif)
## What's next [\#](/blog/text-to-charts-faster-way-to-visualize-clickstack#whats-next)


Currently, the feature relies on users having an Anthropic account. Future iterations of the feature will support other LLM providers, including OpenAI.


This is also one of several AI\-based features we're building to make ClickStack more intuitive and productive. We're just getting started, and there's plenty more to come that will make exploring your observability data even faster and more powerful.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
