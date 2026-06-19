# ClickHouse Cloud is now in Public Beta


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud is now in Public Beta

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 4, 2022 · 7 minutes read![Cloud beta cover - 2 orbits - 5 elements.png](/uploads/Cloud_beta_cover_2_orbits_5_elements_8b925b27e7.png)
Since inception, ClickHouse has been synonymous with lightning fast query speeds over massive datasets. As the creators of the open source ClickHouse technology, our goal has always been to help our user community to take advantage of this capability with as little friction as possible. This is why we are thrilled to announce the Beta release of ClickHouse Cloud!


We are proud to be one of the fastest\-growing, most\-loved open source projects, and we are seeing an ever\-increasing demand for the unique capabilities of ClickHouse. That is why we wanted to remove any remaining barriers to adoption by offering these capabilities as a serverless product, without any need to manage server infrastructure.


**To get started, simply sign up [here](https://clickhouse.cloud/signUp) for a 14\-day free trial.**


## ClickHouse Cloud [\#](/blog/clickhouse-cloud-public-beta#clickhouse-cloud)


To be able to deliver our vision of a cloud native, seamlessly scalable, easy\-to\-use analytical database, we’ve been working on bringing new innovations to the ClickHouse Cloud experience. Some examples include:


- Developing flexible scaling of both compute and storage by decoupling them.
- Negating the need for tedious re\-architecture by using optimized object storage as primary storage.
- Improving performance and mitigating latency with multi\-level caching.
- Improving cost efficiency with higher data compression by default.


ClickHouse Cloud drastically simplifies the use of ClickHouse for developers, data engineers and analysts, allowing them to start building instantly without having to size and scale their cluster. And they only pay for what they use, while at the same time taking advantage of the best price / performance ratio in the industry.


![cloud.png](/uploads/cloud_d553eb32e5.png)
Let’s dig into some of our favorite benefits of ClickHouse Cloud.


### Simplicity [\#](/blog/clickhouse-cloud-public-beta#simplicity)


One of the reasons the ClickHouse self\-managed database became so popular was the simplicity and ease with which anyone could get started. Downloading a binary and running it is essentially all that is needed to start using the open source software. And because of its performance, many users are content with keeping a single server of ClickHouse running. With ClickHouse Cloud, we have continued our commitment to simplicity for any user, be they operators, developers or analysts.


It starts with providing an intuitive user interface where a user can provision ClickHouse Cloud services within minutes. This serverless offering doesn't require any input in regards to server size, number or topology. That work is done by ClickHouse Cloud and abstracted away from the user.


![create_simple_service.gif](/uploads/create_simple_service_191f14bb20.gif)
Once a service is up and running, administrative tasks such as upgrades and load balancing are done automatically and seamlessly in ClickHouse Cloud, simplifying the life of administrators. Our innovative use of S3 object storage as the primary storage in ClickHouse Cloud allows much more flexibility when increasing capacity. The task of re\-architecting server specifications and setups is no longer necessary when using ClickHouse Cloud.


To put it very simply: **It just works.**


### Efficiency [\#](/blog/clickhouse-cloud-public-beta#efficiency)


The vast majority of analytical workloads have a choppy utilization: high inserts and query loads at certain times of the day with significantly lower load otherwise. The periods between changes in demand are typically too short for an administrator to manually tune the provisioned servers. This results in resources sitting idle most of the time, leading to unnecessary spend.


This is why ClickHouse Cloud automatically scales resources up, down and even pauses services depending on demand, maximizing resource efficiency. Our separation of compute and storage means we can provision the specific resource needed in a certain situation, rather than having to over\-provision a full server to serve the increase in demand in one area. It is also worth noting that our use of object storage as the primary storage has a big impact on the cost efficiency of the service, especially when serving large datasets.


Our [pricing model](https://clickhouse.com/pricing) also reflects this commitment to efficiency: you only pay for work done, not idle resources. Reducing wasted resources is also an environmental benefit, which is taking on a growing importance for us and many of our customers who are looking to reduce their carbon footprint where they can.


### Security [\#](/blog/clickhouse-cloud-public-beta#security)


ClickHouse Cloud was built with a security\-first philosophy that permeates the whole platform. This “secure by default” mindset means that ClickHouse Cloud generates secure passwords and enforces IP filtering by default. A security team is constantly monitoring and evaluating security threats, dedicated to ensuring the protection and integrity of our customer’s data.


In addition, the platform has strong authentication and role\-based access control, including federated authentication via Google. It employs strong encryption at rest and in transit, and strong network access controls, including support for AWS PrivateLink, and provides activity and audit logging.


We have already acquired accreditations such as SOC 2 Type I, with SOC 2 Type II in progress. ClickHouse Cloud is also GDPR and CCPA compliant.


### Ecosystem [\#](/blog/clickhouse-cloud-public-beta#ecosystem)


ClickHouse Cloud has the ability to seamlessly interact with other systems, such as data sources, user interfaces, and programming languages, often with the simplicity of a few clicks in our Cloud Console. Building on the top of a solid open\-source base, we are making significant investments developing and maintaining a strategic set of integrations, and have an active partnership with many key vendors in our ecosystem to help them integrate with our platform. Our incredible community is also full of organizations and individuals who are developing and publishing their own ways of interacting with ClickHouse.


At Beta launch, we have curated a list of ClickHouse Integrations available in our Cloud Console that include:




| Data Ingestion | Data Visualization | Language Client | SQL Client |
| --- | --- | --- | --- |
| S3 | Grafana | Go | ClickHouse Client |
| Kafka | HEX | Python | DataGrip |
| DBT | Superset | Java | DBeaver |
| Airbyte | Deepnote | Node.js | Arctype |





The full list with more details about the categories and support levels is available in [our public documentation](https://clickhouse.com/docs/en/integrations/).


![s3-integration.gif](/uploads/s3_integration_1bb489af2a.gif)
### Speed [\#](/blog/clickhouse-cloud-public-beta#speed)


ClickHouse is known for its query speed, especially with massive and quickly growing data volumes. Therefore it was incredibly important to us that ClickHouse Cloud deliver the speed that our users expect, even with all of the additional benefits described above.


The early results from our own benchmarking exercises are public and can be found [here](https://benchmark.clickhouse.com/). The ability to tune and adjust certain elements of the cloud platform means that this aspect of ClickHouse Cloud will see continuous improvement, but even now we are seeing near parity with a well\-tuned ClickHouse self\-managed database with most types of queries. The added latency introduced by using object storage fades into insignificance with complex queries, while being mitigated by the advanced multi\-level caching capabilities built into ClickHouse Cloud.


We believe that ClickHouse Cloud offers the best price to performance ratio in the industry through these efficiency gains and broadly maintained query and data load speeds.


## Try it out for free [\#](/blog/clickhouse-cloud-public-beta#try-it-out-for-free)


**To get started, simply sign up [here](https://clickhouse.cloud/signUp) for a 14\-day free trial.**


## Additional resources [\#](/blog/clickhouse-cloud-public-beta#additional-resources)


- ClickHouse Cloud [Compatibility Guide](https://clickhouse.com/docs/en/whats-new/cloud-compatibility): See what the differences are between self\-managed ClickHouse and ClickHouse Cloud
- Connect with us: Join the ClickHouse community in [Slack.](https://clickhousedb.slack.com/join/shared_invite/zt-1gh9ds7f4-PgDhJAaF8ad5RbWBAAjzFg)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
