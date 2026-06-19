# I've created a website to track the team's activity


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# I've created a website to track the team's activity

![alexey-milovidov.webp](/_next/image?url=%2Fuploads%2Falexey_milovidov_0b4e074704.webp&w=96&q=75)[Alexey Milovidov](/authors/alexey-milovidov)Nov 10, 2025 · 6 minutes readInitially, I wanted to make a single report to incentivise our managers for looking at and resolving GitHub issues. But I'm greedy, so in the end it appeared to be a website where you can compare various metrics on team activities across GitHub repositories. Check it [here](https://velocity.clickhouse.com/).


[![screenshot2.png](/uploads/screenshot2_a81b9da275.png)](https://velocity.clickhouse.com/)


## This is wrong [\#](/blog/velocity#this-is-wrong)


Developer productivity metrics are a problematic topic. I hope no one compares committed [lines of code](https://www.folklore.org/Negative_2000_Lines_Of_Code.html) today. However, if you track something like the number of commits and pull requests, you make the same mistake. Neither commits nor pull requests are the primary activities of the company, and neither the number of such items provides reliable information about the amount of work by particular individuals.


It could be nice to check the metrics out of curiosity, to find general trends on a large scale, but the metrics should not be a primary target for optimization. They could only be used as a secondary signal.


[![velocity2.png](/uploads/velocity2_ddda0afb69.png)](https://velocity.clickhouse.com/#org=ClickHouse&metric=all_activity&range=all&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=godotengine)


## It makes sense anyway [\#](/blog/velocity#it-makes-sense-anyway)


The metrics of your own team are always wrong! So I added the possibility to calculate and compare any repositories and organizations on GitHub.


Examples:


[Rust vs. Zig](https://velocity.clickhouse.com/#org=rust-lang&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=ziglang&deleted=jcs090218%2Clivetdsa%2Cormabr%2CSuperAuguste%2Ctheballtv%2CJJJEJEJEJEJE%2Cgreensm0ke%2Cshizfs%2Capuarwa%2Ctadirnaksam) \| [Polars vs. Datafusion](https://velocity.clickhouse.com/#org=pola-rs&metric=all_activity&range=12&grouping=auto&a%5B%E2%80%A6%5Dyone=0&compare=1&compareOrg=apache%2Fdatafusion*%2C+apache%2Farrow-datafusion*) \| [Superset vs. Metabase](https://velocity.clickhouse.com/#org=apache%2Fsuperset%2C+apache%2Fincubator-superset%2C+airbnb%2Fsuperset&metric=all_activity&range=all&grouping=quarter&alexey=0&everyone=0&compare=1&compareOrg=metabase&deleted=github-automation-metabase) \| [Node vs. Deno](https://velocity.clickhouse.com/#org=nodejs%2C+joyent%2Fnode&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=denoland) \| [Node vs. Bun](https://velocity.clickhouse.com/#org=nodejs%2C+joyent%2Fnode&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=oven-sh) \| [SurrealDB vs ArangoDB](https://velocity.clickhouse.com/#org=surrealdb&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=arangodb) \| [Elasticsearch vs Opensearch](https://velocity.clickhouse.com/#org=elastic%2C+elasticsearch&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=opensearch-project%2C+opendistro-for-elasticsearch&deleted=github-automation-metabase%2Celasticmachine%2Ckibanamachine%2Ckibana-ci%2Celasticsearchmachine%2Capmmachine%2Cprodsecmachine) \| [Redis vs. Valkey](https://velocity.clickhouse.com/#org=valkey-io&metric=all_activity&range=6&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=antirez%2Fredis%2C+redis%2C+RedisLabs) \| [Tensorflow vs. PyTorch](https://velocity.clickhouse.com/#org=tensorflow&metric=all_activity&range=all&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=pytorch&deleted=pytorchmergebot%2Ctensorflowbutler%2Ctensorflow-jenkins) \| [QDrant vs. Weaviate](https://velocity.clickhouse.com/#org=qdrant&metric=all_activity&range=all&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=weaviate%2C+semi-technologies%2Fweaviate&deleted=pytorchmergebot%2Ctensorflowbutler%2Ctensorflow-jenkins) \| [Supabase vs. Neon](https://velocity.clickhouse.com/#org=supabase&metric=all_activity&range=all&grouping=auto&alexey=0&everyone=0&compare=1&compareOrg=neondatabase)


We can see when particular people started and stopped contributing to the project, what the distribution of the community size is, and what the general trends are in a specific repository's activity. The popularity of a project can be estimated by the number of GitHub issues (meaning, feature requests, bug reports, and questions).


Keep in mind that direct comparison is not always possible and can be misleading. For example, [Spark](https://velocity.clickhouse.com/#org=apache%2Fspark*%2C+apache%2Fincubator-spark&metric=all_activity&range=all&grouping=quarter&alexey=0&everyone=0&deleted=github-automation-metabase) and [MongoDB](https://velocity.clickhouse.com/#org=mongodb%2C+10gen%2C+10gen-labs&metric=all_activity&range=all&grouping=quarter&alexey=0&everyone=0&deleted=github-automation-metabase) don't use GitHub issues, forcing their users to register in Jira. [Linux kernel](https://kernel.org/) uses neither issues nor pull requests. [LLVM](https://velocity.clickhouse.com/#org=llvm&metric=all_activity&range=12&grouping=auto&alexey=0&everyone=0&deleted=llvmbot%2Cllvm-ci) has recently migrated from Phabricator and Bugzilla to GitHub pull requests and issues, which made it way more accessible, while [GCC](https://gcc.gnu.org/) is only available on GitHub as a mirror. [Chromium](https://chromium.googlesource.com/chromium/src.git) also does not use issues or pull requests. For established open\-source products, it's more an exception than the rule to use GitHub for issue tracking.


## Implementation [\#](/blog/velocity#implementation)


The website is implemented as a single\-page HTML application, connecting directly to the ClickHouse database. It runs SQL queries from a read\-only user, configured with limits and quotas. The database design and data collection are described in [this article from 2020](https://ghe.clickhouse.tech/).


It has a few neat details in the UX.


In the repository selector, you can type organizations (like `ClickHouse`), single repositories (like `ClickHouse/ClickHouse`), or use wildcards (like `apache/superset*`), as well as list multiple items. It will show suggestions by substring search across all GitHub repositories, sorted by the number of stars.


For the charts, we use the ["horizon chart"](https://en.wikipedia.org/wiki/Horizon_chart) type, which allows a high information density in a narrow space. We also highlight activity on different repositories with different colors, so you can see, for example, when I was contributing to ClickHouse and when I was contributing to [ClickBench](https://benchmark.clickhouse.com/).


In the list of authors, you can click on anyone to see the list of all activities in the ClickHouse SQL UI, and if you click on a single data point on the chart, you can dig into the events for the corresponding time. You can also remove any author from the report to clean it of automations or spam activity.


The source code is available [here](https://github.com/ClickHouse/velocity).


[![implementation.png](/uploads/implementation_267d5599be.png)](https://github.com/ClickHouse/velocity/commits/master/)


## Results [\#](/blog/velocity#results)


It took only half of a weekend to implement this website, and I'm still impressed by how easy it was. Building analytical applications, data exploration tools, and dashboards \- **it's such a joy with ClickHouse!** No other database comes even close in usability.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
