# ClickHouse v21\.10 Released


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse v21\.10 Released

Rich RaposaOct 14, 2021 · 3 minutes readWe're excited to share with you our first release since [announcing ClickHouse, Inc](https://clickhouse.com/blog/en/2021/clickhouse-inc/). The 21\.10 release includes new contributions from multiple contributors including many in our community, and we are grateful for your ongoing ideas, development, and support. Our Engineering team continues to be laser\-focused on providing our community and users with the fastest and most scalable OLAP DBMS available while implementing many new features. In the 21\.10 release, we have a wonderful 79 contributors with 1255 commits across 211 pull requests \- what an amazing community and we cherish your contributions.


Let's highlight some of these new exciting new capabilities in 21\.10:


- User\-defined functions (UDFs) can now be [created as lambda expressions](https://clickhouse.com/docs/en/sql-reference/functions/#higher-order-functions). For example, `CREATE FUNCTION plus_one as (a) -> a + 1`
- Two new table engines: Executable and ExecutablePool which allow you to stream the results of a query to a custom shell script
- Instead of logging every query (which can be a lot of logs!), you can now log a random sample of your queries. The number of queries logged is determined by defining a specified probability between 0\.0 (no queries logged) and 1\.0 (all queries logged) using the new `log_queries_probability` setting.
- Positional arguments are now available in your GROUP BY, ORDER BY and LIMIT BY clauses. For example, `SELECT foo, bar, baz FROM my_table ORDER BY 2,3` orders the results by whatever the bar and baz columns (no need to specify column names twice!)


We're also thrilled to announce some new free training available to you in our Learn ClickHouse portal: [https://clickhouse.com/learn/lessons/whatsnew\-clickhouse\-21\.10/](https://clickhouse.com/learn/lessons/whatsnew-clickhouse-21.10/)


We're always listening for new ideas, and we're happy to welcome new contributors to the ClickHouse project. Whether for submitting code or improving our documentation and examples, please get involved by sending us a pull request or submitting an issue. Our beginner developers contribution guide will help you get started: [https://clickhouse.com/docs/en/development/developer\-instruction/](https://clickhouse.com/docs/en/development/developer-instruction/)


## ClickHouse Release Notes [\#](/blog/click-house-v2110-released#clickhouse-release-notes)


Release 21\.10


Release Date: 2021\-10\-17


Release Notes: [21\.10](https://github.com/ClickHouse/ClickHouse/blob/master/CHANGELOG.md)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
