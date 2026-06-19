# Functions \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-functions/).

# Functions

Functions- 1: [How to encode/decode quantileTDigest states from/to list of centroids](#pg-8901f0b065e0c2cb123803963861d889)
- 2: [kurt \& skew statistical functions in ClickHouse®](#pg-7250ae06848201dd66b3d1120acb0617)
- 3: [\-Resample vs \-If vs \-Map vs Subquery](#pg-b63886f284d8b3200aea9f257cdaca75)
- 4: [arrayFold](#pg-8cd28090a9cdcc63e22d6415102aa754)
- 5: [arrayMap, arrayJoin or ARRAY JOIN memory usage](#pg-464994dc1bdb85d8fd4bcbdd730b4d52)
- 6: [assumeNotNull and friends](#pg-2cc9e1d2bd4b6d913b761f34cd6e3368)
- 7: [Encrypt](#pg-5c6a1f4be6e0f269ae12da9c83e22c70)
- 8: [sequenceMatch](#pg-3b69ced4615b965e64b9829d0ce3226f)

# 1 \- How to encode/decode quantileTDigest states from/to list of centroids

A way to export or import quantileTDigest states from/into ClickHouse®## quantileTDigestState

quantileTDigestState is stored in two parts: a count of centroids in LEB128 format \+ list of centroids without a delimiter. Each centroid is represented as two Float32 values: Mean \& Count.


```
SELECT
    hex(quantileTDigestState(1)),
    hex(toFloat32(1))

┌─hex(quantileTDigestState(1))─┬─hex(toFloat32(1))─┐
│ 010000803F0000803F           │ 0000803F          │
└──────────────────────────────┴───────────────────┘
  01          0000803F      0000803F
  ^           ^             ^
  LEB128      Float32 Mean  Float32 Count

```
We need to make two helper `UDF` functions:


```
cat /etc/clickhouse-server/decodeTDigestState_function.xml
<yandex>
  <function>
    <type>executable</type>
    <execute_direct>0</execute_direct>
    <name>decodeTDigestState</name>
    <return_type>Array(Tuple(mean Float32, count Float32))</return_type>
    <argument>
      <type>AggregateFunction(quantileTDigest, UInt32)</type>
    </argument>
    <format>RowBinary</format>
    <command>cat</command>
    <send_chunk_header>0</send_chunk_header>
  </function>
</yandex>

cat /etc/clickhouse-server/encodeTDigestState_function.xml
<yandex>
  <function>
    <type>executable</type>
    <execute_direct>0</execute_direct>
    <name>encodeTDigestState</name>
    <return_type>AggregateFunction(quantileTDigest, UInt32)</return_type>
    <argument>
      <type>Array(Tuple(mean Float32, count Float32))</type>
    </argument>
    <format>RowBinary</format>
    <command>cat</command>
    <send_chunk_header>0</send_chunk_header>
  </function>
</yandex>

```
Those UDF – `(encode/decode)TDigestState` converts `TDigestState` to the `Array(Tuple(Float32, Float32))` and back.


```
SELECT quantileTDigest(CAST(number, 'UInt32')) AS result
FROM numbers(10)

┌─result─┐
│      4 │
└────────┘

SELECT decodeTDigestState(quantileTDigestState(CAST(number, 'UInt32'))) AS state
FROM numbers(10)

┌─state─────────────────────────────────────────────────────────┐
│ [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1)] │
└───────────────────────────────────────────────────────────────┘

SELECT finalizeAggregation(encodeTDigestState(CAST('[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1)]', 'Array(Tuple(Float32, Float32))'))) AS result

┌─result─┐
│      4 │
└────────┘

```
# 2 \- kurt \& skew statistical functions in ClickHouse®

How to make them return the same result like python scipy
```
from scipy.stats import skew, kurtosis

# Creating a dataset

dataset = [10,17,71,6,55,38,27,61,48,46,21,38,2,67,35,77,29,31,27,67,81,82,75,81,31,38,68,95,37,34,65,59,81,28,82,80,35,3,97,42,66,28,85,98,45,15,41,61,24,53,97,86,5,65,84,18,9,32,46,52,69,44,78,98,61,64,26,11,3,19,0,90,28,72,47,8,0,74,38,63,88,43,81,61,34,24,37,53,79,72,5,77,58,3,61,56,1,3,5,61]

print(skew(dataset, axis=0, bias=True), skew(dataset))

# -0.05785361619432152 -0.05785361619432152

```

```
WITH arrayJoin([10,17,71,6,55,38,27,61,48,46,21,38,2,67,35,77,29,31,27,67,81,82,75,81,31,38,68,95,37,34,65,59,81,28,82,80,35,3,97,42,66,28,85,98,45,15,41,61,24,53,97,86,5,65,84,18,9,32,46,52,69,44,78,98,61,64,26,11,3,19,0,90,28,72,47,8,0,74,38,63,88,43,81,61,34,24,37,53,79,72,5,77,58,3,61,56,1,3,5,61]) AS value
SELECT skewPop(value) AS ex_1

┌──────────────────ex_1─┐
│ -0.057853616194321014 │
└───────────────────────┘

```

```
print(skew(dataset, bias=False))

# -0.05873838908626328

```

```
WITH arrayJoin([10, 17, 71, 6, 55, 38, 27, 61, 48, 46, 21, 38, 2, 67, 35, 77, 29, 31, 27, 67, 81, 82, 75, 81, 31, 38, 68, 95, 37, 34, 65, 59, 81, 28, 82, 80, 35, 3, 97, 42, 66, 28, 85, 98, 45, 15, 41, 61, 24, 53, 97, 86, 5, 65, 84, 18, 9, 32, 46, 52, 69, 44, 78, 98, 61, 64, 26, 11, 3, 19, 0, 90, 28, 72, 47, 8, 0, 74, 38, 63, 88, 43, 81, 61, 34, 24, 37, 53, 79, 72, 5, 77, 58, 3, 61, 56, 1, 3, 5, 61]) AS value
SELECT
    skewSamp(value) AS ex_1,
    (pow(count(), 2) * ex_1) / ((count() - 1) * (count() - 2)) AS G

┌─────────────────ex_1─┬────────────────────G─┐
│ -0.05698798509149213 │ -0.05873838908626276 │
└──────────────────────┴──────────────────────┘

```

```
print(kurtosis(dataset, bias=True, fisher=False), kurtosis(dataset, bias=True, fisher=True), kurtosis(dataset))

# 1.9020275610791184 -1.0979724389208816 -1.0979724389208816

```

```
WITH arrayJoin([10, 17, 71, 6, 55, 38, 27, 61, 48, 46, 21, 38, 2, 67, 35, 77, 29, 31, 27, 67, 81, 82, 75, 81, 31, 38, 68, 95, 37, 34, 65, 59, 81, 28, 82, 80, 35, 3, 97, 42, 66, 28, 85, 98, 45, 15, 41, 61, 24, 53, 97, 86, 5, 65, 84, 18, 9, 32, 46, 52, 69, 44, 78, 98, 61, 64, 26, 11, 3, 19, 0, 90, 28, 72, 47, 8, 0, 74, 38, 63, 88, 43, 81, 61, 34, 24, 37, 53, 79, 72, 5, 77, 58, 3, 61, 56, 1, 3, 5, 61]) AS value
SELECT
    kurtPop(value) AS pearson,
    pearson - 3 AS fisher

┌────────────pearson─┬──────────────fisher─┐
│ 1.9020275610791124 │ -1.0979724389208876 │
└────────────────────┴─────────────────────┘

```

```
print(kurtosis(dataset, bias=False))

# -1.0924286152713967

```

```
WITH arrayJoin([10, 17, 71, 6, 55, 38, 27, 61, 48, 46, 21, 38, 2, 67, 35, 77, 29, 31, 27, 67, 81, 82, 75, 81, 31, 38, 68, 95, 37, 34, 65, 59, 81, 28, 82, 80, 35, 3, 97, 42, 66, 28, 85, 98, 45, 15, 41, 61, 24, 53, 97, 86, 5, 65, 84, 18, 9, 32, 46, 52, 69, 44, 78, 98, 61, 64, 26, 11, 3, 19, 0, 90, 28, 72, 47, 8, 0, 74, 38, 63, 88, 43, 81, 61, 34, 24, 37, 53, 79, 72, 5, 77, 58, 3, 61, 56, 1, 3, 5, 61]) AS value
SELECT
    kurtSamp(value) AS ex_1,
    (((pow(count(), 2) * (count() + 1)) / (((count() - 1) * (count() - 2)) * (count() - 3))) * ex_1) - ((3 * pow(count() - 1, 2)) / ((count() - 2) * (count() - 3))) AS G

┌──────────────ex_1─┬───────────────────G─┐
│ 1.864177212613638 │ -1.0924286152714027 │
└───────────────────┴─────────────────────┘

```
[Google Collab](https://colab.research.google.com/drive/1xoWNi7QAJ9XZtCbmQqJFB8Z_mCreITPW?usp=sharing)

# 3 \- \-Resample vs \-If vs \-Map vs Subquery

### 5 categories


```
SELECT sumResample(0, 5, 1)(number, number % 5) AS sum
FROM numbers_mt(1000000000)

┌─sum───────────────────────────────────────────────────────────────────────────────────────────┐
│ [99999999500000000,99999999700000000,99999999900000000,100000000100000000,100000000300000000] │
└───────────────────────────────────────────────────────────────────────────────────────────────┘

1 rows in set. Elapsed: 1.010 sec. Processed 1.00 billion rows, 8.00 GB (990.20 million rows/s., 7.92 GB/s.)


SELECT sumMap([number % 5], [number]) AS sum
FROM numbers_mt(1000000000)

┌─sum─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ([0,1,2,3,4],[99999999500000000,99999999700000000,99999999900000000,100000000100000000,100000000300000000]) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

1 rows in set. Elapsed: 5.730 sec. Processed 1.00 billion rows, 8.00 GB (174.51 million rows/s., 1.40 GB/s.)

SELECT sumMap(map(number % 5, number)) AS sum
FROM numbers_mt(1000000000)

┌─sum─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ {0:99999999500000000,1:99999999700000000,2:99999999900000000,3:100000000100000000,4:100000000300000000} │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘

1 rows in set. Elapsed: 4.169 sec. Processed 1.00 billion rows, 8.00 GB (239.89 million rows/s., 1.92 GB/s.)

SELECT
    sumIf(number, (number % 5) = 0) AS sum_0,
    sumIf(number, (number % 5) = 1) AS sum_1,
    sumIf(number, (number % 5) = 2) AS sum_2,
    sumIf(number, (number % 5) = 3) AS sum_3,
    sumIf(number, (number % 5) = 4) AS sum_4
FROM numbers_mt(1000000000)

┌─────────────sum_0─┬─────────────sum_1─┬─────────────sum_2─┬──────────────sum_3─┬──────────────sum_4─┐
│ 99999999500000000 │ 99999999700000000 │ 99999999900000000 │ 100000000100000000 │ 100000000300000000 │
└───────────────────┴───────────────────┴───────────────────┴────────────────────┴────────────────────┘

1 rows in set. Elapsed: 0.762 sec. Processed 1.00 billion rows, 8.00 GB (1.31 billion rows/s., 10.50 GB/s.)

SELECT sumMap([id], [sum]) AS sum
FROM
(
    SELECT
        number % 5 AS id,
        sum(number) AS sum
    FROM numbers_mt(1000000000)
    GROUP BY id
)

┌─sum─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ([0,1,2,3,4],[99999999500000000,99999999700000000,99999999900000000,100000000100000000,100000000300000000]) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.331 sec. Processed 1.00 billion rows, 8.00 GB (3.02 billion rows/s., 24.15 GB/s.)

```
### 20 categories


```
SELECT sumResample(0, 20, 1)(number, number % 20) AS sum
FROM numbers_mt(1000000000)

1 rows in set. Elapsed: 1.056 sec. Processed 1.00 billion rows, 8.00 GB (947.28 million rows/s., 7.58 GB/s.)

SELECT sumMap([number % 20], [number]) AS sum
FROM numbers_mt(1000000000)

1 rows in set. Elapsed: 6.410 sec. Processed 1.00 billion rows, 8.00 GB (156.00 million rows/s., 1.25 GB/s.)

SELECT sumMap(map(number % 20, number)) AS sum
FROM numbers_mt(1000000000)

┌─sum────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ {0:24999999500000000,1:24999999550000000,2:24999999600000000,3:24999999650000000,4:24999999700000000,5:24999999750000000,6:24999999800000000,7:24999999850000000,8:24999999900000000,9:24999999950000000,10:25000000000000000,11:25000000050000000,12:25000000100000000,13:25000000150000000,14:25000000200000000,15:25000000250000000,16:25000000300000000,17:25000000350000000,18:25000000400000000,19:25000000450000000} │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

1 rows in set. Elapsed: 4.629 sec. Processed 1.00 billion rows, 8.00 GB (216.04 million rows/s., 1.73 GB/s.)

SELECT
    sumIf(number, (number % 5) = 0) AS sum_0,
    sumIf(number, (number % 5) = 1) AS sum_1,
    sumIf(number, (number % 5) = 2) AS sum_2,
    sumIf(number, (number % 5) = 3) AS sum_3,
    sumIf(number, (number % 5) = 4) AS sum_4,
    sumIf(number, (number % 5) = 5) AS sum_5,
    sumIf(number, (number % 5) = 6) AS sum_6,
    sumIf(number, (number % 5) = 7) AS sum_7,
    sumIf(number, (number % 5) = 8) AS sum_8,
    sumIf(number, (number % 5) = 9) AS sum_9,
    sumIf(number, (number % 5) = 10) AS sum_10,
    sumIf(number, (number % 5) = 11) AS sum_11,
    sumIf(number, (number % 5) = 12) AS sum_12,
    sumIf(number, (number % 5) = 13) AS sum_13,
    sumIf(number, (number % 5) = 14) AS sum_14,
    sumIf(number, (number % 5) = 15) AS sum_15,
    sumIf(number, (number % 5) = 16) AS sum_16,
    sumIf(number, (number % 5) = 17) AS sum_17,
    sumIf(number, (number % 5) = 18) AS sum_18,
    sumIf(number, (number % 5) = 19) AS sum_19
FROM numbers_mt(1000000000)

1 rows in set. Elapsed: 5.282 sec. Processed 1.00 billion rows, 8.00 GB (189.30 million rows/s., 1.51 GB/s.)

SELECT sumMap([id], [sum]) AS sum
FROM
(
    SELECT
        number % 20 AS id,
        sum(number) AS sum
    FROM numbers_mt(1000000000)
    GROUP BY id
)

1 rows in set. Elapsed: 0.362 sec. Processed 1.00 billion rows, 8.00 GB (2.76 billion rows/s., 22.10 GB/s.)

SELECT sumMap(map(id, sum)) AS sum
FROM
(
    SELECT
        number % 20 AS id,
        sum(number) AS sum
    FROM numbers_mt(1000000000)
    GROUP BY id
)

```
### sumMapResample

It’s also possible to combine them.


```
SELECT
    day,
    category_id,
    sales
FROM
(
    SELECT sumMapResample(1, 31, 1)([category_id], [sales], day) AS res
    FROM
    (
        SELECT
            number % 31 AS day,
            100 * (number % 11) AS category_id,
            number AS sales
        FROM numbers(10000)
    )
)
ARRAY JOIN
    res.1 AS category_id,
    res.2 AS sales,
    arrayEnumerate(res.1) AS day

┌─day─┬─category_id──────────────────────────────────┬─sales──────────────────────────────────────────────────────────────────────────┐
│   1 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [143869,148365,142970,147465,142071,146566,151155,145667,150225,144768,149295] │
│   2 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [149325,143898,148395,142999,147494,142100,146595,151185,145696,150255,144797] │
│   3 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [144826,149355,143927,148425,143028,147523,142129,146624,151215,145725,150285] │
│   4 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [150315,144855,149385,143956,148455,143057,147552,142158,146653,151245,145754] │
│   5 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [145783,150345,144884,149415,143985,148485,143086,147581,142187,146682,151275] │
│   6 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [151305,145812,150375,144913,149445,144014,148515,143115,147610,142216,146711] │
│   7 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [146740,151335,145841,150405,144942,149475,144043,148545,143144,147639,142245] │
│   8 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [142274,146769,151365,145870,150435,144971,149505,144072,148575,143173,147668] │
│   9 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [147697,142303,146798,151395,145899,150465,145000,149535,144101,148605,143202] │
│  10 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [143231,147726,142332,146827,151425,145928,150495,145029,149565,144130,148635] │
│  11 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [148665,143260,147755,142361,146856,151455,145957,150525,145058,149595,144159] │
│  12 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [144188,148695,143289,147784,142390,146885,151485,145986,150555,145087,149625] │
│  13 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [149655,144217,148725,143318,147813,142419,146914,151515,146015,150585,145116] │
│  14 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [145145,149685,144246,148755,143347,147842,142448,146943,151545,146044,150615] │
│  15 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [150645,145174,149715,144275,148785,143376,147871,142477,146972,151575,146073] │
│  16 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [146102,150675,145203,149745,144304,148815,143405,147900,142506,147001,151605] │
│  17 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [151635,146131,150705,145232,149775,144333,148845,143434,147929,142535,147030] │
│  18 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [147059,141665,146160,150735,145261,149805,144362,148875,143463,147958,142564] │
│  19 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [142593,147088,141694,146189,150765,145290,149835,144391,148905,143492,147987] │
│  20 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [148016,142622,147117,141723,146218,150795,145319,149865,144420,148935,143521] │
│  21 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [143550,148045,142651,147146,141752,146247,150825,145348,149895,144449,148965] │
│  22 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [148995,143579,148074,142680,147175,141781,146276,150855,145377,149925,144478] │
│  23 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [144507,149025,143608,148103,142709,147204,141810,146305,150885,145406,149955] │
│  24 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [149985,144536,149055,143637,148132,142738,147233,141839,146334,150915,145435] │
│  25 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [145464,150015,144565,149085,143666,148161,142767,147262,141868,146363,150945] │
│  26 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [150975,145493,150045,144594,149115,143695,148190,142796,147291,141897,146392] │
│  27 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [146421,151005,145522,150075,144623,149145,143724,148219,142825,147320,141926] │
│  28 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [141955,146450,151035,145551,150105,144652,149175,143753,148248,142854,147349] │
│  29 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [147378,141984,146479,151065,145580,150135,144681,149205,143782,148277,142883] │
│  30 │ [0,100,200,300,400,500,600,700,800,900,1000] │ [142912,147407,142013,146508,151095,145609,150165,144710,149235,143811,148306] │
└─────┴──────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────┘

```
# 4 \- arrayFold

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
# 5 \- arrayMap, arrayJoin or ARRAY JOIN memory usage

Why do arrayMap, arrayFilter, and arrayJoin use so much memory?## arrayMap\-like functions memory usage calculation.

In order to calculate arrayMap or similar array\* functions ClickHouse® temporarily does arrayJoin\-like operation, which in certain conditions can lead to huge memory usage for big arrays.

So for example, you have 2 columns:


```
SELECT *
FROM
(
    SELECT
        [1, 2, 3, 4, 5] AS array_1,
        [1, 2, 3, 4, 5] AS array_2
)

┌─array_1─────┬─array_2─────┐
│ [1,2,3,4,5] │ [1,2,3,4,5] │
└─────────────┴─────────────┘

```
Let’s say we want to multiply array elements at corresponding positions.


```
SELECT arrayMap(x -> ((array_1[x]) * (array_2[x])), arrayEnumerate(array_1)) AS multi
FROM
(
    SELECT
        [1, 2, 3, 4, 5] AS array_1,
        [1, 2, 3, 4, 5] AS array_2
)

┌─multi─────────┐
│ [1,4,9,16,25] │
└───────────────┘

```
ClickHouse create temporary structure in memory like this:


```
SELECT
    array_1,
	array_2,
    x
FROM
(
    SELECT
        [1, 2, 3, 4, 5] AS array_1,
        [1, 2, 3, 4, 5] AS array_2
)
ARRAY JOIN arrayEnumerate(array_1) AS x

┌─array_1─────┬─array_2─────┬─x─┐
│ [1,2,3,4,5] │ [1,2,3,4,5] │ 1 │
│ [1,2,3,4,5] │ [1,2,3,4,5] │ 2 │
│ [1,2,3,4,5] │ [1,2,3,4,5] │ 3 │
│ [1,2,3,4,5] │ [1,2,3,4,5] │ 4 │
│ [1,2,3,4,5] │ [1,2,3,4,5] │ 5 │
└─────────────┴─────────────┴───┘

```
We can roughly estimate memory usage by multiplying the size of columns participating in the lambda function by the size of the unnested array.

And total memory usage will be 55 values (5(array size)\*2(array count)\*5(row count) \+ 5(unnested array size)), which is 5\.5 times more than initial array size.


```
SELECT groupArray((array_1[x]) * (array_2[x])) AS multi
FROM
(
    SELECT
        array_1,
        array_2,
        x
    FROM
    (
        SELECT
            [1, 2, 3, 4, 5] AS array_1,
            [1, 2, 3, 4, 5] AS array_2
    )
ARRAY JOIN arrayEnumerate(array_1) AS x
)

┌─multi─────────┐
│ [1,4,9,16,25] │
└───────────────┘

```
But what if we write this function in a more logical way, so we wouldn’t use any unnested arrays in lambda.


```
SELECT arrayMap((x, y) -> (x * y), array_1, array_2) AS multi
FROM
(
    SELECT
        [1, 2, 3, 4, 5] AS array_1,
        [1, 2, 3, 4, 5] AS array_2
)

┌─multi─────────┐
│ [1,4,9,16,25] │
└───────────────┘

```
ClickHouse create temporary structure in memory like this:


```
SELECT
    x,
    y
FROM
(
    SELECT
        [1, 2, 3, 4, 5] AS array_1,
        [1, 2, 3, 4, 5] AS array_2
)
ARRAY JOIN
    array_1 AS x,
    array_2 AS y

┌─x─┬─y─┐
│ 1 │ 1 │
│ 2 │ 2 │
│ 3 │ 3 │
│ 4 │ 4 │
│ 5 │ 5 │
└───┴───┘

```
We have only 10 values, which is no more than what we have in initial arrays.


```
SELECT groupArray(x * y) AS multi
FROM
(
    SELECT
        x,
        y
    FROM
    (
        SELECT
            [1, 2, 3, 4, 5] AS array_1,
            [1, 2, 3, 4, 5] AS array_2
    )
ARRAY JOIN
        array_1 AS x,
        array_2 AS y
)

┌─multi─────────┐
│ [1,4,9,16,25] │
└───────────────┘

```
The same approach can be applied to other array\* function with arrayMap\-like capabilities to use lambda functions and ARRAY JOIN (arrayJoin).

## Examples with bigger arrays:


```
SET max_threads=1;
SET send_logs_level='trace';

SELECT arrayMap(x -> ((array_1[x]) * (array_2[x])), arrayEnumerate(array_1)) AS multi
FROM
(
    WITH 100 AS size
    SELECT
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_1,
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_2
    FROM numbers(100000000)
)
FORMAT `Null`

<Debug> MemoryTracker: Current memory usage (for query): 8.13 GiB. 

size=100, (2*size)*size = 2*(size^2)

Elapsed: 24.879 sec. Processed 524.04 thousand rows, 4.19 MB (21.06 thousand rows/s., 168.51 KB/s.)

SELECT arrayMap(x -> ((array_1[x]) * (array_2[x])), arrayEnumerate(array_1)) AS multi
FROM
(
    WITH 100 AS size
    SELECT
        materialize(CAST(range(2*size), 'Array(UInt32)')) AS array_1,
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_2
    FROM numbers(100000000)
)
FORMAT `Null`

<Debug> MemoryTracker: Current memory usage (for query): 24.28 GiB.

size=100, (3*size)*2*size = 6*(size^2)

Elapsed: 71.547 sec. Processed 524.04 thousand rows, 4.19 MB (7.32 thousand rows/s., 58.60 KB/s.)


SELECT arrayMap(x -> ((array_1[x]) * (array_2[x])), arrayEnumerate(array_1)) AS multi
FROM
(
    WITH 100 AS size
    SELECT
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_1,
        materialize(CAST(range(2*size), 'Array(UInt32)')) AS array_2
    FROM numbers(100000000)
)
FORMAT `Null`


<Debug> MemoryTracker: Current memory usage (for query): 12.19 GiB.

size=100, (3*size)*size = 3*(size^2)

Elapsed: 36.777 sec. Processed 524.04 thousand rows, 4.19 MB (14.25 thousand rows/s., 113.99 KB/s.)

```
Which data types we have in those arrays?


```
WITH 100 AS size
SELECT
    toTypeName(materialize(CAST(range(size), 'Array(UInt32)'))) AS array_1,
    toTypeName(materialize(CAST(range(2 * size), 'Array(UInt32)'))) AS array_2,
    toTypeName(arrayEnumerate(materialize(CAST(range(size), 'Array(UInt32)')))) AS x

┌─array_1───────┬─array_2───────┬─x─────────────┐
│ Array(UInt32) │ Array(UInt32) │ Array(UInt32) │
└───────────────┴───────────────┴───────────────┘

```
So each value use 4 bytes.

By default ClickHouse execute query by blocks of 65515 rows (`max_block_size` setting value)

Lets estimate query total memory usage given previous calculations.


```
WITH
    100 AS size,
    4 AS value_size,
    65515 AS max_block_size
SELECT
    array_1_multiplier,
    array_2_multiplier,
    formatReadableSize(((value_size * max_block_size) * ((array_1_multiplier * size) + (array_2_multiplier * size))) * (array_1_multiplier * size) AS estimated_memory_usage_bytes) AS estimated_memory_usage,
    real_memory_usage,
    round(estimated_memory_usage_bytes / (real_memory_usage * 1073741824), 2) AS ratio
FROM
(
    WITH arrayJoin([(1, 1, 8.13), (2, 1, 24.28), (1, 2, 12.19)]) AS tpl
    SELECT
        tpl.1 AS array_1_multiplier,
        tpl.2 AS array_2_multiplier,
        tpl.3 AS real_memory_usage
)

┌─array_1_multiplier─┬─array_2_multiplier─┬─estimated_memory_usage─┬─real_memory_usage─┬─ratio─┐
│                  1 │                  1 │ 4.88 GiB               │              8.13 │   0.6 │
│                  2 │                  1 │ 14.64 GiB              │             24.28 │   0.6 │
│                  1 │                  2 │ 7.32 GiB               │             12.19 │   0.6 │
└────────────────────┴────────────────────┴────────────────────────┴───────────────────┴───────┘

```
Correlation is pretty clear.

What if we will reduce size of blocks used for query execution?


```
SET max_block_size = '16k';

SELECT arrayMap(x -> ((array_1[x]) * (array_2[x])), arrayEnumerate(array_1)) AS multi
FROM
(
    WITH 100 AS size
    SELECT
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_1,
        materialize(CAST(range(2 * size), 'Array(UInt32)')) AS array_2
    FROM numbers(100000000)
)
FORMAT `Null`

<Debug> MemoryTracker: Current memory usage (for query): 3.05 GiB.

Elapsed: 35.935 sec. Processed 512.00 thousand rows, 4.10 MB (14.25 thousand rows/s., 113.98 KB/s.)

```
Memory usage down in 4 times, which has strong correlation with our change: 65k \-\> 16k \~ 4 times.


```
SELECT arrayMap((x, y) -> (x * y), array_1, array_2) AS multi
FROM
(
    WITH 100 AS size
    SELECT
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_1,
        materialize(CAST(range(size), 'Array(UInt32)')) AS array_2
    FROM numbers(100000000)
)
FORMAT `Null`

<Debug> MemoryTracker: Peak memory usage (for query): 226.04 MiB.

Elapsed: 5.700 sec. Processed 11.53 million rows, 92.23 MB (2.02 million rows/s., 16.18 MB/s.)

```
Almost 100 times faster than first query!

# 6 \- assumeNotNull and friends

assumeNotNull and friends`assumeNotNull` result is implementation specific:


```
WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(column + 999) AS x;

┌─column─┬─x─┐
│   null │ 0 │
└────────┴───┘

WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(materialize(column) + 999) AS x;

┌─column─┬───x─┐
│   null │ 999 │
└────────┴─────┘

CREATE TABLE test_null
(
    `key` UInt32,
    `value` Nullable(String)
)
ENGINE = MergeTree
ORDER BY key;

INSERT INTO test_null SELECT
    number,
    concat('value ', toString(number))
FROM numbers(4);

SELECT *
FROM test_null;

┌─key─┬─value───┐
│   0 │ value 0 │
│   1 │ value 1 │
│   2 │ value 2 │
│   3 │ value 3 │
└─────┴─────────┘

ALTER TABLE test_null
    UPDATE value = NULL WHERE key = 3;

SELECT *
FROM test_null;

┌─key─┬─value───┐
│   0 │ value 0 │
│   1 │ value 1 │
│   2 │ value 2 │
│   3 │ null    │
└─────┴─────────┘

SELECT
    key,
    assumeNotNull(value)
FROM test_null;

┌─key─┬─assumeNotNull(value)─┐
│   0 │ value 0              │
│   1 │ value 1              │
│   2 │ value 2              │
│   3 │ value 3              │
└─────┴──────────────────────┘

WITH CAST(NULL, 'Nullable(Enum8(\'a\' = 1, \'b\' = 0))') AS test
SELECT assumeNotNull(test)

┌─assumeNotNull(test)─┐
│ b                   │
└─────────────────────┘

WITH CAST(NULL, 'Nullable(Enum8(\'a\' = 1))') AS test
SELECT assumeNotNull(test)

Error on processing query 'with CAST(null, 'Nullable(Enum8(\'a\' = 1))') as test
select assumeNotNull(test); ;':
Code: 36, e.displayText() = DB::Exception: Unexpected value 0 in enum, Stack trace (when copying this message, always include the lines below):

```
#### Info

Null values in ClickHouse® are stored in a separate dictionary: is this value Null. And for faster dispatch of functions there is no check on Null value while function execution, so functions like plus can modify internal column value (which has default value). In normal conditions it’s not a problem because on read attempt, ClickHouse first would check the Null dictionary and return value from column itself for non\-Nulls only. And `assumeNotNull` function just ignores this Null dictionary. So it would return only column values, and in certain cases it’s possible to have unexpected results.If it’s possible to have Null values, it’s better to use `ifNull` function instead.


```
SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(ifNull(toNullable(number), 0))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 0.705 sec. Processed 1.00 billion rows, 8.00 GB (1.42 billion rows/s., 11.35 GB/s.)

SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(coalesce(toNullable(number), 0))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 2.383 sec. Processed 1.00 billion rows, 8.00 GB (419.56 million rows/s., 3.36 GB/s.)

SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(assumeNotNull(toNullable(number)))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 0.051 sec. Processed 1.00 billion rows, 8.00 GB (19.62 billion rows/s., 156.98 GB/s.)

SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(toNullable(number))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 0.050 sec. Processed 1.00 billion rows, 8.00 GB (20.19 billion rows/s., 161.56 GB/s.)

```
#### Info

There is no overhead for `assumeNotNull` at all.# 7 \- Encrypt

## WHERE over encrypted column


```
CREATE TABLE encrypt
(
    `key` UInt32,
    `value` FixedString(4)
)
ENGINE = MergeTree
ORDER BY key;

INSERT INTO encrypt SELECT
    number,
    encrypt('aes-256-ctr', reinterpretAsString(number + 0.3), 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx')
FROM numbers(100000000);

SET max_threads = 1;

SELECT count()
FROM encrypt
WHERE value IN encrypt('aes-256-ctr', reinterpretAsString(toFloat32(1.3)), 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx')

┌─count()─┐
│       1 │
└─────────┘

1 rows in set. Elapsed: 0.666 sec. Processed 100.00 million rows, 400.01 MB (150.23 million rows/s., 600.93 MB/s.)


SELECT count()
FROM encrypt
WHERE reinterpretAsFloat32(encrypt('aes-256-ctr', value, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxx')) IN toFloat32(1.3)

┌─count()─┐
│       1 │
└─────────┘

1 rows in set. Elapsed: 8.395 sec. Processed 100.00 million rows, 400.01 MB (11.91 million rows/s., 47.65 MB/s.)

```
#### Info

Because encryption and decryption can be expensive due re\-initialization of keys and iv, usually it make sense to use those functions over literal values instead of table column.# 8 \- sequenceMatch

sequenceMatch## Question

I expect the sequence here to only match once as a is only directly after a once \- but it matches with gaps. Why is that?


```
SELECT sequenceCount('(?1)(?2)')(sequence, page ILIKE '%a%', page ILIKE '%a%') AS sequences
  FROM values('page String, sequence UInt16', ('a', 1), ('a', 2), ('b', 3), ('b', 4), ('a', 5), ('b', 6), ('a', 7))

2 # ??

```
## Answer

`sequenceMatch` just ignores the events which don’t match the condition. Check that:


```
SELECT sequenceMatch('(?1)(?2)')(sequence,page='a',page='b') AS sequences　FROM values( 'page String, sequence UInt16' , ('a', 1), ('c',2), ('b', 3));
1 # ??

SELECT sequenceMatch('(?1).(?2)')(sequence,page='a',page='b') AS sequences　FROM values( 'page String, sequence UInt16' , ('a', 1), ('c',2), ('b', 3));
0 # ???

SELECT sequenceMatch('(?1)(?2)')(sequence,page='a',page='b', page NOT IN ('a','b')) AS sequences　from values( 'page String, sequence UInt16' , ('a', 1), ('c',2), ('b', 3));
0 # !

SELECT sequenceMatch('(?1).(?2)')(sequence,page='a',page='b', page NOT IN ('a','b')) AS sequences　from values( 'page String, sequence UInt16' , ('a', 1), ('c',2), ('b', 3));
1 #

```
So for your example \- just introduce one more ’nothing matched’ condition:


```
SELECT sequenceCount('(?1)(?2)')(sequence, page ILIKE '%a%', page ILIKE '%a%', NOT (page ILIKE '%a%')) AS sequences
FROM values('page String, sequence UInt16', ('a', 1), ('a', 2), ('b', 3), ('b', 4), ('a', 5), ('b', 6), ('a', 7))

```
