# 2025年4月ニュースレター


こんにちは、そして2025年4月のClickHouseニュースレターへようこそ！


今月は、CloudQueryがClickHouseを6ヶ月間使用した説得力のある体験レポート、25\.3で強力な新しいクエリ条件キャッシュの発表、1年間のRust開発の振り返り、HyperDXの戦略的買収の発表などをお届けします！


## 注目のコミュニティメンバー: Julian LaNeve [\#](/jp/blog/202504-newsletter-jp#featured-community-member)


今月の注目のコミュニティメンバーは、AstronomerのCTOであるJulian LaNeveです。


![0_april.png](/uploads/0_april_f7df5dfe00.png)
2023年11月にCTOに就任する前は、製品チームに所属し、開発者体験、データ可観測性、オープンソースイニシアチブに注力していました。特に、データパイプラインの作成用に設計されたノートブックツールであるAstronomerのCloud IDEの立ち上げを主導しました。


Julianは最近、Astronomerが新しいデータ可観測性プラットフォームであるAstro Observeの基盤としてClickHouse Cloudを選んだ理由について説明するブログ記事を執筆しました。ClickHouseの、高速なクエリパフォーマンスと最小限のメンテナンス要件で数十億のAirflowワークフローイベントを処理できる能力が、彼らのデータベースの選択の決め手となりました。Julianはまた、[2024年11月のニューヨークClickHouseミートアップ](https://clickhouse.com/blog/why-astronomer-chose-clickhouse-to-power-its-new-data-observability-platform-astro-observe)でも同じトピックについて発表しました。


➡️ [LinkedInでJulianをフォロー](https://www.linkedin.com/in/julianlaneve/)


## 今後のイベント [\#](/jp/blog/202504-newsletter-jp#upcoming-events)


5月29日にサンフランシスコで開催される[Open House, The ClickHouse User Conference](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)まであと1ヶ月強となり、最初の講演者の発表を開始しました。


OpenAIのCPOであるKevin Weilと、Andreessen HorowitzのパートナーであるMartin Casadoが、ClickHouseのCEOであるAaron Katzと共に、大規模AIのためのデータインフラストラクチャの未来について炉辺談話を行います。


Weights \& Biasesの創業者兼CEOであるLukas Biewaldも参加し、AIの未来と、次世代AIアプリを強化するClickHouseのような高性能データベースの役割について議論します。


➡️ [Open Houseに登録](https://clickhouse.com/openhouse?utm_source=marketo&utm_medium=email&utm_campaign=newsletter)


### グローバルイベント [\#](/jp/blog/202504-newsletter-jp#%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [v25\.4 コミュニティコール](https://clickhouse.com/company/events/v25-4-community-release-call) \- 4月22日


### 無料トレーニング [\#](/jp/blog/202504-newsletter-jp#%E7%84%A1%E6%96%99%E3%83%88%E3%83%AC%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0)


- [ClickHouse Fundamentals \- バーチャル](https://clickhouse.com/company/events/202504-emea-clickhouse-fundamentals) \- 4月22日
- [対面 BigQuery to ClickHouse \- ジャカルタ](https://clickhouse.com/company/events/202504-apj-jakarta-inperson-bigquery-to-clickhouse) \- 4月22日
- [ClickHouseを可観測性に活用する](https://clickhouse.com/company/events/202505-amer-clickhouse-observability) \- 5月7日
- [ClickHouse Fundamentals \- バーチャル](https://clickhouse.com/company/events/clickhouse-fundamentals) \- 5月13日
- [対面 ClickHouse Developer Fast Track \- ミュンヘン](https://clickhouse.com/company/events/202505-emea-munich-inperson-developer-fast-track) \- 5月14日
- [ClickHouse Developer Training \- バーチャル](https://clickhouse.com/company/events/202505-amer-clickhouse-developer) \- 5月21日


### AMERのイベント [\#](/jp/blog/202504-newsletter-jp#amer%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [デンバーでのClickHouseミートアップ](https://www.meetup.com/clickhouse-denver-user-group/events/306934991/) \- 4月23日


### EMEAのイベント [\#](/jp/blog/202504-newsletter-jp#emea%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [AWS Summit 2025, ロンドン](https://clickhouse.com/company/events/04-2025-aws-london) \- 4月30日
- [AWS Summit 2025, ポーランド](https://clickhouse.com/company/events/202505-EMEA-Poland-AWS-Summit-MeetingRequests) \- 5月6日
- [ロンドンでのClickHouseミートアップ](https://www.meetup.com/clickhouse-london-user-group/events/306047172/) \- 5月13日
- [ClickHouse Happy Hour ミュンヘン](https://clickhouse.com/company/events/202505-EMEA-Munich-HappyHour) \- 5月14日
- [イスタンブールでのClickHouseミートアップ](https://www.meetup.com/clickhouse-turkiye-meetup-group/events/306978337/) \- 5月14日


### APACのイベント [\#](/jp/blog/202504-newsletter-jp#apac%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [ジャカルタでのClickHouseミートアップ \- AI Night!](https://www.meetup.com/clickhouse-indonesia-user-group/events/306973747/) \- 4月22日
- [AWS Summit ベンガルール](https://aws.amazon.com/events/summits/bengaluru/) \- 5月7〜8日
- [AWS Summit 香港](https://aws.amazon.com/events/summits/hongkong/) \- 5月8日
- [Data Engineering Summit](https://des.analyticsindiamag.com/), ベンガルール \- 5月15〜16日


## 25\.3 リリース [\#](/jp/blog/202504-newsletter-jp#release)


![1_april.png](/uploads/1_april_706d25bab0.png)
25\.3リリースの私のお気に入りの機能は、[クエリ条件キャッシュ](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache)です。これは、`WHERE`句に一致するデータの範囲をキャッシュします。これは、複数のクエリの全体的な形状は異なるものの、フィルタリング条件が同じであるダッシュボードや可観測性のユースケースで役立ちます。


このリリースでは、AWS GlueおよびUnityカタログの読み取りサポート、新しい配列関数、外部データの自動並列化が追加されています。最後に、JSONデータ型が本番環境に対応しました！


➡️ [リリース記事を読む](https://clickhouse.com/blog/clickhouse-release-25-03)


## CloudQueryでのClickHouseの6ヶ月間（良い点、悪い点、そして予想外の点） [\#](/jp/blog/202504-newsletter-jp#six-months-clickhouse)


![2_april.png](/uploads/2_april_e9f4a4925d.png)
Herman SchaafとJoe Karlssonは、クラウド資産インベントリのデータベースバックエンドとしてClickHouseを6ヶ月間使用した経験を共有しました。


彼らの主な洞察には、参照データにJOINを使用する場合と辞書を使用する場合の理解、クエリパフォーマンスのためのソートキーの適切な設計の重要性、カスタムスナップショットテーブルの作成につながったマテリアライズドビューの制限、ロギングおよび可観測性データに対するClickHouseの驚くべき汎用性などがあります。


いくつかの課題にもかかわらず、CloudQueryは、ClickHouseがクラウドガバナンスプラットフォームの速度とスケーラビリティに関する約束を果たしたことを発見しました。


➡️ [ブログ記事を読む](https://www.cloudquery.io/blog/six-months-with-clickhouse-at-cloudquery)


## ClickHouseにおけるRustの1年間 [\#](/jp/blog/202504-newsletter-jp#year-of-rust)


![3_april.png](/uploads/3_april_b8aa814052.png)
ClickHouseのCTOであるAlexey Milovidovは、Rustを彼らのコードベースに統合することについてのブログを書いています。


この取り組みは、Delta Lakeのサポートなどのより実用的な機能を実装する前に、（コミュニティメンバーからの貢献による）BLAKE3やPRQLのような小さなコンポーネントから始まりました。


この過程を通じて、ビルドシステムの統合、サニタイザーの互換性、クロスコンパイルの問題、シンボルサイズの肥大化など、多くの技術的な課題が解決されました。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/rust)


## ClickHouseによるスケーラブルなEDR高度エージェント分析 [\#](/jp/blog/202504-newsletter-jp#scalable-edr-analytics)


![7_april.png](/uploads/7_april_c5df7e0bec.png)
Huntressは、EDR分析機能を強化するためにClickHouseを実装しました。ClickHouseを使用することで、数百万のエンドポイントにわたる数十億のデータポイントを毎日処理しながら、高速なクエリパフォーマンスを維持できるようになりました。


この実装では、エージェントの健全性と安定性を効率的に監視するために、[AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree)と[マテリアライズドビュー](https://clickhouse.com/docs/materialized-view/incremental-materialized-view)を活用しています。


➡️ [ブログ記事を読む](https://www.huntress.com/blog/scalable-edr-advanced-agent-analytics-with-clickhouse)


## ClickHouseがHyperDXを買収：オープンソース可観測性の未来 [\#](/jp/blog/202504-newsletter-jp#clickhouse-hyperdx)


![4_april.png](/uploads/4_april_f55fe2c585.png)
ClickHouseは、ClickHouse上に構築された完全にオープンソースの可観測性プラットフォームであるHyperDXを買収しました。


この買収により、開発者や企業に効率的でスケーラブルな可観測性ソリューションを提供する能力が強化されます。HyperDXのUIとセッションリプレイ機能をClickHouseのデータベースパフォーマンスと組み合わせることで、オープンソースの可観測性製品を強化しています。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability)


## Make Before Break \- ClickHouse Cloudのより高速なスケーリングメカニズム [\#](/jp/blog/202504-newsletter-jp#make-before-break)


![5_april.png](/uploads/5_april_bafbeed1b7.png)
Jayme BirdとManish Gillは、以前のスケーリング方法の制限に対処するためにClickHouse Cloudに導入された「Make Before Break」（MBB）スケーリングアプローチに関するブログ記事を執筆しました。


当初、ClickHouse Cloudは単一のStatefulSetを使用してすべてのサーバーレプリカを管理しており、スケーリング中に数時間かかるローリング再起動が必要でした。MBBアプローチでは、古いポッドを削除する前に、必要なリソースを持つ新しいポッドを作成することで、スケーリング操作中のダウンタイムを排除します。


これには、各ポッドが独自のStatefulSetとカスタムKubernetesコントローラーによって管理され、移行を調整するMultiSTSアーキテクチャの開発が必要でした。技術的な課題にもかかわらず、チームはフリート全体をこの新しいアーキテクチャに正常に移行し、スケーリング時間を大幅に改善し、顧客の中断を減らしました。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/make-before-break-faster-scaling-mechanics-for-clickhouse-cloud)


## クイックリード [\#](/jp/blog/202504-newsletter-jp#quick-reads)


- Hossein Kohzadiは、[.NETアプリケーションでClickHouseを使用する方法](https://itnext.io/integrating-clickhouse-with-net-a-comprehensive-guide-to-blazing-fast-analytics-3e178503d54e)について説明するブログ記事を書いています。
- Roman Ianvarevは、ClickHouseクエリログを分析し、dbtプロジェクトのインテリジェントな最適化の推奨事項を提供するコマンドラインツールである[QuerySightを紹介](https://medium.com/@rianvarev/introducing-querysight-a-query-driven-approach-to-data-warehouse-development-5f29b4bde4be)しています。
- Raj Kantariaは、ClickHouse MCP Serverを例として使用して、[AnthropicのModel Context Protocolを簡単に紹介](https://medium.com/@kantariyaraj/talk-to-your-database-with-mcp-88cf2468851d)しています。
- Tom Schreiberは、BlueSkyデータセットを使用して、[JSONデータに対するClickHouseクエリを高速化](https://clickhouse.com/blog/accelerating-clickhouse-json-queries-for-fast-bluesky-dashboards)する方法を解説しています。
- Keshav Agrawalは、[Go、Kafka、ClickHouse、およびApache Supersetを使用したリアルタイムデータパイプライン](https://www.akitmcs.com/post/building-a-real-time-data-pipeline-with-go-kafka-clickhouse-and-apache-superset)を構築しています。


## 今月の投稿 [\#](/jp/blog/202504-newsletter-jp#post-of-the-month)


今月のお気に入りの投稿は、Delta Lakeカタログからの読み取りに対するClickHouseのサポートを試している[Andi Pangeran](https://x.com/A_Pangeran)によるものです。


![6_april.png](/uploads/6_april_c0fe0f49cb.png)
➡️ [投稿を読む](https://x.com/A_Pangeran/status/1904807887463211506)
