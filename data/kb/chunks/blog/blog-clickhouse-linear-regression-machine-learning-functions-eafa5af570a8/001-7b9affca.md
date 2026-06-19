---
source: blog
url: https://ensembleanalytics.io/blog/linear-regression-using-clickhouse
topic: linear-regression-using-clickhouse-machine-learning-functions
ch_version_introduced: '43.81204'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 6
---

# Linear Regression Using ClickHouse Machine Learning Functions

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Linear Regression Using ClickHouse Machine Learning Functions

![](/_next/image?url=%2Fuploads%2Fensembleanalytics_logo_avatar_89130dd8b9.png&w=96&q=75)[Ensemble](/authors/ensemble)Dec 13, 2023 · 10 minutes read![linear_regression_clickhouse.png](/uploads/linear_regression_clickhouse_4dc95f89e1.png)

> This was originally [a post by ensemble analytics](https://ensembleanalytics.io/blog/linear-regression-using-clickhouse), who have kindly allowed republishing of this content. We welcome posts from our community and thank them for their contributions.

## Introduction [\#](/blog/clickhouse-linear-regression-machine-learning-functions#introduction)

This article is part of a series where we look at doing data science work within [ClickHouse](https://clickhouse.com). Articles in this series include [forecasting](https://ensembleanalytics.io/blog/forecasting-using-clickhouse), [anomaly detection](https://ensembleanalytics.io/blog/anomaly-detection-using-clickhouse), [linear regression](https://ensembleanalytics.io/blog/linear-regression-using-clickhouse) and [time series classification](https://ensembleanalytics.io/blog/time-series-analysis-using-clickhouse).

Though this type of analysis would more typically take place outside of ClickHouse in a programming language such as Python or R, our preference is to take things as far as possible using just the database.

By doing this, we can rely on the power of ClickHouse to process large datasets with high performance, and reduce or even totally avoid the amount of code that we need to write. This also means that we can work with smaller in\-memory datasets on the client side and potentially avoid the need for distributed computation using frameworks such as Spark.

A notebook describing the full worked example can be found [here](https://app.hex.tech/d83ae9cc-7cbe-40f3-9899-0c348f283047/hex/9206f58c-0bde-4dae-94d7-aa9379773d84/draft/logic).

## About This Example [\#](/blog/clickhouse-linear-regression-machine-learning-functions#about-this-example)

In this article, we will carry out a simple linear regression analysis, which we will use to predict delivery times based on two variables \- the distance of the delivery and the hour the package was picked up for delivery.

We will work with and render geographical data as part of the analysis, for instance making use of Clickhouse's [geoDistance](https://clickhouse.com/docs/en/sql-reference/functions/geo/coordinates) function to calculate distances based on geographical coordinates.

## Dataset [\#](/blog/clickhouse-linear-regression-machine-learning-functions#dataset)

Our dataset is a small extract of this [last\-mile delivery dataset](https://huggingface.co/datasets/Cainiao-AI/LaDe) by Hugging Face.

Though the dataset is large and detailed, we will look at a subset of 2,293 orders delivered by a single courier, number 75, in region 53 of the Chinese city of Jilin in order to make it easier to follow the example.
