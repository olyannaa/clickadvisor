# Open House 2026 2日目: オープンソース10年の歩みと、エコシステムが次に築くもの


Day 1を見逃した方は、[Day 1まとめブログ記事](https://clickhouse.com/blog/open-house-2026-day-1-jp)で、ClickHouse CloudおよびClickStackに関するすべての発表をキャッチアップしてください。


昨年は初の年次Open Houseカンファレンスを開催し、1日でたくさんの内容をお届けしました。今年は、ご紹介すべきコンテンツや発表があまりに多かったため、もう1日延長することにしました。Day 2では、オープンソースコミュニティ、パートナー、お客様がClickHouseの上に何を構築しているのかをより深く掘り下げました。構築されている機能だけでなく、なぜ世界中がこのデータプラットフォームに賭けているのかにフォーカスしました。


今年、ClickHouseはオープンソースプロジェクトとして10周年を迎えます。この10年で、エコシステムは私たち、パートナー、そして絶えずリリースを続けるコミュニティによって構築された200以上のインテグレーションにまで成長しました。そのペースは最近さらに加速しています。MCPサポートと当社のスキルフレームワークは爆発的な採用を見せており、組み込み型やカスタムのインテグレーションが、まったく新しいカテゴリとして有機的に生まれてくる様子を私たちは目の当たりにしています。人もエージェントも、私たち自身が作ろうとは思いつかなかったような方法で、ClickHouseを自分たちのスタックに組み込んでいます。


### オープンソース10周年 [\#](/jp/blog/open-house-2026-day-2-jp#10-years-of-open-source)


オープニングキーノートでは、ClickHouseがオープンソースプロジェクトとして歩んだ10年間を振り返り、コントリビューターの成長、コミュニティのマイルストーン、そして[Community Champions Program](https://clickhouse.com/community)の立ち上げについて紹介しました。Alexey Milovidovが登壇し、「How to build a great database(優れたデータベースの作り方)」と題したセッションで、ClickHouseの構築と設計における自身の思考プロセス、そして長年の経験から学んだことを語りました。この間ずっとClickHouseに取り組んでいたのはAlexeyだけではありません。ClickHouseには2,600人以上のコントリビューターがおり、GitHubでは48,000近いスターを獲得しています。この10年間にコミュニティからいただいたサポートは素晴らしいものであり、皆様のすべての貢献に心から感謝しています。


![open_house_day2_may2026_image5.png](/uploads/open_house_day2_may2026_image5_54d9436e8d.png)
### House Mates: 初代メンバー [\#](/jp/blog/open-house-2026-day-2-jp#house-mates-the-inaugural-cohort)


ClickHouseエコシステムの勢いを後押しするため、ClickHouseの公式パートナープログラムである[House Mates](https://clickhouse.com/blog/introducing-house-mates)を発表しました。House Matesは、25社以上のISV・テクノロジーパートナー、35社以上のサービス・チャネルパートナーとともに正式にローンチしました。初代メンバーとしてこれ以上望むものはありません。彼らはきっちり成果を出してくれました。


House Matesの第1弾には、お客様から最も多くお問い合わせをいただいたインテグレーションが揃っています。データと変換の領域では、FivetranがClickHouse Cloudの宛先として一般提供を開始し、スキーマ移行サポートとエンタープライズSLAを備えた500以上のソースを利用できるようになりました。Sigma Computingは公式コネクタをパブリックベータへ移行します。Notionはカスタムエージェント向けにClickHouse MCPサーバーのファーストパーティサポートを追加します。そしてClickHouseは、コミュニティdbt Fusionアダプタを構築する初のパートナーとなり、dbtプラットフォーム上でネイティブに動作させるための第一歩を踏み出しました。それぞれの詳細は以下をご覧ください。


これらの発表に加え、第1弾メンバーには次のようなパートナーが含まれます。Postgres、MySQL、SQL Server、Oracle、MongoDBからの分以下のCDCレプリケーションを実現するArtie、ClickHouseとSupabaseを接続するAIネイティブ分析プラットフォームDreambase、EloquentモデルやQuery Builder、Schema Builder、artisanを介したネイティブマイグレーションサポートなど、機能満載のClickHouseドライバを提供するLaravel、ClickHouseを分析バックエンドとして利用するゼロコードのOpenTelemetryトレーシングを実現するOdigos、ClickHouse Agentsを高速な検索バックエンドとして使うAI検索のTavily、ClickHouseからCRM、広告プラットフォーム、SaaS宛先へのリバースETLを提供するHightouch、ClickHouseのテーブルとパイプラインに対するリネージとディスカバリを備えたオープンソースのデータカタログDataHub。リストはまだまだ続きます。


明日を一緒に作り上げる素晴らしいパートナーグループが揃ったことを、私たちは光栄に思います。カンファレンスの中で、ClickHouseエコシステム全体にわたるエキサイティングな発表をいくつかご紹介しました。


### Fivetran: 一般提供開始 [\#](/jp/blog/open-house-2026-day-2-jp#fivetran-generally-available)


ClickHouse Cloud向けFivetran宛先コネクタが一般提供を開始しました。これは過去2年間でお客様から最もリクエストの多かったインテグレーションの1つです。


これにより、チームはパイプラインコードを書いたり保守したりすることなく、500以上のソースからClickHouseへデータをレプリケートできるようになります。Fivetranはスキーマ移行、カラムの追加、リトライを自動的に処理します。GAリリースにはスキーマ移行サポートとエンタープライズSLAが含まれ、Salesforce、HubSpot、Google Ads、Stripe、SAP、NetSuite、Snowflake、Databricks、その他数百のエンタープライズSaaSデータをClickHouseで実行するチームにとって、本番運用に耐える経路となります。



> "ClickHouseはFivetran上で急成長中のデータ宛先であり、GA化は両チームがこのパートナーシップにいかに真剣に投資してきたかを示しています。エンタープライズのデータチームは、Salesforce、Google Analytics、SAP、Databricks、Snowflake、Workday、NetSuiteといったソースで事業を運営しています。これらのデータを、自動化されたスキーマ管理とエンタープライズSLAを備えて確実にClickHouseに取り込むことこそ、Fivetranが目指してきた姿です。あらゆる主要なエンタープライズソースからClickHouse Cloudへの本番グレードの経路をお客様にお届けできることを誇りに思います。"
> 
> 
> \-\- Shiva Mogili, Director of Product Management, Connectors \& Extensibility


**Google Cloud Dataflow: Pub/Subテンプレートが一般提供開始**


BigQueryテンプレートに加えて、Pub/SubサポートのためのClickHouseテンプレートがGoogle Cloud Dataflowギャラリーで利用可能になりました。


これまで、Pub/SubのデータをClickHouseに取り込むには、公式サポートのないカスタムBeamパイプラインが必要でした。今後、チームはDataflowコンソールから直接、ClickHouseへのマネージドパイプラインを構成できます。ClickHouse Cloudをご利用のチーム向けには、[同じインテグレーションがネイティブClickPipesコネクタとしても利用可能](https://clickhouse.com/blog/open-house-2026-day-1#clickpipes)なので、ワークフローに合った方を選択してセットアップできます。


Dataflow上でPub/Subを使い始める方法の詳細は[こちら](https://clickhouse.com/docs/integrations/google-dataflow/templates/pubsub-to-clickhouse)をご覧ください。


### Sigma Computing: コネクタがパブリックベータに [\#](/jp/blog/open-house-2026-day-2-jp#sigma-computing-connector-in-public-beta)


ClickHouse向けSigma Computingコネクタは、さまざまなお客様の本番環境で運用された実績を経て、プライベートベータからパブリックベータへ移行します。コネクタは、ClickHouseに接続したいすべてのSigmaユーザーが利用可能になりました。


コネクタのパブリックベータ化に加え、Sigmaは新しいETL Cache Layer(現在プライベートプレビュー中)の最初のデータベースターゲットとしてClickHouseを選択しました。ダッシュボードがロードされるたびにSigmaのクエリがプライマリウェアハウスに到達すると、その下のデータが実際にどれだけ変化しているかに関係なく、チームはフルのコンピュートコストを支払うことになります。ETL Cache Layerはホットなデータセットを事前にマテリアライズし、どのような同時実行レベルでもサブ秒で配信します。さらに、キャッシュミス時にはソースウェアハウスにフォールバックするインテリジェントなルーティング機能を備えています。これは大きなパフォーマンス上の利点だけでなく、コスト面でもメリットをもたらします。


*「ClickHouseは市場で最も急成長しているデータベースの1つであり、当社のお客様は、それが破壊的なコストパフォーマンスを提供するからこそClickHouseの上に構築しています」とSigmaのCEO、Mike Palmerは語っています。「House Matesパートナープログラムへの参加は、SigmaをClickHouse上で最高のAIランタイム体験にするというコミットメントです。」*


### dbt: ClickHouse Fusionアダプタ [\#](/jp/blog/open-house-2026-day-2-jp#dbt-clickhouse-fusion-adapter)


ClickHouseは、dbt Labsと共同でdbt Fusionエンジンアダプタを開発する初のパートナーです。Fusionは、Rustで構築された真のSQLコンパイラです。dbtの下層にあるこのエンジンが、どんな規模のプロジェクトでもdbtを高速化し、ウェアハウスに到達する前に開発者にリアルな実フィードバックを提供し、AI支援によるデータ作業を信頼できるものにする構造化メタデータを生成します。これはdbtの未来であり、私たちはdbt Labsと提携し、このアダプタを両者の共通コミュニティに届けられることを嬉しく思います。


成長を続けるdbtユーザーコミュニティとdbtのビジョンが、この取り組みの触媒となりました。その結果、アダプタは現在CLI経由でアルファ版が利用可能となっています。アナリティクスエンジニアは、Fusionを使って今日からClickHouseに対してdbtモデルを実行できます。これは、フルdbtプラットフォーム(旧Cloud)統合に向けた最初のマイルストーンです。最も多くいただくインテグレーションリクエストの1つに応えるだけでなく、dbt Labsの新しいアダプタプログラムの形成に貢献できることを嬉しく思います。Fusionがデフォルトになるにつれ、共通のお客様にファーストクラスの体験をお届けすることに私たちはコミットしています。



> "ClickHouseはdbtコミュニティで最も急成長しているデータベースの1つになっており、その理由は明らかです。スケールにおけるスピードと、オープンエコシステムへの真摯なコミットメントの組み合わせは、市場が向かっているコンポーザブルなデータインフラストラクチャに自然にマッチします。Fusionは、dbtが今後プラットフォームを支える方法であり、ClickHouseを早期に対応させることで、私たちの共通のお客様は今日から完全にオープンなスタックを構築できます。私たちが共に作り上げているものに私たちは興奮しており、まだまだ多くのことが控えています。"
> 
> 
> \-\- Hope Watson, Product Manager, dbt Labs


### Apache Airflow: ネイティブプロバイダ [\#](/jp/blog/open-house-2026-day-2-jp#apache-airflow-native-provider)


ClickHouse向けネイティブApache Airflowプロバイダが、Airflowレジストリから[まもなく](https://github.com/apache/airflow/pull/67080)利用可能になります。ネイティブオーケストレーションコネクタへの関心の高さを感じており、これまでこの[取り組みをサポート](https://github.com/bryzgaloff/airflow-clickhouse-plugin)してきたIvan Klimenko ([klimenkoIv](https://github.com/klimenkoIv))、Anton Bryzgalov ([bryzgaloff](https://github.com/bryzgaloff))、そしてAirflowコミュニティに感謝します。当社のネイティブプロバイダは、ClickHouseフックとオペレータをAirflowエコシステムに追加するもので、チームはカスタムオペレータラッパーを書くことなく、DAGから直接クエリ、テーブルリフレッシュ、データロードをスケジュールできます。新しいプロバイダは、新しいApache Airflow標準に基づいて構築されており、ClickHouseが保守し、レジストリ登録が完了すればAstronomer Astroのコネクションでそのまま動作します。このプロジェクトがどのように進化するかが楽しみで、コミュニティへのリリースが待ち遠しいです。


### Vercel AI SDK v7 \+ Langfuse [\#](/jp/blog/open-house-2026-day-2-jp#vercel-ai-sdk-v7-langfuse)


Vercel AI SDK v7は、より細かなエージェントの可観測性を実現する新しいテレメトリーシステムとともに出荷されます。Langfuseは、OpenTelemetryを介してこの新しいテレメトリーシステムとネイティブインテグレーションを提供します。


AI SDK v7は本日カナリービルドとして利用可能で、6月に一般提供を開始する予定です。


Langfuseは`registerTelemetry()`を1回呼び出すだけでAI SDK v7と統合され、本番AIエージェントにおけるすべてのツール呼び出し、サブエージェントスパン、LLM呼び出しの完全な階層トレース可視性を提供します。追加のボイラープレートやカスタム計装の配線は不要です。


![open_house_day2_may2026_image4.png](/uploads/open_house_day2_may2026_image4_7d04c525ed.png)
### Notion: カスタムエージェント向けネイティブClickHouseコネクタ [\#](/jp/blog/open-house-2026-day-2-jp#notion-native-clickhouse-connector-for-custom-agents)


Notionは、カスタムエージェント向けのネイティブコネクタとしてClickHouseを追加します。これにより、チームは外部ツールを使わずに、Notion内から直接ClickHouseデータをクエリできます。


このインテグレーションが興味深いのは、そのアーキテクチャです。データと質問の間に独立したセマンティックレイヤーが置かれているわけではありません。代わりに、平易な英語で書かれたNotionページが、テーブル構造、データのタグ付け方法、各フィールドの意味を記述します。エージェントはそれらのドキュメントを読み、MCP経由でClickHouseに接続し、自然言語で回答を返します。既存のNotionワークスペースがコンテキストレイヤーとなり、ClickHouseがクエリを担当します。これは間もなくNotionカスタムエージェントへ展開される予定です。



> "毎日、ClickHouseユーザーは、最も要求の厳しいデータワークロードの一部を処理するサービスに頼っています。しかし、そうしたインサイトを、チームが実際に意思決定を行うツールに取り込むには、これまで多くのつなぎ込みが必要でした。Notionカスタムエージェントが直接ClickHouseにクエリできるようになったことを大変嬉しく思います。私たちの共通のお客様は、平易な言葉で質問し、SQL不要で実際にデータに富んだ回答を得られます。これは、スケジュール化されたレポート、自動化されたワークフロー、ドキュメントやダッシュボードに直接取り込まれるライブデータを意味します。ClickHouseが数値を処理し、Notionがそれを実行可能なものに変えるのです。"
> 
> 
> \-\- David Rosenberg, Ecosystem Lead, Notion


### Pythonクライアントがv1に! [\#](/jp/blog/open-house-2026-day-2-jp#python-client-is-now-v1)


[clickhouse\-connect v1](https://github.com/ClickHouse/clickhouse-connect)がPyPIで一般提供を開始しました。これは大きなマイルストーンであり、クライアントの最初のメジャーリリースです。最初の1\.0リリースの目玉は、aiohttp上にゼロから構築されたネイティブ非同期クライアントです。これは旧来のエグゼキュータベースのラッパーを置き換えるもので、ストリーミングを含めて同期クライアントと完全な機能パリティを実現します。


DateTime型、固定幅数値、Map、Decimal、BigDecimalに対するパフォーマンスの大幅な高速化も得られます。さらに、Variantカラムのサポートにより、クライアント側でClickHouseネイティブの型を使ってシリアライズできるようになりました。


numpy、pandas、pyarrow、polarsをインストールしているプロジェクトでは、コールドスタート時間が4倍改善されます。この改善は、すべてを最初にインポートするのではなく、オプション依存関係を遅延ロードすることで実現されています。


SQLAlchemyダイアレクトのファーストクラスサポートを導入し、ClickHouse固有のSQLサポートを深め、v1\.1\.0で出荷予定のAlembicスキーママイグレーションへの道筋を整えました。


互換性の面では、本リリースはPandas 3\.xとの互換性を追加し、Python 3\.14のフリースレッディングへの実験的サポートも加わったため、既存のclickhouse\-connectユーザーにとってアップグレードする説得力のある理由が揃いました。


### .NETスタック: NuGetで一般提供開始 [\#](/jp/blog/open-house-2026-day-2-jp#net-stack-generally-available-on-nuget)


最近の安定版リリース1\.2\.0により、[clickhouse\-cs](https://github.com/ClickHouse/clickhouse-cs)はNuGetで4つのパッケージを備えた完全な.NET開発スタックを提供するようになりました。


[ClickHouse.EntityFrameworkCore](https://github.com/ClickHouse/ClickHouse.EntityFrameworkCore)はORMサポートを追加し、JOIN、UNION、サブクエリ、DDL生成、スキーママイグレーションを含みます。[Serilog.Sinks.ClickHouse](https://github.com/ClickHouse/Serilog.Sinks.ClickHouse)はClickHouseへの構造化ロギングのためのカラムおよびクラスタのフルーエント構成とともに出荷されます。[ClickHouse.Aspire](https://github.com/ClickHouse/ClickHouse.Aspire/)は、クラウドネイティブな.NETアプリケーションを構築するチーム向けにスタックを完成させます。[ClickHouse.SemanticKernel](https://github.com/ClickHouse/ClickHouse.SemanticKernel/)はClickHouseをMicrosoft AIオーケストレーションエコシステムに接続します。各パッケージは本日より、.NETエコシステムで開発するユーザーが利用できます。


### ClickStackの発表 [\#](/jp/blog/open-house-2026-day-2-jp#clickstack-announcements)


昨日のClickStack Cloud発表に続き、ClickStackに2つの大きな追加機能を発表しました。**AI Notebooks**と**ClickStack MCPサーバー**です。両者は非常にシンプルなアイデアに基づいて構築されています。それは、可観測性ワークフローは、今日のエンジニアが実際にシステムをデバッグする方法から切り離されたものであってはならない、ということです。


**AI Notebooks**は、現在Managed ClickStackでパブリックベータとなっており、チームに調査用の永続的なワークスペースを提供します。ダッシュボード、チャット、ターミナル、アドホッククエリの間でコンテキストを失う代わりに、エンジニアは調査を進める中で、クエリ、チャート、メモ、発見事項を1か所にまとめておくことができます。


ほとんどの本番インシデントは線形ではありません。1つのリードを追い、行き詰まり、以前の仮定を見直し、トレースをログと比較し、別の方法を試します。Notebooksは、すべてを1つのチャットセッションや厳格なステップのシーケンスに押し込めることなく、その種のワークフローをサポートするように設計されています。


![open_house_day2_may2026_image1.png](/uploads/open_house_day2_may2026_image1_a745b3bbd1.png)
同時に、Claude Code、Cursor、カスタムSDKベースのシステムなどのツールを使い、可観測性データの周辺で独自の内部エージェントや自動化を構築するチームが増えています。**ClickStack MCP**サーバーはそうした世界向けに設計されており、「Bring Your Own Agents(自分のエージェントを持ち込む)」という哲学に基づいて構築されています。


もう1つのスタンドアロンAIインターフェースを導入するのではなく、MCPサーバーはNotebooksが内部で使用するのと同じ可観測性ツールを公開し、外部エージェントから利用できるようにします。内部的には、MCPがこれらの操作を最適化されたClickHouseクエリへ変換するため、エージェントは調査ロジックを繰り返し再構築したり、複雑なSQLをゼロから生成したりすることなく、より高レベルのセマンティックエンドポイントで作業できます。


![open_house_day2_may2026_image3.png](/uploads/open_house_day2_may2026_image3_d527806633.png)
より汎用的なClickHouse MCP実装と比較して、当社の内部テストでは、ClickStack MCPサーバーは効率、パフォーマンス、調査の精度を向上させることが示されています。内部テストでは、調査が最大25%少ないツール呼び出しで完了し、一貫性が2\.5倍向上し、評価が約20%改善しました。


NotebooksとMCP駆動のワークフローの統合をより緊密にしていく今後の方向性を含む詳細については、[メインの発表記事](https://clickhouse.com/blog/observability-mcp-server-ai-notebooks)をご覧ください。


## まとめ [\#](/jp/blog/open-house-2026-day-2-jp#what-this-adds-up-to)


10年を経て、ClickHouseを取り巻くエコシステムはかつてないほど健全であり、急速に拡大しています。本日発表したインテグレーションは、ELT、BI、オーケストレーション、言語クライアント、MCP、AI可観測性にまたがります。それらは長らく当社のリストにあったギャップを埋め、人々(およびそのエージェント)が構築できる完全に新しいカテゴリを切り拓きます。


コミュニティ、パートナー、お客様は皆、同じ方向に引っ張ってくれています。それがDay 2のテーマであり、皆さんが何を作り上げるかを見るのが待ちきれません。


セッションの録画はまもなく公開予定です。Day 1の発表内容については、こちらからどうぞ: [Day 1 ClickHouse Cloudまとめ](https://clickhouse.com/blog/open-house-2026-day-1-jp)。

### 今すぐ始める

ClickHouseがお客様のデータでどのように動作するか興味がありますか？ClickHouse Cloudを数分で開始でき、$300分の無料クレジットを受け取れます。[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-728-sign-up&utm_blogctaid=728)
