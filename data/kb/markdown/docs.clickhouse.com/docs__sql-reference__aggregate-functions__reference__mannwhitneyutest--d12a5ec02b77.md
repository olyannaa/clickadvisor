# mannWhitneyUTest \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- mannWhitneyUTest
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/mannWhitneyUTest.md)# mannWhitneyUTest

## mannWhitneyUTest[​](#mannWhitneyUTest "Direct link to mannWhitneyUTest")


Introduced in: v21\.1\.0


Applies the Mann\-Whitney rank test to samples from two populations.


Values of both samples are in the `sample_data` column.
If `sample_index` equals to 0 then the value in that row belongs to the sample from the first population.
Otherwise it belongs to the sample from the second population.
The null hypothesis is that two populations are stochastically equal.
Also one\-sided hypotheses can be tested.
This test does not assume that data have normal distribution.


**Syntax**



```
mannWhitneyUTest[(alternative[, continuity_correction])](sample_data, sample_index)

```

**Parameters**


- `alternative` — Optional. Alternative hypothesis. 'two\-sided' (default): two populations are not stochastically equal. 'greater': values in the first sample are stochastically greater than those in the second sample. 'less': values in the first sample are stochastically less than those in the second sample. [`String`](/docs/sql-reference/data-types/string)
- `continuity_correction` — Optional. If not 0 then continuity correction in the normal approximation for the p\-value is applied. The default value is 1\. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `sample_data` — Sample data. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)
- `sample_index` — Sample index. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two elements: calculated U\-statistic and calculated p\-value. [`Tuple(Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Mann\-Whitney U test example**



```
CREATE TABLE mww_ttest (sample_data Float64, sample_index UInt8) ENGINE = Memory;
INSERT INTO mww_ttest VALUES (10, 0), (11, 0), (12, 0), (1, 1), (2, 1), (3, 1);

SELECT mannWhitneyUTest('greater')(sample_data, sample_index) FROM mww_ttest;

```


```
┌─mannWhitneyUTest('greater')(sample_data, sample_index)─┐
│ (9,0.04042779918503192)                                │
└────────────────────────────────────────────────────────┘

```

**See Also**


- [Mann–Whitney U test](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test)
- [Stochastic ordering](https://en.wikipedia.org/wiki/Stochastic_ordering)
[Previouslast\_value](/docs/sql-reference/aggregate-functions/reference/last_value)[Nextmax](/docs/sql-reference/aggregate-functions/reference/max)- [mannWhitneyUTest](#mannWhitneyUTest)
Was this page helpful?
