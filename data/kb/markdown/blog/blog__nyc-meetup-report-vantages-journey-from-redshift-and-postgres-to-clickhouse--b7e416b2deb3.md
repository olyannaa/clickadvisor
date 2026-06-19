# Vantage's Journey from Redshift and Postgres to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Vantage's Journey from Redshift and Postgres to ClickHouse

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[ClickHouse Editor](/authors/clickhouse-editor)Jul 13, 2023 · 7 minutes read
  

Brooke McKim, co\-founder and CTO of Vantage shares their experience of transitioning from Redshift and Postgres to ClickHouse. In their talk they took us through Vantage's journey, discussing the challenges with their previous architecture, the decision to switch to ClickHouse, and the benefits they've seen since making the move.


[Vantage](https://vantage.sh/) is a cloud cost optimization platform enabling teams to manage and optimize their cloud costs across ten cloud infrastructure and service providers, such as AWS, Azure, Google Cloud, Datadog, New Relic, Snowflake, Databricks, Fastly, MongoDB Atlas, and Kubernetes. Their Autopilot managed service optimizes AWS bills by automatically buying and selling financial commitments, resulting in up to 72% savings.


The Vantage user interface (UI) offers a comprehensive view of all relevant data, with features for filtering, aggregation, and reporting. A standout feature is the ability to drill down into specific dimensions. For instance, if you're looking at the cost for Amazon's S3 service, you can click into that category and break it down further. Even with larger accounts, which can have billions of records spanning six to twelve months, you can delve into specific resources, providing an in\-depth perspective on cost data at scale.


![Vantage UI.png](/uploads/Vantage_UI_5eba58e23e.png)
*The Vantage UI provides a detailed view of cloud costs with unique drill\-down capabilities for in\-depth data analysis.*
## Challenges with Redshift and Postgres [\#](/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse#challenges-with-redshift-and-postgres)


Vantage initially started with Postgres, which seemed adequate at first. However, McKim explained they quickly encountered performance issues as they began to scale. “We were in this growth phase and it seemed like every week or month we were getting a customer that was an order of magnitude larger than the one we had the previous. A lot of that time was spent keeping up with the performance issues. Eventually we just hit a wall with Postgres and had to figure out a different solution.”


Postgres uses a process called 'vacuum' to remove deleted records from disk space. However, with Vantage's frequent data deletions and insertions, this vacuum process was constantly running, using up resources and slowing performance. The system struggled to keep indexes in memory due to constant changes, leading to slow response times. This led Vantage to seek alternatives that offered similar functionality but were more efficient.


The team at Vantage sought a solution similar to Postgres for a quick transition with minimal operational overhead. They decided to choose Redshift for its familiarity, as it's based on an older version of Postgres. However, [Redshift presented its own challenges](https://clickhouse.com/blog/redshift-vs-clickhouse-comparison). Although it could handle larger volumes of data, it struggled with Vantage's constant deletes and updates and required data to always be inserted in sort order for optimal performance. The team attempted to mitigate these issues by running vacuum sort operations frequently and partitioning tables. They also created a hybrid architecture with Redshift as their data warehouse and Postgres as a cache. However, this resulted in a limited user experience and the need to move billions of records daily between Redshift and Postgres. Conversely, ClickHouse’s ReplicatedMergeTree table engine allows row updates to be handled efficiently and transparently.


![Vantage - Redshift.png](/uploads/Vantage_Redshift_cf31a64863.png)
To be able to present cost data to users, Vantage was generating tens of thousands of reports nightly, leading to a large amount of data being deleted and reinserted into Postgres. This resulted in high cloud costs, with Postgres costs surpassing those of Redshift due to the provision of IOPS and the numerous write operations. They could have scaled this further, but reached a cost limit they were unwilling to exceed. This resulted in numerous "roll up" tables with various data variations. McKim mentioned, "We're inserting data into Redshift. It's unsorted. We have to go back and run this job, which ends up being very expensive, especially as your table gets very large."


## Discovering ClickHouse Cloud as an Alternative [\#](/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse#discovering-clickhouse-cloud-as-an-alternative)


As Vantage started exploring alternatives, they met with the ClickHouse team at the AWS re conference. They were attracted to ClickHouse Cloud for its ease of use, low operational overhead, and comprehensive documentation.


“ClickHouse has been great to work with. I think there's a bit of a learning curve when you first approach ClickHouse, but once you understand some of the intricacies of how it differs from traditional relational databases, and how the different engines work, it's actually pretty easy to move over to,” explained McKim.


The team embarked on a 60\-day transition process, which mostly involved ensuring the quality and correctness of the data. McKim mentioned, "The documentation is just far more comprehensive and technically deeper than anything you'll get from AWS on Redshift, which has just been super helpful because you can just understand how the system works."


## Transitioning to ClickHouse and Tackling Data Ingestion Challenges [\#](/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse#transitioning-to-clickhouse-and-tackling-data-ingestion-challenges)


With ClickHouse, Vantage no longer needed to delete and reinsert data for their nightly report generation. Instead, they began versioning imports using the [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engine and added an import version column that increments with each data import. This approach allowed them to reduce their operational overhead and cut costs while still maintaining high performance. McKim said, "ClickHouse is just taking the existing data in the table and doing a merge automatically with any new data that is inserted, which is great as it saves us having to delete and update rows."


In contrast to Redshift, ClickHouse automatically sorts and merges data, which saves both time and resources. They also appreciate ClickHouse's comprehensive documentation, no downtime updates, and data storage in S3 which is cost\-effective. They contrast this with their experiences with Redshift, which has forced updates incuring downtime, potential service interruptions, and seems less suited for real\-time analytics.


![Vantage ClickHouse Cloud benefits.png](/uploads/Vantage_Click_House_Cloud_benefits_d31c7c436c.png)
Since making the switch to ClickHouse Cloud, Vantage has experienced significant cost savings and performance improvements. They have doubled the resources on their ClickHouse setup at a similar price to their Redshift setup. Additionally, the performance they see from ClickHouse is comparable to a well\-indexed, pre\-aggregated table in RDS Postgres, which is also cheaper than their previous Postgres setup.


## Looking Forward to Future Opportunities with ClickHouse [\#](/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse#looking-forward-to-future-opportunities-with-clickhouse)


Vantage is excited about the potential for reducing operational overhead and is enthusiastic about the rate of innovation they see from the ClickHouse team, as they continue to improve and expand their product. They also look forward to exploring new use cases and taking advantage of ClickHouse's capabilities to further enhance their platform and better serve their customers.


Vantage's journey from Redshift and Postgres to ClickHouse demonstrates the value of finding a database solution that better aligns with a company's specific needs. With ClickHouse Cloud, Vantage has found a more cost\-effective, high\-performance solution that has enabled them to grow and improve their platform.


## More Details [\#](/blog/nyc-meetup-report-vantages-journey-from-redshift-and-postgres-to-clickhouse#more-details)


- This talk was given at the [ClickHouse Community Meetup](https://www.meetup.com/clickhouse-new-york-user-group/events/292517734/) in NYC on April 26, 2023
- The presentation materials are available [on GitHub](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup72/Vantage_%20Our%20Journey%20from%20Redshift%20to%20Clickhouse.pdf)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
