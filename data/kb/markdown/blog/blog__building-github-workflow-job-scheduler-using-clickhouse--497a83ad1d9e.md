# Building an Auto\-Scaling Lambda based on Github's Workflow Job Queue


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building an Auto\-Scaling Lambda based on Github's Workflow Job Queue

![](/_next/image?url=%2Fuploads%2Fmisha_3ac4306654.png&w=96&q=75)[Misha Shiryaev](/authors/misha-shiryaev)Jun 15, 2023 · 3 minutes readIn a [previous post](https://clickhouse.com/blog/monitor-github-action-workflow-job-queues) I introduced how you can build a table in ClickHouse containing all of the data from your GitHub Actions using GitHub Webhooks. We do this for the ClickHouse organization, to provide essential metrics on the internal queue of workflow jobs.


Just having this and doing nothing with it would be a huge waste of gemstone data, so a couple of months ago the data was used to implement a lambda to quickly inflate and deflate our workers on demand. This has improved the responsiveness of our job launching, reacting to an increase in scheduled tests, as well as saving us compute when the workload is lower. Let's discuss how we achieved this!


## The Idea [\#](/blog/building-github-workflow-job-scheduler-using-clickhouse#the-idea)


We have all events in our database for when a workflow job was created, started or finished. Consider this query from the previous post, which returns the current ClickHouse queue size for self\-managed GitHub Runners:



```

SELECT
    last_status,
    count() AS queue,
    labels
FROM
(
    SELECT
        argMax(status, updated_at) AS last_status,
        labels,
        id,
        html_url
    FROM default.workflow_jobs
    WHERE has(labels, 'self-hosted') AND (started_at > (now() - toIntervalHour(3)))
    GROUP BY ALL
    HAVING last_status != 'completed'
)
GROUP BY ALL
ORDER BY
    labels ASC,
    last_status ASC
 

```


![query-result.png](/uploads/query_result_1ebbf3568f.png)
Knowing this allows us proactively to scale\-up the runners to cover the demand, or scale\-down to free unnecessary resources.


The new desired capacity is calculated based on the current number of runners and jobs in progress and queue. If there is a deficit, we increase the capacity proportional to it (usually, deficit / 5\). And for the unnecessary reserve, we quickly deflate the group (reserve / 2\).


## An old system [\#](/blog/building-github-workflow-job-scheduler-using-clickhouse#an-old-system)


The officially recommended approach in AWS to trigger scaling up/down is assigning CloudWatch alarms to Auto\-Scaling Groups (ASG.) So, whenever an alarm is in an alarm state, the ASG adds or removes some instances.


We used to monitor how many instances of each ASG were in a busy state using the GitHub runners API. If there were more than 97% busy runners for 5 minutes, another one runner was added. For scaling out the rule was less than 70%.


The system used to be very reactive and inert. To warm up groups with 50\+ runners it required a few hours.


## Improvements and statistics [\#](/blog/building-github-workflow-job-scheduler-using-clickhouse#improvements-and-statistics)


After switching to our new system, we both achieved faster jobs launching and a saving of compute time after the job was done. You can see how it affected the runners on the graphs:


The old system:


[![](/uploads/old_system_8e1bd87afb.png)](/uploads/old_system_8e1bd87afb.png)


The new system:


[![](/uploads/new_system_232c534dda.png)](/uploads/new_system_232c534dda.png)


We can see how the Busy and Active Runners are more tightly correlated in the new system, indicating that provisioned workers are more heavily utilized. The code used here is all available in [our repository](https://github.com/ClickHouse/ClickHouse/blob/2ab313e6b4272f5888bc7d3b54533b3f8ba86fba/tests/ci/autoscale_runners_lambda/app.py). Hopefully others can make similar improvements and savings!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
