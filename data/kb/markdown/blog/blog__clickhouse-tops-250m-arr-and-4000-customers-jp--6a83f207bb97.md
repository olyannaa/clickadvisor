# ClickHouse、ARR前年同期比300%超、顧客数4,000社突破、Claude搭載のAIエージェントを発表


Previous slide\<\-Next slide\-\>![](/_next/image?url=%2Fuploads%2FJP_arr250m_4000customers_1822cecf62.png&w=3840&q=75)![](/_next/image?url=%2Fuploads%2FJP_arr250m_4000customers_1822cecf62.png&w=384&q=75)*〜 年次カンファレンス「Open House 2026」にて発表。年間経常収益（ARR）は2億5,000万ドルに到達、新たなベンチマーク「CostBench」では競合比23倍の優れたコストパフォーマンスを実証 〜*


**サンフランシスコ — 2026年5月27日** — 本日、ClickHouseは第2回年次ユーザーカンファレンス「Open House 2026」を開幕し、創業以来最も躍進した四半期を象徴する一連の重大発表を行いました。


ClickHouseのサーバーレスクラウドサービスは、年間経常収益（ARR）が前年同期比の3倍以上となる2億5,000万ドルを突破しました。また、2026年1月以降に1,000社以上の新規顧客を獲得し、総顧客数は4,000社に達しています。


さらに、AI時代のワークロード需要に応えるため、Anthropic社の「Claude」を搭載したフルマネージド型のエージェント型分析サービス「ClickHouse Agents」のローンチ、主要クラウド・データウェアハウスのコストパフォーマンスを比較するオープンベンチマーク「CostBench」の公開、および同社初となる公式パートナープログラム「House Mates」の設立を発表しました。




---


## 主な発表概要 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#%E4%B8%BB%E3%81%AA%E7%99%BA%E8%A1%A8%E6%A6%82%E8%A6%81)


### 1\. 驚異的なビジネス成長 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#1-%E9%A9%9A%E7%95%B0%E7%9A%84%E3%81%AA%E3%83%93%E3%82%B8%E3%83%8D%E3%82%B9%E6%88%90%E9%95%B7)


2026年1月に4億ドルのシリーズD資金調達を完了した時点で約3,000社だった顧客数は、わずか1四半期で4,000社を突破しました。ARRも前年同期比3倍以上の2億5,000万ドル超に達しています。


- **新規・拡大ユーザーの例：** 既存ユーザーである Anthropic、Meta、Cursor、Sony、Tesla、Memorial Sloan Kettering、Lyft、Instacart などに加えて、新たにCapital One、Lovable、Decagon、Polymarket、Airwallexなどが導入。
- **Open House 2026の登壇企業：** Visa、Cisco、Intuit、Shopify、DoorDash、Mercado Libre、Vercel、Weights \& Biases、Zoox、Jump Tradingなど、企業のデータ基盤の中核としてClickHouseは幅広く採用されています。



> **Aaron Katz（CEO, ClickHouse）のコメント：**
> 「AIの処理には、ClickHouseの本質である『高い性能』と『コストパフォーマンス』が不可欠です。この四半期、その需要はかつてないほどの高まりを見せました。シリーズDの資金調達からわずか数ヶ月で1,000社を超えるお客様が増え、ARRが3倍に急増したという事実は、これが一過性のブームではなく、データインフラのあり方そのものが根本から変わったことを意味しています。今週の発表は、AIが実験段階から本格的な本番運用へと移行する中で、当社の市場における優位性をさらに確固たるものにするためのものです。」


### 2\. Claude搭載の「ClickHouse Agents」を発表 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#2-claude%E6%90%AD%E8%BC%89%E3%81%AEclickhouse-agents%E3%82%92%E7%99%BA%E8%A1%A8)


「ClickHouse Agents」は、ClickHouse Cloud上で提供される、Claudeを基盤としたフルマネージドのエージェント型分析サービスです。ノーコードのエージェントビルダーにより、誰でも簡単にClickHouseのデータを基盤としたAIエージェントを定義・構築・デプロイできます。


- **機能：** チャットインターフェース、サンドボックス化されたコードインタープリター、共有可能なアーティファクト、スキル管理、メモリ、マルチエージェントワークフローなどを標準装備。
- **拡張性：** ClickHouseのほか、MCP（Model Context Protocol）互換のサードパーティシステムや、AWS Agent Registryともネイティブに連携し、組織全体のデータを活用可能です。


#### 【その他のAI向けプロダクト投資】 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#%E3%81%9D%E3%81%AE%E4%BB%96%E3%81%AEai%E5%90%91%E3%81%91%E3%83%97%E3%83%AD%E3%83%80%E3%82%AF%E3%83%88%E6%8A%95%E8%B3%87)


- **Managed Postgres（パブリックベータ版）：** ClickHouseの分析機能とネイティブに統合。AIアプリケーション開発において、トランザクション状態（ステート）の管理と、同一データに対する高スループットな分析を単一のプラットフォーム上で実現します。
- **AIオブザーバビリティ（可観測性）：** インフラやモデル学習のモニタリングを行う「Managed ClickStack」を、フルマネージドサービスとして提供開始。また、2026年1月に買収した「Langfuse」により、本番環境におけるAIエージェントの出力の正確性、評価、モデルコストの追跡（エージェント・オブザーバビリティ）が可能になります。
- **分析機能の拡張：** オブザーバビリティやAIのグラウンディング（根拠付け）で最も需要の高い「全文検索機能」の一般提供（GA）を開始。さらに、クエリの自動最適化機能により、TPC\-Hをはじめとする標準的なJOINベンチマークにおいて、既存の主要データウェアハウスと同等以上の性能を達成しました。
- **ClickHouse Cloudの進化：** 「エージェント駆動型オンボーディング」により、新規ユーザーは手動でのスキーマ設計を行うことなく、サインアップから最初の本番クエリ実行までをシームレスに行えます。また、企業のレジリエンス（可用性）を強化する「クロスリージョン・レプリケーション」の提供を開始しました。


### 3\. コストパフォーマンスを可視化するベンチマーク「CostBench」 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#3-%E3%82%B3%E3%82%B9%E3%83%88%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%82%92%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%99%E3%82%8B%E3%83%99%E3%83%B3%E3%83%81%E3%83%9E%E3%83%BC%E3%82%AFcostbench)


AIワークロードには、高い同時実行性と低レイテンシが求められるため、単なる処理速度だけでなく「コストパフォーマンス」が極めて重要になります。本日公開された「CostBench」は、各ベンダーの実際の計算料金モデルを同一の分析ワークロードに適用し、コストを直接比較できるオープンなベンチマークです。


- **結果：** ClickHouse Cloud、Snowflake、Databricks、BigQuery、Redshiftを比較した結果、さまざまなデータスケールにおいて「高速かつ低コスト」の領域を維持できたのはClickHouse Cloudのみでした。最も近い競合相手でも、コストパフォーマンスはClickHouseより23倍劣る結果となっています。
- *詳細は [clickhouse.com/benchmarks](https://clickhouse.com/benchmarks) にて公開中。*


### 4\. 初の公式パートナープログラム「House Mates」の発足 [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#4-%E5%88%9D%E3%81%AE%E5%85%AC%E5%BC%8F%E3%83%91%E3%83%BC%E3%83%88%E3%83%8A%E3%83%BC%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0house-mates%E3%81%AE%E7%99%BA%E8%B6%B3)


世界6大陸から25社以上のテクノロジーパートナー、35社以上のサービス／コンサルティング／チャネルパートナー（dbt Labs、Fivetran、Sigma、Notion、Temporal、Tiger Analytics、DoIT、Ciklum、MegazoneCloud等）を創設メンバーに迎え、初の公式パートナーコミュニティを立ち上げました。


- **3つのパートナータイプと3つのパートナーティア：** 「サービスパートナー」「チャネルパートナー」「テクノロジーパートナー」の3タイプ、および「プライム」「アクセラレート」「イグナイト」の3ティアで構成。
- AWS、Microsoft、Google Cloudとの深い連携をベースに、エコシステム全体へとプログラムを拡張し、顧客に対して構築済みの統合環境や実証済みの導入ノウハウを提供します。




---


### ClickHouseについて [\#](/jp/blog/clickhouse-tops-250m-arr-and-4000-customers-jp#clickhouse%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)


ClickHouseは、リアルタイムデータ処理および分析のために設計された、高速なオープンソースのカラム型データベース管理システムです。高いパフォーマンスを実現するよう設計されたClickHouse Cloudは、卓越したクエリ速度と高い同時実行性能を提供し、膨大なデータ量から即座に洞察を得ることが求められるアプリケーションに最適です。


AIエージェントがソフトウェアにますます組み込まれ、これまでよりもはるかに頻繁かつ複雑なクエリを生成するようになる中で、ClickHouseは、こうした課題に対応するために特別に設計された、高スループットかつ低レイテンシのエンジンを提供します。




---


![Founders_AMS_2025.jpeg](/uploads/Founders_AMS_2025_df2919ac2a.jpeg)
※本記事（プレスリリース）は、米国ClickHouse本社が発表した内容の抄訳版です。原文は下記URLをご参照ください。
[https://clickhouse.com/blog/clickhouse\-tops\-250m\-arr\-and\-4000\-customers](https://clickhouse.com/blog/clickhouse-tops-250m-arr-and-4000-customers)
