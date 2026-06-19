# CatBoost / MindsDB / Fast.ai \| Altinity® Knowledge Base for ClickHouse®


1. [Integrations](/altinity-kb-integrations/)
2. CatBoost / MindsDB / Fast.ai
# CatBoost / MindsDB / Fast.ai

#### Info

Article is based on feedback provided by one of Altinity clients.CatBoost:

- It uses gradient boosting \- a hard to use technique which can outperform neural networks. Gradient boosting is powerful but it’s easy to shoot yourself in the foot using it.
- The documentation on how to use it is quite lacking. The only good source of information on how to properly configure a model to yield good results is this video: [https://www.youtube.com/watch?v\=usdEWSDisS0](https://www.youtube.com/watch?v=usdEWSDisS0)
. We had to dig around GitHub issues to find out how to make it work with ClickHouse®.
- CatBoost is fast. Other libraries will take \~5X to \~10X as long to do what CatBoost does.
- CatBoost will do preprocessing out of the box (fills nulls, apply standard scaling, encodes strings as numbers).
- CatBoost has all functions you’d need (metrics, plotters, feature importance)

It makes sense to split what CatBoost does into 2 parts:

- preprocessing (fills nulls, apply standard scaling, encodes strings as numbers)
- number crunching (convert preprocessed numbers to another number \- ex: revenue of impression)

Compared to [Fast.ai](http://fast.ai/)
, CatBoost pre\-processing is as simple to use and produces results that can be as good as [Fast.ai](http://fast.ai/)
.

The number crunching part of [Fast.ai](http://fast.ai/)
is no\-config. For CatBoost you need to configure it, a lot.

CatBoost won’t simplify or hide any complexity of the process. So you need to know data science terms and what it does (ex: if your model is underfitting you can use a smaller l2\_reg parameter in the model constructor).

In the end both [Fast.ai](http://fast.ai/)
and CatBoost can yield comparable results.

Regarding deploying models, CatBoost is really good. The model runs fast, it has a simple binary format which can be loaded in ClickHouse, C, or Python and it will encapsulate pre\-processing with the binary file. Deploying [Fast.ai](http://fast.ai/)
models at scale/speed is impossible out of the box (we have our custom solution to do it which is not simple).

TLDR: CatBoost is fast, produces awesome models, is super easy to deploy and it’s easy to use/train (after becoming familiar with it despite the bad documentation \& if you know data science terms).

## Regarding MindsDB

The project seems to be a good idea but it’s too young. I was using the GUI version and I’ve encountered some bugs, and none of those bugs have a good error message.

- It won’t show data in preview.
- The “download” button won’t work.
- It’s trying to create and drop tables in ClickHouse without me asking it to.
- Other than bugs:


	- It will only use 1 core to do everything (training, analysis, download).
	- Analysis will only run with a very small subset of data, if I use something like 1M rows it never finishes.
- Training a model on 100k rows took 25 minutes \- (CatBoost takes 90s to train with 1M rows)
- The model trained on MindsDB is way worse. It had r\-squared of 0\.46 (CatBoost\=0\.58\)

To me it seems that they are a plugin which connects ClickHouse to MySQL to run the model in Pytorch.

It’s too complex and hard to debug and understand. The resulting model is not good enough.

TLDR: Easy to use (if bugs are ignored), too slow to train \& produces a bad model.

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
