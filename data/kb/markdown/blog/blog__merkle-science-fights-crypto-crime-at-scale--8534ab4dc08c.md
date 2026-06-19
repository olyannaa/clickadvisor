# How Merkle Science fights crypto crime at scale with ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Merkle Science fights crypto crime at scale with ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FMerkle_Science_User_Story_Issue_1200_1_2237a4d174.png&w=96&q=75)![](/_next/image?url=%2Fuploads%2FMerkle_Science_User_Story_Issue_1200_8603a63406.png&w=96&q=75)Akshay Gupta, Lead Data Engineer, and Priyanshu Sehgal, Sr. Data EngineerNov 13, 2025 · 7 minutes readStopping crypto crime starts with seeing the whole picture. That’s the philosophy behind [Merkle Science](https://www.merklescience.com/), an AI\-powered blockchain analytics and predictive risk platform that helps regulators, law enforcement agencies, financial institutions, and crypto companies detect, trace, and prevent illicit activity across the Web3 ecosystem.


As blockchain adoption accelerates, the volume and complexity of on\-chain data has never been greater. Every week, Merkle Science ingests around 1\.5 terabytes of data and runs more than 18 million queries. From transaction monitoring and wallet attribution to cross\-chain forensics and ecosystem\-wide threat detection, their ability to scale, move fast, and surface risks in real time depends on having the right data infrastructure.


“Over the years, ClickHouse has become a core part of our architecture,” says Akshay Gupta, lead data engineer at Merkle Science. “A lot of our data sits there. It’s a very critical component.”


We caught up with Akshay and senior data engineer Priyanshu Sehgal to learn how migrating to [ClickHouse Cloud](https://clickhouse.com/cloud) has helped their team move faster, scale more easily, and stay focused on building features that help customers stay ahead of evolving threats.


## The pains of managing infrastructure [\#](/blog/merkle-science-fights-crypto-crime-at-scale#the-pains-of-managing-infrastructure)


When Akshay joined Merkle Science in 2021, the company was already running ClickHouse on their own. They’d been drawn to it as a “hybrid database between OLAP and OLTP,” he explains, capable of handling both point lookups and large\-scale aggregations.


“The latency and performance have been really good with ClickHouse,” he adds. “It hits a sweet spot and means we don’t have to bother with maintaining two databases.”


But while the setup delivered best\-in\-class performance, it came with baggage. What started as a single cluster ballooned into four ClickHouse clusters, three ZooKeeper nodes, and seven VMs. For a small team, keeping all that running was practically a full\-time job.


![Merkle Science User Story Issue 1200 (2).png](/uploads/Merkle_Science_User_Story_Issue_1200_2_3ee70ec7af.png)
*Diagram illustrates Merkle Science’s on\-prem ClickHouse architecture*
“There was always infrastructure anxiety,” Akshay says. “Being a startup and a lean team, we want to focus more on building features, not dealing with infra.”


Even with automation in place, they were spending more time managing clusters and wrangling ZooKeeper than writing code. Storage costs were also a constant stressor. “If I wanted to add a new chain—say, terabytes of additional data—the cost would shoot up,” Akshay says. And scaling wasn’t much easier. “It was technically possible, but painful and way too labor\-intensive.”


By 2023, they were ready for a change. ClickHouse was still the right tool for the job, but they needed a version that could keep up without slowing them down. Thankfully, the perfect managed service [had just hit the market](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year), and it promised an easier ride.


## Smooth sailing to the cloud [\#](/blog/merkle-science-fights-crypto-crime-at-scale#smooth-sailing-to-the-cloud)


In March 2024, the team migrated to [ClickHouse Cloud](https://clickhouse.com/cloud). While the benefits of a managed service were clear—less time managing infrastructure, more time building features—Akshay admits he was skeptical at first. “I thought that because it was backed by S3, performance would take a hit,” he says. “But that was absolutely not the case.”


From day one, the system felt fast and responsive, without the operational overhead they were used to. “Now, if I want to scale up CPU or make other changes, it’s just a few clicks in the ClickHouse Cloud UI,” Akshay says.


Like any migration, it came with a bit of a learning curve. Some patterns from their self\-hosted setup, like manually sharding [distributed tables](https://clickhouse.com/docs/engines/table-engines/special/distributed), didn’t work as expected in the cloud. “We added sharding at first, and the performance wasn’t great,” Priyanshu says. “But once we removed it and let ClickHouse Cloud manage [partitioning](https://clickhouse.com/docs/observability/managing-data) in the background, things improved a lot.”


They also saw some delays with [background merges](https://clickhouse.com/docs/merges) on pre\-aggregated tables, which affected query freshness. But with help from ClickHouse support and documentation, the team quickly adapted. “We can sort these out on the fly,” Priyanshu says.


“It’s been a very smooth ride for us,” Akshay adds. After years of managing everything in\-house, the team finally has peace of mind knowing infrastructure is taken care of.


## More time for what matters [\#](/blog/merkle-science-fights-crypto-crime-at-scale#more-time-for-what-matters)


Sharing their journey to a successful migration at the Open House Bangalore roadshow in October 2025, since moving to ClickHouse Cloud, Merkle Science has seen big\-time improvements in performance, stability, and developer productivity.



Priyanshu highlights data ingestion as a major win. Back in their self\-hosted days, the team had to load CSV or Parquet files one at a time. Loading five terabytes could take upwards of 20 engineer hours. Now, thanks to ClickHouse Cloud’s S3\-backed architecture, those same jobs finish in six to seven hours—more than three times faster—with far less oversight.


“We no longer have employees babysitting the data ingestion process,” Priyanshu says. “That’s a very big productivity boost, because that time can be spent on something more valuable.”


Askhay agrees, noting that the team’s efficiency gains have accelerated development across the board. “We’re shipping things much, much faster because we don’t have to worry about whether things will break or whether the infra will scale,” he says.


ClickHouse Cloud has also made it easier to test and deploy new features. “Previously, we had to contact our DevOps team to create a dev system and test there,” Priyanshu says. “Now it's easy to spin up dev environments and move to production when we’re ready.”


Akshay calls out the UI as another plus, making monitoring simple. “It’s a very, very neat UI,” he says. “I can search by user, check P99s, see where performance bottlenecks are, and debug issues instantly. That’s been a major, major boost for us.”


They’ve also seen smoother background merges for [materialized views](https://clickhouse.com/docs/materialized-views), [simpler backups](https://clickhouse.com/docs/cloud/manage/backups), and easier handling of [MergeTree tables](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree), things that used to require heavy lifting but now run effortlessly in the cloud.


## Innovating without limits [\#](/blog/merkle-science-fights-crypto-crime-at-scale#innovating-without-limits)


With infrastructure off their plate, the Merkle Science team can focus full\-time on building and innovating. Instead of worrying about whether a cluster will scale or a job might fail, they’re channeling that energy into solving problems for customers. “ClickHouse is our go\-to tool for that, because we know its capabilities and how we can leverage it,” Akshay says.


That confidence goes a long way. Since switching to ClickHouse Cloud, Merkle Science’s footprint has grown to around 130 TB of compressed data, with 1\.5 TB being added each week. They’re already running over 18 million queries weekly, and Akshay adds: “That number is only going to rise, because we’re adding more and more features that will rely on ClickHouse.”


As blockchain adoption continues to surge, Akshay knows the team is ready. “Even if data increases by 4x or 5x in the next year, we literally don't have to worry about it. We’ve got the architecture right, the stack right, and the right platform at the end of the day.”

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
