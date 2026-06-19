# ClickHouse welcomes Metabase Cloud GA integration


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse welcomes Metabase Cloud GA integration

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 15, 2023 · 4 minutes read
  

At ClickHouse, we passionately believe supporting our open\-source ecosystem is fundamental to adoption and ensuring our users are successful. As part of this, it's always a pleasure to work with other companies whose complementary technologies are also grounded in open source. Today we are pleased to announce the availability of the ClickHouse plugin in Metabase Cloud!
In this blog post, we explore the history of the plugin and its journey to becoming available in Metabase Cloud and our plans for the future.


To learn more about Metabase and the ClickHouse plugin, join our [joint webinar on the 7th of March](/company/events/2023-03-07-metabase-clickhouse-webinar) as we build visualizations on multi\-TB datasets with a few clicks! As a teaser, we've recorded a simple introduction to go with today's announcement.


## What is Metabase? [\#](/blog/metabase-clickhouse-plugin-ga-release#what-is-metabase)


Users new to ClickHouse have several visualization options, and your choice will often depend on your existing tooling and requirements. However, we increasingly see users gravitating to Metabase due to its simplicity and ability to allow users to construct beautiful visualizations without needing to worry about writing SQL.


Queries can be constructed by simply dragging and dropping fields \- a feature likely to appeal to business users. Focusing on fast data exploration, the breadth of visuals and customizability is constantly expanding, with users enthusiastic about the clean and simple interface and workflow.


## A little bit of history [\#](/blog/metabase-clickhouse-plugin-ga-release#a-little-bit-of-history)


Many of [our community integrations](https://clickhouse.com/blog/clickhouse-dbt-project-introduction-and-webinar) experience a similar journey, starting off as a community project for one user and growing in adoption before becoming an official project sponsored by ClickHouse. The [ClickHouse plugin for Metabase](https://github.com/ClickHouse/metabase-clickhouse-driver) is another great example of this, and largely thanks to the work of [Felix Mueller](https://github.com/enqueue) and the [early work of other contributors](https://github.com/metabase/metabase/pull/8722), it is another example of community success. In November last year, the repository was transferred to ClickHouse. As well as addressing a [few compatibility issues](https://github.com/ClickHouse/metabase-clickhouse-driver/pull/107), we [improved tests](https://github.com/ClickHouse/metabase-clickhouse-driver/pull/112), [upgraded the underlying JDBC driver](https://github.com/ClickHouse/metabase-clickhouse-driver/issues/90), [improved CI](https://github.com/ClickHouse/metabase-clickhouse-driver/pull/106), and allowed [advanced connection settings](https://github.com/ClickHouse/metabase-clickhouse-driver/pull/109) such as [SSH tunnels](https://github.com/ClickHouse/metabase-clickhouse-driver/pull/116).


Confident the integration was mature with wide adoption, we approached Metabase to expose this plugin within their Cloud offering with the hope this would ensure the widest possible adoption.


## Collaboration [\#](/blog/metabase-clickhouse-plugin-ga-release#collaboration)


The release of any plugin in Metabase Cloud requires an extensive code review process. In late January, we began the process of making our plugin available in Metabase Cloud. Thanks to the historical efforts of the community and recent improvements, the required changes were minimal. Impressively, Metabase provided feedback within a few days, and the plugin was released today in Metabase Cloud.


## Future Plans [\#](/blog/metabase-clickhouse-plugin-ga-release#future-plans)


At this point, we consider the plugin stable and ready for production deployment. We have a few minor issues we’d like to address in the coming weeks \- specifically [improving table listings](https://github.com/ClickHouse/metabase-clickhouse-driver/issues/137) and making SSL certificate configuration [more user\-friendly](https://github.com/ClickHouse/metabase-clickhouse-driver/issues/136). However, we’re always open to community feedback and would welcome ideas from the community.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
