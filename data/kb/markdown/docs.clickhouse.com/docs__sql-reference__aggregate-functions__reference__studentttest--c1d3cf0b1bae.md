# studentTTest \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- studentTTest
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/studentTTest.md)# studentTTest

## studentTTest[​](#studentTTest "Direct link to studentTTest")


Introduced in: v21\.1\.0


Applies Student's t\-test to samples from two populations.


Values of both samples are in the `sample_data` column. If `sample_index` equals to 0 then the value in that row belongs to the sample from the first population. Otherwise it belongs to the sample from the second population.
The null hypothesis is that means of populations are equal. Normal distribution with equal variances is assumed.


**See Also**


- [Student's t\-test](https://en.wikipedia.org/wiki/Student%27s_t-test)
- [welchTTest function](/docs/sql-reference/aggregate-functions/reference/welchttest)


**Syntax**



```
studentTTest([confidence_level])(sample_data, sample_index)

```

**Parameters**


- `confidence_level` — Optional. Confidence level in order to calculate confidence intervals. [`Float`](/docs/sql-reference/data-types/float)


**Arguments**


- `sample_data` — Sample data. [`Integer`](/docs/sql-reference/data-types/int-uint) or [`Float`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `sample_index` — Sample index. [`Integer`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple with two or four elements (if the optional `confidence_level` is specified): calculated t\-statistic, calculated p\-value, \[calculated confidence\-interval\-low], \[calculated confidence\-interval\-high]. [`Tuple(Float64, Float64)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float64, Float64, Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT studentTTest(sample_data, sample_index) FROM student_ttest;

```


```
┌─studentTTest(sample_data, sample_index)───┐
│ (-0.21739130434783777,0.8385421208415731) │
└───────────────────────────────────────────┘

```

**See Also**


- [Student's t\-test](https://en.wikipedia.org/wiki/Student%27s_t-test)
- [welchTTest function](/docs/sql-reference/aggregate-functions/reference/welchttest)
[PreviousstochasticLogisticRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlogisticregression)[NextstudentTTestOneSample](/docs/sql-reference/aggregate-functions/reference/studentttestonesample)- [studentTTest](#studentTTest)
Was this page helpful?
