---
source: blog
url: https://clickhouse.com/blog/clickhouse-cloud-public-beta
topic: clickhouse-cloud-is-now-generally-available
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

get started, go to the [ClickHouse Cloud AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-jettukeanwrfc). When you subscribe to the AWS Marketplace, you get $300 in free credits towards your usage. ![GA_aws_marketplace.png](/uploads/GA_aws_marketplace_8f4c0a08f3.png) ## Development and Production Services designed for your use case [\#](/blog/clickhouse-cloud-generally-available#development-and-production-services-designed-for-your-use-case)

ClickHouse Cloud is always deployed in a redundant manner to ensure that your analytical data is highly available and secure. We run a typical production\-level service across three availability zones and take care to ensure high availability during auto\-scaling, idle/resume, and ClickHouse version upgrade operations.

However, we recognize that for some use cases, users are looking for simplified services that are more cost\-effective. In addition to robust production\-level services, the GA release introduces Development services – still highly available and redundant, but fixed\-capacity, deployed on leaner hardware and across two availability zones instead of three.

Development services cost less than $200/mo for the most widely used AWS regions, and a lot less for intermittent development workloads that are automatically idled by ClickHouse Cloud. With this new offering, ClickHouse Cloud users can now much more effectively architect, model, and experiment with ClickHouse Cloud until they are ready to deploy the solution in production.

Check out our [pricing page](https://clickhouse.com/pricing) or simply spin up a Development service in your cloud console to find out more.

![GA_dev_pricing.png](/uploads/GA_dev_pricing_7082cab390.png)
## Interactive SQL console for ClickHouse Cloud users [\#](/blog/clickhouse-cloud-generally-available#interactive-sql-console-for-clickhouse-cloud-users)

ClickHouse has a great command\-line client used and loved by many. However, we know that many users prefer to use a GUI instead of a terminal.

For the ClickHouse Cloud GA release, we are also launching the new SQL console, a fully\-featured workbench for ClickHouse Cloud. This UI enables database schema browsing, interactive SQL queries, auto\-complete, query history and sharing, basic visualizations, and more!

The new SQL console makes it easy to learn, manage, and use ClickHouse all from your web browser.

![GA_sql_console.png](/uploads/GA_sql_console_4ea474d5a1.png)
## ClickHouse Academy [\#](/blog/clickhouse-cloud-generally-available#clickhouse-academy)

In the spirit of helping even more users learn how to use ClickHouse to unlock the potential of their analytical datasets, we are launching ClickHouse Academy, a self\-paced learning center for ClickHouse. This offering includes courses that are available for free to everyone.

Visit the ClickHouse Academy [catalog](http://learn.clickhouse.com/visitor_class_catalog) to view our free on\-demand courses, and also recordings of previous live deliveries of our onboarding workshops.

![GA_academy.png](/uploads/GA_academy_c379fc9a73.png)
## New and improved integrations [\#](/blog/clickhouse-cloud-generally-available#new-and-improved-integrations)
