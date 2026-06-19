# Optimizing your customer\-facing analytics experience with Luzmo and ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Optimizing your customer\-facing analytics experience with Luzmo and ClickHouse

![](/_next/image?url=%2Fuploads%2Fluzmo_684f03b8a8.png&w=96&q=75)[Luzmo](/authors/luzmo)Jun 29, 2022 · 6 minutes read*We’d like to welcome Luzmo as a guest to our blog. Read on to find out how Luzmo is using ClickHouse to enable their users to build embedded, customer\-facing analytics.*


Your software application generates terabytes of data. And with that data, your users can make smart, confident decisions faster. But how do you transform all that product data into visual insights for your users?


In this article, we’ll discuss how to build empowering customer\-facing analytics in no time, with a well\-designed, modern data architecture using [Luzmo](https://www.luzmo.com) and ClickHouse as building blocks.


## The challenges of building customer\-facing analytics [\#](/blog/optimizing-your-customer-facing-analytics-experience-with-luzmo-and-clickhouse#the-challenges-of-building-customer-facing-analytics)


Delivering analytics in SaaS is a two\-fold challenge because you are balancing two work streams:


- User experience: you want to provide an easy\-to\-use, interactive and personalized experience for your end\-users
- Data architecture: you want to build a coherent and high\-performing data architecture with tailored visualizations fast and painlessly, without dedicating weeks of engineering time


Typically, the more advanced analytics you want to build, the harder it becomes for developers to maintain. And there’s the extra complexity of data security. Every user should only get access to their personal data, and not to the data of another user. How do you scale tailored insights to hundreds or even thousands of users?


[Embedded analytics tools](https://www.luzmo.com/blog/embedded-analytics-tools) offer the perfect sweet spot. They combine an easy\-to\-use UI for non\-technical users with a powerful and consistent API, accessible to developers. You can even bring your own authentication into dashboard filtering, keeping your user data strictly on your premises.
Below, you’ll learn how to build an embedded analytics setup using [Luzmo](https://www.luzmo.com) for visualizations, and ClickHouse as your data infrastructure.


## Building embedded analytics with Luzmo [\#](/blog/optimizing-your-customer-facing-analytics-experience-with-luzmo-and-clickhouse#building-embedded-analytics-with-luzmo)


What your users want is an engaging [customer analytics experience](https://www.luzmo.com/blog/customer-analytics-experience):


- Personalized reports and dashboards that show relevant insights in a flash
- Dashboards with interactive exploring: let users filter, drill down or receive alerts when they reach a certain a threshold
- Dashboards that look nice and load fast


With the [embedded analytics platform](https://www.luzmo.com/product/embedded-analytics) of Luzmo, you can inject all of the above functionality into your platform with one snippet of code. You won’t need to develop a single chart: non\-technical colleagues can completely manage the creation of dashboards using Luzmo’s drag\-and\-drop UI.


![Luzmo_1.png](/uploads/Luzmo_1_8b48882836.png)
As a developer, you’ll be more interested in Luzmo’s powerful API. By using the [embedding libraries](https://developer.luzmo.com/#embedding), you can plug Luzmo’s analytics straight into your platform, while re\-using any authentication or business logic you’ve already built inside your software. This will considerably speed up your development cycle, while retaining full control over your analytics feature set.
To get up and running, all you need to do is create a dashboard in Luzmo, make a server\-side request to our API to generate an authorization token (or SSO token), and embed the code snippet below into your application. [This article](https://css-tricks.com/embedded-analytics-made-simple-with-cumul-io-integrations) will take you through a step\-by\-step guide!



```
<luzmo-dashboard
  appServer="< Luzmo App server, defaults to https://app.luzmo.com >"
  apiHost="< Luzmo API server, defaults to https://api.luzmo.com >"
  authKey="< SSO authorization key >"
  authToken="< SSO authorization token >"
  dashboardId="< dashboard id you want to embed >"
  dashboardSlug="< instead of dashboardId: a dashboard slug as specified in the Integration. >"
></luzmo-dashboard>

```

Below is a basic diagram of how the embedding process works:


![Luzmo2.png](/uploads/Luzmo2_26704ae8af.png)
As a developer, you can [use the SSO token](https://academy.luzmo.com/course/bf528f25-2e7b-4544-8255-e08da35a0eb6) to set as many additional rules as you want for every user or user group. For example, customize the styling of your dashboards, show different statistics depending on the user role, adapt the language or timezone, etc. All with just a few lines of additional code.


## Using ClickHouse as a data infrastructure for embedded analytics [\#](/blog/optimizing-your-customer-facing-analytics-experience-with-luzmo-and-clickhouse#using-clickhouse-as-a-data-infrastructure-for-embedded-analytics)


Any embedded analytics solution will only provide a good experience if the data model behind it is performant.


Like many companies, maybe you are already using a relational database for your operations. The problem with relational databases is that they aren’t optimal for analytical queries. As a result, dashboards may load more slowly, causing frustration for your end\-users.


Is your data model complex, with a lot of joins or aggregations? A columnar database is designed with aggregations in mind, rather than row\-level queries. For this use case, ClickHouse provides a high\-performance and scalable database solution for customer\-facing, ad\-hoc aggregations and analytics.


[TEIMAS](https://teimas.com/en/), a software company building solutions for waste management, has been using Luzmo for its customer\-facing analytics for over 3 years. Their platform’s backend runs on MySQL, but the more data they were dealing with, the more they felt the need for a separate analytical database like ClickHouse.
“We needed to connect directly to an analytical database,” said Iago Elizechea, CTO at Teimas. “Not only to improve the speed of our dashboards, but also to ensure the performance of the entire platform.”


Elizechea started using ClickHouse in their setup because of its accessibility. Because it’s open\-source, they can easily deploy it into their own infrastructure. When the setup is well\-designed, Elizechea claims ClickHouse has amazing performance: “For some types of queries, ClickHouse can be up to 100x faster than MySQL. Even when there’s a huge amount of data, I get the results immediately.”


## Getting started with ClickHouse and Luzmo [\#](/blog/optimizing-your-customer-facing-analytics-experience-with-luzmo-and-clickhouse#getting-started-with-clickhouse-and-luzmo)


With Luzmo’s easy\-to\-deploy visualization and ClickHouse’s laser\-fast performance, you can provide a seamless analytics experience to your customers without the stress of clunky deployment.


If you’d like to explore further, below are a few resources:


- [Luzmo free trial](https://app.luzmo.com/signup)
- [How to connect ClickHouse in Luzmo](https://academy.luzmo.com/article/ovvkqfo5)
- [Developer documentation on embedding](https://developer.luzmo.com/#embedding)
- [How to use Luzmo’s drag and drop editor](https://academy.luzmo.com/course/a0bf5530-edfb-441e-901b-e1fcb95dfac7)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
