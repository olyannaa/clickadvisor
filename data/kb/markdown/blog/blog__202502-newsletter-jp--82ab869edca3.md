# 2025年2月ニュースレター


1月はあっという間に過ぎましたね！ということは、2025年2回目のニュースレターの時間です。


今月の大きなニュースは、JSON分析のためのベンチマークスイートであるJSONBenchのリリースです。Ryadh Dahimeneがエージェント向けの分析について語り、Shahar GvirtzがClickHouseを気に入る理由を説明し、Tom Schreiberが25\.1でのjoinの改善点について深く掘り下げています。その他にも多くの情報があります。


## 注目のコミュニティメンバー: Chris Lawrence [\#](/jp/blog/202502-newsletter-jp#%E6%B3%A8%E7%9B%AE%E3%81%AE%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC-chris-lawrence)


今月の注目のコミュニティメンバーは、[AMP](https://www.linkedin.com/company/use-amp/)のDev Lead兼シニアソフトウェアエンジニアであるChris Lawrenceです。


![1_newsletter202502.png](/uploads/1_newsletter202502_4f144a0657.png)
Chrisは以前、ReSync Digitalを共同設立し、初期段階のスタートアップ向けに30以上の製品を成功裏に立ち上げました。また、Skip\-Line, LLCでの仕事を通じて、マシンビジョンとIoTソリューションの経験も持っています。


Chris Lawrenceは、[2024年8月にメルボルンで開催されたClickHouseミートアップで講演](https://clickhouse.com/videos/amp-from-batch-processing-to-streaming)しました。彼は、AMPのClickHouse Cloudの実装が、データパイプラインをバッチ処理からリアルタイムストリーミングにどのように変革し、分析プラットフォームの速度と信頼性を向上させたかを共有しました。Chrisはまた、[最近のブログ記事](https://clickhouse.com/blog/amp-clickhouse-oss-to-clickhouse-cloud)で彼の講演について詳しく説明しています。


➡️ [LinkedInでChrisをフォロー](https://www.linkedin.com/in/chrislawrence121/)


## 今後のイベント [\#](/jp/blog/202502-newsletter-jp#%E4%BB%8A%E5%BE%8C%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


### グローバルイベント [\#](/jp/blog/202502-newsletter-jp#%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [v25\.2 コミュニティコール](https://clickhouse.com/company/events/v25-2-community-release-call) \- 2月27日


### 無料トレーニング [\#](/jp/blog/202502-newsletter-jp#%E7%84%A1%E6%96%99%E3%83%88%E3%83%AC%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0)


- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals) \- 2月26日、3月19日
- [Formation ClickHouse en présentiel](https://clickhouse.com/company/events/202503-emea-paris-inperson-clickhousetraining), パリ \- 3月4日
- [In\-Person ClickHouse Developer Fast Track \- シアトル](https://clickhouse.com/company/events/202503-amer-seattle-inperson-developer-fast-track) \- 3月5日
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202503-emea-query-optimization) \- 3月12日
- [ClickHouse Admin Workshop](https://clickhouse.com/company/events/202503-amer-clickhouse-admin-workshop) \- 3月12日
- [In\-Person ClickHouse Developer \- シドニー](https://clickhouse.com/company/events/202503-apj-sydney-inperson-clickhouse-developer) \- 3月24\-25日
- [In\-Person ClickHouse Developer \- メルボルン](https://clickhouse.com/company/events/202503-apj-melbourne-inperson-clickhouse-developer) \- 3月27\-28日
- [In\-Person ClickHouse Developer Fast Track \- バンガロール](https://clickhouse.com/company/events/202504-apj-bangalore-inperson-developer-fast-track) \- 4月1日


### AMERのイベント [\#](/jp/blog/202502-newsletter-jp#amer%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [Clickhouse Meetup with LA DevOps](https://www.meetup.com/clickhouse-los-angeles-user-group/events/305952193/?slug=clickhouse-los-angeles-user-group&isFirstPublish=true) \- 2月20日
- [ClickHouse Meetup in Seattle](https://www.meetup.com/clickhouse-seattle-user-group/events/305916325/?eventOrigin=your_events) \- 3月5日
- [Scale 22x](https://clickhouse.com/company/events/2025-03-scale-22), パサデナ \- 3月6日 \- 3月9日
- [Game Developers Conference](https://clickhouse.com/company/events/03-2025-san-francisco), サンフランシスコ \- 3月17日
- [ClickHouse Meetup @ Cloudflare](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/306046697/?eventOrigin=group_events_list), サンフランシスコ \- 3月19日
- [ClickHouse Meetup @ Klaviyo](https://www.meetup.com/clickhouse-boston-user-group/events/305882607/?slug=clickhouse-boston-user-group&eventId=300907870&isFirstPublish=true), ボストン \- 3月25日
- [ClickHouse Meetup @ Braze](https://www.meetup.com/clickhouse-new-york-user-group/events/305916369/?eventOrigin=group_upcoming_events), ニューヨーク \- 3月26日
- [Google Next](https://clickhouse.com/company/events/2025-04-google-next), ラスベガス \- 4月9日
- [Open House User Conference](https://clickhouse.com/openhouse), サンフランシスコ \- 5月28日


### EMEAのイベント [\#](/jp/blog/202502-newsletter-jp#emea%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [ClickHouse Meetup @ Nexton](https://www.meetup.com/clickhouse-france-user-group/events/305792997/), パリ \- 3月4日
- [KubeCon 2025](https://clickhouse.com/company/events/04-2025-kubecon-london), ロンドン \- 4月1\-4日
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-paris), パリ \- 4月9日
- [AWS Summit 2025](https://clickhouse.com/company/events/2025-04-aws-summit-amsterdam), アムステルダム \- 4月16日
- [AWS Summit, 2025](https://clickhouse.com/company/events/04-2025-aws-london), ロンドン \- 4月30日


### APACのイベント [\#](/jp/blog/202502-newsletter-jp#apac%E3%81%AE%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88)


- [ClickHouse Singapore Meetup](https://www.meetup.com/clickhouse-singapore-meetup-group/events/305917892/) \- 2月25日
- [ClickHouse Shanghai Meetup](https://www.huodongxing.com/event/3794544969111?td=3894807410019), 中国 \- 3月1日
- [Data \& AI Summit NSW](https://forefrontevents.co/event/data-ai-summit-nsw-2025/), オーストラリア \- 3月18日
- [Current Bengaluru](https://current.confluent.io/bengaluru), インド \- 3月19日
- [ClickHouse Delhi Meetup](https://www.meetup.com/clickhouse-delhi-user-group/events/306253492/), インド \- 3月22日
- [Latency Conference](https://latencyconf.io/), オーストラリア \- 4月3\-4日
- [TEAMZ Web3/AI Summit](https://web3.teamz.co.jp/en), 日本 \- 4月16\-17日


## JSONBenchの紹介：10億件のドキュメントJSONチャレンジ vs MongoDB、Elasticsearchなど [\#](/jp/blog/202502-newsletter-jp#jsonbench%E3%81%AE%E7%B4%B9%E4%BB%8B10%E5%84%84%E4%BB%B6%E3%81%AE%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88json%E3%83%81%E3%83%A3%E3%83%AC%E3%83%B3%E3%82%B8-vs-mongodbelasticsearch%E3%81%AA%E3%81%A9)


![2_newsletter202502.png](/uploads/2_newsletter202502_fd28c5c96d.png)
[11月のニュースレター](https://clickhouse.com/blog/202411-newsletter#how-we-built-a-new-powerful-json-data-type-for-clickhouse)では、新しいJSONデータ型について言及し、そのパフォーマンス上の利点を説明しました。これらの主張を検証するために、JSON分析用のベンチマークスイートである[JSONBench](https://jsonbench.com/)を開発しました。


Tom Schreiberは、さまざまなデータベースがJSONデータをどのように処理するかを比較する包括的なブログ記事を公開しました。この分析では、ClickHouse、MongoDB、Elasticsearchを含む複数のシステムにおけるパフォーマンスベンチマークとストレージアプローチについて取り上げています。


彼の調査結果では、各データベースがJSONデータに対する分析クエリでどのように動作するかを詳細に示し、それらの基盤となるJSONストレージメカニズムを探求しています。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql)


## Shahar Gvirtz: 私がClickHouseを好きな7つの理由 [\#](/jp/blog/202502-newsletter-jp#shahar-gvirtz-%E7%A7%81%E3%81%8Cclickhouse%E3%82%92%E5%A5%BD%E3%81%8D%E3%81%AA7%E3%81%A4%E3%81%AE%E7%90%86%E7%94%B1)


コミュニティメンバーがClickHouseを楽しんでいるブログ記事を見つけるのはいつも楽しいものです！


ShaharがClickHouseを好きなすべての理由を説明するつもりはありませんが、彼が気に入っていることの1つ、つまりClickHouseの過小評価されている機能であるデータ圧縮機能に焦点を当てたいと思います。Shaharの言葉を借りれば：



> ClickHouseに保存されたログは、Elasticsearchで占めるスペースのわずか28%しか占めません。


友人や同僚にClickHouseを好きな理由を説明する必要がある場合は、このブログ記事を紹介するのが良いでしょう！


➡️ [ブログ記事を読む](https://shahargv.medium.com/7-reasons-why-i-like-clickhouse-9cbb11b142d5)


## エージェント指向分析 [\#](/jp/blog/202502-newsletter-jp#%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E6%8C%87%E5%90%91%E5%88%86%E6%9E%90)


![3_newsletter202502.png](/uploads/3_newsletter202502_1727daa7b3.png)
Ryadh Dahimeneは、（私の謙虚な意見では）素晴らしいブログ記事を書き、[リアルタイム分析](https://clickhouse.com/engineering-resources/what-is-real-time-analytics)データベースの新しいユーザーペルソナ、つまりAIエージェントについて説明しています！


Ryadhはまず、2022年のChatGPTのリリース以降のAI開発の簡単な概要を示し、「認識\-思考\-行動」ループ、LLMによるツールサポートの導入、そして最近のOpenAI o1やDeepSeek\-R1のような推論モデルの進化について説明します。


次に、エージェントワークフローにおけるリアルタイム分析データベースの役割を探求し、[ClickHouse MCP Server](https://github.com/ClickHouse/mcp-clickhouse/tree/f8cc7e09d71b624691702520a4741e1849b4b4be)を紹介します。これは、AnthropicのModel Context Protocolのサーバー側の実装であり、Claude DesktopからClickHouseデータベースと簡単に会話できることを意味します。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/agent-facing-analytics)


## ClickHouseとCribl：強力なデータ取り込みと分析のデュオ [\#](/jp/blog/202502-newsletter-jp#clickhouse%E3%81%A8cribl%E5%BC%B7%E5%8A%9B%E3%81%AA%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E3%82%8A%E8%BE%BC%E3%81%BF%E3%81%A8%E5%88%86%E6%9E%90%E3%81%AE%E3%83%87%E3%83%A5%E3%82%AA)


![4_newsletter202502.png](/uploads/4_newsletter202502_08ff7adaee.png)
Cribl Streamは、ログ、メトリクス、トレースデータなどの[テレメトリーデータ](https://clickhouse.com/engineering-resources/telemetry-data)を含むさまざまなデータソースと連携するデータ処理プラットフォームです。宛先に転送する前にイベントを前処理、フィルタリング、変換することで、ストレージの使用率とクエリ効率を最適化するのに役立ちます。ClickHouseのサポートは、最近サポートされている出力のリストに追加されました。


David Maislinは、この統合を設定して使用する方法を示す詳細なガイドを執筆しました。このガイドには、ClickHouseテーブルの作成、Cribl Stream宛先の構成、Cribl Searchを使用したデータのクエリに関するステップバイステップの手順が含まれています。また、CriblのDatagen機能を使用してテストデータを生成する例を含め、Criblのデータ処理機能と並行してClickHouseを使用する方法も示しています。


➡️ [ブログ記事を読む](https://cribl.io/blog/clickhouse-and-cribl-a-powerful-data-ingestion-and-analysis-duo/)


## ClickHouse Cloudの進化：コンピュート\-コンピュート分離、改善された自動スケーリングなど！ [\#](/jp/blog/202502-newsletter-jp#clickhouse-cloud%E3%81%AE%E9%80%B2%E5%8C%96%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%83%88-%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%83%88%E5%88%86%E9%9B%A2%E6%94%B9%E5%96%84%E3%81%95%E3%82%8C%E3%81%9F%E8%87%AA%E5%8B%95%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0%E3%81%AA%E3%81%A9)


![5_newsletter202502.png](/uploads/5_newsletter202502_24dd703b23.png)
ClickHouse Cloudは、記録的な速さで構築され、2022年12月に市場に投入されました。それ以来、1000社を超える企業がワークロードを私たちのマネージドサービスに移行し、現在では毎日、合計55億件のクエリを実行し、100PBのデータ上で3500兆件のレコードをスキャンしています！


過去2年間、ユーザーとの緊密な連携を通じて貴重な洞察を得て、クラウドアーキテクチャを大幅に進化させてきました。このブログでは、[コンピュート\-コンピュート分離](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud)、高性能マシンタイプ（[AWSでのGravitonへの移行](https://clickhouse.com/blog/graviton-boosts-clickhouse-cloud-performance)）、シングルレプリカサービス、より反応が良くシームレスな自動スケーリングなど、最新の改善について説明します。


➡️ [ブログ記事を読む](https://clickhouse.com/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings)


## 25\.1 リリース [\#](/jp/blog/202502-newsletter-jp#251-%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)


25\.1リリースブログ記事では、Tom Schreiberが並列ハッシュ結合アルゴリズムのプローブフェーズに加えられた改善について深く掘り下げました。データベースの内部構造に興味がある方は、一読の価値があります。


このリリースでは、テーブルレベルでのMinMaxインデックスの導入、Mergeテーブルエンジンとテーブル関数の改善、自動インクリメント機能の追加、そしていくつかの優れたCLIの使いやすさの改善も行われました。


➡️ [リリース記事を読む](https://clickhouse.com/blog/clickhouse-release-25-01)


## 興味深いプロジェクト [\#](/jp/blog/202502-newsletter-jp#%E8%88%88%E5%91%B3%E6%B7%B1%E3%81%84%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88)


毎月ニュースレターをまとめていると、ClickHouseベースの多くのプロジェクトに出会うので、今月はそのうちのいくつかを紹介したいと思います。


- [apitally.io](https://apitally.io/) \- Python / Node.jsアプリ向けのAPI監視および分析ツール。APIの使用状況とパフォーマンスを理解し、問題を早期に発見し、問題発生時に効果的にトラブルシューティングするのに役立ちます。創設者は、[Hacker Newsのスレッド](https://news.ycombinator.com/item?id=42915435)で、ClickHouseを使用してデータを保存していると述べています。
- [Openpanel](https://github.com/Openpanel-dev/openpanel) \- Web、モバイルアプリ、バックエンドサービス全体でユーザーの行動をキャプチャするためのMixpanelのオープンソース代替。ClickHouseを使用してイベントを保存します。
- [Vigilant](https://www.vigilant.run/home) \- 構造化ログを管理するための軽量ツール。ログを一元化し、検索し、アラートを作成できます。[内部的にはClickHouseを使用](https://news.ycombinator.com/item?id=42814930)しています。
- [CH\-UI](https://github.com/caioricciuti/ch-ui) \- ClickHouse Serverと対話するためのユーザーインターフェース。クエリの構文ハイライト表示があり、インスタンスに関する視覚的なメトリクスを確認できます。


## ビデオコーナー [\#](/jp/blog/202502-newsletter-jp#%E3%83%93%E3%83%87%E3%82%AA%E3%82%B3%E3%83%BC%E3%83%8A%E3%83%BC)


- Benjamin Woottonが[この実践的なビデオで実演している](https://clickhouse.com/videos/replicating-data-postgres-clickhouse-cloud)ように、トランザクション処理にはPostgreSQL、分析にはClickHouseというようにワークロードを分割する手法がますます一般的になっています。彼は、これらのデータベースを同期させる2つの方法、つまりオープンソースの[PeerDB](https://github.com/PeerDB-io/peerdb)ツールを使用する方法と、[ClickHouse Cloudの組み込みソリューション](https://clickhouse.com/docs/en/integrations/clickpipes/postgres)を使用する方法を紹介しています。
- [最近リリースされたClickHouse MCPサーバーの使用方法](https://clickhouse.com/videos/clickhouse-mcp-server)を示すビデオを作成しました。
- また、[組み込みの監視ダッシュボードを使用して一般的な問題をデバッグする方法](https://clickhouse.com/videos/clickhouse-monitoring-dashboard)を示すビデオも作成しました。
- Flock SafetyのLeon Kozlowskiは、彼らがどのように[遅い日次バッチ処理のRedshiftセットアップからClickHouseを使用したリアルタイムソリューションにトラフィック分析システムを変革したか](https://clickhouse.com/videos/real-time-traffic-analytics-flock-safety)を説明しています。このシステムは、監視カメラのネットワークから1日あたり10億件を超えるML予測を処理しています。
- Derek ChiaとKarthikayan Muthuramalingamは、[ClickHouseとKafkaを統合するための技術的な概要](https://clickhouse.com/videos/maximising-analytics-clickhouse-kafka)を発表し、これらのテクノロジーがリアルタイムデータ処理と分析のために効果的に連携する方法を示しています。Derekは、分析に最適化されたオープンソースの列指向データベースとしてのClickHouseの機能について説明し、Karthikayanは、分散イベントストリーミングプラットフォームとしてのKafkaの役割について詳しく説明しています。


## 今月の投稿 [\#](/jp/blog/202502-newsletter-jp#%E4%BB%8A%E6%9C%88%E3%81%AE%E6%8A%95%E7%A8%BF)


今月のお気に入りの投稿は、ClickHouseに大量のデータを取り込んでいる[Jacob Wolf](https://x.com/JacobWolf)によるものです。


![6_newsletter202502.png](/uploads/6_newsletter202502_1b466bad33.png)
➡️ [投稿を読む](https://x.com/JacobWolf/status/1884316267093582231)
