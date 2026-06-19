# arrayFold \| Altinity® Knowledge Base for ClickHouse®


1. [Functions](/altinity-kb-functions/)
2. arrayFold
# arrayFold

## EWMA example


```
WITH
    [40, 45, 43, 31, 20] AS data,
    0.3 AS alpha
SELECT arrayFold((acc, x) -> arrayPushBack(acc, (alpha * x) + ((1 - alpha) * (acc[-1]))), arrayPopFront(data), [CAST(data[1], 'Float64')]) as ewma

┌─ewma─────────────────────────────────────────────────────────────┐
│ [40,41.5,41.949999999999996,38.66499999999999,33.06549999999999] │
└──────────────────────────────────────────────────────────────────┘

```
Last modified 2023\.11\.04: [Create arrayfold.md (03db46b)](https://github.com/Altinity/altinityknowledgebase/commit/03db46b3b728f6ad98371b360170ba325d5601ba)
