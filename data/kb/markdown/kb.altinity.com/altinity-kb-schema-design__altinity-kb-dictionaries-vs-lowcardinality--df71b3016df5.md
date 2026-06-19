# Dictionaries vs LowCardinality \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. Dictionaries vs LowCardinality
# Dictionaries vs LowCardinality

Q. I think I’m still trying to understand how de\-normalized is okay \- with my relational mindset, I want to move repeated string fields into their own table, but I’m not sure to what extent this is necessary

I will look at LowCardinality in more detail \- I think it may work well here

A. If it’s a simple repetition, which you don’t need to manipulate/change in future \- LowCardinality works great, and you usually don’t need to increase the system complexity by introducing dicts.

For example: name of team ‘Manchester United’ will rather not be changed, and even if it will you can keep the historical records with historical name. So normalization here (with some dicts) is very optional, and de\-normalized approach with LowCardinality is good \& simpler alternative.

From the other hand: if data can be changed in future, and that change should impact the reports, then normalization may be a big advantage.

For example if you need to change the used currency rare every day\- it would be quite stupid to update all historical records to apply the newest exchange rate. And putting it to dict will allow to do calculations with latest exchange rate at select time.

For dictionary it’s possible to mark some of the attributes as injective. An attribute is called injective if different attribute values correspond to different keys. It would allow ClickHouse® to replace dictGet call in GROUP BY with cheap dict key.

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
