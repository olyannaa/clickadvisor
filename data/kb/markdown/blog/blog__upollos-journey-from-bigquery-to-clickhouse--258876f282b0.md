# Scaling predictive insights: Upollo’s journey from BigQuery to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Scaling predictive insights: Upollo’s journey from BigQuery to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 4, 2024 · 9 minutes read
In 2021, Cayden Meyer was leading Canva’s enterprise, education, and teams efforts. Identifying opportunities for conversion, expansion, and retention, and understanding what influenced them, was key for helping Canva’s sales, customer success, and product teams focus their efforts, but no solution existed to help them do that easily. It was a gap Cayden had faced before as a product manager at Google, and that he knew must be shared by millions of subscription businesses around the world. 




“There just wasn’t a tool that solved that problem for me,” he says. “So I went out and built it.”




Today, Cayden’s company, [Upollo](https://upollo.ai/), helps businesses drive revenue and growth by predicting who’s likely to churn, convert, or expand — and why. Analyzing over 50 million users (plus millions more added each week) and $500 million in revenue, Upollo serves predictive insights to help its customers grow faster and build more effective products.




At the core of Upollo’s mission and offering is the need to process and analyze “billions and billions of events,” which include everything from clicks and page views to billing events and support interactions. As the company grew, however, serving more and more customers while handling over 40 terabytes of data, Cayden and the team recognized that their existing data warehouse, BigQuery, had become prohibitively costly and inefficient. 




To keep growing and delivering real\-time insights at scale, they needed a more efficient, scalable, cost\-effective solution — and their search led them to [ClickHouse Cloud](https://clickhouse.com/cloud).



## The BigQuery and Postgres bottleneck [\#](/blog/upollos-journey-from-bigquery-to-clickhouse#the-bigquery-and-postgres-bottleneck)



Cayden began using BigQuery during his time at Google, where he managed products like Google Keep, App Engine, Maps and Drive. Impressed by its performance and functionality, he chose BigQuery for Upollo’s initial data warehouse.




“BigQuery is a great product that can run internet\-scale queries very quickly,” Cayden says. “However, it presented two key challenges for us — cost and the scalability required for more complex workflows, like the ones needed for our use cases.”




As Upollo grew and onboarded more customers — “especially a few that had quite large datasets,” Cayden notes — database management costs steadily increased, until BigQuery expenses made up the majority of their monthly bill. “We were running queries that were thousands of dollars, while at the same time watching our data grow very quickly,” he says. “We did the math and found that no matter how we priced it, it just wasn’t scalable.”




The inefficiencies extended beyond cost. To serve analytics, Upollo had to duplicate work across BigQuery and Postgres — creating schemas, running queries, and transferring results. As Cayden explains, this workflow added unnecessary latency and increased engineering overhead. “We basically had to do the same work twice,” he says. “This created a ton of extra latency and added a huge amount of work for our team.”




Periodic data transfers from BigQuery to Postgres introduced even more delays, while Postgres struggled to handle large aggregations, often slowing down or timing out with bigger datasets. The combination of high costs, latency, and the operational headache of managing two separate databases made it increasingly difficult to deliver fresh analytics to customers. These limitations underscored the need for a more streamlined and scalable solution — one that could eliminate the dual\-database approach and simplify Upollo’s workflows.






![Blog_Upollo_var1_202411_FNL.png](/uploads/Blog_Upollo_var1_202411_FNL_00cff0be49.png)

## A more scalable solution [\#](/blog/upollos-journey-from-bigquery-to-clickhouse#a-more-scalable-solution)



As they began researching alternatives, the Upollo team established a few requirements. First and foremost, they needed a solution that could scale affordably with their massive data volumes. It had to support real\-time data serving without complex workarounds and duplications, while handling the big analytical queries that power Upollo’s predictive capabilities. Performance and reliability were essential, and they wanted a platform backed by a strong community to make sure it would keep improving over time.




“There’s a lot of interesting, amazing products out there, but we wanted a solution that we knew was used at the scale we needed and had a community of companies pushing for it to get better over time,” Cayden says. 




They also prioritized finding a managed service that would let them avoid the hassle of maintaining the database themselves. “We don’t want our engineers spending their time on upgrades, patches, and maintenance,” Cayden says. “We’d rather them focus on developing new features and building an amazing product.”




They were familiar with ClickHouse through the open\-source community and had seen it discussed on platforms like Hacker News, particularly for event\-heavy workloads. Comparing benchmarks on [ClickBench](https://benchmark.clickhouse.com/) and reading about other companies’ experience moving similar workloads, it became clear that ClickHouse might be the solution they were looking for. With its managed service offering, along with an active community and open\-source foundation, the OLAP database promised to simplify Upollo’s workflows and support its vision for an efficient, scalable data infrastructure. 




“We decided to give it a shot, see if it could handle our workloads, and decide if it made good long\-term sense for us,” Cayden says.



## ClickHouse in action [\#](/blog/upollos-journey-from-bigquery-to-clickhouse#clickhouse-in-action)



Cayden migrated Upollo’s core data to ClickHouse Cloud in just 30 minutes one afternoon. Setup was easy, allowing the team to quickly load and interact with their data. “We’ve been able to ingest very large batches of data very efficiently and very quickly,” Cayden says, highlighting their use of [ClickPipes](https://clickhouse.com/cloud/clickpipes) to move huge batches of event data in minutes.




For Upollo’s team and business, the impact has been massive. Not only has ClickHouse’s performance made queries up to 20 times faster, it has unlocked capabilities Upollo couldn’t even attempt before. As Cayden explains, “We had customers asking to combine filters to identify more people to sell to. This would take minutes or time out before, and now it’s there instantly.”




An example is high\-count queries and large analytical queries. Previously, their database struggled with large\-scale counting tasks, often taking tens of seconds, if not crashing or timing out. With ClickHouse, those same queries — common given the customers Upollo serves, who often have 100 millions users or more — complete in fractions of a second. “What used to be days and days of work, can now be done in an hour or two,” Cayden says. 






![1Blog_Upollo_var2_202411_FNL copy.png](/uploads/1_Blog_Upollo_var2_202411_FNL_copy_588ed73c51.png)


ClickHouse has also simplified Upollo’s data architecture. By consolidating storage, processing, and serving in one platform, they’ve reduced duplication and latency. “It’s a far more efficient setup than managing multiple schemas and syncing across databases,” Cayden says.




Finally, ClickHouse Cloud’s separation of storage and compute has been a “game changer” for Upollo’s cost and workload flexibility, Cayden says. “We can scale up or down as needed, handle batch jobs without impacting production, and avoid the high costs of maintaining a large cluster.” This means Upollo can optimize resources for both performance and budget as their data needs continue to grow.



## Initial hurdles and lessons learned [\#](/blog/upollos-journey-from-bigquery-to-clickhouse#initial-hurdles-and-lessons-learned)



Of course, no migration is without growing pains, and Upollo’s move to ClickHouse brought its own set of challenges. The first of these, Cayden says, was simply the learning curve of understanding a new system. “To get everything we wanted out of ClickHouse, we ended up diving very deep into the code to understand how the product works and how we could get the most out of it,” he says. They've also gotten help from ClickHouse's community, documentation, and support team.




One challenge early on was managing memory to avoid out\-of\-memory (OOM) issues during large queries. “The ClickHouse team has been helpful, giving advice on flags to work around these challenges, making changes to the core product, putting things on the roadmap,” Cayden says. “We still run into OOMs occasionally, but far less frequently than before.”




Around the same time Upollo adopted ClickHouse, they also introduced [dbt](https://clickhouse.com/docs/en/integrations/dbt) (data build tool) to streamline their data workflows. dbt Cloud didn’t support ClickHouse, so the Upollo team created their own tooling to bridge the gap. When they reported a long\-standing bug that was blocking them, the ClickHouse team jumped in the next day to provide a fix.




Throughout the transition, they’ve needed to tune ClickHouse’s various flags and settings to optimize performance. “There are some sharp edges,” Cayden says, noting that running ClickHouse straight out of the box might not always deliver peak performance. But ClickHouse’s team has offered guidance, he says, helping Upollo’s engineers tune the platform to handle their unique, data\-heavy workloads.



## Growing with ClickHouse [\#](/blog/upollos-journey-from-bigquery-to-clickhouse#growing-with-clickhouse)



For anyone considering ClickHouse Cloud, Cayden’s advice is simple: give it a try. “It’s easier than you think to get data across and start playing with it,” he says, adding that ClickHouse’s trial credits make it easy to explore and test the database 




ClickHouse’s open\-source community and comprehensive documentation made Upollo’s transition much smoother. '”There are some incredible resources available,” Cayden says. He also suggests reaching out to the friendly folks at ClickHouse to join beta programs, noting that it's a great way to get early access to new features—”as long as you're comfortable with being on the bleeding\-edge."




With their core data moved over, Cayden and the team look forward to deepening their relationship with ClickHouse by migrating additional workloads and taking advantage of new features like inverted indexes. “Our dream state is for all of our analytical workloads and queries that can run performantly on ClickHouse, be running on Clickhouse,” he says.




For Upollo, the move to ClickHouse has improved cost efficiency and performance, allowing them to scale and deliver predictive insights to customers without the constraints they faced previously. Queries run faster, large data batches are ingested in minutes, and Upollo’s engineers can focus on innovation rather than maintenance. 




“ClickHouse lets us scale in a cost effective way that BigQuery simply couldn’t,” Cayden says. 




To learn more about how ClickHouse can improve the scalability of your data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/docs/en/cloud-quick-start).


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
