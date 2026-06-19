# stochasticLinearRegression \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- stochasticLinearRegression
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/stochasticLinearRegression.md)# stochasticLinearRegression

## stochasticLinearRegression[​](#stochasticLinearRegression "Direct link to stochasticLinearRegression")


Introduced in: v20\.1\.0


This function implements stochastic linear regression.
It supports custom parameters for:


- learning rate
- L2 regularization coefficient
- mini\-batch size


It also has a few methods for updating weights:


- Adam (used by default)
- simple SGD
- Momentum
- Nesterov


**Usage**


The function is used in two steps: fitting the model and predicting on new data.


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
stochasticLinearRegressionState(0.1, 0.0, 5, 'SGD')(target, x1, x2)
AS state FROM train_data;

```

Here, we also need to insert data into the `train_data` table.
The number of parameters is not fixed, it depends only on the number of arguments passed into `linearRegressionState`.
They all must be numeric values.
Note that the column with target value (which we would like to learn to predict) is inserted as the first argument.


2. Predicting


After saving a state into the table, we may use it multiple times for prediction or even merge with other states and create new, even better models.



```
WITH (SELECT state FROM your_model) AS model SELECT
evalMLMethod(model, x1, x2) FROM test_data

```

The query will return a column of predicted values.
Note that first argument of `evalMLMethod` is `AggregateFunctionState` object, next are columns of features.


`test_data` is a table like `train_data` but may not contain target value.


**Notes**


1. To merge two models user may create such query:



```
SELECT state1 + state2 FROM your_models

```

where the `your_models` table contains both models.
This query will return a new `AggregateFunctionState` object.


2. You may fetch weights of the created model for its own purposes without saving the model if no `-State` combinator is used.



```
SELECT stochasticLinearRegression(0.01)(target, param1, param2)
FROM train_data

```

A query like this will fit the model and return its weights \- first are weights, which correspond to the parameters of the model, the last one is bias.
So in the example above the query will return a column with 3 values.


**Syntax**



```
stochasticLinearRegression([learning_rate, l2_regularization_coef, mini_batch_size, method])(target, x1, x2, ...)

```

**Arguments**


- `learning_rate` — The coefficient on step length when gradient descent step is performed. A learning rate that is too big may cause infinite weights of the model. Default is `0.00001`. [`Float64`](/docs/sql-reference/data-types/float)
- `l2_regularization_coef` — L2 regularization coefficient which may help to prevent overfitting. Default is `0.1`. [`Float64`](/docs/sql-reference/data-types/float)
- `mini_batch_size` — Sets the number of elements which gradients will be computed and summed to perform one step of gradient descent. Pure stochastic descent uses one element, however having small batches (about 10 elements) makes gradient steps more stable. Default is `15`. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `method` — Method for updating weights: `Adam` (by default), `SGD`, `Momentum`, `Nesterov`. `Momentum` and `Nesterov` require slightly more computations and memory, however they happen to be useful in terms of speed of convergence and stability of stochastic gradient methods. [`const String`](/docs/sql-reference/data-types/string)
- `target` — Target value (dependent variable) to learn to predict. Must be numeric. [`Float*`](/docs/sql-reference/data-types/float)
- `x1, x2, ...` — Feature values (independent variables). All must be numeric. [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the trained linear regression model weights. First values correspond to the parameters of the model, the last one is bias. Use `evalMLMethod` for predictions. [`Array(Float64)`](/docs/sql-reference/data-types/array)


**Examples**


**Training a model**



```
CREATE TABLE your_model
ENGINE = Memory
AS SELECT
stochasticLinearRegressionState(0.1, 0.0, 5, 'SGD')(target, x1, x2)
AS state FROM train_data

```


```
Saves trained model state to table

```

**Making predictions**



```
WITH (SELECT state FROM your_model) AS model SELECT
evalMLMethod(model, x1, x2) FROM test_data

```


```
Returns predicted values for test data

```

**Getting model weights**



```
SELECT stochasticLinearRegression(0.01)(target, x1, x2) FROM train_data

```


```
Returns model weights without saving state

```

**See Also**


- [stochasticLogisticRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlogisticregression)
- [Difference between linear and logistic regressions](https://stackoverflow.com/questions/12146914/what-is-the-difference-between-linear-regression-and-logistic-regression)
[PreviousstddevSampStable](/docs/sql-reference/aggregate-functions/reference/stddevsampstable)[NextstochasticLogisticRegression](/docs/sql-reference/aggregate-functions/reference/stochasticlogisticregression)- [stochasticLinearRegression](#stochasticLinearRegression)
Was this page helpful?
