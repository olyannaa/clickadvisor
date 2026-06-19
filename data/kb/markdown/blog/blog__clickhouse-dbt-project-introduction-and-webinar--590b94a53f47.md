# ClickHouse and dbt \- A Gift from the Community


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse and dbt \- A Gift from the Community

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 1, 2023 · 11 minutes read![dbt_clickhouse.png](/uploads/DBT_Post_0e9aeb08ea.png)
## Introduction [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#introduction)


As a company dedicated to the ethos of open\-source, it is important that we accept not only requests from the community but also features and new integrations.


Last week we [delivered a webinar](https://www.youtube.com/watch?v=16VBGdNuHv8) on such a project \- the [`dbt-clickhouse`](https://github.com/ClickHouse/dbt-clickhouse) plugin.


Initially created by a community contributor to address their needs and released in the spirit of OSS, this plugin has seen increasing adoption as users utilize dbt's capabilities with ClickHouse.


In this blog post, we explore dbt, the value it potentially brings when combined with ClickHouse, and a small tale of evolving support for more advanced capabilities leveraging new capabilities recently released in ClickHouse.


## What is dbt? [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#what-is-dbt)


**dbt** (data build tool) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles materializing these select statements into objects in the database in the form of tables and views \- performing the T of [Extract Load and Transform (ELT)](https://en.wikipedia.org/wiki/Extract,_load,_transform). Users can create a model defined by a SELECT statement.


Within dbt, these models can be cross\-referenced and layered to allow the construction of higher\-level concepts. The boilerplate SQL required to connect models is automatically generated. Furthermore, dbt identifies dependencies between models and ensures they are created in the appropriate order using a directed acyclic graph (DAG).


In summary, users can define a model representing a concept, e.g., a summary of actor appearances **as SQL**. These models can then be materialized\* as either views or tables. These models can then be combined to produce more complex models.


In our recent webinar, we presented the following data schema for IMDB movie data. From this, we utilize dbt to create two models: one summarizing directors and another providing an overview of every actor, e.g., the number of movie appearances, their average rating, the director they have mostly worked with, etc. In this case, the actor's model is dependent on the director's model. dbt allows these models to be defined as SQL statements, with a Jinja templating language to connect and reference them. Note how some data sources aren’t even in ClickHouse, with the movie\_genres and movie\_director tables in S3 and Postgres respectively. This final model is then represented in ClickHouse as either a view or table named `actor_summary`.


![model.png](/uploads/model_76d75387fd.png)
## How is this supported in ClickHouse? [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#how-is-this-supported-in-clickhouse)


dbt supports an [adapter plugin API](https://docs.getdbt.com/guides/dbt-ecosystem/adapter-development/1-what-are-adapters) to allow users to connect to data platforms that are not included in the [core offering](https://docs.getdbt.com/docs/supported-data-platforms). In [early 2021](https://sql.clickhouse.com?query_id=9YHSK62D6WHC5ARCBOJEO7) a member of the ClickHouse community, [Dmitriy Sokolov](https://github.com/silentsokolov), [created a plugin](https://github.com/clickHouse/dbt-clickhouse) to support ClickHouse for his requirements and kindly open\-sourced his work. In response to growing adoption and a little [over a year later](https://sql.clickhouse.com?query_id=1IXC5PU4QCXSH5DHGQRU6F), this project was transferred to ClickHouse and officially made a vendor\-supported plugin. We continue to invest in this plugin to support the dbt latest features and utilize the best practices of ClickHouse to expose this functionality.


We test this plugin rigorously against ClickHouse Cloud and ensure the [current dbt plugin test](https://docs.getdbt.com/guides/dbt-ecosystem/adapter-development/4-testing-a-new-adapter) suite passes.


## How is it useful to ClickHouse users? [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#how-is-it-useful-to-clickhouse-users)


We primarily see users using dbt with ClickHouse for a number of tasks:


- Data analysts serving requests for views on the data, e.g., to the business for BI purposes or data scientists who need a specific view for their latest model. It is essential to manage these views and models and ensure they are tracked, minimized, tested, documented, and versioned.
- Users have data in various systems, such as Postgres, MySQL, and S3, and wish to model these data as a set of tables or views in ClickHouse. Using ClickHouse’s table functions and engines, users create dbt models to manage this data migration process. They, in turn, benefit from dbt representing these data integration tasks as code which can then be versioned, documented, and tested \- again using dbt features.
- User’s often need to [migrate data from other OLTP databases](https://clickhouse.com/blog/migrating-data-between-clickhouse-postgres), such as Postgres, to ClickHouse to serve real\-time analytical workloads. In simple cases, this can be achieved using native [ClickHouse table functions](https://clickhouse.com/docs/en/sql-reference/table-functions/). However, ClickHouse tables represented by many source tables subject to updates typically require [Change data capture processes](https://www.striim.com/blog/change-data-capture-cdc-what-it-is-and-how-it-works/). Dbt can assist with the [management and modeling](https://davidsj.substack.com/p/data-activated) of the queries required in this process.
- Users may alternatively need to track changes to rows in ClickHouse \- a form of change capture\- to answer questions concerning a former state in the database. Dbt offers features [such as incremental models and snapshots](https://docs.getdbt.com/blog/change-data-capture) that can assist with these requirements.


## Model types [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#model-types)


The process of persisting the results of a model’s SQL query is known as “materializing the model”. Models can be materialized in a number of ways. The `clickhouse-dbt` plugin ensures this is achieved using the most appropriate ClickHouse functionality and best practices:


- **[View Materialization](https://docs.getdbt.com/docs/build/materializations#view)** \- the simplest and default approach. Here the model is simply created in ClickHouse using the [CREATE VIEW AS](https://clickhouse.com/docs/en/sql-reference/statements/create/view/#normal-view) as syntax. Changes to the model cause the view to be recreated when dbt is run.
- **[Table Materialization](https://docs.getdbt.com/docs/build/materializations#table)**\- The results from the model’s SQL query are streamed into a new table with the appropriate schema, using the [`INSERT INTO table SELECT &lt;model_query>`](https://clickhouse.com/docs/en/sql-reference/statements/insert-into/#inserting-the-results-of-select) statement. The user pays the storage cost of representing the model as a table for the benefit of improved performance.
- **[Incremental materialization](https://docs.getdbt.com/docs/build/incremental-models)**\- Provides a means to materialize a model as a table but maintain updates. Subsequent runs of the model identify changes in the source data using a unique key field and condition (e.g., based on a timestamp), and ensure this is reflected in the target table in ClickHouse. This is extremely powerful for the event\-type data associated with ClickHouse.
- **[Ephemeral materialization](https://docs.getdbt.com/docs/build/materializations#ephemeral)** \- Represents the model as a CTE, which can then be referenced in other models.


Models of different types can be combined to produce more complex models, allowing component [parts to be tested](https://docs.getdbt.com/docs/build/tests) and [documented](https://docs.getdbt.com/docs/collaborate/documentation). A simple table materialization for the actors model, as used on the webinar, is shown below:



```
{{ config(order_by='director_id', engine='MergeTree()', materialized='table') }}


WITH directors AS (
   SELECT directors.id as director_id, movie_id, first_name, last_name FROM {{ source('imdb', 'movie_directors') }} OUTER JOIN {{ source('imdb', 'directors') }} ON {{ source('imdb', 'movie_directors') }}.director_id = {{ source('imdb', 'directors') }}.id
)

select *
from directors

```

For further details, see the [webinar recording](https://www.youtube.com/watch?v=16VBGdNuHv8) or our [documentation](https://clickhouse.com/docs/en/integrations/dbt/dbt-intro), which contains similar examples.


## Recent developments [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#recent-developments)


Incremental materializations represent the most complex model type to implement in ClickHouse. Historically ClickHouse has had only limited support for updates and deletes in the form of asynchronous [mutations](https://clickhouse.com/docs/en/operations/system-tables/mutations/). These need to be [used carefully](https://clickhouse.com/docs/en/cloud/bestpractices/avoid-mutations/) since they rewrite all of the affected data parts and can be extremely IO\-intensive as a result.


![model-update.png](/uploads/model_update_663c7ca903.png)
Suppose we have an original table, `X`, which represents a materialized model. To implement the incremental semantics required by dbt, `dbt-clickhouse`, by default, creates a new temporary table `T` with the new records identified by a condition the user specifies e.g. `select max(updated_at) from {{this}}`. A new table, `N`, is then created with the same schema as the original. Data is streamed into table `N` from the original table, using an `INSERT INTO SELECT` with a check to ensure the records aren't in `T`. Finally, we stream the records from `T` into `N` and do an atomic table exchange with `X` and `N` to expose the new realized model. This is visualized below:


![incremental-old-generic.png](/uploads/incremental_old_generic_b5b954c847.png)
While this approach works, it involves a complete duplication of the data being created for each dbt run and capture of the changes. Ideally, we would avoid this overhead and only write the new record,s. The above process is complicated as it supports duplicates and updates in the source data. If the user is comfortable with handling duplicates themselves in ClickHouse or is confident their source data is immutable and append\-only, the incremental model can be [configured to use an `append-only` strategy](https://github.com/ClickHouse/dbt-clickhouse#the-append-strategy). In this case, the changes are simply identified in the source data and streamed directly into the existing table, as shown below


While improving the situation for a subset of cases, we remain dissatisfied with the current solution for the case where duplicates were a possibility. Fortunately, in 22\.8 ClickHouse added [lightweight deletes](https://clickhouse.com/docs/en/sql-reference/statements/delete/) as an experimental feature. Lightweight deletes are significantly faster than `ALTER TABLE ... DELETE` operations because they don't require rewriting ClickHouse data parts. “Tombstones” are simply added to deleted rows which allow records to be automatically excluded at query time. These deleted records are, in turn, merged away during normal merge processes. Armed with deletes that don’t consume as much IO and threaten cluster stability, we could add a new approach known as `delete+insert` to incremental materializations.


In summary, this approach:


1. Creates a temporary table `T`. Rows that have changed are streamed into this table. A `DELETE` is issued against the current table `X`, deleting rows by id based on the values in `T`.
2. The rows from `T` are inserted into the current table `X` using an `INSERT INTO X SELECT * FROM T`.


We visualize this below:


![incremental-new-generic.png](/uploads/incremental_new_generic_8dd05c2454.png)
Our testing suggests this approach performs significantly better than the "legacy" strategy. However, there are important caveats to using this strategy:


- The setting `allow_experimental_lightweight_delete` must be enabled on your ClickHouse server or included in the custom\_settings for your ClickHouse profile.
- As suggested by the setting name, lightweight delete functionality is still experimental and is not quite considered production\-ready, so usage should be limited to datasets that are easily recreated.
- This strategy operates directly on the affected table/relation (without creating any intermediate or temporary tables), so if there is an issue during the operation, the data in the incremental model is likely to be in an invalid state


While the first two of these issues are likely to be addressed soon with lightweight deletes expected to GA soon, the latter requires further development work. What about transactions, you say? Well, that's a good idea…


## Conclusions [\#](/blog/clickhouse-dbt-project-introduction-and-webinar#conclusions)


In this post, we have introduced dbt and the ClickHouse plugin. We have covered the value of dbt to ClickHouse users and discussed some of the key features before presenting recent developments based on new capabilities in ClickHouse. For more details, we recommend the [recent webinar](https://www.youtube.com/watch?v=16VBGdNuHv8) and examples in [our documentation](https://clickhouse.com/docs/en/integrations/dbt/dbt-intro). Happy modeling.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
