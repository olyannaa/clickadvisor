# Announcing ClickGems: Free analytics for RubyGems


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing ClickGems: Free analytics for RubyGems

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2Frubycentral_2748b7b7b1.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Fmetabase_logo_icon_170959_b82fe563a7.png&w=96&q=75)The ClickHouse, Ruby Central and Metabase teamsOct 2, 2025 · 5 minutes readA few months ago, the Ruby Central team, inspired by our work on [ClickPy](https://clickpy.clickhouse.com/), asked if we could load public RubyGems download stats into a public ClickHouse instance. The goal was to make it easier for the open\-source community to analyze the data. [We were glad to help](https://clickhouse.com/blog/announcing-ruby-gem-analytics-powered-by-clickhouse), supporting open source projects has always been a priority for us, and we enjoy working with large, real\-world datasets that show what ClickHouse can do.


After bringing the dataset into our [SQL Playground](https://sql.clickhouse.com/?query_id=HVMKR3JXFT4DA8NMAPGXKM), we decided to go a step further and build a dedicated analytics site for the RubyGems community.


Today, we're introducing [ClickGems](https://clickgems.clickhouse.com/), a new platform that provides analytics for RubyGems. It lets you explore download statistics for more than 200,000 gems, covering data from 2017 to today and totaling over 200 billion downloads.


## What is ClickGems? [\#](/blog/announcing-clickgems#what-is-clickgems)


ClickGems is a website designed to empower Ruby developers with in\-depth analytics for their favorite Ruby gems.


![clickgems-1.png](/uploads/clickgems_1_7d1b56c822.png)
ClickGems follows the same purpose as ClickPy, so we decided to reuse the same code base. For now, development lives in a [dedicated branch](https://github.com/ClickHouse/clickpy/tree/clickgems) of the ClickPy GitHub repository, though we may fork it later if it makes sense.


If you've used ClickPy before, ClickGems will feel familiar. The design and features are the same. The landing page shows global statistics such as recent releases for popular gems and top repositories.


From there, you can click on any gem to open its detail page. Each gem page includes charts and metrics such as downloads over time or downloads by country.


![clickgems-2.png](/uploads/clickgems_2_0bf618d631.png)
## How we build visualizations [\#](/blog/announcing-clickgems#how-we-build-visualizations)


Each visualization is powered by a SQL query, which you can view by clicking the link icon in the top\-right corner. This opens the SQL Playground, where you can see the query and run it against the raw data. You can use this as a base to build your own visualizations.


To ensure fast execution, we use Materialized Views in ClickHouse to pre\-aggregate data as it's ingested. For more details on how we set up these Materialized Views to speed up queries for ClickGems, see our [previous blog post](https://clickhouse.com/blog/announcing-ruby-gem-analytics-powered-by-clickhouse#materialized-views) on bringing RubyGems data into ClickHouse.


![CleanShot 2025-10-02 at 21.16.22@2x.png](/uploads/Clean_Shot_2025_10_02_at_21_16_22_2x_fd970c0daa.png)
## New feature: Shareable charts [\#](/blog/announcing-clickgems#new-feature-shareable-charts)


While building ClickGems, we had the chance to work with [Metabase](https://www.metabase.com/), which offers the ability to host and embed charts anywhere. Thanks to their support, we were able to add this functionality to both ClickGems and ClickPy.


Now, from any gem or package page, you can export a chart and embed it directly into your website, documentation, blog post, or project page. This makes it easy to share usage trends and showcase the impact of your favorite libraries.


![clickgems-gif.gif](/uploads/clickgems_gif_03e56b5954.gif)
## How we power ClickGems  [\#](/blog/announcing-clickgems#how-we-power-clickgems)


ClickGems and ClickPy, along with other public demos like our SQL Playground and AgentHouse, are all powered by the same ClickHouse Cloud deployment.


This unified infrastructure allows us to manage large volumes of data and use cases while keeping the infrastructure and maintenance cost fairly low. ClickHouse ability to ingest large volumes while handling large numbers of parallel queries makes it possible.


We also decided to leverage [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud) within our ClickHouse Cloud in order to dedicate resources to ClickPy and ClickGems website. This architectural decision ensures that peak usage on one service, such as a surge in ClickGems queries, does not affect the performance or availability of other services like ClickPy or our other public demos. This guarantees a smooth and consistent experience for all our users across all our analytics platforms.


Below is a high\-level overview of the deployment.


![clickgems-diagram.jpg](/uploads/clickgems_diagram_c7822f23bd.jpg)
## Try ClickGems!  [\#](/blog/announcing-clickgems#try-clickgems)


This is exciting to see three organizations, ClickHouse, Ruby Central and Metabase come together to offer a fully fledged analytical application to the open\-source community!


We invite you to go today to [ClickGems](https://clickgems.clickhouse.com/) and see how your favorite gems are doing. We'd also love your feedback and contributions, feel free to open an [issue](https://github.com/ClickHouse/clickpy/issues) in the ClickPy GitHub repository if you have questions, suggestions, or ideas.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
