# ClickHouse Newsletter July 2023: Seeing Clearly


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter July 2023: Seeing Clearly

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 24, 2023 · 13 minutes readWelcome to the July ClickHouse Newsletter. Summer is finally here (in half of the world) but we aren’t slowing down. This month’s edition of the newsletter not only brings you an update on the recent release, interesting links, and upcoming events but also a truly exciting query of the month!


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? [Sign up here](https://discover.clickhouse.com/newsletter.html?utm_medium=email&utm_source=clickhouse&utm_campaign=newsletter).


If you’d like to continue receiving these updates, please [click here](https://discover.clickhouse.com/newsletter.html?utm_medium=email&utm_source=clickhouse&utm_campaign=newsletter) to confirm your email preferences.


## ClickHouse v23\.6 [\#](/blog/newsletter_2023_july#clickhouse-v236)


- 10 new features.
- 12 performance optimisations.
- 31 bug fixes.


You can catch all the features in detail in the recorded [v23\.6 release call on YouTube](https://www.youtube.com/watch?v=cuf_hYn7dqU) and, if you are interested, don’t forget to sign\-up for the live [23\.7 release call](https://clickhouse.com/company/events/v23-7-community-release-call?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter) (Q\&A welcome).


A special welcome to all the new contributors to 23\.6! ClickHouse's popularity is, in large part, due to the efforts of the community who contributes. Seeing that community grow is always humbling.


If you see your name here, please reach out to us...but we will be finding you on Twitter, etc as well.



```
Chang Chen, Dmitry Kardymon, Hongbin Ma, Julian Maicher, Thomas Panetti, YalalovSM, kevinyhzou, tpanetti, 郭小龙

```

### Sorting Almost Sorted Data [\#](/blog/newsletter_2023_july#sorting-almost-sorted-data)


[Watch the introduction of this feature!](https://www.youtube.com/watch?v=cuf_hYn7dqU&t=33m55s)


ClickHouse loves sorted data. As a column\-oriented database, sorting data on insert is fundamental to query performance and one of the early concepts users encounter when needing to specify an `ORDER BY` clause when creating a table. In 23\.6, ClickHouse will now exploit any natural sorting patterns in the data to improve query performance. This is particularly in cases where a column is known to be monotonically increasing in most cases but is not part of the ordering key.


### Mongo 6\.x Support [\#](/blog/newsletter_2023_july#mongo-6x-support)


[Watch the introduction of this feature!](https://www.youtube.com/watch?v=cuf_hYn7dqU&t=25m00s)


If there is one data store that is almost ubiquitous in modern web application stacks, it's MongoDB. MongoDB is a document\-oriented database designed to store and retrieve JSON\-like data. While ClickHouse has supported MongoDB with a table function for some time, Mongo v5\.1 introduced protocol changes that required this integration to be updated. We are now pleased to announce support for Mongo up to the latest v6\.


### Transform function [\#](/blog/newsletter_2023_july#transform-function)


[Watch the introduction of this feature!](https://www.youtube.com/watch?v=cuf_hYn7dqU&t=06m56s)


A common problem in data processing is the need to map values \- often codes to something meaningful. This task is best performed in SQL using the transform function. This function has been supported in ClickHouse for some time for numbers, dates, and strings. In 23\.6, we have added support to this function for all data types. The transform function can now be used to transform columns to other types.


## Query of the Month \- windowFunnel [\#](/blog/newsletter_2023_july#query-of-the-month---windowfunnel)


Users new to ClickHouse with prior database experience will often be surprised by the number of analytical functions supported beyond standard ANSI SQL. These are specifically targeted at making certain queries simpler to write and faster to execute.


A less well known function designed for a common question asked by many businesses, is the windowFunnel. For this month's “Query of Month” we’ll explore how this function can be used to solve a funnel analysis of user behavior. At the same time we’ll use the opportunity to understand our own contributors a little more.


The windowFunnel function allows the counting of sequences of events in a sliding time window. More specifically, users can specify an expected sequence and the allowed time period in which they can occur. The function will in turn calculate the maximum number of events that occurred for each sub\-sequence in the chain.


The name of this function indicates its intended application: funnel analysis. This can be succinctly described as counting several events users perform one after another. By counting how many unique users reach each event in sequence, a conversion rate for each step can be calculated allowing business owners to localize a problem down to a certain stage. This is a common problem in ecommerce, where businesses aim to identify how users “drop off” during the required steps to making a purchase.


While this can be [solved in classic SQL](https://medium.com/cube-dev/sql-queries-for-funnel-analysis-35d5e456371d), this is an example of how ClickHouse functions can dramatically simplify a query.


For example purposes, we’ll use the popular Github Events dataset. This dataset, present in our documentation, captures all events on GitHub from 2011\. This includes events such as user's adding a repository star, creating a fork, issuing a PR and making a comment. This event data naturally lends itself to a funnel analysis. In our case, we were curious to see what percentage of our users on forking the ClickHouse repository raise a PR within 30 days and how this behavior compares to other popular open\-source projects.


For this query our event sequence consists of only two event types: a `ForkEvent` followed by a `PullRequestEvent`. These events need to occur for a specific user, on the ClickHouse repository, within a 30 day period.


In the interests of making our query efficient, we first identify the users who have forked the ClickHouse repository:



```
SELECT DISTINCT actor_login AS logins FROM github_events
WHERE ((repo_name = 'ClickHouse/ClickHouse') OR (repo_name = 'yandex/ClickHouse')) AND (event_type = 'ForkEvent'))

```

The full parameters of windowFunnel function, and the algorithm it uses, can be found in our docs. In summary, we need to specify the permitted time period and the sequence of events:



```
windowFunnel(2592000)(created_at, event_type = 'ForkEvent', event_type = 'PullRequestEvent')

```

Limiting our analysis to those users who have forked the repository, our query:



```
WITH logins AS
	(
    	SELECT DISTINCT actor_login AS logins
    	FROM github_events
    	WHERE (repo_name IN ['yandex/ClickHouse', 'ClickHouse/ClickHouse']) AND (event_type = 'ForkEvent')
	)
SELECT
	actor_login,
	windowFunnel(2592000)(created_at, event_type = 'ForkEvent', event_type = 'PullRequestEvent') AS step
FROM github_events
WHERE (repo_name IN ['yandex/ClickHouse', 'ClickHouse/ClickHouse']) AND (actor_login IN (logins)) AND (event_type IN ['ForkEvent', 'PullRequestEvent'])
GROUP BY actor_login
LIMIT 10

┌─actor_login──────┬─step─┐
│ AntiTopQuark 	   │	1 │
│ AndreyTokmakov   │	2 │
│ aig          	   │	1 │
│ maks-buren630501 │	2 │
│ qwe4815124   	   │	1 │
│ amdfansheng  	   │	1 │
│ lenovore     	   │	1 │
│ calipeng     	   │	1 │
│ xiaohan2013  	   │	1 │
│ fjteam       	   │	1 │
└──────────────────┴──────┘

10 rows in set. Elapsed: 0.095 sec. Processed 812.09 thousand rows, 6.30 MB (8.54 million rows/s., 66.20 MB/s.)

```

This returns the number of steps in our chain performed by each user, with 1 indicating a Fork event and 2 a Fork followed by a PR within 30 days. Finally, we need to aggregate across these users and compute the total number of users who reach each step:



```
WITH logins AS
	(
    	SELECT DISTINCT actor_login AS logins
    	FROM github_events
    	WHERE (repo_name IN ['yandex/ClickHouse', 'ClickHouse/ClickHouse']) AND (event_type = 'ForkEvent')
	)
SELECT
	step,
	count()
FROM
(
	SELECT
    	actor_login,
    	windowFunnel(2592000)(created_at, event_type = 'ForkEvent', event_type = 'PullRequestEvent') AS step
	FROM github_events
	WHERE (repo_name IN ['yandex/ClickHouse', 'ClickHouse/ClickHouse']) AND (actor_login IN (logins)) AND (event_type IN ['ForkEvent', 'PullRequestEvent'])
	GROUP BY actor_login
)
GROUP BY step
ORDER BY step ASC

┌─step─┬─count()─┐
│	1  │	5234 │
│	2  │	1115 │
└──────┴─────────┘

2 rows in set. Elapsed: 0.108 sec. Processed 812.09 thousand rows, 6.30 MB (7.49 million rows/s., 58.03 MB/s.)

```

So around 17% of users who fork the ClickHouse repository go on to create a PR within 30 days. This feels like an encouraging number, but we were curious to see how this compares to other similarly popular projects. We define popular as being more than 25k stars and 5k forks (yes, a high bar) and compute this ratio for all projects meeting the criteria. Note here we need to group by user and repository, to avoid counting users forking a repository and PR’ing another within 30 days. This is quite computationally expensive but still completes in a few seconds:



```
WITH repos AS
	(
    	SELECT if(repo_name = 'yandex/ClickHouse', 'ClickHouse/ClickHouse', repo_name) AS repo_name
    	FROM github_events
    	WHERE event_type IN ['ForkEvent', 'WatchEvent']
    	GROUP BY repo_name
    	HAVING (countIf(event_type = 'ForkEvent') > 5000) AND (countIf(event_type = 'WatchEvent') > 25000)
	)
SELECT
	rowNumberInAllBlocks() AS position,
	repo,
	round(countIf(step = 2) / count(), 3) AS ratio
FROM
(
	SELECT
    	repo,
    	windowFunnel(2592000)(created_at, event_type = 'ForkEvent', event_type = 'PullRequestEvent') AS step
	FROM github_events
	WHERE ((repo_name IN (repos)) OR (repo_name = 'yandex/ClickHouse')) AND (event_type IN ['ForkEvent', 'PullRequestEvent'])
	GROUP BY
    	actor_login,
    	if(repo_name = 'yandex/ClickHouse', 'ClickHouse/ClickHouse', repo_name) AS repo
	HAVING step > 0 //ignore users who can raise a PR without forking
)
GROUP BY repo
ORDER BY ratio DESC
LIMIT 25

┌─position─┬─repo───────────────────────────────────┬─ratio─┐
│    	0  │ firstcontributions/first-contributions │ 0.711 │
│    	1  │ tldr-pages/tldr                    	│ 0.458 │
│    	2  │ DefinitelyTyped/DefinitelyTyped    	│ 0.451 │
│    	3  │ laravel/framework                  	│ 0.373 │
│    	4  │ gatsbyjs/gatsby                    	│ 0.298 │
│    	5  │ rust-lang/rust                     	│ 0.275 │
│    	6  │ sequelize/sequelize                	│ 0.268 │
│    	7  │ symfony/symfony                    	│  0.26 │
│    	8  │ ansible/ansible                    	│ 0.231 │
│    	9  │ JuliaLang/julia                    	│ 0.215 │
│   	10 │ facebook/jest                      	│  0.21 │
│   	11 │ hashicorp/terraform                	│ 0.202 │
│   	12 │ home-assistant/home-assistant      	│ 0.199 │
│   	13 │ ripienaar/free-for-dev             	│ 0.193 │
│   	14 │ fastlane/fastlane                  	│ 0.191 │
│   	15 │ freeCodeCamp/freeCodeCamp          	│  0.19 │
│   	16 │ hwchase17/langchain                	│ 0.186 │
│   	17 │ neovim/neovim                      	│ 0.185 │
│   	18 │ serverless/serverless              	│ 0.182 │
│   	19 │ vuejs/awesome-vue                  	│ 0.181 │
│   	20 │ kubernetes/minikube                	│ 0.177 │
│   	21 │ sveltejs/svelte                    	│ 0.176 │
│   	22 │ ClickHouse/ClickHouse              	│ 0.176 │
│   	23 │ go-gitea/gitea                     	│ 0.175 │
│   	24 │ avelino/awesome-go                 	│ 0.174 │
└──────────┴────────────────────────────────────────┴───────┘

25 rows in set. Elapsed: 2.970 sec. Processed 554.18 million rows, 1.87 GB (186.58 million rows/s., 629.18 MB/s.)

```

Perhaps all Github\-based metrics tend towards a vanity exercise, but we think 22nd here isn’t too bad and shows a healthy engagement pattern from our users. More importantly, it allowed us to show you a cool ClickHouse function which hopefully will make your queries simpler!


## Interesting Links [\#](/blog/newsletter_2023_july#interesting-links)


Some of our favorite reads that you may have missed include:


1. **[Monitorama PDX 2023 \- How to Scale Observability Without Bankrupting the Company \- David Gildeh, Netflix](https://vimeo.com/843994807)** \- From the talk description: “Every company has struggled with controlling their Observability costs as the amount of data that needs to be collected, stored and queried in real time has gone up exponentially! Netflix has had to solve this problem as it rapidly scaled into a web scale company with 100m's of customers around the world.” Keep an eye out for ClickHouse and how it fits into the infrastructure!!
2. **[Working with Time Series Data in ClickHouse](https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter)** \- Many datasets are collected over time to analyze and discover meaningful trends. Each data point usually has a time assigned when we collect logs or business events. This blog post provides tips and tricks for working with time series data based on everyday tasks that we see our users needing to perform. We cover querying and common data type problems, such as handling gauges, and explore how performance can be improved as we scale.
3. **[ClickHouse and PostgreSQL \- a Match Made in Data Heaven](https://clickhouse.com/blog/migrating-data-between-clickhouse-postgres?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter)** \- PostgreSQL and ClickHouse represent the best of class concerning open\-source databases, each addressing different use cases with their respective strengths and weaknesses. Having recently enabled our PostgreSQL (and MySQL) integrations in ClickHouse Cloud, we thought we’d take the opportunity to remind users of how these powerful integrations can be used with ClickHouse. (part 1 of a series)
4. **[Vector Search with ClickHouse](https://clickhouse.com/blog/vector-search-clickhouse-p1?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter)** \- Over the past year, Large Language Models (LLMs) along with products like ChatGPT have captured the world's imagination and have been driving a new wave of functionality built on top of them. The concept of vectors and vector search is core to powering features like recommendations, question answering, image / video search, and much more. In case you missed it, this series covers the basics of Vector Search and ClickHouse implementation all in one convenient series.
5. **[NYC Meetup Report: Vantage's Journey from Redshift and Postgres to ClickHouse](https://clickhouse.com/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter)** \- In case you missed the recording of Vantage’s great talk at our recent NYC meetup, you can read all about it in our meetup report. Vantage shares why they moved from Redshift and Postgres to ClickHouse including their challenges, decision to switch, and the benefits gained.


## Upcoming Events [\#](/blog/newsletter_2023_july#upcoming-events)


Mark your calendars for the following events:


**ClickHouse v23\.7 Release Webinar**   

Thursday, July 27 @ 9 AM PDT / 6 PM CEST   

Register [here](https://clickhouse.com/company/events/v23-7-community-release-call?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter).


**Meetup Boston**   

Tuesday, July 18 @ 6 PM EDT   

Register [here](https://www.meetup.com/clickhouse-boston-user-group/events/293913596).


**Meetup NYC**   

Wednesday, July 19 @ 6 PM EDT   

Register [here](https://www.meetup.com/clickhouse-new-york-user-group/events/293913441).


**Meetup Toronto**   

Thursday, July 20 @ 6 PM EDT   

Register [here](https://www.meetup.com/clickhouse-toronto-user-group/events/294183127).


**Meetup Singapore**   

Thursday, July 27 @ 6 PM SST   

Register [here](https://www.meetup.com/clickhouse-singapore-meetup-group/events/294428050/).


**ClickHouse Fundamentals \- Free Training**   

Wednesday, Aug 16 @ 1 PM BST / 2 PM CEST   

Register [here](https://clickhouse.com/company/events/clickhouse-workshop?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter).


**ClickHouse Cloud Onboarding \- Free Training**   

Wednesday, Aug 23 @ 8 AM PDT / 11 AM EDT / 5 PM CEST   

Register [here](https://clickhouse.com/company/events/clickhouse-onboarding-workshop?utm_medium=email&utm_source=clickhouse&utm_campaign=202307-newsletter).


Thanks for reading, and we’ll see you next month.


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
