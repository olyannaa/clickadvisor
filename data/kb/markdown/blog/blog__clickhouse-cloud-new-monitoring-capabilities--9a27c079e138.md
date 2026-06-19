# More Visibility, Less Guesswork: ClickHouse Cloud's New Monitoring Capabilities


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# More Visibility, Less Guesswork: ClickHouse Cloud's New Monitoring Capabilities

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U02_HHFZ_0874_2cba508d09c4_512_e984252673.png&w=96&q=75)[Mihir Gokhale](/authors/mihir-gokhale)Mar 25, 2026 · 3 minutes readClickHouse gives users an incredible amount of control to optimize database performance. Platform administrators sit at the center of this experience: they tune scaling controls, configure server settings, and ultimately own the health of their deployment. On ClickHouse Cloud, we're releasing a set of improvements designed to give deeper visibility into how the ClickHouse server is behaving to proactively surface warnings before they become problems.


## More dashboards [\#](/blog/clickhouse-cloud-new-monitoring-capabilities#more-dashboards)


The ClickHouse Cloud console already comes built\-in with several monitoring dashboards. We added a few more.


### New overview page [\#](/blog/clickhouse-cloud-new-monitoring-capabilities#new-overview-page)


The new Overview page brings the most important signals about your deployment into a single, unified view. Designed to give administrators an at\-a\-glance health check of their ClickHouse environment, you can now spend less time hunting for information and more time acting on it.


### Infrastructure page: Deeper scaling visibility [\#](/blog/clickhouse-cloud-new-monitoring-capabilities#infrastructure-page-deeper-scaling-visibility)


The new Infrastructure page gives administrators a clearer view into how their services are scaling over time. CPU and Memory utilization metrics, now with additional aggregation types, show how much utilization your ClickHouse cluster is getting.


New modals showcase ClickHouse's [automatic scaling](https://clickhouse.com/docs/manage/scaling) behavior to help users better understand why and how their cluster scaled, and also make better decisions around custom scaling configurations like vertical scaling limits and idling behavior.


![](/uploads/clicklens_mar2026_image1_621e99285e.png)
## Get ahead of issues with new notifications [\#](/blog/clickhouse-cloud-new-monitoring-capabilities#get-ahead-of-issues-with-new-notifications)


When users onboard onto ClickHouse, a common set of issues frequently come up. Administrators will be automatically notified via email when a service is at risk of degraded performance or failures, including due to:


- **Too many parts**: a common cause of merge pressure and query slowdowns
- **Failed mutations**: which can silently stall data changes if left undetected
- **Query concurrency**: helping you catch saturation before high query concurrency impacts end users


### Slack notifications [\#](/blog/clickhouse-cloud-new-monitoring-capabilities#slack-notifications)


You can configure all these notifications, and more, to be sent directly to Slack via your organization's notification settings.


These improvements provide administrators with better visibility into ClickHouse behavior, so you can spend less time diagnosing issues and more time optimizing your performance.


These features are being rolled out now in ClickHouse Cloud. Log in to your console to explore the new dashboards and configure your notification preferences.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-271-get-started-today-sign-up&utm_blogctaid=271)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
