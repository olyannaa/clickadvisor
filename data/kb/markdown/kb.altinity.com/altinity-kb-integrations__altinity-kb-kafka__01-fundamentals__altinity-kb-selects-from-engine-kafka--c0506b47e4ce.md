# SELECTs from engine\=Kafka \| Altinity® Knowledge Base for ClickHouse®


1. [Integrations](/altinity-kb-integrations/)
2. [Kafka engine](/altinity-kb-integrations/altinity-kb-kafka/)
3. [Fundamentals](/altinity-kb-integrations/altinity-kb-kafka/01-fundamentals/)
4. SELECTs from engine\=Kafka
# SELECTs from engine\=Kafka

## Question

What will happen, if we would run SELECT query from working Kafka table with MV attached? Would data showed in SELECT query appear later in MV destination table?

## Answer

1. Most likely SELECT query would show nothing.
2. If you lucky enough and something would show up, those rows **wouldn’t appear** in MV destination table.

So it’s not recommended to run SELECT queries on working Kafka tables.

In case of debug it’s possible to use another Kafka table with different `consumer_group`, so it wouldn’t affect your main pipeline.

Last modified 2026\.03\.12: [Restructure Kafka KB sections and refresh named\-collection guidance (fde5b9e)](https://github.com/Altinity/altinityknowledgebase/commit/fde5b9e9f6579a89f6b9ec2f41821d880733aacb)
