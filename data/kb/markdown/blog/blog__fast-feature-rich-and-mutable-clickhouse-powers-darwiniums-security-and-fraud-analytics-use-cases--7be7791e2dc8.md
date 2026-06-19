# Fast, Feature Rich and Mutable : ClickHouse Powers Darwinium's Security and Fraud Analytics Use Cases


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Fast, Feature Rich and Mutable : ClickHouse Powers Darwinium's Security and Fraud Analytics Use Cases

![darwiniumlogo.png](/_next/image?url=%2Fuploads%2Fdarwiniumlogo_9bec4fbbe4.png&w=96&q=75) Ananth GundabattulaJul 27, 2022 · 15 minutes read*We’d like to welcome Darwinium as a guest to our blog. Read on to find out how Darwinium is using ClickHouse and, most importantly, why they chose ClickHouse as their database engine.*


## What is Darwinium? [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#what-is-darwinium)


Darwinium is a digital risk platform that supports real time journey orchestration and continuous adaptive trust for digital user authentication. It was built to tackle complex business problems as they happen, adapting to adversaries regardless of how quickly they attack. The platform is designed for developers and data scientists to test, model and deploy with ease, regardless of business processes or organisational constraints.


Darwinium Integrates with your Content Delivery Network (CDN) or Proxy as a Darwinium\-hosted solution, or optional one\-click install onto a new or existing Kubernetes cluster.


## Challenges for the Security and Fraud Domain [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#challenges-for-the-security-and-fraud-domain)


Dealing with Cyber Security and Fraud domains, Darwinium needed capabilities to:


**Ingest and process data at a high throughput:**


- Having a database backend that can handle high throughput (and fast) writes is a fundamental requirement. Additionally, having the capability to serve this data for analysis as soon as the data is ingested is an expectation from digital driven workloads of today and the future.


**Deal with large volumes of data:**


- Darwinium is built from the ground up on the construct of a journey; wherein there is a continuous monitoring of the digital asset. This results in large volumes of data because the Darwinium real time engine needs to continuously profile and monitor a digital asset. The database needs to be capable of analysing data at scale. Additionally, question of scale also arises from the need that an entire year's worth of data may need to be processed. As an example, a year's worth of data needs to be queried to look at the behaviour of a single credit card. Another use case could be for an account administrator to analyse years worth of data to understand the outliers of all logins to the website.
- Technical types of fraud and security challenges, including malware, remote desktop and bots are highly forensic in nature, requiring storing most digital datapoints that are available on a journey step for future investigations that only then pinpoint the patterns that help to detect that threat.
- Darwinium emphasises the importance of continuously profiling and monitoring of digital journeys for comprehensive view of user intent. That results in a many\-one relationship between the records of storage needed for every journey completed. Additionally, some types of fraud such as account takeover, scams and social engineering require long timeframe periods of ‘normal’ behavioural data to compare against the interactions now to detect changes. Storing multi\-step journey data and long timeframe data means increase in number of records and storage needed.
- The result is lots of data: both from the amount of data stored per record, many to one relationship of records stored to journey conducted and long timeframes of lookback needed for investigations.


**Have capabilities to analyse data in a complex way:**


- The nature of analysing fraudulent data requires complex interactive analysis. Having a feature rich, analytical capabilities stack makes a lot of difference; thus translating to reduced human costs. Having a database system that can respond in timeframes of 1 second or less, and at the same time provide a feature rich functional toolbox is a really compelling use case that modern database systems need to support.


## Why did Darwinium Choose ClickHouse? [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#why-did-darwinium-choose-clickhouse)


Darwinium assessed a few solutions before finally landing on ClickHouse as the choice of database engine. There are a few reasons that led to this decision.


The following sections use a hypothetical database table called events to denote an event in the digital journey of an end user. A row in this table represents all the attributes collected for a given interaction in the digital journey. Examples of attributes that an event can include are the device fingerprint, city from which the event was generated and so on.


## Simpler Data Pipelines [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#simpler-data-pipelines)


### Mutable Engine leads to a simpler data pipeline [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#mutable-engine-leads-to-a-simpler-data-pipeline)


Mutable database engines really simplify the data ingestion pipeline complexity. While immutable storage file systems like HDFS and the query processing engines that can execute on top of these immutable storage layers have their strengths, they do introduce additional implementation complexity when data pipelines need to be designed and implemented for mutable data processing patterns.


Let us take the example of ingesting data within a time window of 5 seconds after it is generated in a messaging/ queuing system. We are talking about the need for a cyber security analyst/fraud analyst to see the details of all login attempts not later than 5 seconds after the event is generated. Using an immutable storage file system would mean: to “ingest” the data into a file starting with a “.” extension at the beginning, ingest the streaming data and close the file after the time window elapsed. Finally the file needs to be renamed to a valid file name so that it can be considered by the query processing engine. This operation has to be taken care of across all data partitions that the pipeline needs to maintain for a single table.


With ClickHouse, the data pipeline logic is simplified, and is only dealing with the “streaming” aspect of the write as opposed to all of these complexities. ClickHouse thus enables a simpler write design pattern just like any other new age data lake systems like Hudi etc. but with a more simplistic developer experience.


### Choice of table engine leads to simpler data pipelines [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#choice-of-table-engine-leads-to-simpler-data-pipelines)


To serve data summaries for an analyst who is interested in looking at aggregates, various implementation patterns are adopted in today's lakehouse architectures. The approach ClickHouse takes to solve for patterns like aggregates is simple yet powerful.


Let us take the need to summarise data at regular time windows of 5 minutes for each city. One can define a City Entity aggregation summary table using an AggregatingMergeTree Engine that can “listen” to changes in the “events” table and accumulate and summarise the City summaries for the time grain that the aggregation can be arrived at. This radically simplifies the data ingestion logic as we are able to do away with a need for a separate data pipeline for creating aggregated summaries (so that aggregates are served faster as opposed to a full table scan). The data pipeline could then focus on writing data to the “events” table only and a “CitySummary” table would be available for analysis as managed by ClickHouse.


## High Throughput Writes with Consistent Very Low CPU Core Readings [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#high-throughput-writes-with-consistent-very-low-cpu-core-readings)


A digital risk engine like Darwinium can process a few thousand writes per second per installation. On top of this, Darwinium had a wide table approach for each digital interaction. Darwinium collects a few thousand attributes per event that is captured in each interaction of a digital journey. A single ClickHouse server could easily handle a few thousand writes per second, with multiple data pipeline writers writing to a single ClickHouse server at any given instant. Moreover, the ClickHouse server side metrics showed a consistent and very low (\<5%) user space and system space core usage while the write operations alone were being executed. This leaves ample CPU allocation for query processing workloads.


ClickHouse was therefore very well suited for write\-heavy workloads commonly associated with the security and fraud domain use cases.


## Support for Complex Data Types [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#support-for-complex-data-types)


Some of the data points collected per event by the Darwinium real time engine in the digital interaction required a map data structure representation. An example of such a map is the set of signals generated by the models that are executed in a given digital interaction. Darwinium analytic use cases require that an analyst needs capabilities to generate fine grained query filter expressions while analysing digital interactions. As an example, a query expression might involve looking at the distribution counts of the signals for a particular cohort of digital interaction types. If it were not a map data structure and the query ability on top of this map data structure thereof, we would need as many columns as the number of possible signals that could be generated (as each signal is specific to the model that was executed in that particular digital interaction.) Maps and arrays thus became a fundamental requirement for us to build upon for interactive analytics. ClickHouse is a pleasure to interact with, providing support for complex data types and the query expressions that can be executed using these data structures.


Fraud and Security, more than most industries is expected to experience a high churn of models, risk assessments and signals generated. These change dynamically from month to month to cater to business goals and evolving threats. A data storage solution needs to be able to deal with these changing configurations in a way that doesn’t require breaking queries, and adding to or overloading an existing schema. The ClickHouse Map and Array data types are ideal candidates for storing the state and outputs of these types of risk assessments. The richness of the associated functions on these data points provides the analytical power needed to interpret and monitor these important outputs, in a way that often negates the need for seperate downstream processing using more analytical oriented languages eg. Python.


The recent addition of JSON type support took this a step further when it came to the analytics requirements of Darwinium. Having a mechanism to have a “schema on read” pattern helps build a multi\-tenanted setup of the Darwinium analytics components, by using a JSON column type for some of the digital interaction events.


## Cost Aware Storage patterns [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#cost-aware-storage-patterns)


While the expectations from the digital systems of today are becoming more demanding in terms of latencies and query capabilities, so is the expectation that the cost to run is as small as possible. In particular, the security and fraud data analysis use cases align with the principle of diminishing interest. As the lifetime of an event in digital interaction grows older, so is the need for analysing it. Of course there would be the occasional need to analyse the entire year's worth of data but that probably will not be a continuous requirement.


ClickHouse supports the concept of tumbling data retention windows where “hot” data can be initially placed on a fast access medium like a local SSD, with the ability to subsequently move the data to a relatively slower but cheaper storage system like S3 (and is a matter of configuring the right data retention policy at the table level).


## Cloud Native [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#cloud-native)


No new age digital platform can claim to be a complete solution offering without having capabilities to deploy and run in at least one of the major cloud vendors. Darwinium is no exception to this thinking.


Besides being Cloud Native, there is the additional need to deploy Darwinium stack in an on\-premise or even a developers laptop. The fact that ClickHouse can be run from a low end laptop or an on\-premise cluster of nodes or on any of the myriad hardware configurations possible even on a single cloud provider like AWS enabled Darwinium deployment use cases in a big way.


Some of the other aspects that makes ClickHouse a cloud native offering for Darwinium use cases are:


- Support S3 (in case of AWS) as a disk type.
- Ability to configure a metadata path (and cacheable metadata path) shows the amount of design thinking that went into making ClickHouse Cloud Native.
- Mange how secrets like AWS credentials are configurable when using an S3 disk (AWS as an example cloud provider).
- The Darwinium team was able to install, configure and upgrade ClickHouse by using Kubernetes ecosystem tooling like Replicated.


The ClickHouse cloud service offering that is shortly being released as a turn key solution takes this a step further. All the complexities of managing a ClickHouse instance are greatly simplified; becoming as simple as configuring the write or read API endpoint and then simply to start using it.


## Distributed \& Highly Available [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#distributed--highly-available)


Fraud and security use cases generate information that essentially cannot be stored on a single node. Also it would be more advantageous to process a query in the most parallel way possible. ClickHouse can utilise all of the cores available on a single node that it is running on to process a query. In addition the data for a single table can be sharded across multiple nodes. This helps Darwinium use cases to process as many queries as possible using the maximum possible compute power available, by using all cores in a given cluster of nodes.


Replicating the data as the data gets ingested results in providing a higher level uptime for Darwinium customers. This aspect significantly reduced the risk of an AWS node inadvertently getting shut down and thus losing all of the data hosted on its local SSD. Replication thus allowed for a lower risk on a cloud construct as well as providing for distributing the query processing workloads.


## Rich Function Catalogue [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#rich-function-catalogue)


While having a distributed compute paradigm is advantageous, having a rich number of functions further augments these advantages, and drastically reduces the time taken by a security or a fraud analyst to arrive at analytical conclusions. The catalogue of functions that are available for collections like Arrays and Maps, User defined functions and also the concept of lambdas, offer new ways to analyse data on cyber security and fraud data sets.


## SQL as a Simpler Interface [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#sql-as-a-simpler-interface)


While there are database/search systems that can index data, having a system that provides SQL as the interface to analyse and query data makes a lot of difference. Darwinium allows analysts to build custom data analysis views and charts using a jupyter notebook experience in addition to forensics dashboards and interactive analyses screens. SQL, which is one of the well known and proven “languages”, is thus a compelling querying interface to enable such custom data analysis use cases.


Here is a pictorial representation of the latencies of queries run on a 40M entries dataset on a single node hosting a very wide table of approximately 3k columns. Here are some comments on the chart below:


- The queries involve a group by expression over randomly chosen columns.
- The readings are taken when there are only a couple of analyst queries running in parallel shown as “lower loads”, between a couple and less than 10 parallel running analyst queries as “medium loads” and more than 10 as “Very high loads”.
- Note that the first cell is the readings from a cold state of the dataset i.e. the dataset is being hit for the first time and absolutely no caches were involved.
- The first row represents the SQL query when 5 filter expressions were part of the SQL query, second row when there are 6 filter expressions with one complex data type and the third row when there are 7 columns that include two complex data types.
- Please note that the y\-axis scale is not the same across all these 3 rows of data. Each column represents the time range that was used to filter the data on before applying the query filters.


![DarwiniumStats.png](/uploads/Darwinium_Stats_52acf5144d.png)
## Conclusion [\#](/blog/fast-feature-rich-and-mutable-clickhouse-powers-darwiniums-security-and-fraud-analytics-use-cases#conclusion)


After analysing a few other database systems and weighing up the pros and cons of each, the Darwinium team chose ClickHouse as the database engine of choice to power its interactive analytics use cases for fraud and cybersecurity analysts. In essence, it is a database system of choice because ClickHouse is:


- Fast (lower latency and high throughput ingest).
- Flexible, with cost aware deployment models.
- Rich in capabilities.
- Cloud\-ready
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
