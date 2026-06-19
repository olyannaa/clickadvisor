# Roaring bitmaps for calculating retention \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Roaring bitmaps for calculating retention
# Roaring bitmaps for calculating retention


```
CREATE TABLE test_roaring_bitmap
ENGINE = MergeTree
ORDER BY h AS
SELECT
    intDiv(number, 5) AS h,
    groupArray(toUInt16(number - (2 * intDiv(number, 5)))) AS vals,
    groupBitmapState(toUInt16(number - (2 * intDiv(number, 5)))) AS vals_bitmap
FROM numbers(40)
GROUP BY h

SELECT
    h,
    vals,
    hex(vals_bitmap)
FROM test_roaring_bitmap

┌─h─┬─vals─────────────┬─hex(vals_bitmap)─────────┐
│ 0 │ [0,1,2,3,4]      │ 000500000100020003000400 │
│ 1 │ [3,4,5,6,7]      │ 000503000400050006000700 │
│ 2 │ [6,7,8,9,10]     │ 000506000700080009000A00 │
│ 3 │ [9,10,11,12,13]  │ 000509000A000B000C000D00 │
│ 4 │ [12,13,14,15,16] │ 00050C000D000E000F001000 │
│ 5 │ [15,16,17,18,19] │ 00050F001000110012001300 │
│ 6 │ [18,19,20,21,22] │ 000512001300140015001600 │
│ 7 │ [21,22,23,24,25] │ 000515001600170018001900 │
└───┴──────────────────┴──────────────────────────┘

SELECT
    groupBitmapAnd(vals_bitmap) AS uniq,
    bitmapToArray(groupBitmapAndState(vals_bitmap)) AS vals
FROM test_roaring_bitmap
WHERE h IN (0, 1)

┌─uniq─┬─vals──┐
│    2 │ [3,4] │
└──────┴───────┘

```
See also [A primer on roaring bitmaps](https://vikramoberoi.com/a-primer-on-roaring-bitmaps-what-they-are-and-how-they-work/)

Last modified 2024\.02\.01: [Fixed broken links, other housekeeping (33dff8b)](https://github.com/Altinity/altinityknowledgebase/commit/33dff8b40c62828a1baf7b31d3a22f87a0950e8c)
