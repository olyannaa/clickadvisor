# meanZTest \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- meanZTest
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/meanZTest.md)# meanZTest

## meanZTest[​](#meanZTest "Direct link to meanZTest")


Introduced in: v22\.2\.0


Applies mean z\-test to samples from two populations.


Values of both samples are in the `sample_data` column.
If `sample_index` equals to 0 then the value in that row belongs to the sample from the first population.
Otherwise it belongs to the sample from the second population.
The null hypothesis is that means of populations are equal.
A normal distribution is assumed.
Populations may have unequal variance and the variances are known.


**Syntax**



```
meanZTest(population_variance_x, population_variance_y, confidence_level)(sample_data, sample_index)

```

**Parameters**


- `population_variance_x` — Variance for population x. [`Float*`](/docs/sql-reference/data-types/float)
- `population_variance_y` — Variance for population y. [`Float*`](/docs/sql-reference/data-types/float)
- `confidence_level` — Confidence level in order to calculate confidence intervals. [`Float*`](/docs/sql-reference/data-types/float)


**Arguments**


- `sample_data` — Sample data. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `sample_index` — Sample index. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with four elements: calculated z\-statistic, calculated p\-value, calculated confidence\-interval\-low, calculated confidence\-interval\-high. [`Tuple(Float64, Float64, Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Mean Z\-test example**



```
CREATE TABLE mean_ztest (sample_data Float64, sample_index UInt8) ENGINE = Memory;
INSERT INTO mean_ztest VALUES (20.3, 0), (21.9, 0), (22.1, 0), (18.9, 1), (19, 1), (20.3, 1);

SELECT meanZTest(0.7, 0.45, 0.95)(sample_data, sample_index) FROM mean_ztest;

```


```
┌─meanZTest(0.7, 0.45, 0.95)(sample_data, sample_index)───────────────────────────────┐
│ (3.2841296025548123, 0.0010229786769086013, 0.8198428246768334, 3.2468238419898365) │
└─────────────────────────────────────────────────────────────────────────────────────┘

```
[PreviousmaxMap](/docs/sql-reference/aggregate-functions/reference/maxmap)[Nextmedian](/docs/sql-reference/aggregate-functions/reference/median)- [meanZTest](#meanZTest)
Was this page helpful?
