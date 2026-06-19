# Financial functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Financial
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/financial-functions.md)# Financial functions

NoteThe documentation below is generated from the `system.functions` system table


## financialInternalRateOfReturn[​](#financialInternalRateOfReturn "Direct link to financialInternalRateOfReturn")


Introduced in: v25\.7\.0


Calculates the Internal Rate of Return (IRR) for a series of cash flows occurring at regular intervals.
IRR is the discount rate at which the Net Present Value (NPV) equals zero.


IRR attempts to solve the following equation:


∑i\=0ncashflowi(1\+irr)i\=0\\sum\_{i\=0}^n \\frac{cashflow\_i}{(1 \+ irr)^i} \= 0i\=0∑n​(1\+irr)icashflowi​​\=0
**Syntax**



```
financialInternalRateOfReturn(cashflows[, guess])

```

**Arguments**


- `cashflows` — Array of cash flows. Each value represents a payment (negative value) or income (positive value). [`Array(Int8/16/32/64)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `[, guess]` — Optional initial guess (constant value) for the internal rate of return (default 0\.1\). [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the internal rate of return or `NaN` if the calculation cannot converge, input array is empty or has only one element, all cash flows are zero, or other calculation errors occur. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**simple\_example**



```
SELECT financialInternalRateOfReturn([-100, 39, 59, 55, 20])

```


```
0.2809484211599611

```

**simple\_example\_with\_guess**



```
SELECT financialInternalRateOfReturn([-100, 39, 59, 55, 20], 0.1)

```


```
0.2809484211599611

```

## financialInternalRateOfReturnExtended[​](#financialInternalRateOfReturnExtended "Direct link to financialInternalRateOfReturnExtended")


Introduced in: v25\.7\.0


Calculates the Extended Internal Rate of Return (XIRR) for a series of cash flows occurring at irregular intervals. XIRR is the discount rate at which the net present value (NPV) of all cash flows equals zero.


XIRR attempts to solve the following equation (example for `ACT_365F`):


∑i\=0ncashflowi(1\+rate)(datei−date0)/365\=0\\sum\_{i\=0}^n \\frac{cashflow\_i}{(1 \+ rate)^{(date\_i \- date\_0\)/365}} \= 0i\=0∑n​(1\+rate)(datei​−date0​)/365cashflowi​​\=0
Arrays should be sorted by date in ascending order. Dates need to be unique.


**Syntax**



```
financialInternalRateOfReturnExtended(cashflow, date [, guess, daycount])

```

**Arguments**


- `cashflow` — An array of cash flows corresponding to the dates in second param. [`Array(Int8/16/32/64)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `date` — A sorted array of unique dates corresponding to the cash flows. [`Array(Date)`](/docs/sql-reference/data-types/array) or [`Array(Date32)`](/docs/sql-reference/data-types/array)
- `[, guess]` — Optional. Initial guess (constant value) for the XIRR calculation. [`Float*`](/docs/sql-reference/data-types/float)
- `[, daycount]` —
Optional day count convention (default 'ACT\_365F'). Supported values:
- 'ACT\_365F' \- Actual/365 Fixed: Uses actual number of days between dates divided by 365
- 'ACT\_365\_25' \- Actual/365\.25: Uses actual number of days between dates divided by 365\.25
[`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the XIRR value. If the calculation cannot be performed, it returns NaN. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**simple\_example**



```
SELECT financialInternalRateOfReturnExtended([-10000, 5750, 4250, 3250], [toDate('2020-01-01'), toDate('2020-03-01'), toDate('2020-10-30'), toDate('2021-02-15')])

```


```
0.6342972615260243

```

**simple\_example\_with\_guess**



```
SELECT financialInternalRateOfReturnExtended([-10000, 5750, 4250, 3250], [toDate('2020-01-01'), toDate('2020-03-01'), toDate('2020-10-30'), toDate('2021-02-15')], 0.5)

```


```
0.6342972615260243

```

**simple\_example\_daycount**



```
SELECT round(financialInternalRateOfReturnExtended([100000, -110000], [toDate('2020-01-01'), toDate('2021-01-01')], 0.1, 'ACT_365_25'), 6) AS xirr_365_25

```


```
0.099785

```

## financialNetPresentValue[​](#financialNetPresentValue "Direct link to financialNetPresentValue")


Introduced in: v25\.7\.0


Calculates the Net Present Value (NPV) of a series of cash flows assuming equal time intervals between each cash flow.


Default variant (`start_from_zero` \= true):


∑i\=0N−1valuesi(1\+rate)i\\sum\_{i\=0}^{N\-1} \\frac{values\_i}{(1 \+ rate)^i}i\=0∑N−1​(1\+rate)ivaluesi​​
Excel\-compatible variant (`start_from_zero` \= false):


∑i\=1Nvaluesi(1\+rate)i\\sum\_{i\=1}^{N} \\frac{values\_i}{(1 \+ rate)^i}i\=1∑N​(1\+rate)ivaluesi​​
**Syntax**



```
financialNetPresentValue(rate, cashflows[, start_from_zero])

```

**Arguments**


- `rate` — The discount rate to apply. [`Float*`](/docs/sql-reference/data-types/float)
- `cashflows` — Array of cash flows. Each value represents a payment (negative value) or income (positive value). [`Array(Int8/16/32/64)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `[, start_from_zero]` — Optional boolean parameter indicating whether to start the NPV calculation from period `0` (true) or period `1` (false, Excel\-compatible). Default: true. [`Bool`](/docs/sql-reference/data-types/boolean)


**Returned value**


Returns the net present value as a Float64 value. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**default\_calculation**



```
SELECT financialNetPresentValue(0.08, [-40000., 5000., 8000., 12000., 30000.])

```


```
3065.2226681795255

```

**excel\_compatible\_calculation**



```
SELECT financialNetPresentValue(0.08, [-40000., 5000., 8000., 12000., 30000.], false)

```


```
2838.1691372032656

```

## financialNetPresentValueExtended[​](#financialNetPresentValueExtended "Direct link to financialNetPresentValueExtended")


Introduced in: v25\.7\.0


Calculates the Extended Net Present Value (XNPV) for a series of cash flows occurring at irregular intervals. XNPV considers the specific timing of each cash flow when calculating present value.


XNPV equation for `ACT_365F`:


XNPV\=∑i\=1ncashflowi(1\+rate)(datei−date0)/365XNPV\=\\sum\_{i\=1}^n \\frac{cashflow\_i}{(1 \+ rate)^{(date\_i \- date\_0\)/365}}XNPV\=i\=1∑n​(1\+rate)(datei​−date0​)/365cashflowi​​
Arrays should be sorted by date in ascending order. Dates need to be unique.


**Syntax**



```
financialNetPresentValueExtended(rate, cashflows, dates[, daycount])

```

**Arguments**


- `rate` — The discount rate to apply. [`Float*`](/docs/sql-reference/data-types/float)
- `cashflows` — Array of cash flows. Each value represents a payment (negative value) or income (positive value). Must contain at least one positive and one negative value. [`Array(Int8/16/32/64)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `dates` — Array of dates corresponding to each cash flow. Must have the same size as cashflows array. [`Array(Date)`](/docs/sql-reference/data-types/array) or [`Array(Date32)`](/docs/sql-reference/data-types/array)
- `[, daycount]` — Optional day count convention. Supported values: `'ACT_365F'` (default) — Actual/365 Fixed, `'ACT_365_25'` — Actual/365\.25\. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the net present value as a Float64 value. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT financialNetPresentValueExtended(0.1, [-10000., 5750., 4250., 3250.], [toDate('2020-01-01'), toDate('2020-03-01'), toDate('2020-10-30'), toDate('2021-02-15')])

```


```
2506.579458169746

```

**Using different day count convention**



```
SELECT financialNetPresentValueExtended(0.1, [-10000., 5750., 4250., 3250.], [toDate('2020-01-01'), toDate('2020-03-01'), toDate('2020-10-30'), toDate('2021-02-15')], 'ACT_365_25')

```


```
2507.067268742502

```

## Related resources[​](#related-resources "Direct link to Related resources")


- [Financial functions in ClickHouse video](https://www.youtube.com/watch?v=BePLPVa0w_o)
[PreviousFiles](/docs/sql-reference/functions/files)[NextNullable](/docs/sql-reference/functions/functions-for-nulls)- [financialInternalRateOfReturn](#financialInternalRateOfReturn)- [financialInternalRateOfReturnExtended](#financialInternalRateOfReturnExtended)- [financialNetPresentValue](#financialNetPresentValue)- [financialNetPresentValueExtended](#financialNetPresentValueExtended)- [Related resources](#related-resources)
Was this page helpful?
