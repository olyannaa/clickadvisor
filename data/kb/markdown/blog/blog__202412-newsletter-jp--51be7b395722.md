# 2024年12月ニュースレター


2024年最後となる12月のClickHouseニュースレターへようこそ！今月はクエリ最適化ガイド、SQLベースのオブザーバビリティの実例、Amazonのre、Postgres CDCコネクタ（ClickPipes向け）のプライベートプレビュー開始など、多彩なトピックをお届けします。


 


## 今回の内容 [\#](/jp/blog/202412-newsletter-jp#%E4%BB%8A%E5%9B%9E%E3%81%AE%E5%86%85%E5%AE%B9)


- [今後のイベント](https://clickhouse.com/blog/202412-newsletter#upcoming-events)
- [注目のコミュニティメンバー](https://clickhouse.com/blog/202412-newsletter#featured-community-member)
- [24\.11リリース](https://clickhouse.com/blog/202412-newsletter#2411-release)
- [ClickHouseクエリ最適化のシンプルガイド：パート1](https://clickhouse.com/blog/202412-newsletter#a-simple-guide-to-clickhouse-query-optimization-part-1)
- [ClickHouseとGrafanaで実現するSQLベースのオブザーバビリティ構築](https://clickhouse.com/blog/202412-newsletter#building-sql-based-observability-with-clickhouse-and-grafana)
- [Postgres CDCコネクタがClickPipesでプライベートプレビューに](https://clickhouse.com/blog/202412-newsletter#postgres-cdc-connector-for-clickpipes-is-now-in-private-preview)
- [ClickHouse Decoded: 超高速データの仕組みを徹底解説](https://clickhouse.com/blog/202412-newsletter#clickhouse-decoded-making-sense-of-fast-data)
- [AWS re:Invent 2024でのClickHouse](https://clickhouse.com/blog/202412-newsletter#clickhouse-at-aws-reinvent-2024)
- [ビデオコーナー](https://clickhouse.com/blog/202412-newsletter#video-corner)
- [クイックリード](https://clickhouse.com/blog/202412-newsletter#quick-reads)
- [ClickHouseユーザーカンファレンス](https://clickhouse.com/blog/202412-newsletter#clickhouse-user-conference)
- [今月の投稿](https://clickhouse.com/blog/202412-newsletter#post-of-the-month)


 


## 今後のイベント [\#](/jp/blog/202412-newsletter-jp#%E4%BB%8A%E5%BE%8C%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


**グローバルイベント**


- [Release call 24\.12](https://clickhouse.com/company/events/v24-12-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- 12月19日
- [Release call 25\.1](https://clickhouse.com/company/events/v25-1-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- 1月30日


**無料トレーニング**


- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- バーチャル \- 1月8日・1月15日
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202501-emea-query-optimization?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- バーチャル \- 1月22日
- [Using ClickHouse for Observability](https://clickhouse.com/company/events/202501-amer-clickhouse-observability?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter) \- バーチャル \- 1月29日


**EMEAでのイベント**


- [Meetup in London](https://www.meetup.com/clickhouse-london-user-group/events/305146729/) \- 2月5日
- [Meetup in Dubai](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/) \- 2月10日


**APACでのイベント**


- [Alibaba Developer Summit Jakarta](https://www.alibabacloud.com/en/events/alibabacloud-developer-summit-2025?_p_lc=1) \- 1月21日
- [Meetup in Tokyo](https://www.meetup.com/clickhouse-tokyo-user-group/events/305126993/) \- 1月23日


  

## 注目のコミュニティメンバー [\#](/jp/blog/202412-newsletter-jp#%E6%B3%A8%E7%9B%AE%E3%81%AE%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC)


今月の注目コミュニティメンバーは、SemrushのリードエンジニアであるAzat Khuzhinさんです。


![featured-202412.png](/uploads/featured_202412_d0a6498ade.png)

AzatさんはSemrushで13年以上の経験を持ち、ClickHouseやその他のデータベース管理システムの運用、大規模な分散システムやデータ処理に精通しています。



彼はClickHouseへ定期的に貢献しており、今年だけで60以上のPull Requestを提出。パフォーマンス向上、システム安定性の強化、さまざまなコンポーネントの機能拡張に取り組んでいます。分散クエリ処理やレプリケーションの改善から、セキュリティ、コンフィグ管理、ユーザーエクスペリエンスの向上など、多岐にわたる分野で活動しています。



[LinkedInでAzatをフォローする](https://www.linkedin.com/in/iamazat?utm_source=clickhouse&utm_medium=email&utm_campaign=202412-newsletter)


 


## 24\.11リリース [\#](/jp/blog/202412-newsletter-jp#2411%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)


![release-24.11.png](/uploads/release_24_11_7412f9e511.png)
24\.11リリースの目玉は、並列ハッシュ結合がデフォルトの結合戦略になったことです。他にも、マークキャッシュの事前ウォーム機能、ベクトル検索向けBFloat16データ型、WITH FILLで使えるSTALENESS修飾子などが追加されています。


[24\.11コミュニティコール](https://clickhouse.com/videos/202411-release-call)では、[HyperDX](https://www.hyperdx.io/)（ClickHouseを使ったオープンソースのオブザーバビリティプラットフォーム）のデモも行われ、盛り上がりました。


[リリース記事を読む](https://clickhouse.com/blog/clickhouse-release-24-11)


 


## ClickHouseクエリ最適化のシンプルガイド：パート1 [\#](/jp/blog/202412-newsletter-jp#clickhouse%E3%82%AF%E3%82%A8%E3%83%AA%E6%9C%80%E9%81%A9%E5%8C%96%E3%81%AE%E3%82%B7%E3%83%B3%E3%83%97%E3%83%AB%E3%82%AC%E3%82%A4%E3%83%89%E3%83%91%E3%83%BC%E3%83%881)


![query-optimization.png](/uploads/query_optimization_b787976d7b.png)
最近ClickHouseのプロダクトマーケティングエンジニアリングチームに加わったLionel Palacin（Lio）が、新しい[ClickHouse Playground](https://sql.clickhouse.com/)でのサンプルクエリのパフォーマンスを向上させたいと思ったのがきっかけで、学んだことを二回シリーズのブログにまとめています。



パート1では、クエリが実行される仕組み、遅いクエリを特定する方法、EXPLAIN句を使ってクエリ実行時の動作を理解する手順などを解説しています。その上で、さまざまな最適化を試し、その結果をどのように確認するかを紹介しています。



[ブログ記事を読む](https://clickhouse.com/blog/a-simple-guide-to-clickhouse-query-optimization-part-1)


 


## ClickHouseとGrafanaで実現するSQLベースのオブザーバビリティ構築 [\#](/jp/blog/202412-newsletter-jp#clickhouse%E3%81%A8grafana%E3%81%A7%E5%AE%9F%E7%8F%BE%E3%81%99%E3%82%8Bsql%E3%83%99%E3%83%BC%E3%82%B9%E3%81%AE%E3%82%AA%E3%83%96%E3%82%B6%E3%83%BC%E3%83%90%E3%83%93%E3%83%AA%E3%83%86%E3%82%A3%E6%A7%8B%E7%AF%89)


![observability-grafana.png](/uploads/observability_grafana_f791b8b1f7.png)
[Timofey Chuchkanov](https://www.linkedin.com/in/crt0r/)（EVALAR JSCのDevOpsエンジニア）が、ClickHouseとGrafanaを使ったオブザーバビリティスタック構築について詳しくブログで紹介しています。


理想のスタックとして挙げた条件（SQLでクエリできること、ログやメトリクスを同じ仕組みで扱えること、各種ソフトウェアとの連携など）を元にElasticserach、Loki、Timescaleなどを比較した結果、ClickHouseを使うことに決めたそうです。



こうした実際の事例を見ると、[SQLベースのオブザーバビリティ](https://clickhouse.com/blog/evolution-of-sql-based-observability-with-clickhouse)が進化しているのを実感できておもしろいですね。



[ブログ記事を読む](https://cmtops.dev/posts/building-observability-with-clickhouse/)


 


## Postgres CDCコネクタがClickPipesでプライベートプレビューに [\#](/jp/blog/202412-newsletter-jp#postgres-cdc%E3%82%B3%E3%83%8D%E3%82%AF%E3%82%BF%E3%81%8Cclickpipes%E3%81%A7%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%97%E3%83%AC%E3%83%93%E3%83%A5%E3%83%BC%E3%81%AB)


![postgres-connector.png](/uploads/postgres_connector_3b1f2f93e3.png)
先日、ClickPipesでPostgresのChange Data Capture（CDC）コネクタのプライベートプレビューを開始しました。



このコネクタを使えば、Postgresデータベースを数クリックでClickHouse Cloudにレプリケートし、高速な分析を実現できます。連続レプリケーションや一回限りの移行にも使えます。



[ブログ記事を読む](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-private-preview)


 


## ClickHouse Decoded: 超高速データの仕組みを徹底解説 [\#](/jp/blog/202412-newsletter-jp#clickhouse-decoded-%E8%B6%85%E9%AB%98%E9%80%9F%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E4%BB%95%E7%B5%84%E3%81%BF%E3%82%92%E5%BE%B9%E5%BA%95%E8%A7%A3%E8%AA%AC)


![fast-data.png](/uploads/fast_data_12c5108f28.png)
Shubham Bhardwajが、ClickHouseの仕組みを詳細に解説しています。まずディスク上のデータ配置とその構成要素を説明し、その後マテリアライズドビューやテーブルエンジンといった機能、最後にClickHouseをスケールさせる方法についても触れています。



[ブログ記事を読む](https://towardsdev.com/clickhouse-decoded-making-sense-of-fast-data-41c5a020734d)


 


## AWS re 2024でのClickHouse [\#](/jp/blog/202412-newsletter-jp#aws-re-2024%E3%81%A7%E3%81%AEclickhouse)


![product-reinvent.png](/uploads/product_reinvent_9dc038e9ff.png)
12月初旬にラスベガスで行われたAWS re\-Inventカンファレンスに、ClickHouseのメンバーが集結しました。同時にいくつかの新製品アナウンスも行われました。



主な発表としては、独自のクラウド環境を利用可能にするBring Your Own Cloud、ダッシュボード機能、ネイティブJSONサポートのベータ版提供、Postgres CDCコネクタのプライベートプレビュー、ベクター類似検索インデックスのアーリーアクセスなどがあります。



[ブログ記事を読む](https://clickhouse.com/blog/reinvent-2024-product-announcements)


 


## ビデオコーナー [\#](/jp/blog/202412-newsletter-jp#%E3%83%93%E3%83%87%E3%82%AA%E3%82%B3%E3%83%BC%E3%83%8A%E3%83%BC)


- ClickHouseにはPIVOT演算子がありませんが、集計関数のコンビネータを使って同等の機能を実現できます。Markが最新のビデオ「[Can you PIVOT in ClickHouse?](https://clickhouse.com/videos/pivot-clickhouse)」でそのやり方を紹介しています。
- Tony BurkeはSolarWindsのプラットフォームエンジニアリングチームで働き、1秒あたり300万件のメッセージをClickHouseに取り込んでいます。Tonyが[ClickHouseのパフォーマンスをどう向上させたか](https://clickhouse.com/videos/solarwinds-observability-3-milion-records-per-second)を解説していて、リアルタイムのテレメトリデータ管理やクエリ最適化のヒントが得られます。
- [Refreshable materialized views](https://clickhouse.com/videos/intro-refreshable-materialized-views)がプロダクション対応になったので、Markが改めて概要やユースケースを紹介するビデオを公開しました。


 


## クイックリード [\#](/jp/blog/202412-newsletter-jp#%E3%82%AF%E3%82%A4%E3%83%83%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%89)


- Pythonのitertools風のGROUP BYをClickHouse SQLで実現しようとした[Niels Reijers](https://medium.com/@nielsreijers/python-itertools-style-group-by-in-sql-with-some-help-from-ai-ab072018fea4)さんのブログは、AIを使って試行錯誤し、最終的に上手く動かすまでの過程が面白いです。
- [Bytewaxの新しいコネクタモジュールであるClickHouse Sink](https://bytewax.io/blog/building-a-click-house-sink-for-bytewax)についてZander Mathesonさんが紹介しています。BytewaxからClickHouseへのデータ書き込みをシームレスに実現できます。
- [Wolfram KriesingはDjangoからClickHouseの集計関数を呼び出す方法](https://picostitch.hashnode.dev/clickhouse-aggregations-and-django)をまとめています。
- Matt Blewittは[2025年に注目しておきたい7つのデータベース](https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/)を挙げています。その中で「もし2つだけDBを使うとしたら、OLTP用にPostgres、OLAP用にClickHouseがあれば十分」とのコメントが。納得です。


 


## ClickHouseユーザーカンファレンス [\#](/jp/blog/202412-newsletter-jp#clickhouse%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%AB%E3%83%B3%E3%83%95%E3%82%A1%E3%83%AC%E3%83%B3%E3%82%B9)


![user-conference.png](/uploads/user_conference_a2b03043e6.png)
2025年に参加するカンファレンスを検討中なら、5月28日・29日にサンフランシスコで開催予定のOpen House（ClickHouseユーザーカンファレンス）をおすすめします。



28日は無料トレーニング、29日はセッションを予定しています。チケットはまだ入手できませんが、以下から登録すれば最新情報をお届けします。



[最新情報を受け取るために登録](https://clickhouse.com/company/events/202505-global-open-house)


 


## 今月の投稿 [\#](/jp/blog/202412-newsletter-jp#%E4%BB%8A%E6%9C%88%E3%81%AE%E6%8A%95%E7%A8%BF)


今月の注目投稿は、[Gulzar Ahmed](https://x.com/megulzar)さんのポストです。インド国内のローカルビジネス向けオンラインデリバリーソフト「Hyperzod」をClickHouseで支援しているそうです。


![twitter-202412.png](/uploads/twitter_202412_72254b4837.png)

[投稿を見る](https://x.com/megulzar/status/1864880796143583399)
