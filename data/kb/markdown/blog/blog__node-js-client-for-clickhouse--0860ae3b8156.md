# Node.js client for ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Node.js client for ClickHouse

![integrations.png](/_next/image?url=%2Fuploads%2Fintegrations_80a6d9dfe5.png&w=96&q=75)Serge Klochkov, Mikhail ShustovOct 20, 2022 · 4 minutes read![clickhouse-node.png](/uploads/clickhouse_node_578988e794.png)
## Introduction [\#](/blog/node-js-client-for-clickhouse#introduction)


Modern, data\-driven applications need a way to communicate with persistent data storage. Implementing this communication on the network layer is time\-consuming and requires understanding low\-level concepts such as connection management, data formatting and data marshalling. Language clients are a standard pattern to provide a language specific abstraction which hides the technical complexity of connecting to a datastore.


ClickHouse already provided official language clients in [Java](https://github.com/ClickHouse/clickhouse-jdbc), [Python](https://github.com/ClickHouse/clickhouse-connect), and [Go](https://github.com/ClickHouse/clickhouse-go). Today, we're happy to introduce an official, fully\-featured open\-source [Node.js client](https://github.com/ClickHouse/clickhouse-js) to join the family. The client was created to deliver blazing\-fast performance and ease of use of ClickHouse in the Node.js ecosystem. This language client joins our growing list of ClickHouse core [integrations](https://clickhouse.com/docs/en/integrations/) (maintained and supported by ClickHouse).


## Client features [\#](/blog/node-js-client-for-clickhouse#client-features)


- Written entirely in TypeScript with strong typing (including all ClickHouse server settings)
- Node.JS 14\.x, 16\.x, 18\.x runtimes
- HTTP(s) protocol with persistent connection
- HTTP request and response compression
- Node.js streaming API for both data insertion and selection
- Support for [a variety of data input and output formats](https://github.com/ClickHouse/clickhouse-js#supported-formats) \- JSON, CSV, TabSeparated, and CustomSeparated formats families
- Support for the [majority of the ClickHouse data types](https://github.com/ClickHouse/clickhouse-js#supported-clickhouse-data-types)
- Parametrized queries
- Request cancellation
- Custom logger support
- Extensive continuous testing with [ClickHouse Cloud](https://clickhouse.cloud/signUp) and [the latest actual ClickHouse versions](https://github.com/ClickHouse/clickhouse-js#compatibility)


Code samples for the most common usecases are available [in our repository examples folder.](https://github.com/ClickHouse/clickhouse-js/tree/main/examples) Additionally, we recommend reviewing the [integration tests folder](https://github.com/ClickHouse/clickhouse-js/tree/main/__tests__/integration) for further examples.


## Why we decided to write our client [\#](/blog/node-js-client-for-clickhouse#why-we-decided-to-write-our-client)


OSS enthusiasts are the key to creating a flourishing ecosystem. We see our primary goal as assisting the community in nurturing an open ecosystem around ClickHouse. As language clients are an integral part of the ClickHouse ecosystem, we decided to formalize a common specification for language client architecture and functionality. This provides recommendations for anyone creating a client in their favorite programming language and captures expected functionality with guidance on solving common problems. We aim to reduce the maintenance and developer onboarding costs though a standard specification which all clients can follow, contributing to a better developer experience.


A few months ago, we created a first draft of the language client specification and considered the Node.js client a good candidate to try out and validate the ideas described in the document. You can find a draft of the spec in this live [document.](https://docs.google.com/document/d/1924Dvy79KXIhfqKpi1EBVY3133pIdoMwgCQtZ-uhEKs/edit?usp=sharing) Feel free to share your thoughts there. We plan to adapt the spec to the customers' needs iteratively by getting feedback from the community. We welcome any ideas about what functionality the standard language client should provide, what the API should look like, what tooling is needed to simplify long\-term maintenance, etc. Gradually all clients will aim conform to this specification.


## Closing words and call for contribution [\#](/blog/node-js-client-for-clickhouse#closing-words-and-call-for-contribution)


We've just released [the very first versions of the client](https://www.npmjs.com/package/@clickhouse/client). We can't wait to hear how you use the client in your applications and get feedback about the features it provides, API ergonomics, performance, and possible improvements.


Have fun experimenting, and see you in our [repository.](https://github.com/ClickHouse/clickhouse-js) 


## Links [\#](/blog/node-js-client-for-clickhouse#links)


- GitHub repository: [https://github.com/ClickHouse/clickhouse\-js](https://github.com/ClickHouse/clickhouse-js)
- NPM registry: <https://www.npmjs.com/package/@clickhouse/client>


*If you’re enthusiastic about the latest technologies and are passionate about Open Source, we’re currently hiring for our [integrations team](https://clickhouse.com/company/careers) and would love to hear from you.*

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
