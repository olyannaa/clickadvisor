# welchTTest \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- welchTTest
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/welchTTest.md)# welchTTest

## welchTTest[​](#welchTTest "Direct link to welchTTest")


Introduced in: v21\.1\.0


Applies [Welch's t\-test](https://en.wikipedia.org/wiki/Welch%27s_t-test) to samples from two populations.


Values of both samples are in the `sample_data` column.
If `sample_index` equals to 0 then the value in that row belongs to the sample from the first population.
Otherwise it belongs to the sample from the second population.
The null hypothesis is that means of populations are equal.
Normal distribution is assumed.
Populations may have unequal variance.


**Syntax**



```
welchTTest([confidence_level])(sample_data, sample_index)

```

**Parameters**


- `confidence_level` — Optional. Confidence level in order to calculate confidence intervals. [`Float`](/docs/sql-reference/data-types/float)


**Arguments**


- `sample_data` — Sample data. [`Int*`](/docs/sql-reference/data-types/int-uint) or [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)
- `sample_index` — Sample index. [`Int*`](/docs/sql-reference/data-types/int-uint) or [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Tuple with two or four elements (if the optional `confidence_level` is specified): calculated t\-statistic, calculated p\-value, and optionally calculated confidence\-interval\-low and confidence\-interval\-high. [`Tuple(Float64, Float64)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float64, Float64, Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic Welch's t\-test**



```
CREATE TABLE welch_ttest (sample_data Float64, sample_index UInt8) ENGINE = Memory;
INSERT INTO welch_ttest VALUES (20.3, 0), (22.1, 0), (21.9, 0), (18.9, 1), (20.3, 1), (19, 1);

SELECT welchTTest(sample_data, sample_index) FROM welch_ttest;

```


```
┌─welchTTest(sample_data, sample_index)──────┐
│ (2.7988719532211235, 0.051807360348581945) │
└────────────────────────────────────────────┘

```

**With confidence level**



```
SELECT welchTTest(0.95)(sample_data, sample_index) FROM welch_ttest;

```


```
┌─welchTTest(0.95)(sample_data, sample_index)─────────────────────────────────────────┐
│ (2.7988719532211235, 0.05180736034858519, -0.026294346671631885, 4.092961013338302) │
└─────────────────────────────────────────────────────────────────────────────────────┘

```

**See Also**


- [Welch's t\-test](https://en.wikipedia.org/wiki/Welch%27s_t-test)
- [studentTTest function](/docs/sql-reference/aggregate-functions/reference/studentttest)
[PreviousvarSampStable](/docs/sql-reference/aggregate-functions/reference/varsampstable)[NextCombinators](/docs/sql-reference/aggregate-functions/combinators)- [welchTTest](#welchTTest)
Was this page helpful?
