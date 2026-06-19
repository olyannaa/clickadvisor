# stochasticLogisticRegression \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- stochasticLogisticRegression
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/stochasticLogisticRegression.md)# stochasticLogisticRegression

## stochasticLogisticRegression[​](#stochasticLogisticRegression "Direct link to stochasticLogisticRegression")


Introduced in: v20\.1\.0


This function implements stochastic logistic regression.
It can be used for binary classification problem, supports the same custom parameters as [`stochasticLinearRegression`](/docs/sql-reference/aggregate-functions/reference/stochasticlinearregression) and works the same way.


**Usage**


The function is used in two steps:


1. Fitting


For fitting a query like this can be used:



```
CREATE TABLE IF NOT EXISTS train_data
(
    param1 Float64,
    param2 Float64,
    target Float64
) ENGINE = Memory;

CREATE TABLE your_model ENGINE = Memory AS SELECT
stochasticLogisticRegression(0.1, 0.0, 5, 'SGD')(target, x1, x2)
AS state FROM train_data;

```

Here, we also need to insert data into the `train_data` table.
The number of parameters is not fixed, it depends only on the number of arguments passed into `logisticRegressionState`.
They all must be numeric values.
Note that the column with target value (which we would like to learn to predict) is inserted as the first argument.


Predicted labels have to be in \[\-1, 1].


2. Predicting


Using saved state we can predict the probability of an object having label `1`.



```
WITH (SELECT state FROM your_model) AS model SELECT
evalMLMethod(model, param1, param2) FROM test_data

```

The query will return a column of probabilities.
Note that first argument of `evalMLMethod` is an `AggregateFunctionState` object, next are columns of features.


We can also set a bound of probability, which assigns elements to different labels.



```
SELECT result < 1.1 AND result > 0.5 FROM
(WITH (SELECT state FROM your_model) AS model SELECT
evalMLMethod(model, param1, param2) AS result FROM test_data)

```

Then the result will be labels.


`test_data` is a table like `train_data` but may not contain target value.


**Syntax**



```
stochasticLogisticRegression([learning_rate, l2_regularization_coef, mini_batch_size, method])(target, x1, x2, ...)

```

**Arguments**


- `learning_rate` — The coefficient on step length when gradient descent step is performed. A learning rate that is too big may cause infinite weights of the model. Default is `0.00001`. [`Float64`](/docs/sql-reference/data-types/float)
- `l2_regularization_coef` — L2 regularization coefficient which may help to prevent overfitting. Default is `0.1`. [`Float64`](/docs/sql-reference/data-types/float)
- `mini_batch_size` — Sets the number of elements which gradients will be computed and summed to perform one step of gradient descent. Pure stochastic descent uses one element, however having small batches (about 10 elements) makes gradient steps more stable. Default is `15`. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `method` — Method for updating weights: `Adam` (by default), `SGD`, `Momentum`, `Nesterov`. `Momentum` and `Nesterov` require a little bit more computations and memory, however they happen to be useful in terms of speed of convergence and stability of stochastic gradient methods. [`String`](/docs/sql-reference/data-types/string)
- `target` — Target binary classification labels. Must be in range \[\-1, 1]. [`Float`](/docs/sql-reference/data-types/float)
- `x1, x2, ...` — Feature values (independent variables). All must be numeric. [`Float`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the trained logistic regression model weights. Use `evalMLMethod` for predictions which returns probabilities of object having label `1`. [`Array(Float64)`](/docs/sql-reference/data-types/array)


**Examples**


**Training a model**



```
CREATE TABLE your_model
ENGINE = MergeTree
ORDER BY tuple()
AS SELECT
stochasticLogisticRegressionState(1.0, 1.0, 10, 'SGD')(target, x1, x2)
AS state FROM train_data

```


```
Saves trained model state to table

```

**Making predictions**



```
WITH (SELECT state FROM your_model) AS model
SELECT
evalMLMethod(model, x1, x2)
FROM test_data

```


```
Returns probability values for test data

```

**Classification with threshold**



```
SELECT result < 1.1 AND result > 0.5
FROM (
WITH (SELECT state FROM your_model) AS model SELECT
evalMLMethod(model, x1, x2) AS result FROM test_data)

```


```
Returns binary classification labels using probability threshold

```

**See Also**


- [stochasticLinearRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlogisticregression)
- [Difference between linear and logistic regressions.](https://stackoverflow.com/questions/12146914/what-is-the-difference-between-linear-regression-and-logistic-regression)
[PreviousstochasticLinearRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlinearregression)[NextstudentTTest](/docs/sql-reference/aggregate-functions/reference/studentttest)- [stochasticLogisticRegression](#stochasticLogisticRegression)
Was this page helpful?
