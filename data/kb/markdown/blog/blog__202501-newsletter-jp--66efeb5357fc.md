# 2025年1月ニュースレター


2025年最初のClickHouseニュースレターへようこそ。今月は、24\.12リリースにおけるApache Iceberg RESTカタログとスキーマ進化についてご紹介します。プロダクト分析ソリューションの構築方法や、ClickHouseを使用したメダリオンアーキテクチャの実装方法を学びます。また、The All Things Open Conferenceからのビデオもあります！


 


## この号の内容 [\#](/jp/blog/202501-newsletter-jp#%E3%81%93%E3%81%AE%E5%8F%B7%E3%81%AE%E5%86%85%E5%AE%B9)


- [注目のコミュニティメンバー](https://clickhouse.com/blog/202501-newsletter#featured-community-member)
- [今後のイベント](https://clickhouse.com/blog/202501-newsletter#upcoming-events)
- [24\.12 リリース](https://clickhouse.com/blog/202501-newsletter#2412-release)
- [ClickHouseを使用したプロダクト分析ソリューションの構築](https://clickhouse.com/blog/202501-newsletter#building-a-product-analytics-solution-with-clickhouse)
- [パーティション化されたテーブルへのバルクインサートの最適化](https://clickhouse.com/blog/202501-newsletter#optimizing-bulk-inserts-for-partitioned-tables)
- [ゼロからスケールへ：Langfuseのインフラストラクチャ進化](https://clickhouse.com/blog/202501-newsletter#from-zero-to-scale-langfuses-infrastructure-evolution)
- [ClickHouseを使用したメダリオンアーキテクチャの構築](https://clickhouse.com/blog/202501-newsletter#building-a-medallion-architecture-with-clickhouse)
- [Blueskyデータのためのメダリオンアーキテクチャの構築](https://clickhouse.com/blog/202501-newsletter#building-a-medallion-architecture-for-bluesky-data)
- [クイックリード](https://clickhouse.com/blog/202501-newsletter#quick-reads)
- [ビデオコーナー](https://clickhouse.com/blog/202501-newsletter#video-corner)
- [今月の投稿](https://clickhouse.com/blog/202501-newsletter#post-of-the-month)


 


## 注目のコミュニティメンバー [\#](/jp/blog/202501-newsletter-jp#%E6%B3%A8%E7%9B%AE%E3%81%AE%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC)


今月の注目のコミュニティメンバーは、コミュニティプラットフォームであるSkoolのデータ責任者、[Jason Anderson](https://www.linkedin.com/in/andersonljason/)です。


![featured-member-202501.png](/uploads/featured_member_202501_664885507d.png)

Jason Andersonは、チームを率い、データ駆動型のソリューションを開発してきた経験豊富なデータおよびテクノロジーの専門家です。以前はMythical Gamesのデータ責任者、Comp Threeのパートナーを務め、機械学習、分析、クラウドアーキテクチャに注力していました。彼のキャリアには、IBMやPolySatでの役割も含まれており、クラウドサービスや衛星ソフトウェア開発に貢献しました。



Jasonは最近、[ロサンゼルスのClickHouseミートアップでSkoolでの彼の仕事について発表](https://clickhouse.com/videos/skools-journey-with-clickhouse)しました。Jasonは、1日に1億行以上のデータを処理しながら、非常に高速なクエリを実現するために、PostgresからClickHouseに移行した経緯を説明しました。また、[SkoolでのClickHouseの利用についてより詳細に説明したブログ記事](https://clickhouse.com/blog/how-skool-uses-clickhouse-for-observability-behavioral-analytics)もあります。



[LinkedInでJasonをフォロー](https://www.linkedin.com/in/andersonljason?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter)


  

## 今後のイベント [\#](/jp/blog/202501-newsletter-jp#%E4%BB%8A%E5%BE%8C%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


**グローバルイベント**


- [リリースコール 25\.1](https://clickhouse.com/company/events/v25-1-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) \- 1月28日


**無料トレーニング**


- [ClickHouseクエリ最適化ワークショップ](https://clickhouse.com/company/events/202501-emea-query-optimization?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) \- 1月22日
- [ClickHouseを可観測性に活用する](https://clickhouse.com/company/events/202501-amer-clickhouse-observability?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) \- 1月29日
- [ClickHouseデベロッパー対面トレーニング \- ロンドン、イングランド](https://clickhouse.com/company/events/202502-emea-london-inperson-clickhouse-developer?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) \- 2月4\-5日
- [対面ClickHouseトレーニング](https://clickhouse.com/company/events/202502-emea-dubai-inperson-clickhousetraining?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) \- 2月10日
- [ClickHouseクエリ最適化ワークショップ](https://clickhouse.com/company/events/202502-apj-query-optimization?utm_source=clickhouse&utm_medium=email&utm_campaign=202501-newsletter) (APJ向け時間帯) \- 2月12日


**EMEAのイベント**


- [ロンドンでのミートアップ](https://www.meetup.com/clickhouse-london-user-group/events/305146729/) \- 2月5日
- [ドバイでのミートアップ](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/) \- 2月10日


**APACのイベント**


- [Alibaba Developer Summit Jakarta](https://www.alibabacloud.com/en/events/alibabacloud-developer-summit-2025?_p_lc=1) \- 1月21日
- [東京でのミートアップ](https://www.meetup.com/clickhouse-tokyo-user-group/events/305126993/) \- 1月23日
- [ムンバイでのミートアップ](https://www.meetup.com/clickhouse-mumbai-user-group/events/305497320/) \- 2月1日
- [バンガロールでのミートアップ](https://www.meetup.com/clickhouse-bangalore-user-group/events/305497951/) \- 2月8日
- [Developers Summit Tokyo](https://event.shoeisha.jp/devsumi/20250213) \- 2月13\-14日


 


## 24\.12 リリース [\#](/jp/blog/202501-newsletter-jp#2412-%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)


![release-24.12.png](/uploads/release_24_12_1cf63e9515.png)
2024年の最終リリースでは、Iceberg RESTカタログとスキーマ進化のサポートが導入されました。Apache Icebergの共同作成者である[Daniel Weeks](https://www.linkedin.com/in/daniel-weeks-a1946860/)が24\.12コミュニティコールにゲスト出演しましたので、[録画をぜひご覧ください](https://www.youtube.com/watch?v=bv-ut-Q6vnc)。


Enumの使いやすさの改善、テーブルを列で逆順にソートする実験的な機能、テーブルの主キーとしてのJSONサブカラム、自動JOINの並べ替え、JOIN式の最適化なども含まれています！


[リリース記事を読む](https://clickhouse.com/blog/clickhouse-release-24-12)


 


## ClickHouseを使用したプロダクト分析ソリューションの構築 [\#](/jp/blog/202501-newsletter-jp#clickhouse%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E5%88%86%E6%9E%90%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E6%A7%8B%E7%AF%89)


![building-product-analytics-solution.png](/uploads/building_product_analytics_solution_bfe00baa89.png)
プロダクト分析とは、ユーザーが製品をどのように操作するかに関するデータを収集、分析、解釈することです。



Chloé CarassoはClickHouseのプロダクト分析を主導しており、社内プロダクト分析プラットフォームの構築方法についてブログ記事を執筆しました。



Chloeは、既製のソリューションを購入するのではなく、なぜ自分たちで構築することにしたのかを説明し、この道に興味がある場合に、ClickHouseを活用した分析ソリューションの設計と運用に関するいくつかのアイデアを共有しています。また、コホート分析、ユーザーパス、リテンション/チャーンの測定など、彼女が実行する一般的なクエリも共有しています。



[ブログ記事を読む](https://clickhouse.com/blog/building-product-analytics-with-clickhouse)


 


## パーティション化されたテーブルへのバルクインサートの最適化 [\#](/jp/blog/202501-newsletter-jp#%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3%E3%82%B7%E3%83%A7%E3%83%B3%E5%8C%96%E3%81%95%E3%82%8C%E3%81%9F%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%81%B8%E3%81%AE%E3%83%90%E3%83%AB%E3%82%AF%E3%82%A4%E3%83%B3%E3%82%B5%E3%83%BC%E3%83%88%E3%81%AE%E6%9C%80%E9%81%A9%E5%8C%96)


![optimizing-bulk-inserts.png](/uploads/optimizing_bulk_inserts_b0f86fdc37.png)
Triple Whaleのソフトウェアエンジニアである[Jesse Grodman](https://www.linkedin.com/in/jesse-grodman)が、高度にパーティション化されたClickHouseテーブルにデータを高速にロードするためのヒントをいくつか共有しています。


S3ファイルからテーブルに直接データを書き込み始めましたが、その結果、多くの小さな[parts](https://clickhouse.com/docs/en/parts)が発生し、クエリの観点からは理想的ではなく、[too many partsエラー](https://clickhouse.com/docs/knowledgebase/exception-too-many-parts)が発生する可能性があります。彼は、取り込みクエリの一部としてパーティションキーでデータをソートするなど、この問題を回避するためのさまざまな方法を検討していますが、メモリ不足エラーが発生します。



Jesseは、ClickHouseに書き込む前にパーティションキーでデータをソートする方がはるかに効果的であることを発見しました。彼はまた、最初にデータを非パーティション化されたテーブルにロードし、その後ClickHouseでソートを実行しながらパーティション化されたテーブルにデータを投入することも試しています。



[ブログ記事を読む](https://medium.com/@jgrodman/clickhouse-optimizing-bulk-inserts-for-partitioned-tables-9ea91b3e7c3b)


 


## ゼロからスケールへ：Langfuseのインフラストラクチャ進化 [\#](/jp/blog/202501-newsletter-jp#%E3%82%BC%E3%83%AD%E3%81%8B%E3%82%89%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E3%81%B8langfuse%E3%81%AE%E3%82%A4%E3%83%B3%E3%83%95%E3%83%A9%E3%82%B9%E3%83%88%E3%83%A9%E3%82%AF%E3%83%81%E3%83%A3%E9%80%B2%E5%8C%96)


![from-zero-to-scale.png](/uploads/from_zero_to_scale_4915d25e1f.png)
[Langfuse](https://langfuse.com/)は、Y Combinator Winter 2023バッチに参加したオープンソースのLLM可観測性プラットフォームです。製品の最初のリリースは、Next.js、Vercel、Postgresで記述されました。これにより、迅速なリリースが可能になりましたが、システムをスケールしようとしたときに問題が発生しました。



ブログ記事では、これらの問題を解決するための彼らの道のりを説明しており、それには広範なインフラストラクチャの再設計が含まれていました。スパイキーな取り込みトラフィックを処理するためにRedisキューが導入され、ClickHouse ReplacingMergeTreeテーブルの助けを借りて分析クエリが高速化されました。



[ブログ記事を読む](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution)


 


## ClickHouseを使用したメダリオンアーキテクチャの構築 [\#](/jp/blog/202501-newsletter-jp#clickhouse%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E3%83%A1%E3%83%80%E3%83%AA%E3%82%AA%E3%83%B3%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A3%E3%81%AE%E6%A7%8B%E7%AF%89)


![building-medallion-ch.png](/uploads/building_medallion_ch_222ec65015.png)
メダリオンアーキテクチャは、データレイクハウス内のデータを論理的に整理するデータ設計パターンです。アーキテクチャの各レイヤー（ブロンズ ⇒ シルバー ⇒ ゴールドレイヤーテーブル）をデータが流れるにつれて、データの構造と品質を段階的かつ漸進的に向上させることを目的としています。



ClickHouseプロダクトマーケティングエンジニアリング（PME）チームは、このアーキテクチャがClickHouseのようなリアルタイムデータウェアハウスに適用できるかどうかに関心を持ち、彼らの経験を説明するブログ記事を執筆しました。



[ブログ記事を読む](https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse)


 


## Blueskyデータのためのメダリオンアーキテクチャの構築 [\#](/jp/blog/202501-newsletter-jp#bluesky%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%A1%E3%83%80%E3%83%AA%E3%82%AA%E3%83%B3%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A3%E3%81%AE%E6%A7%8B%E7%AF%89)


![building-medallion-bluesky.png](/uploads/building_medallion_bluesky_266c2b5133.png)
メダリオンアーキテクチャの紹介記事に続いて、ClickHouse PMEチームはこの設計パターンをBlueSkyソーシャルネットワークからのデータに適用しました。



多くのレコードに不正な形式または誤ったタイムスタンプが含まれていたため、これはこの実験に最適なデータセットでした。データセットには頻繁な重複も含まれていました。



ブログでは、これらの課題に対処し、このデータセットをメダリオンアーキテクチャの3つの異なる層（ブロンズ、シルバー、ゴールド）に整理するワークフローについて説明しています。チームは、[最近リリースされたJSON型](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse)も多用しています。



[ブログ記事を読む](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse)


 


## クイックリード [\#](/jp/blog/202501-newsletter-jp#%E3%82%AF%E3%82%A4%E3%83%83%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%89)


- [Hellmar Becker](https://www.linkedin.com/in/hellmarbecker/)が最近ClickHouseに入社し、その機能を試しています。彼の最初のブログ記事では、[配列処理関数](https://blog.hellmar-becker.de/2025/01/01/new-years-greetings-from-the-data-cookbook-elf/)について探求し、2番目の記事では、ClickHouseで[線形代数を行う方法](https://blog.hellmar-becker.de/2025/01/05/clickhouse-data-cookbook-linear-algebra-in-sql/)を解説しています。
- [Hardik Singh Behl](https://www.linkedin.com/in/hardiksinghbehl/)は、[ClickHouseをSpring Bootアプリケーションに統合する方法](https://www.baeldung.com/spring-boot-olap-clickhouse-database)を探求しています。彼は最初にアプリケーションを設定し、データベース接続を確立してから、いくつかのCRUD操作を実行しています。
- Andrei Tserakhauは、オープンソースのクラウドネイティブな取り込みエンジンであるTransferを使用して、[MySQLからClickHouseにデータを転送する方法](https://medium.com/@laskoviymishka/cdc-from-mysql-to-clickhouse-c791fe414fe1)を示しています。
- [Shivji kumar Jha](https://www.linkedin.com/in/shivjijha/)は、トランザクションの信頼性と高速分析のバランスを取りながら、[PostgresとClickHouseが統合されたデータ管理ソリューションとしてどのように連携できるか](https://www.linkedin.com/pulse/unified-data-platforms-ft-postgres-clickhouse-shivji-kumar-jha-jylqc/)を探求しています。


 


## ビデオコーナー [\#](/jp/blog/202501-newsletter-jp#%E3%83%93%E3%83%87%E3%82%AA%E3%82%B3%E3%83%BC%E3%83%8A%E3%83%BC)


- [All Things Open 2024 conference](https://2024.allthingsopen.org/speakers)では、2名のClickHouseスピーカーが登壇しました。Tanya Braginは、モノリシックなクラウドデータウェアハウスの代替案を提供することで、[オープンソース技術とデータレイク標準が最新のデータスタックをどのように変革しているか](https://clickhouse.com/videos/all-things-open-open-source-cloud-datawarehouse)を探求しました。
- Zoe Steinkampは、従来の行ベースシステムよりも優れたパフォーマンスを提供することで、[列指向データベースがデータウェアハウジングと分析に革命を起こしているか](https://clickhouse.com/videos/all-things-open-columnar-storage)を説明しました。Zoeはまた、コストを削減し、クエリパフォーマンスを向上させながら、Apache Arrow、Parquet、Pandasなどのツールを使用して効率的な分析アプリケーションを構築する方法も実演しました。/li\>
- Markは、ClickHouse Server、clickhouse\-local、chDBなど、[ClickHouseのさまざまなデプロイメントモード](https://www.youtube.com/watch?v=EOXEW_-r10A&t=5s)について説明しました。
- Avi Pressは、Scarfがどのように[毎日約25GBのデータと5000万件のイベントを処理するClickHouseをバックエンドとしたデータパイプラインを構築したか](https://clickhouse.com/videos/open-source-scarf)を説明しています。


 


## 今月の投稿 [\#](/jp/blog/202501-newsletter-jp#%E4%BB%8A%E6%9C%88%E3%81%AE%E6%8A%95%E7%A8%BF)


今月のお気に入りの投稿は、[Dmytro Shevchenko](https://x.com/dschewchenko1/status/1872671222569271573)によるものです。


![post-of-month-202501.png](/uploads/post_of_month_202501_cb6b65fa1c.png)

[投稿を読む](https://x.com/dschewchenko1/status/1872671222569271573)
