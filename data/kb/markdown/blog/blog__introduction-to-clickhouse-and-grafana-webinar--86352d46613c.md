# A Story of Open\-source GitHub Activity using ClickHouse \+ Grafana


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# A Story of Open\-source GitHub Activity using ClickHouse \+ Grafana

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 10, 2023 · 6 minutes read
 


We recently [delivered a webinar](https://www.youtube.com/watch?v=fXC6vzNc7g0) with our friends at Grafana, introducing the [official ClickHouse Grafana plugin](https://grafana.com/grafana/plugins/grafana-clickhouse-datasource/). During this webinar, we presented the plugin's history and the reasons behind the design choices and plans for the future.


Like any good webinar, however, we wanted to present a demo of the technology itself. Coincidentally, we were presenting that webinar exactly 10 years since the first Git commit to Grafana. Coupled with some recent frustration over limited GitHub analytics, we decided to present an analysis of the Grafana repository.


In this blog post, we review our findings and hopefully give our readers the tools to reproduce the same work on their projects.


## A source of frustration [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#a-source-of-frustration)


Whenever looking at a new GitHub project, as engineers, we often turn to GitHub analytics \- officially known as Pulse. At this point, our frustration typically begins, and we’re presented with some pretty underwhelming analytics.


![github_analytics_1.png](/uploads/github_analytics_1_c6ebb0cf85.png)
![github_analytics_2.png](/uploads/github_analytics_2_a148685719.png)
Given the importance of the date, with it being 10 years since the first commit, we decided to see if we could do better. What better tools to solve the task than the world’s leading OSS OLAP database and data visualization tool?!


## Finding the data [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#finding-the-data)


For any good analysis, we need good data. Fortunately for us, the data we need is either public or can be generated.


GitHub publishes the full event history of all public repositories through a wonderful project [GH Archive](https://www.gharchive.org/). This represents a fairly small dataset for ClickHouse, and we’ve already documented [thoroughly how to load and analyze this](https://ghe.clickhouse.tech/#how-this-dataset-is-created). With all pull requests, issues, stars, forks, watches \& comments for every repository on GitHub since the beginning of 2011, and over 5\.5 billion events, it provides an excellent “background” dataset for our analysis. Note that this dataset is also available in [play.clickhouse.com](https://sql.clickhouse.com?query_id=JAUTYJJXBOSATPJD9B624X) for you to query for free. Alternatively, [load this dataset](https://ghe.clickhouse.tech/#download-the-dataset) into ClickHouse yourself.


While the above dataset provides us with an overview of GitHub Projects, it doesn’t provide commit histories. Admittedly, this would be a much larger dataset. However, using the [git\-import](https://clickhouse.com/docs/en/getting-started/example-datasets/github#generating-the-data) tool distributed with ClickHouse, we can easily generate the full commit history of a repository with a single command. This produces three files of increasing granularity: a file with a row for every commit, a file with a row per file change, and finally, a line\-by\-line change history. We had already used this same tool to do an analysis on our own ClickHouse repository and documented the steps [here](https://clickhouse.com/docs/en/getting-started/example-datasets/github#downloading-and-inserting-the-data).


While all of the datasets used in our demo are public and can be downloaded or generated, we’ve also assembled [some simple instructions](https://gist.github.com/gingerwizard/1c03af6be54b56fe0f11871278555cfd) to make reproducing this demo a little easier. Our dashboard is also available in [Grafana’s public catalog](https://grafana.com/grafana/dashboards/18065).


## Building the visualizations [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#building-the-visualizations)


Armed with both datasets, building visualizations became straightforward. Our final dashboard aimed to use both datasets, with a list of possible questions already documented \- [here](https://ghe.clickhouse.tech/#let-s-play-with-the-data) and [here](https://clickhouse.com/docs/en/getting-started/example-datasets/github#queries). This left us simply needing to select those questions of interest and use the appropriate Grafana syntax to ensure time filters were respected before choosing a visualization. In the spirit of OSS, we also explored some of Grafana’s community visualizations, such as the [Treemap](https://grafana.com/grafana/plugins/marcusolsson-treemap-panel/) and [Word Cloud](https://grafana.com/grafana/plugins/magnesium-wordcloud-panel/) plugins. To visualize committers over time, for example, we simply need to inject the variables `$__timeFilter(time)` and `$__timeInterval(time)` to ensure the time filter is applied and the bucket sizes are appropriate. For more details on how these work, either watch the webinar or see [here](https://github.com/grafana/clickhouse-datasource#macros).


![grafana_heatmap.png](/uploads/grafana_heatmap_5fb5bda626.png)

```
SELECT $__timeInterval(time) as time, author, count(*) as ` ` FROM commits WHERE $__timeFilter(time) AND author IN (
    SELECT author
    FROM commits WHERE author NOT LIKE '%renovate[bot]%' AND $__timeFilter(time)
    GROUP BY author
    ORDER BY count() DESC
    LIMIT 15
) GROUP BY author, time ORDER BY time, author ASC, time DESC LIMIT 10000

```

## The final result [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#the-final-result)


We encourage the users to watch the webinar to not only learn some tips and tricks for building ClickHouse powered visualizations in Grafana but also to obtain a better appreciation for the history of such as successful OSS project as Grafana. For us, we’re impressed that Grafana founder [Torkel](https://github.com/torkelo) remains such an instrumental committer today as when the project was founded. Having spent a good part of the first 5yrs rewriting each other's code, [Carl Bergquist](https://github.com/bergquist) and Torkel have clearly had a huge impact on what is a thriving community today. While the number of commits per day has steadily increased, what is apparent is the amount of work done by commits has increased dramatically. Key features such as alerting being added and a docker file being made available are by far the most popular issues. Finally, we were happy to see people committing to both repositories while noticing that community members starring both repositories (now over 6500\) star Grafana first! Hopefully you agree our final dashboard is alittle richer than Github Pulse.


![grafana-1.png](/uploads/grafana_1_c609ddf5bc.png)
![grafana-2.png](/uploads/grafana_2_46122611c0.png)
## Gathering community feedback [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#gathering-community-feedback)


Webinars give us the opportunity to collect direct feedback from our community. At the end, we thus asked our users which features they would next want to see supported in the ClickHouse datasource for Grafana. The results below were enlightening to us, and you can expect them to influence our roadmap, which we will publish shortly in our [public repository](https://github.com/grafana/clickhouse-datasource/issues).


![grafana_poll.png](/uploads/grafana_poll_222766278a.png)
## Conclusion [\#](/blog/introduction-to-clickhouse-and-grafana-webinar#conclusion)


In this post, we’ve summarised our recent webinar with Grafana concerning the official Grafana plugin for ClickHouse. Thanks to our friends at Grafana for hosting, congratulations on the last 10 yrs, and we enjoy watching.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
