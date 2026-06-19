# ClickHouseが管理するPostgresがベータ版で提供開始


**TL;DR:** ClickHouse Cloud ユーザーは、ローカル NVMe を活用してトランザクションを最大 10 倍高速化するフルマネージドの Postgres サービスを利用できるようになりました。リアルタイム分析向けに ClickHouse へのネイティブ CDC、さらに pg\_clickhouse による統一クエリレイヤーも備えています。2026 年 6 月 15 日まで無料で、それ以降はベータ期間中 50% 割引でご利用いただけます。CDC と pg\_clickhouse は追加料金なしで含まれます。


ClickHouse Cloud ユーザーは、ローカル NVMe ストレージを活用したフルマネージドの Postgres サービスを、ClickHouse とネイティブに統合された形でプロビジョニングできるようになりました。すべての ClickHouse Cloud ユーザーが、ローカル NVMe ストレージを基盤とし、ClickHouse とネイティブに統合されたエンタープライズグレードのフルマネージド Postgres サービスを利用できます。私たちは、トランザクション (OLTP) ワークロード向けの Postgres と、分析 (OLAP) ワークロード向けの ClickHouse を組み合わせた **ベスト・オブ・ブリードのデータスタック** を提供します。これにより、別々のシステムを組み合わせる従来の複雑さを排除し、リアルタイムおよび AI ネイティブなアプリケーションに不可欠な基盤を提供します。



> [今すぐ ClickHouse Cloud にサインアップして、ClickHouse 管理の Postgres を始めましょう](https://console.clickhouse.cloud/signUp?intent=PG)


ローカル NVMe を活用した高性能な Postgres サービスにより、トランザクション性能が最大 10 倍高速 になります。ネイティブ CDC を使えば、わずか数クリックで Postgres から ClickHouse にデータを同期し、[100 倍高速な分析](https://benchmark.clickhouse.com/) を実現できます。[pg\_clickhouse](https://clickhouse.com/blog/introducing-pg_clickhouse) 拡張による統一クエリレイヤーを使えば、別々のシステムを管理することなく、トランザクションと分析を組み合わせたアプリケーションを構築できます。そしてこれらすべてが費用対効果の高い価格で提供されるため、アプリ構築のための高速かつ信頼性の高いデータ基盤について妥協する必要はありません。


## AI には「ベスト・オブ・ブリード」なデータスタックが必要 [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#ai-needs-the-best-of-breed-data-stack)


[AI ワークロードは、トランザクションデータベースと分析データベースの伝統的な境界を崩しつつあります。](https://clickhouse.com/blog/ai-redrawing-database-market#real-time_analytics) かつて予測可能でハードコーディングされたクエリを実行していたアプリケーションは、今やスタックの両側から回答を必要とする、エージェント駆動の予測不可能なリクエストのバーストを生成しています。同時に、データ量、同時実行性、パフォーマンスへの期待は指数関数的に増大しており、セキュリティと信頼性はかつてないほど重要になっています。


だからこそ、ベスト・オブ・ブリードがこれまで以上に重要なのです。OLTP には Postgres、OLAP には ClickHouse。何千もの AI ネイティブ企業がすでにこのアーキテクチャに集約している理由もここにあります。


![postgres_beta_may2026_image1.png](/uploads/postgres_beta_may2026_image1_4ffdd4d2c0.png)
ClickHouse 管理の Postgres に対する私たちのビジョンはシンプルです。Postgres と ClickHouse を外部パイプライン、カスタムアプリケーションロジック、運用上の複雑さで繋ぎ合わせるオーバーヘッドを排除し、開発者が統一されたデータスタック上で AI ネイティブなアプリケーションを簡単に構築できるようにすることです。


## お客様 [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#customers)


今年初めに ClickHouse 管理の Postgres のプライベートプレビューを発表したところ、すでに数千社がウェイトリストに登録し、多くがマルチテラバイト規模のミッションクリティカルな本番ワークロードを稼働させています。


お客様は RDS、Aurora、CloudSQL、Neon、PlanetScale Postgres などから移行しており、また AI ネイティブな新しいアプリケーションを一から構築している企業もあります。これらのワークロードは、サイバーセキュリティ、フィンテック、リテール、不動産、ソーシャルメディアなど多岐にわたり、いずれも Postgres と ClickHouse によって OLTP と OLAP を統合した、深く統合されたプラットフォームを基盤としています。


以下は、リファレンスカスタマーから寄せられた率直な声の一部です。


### **Physical Intelligence** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#physical-intelligence)


*AI ワークロードとアノテーションパイプラインのスケーリング、RDS から移行*


「ClickHouse は、私たちが RDS から脱却し、成長する AI ワークロードを支えるデータプラットフォームを構築するのに役立ちました。ClickHouse Cloud プラットフォーム内で OLTP には Postgres、OLAP には ClickHouse を使用しており、研究者、トレーニングパイプライン、エージェントが同じデータ基盤に高速にアクセスできるようになっています…アノテーション量が 10 倍に増加し、数十億件のアノテーションへと向かう中、ClickHouse はスケーリングを続けるためのプラットフォーム上の余裕を提供してくれます…」


### **Sterling Labs** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#sterling-labs)


*Aurora から移行し、NVMe 上で 8\.5 TB のホットな Postgres データを運用*


「ClickHouse 管理の Postgres は、Aurora から移行し本番ワークロードをスケールする上で、私たちにとって素晴らしくフィットしました…現在、Postgres で約 8\.5 TB のホットデータを実行しており、NVMe ドライブが提供する超低レイテンシを享受しています…パフォーマンスはまさに圧巻です…」


### **Quinto Andar** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#quinto-andar)


*分析のための汎用インターフェースとして Postgres を活用*


「pg\_clickhouse があれば、ClickHouse は事実上あらゆるサードパーティツールにとってのプラグアンドプレイなデータベースになります…Hightouch のような統合のためだけに BigQuery や Snowflake のオーバーヘッドを強いられる代わりに、主要なデータセットを Postgres 経由で直接公開できるようになりました…ClickHouse の生のパフォーマンスと Postgres の遍在する互換性の両方を備えた、両方の世界の良いとこ取りです。」


### **DoControl** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#docontrol)


*大規模なサイバーセキュリティデータパイプラインの簡素化*


「ClickHouse チームの手厚いサポートを受けて、複数のマルチテラバイト規模のワークロードを RDS と Aurora から ClickHouse 管理の Postgres へ移行しました。私たちのサイバーセキュリティデータソースの規模と複雑さを考えると、信頼性とコストパフォーマンスは極めて重要でした…ClickHouse 管理の Postgres により、Postgres ワークロードをより簡単に移行し、ClickPipes を活用し、当初予想していた運用上の複雑さなしでデータを ClickHouse に取り込めるようになりました。」


その他のリファレンスカスタマーとして特筆したいのは、Trainy.ai や EndClose といった Y Combinator 企業、Mpathic のような AI セーフティ企業、Prediko のような AI ネイティブな在庫管理企業など、ClickHouse 管理の Postgres 上で次世代の AI ネイティブアプリケーションを支える数多くの企業です。


## **製品** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#product)


ClickHouse 管理の Postgres は、高性能な OLTP とリアルタイム OLAP を、深く統合された単一のプラットフォームに統合します。プラットフォームの中核には、3 つの基盤的な機能があります:


- **NVMe 基盤の Postgres** によりトランザクション性能を最大 10 倍高速化
- **ClickHouse へのネイティブ CDC** により外部パイプラインなしでリアルタイム分析を実現
- **pg\_clickhouse**、アプリケーションがトランザクションと分析にまたがれる統一クエリレイヤー


これらの機能が組み合わさることで、Postgres と分析インフラを手作業で繋ぎ合わせる運用上の複雑さが解消され、リアルタイムおよび AI ネイティブなアプリケーションをよりシンプルに構築できるようになります。

Loading video...### **ClickPipesによるフルマネージドな移行** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#fully-managed-migrations-with-clickpipes)


本番環境のPostgresワークロードを移行することは、新しいプラットフォームを導入するうえで最も困難な作業の1つです。[ClickPipes](https://clickhouse.com/docs/cloud/managed-postgres/migrations/clickpipes)を活用したフルマネージドの移行ワークフローにより、お客様はRDS、Aurora、CloudSQL、Neonなどの各種プロバイダーから、最小限のダウンタイムと運用負荷でワークロードを移行できます。


リアルタイムでデータを継続的にレプリケーションし、カットオーバーをシンプル化し、独自の移行インフラを構築する必要をなくすことができます。これは、本番ワークロードを運用しているお客様の間で、すでに最も支持されている機能の1つとなっています。


### **本番ワークロード向けのエンタープライズグレードPostgres** [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#enterprise-grade-postgres-for-production-workloads)


ClickHouseが管理するPostgresには、ミッションクリティカルなアプリケーションを大規模に運用するためにお客様が期待する運用機能が含まれています。たとえば次のようなものです。


- 最大2つのスタンバイによる高可用性
- ポイントインタイムリカバリとデータベースブランチング
- 読み取り負荷の高いワークロードをスケールさせるリードレプリカ
- 90以上のPostgreSQL拡張機能
- Private Linkによるエンタープライズグレードのセキュリティ
- 統合されたモニタリング、ログ、および[Query Insights](https://clickhouse.com/blog/postgres-query-insights-clickhouse-cloud)
- Prometheus互換のメトリクス
- `clickhousectl`によるエージェントベースのアクセス
- OpenAPIによるInfrastructure as Code
- その他多数!


そして、これはまだ始まりに過ぎません。私たちは、リアルタイムおよびAIネイティブのアプリケーション向けに、運用系と分析系を完全に統合したデータプラットフォームの構築を目指しています。


上記の機能に関する詳細なドキュメントは、[こちら](https://clickhouse.com/docs/cloud/managed-postgres)の公式ドキュメントをご参照ください。


## 料金 [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#pricing)


ClickHouseが管理するPostgresは、コスト効率を重視して設計されており、開発者はPostgresとClickHouseによる高速で信頼性の高いデータ基盤を妥協なく利用できます。本サービスは、他のマネージドPostgresサービスと比較しても非常に競争力のある価格設定となっています。これには、ローカルNVMeストレージによる価格性能上のメリットは含まれていません。


本サービスは、2026年6月15日に利用量メータリングが開始されるまで無料です。Beta期間中は、早期にご利用いただくお客様への感謝の意を込めて、すべてのプランで50%の割引が適用されます。



> 正確な料金については、[料金計算ツール](https://clickhouse.com/pricing?service=postgres#pricing-calculator)にアクセスして、ワークロードに最適な構成と料金をご確認ください。


ClickPipesによるネイティブCDCおよびpg\_clickhouse拡張機能は追加料金なしで提供され、PostgresとClickHouseによる統合OLTP \+ OLAPプラットフォームというビジョンに沿ったものとなっています。


本プラットフォームは、1 vCPU / 8 GB RAM / 59 GB NVMe(月額約32ドルから)の構成から、96 vCPU / 768 GB RAM / 60 TB NVMeストレージのクラスタまで、50を超えるローカルNVMeバックアップ型のVM構成をサポートします。これにより、軽量な開発者向けワークロードから、コンピューティング集約型およびストレージ集約型の本番デプロイメントまで、柔軟に対応できます。


Beta期間中は、バックアップとネットワーク送信(egress)も追加料金なしで提供されます。


一般提供(General Availability)に向けて、料金やパッケージは変更される可能性があります。詳細および免責事項については、料金[ドキュメント](https://clickhouse.com/docs/cloud/managed-postgres/pricing)をご参照ください。


## はじめる [\#](/jp/blog/postgres-managed-by-clickhouse-beta-jp#get-started)


ClickHouseが管理するPostgresは、本日よりClickHouse CloudでBeta提供を開始しました!

### 今すぐ始める

ClickHouse Cloud にサインアップして、最初の NVMe ベース Postgres サービスをプロビジョニングし、ClickHouse へのネイティブ CDC をセットアップして、pg\_clickhouse で両者をまたいだクエリを開始しましょう。

新規アカウントにはすべて $300 分の無料クレジットが含まれます。[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-736-sign-up&utm_blogctaid=736)詳細については [ClickHouse によるマネージド Postgres ページ](https://clickhouse.com/cloud/postgres) をご覧いただくか、[ドキュメント](https://clickhouse.com/docs/cloud/managed-postgres) を参照して構築を始めてください。
