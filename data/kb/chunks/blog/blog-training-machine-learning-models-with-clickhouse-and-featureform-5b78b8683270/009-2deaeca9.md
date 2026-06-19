---
source: blog
url: https://clickhouse.com/blog/powering-featurestores-with-clickhouse
topic: training-machine-learning-models-with-clickhouse
ch_version_introduced: '23.3'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 19
---

we should understand the distribution of the classes. While we could compute this over our previous data frame, this limits our analysis to the 100 rows it contains. ``` data['Class'].value_counts().plot.pie(autopct='%3.1f%%',shadow=True, legend= True,startangle =45) plt.title('Distribution of Class',size=14) plt.show() ```

Ideally, we’d like to compute this for all of the rows in the table. For our dataset, we could probably just load the entire dataset of 550k rows into memory by removing the limit. However, this is not viable for the larger datasets from either a network or memory perspective. To push this work down to ClickHouse, we can define a transformation.

```
@clickhouse.sql_transformation(inputs=[creditcard])
def classCounts(creditcard):
    return "SELECT Class,count() c FROM {{creditcard}} GROUP BY Class"

client.dataframe(classCounts).pivot_table(index='Class', columns=None, values='c', aggfunc='sum').plot.pie(
    explode=[0.1, 0], autopct='%3.1f%%', shadow=True, legend=True, startangle=45, subplots=True)

```

We use a simple aggregation here to compute the count per class. Note the use of templating for our query. The variable `{{creditcard}}` will be replaced with the table name of the credit card dataset. This will not be the original table \- as we noted earlier, with Featureform making an immutable copy of the data in ClickHouse, this will be a table with a name specific to the version. Once created, we can convert the results of the transformation into a data frame and plot the results.

![class_split.png](/uploads/class_split_aefdab4c89.png)
This dataset is balanced (50% fraud and 50% non fraud). While this significantly simplifies future training, it makes us wonder if this dataset is artificial. This is also likely to heavily contribute to the rather high accuracy scores advertised in the original notebook.

> With our primary data serving as the raw materials, these are then transformed into data sets containing the set of features and labels required for serving and training machine learning models. These transformations can be directly applied to primary data sets or sequenced and executed on other previously transformed data sets. It’s essential to understand that Featureform does not perform the data transformations itself. Instead, it orchestrates ClickHouse to execute the transformation. The results of the transformation will also be stored as a versioned table in ClickHouse for later fast retrieval \- a process known as materialization.

Similarly, when first exploring data, users often use the `describe` method for a data frame to understand the properties of the columns.

```
data.describe()

```
