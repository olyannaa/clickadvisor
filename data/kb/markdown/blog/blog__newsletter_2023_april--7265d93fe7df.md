# ClickHouse Newsletter April 2023: Lightweight Deletes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter April 2023: Lightweight Deletes

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 25, 2023 · 9 minutes readHave you noticed our new look? We took an opportunity to update our website, refresh our brand, and are – presently – designing swag. Keep an eye on the website, or join an event near you, for an opportunity to acquire some new ClickHouse gear!


We’ve reordered this month’s newsletter to get into the query of the month more quickly, but the customary reading list and upcoming events appear at the bottom.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox? [Sign up here](https://discover.clickhouse.com/newsletter.html?utm_medium=email&utm_source=clickhouse&utm_campaign=newsletter).


## ClickHouse v23\.3 [\#](/blog/newsletter_2023_april#clickhouse-v233)


- 22 new features.
- 14 performance optimisations.
- 61 bug fixes.


You can read about all the features in detail in the [v23\.3 blog post](https://clickhouse.com/blog/clickhouse-release-23-03) and, if you are interested, don’t forget to sign\-up for the live [23\.4 release call](https://clickhouse.com/company/events/v23-4-release-webinar) (Q\&A welcome).


**Lightweight Deletes are now GA (Jianmei Zhang and Alexander Gololobov)**


This approach to removing data now represents the preferred and most efficient way to remove data from ClickHouse. Exposed via the DELETE FROM table syntax, users can specify a condition to remove specific rows.


**Traces in Grafana**


As part of our [recent blog post](https://clickhouse.com/blog/storing-traces-and-spans-open-telemetry-in-clickhouse) on building an Observability solution on ClickHouse we focused on traces and realized that their rendering in our official Grafana plugin could be significantly improved. With a small few changes, the latest release now supports the visualization of traces using the [Traces Panel](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/traces/) and [Explore view](https://grafana.com/docs/grafana/latest/explore/) in Grafana.


**Parallel Replicas (Nikita Mikhailov)**


With [parallel replicas](https://github.com/ClickHouse/ClickHouse/pull/29279), data can be processed in parallel by multiple replicas of the same shard. This allows query performance to be scaled as distinct subsets of data can be processed in parallel by multiple ClickHouse hosts.


## Query of the Month \- “Lightweight Deletes” [\#](/blog/newsletter_2023_april#query-of-the-month---lightweight-deletes)


Lightweight deletes have the potential to impact how users fundamentally approach handling uses in ClickHouse, where the data is not immutable. For this month's query, we explore how Lightweight deletes can be used when incrementally updating materialized tables.


We regularly see users with complex schemas needing to materialize multiple tables into a new table via a JOIN operation to accelerate subsequent queries. In data warehousing use cases, this table would typically represent a model. This "de\-normalization" process is typically achieved in ClickHouse by using an `INSERT INTO SELECT` query [link](https://clickhouse.com/docs/en/sql-reference/statements/insert-into#inserting-the-results-of-select), where the results of the join are inserted into a target table. We visualize this below:


![materialized-target.png](/uploads/materialized_target_d864e66596.png)
As well as simplifying subsequent queries, this approach has the potential to improve query performance dramatically. While this solves cases where the data is static, more thought is required if the source tables are subject to changes. In cases where the source tables are append\-only, the denormalized table can easily be updated with a simple condition that identifies any changes. For example, this could be a timestamp column on the source tables that identifies new rows. With this condition, we can stream new rows into the target table by re\-executing the `INSERT INTO SELECT`.


![Update-materializedsimple.png](/uploads/Update_materializedsimple_125e068d05.png)
Things get a little more complex if the source tables are subject to updates and duplicates. In this case, users might stream new rows into a temporary table (1\). The target table could then be streamed into a new table, with a check to omit results in the temporary table (2\) \- this assumes the presence of a unique row identifier (`id` below). Rows from the temporary table are then inserted into the new table (3\). This new table could subsequently be exposed as the latest version of the model, e.g., with an `EXCHANGE` statement [link](https://clickhouse.com/docs/en/sql-reference/statements/exchange#exchange-tables). This rather complex process is shown below:


![old-incremental.png](/uploads/old_incremental_10d5efe4be.png)
This process requires a complete copy of the data to be made in order to update the target table. This was historically preferred in ClickHouse to [delete Mutations](https://clickhouse.com/blog/handling-updates-and-deletes-in-clickhouse), which incur a [higher resource cost](https://clickhouse.com/docs/en/cloud/bestpractices/avoid-mutations) than simple appends. However, the arrival of lighter\-weight deletes opens the potential to simplify this process. Below we show how new rows are still streamed into a temporary table (1\). However, this temporary table can now be used to remove rows from the existing target table (using the new DELETE syntax) before inserting the new rows. This avoids copying data and provides a faster means of updating a materialized model.


![delete-incremental.png](/uploads/delete_incremental_7c3f2d8576.png)
Note: the temporary table here can potentially just be a subquery. The use of a table ensures the process isn’t memory bound.


The above logic is still quite complex: surely there is a way to encapsulate this process and make it simpler? Readers of this newsletter, who are also dbt users, will immediately recognize the above use case as "[Incremental Materializations](https://docs.getdbt.com/docs/build/materializations#incremental)" \- a simple model type in dbt. Hence, the [dbt\-clickhouse plugin](https://github.com/ClickHouse/dbt-clickhouse) utilizes the exact processes above, with the lightweight deletes approach now recommended.


The use cases for Lightweight deletes go beyond incremental models...support for processing [Kafka tombstone messages](https://medium.com/@damienthomlutz/deleting-records-in-kafka-aka-tombstones-651114655a16) anyone? We'd love to hear how Lightweight deletes have changed your workflows!


## Reading List [\#](/blog/newsletter_2023_april#reading-list)


Some of our favorite reads that you may have missed include:


1. [A Deep Dive into Apache Parquet with ClickHouse \- Part 1](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing) \- Since its release in 2013 as a columnar storage for Hadoop, Parquet has become almost ubiquitous as a file interchange format that offers efficient storage and retrieval. In this blog series, we explore how ClickHouse can be used to read and write this format before diving into the Parquet in more detail. For more experienced Parquet users, we also discuss some optimizations that users can make when writing Parquet files using ClickHouse to maximize compression, as well as some recent developments to optimize read performance using parallelization.
2. [My Journey as a Serial Startup Product Manager](https://clickhouse.com/blog/my-journey-as-a-serial-startup-product-manager) \- In this post our VP of Product, Tanya Bragin, shares the story of her career. In her own words, “I often get questions about how I decided to become a product manager at startups, and what I learned over the years. The truth is, I had no such plan in life \- I fell into the product management career somewhat by accident. But I have learned a few things along the way, and I will attempt to summarize the highlights in this blog.”
3. [Speeding up LZ4 in ClickHouse](https://clickhouse.com/blog/lz4-compression-in-clickhouse) \- This blog was originally posted in 2019\. We edited and reposted in tribute to the authors of the LZ family of algorithms: Abraham Lempel and Jacob Ziv, who recently passed away. It can be tempting to think that every new feature is novel. That every new release is set to change the market. However, we \-\- as an industry \-\- stand on the shoulder of giants. Jacob's contributions to information theory (beyond compression algorithms) are, and remain, an inspiration to generations of practitioners and researchers.
4. [Building Real\-time Analytics Apps with ClickHouse and Hex](https://clickhouse.com/blog/building-real-time-applications-with-clickhouse-and-hex-notebook-keeper-engine) \- As the world’s fastest analytical database, we are always looking for tools that help our users quickly and easily realize their dream of building applications on top of ClickHouse. So when Hex.tech announced the availability of ClickHouse as a data source, we were excited to see the potential for building real\-time applications. In this blog post, we explore how we collected data and built a simple proof of concept for our application “ClickHub” using Hex.tech.


## Upcoming Events [\#](/blog/newsletter_2023_april#upcoming-events)


Mark your calendars for the following events:


**ClickHouse v23\.4 Release Webinar**   

Wednesday, April 26 @ 9 AM PDT / 6 PM CEST   

[Register here](https://clickhouse.com/company/events/v23-4-release-webinar)


**Introduction to ClickHouse Cloud Workshop in NYC (space is limited!)**   

Wednesday, April 26 @ 10 AM EDT   

[Register here](https://clickhouse.com/company/events/2023-04-26-clickhouse-workshop-nyc)


**ClickHouse Spring Meetup in Manhattan**   

Wednesday, April 26 @ 5 PM EDT   

[Register here](https://www.meetup.com/clickhouse-new-york-user-group/events/292517734)


**Supabase \+ ClickHouse: Combining the Best of the OLTP and OLAP Worlds**   

Tuesday, May 2 @ 8 AM PDT   

[Register here](https://clickhouse.com/company/events/2023-05-02-supabase-webinar)


**Introduction to ClickHouse Workshop @ AWS Munich (space is limited!)**   

Wednesday, May 3 @ 9 AM CEST   

[Register here](https://clickhouse.com/company/events/2023-05-03-clickhouse-workshop-munich)


**Building Real\-time Analytics Apps with ClickHouse and Hex**   

Wednesday, May 10 @ 9 AM PDT / 6 PM CEST   

[Register here](https://clickhouse.com/company/events/2023-05-10-hex-webinar)


**ClickHouse Meetup in Berlin**   

Tuesday, May 16 @ 6 PM CEST   

[Register here](https://www.meetup.com/clickhouse-berlin-user-group/events/292892466)


**ClickHouse Meetup in Barcelona**   

Tuesday, May 23 @ 6 PM CEST   

[Register here](https://www.meetup.com/clickhouse-barcelona-user-group/events/292892669)


Thanks for reading, and we’ll see you next month!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
