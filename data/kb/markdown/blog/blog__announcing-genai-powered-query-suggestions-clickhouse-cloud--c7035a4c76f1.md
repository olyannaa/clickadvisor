# Announcing GenAI powered query suggestions in ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing GenAI powered query suggestions in ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 25, 2023 · 4 minutes read

We are pleased to announce the general availability of GenAI\-powered query suggestions in the ClickHouse Cloud query console. Users of ClickHouse Cloud can now write queries as natural language questions and leave the query console to convert these to SQL queries based on the context of the available tables.
Generative AI and Large Language Models (LLM) are a hot topic of late. Many of us will have used services, such as ChatGPT, to make our daily working practices more efficient. The emergence of these technologies has no less impacted the work of a data analyst, engineer, or database administrator. While the ability for LLMs to write SQL has been known for some time, services such as ChatGPT can be imprecise and prone to generate less than correct queries unless provided with context. By integrating ChatGPT APIs directly into Cloud’s SQL console, we are to provide the tables and their respective schemas as context to any query \- thus improving the accuracy and usefulness of responses.


Users of all levels of SQL experience can benefit from this feature. As well as lowering the barrier for non\-technical users to write queries against ClickHouse, experienced SQL experts can improve their productivity and utilize the query assistant to provide the basis for complex questions or just syntax they can’t quite remember :)


An an example, consider the following table schema from our commonly used [UK house price paid dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid):



```
CREATE TABLE default.uk_price_paid ( 
  `price` UInt32, 
  `date` Date, 
  `postcode1` LowCardinality(String), 
  `postcode2` LowCardinality(String), 
  `type` Enum8('other' = 0, 'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4), 
  `is_new` UInt8, 
  `duration` Enum8('unknown' = 0, 'freehold' = 1, 'leasehold' = 2), 
  `addr1` String, 
  `addr2` String, 
  `street` LowCardinality(String), 
  `locality` LowCardinality(String), 
  `town` LowCardinality(String), 
  `district` LowCardinality(String), 
  `county` LowCardinality(String) 
) ENGINE = MergeTree()
ORDER BY (postcode1, postcode2, addr1, addr2)

```

Let’s say we want to run a year\-by\-year analysis of transaction volume and value on this table. We can simply enter a prompt like:



> Show me the total price and total number of all uk\_price\_paid transactions by year


As we can see, the LLM returns a valid query:


![gpt-generated-query.png](/uploads/gpt_generated_query_b7a0b7f501.png)
While query suggestions may not always be perfect, they can still provide the basis from which a user can iterate. As well as providing the ability to write queries from just a description, the service also provides a quick means to correct queries \- fixing syntax based on the context of the error provided by ClickHouse.


Consider the following:



```
SELECT
    startOfYear(date) as year,
    countIf(price < 1000000) as small_transactions,
    countIf(price >= 1000000) as large_transactions
FROM uk_price_paid
WHERE
    twon = 'LONDON'
GROUP BY
    year
ORDER BY
    year ASC

```

This query has a couple of different issues \- `startOfYear` is not a valid ClickHouse function and `twon` is a typo (should be `town`). Running this query will throw an error:


![query_error.png](/uploads/query_error_76fa58481d.png)
In\-line with the error message, we can click the ‘Fix query’ button to ask the LLM for help debugging this query:


![query_error_fix_gpt.png](/uploads/query_error_fix_gpt_12111708b1.png)
From the diff, we can see that the LLM has correctly identified and fixed both issues in this query. Simply click ‘Apply’ to commit the changes and re\-run the query:


![fixed_query.png](/uploads/fixed_query_c6d630a3e4.png)
Try our new GenAI\-powered query suggestions in ClickHouse Cloud today. [Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=twitter&utm_medium=social&utm_campaign=meetup&ajs_aid=d24c2cdc-82e6-4a23-9b40-e11da125c86d) today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](https://clickhouse.com/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](https://clickhouse.com/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
