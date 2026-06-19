# ClickStack APIs arrive in the ClickHouse Cloud OpenAPI


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickStack APIs arrive in the ClickHouse Cloud OpenAPI

![](/_next/image?url=%2Fuploads%2FImage_512x512_7_0bce552efb.jpeg&w=96&q=75)Alex FedotyevMar 4, 2026 · 6 minutes read
div.w\-full \+ p,
span.relative \+ p {
 text\-align: center;
 font\-style: italic;
}

As teams scale their observability with ClickStack across more services and environments, keeping configuration consistent becomes its own challenge. A dashboard built for one service needs to be replicated for the next. Alerts configured in development need to be recreated in staging and production. The more environments you operate, the more manual work is involved. And with it, the risk of drift, missed alerts, and inconsistency.


With ClickStack resources now in the ClickHouse Cloud API, observability configuration can live in your deployment pipelines, version control, and infrastructure\-as\-code workflows. Dashboards follow a service from dev through staging to production. Alerts ship alongside the applications they monitor. Configuration is reviewed in pull requests and deployed through CI/CD.


Together with capabilities like role\-based access control on the roadmap, this lays the foundation for production\-grade observability workflows with the same controls teams already apply to application code.


[Explore the full API reference](https://clickhouse.com/docs/cloud/manage/api/swagger#tag/ClickStack)


## **Getting started** [\#](/blog/clickstack-api#getting_started)


Getting started takes minutes if you already have a Managed ClickStack service and a ClickHouse Cloud API key.


**Prerequisites:** a ClickHouse Cloud organization with a Managed ClickStack service, and an API key with Service Admin or Org Admin permissions.


The full endpoint reference — including request and response schemas for all supported resources — is available in the [ClickStack API documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/api-reference). The OpenAPI spec can also be [downloaded directly](https://api.clickhouse.cloud/v1) for SDK generation or to import into tools like [Postman](https://www.postman.com/) for interactive exploration.


## **What you can do now** [\#](/blog/clickstack-api#what_you_can_do_now)


The API covers the core resources teams need to manage ClickStack programmatically:


**Dashboards** can be created, read, updated, and deleted through the API, including chart configurations and dashboard\-level filters. Dashboards built through the API render identically in the ClickStack UI, with the same layout and behavior you would get by building them interactively.


**Alerts** can be defined as rules tied to dashboard tiles or saved searches with webhook delivery.


**Sources** and **Webhooks** round out the supported resources — list your configured data sources and webhook destinations to retrieve the IDs that dashboard and alert configurations require, without manual lookups.


This release enables the first wave of the config\-as\-code improvements. We are continuing to expand coverage — a Terraform provider for ClickStack is actively in development, and additional resource types are on the way.


## **How it works** [\#](/blog/clickstack-api#how_it_works)


ClickStack endpoints live under the same base path as the rest of the ClickHouse Cloud API:



```
https://api.clickhouse.cloud/v1/organizations/{organizationId}/services/{serviceId}/clickstack/...

```

**If you are already using ClickHouse Cloud API keys, you can start making ClickStack API calls immediately — no separate credentials or token exchange required.** The only requirement is that the API key has Org Admin or Service Admin permissions. API keys scoped to particular services will have access to the ClickStack teams corresponding to those services, while Org Admin keys have access to all services.


A dedicated "Manage ClickStack API" permission is assigned by default to Org Admin and Service Admin roles, with finer\-grained access control planned for a future release.


We also invested in making the API spec clean and predictable for tooling consumers. Inline schemas have been replaced with named types, number fields use `integer` rather than `number`, and validation errors return structured details rather than opaque 400 responses. These choices matter when generating SDKs, writing Terraform providers, or integrating with CI/CD tooling that consumes the OpenAPI spec directly.


## **Examples** [\#](/blog/clickstack-api#examples)


Here are a few common examples to illustrate how the API works in practice.


**List all dashboards for a ClickStack service:**



```

```
1curl -X GET \
2  'https://api.clickhouse.cloud/v1/organizations/{organizationId}/services/{serviceId}/clickstack/dashboards' \
3  --user '<keyId>:<keySecret>' \
4  -H 'Content-Type: application/json'
```

```

**Create a dashboard with a request volume time series chart filtered by service name:**



```

```
1curl -X POST \
2  'https://api.clickhouse.cloud/v1/organizations/{organizationId}/services/{serviceId}/clickstack/dashboards' \
3  --user '<keyId>:<keySecret>' \
4  -H 'Content-Type: application/json' \
5  -d '{
6    "name": "API Monitoring Dashboard",
7    "tiles": [
8      {
9        "x": 0,
10        "y": 0,
11        "w": 24,
12        "h": 12,
13        "name": "Request Volume",
14        "config": {
15          "displayType": "line",
16          "sourceId": "<sourceId>",
17          "asRatio": false,
18          "alignDateRangeToGranularity": true,
19          "fillNulls": true,
20          "select": [
21            {
22              "valueExpression": "",
23              "aggFn": "count",
24              "where": "ServiceName:\"api\"",
25              "whereLanguage": "lucene"
26            }
27          ]
28        }
29      }
30    ],
31    "tags": ["monitoring"]
32  }'
```

```

**Create an alert on a dashboard chart with webhook notification to Slack:**



```

```
1curl -X POST \
2  'https://api.clickhouse.cloud/v1/organizations/{organizationId}/services/{serviceId}/clickstack/alerts' \
3  --user '<keyId>:<keySecret>' \
4  -H 'Content-Type: application/json' \
5  -d '{
6        "name": "Alert SREs when request rate is high",
7        "message": "API request rate exceeded expected volume",
8        "threshold": 1000,
9        "interval": "1m",
10        "thresholdType": "above",
11        "source": "tile",
12        "channel": {
13        	"type": "webhook",
14        	"webhookId": "<webhookId>",
15        	"webhookService": "slack_api",
16        	"slackChannelId": "#prod-api-alerts"
17        	},
18        "tileId": "<tileId>",
19        "dashboardId": "<dashboardId>"
20}'
```

```

The response includes the created resource with its assigned `id`, which you can then use for updates. Validation errors return structured details so issues surface immediately rather than silently producing misconfigured resources.


**Tip:** The OpenAPI spec is available for [download](https://api.clickhouse.cloud/v1) and works with the tooling you already use. Import it into [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) to generate a ready\-to\-use collection, open it in the [Swagger Editor](https://editor.swagger.io/) to explore endpoints in your browser, or use it with VS Code extensions like [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or [Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client) for a lightweight workflow without leaving your editor.


## **What comes next** [\#](/blog/clickstack-api#what_comes_next)


The ClickStack API is the first of several capabilities focused on making ClickStack easier to integrate and operate at scale. A Terraform provider is in active development, finer\-grained access control is on the roadmap, and we plan to expand the API surface with additional resources as the offering matures.


We would love to hear what resources and workflows matter most to your team. Join the ClickHouse Slack and hop into the [\#olly\-clickstack channel](https://clickhouse.com/slack) to share feedback, ask questions, or help shape what comes next.

### Get started today with ClickStack

Interested in seeing how ClickStack works for your observability data? Get started in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-91-get-started-today-with-clickstack-sign-up&utm_blogctaid=91)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
