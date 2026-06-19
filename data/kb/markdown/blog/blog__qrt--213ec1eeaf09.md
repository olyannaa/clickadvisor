# How QRT powers real\-time research and risk management at petabyte scale


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How QRT powers real\-time research and risk management at petabyte scale

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 9, 2026 · 2 minutes read## Summary

- QRT, a global investment manager, uses ClickHouse Cloud to power a data platform serving researchers, as well as a real\-time risk and P\&L system.
- Beyond supporting researchers, ClickStack is also the foundation for QRT's observability infrastructure.
Quantitative trading is, at its core, a data challenge. Funds seek to store more of it, query it faster, and act on it first.


[Qube Research \& Technologies (QRT)](https://www.qube-rt.com/) is a global quantitative investment manager headquartered in London. The firm's decision to use [ClickHouse Cloud](https://clickhouse.com/cloud) reflects a philosophy that dates back to the firm's origins. Most hedge funds founded in the 1990s and 2000s run on\-premise data centers built up over decades. But QRT, launched in 2018 amid a rapid spinout of Credit Suisse's proprietary trading arm, was originally built in the cloud. Rather than inheriting legacy on\-premise infrastructure, it built itself cloud\-native from day one.


## Built for the cloud, ready to scale [\#](/blog/qrt#built-for-the-cloud-ready-to-scale)


QRT uses [ClickHouse Cloud](https://clickhouse.com/cloud) across two of their major systems. One centralized platform that gives researchers across the firm access to the data they need to develop trading strategies, and another near real\-time risk monitoring, management, and P\&L system.


"We wanted something faster and much more scalable," says a senior engineer on the team. "With our previous database, we were limited by the number of writers, the number of readers, and the total load per cluster. With ClickHouse, we don't have those limitations."


Beyond supporting researchers, ClickHouse is also the foundation for QRT's observability infrastructure. The migration to [ClickStack](https://clickhouse.com/clickstack), ClickHouse's integrated observability stack, consolidated logs, metrics, and traces onto a single backend for the first time. Alerts, log queries, and metric aggregations that used to require managing multiple systems now run against a single ClickHouse instance using standard SQL. "Having all our monitoring on one backend gives us the simplicity to maintain and is reliably fast," says the QRT engineer.

### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-828-get-started-today-sign-up&utm_blogctaid=828)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_appoints_apac_leader_f2c3722e9c.jpg&w=828&q=75)Company and culture### [ClickHouse appoints new leader for Asia Pacific and expands global go\-to\-market leadership team](/blog/clickhouse-appoints-apac-leader-and-expands-global-gtm-leadership)

ClickHouse · Jun 8, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
