# ClickPipes向けPostgres CDCコネクタが一般提供開始


本日、ClickPipes向け [Postgres CDCコネクタ](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector)の一般提供開始を発表できることを嬉しく思います。これにより、お客様はPostgresデータベースをClickHouse Cloudへ数クリックで簡単にレプリケートできるようになります。


この発表は、大きなマイルストーンです。[PeerDB](https://www.peerdb.io/) ― Postgres CDCに特化した企業であり、昨年[ClickHouseが統合](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database)したパートナー ― は、ClickPipes内のPostgres CDCコネクタとしてClickHouse Cloudに完全統合されました。このコネクタは、エンタープライズレベルのPostgresユースケースにも対応可能です。



> [ClickHouse Cloudにサインアップ](https://console.clickhouse.cloud/signup)して、[ClickPipes向けPostgres CDCコネクタ](https://clickhouse.com/docs/integrations/clickpipes/postgres)をお試しください。


## Postgres \+ ClickHouse \= 「デフォルトのデータスタック」 [\#](/jp/blog/postgres-cdc-connector-clickpipes-ga-jp#postgres--clickhouse--%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%B9%E3%82%BF%E3%83%83%E3%82%AF)


近年、[GitLab](https://about.gitlab.com/blog/2022/04/29/two-sizes-fit-most-postgresql-and-clickhouse/)、[CloudFlare](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse...)、[Instacart](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4) などの企業をはじめ、多くのビジネスで共通のパターンが見られるようになっています。それは、PostgresとClickHouseを組み合わせて、あらゆるデータ課題を解決するというものです。


- **Postgres** はトランザクション型Webアプリケーションのためのシステム・オブ・レコードとして機能します。
- **ClickHouse** はリアルタイム分析とレポート用途のためのシステム・オブ・アナリシスとして機能します。


このパターンはAI時代に入りさらに加速しており、[LangChain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain)、[LangFuse](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution)、[Vapi](https://neon.tech/blog/vapi-voice-agents-neon) などの企業も同様のアーキテクチャを採用しています。私たちは、Postgres \+ ClickHouseがモダンビジネスにおける「標準的なデータスタック」になりつつあると考えています。その統合を“魔法のようにシームレス”にすることが私たちの目標です。そして今回のPostgres CDCコネクタは、そのための**最初の大きなステップ**です。PostgresのデータをClickHouseへ簡単に取り込むことで、リアルタイム分析をスムーズに実現できるようになります。


以下は、PostgresとClickHouseをPostgres CDCで組み合わせた際のリファレンスアーキテクチャの図です。Postgresは低レイテンシなトランザクションを処理し、ClickHouseが高速な分析を支えます。


![catalogue_lakehouse.png](/uploads/Postgres_Click_House_reference_architecture_61fe52239a.png)
## メトリクスと導入企業の事例 [\#](/jp/blog/postgres-cdc-connector-clickpipes-ga-jp#%E3%83%A1%E3%83%88%E3%83%AA%E3%82%AF%E3%82%B9%E3%81%A8%E5%B0%8E%E5%85%A5%E4%BC%81%E6%A5%AD%E3%81%AE%E4%BA%8B%E4%BE%8B)


過去6か月間、このコネクタはユーザーフィードバックをもとに急速に進化を遂げながら、広範なベータフェーズを経てきました。現在では、**数百のミッションクリティカルなワークロード**を支え、**月間100TB以上のデータ**をClickHouseに移行しています。


代表的な導入企業には、米国の大手採用プラットフォーム [**Ashby**](https://www.ashbyhq.com/)、急成長中のサイバーセキュリティスタートアップ [**Seemplicity**](https://seemplicity.io/)、米国有数の自動車小売企業 [**AutoNation**](https://www.autonation.com/) などがあります。以下は、一部のお客様からの声です。



> 「ClickHouseはAshbyの顧客向け分析基盤として稼働しており、完全に動的なインサイトを超高速で提供しています。一方でPostgresはコアトランザクションを処理しています。ClickPipes経由のPostgres CDCにより、テラバイト規模のデータをシームレスにレプリケートでき、リアルタイム分析がさらに高速化しました。以前は数分かかっていたレポートが、今では1秒以内で完了します。エンタープライズ顧客がリアルタイムで意思決定する際に活用するダッシュボードは、まさに“真実の情報源”です。PostgresとClickHouseを組み合わせることで、私たちは信頼性の高い体験と、スケールに応じたデータ処理を提供できています。」
> — [Elenie Godzaridis](https://www.linkedin.com/in/elenie-godzaridis/), Director of Engineering, [Ashby](https://www.ashbyhq.com/)



> 「最初はDebeziumを使って社内でPostgres CDCを実装しようとしましたが、あまりに複雑すぎました。PostgresのビットをClickHouseに変換することを使命にしているエンジニアたちが作ったマネージド製品のほうが、自分たちの手で作るものよりも優れていると確信していました。」
> — [Tal Shargal](https://www.linkedin.com/in/tal-shargal-29388671/), Chief Architect, [Seemplicity](https://seemplicity.io/), [*導入事例はこちら*](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse)


![Chart.png](/uploads/Chart_7c2a541127.png)
**このグラフは、過去1年間におけるPostgres CDCからClickHouseへの使用量の成長を示しています。** [**リファレンス**](https://www.linkedin.com/feed/update/urn:li:activity:7310749593296588800/)


## 製品の特長 [\#](/jp/blog/postgres-cdc-connector-clickpipes-ga-jp#%E8%A3%BD%E5%93%81%E3%81%AE%E7%89%B9%E9%95%B7)



Postgres CDCコネクタは、PostgresとClickHouseのために専用設計されたコネクタであり、豊富な機能を備えています。以下は特に注目すべき機能の一部です：


1. **初回ロードおよび再同期が10倍高速化** – [並列スナップショット](https://blog.peerdb.io/parallelized-initial-load-for-cdc-based-streaming-from-postgres)により、大規模な単一テーブルを並列に読み込み可能。テラバイト規模のデータでも、従来の「数日」ではなく「数時間」で移行できます。
2. **最小10秒のレプリケーション遅延** – レプリケーションスロットは[再接続なしで継続的に消費](https://clickhouse.com/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#efficiently-flush-the-replication-slot)され、ClickHouseの[ReplacingMergeTree](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2)がエンドツーエンドの遅延を最小化します。
3. **スキーマ変更の自動レプリケーション** – [ADD COLUMNやDROP COLUMNといった操作](https://clickhouse.com/docs/integrations/clickpipes/postgres/schema-changes)にも対応し、手動による対応は不要です。
4. **テーブル・カラム単位の除外設定** – PII（個人情報）保護やネットワークスループットの最適化のために、きめ細かな制御が可能です。
5. **セキュアな接続** – [**AWS PrivateLink**](https://clickhouse.com/docs/integrations/clickpipes/aws-privatelink) や [**SSHトンネリング**](https://clickhouse.com/docs/integrations/clickpipes/postgres#optional-setting-up-ssh-tunneling) に対応しており、ソースのPostgresデータベースと安全かつプライベートに接続できます。
6. **Postgresのネイティブ機能に対応** – [パーティションテーブル](https://blog.peerdb.io/real-time-change-data-capture-for-postgres-partitioned-tables)、TOASTカラム、[配列やJSONなどの高度なデータ型](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#how-are-postgres-data-types-mapped-to-clickhouse)のレプリケーションもサポートしています。
7. **Open API（ベータ）** – [APIやCLIによるパイプの作成・管理](https://clickhouse.com/docs/integrations/clickpipes/postgres/faq#can-clickpipe-creation-be-automated-or-done-via-api-or-cli)が可能で、ClickHouse Cloud \+ ClickPipes環境を個別に構築・運用するISV（独立系ソフトウェアベンダー）にも最適です。[**Terraform**](https://registry.terraform.io/providers/ClickHouse/clickhouse/3.2.0-alpha1/docs/resources/clickpipe) **によるIaC対応も近日提供予定です。**


## 料金について [\#](/jp/blog/postgres-cdc-connector-clickpipes-ga-jp#%E6%96%99%E9%87%91%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)


一般提供（GA）の開始に伴い、[ベータ期間中にもお知らせしていた](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta#pricing)とおり、Postgres CDCコネクタの料金体系を導入します。私たちの目標は、PostgresデータベースをClickHouseにシームレスかつ手頃な価格で接続できるようにするというビジョンを保ちながら、非常に競争力のある価格を実現することです。


このコネクタは、外部のETLツールや他のデータベースプラットフォームにある類似機能と比べて、**5倍以上のコスト効率**を誇ります。


なお、Postgres CDC ClickPipesを利用している**すべてのお客様（既存・新規）に対して、2025年9月1日より月次課金が開始**されます。必要に応じてコストを最適化するための**3か月間の猶予期間**が設けられていますが、多くのお客様にとって設定の変更は不要と想定しています。料金体系の詳細、具体的な例、よくある質問については[こちら](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-for-postgres-cdc)をご覧ください。


## Postgres CDC を使って ClickHouse にデータを取り込む方法 [\#](/jp/blog/postgres-cdc-connector-clickpipes-ga-jp#postgres-cdc-%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6-clickhouse-%E3%81%AB%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E5%8F%96%E3%82%8A%E8%BE%BC%E3%82%80%E6%96%B9%E6%B3%95)


以下のリンクから、PostgresデータベースをClickHouse Cloudに接続して、超高速な分析を体験してみてください。


- [PostgresからClickHouseへのデータ取り込み（CDCを使用）](https://clickhouse.com/docs/en/integrations/clickpipes/postgres)
- [ClickPipes for Postgres よくある質問（FAQ）](https://clickhouse.com/docs/en/integrations/clickpipes/postgres/faq)
- [ClickHouse Cloudを無料で試す](https://clickhouse.com/docs/en/cloud/get-started/cloud-quick-start)
