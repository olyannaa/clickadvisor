---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Instrumenting
topic: instrumenting-your-nextjs-application-with-opentelemetry-and-clickstack-clickhouse
ch_version_introduced: '0.9'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 13
---

with authentication handled automatically. ![cloud_clickstack.gif](/_next/image?url=%2Fuploads%2Fcloud_clickstack_a22ee815a1.gif&w=2048&q=75) At the time of writing, an ingestion endpoint is not provided in Cloud, so users will need to run an OTel collector locally to handle ingestion. The following commands should get you started:

```
1curl -O https://raw.githubusercontent.com/ClickHouse/clickhouse-docs/refs/heads/main/docs/use-cases/observability/clickstack/deployment/_snippets/otel-cloud-config.yaml
2
3# modify to your cloud endpoint
4export CLICKHOUSE_ENDPOINT=
5export CLICKHOUSE_PASSWORD=
6# optionally modify 
7export CLICKHOUSE_DATABASE=default
8
9# osx
10docker run --rm -it \
11  -p 4317:4317 -p 4318:4318 \
12  -e CLICKHOUSE_ENDPOINT=${CLICKHOUSE_ENDPOINT} \
13  -e CLICKHOUSE_USER=default \
14  -e CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD} \
15  -e CLICKHOUSE_DATABASE=${CLICKHOUSE_DATABASE} \
16  --user 0:0 \
17  -v "$(pwd)/otel-cloud-config.yaml":/etc/otel/config.yaml \
18  -v /var/log:/var/log:ro \
19  -v /private/var/log:/private/var/log:ro \
20  otel/opentelemetry-collector-contrib:latest \
21  --config /etc/otel/config.yaml
```
Copy command
Once the collector is deployed, return to the HyperDX UI to create a trace and session source.

![clickstack-sources.gif](/_next/image?url=%2Fuploads%2Fclickstack_sources_8ffbedf7f1.gif&w=2048&q=75)

### Instrumenting the browser \#

Our [Next.js](https://clickhouse.com/docs/clickstack/ingesting-data/sdks/nextjs) application has both client and server\-side components. For the client side, we’ll use the ClickStack Browser SDK. While you could use the vanilla OpenTelemetry SDK (fully compatible with ClickStack), the ClickStack JavaScript SDK brings one big advantage: session replay, alongside built\-in features like console and network capture of HTTP requests, which can be enabled with a simple flag.

Instrumentation only takes a few lines of code. First, install the package:

```
1npm install @hyperdx/browser
```
Copy command
Next, we need to initialize the SDK in a place that’s guaranteed to load when your app starts. In our case, ClickPy shows a cookie consent banner before anything else \- [added in layout.js](https://github.com/ClickHouse/clickpy/blob/main/src/app/layout.js). This is a perfect place to add the initialization:

```
1import HyperDX from '@hyperdx/browser';
2
3HyperDX.init({
4 url: process.env.NEXT_PUBLIC_OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318',
5 apiKey: process.env.NEXT_PUBLIC_HYPERDX_API_KEY || '',
6 service: 'clickpy-frontend',
7 tracePropagationTargets: [
8   /localhost:\d+/i,
9   new RegExp(process.env.NEXT_PUBLIC_DOMAIN || 'localhost', 'i')
10 ],
11 consoleCapture: true,
12 advancedNetworkCapture: true,
13});
```
Copy command
A couple of things to notice here:
