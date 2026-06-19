# 2025年3月ニュースレター


北半球の天気は春の訪れを迷っているようですが、3月のClickHouseニュースレターの時期であることに疑いの余地はありません。


今月は、ClickPipesのPostgres CDCコネクタがパブリックベータ版となり、AWSでのBring Your Own Cloudの一般提供開始を発表しました。Apache IcebergのClickHouseサポートの最新情報、コンタクトセンター分析用のClickHouseベースのデータウェアハウスの構築方法、Theta Sketchesによる訪問者セグメンテーションなどをご紹介します！


## 注目のコミュニティメンバー: Matteo Pelati [\#](/jp/blog/202503-newsletter-jp#%E6%B3%A8%E7%9B%AE%E3%81%AE%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC-matteo-pelati)


今月の注目のコミュニティメンバーは、[LangDB](https://langdb.ai/)の共同創業者であるMatteo Pelatiです。


![0_march2025.png](/uploads/0_march2025_dea5945f2b.png)
LangDBを設立する前は、MatteoはGoldman Sachsでプロダクトデータエンジニアリングのグローバルヘッド、DBS Bankでデータプラットフォームテクノロジーのエグゼクティブディレクターとして上級管理職を務め、130人以上のエンジニアのチームを率いて銀行全体のデータプラットフォームを構築しました。


LangDBは、エンタープライズ対応の機能を備えた250以上のLLMへの即時アクセスを提供する、フル機能のマネージドAIゲートウェイです。ClickHouseを基盤となるデータストアとして使用し、すべてのAIゲートウェイデータ、トレース、分析が保存されます。また、ClickHouseのカスタムUDF機能を利用して、SQLクエリからの直接的なAIモデル呼び出しを可能にし、構造化データ分析とAI機能をシームレスに統合します。


Mateoは最近、[シンガポールのClickHouseミートアップでLangDBについて発表](https://clickhouse.com/videos/singapore-meetup-langdb-building-intelligent-applications-with-clickhouse)し、組織がこの統合を活用して、データインフラストラクチャと分析パイプラインを完全に制御しながら、高度なAIアプリケーションを構築する方法を実演しました。


➡️ [LinkedInでMateoをフォロー](https://www.linkedin.com/in/matteopelati/)


## 今後のイベント [\#](/jp/blog/202503-newsletter-jp#%E4%BB%8A%E5%BE%8C%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


今年最大のイベントである[Open House, The ClickHouse User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)が5月28〜29日にサンフランシスコで開催されるまで、あと2ヶ月強です。


技術的な詳細な解説、トップClickHouseユーザーによるユースケースのプレゼンテーション、創業者からの最新情報、そして他のClickHouseユーザーとの交流の1日をご一緒しましょう。ClickHouse初心者から経験豊富なユーザーまで、どなたにとっても役立つ情報があります。


➡️ [Open Houseに登録](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)


### グローバルイベント [\#](/jp/blog/202503-newsletter-jp#%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [v25\.3 コミュニティコール](https://clickhouse.com/company/events/v25-3-community-release-call) \- 3月20日


### 無料トレーニング [\#](/jp/blog/202503-newsletter-jp#%E7%84%A1%E6%96%99%E3%83%88%E3%83%AC%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0)


- [対面ClickHouseデベロッパー \- シドニー](https://clickhouse.com/company/events/202503-apj-sydney-inperson-clickhouse-developer) \- 3月24〜25日
- [対面ClickHouseデベロッパートレーニング \- サンパウロ、ブラジル](https://clickhouse.com/company/events/202503-latam-sao-paulo-inperson-clickhouse-developer) \- 3月25〜26日
- [対面ClickHouseデベロッパー \- メルボルン](https://clickhouse.com/company/events/202503-apj-melbourne-inperson-clickhouse-developer) \- 3月27〜28日
- [対面ClickHouseデベロッパーファストトラック \- バンガロール](https://clickhouse.com/company/events/202504-apj-bangalore-inperson-developer-fast-track) \- 4月1日
- [BigQuery to ClickHouseワークショップ \- バーチャル](https://clickhouse.com/company/events/202504-emea-clickhouse-bigquery-workshop) \- 4月1日
- [対面ClickHouseデベロッパートレーニング \- ウィーン、オーストリア](https://clickhouse.com/company/events/202504-emea-vienna-inperson-clickhouse-developer) \- 4月7〜8日
- [ClickHouseを可観測性に活用する \- バーチャル](https://clickhouse.com/company/events/202504-apj-clickhouse-observability) \- 4月15日
- [ClickHouse Fundamentals \- バーチャル](https://clickhouse.com/company/events/202504-emea-clickhouse-fundamentals) \- 4月22日


### AMERのイベント [\#](/jp/blog/202503-newsletter-jp#amer%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [ClickHouse Meetup @ Klaviyo](https://www.meetup.com/clickhouse-boston-user-group/events/305882607/?slug=clickhouse-boston-user-group&eventId=300907870&isFirstPublish=true), ボストン \- 3月25日
- [サンパウロでのClickHouseミートアップ](https://www.meetup.com/clickhouse-brasil-user-group/events/306385974/) \- 3月25日
- [ClickHouse Meetup @ Braze](https://www.meetup.com/clickhouse-new-york-user-group/events/305916369/?eventOrigin=group_upcoming_events), ニューヨーク \- 3月26日
- [DCでのClickHouse立ち上げミートアップ](https://www.meetup.com/clickhouse-dc-user-group/events/306439995/) \- 3月27日
- [Google Next](https://clickhouse.com/company/events/2025-04-google-next), ラスベガス \- 4月9日
- [Open House User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter), サンフランシスコ \- 5月28〜29日


### EMEAのイベント [\#](/jp/blog/202503-newsletter-jp#emea%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [チューリッヒでのClickHouseミートアップ](https://www.meetup.com/clickhouse-switzerland-meetup-group/events/306435122/) \- 3月24日
- [ブダペストでのClickHouseミートアップ](https://www.meetup.com/clickhouse-hungary-user-group/events/306435234/) \- 3月25日
- [KubeCon 2025](https://clickhouse.com/company/events/04-2025-kubecon-london), ロンドン \- 4月1〜4日
- [オスロでのClickHouseミートアップ](https://clickhouse.com/company/events/202504-emea-oslo-meetup) \- 4月8日
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-paris), パリ \- 4月9日
- [AWS Summit 2025](https://clickhouse.com/company/events/2025-04-aws-summit-amsterdam), アムステルダム \- 4月16日
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-london), ロンドン \- 4月30日


### APACのイベント [\#](/jp/blog/202503-newsletter-jp#apac%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [デリーでのClickHouseミートアップ](https://www.meetup.com/clickhouse-delhi-user-group/events/306253492/), インド \- 3月22日
- [シドニーでのClickHouseミートアップ](https://www.meetup.com/clickhouse-australia-user-group/events/306549810/) \- 4月1日
- [Latency Conference](https://latencyconf.io/), オーストラリア \- 4月3〜4日
- [TEAMZ Web3/AI Summit](https://web3.teamz.co.jp/en), 日本 \- 4月16〜17日


## 25\.2 リリース [\#](/jp/blog/202503-newsletter-jp#252-%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)


![1_march2025.png](/uploads/1_march2025_efc9bd623e.png)
ClickHouse 25\.2では、joinのパフォーマンスがさらに向上しています。並列ハッシュjoinシステムがさらに最適化され、100%のCPUコア利用率を確保しています。Tom Schreiberが、これがどのように達成されたかを説明しています。


このリリースでは、Parquet Bloomフィルタ、新しいバックアップデータベースエンジン、Delta Rust Kernelとの統合、リアルタイムデータ消費のための拡張されたHTTPストリーミング機能なども導入されています！


➡️ [リリース記事を読む](https://clickhouse.com/blog/clickhouse-release-25-02)


## ClickPipesのPostgres CDCコネクタがパブリックベータ版に [\#](/jp/blog/202503-newsletter-jp#clickpipes%E3%81%AEpostgres-cdc%E3%82%B3%E3%83%8D%E3%82%AF%E3%82%BF%E3%81%8C%E3%83%91%E3%83%96%E3%83%AA%E3%83%83%E3%82%AF%E3%83%99%E3%83%BC%E3%82%BF%E7%89%88%E3%81%AB)


![2_march2025.png](/uploads/2_march2025_5d2086949f.png)
ClickPipesのPostgres CDCコネクタがパブリックベータ版となり、数回のクリックだけでPostgreSQLデータベースからClickHouse Cloudへのシームレスなレプリケーションが可能になりました。


このコネクタは、10倍高速な初期ロードのための並列スナップショットや、ほぼリアルタイムのデータの鮮度など、高性能な機能を備えています。


SyntageやNeonなどの組織ではすでにテラバイト規模の移行が成功しています。パブリックベータ期間中、この強力な統合ツールはすべてのユーザーが無料で使用できます。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta)


## 高カーディナリティメトリクスにおけるClickHouseとGrafana [\#](/jp/blog/202503-newsletter-jp#%E9%AB%98%E3%82%AB%E3%83%BC%E3%83%87%E3%82%A3%E3%83%8A%E3%83%AA%E3%83%86%E3%82%A3%E3%83%A1%E3%83%88%E3%83%AA%E3%82%AF%E3%82%B9%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8Bclickhouse%E3%81%A8grafana)


Tomer Ben Davidは、ClickHouseとGrafanaが、個々のユーザーセッション、コンテナID、地理的な場所など、多数の一意のディメンションにわたるデータを追跡する際の一般的な課題である高カーディナリティメトリクスを効果的に処理する方法を探求しています。


この記事では、ClickHouseの列指向ストレージ、ベクトル化されたクエリ実行、効率的な圧縮機能が、大量の粒度の細かいデータを処理するのにいかに理想的であるかを詳しく説明しています。Grafanaは、このデータを実用的なものにするための強力な可視化、テンプレート機能、アラート機能を提供します。


Tomerはまた、データ集約テクニック、次元削減、ソースでの事前集約など、高カーディナリティを管理するための実践的な戦略も提供しています。


➡️ [ブログ記事を読む](https://medium.com/@Tom1212121/clickhouse-grafana-for-high-cardinality-metrics-4fc3708ba617)


## ClickHouseとIcebergを登る [\#](/jp/blog/202503-newsletter-jp#clickhouse%E3%81%A8iceberg%E3%82%92%E7%99%BB%E3%82%8B)


![3_march2025.png](/uploads/3_march2025_9f42276fd5.png)
Melvyn Peignonは、データレイクとレイクハウスのエコシステムにおけるClickHouseの進化する役割を探求し、データレイクからのデータロード、アドホッククエリ、レイクデータの頻繁なクエリという3つの主要な統合パターンを強調しています。


彼はまた、カタログ統合の拡張によるデータレイククエリのユーザーエクスペリエンスの向上、IcebergおよびDelta形式の書き込みサポートを含むデータレイク操作機能の改善、ClickPipesでのIceberg CDCコネクタの開発という3つの主要な分野に焦点を当てた、レイクハウス統合に関するClickHouseの2025年のロードマップの概要を示しています。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/climbing-the-iceberg-with-clickhouse)


## CrestaがClickHouseでリアルタイムインサイトをどのようにスケールしているか [\#](/jp/blog/202503-newsletter-jp#cresta%E3%81%8Cclickhouse%E3%81%A7%E3%83%AA%E3%82%A2%E3%83%AB%E3%82%BF%E3%82%A4%E3%83%A0%E3%82%A4%E3%83%B3%E3%82%B5%E3%82%A4%E3%83%88%E3%82%92%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B%E3%81%8B)


![4_march2025.png](/uploads/4_march2025_1bf99b75a7.png)
Xiaoyi Ge、Daniel Hoske、Florin Szilagyiは、コンタクトセンター分析を処理するための主要なデータウェアハウスソリューションとしてのCrestaのClickHouseの実装について説明するブログ記事を執筆しました。PostgreSQLからの移行後、リアルタイム集計、生イベントストレージ、可観測性のための3つの専用クラスターで、1日あたり数千万件のレコードを処理しながら、ストレージコストを50%削減しました。


このプラットフォームは現在、CrestaのDirector UIを強化し、エンタープライズ顧客は柔軟な時間範囲で数十億件のレコードをクエリしながら、リアルタイムのコンタクトセンターインサイトのために応答性の高いパフォーマンスを維持できます。


彼らはまた、クエリパターンに合わせた慎重なスキーマ設計、頻繁なクエリのためのマテリアライズドビューの活用、特定のクエリを高速化するためのClickHouseのスパースインデックスとブルームフィルターの利用など、主要な最適化戦略も共有しました。


➡️ [ブログ記事を読む](https://cresta.com/blog/how-cresta-scales-real-time-insights-with-clickhouse/)


## AWSでのClickHouse BYOC（Bring Your Own Cloud）の一般提供開始を発表 [\#](/jp/blog/202503-newsletter-jp#aws%E3%81%A7%E3%81%AEclickhouse-byocbring-your-own-cloud%E3%81%AE%E4%B8%80%E8%88%AC%E6%8F%90%E4%BE%9B%E9%96%8B%E5%A7%8B%E3%82%92%E7%99%BA%E8%A1%A8)


![5_march2025.png](/uploads/5_march2025_cd7c95fba4.png)
AWSでのBYOC（Bring Your Own Cloud）が一般提供開始となり、企業はすべてのデータを独自のAWS VPC環境内に保持しながら、ClickHouse Cloudを実行できるようになりました。


AWSとの5年間の戦略的提携の一部であるこのデプロイメントモデルにより、組織はClickHouseのマネージドサービス機能の恩恵を受けながら、完全なデータ制御とセキュリティコンプライアンスを維持できます。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/announcing-general-availability-of-clickhouse-bring-your-own-cloud-on-aws)


## PostgresからClickHouseへ：データモデリングのヒント V2 [\#](/jp/blog/202503-newsletter-jp#postgres%E3%81%8B%E3%82%89clickhouse%E3%81%B8%E3%83%87%E3%83%BC%E3%82%BF%E3%83%A2%E3%83%87%E3%83%AA%E3%83%B3%E3%82%B0%E3%81%AE%E3%83%92%E3%83%B3%E3%83%88-v2)


![6_march2025.png](/uploads/6_march2025_461dacaee6.png)
Lionel PalacinとSai Srirampurは、Change Data Capture（CDC）を使用してPostgreSQLからClickHouseにデータを移行するための包括的なガイドを提供しています。この記事では、ClickPipesとPeerDBがPostgresでの挿入、更新、削除の継続的な追跡をどのように可能にし、ClickHouseのReplacingMergeTreeエンジンを通じてデータの整合性を維持しながら、リアルタイム分析のためにClickHouseにそれらをレプリケートするかを説明しています。


著者は、FINALキーワード、ビュー、マテリアライズドビューを使用した重複排除アプローチを含む、パフォーマンスを最適化するためのいくつかの戦略を詳しく説明しています。また、カスタム順序付けキー、JOINの最適化、リフレッシュ可能および増分マテリアライズドビューを使用した非正規化テクニックなどの高度なトピックも探求しています。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2)


## クイックリード [\#](/jp/blog/202503-newsletter-jp#%E3%82%AF%E3%82%A4%E3%83%83%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%89)


- Corootは、[ClickHouseネイティブおよびZooKeeperプロトコルのサポートを追加](https://coroot.com/blog/engineering/coroot-v1-7-monitoring-clickhouse-and-zookeeper-with-ebpf/)し、これらの分散システムの監視を大幅に容易にしました。
- Keshav Agrawalは、データ生成にGo、メッセージキューイングにKafka、高性能ストレージにClickHouse、可視化にApache Supersetを組み合わせた[スケーラブルなリアルタイムデータパイプラインの構築方法](https://www.akitmcs.com/post/building-a-real-time-data-pipeline-with-go-kafka-clickhouse-and-apache-superset)を実演し、ストリーミングデータとバッチデータの両方を処理するための完全なソリューションを提供しています。
- GrafanaのLokiがWebログ分析に不十分であると判断した後、Scott Lairdは[ClickHouseへの移行](https://scottstuff.net/posts/2025/02/27/caddy-logs-in-clickhouse-via-vector/)を記録しています。彼のガイドは、適切な認証によるClickHouseのセットアップ、CaddyのJSONログに適したスキーマの作成、ログを変換してClickHouseにストリーミングするためのデータパイプラインミドルウェアとしてのVectorの構成に関するステップバイステップの手順を提供しています。
- [sateesh.pyによるチュートリアル](https://sateeshpy.medium.com/building-a-scalable-etl-pipeline-data-warehouse-with-apache-spark-minio-and-clickhouse-0154342872e9)では、データ処理にApache Spark、S3互換ストレージにMinIO、データストレージにDelta Lake、高速分析クエリにClickHouseを組み合わせた最新のETLパイプラインを構築する方法をコード例とともに示しています。
- Hellmar Beckerは、[ClickHouseのtheta sketchesを使用して、訪問者のセグメンテーションと集合演算を行う方法](https://blog.hellmar-becker.de/2025/03/09/clickhouse-data-cookbook-visitor-segmentation-with-theta-sketches/%20)を実演し、異なるコンテンツセグメントにわたるユニークな訪問者を効率的にカウントすると同時に、積集合や和集合などのより複雑な演算も実行しています。


## 今月の投稿 [\#](/jp/blog/202503-newsletter-jp#%E4%BB%8A%E6%9C%88%E3%81%AE%E6%8A%95%E7%A8%BF)


今月のお気に入りの投稿は、ClickHouseの圧縮機能を気に入っている[Chris Elgee](https://x.com/chriselgee)によるものです。


![7_march2025.png](/uploads/7_march2025_5110d40afa.png)
➡️ [投稿を読む](https://x.com/chriselgee/status/1894760925527245261)
