# Laravel Nightwatchのオブザーバビリティパイプラインの内側:Amazon MSKとClickHouse Cloudによるリアルタイムイベント処理


*元記事は [AWS blog](https://aws.amazon.com/blogs/big-data/how-laravel-nightwatch-handles-billions-of-observability-events-in-real-time-with-amazon-msk-and-clickhouse-cloud/) に掲載されました*


世界で最も人気のあるWebフレームワークの1つである[Laravel](https://laravel.com/)は、開発者にアプリケーションパフォーマンスのリアルタイムなインサイトを提供するため、自社製のオブザーバビリティプラットフォーム[Laravel Nightwatch](https://nightwatch.laravel.com/)をリリースしました。AWSマネージドサービスと[ClickHouse Cloud](https://clickhouse.com/cloud)を全面的に基盤として構築されたこのサービスは、サブセカンドのクエリレイテンシを維持しながら、すでに1日あたり10億件を超えるイベントを処理しており、開発者は自分のアプリケーションの健全性を即座に可視化できます。


[Amazon Managed Streaming for Apache Kafka (Amazon MSK)](https://aws.amazon.com/msk/) を ClickHouse Cloud と [AWS Lambda](https://aws.amazon.com/lambda/) と組み合わせることで、Laravel Nightwatch は Laravel ならではのシンプルさと開発者体験を維持しつつ、大規模かつ低レイテンシなモニタリングを実現しています。


## 課題: グローバルな開発者コミュニティ向けにリアルタイムモニタリングを提供する [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E8%AA%B2%E9%A1%8C-%E3%82%B0%E3%83%AD%E3%83%BC%E3%83%90%E3%83%AB%E3%81%AA%E9%96%8B%E7%99%BA%E8%80%85%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E5%90%91%E3%81%91%E3%81%AB%E3%83%AA%E3%82%A2%E3%83%AB%E3%82%BF%E3%82%A4%E3%83%A0%E3%83%A2%E3%83%8B%E3%82%BF%E3%83%AA%E3%83%B3%E3%82%B0%E3%82%92%E6%8F%90%E4%BE%9B%E3%81%99%E3%82%8B)


Laravelフレームワークは世界中で数百万のアプリケーションを支えており、毎月数十億のリクエストを処理しています。各リクエストでは、データベースクエリ、キュージョブ、キャッシュルックアップ、メール、通知、例外など、潜在的に数百件ものオブザーバビリティイベントが生成されることがあります。Nightwatch のローンチにあたり、Laravel はグローバルコミュニティからの即時の採用を予想しており、初日から数万のアプリケーションが24時間体制でイベントを送信することを見込んでいました。


Laravel Nightwatch には、以下を満たすアーキテクチャが必要でした:


- 顧客アプリケーションから毎秒数百万件のJSONイベントを確実に取り込めること。
- リアルタイムダッシュボード向けにサブセカンドの分析クエリを提供できること。
- 予測不能なトラフィックスパイクに対応するために水平方向にスケールできること。
- これらすべてをコスト効率よく、低メンテナンスで提供できること。


課題は、グローバル規模でデータを処理し、アプリケーションの健全性についての深いインサイトを提供しつつ、開発者にとってシンプルなセットアップ体験を損なわないことでした。



## ソリューション: 疎結合なストリーミング・アナリティクスパイプライン [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E3%82%BD%E3%83%AA%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-%E7%96%8E%E7%B5%90%E5%90%88%E3%81%AA%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A2%E3%83%8A%E3%83%AA%E3%83%86%E3%82%A3%E3%82%AF%E3%82%B9%E3%83%91%E3%82%A4%E3%83%97%E3%83%A9%E3%82%A4%E3%83%B3)


![blog-laravel-1.png](/uploads/blog_laravel_1_2b8e4a05cc.png)
Laravel Nightwatch は、上図に示すように、トランザクションワークロードと分析ワークロードを分離した、デュアルデータベース、ストリーミングファーストのアーキテクチャを実装しました。


- **トランザクションワークロード** – ユーザーアカウント、組織設定、課金などのワークロードは[Amazon RDS](https://aws.amazon.com/rds/) for PostgreSQL 上で動作します。
- **分析ワークロード** – テレメトリイベント、メトリクス、クエリログ、リクエストトレースは ClickHouse Cloud で処理されます。


### 主要コンポーネント [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E4%B8%BB%E8%A6%81%E3%82%B3%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%8D%E3%83%B3%E3%83%88)


このソリューションの主要コンポーネントは以下の通りです:


1. **取り込みレイヤー**
	- [Amazon API Gateway](https://aws.amazon.com/gateway) が顧客アプリケーションに組み込まれた Laravel エージェントからテレメトリを受信します
	- **Lambda** がイベントの検証とエンリッチメントを行います。検証・エンリッチされたイベントは Amazon MSK に発行され、スケーラビリティのためにパーティション化されます
2. **アナリティクスへのストリーミング**
	- ClickHouse Cloud の [ClickPipes](https://clickhouse.com/cloud/clickpipes) が MSK トピックを直接サブスクライブし、抽出、変換、ロード (ETL) パイプラインの構築と管理の必要性を軽減します
	- ClickHouse のマテリアライズドビューが生のJSONを事前集計し、クエリしやすい形式に変換します
3. **ダッシュボードと配信**
	- Laravel、Inertia、React で構築された Nightwatch ダッシュボードは、[AWS Fargate for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html) 上で動作します
	- [Amazon ElastiCache for Redis](https://aws.amazon.com/elasticache/redis/) がセッションとキャッシュルックアップを高速化します
	- Cloudflare CDN がグローバルユーザーへの低レイテンシ配信を提供します


## なぜ Amazon MSK と ClickHouse Cloud なのか? [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E3%81%AA%E3%81%9C-amazon-msk-%E3%81%A8-clickhouse-cloud-%E3%81%AA%E3%81%AE%E3%81%8B)


Nightwatch には、耐久性があり、水平方向にスケーラブルで、メンテナンスの少ないストリーミングのバックボーンが必要です。


[Amazon MSK Express ブローカー](https://docs.aws.amazon.com/msk/latest/developerguide/msk-broker-types-express.html) を使用することで、低レイテンシ、弾力的なスケーリング、簡素化されたオペレーションのメリットを享受しながら、負荷テスト中に毎秒100万件を超えるイベントを達成しました。MSK Express ブローカーはストレージのサイジングやプロビジョニングが不要で、標準的な Apache Kafka ブローカーに比べて最大20倍速くスケールアップし、90%速く復旧します。さらに、信頼性の高いパフォーマンスのためにベストプラクティスに準拠したデフォルト値とクライアントクォータが適用されます。Lambda、[Amazon Simple Storage Service (Amazon S3\)](https://aws.amazon.com/s3/)、[Amazon CloudWatch](https://aws.amazon.com/cloudwatch) などの他のAWSサービスとのシームレスな統合により、堅牢なエンドツーエンドのストリーミングアーキテクチャを簡単に構築できました。


これらのイベントをリアルタイムで取り込み、変換するために、Nightwatch は ClickHouse Cloud とそのマネージド統合プラットフォーム [ClickPipes](https://clickhouse.com/docs/integrations/clickpipes) を使用しています。ClickHouse Cloud は、従来の行ベースのデータベースに比べてアナリティクスにおいて最大100倍速いクエリパフォーマンスを提供することで、分析ワークロードに優れています。高度な圧縮アルゴリズムにより最大90%のストレージ削減を実現し、高パフォーマンスを維持しながらインフラコストを大幅に削減します。カラムナアーキテクチャと最適化された実行エンジンにより、ClickHouse Cloud は数十億行を1秒未満でクエリできるため、Laravel Nightwatch はグローバル規模でリアルタイムダッシュボードと分析を提供できます。


ClickPipes を使用して Amazon MSK と ClickHouse を統合することで、Laravel は ETL パイプラインの構築と管理に伴う運用負担を軽減し、レイテンシと複雑性を低減しました。


## 課題の克服 [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E8%AA%B2%E9%A1%8C%E3%81%AE%E5%85%8B%E6%9C%8D)


### テストの複雑性 [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E3%83%86%E3%82%B9%E3%83%88%E3%81%AE%E8%A4%87%E9%9B%91%E6%80%A7)


合成ベンチマークやテストデータセットも有用な結果をもたらしますが、本番デプロイ前にインフラとコードを厳密にテストするには、より現実的なワークロードが必要です。チームは Terraform を使用してアプリケーションコードと並行してインフラを管理し、複数の開発・テスト環境を作成して、各リリース前に独自のアプリケーションを使ってプラットフォームを社内でテストしました。


### マルチリージョンインフラ [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E3%83%9E%E3%83%AB%E3%83%81%E3%83%AA%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%82%A4%E3%83%B3%E3%83%95%E3%83%A9)


複数のデータ保存リージョンに対応する必要性も課題をもたらし、レイテンシ、複雑性、コストが最大の懸念事項でした。しかし、AWS、ClickHouse Cloud、Cloudflare のスタックは、強力なネットワーキングツールとスケーリングオプションを提供してくれました。VPCピアリング、RDSレプリケーション、グローバルサーバーロードバランシングがネットワーキング面の重作業を担う一方で、各リソースをスケールし適切なサイズに調整できることにより、コストを最小限に抑えることができました。


### 大規模でのクエリパフォーマンス [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E5%A4%A7%E8%A6%8F%E6%A8%A1%E3%81%A7%E3%81%AE%E3%82%AF%E3%82%A8%E3%83%AA%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9)


マテリアライズドビュー、インテリジェントな時系列パーティショニング、特化したClickHouseコーデックにより、データ量が数十億規模に成長してもクエリはサブセカンドを維持できました。さらに、コンピュートの分離により、異なるワークロードが同じデータにアクセスしながら独立してスケールでき、各ロードの要件に応じて水平・垂直方向にクラスタを適切にサイジングすることが可能になりました。


## 成果 [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E6%88%90%E6%9E%9C)


Laravel Nightwatch のローンチは期待を超えました:


- 最初の24時間で5,300人のユーザーが登録
- 初日に5億件のイベントを処理
- ダッシュボードリクエストの平均レイテンシ97ミリ秒
- 76万件の例外をリアルタイムで記録・分析


Amazon MSK と ClickHouse Cloud を基盤として構築することで、パフォーマンスや開発者体験を犠牲にすることなく、ゼロから数十億イベントへとスケールすることができました。


## 今後の展望 [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E4%BB%8A%E5%BE%8C%E3%81%AE%E5%B1%95%E6%9C%9B)


Laravelはこれから Nightwatch を以下のように拡張する予定です:


- 米国と欧州外のデータ主権要件を持つ顧客に対応するための **より多くのリージョン**
- 顧客のアプリケーションについてさらに深いインサイトを提供する **より広範なデータ収集**
- より厳格なコンプライアンス要件を持つ顧客に対応するための **SOC 2 認証**
- ユーザーに影響が及ぶ前に問題を特定する **より高度なモニタリングと分析**


現在のアーキテクチャは、趣味レベルからエンタープライズ規模まで、あらゆる規模のアプリケーションを快適にサポートし(寛大なフリーティアを含む)、パフォーマンスの低下なしに月間1兆を超えるイベントを処理できるように設計されています。


## まとめ [\#](/jp/blog/laravel-nighwatch-clickhouse-jp#%E3%81%BE%E3%81%A8%E3%82%81)


Laravel Nightwatch は、Amazon MSK、ClickHouse Cloud、AWSサーバーレステクノロジーを組み合わせることで、コスト効率の高いリアルタイムモニタリングプラットフォームをグローバル規模で構築できることを実証しています。初日からスケールを念頭に設計することで、Laravel はコミュニティが期待する開発者フレンドリーな体験を維持しながら、数十億イベントにわたるサブセカンドの分析を提供しました。
