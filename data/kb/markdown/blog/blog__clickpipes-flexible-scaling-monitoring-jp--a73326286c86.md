# ストリーミング ClickPipes の柔軟なスケーリングと強化されたモニタリング


## はじめに [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)


データ取り込みワークロードは千差万別で、そのパターンも予測しやすいものからそうでないものまで存在します。私たちが [ClickPipes](https://clickhouse.com/cloud/clickpipes) を開発した際には、オブジェクトストレージ、メッセージブローカー、データベースといったデータ基盤の最も一般的な構成要素から、あらゆるスループット、データサイズ、トポロジーに対応できるようにすることを目指しました。現在では、[Property Finder](https://clickhouse.com/blog/how-property-finder-migrated-to-clickhouse)、[Flock Safety](https://clickhouse.com/blog/why-flock-safety-turned-to-clickhouse)、[Seemplicity](https://clickhouse.com/blog/seemplicity-scaled-real-time-security-analytics-with-postgres-cdc-and-clickhouse) を含む数百社のお客様が、リアルタイムでの大規模データ取り込みを効率的かつ低コストで管理するために ClickHouse Cloud の ClickPipes を利用しています。


製品の進化に伴い、最も多かったリクエストのひとつは、多様なデータ取り込みワークロードのニーズにより適合させるために、ストリーミング ClickPipes の構成にさらなる柔軟性を持たせてほしい、というものでした。これに応える形で、今回 **新しいスケーリングオプション** を導入しました。これにより、ストリーミング ClickPipes の **水平スケーリングと垂直スケーリング** の両方を制御できるようになります。レプリカ数やレプリカサイズを直接選択できるようになり、さらにリソース使用状況を追跡できる強化されたモニタリングも利用可能になりました。


### ストリーミング ClickPipes のサイズ指定はどのように動作するのか？ [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0-clickpipes-%E3%81%AE%E3%82%B5%E3%82%A4%E3%82%BA%E6%8C%87%E5%AE%9A%E3%81%AF%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E5%8B%95%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B)



> **注記**: データベース用およびオブジェクトストレージ用の ClickPipes は異なるアーキテクチャを採用しており、計算リソースの割り当てを直接制御する必要はありません。今回の新機能はストリーミング ClickPipes のみに適用され、ClickPipe ごとのコストとパフォーマンスの比率をお客様がより柔軟に制御できるようにします。


ClickPipes は ClickHouse Cloud 内にレプリカをデプロイすることで動作します。各レプリカは Kafka または Kinesis のストリーミングデータソースのコンシューマーとして機能します。デフォルトでは、ClickPipes は **Extra Small レプリカ（0\.125 vCPU、512 MiB RAM）** を 1 つ起動してデータストリームを処理します。これらのレプリカは並列でデータを取得し、必要に応じて処理や変換を行い、ストリームのオフセットをコミットし、その結果を直接 ClickHouse サービスに書き込みます。このアーキテクチャにより、高スループットかつスケーラブルなデータ取り込みが可能となり、フォールトトレランスと効率的な負荷分散を実現します。


![unnamed.png](/uploads/unnamed_357981c8a1.png)
### レプリカとは？ [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E3%83%AC%E3%83%97%E3%83%AA%E3%82%AB%E3%81%A8%E3%81%AF)


ClickPipes における レプリカ とは、受信するデータストリームを処理するために並列で動作するデータ処理パイプラインのインスタンスを指します。各レプリカは Kafka または Kinesis ストリームのコンシューマーとして機能し、データ量が増加してもシステムが効率的にスケールし、パフォーマンスを維持できるようにします。レプリカは、ワークロードの特定のニーズに応じて 垂直方向（スケールアップ） と 水平方向（スケールアウト） の両方で拡張することが可能です。


## 柔軟なスケーリングオプション [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E6%9F%94%E8%BB%9F%E3%81%AA%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3)


ストリーミング ClickPipes のトポロジーをより細かく制御できるよう、レプリカ数（*水平スケーリング*）とレプリカサイズ（*垂直スケーリング*）の2つの新しいスケーリングオプションを導入しました。これらのスケーリングオプションは、新しい ClickPipe の作成時や既存の ClickPipe を編集する際に UI（下図参照）から選択可能です。また、[OpenAPI](https://clickhouse.com/docs/cloud/manage/api/swagger#tag/ClickPipes/paths/~1v1~1organizations~1%7BorganizationId%7D~1services~1%7BserviceId%7D~1clickpipes~1%7BclickPipeId%7D~1scaling/patch) や [Terraform](https://github.com/ClickHouse/terraform-provider-clickhouse/blob/619ba02fc70e5d672e221f424a9aeedc43fa2d0a/examples/clickpipe/multiple_pipes_example/main.tf) からもスケーリングを設定できます。


![unnamed.gif](/uploads/unnamed_8240b37fa9.gif)
### 垂直スケーリング（Vertical scaling） [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E5%9E%82%E7%9B%B4%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0vertical-scaling)


垂直スケーリング、または *スケールアップ* とは、ClickPipe 内の各レプリカに割り当てるリソース（CPU とメモリ）を増やすことを指します。これは、大きなペイロードや複雑なスキーマを持つ Kafka や Kinesis ストリームのように、各レプリカごとにより多くの処理能力が必要なワークロードに最適です。
垂直スケーリングでは以下の構成が利用できます：




| レプリカサイズ | CPU | メモリ |
| --- | --- | --- |
| Extra Small (デフォルト) | 0\.125 Cores | 512 Mb |
| Small | 0\.25 Cores | 1 Gb |
| Medium | 0\.5 Cores | 2 Gb |
| Large | 1 Core | 4 Gb |
| Extra Large | 2 Cores | 8 Gb |


### サイズ別ベンチマーク [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E3%82%B5%E3%82%A4%E3%82%BA%E5%88%A5%E3%83%99%E3%83%B3%E3%83%81%E3%83%9E%E3%83%BC%E3%82%AF)


以下は Kafka ストリームからデータを取り込む Large サイズ（1 vCPU / 4 GB）の ClickPipe レプリカに関する性能ベンチマークの一例です。ワークロードに適したレプリカサイズを選択する際の参考として利用してください。詳細や追加のサイズ選定ガイダンスについては、ドキュメントを参照ください。




| レプリカサイズ | メッセージサイズ | データ形式 | スループット |
| --- | --- | --- | --- |
| Large | 1\.6 kb | JSON | 63 mb/s |
| Large | 1\.6 kb | AVRO | 99 mb/s |


### 水平スケーリング（Horizontal scaling） [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E6%B0%B4%E5%B9%B3%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0horizontal-scaling)


水平スケーリング、または *スケールアウト* とは、ClickPipe にレプリカを追加することを指します。これによりワークロードを複数のレプリカに分散でき、より大量のデータを同時に処理できるようになります。Kafka と Kinesis は、それぞれ複数のパーティションやシャードにデータを分散する仕組みを持っており、ClickPipes は水平スケーリングによってこの仕組みに比例して処理をスケールできます。


## 強化されたリソースモニタリング [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E5%BC%B7%E5%8C%96%E3%81%95%E3%82%8C%E3%81%9F%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E3%83%A2%E3%83%8B%E3%82%BF%E3%83%AA%E3%83%B3%E3%82%B0)


各 ClickPipe の詳細ページには、レプリカごとの CPU およびメモリ使用率が表示され、レプリカ全体の平均リソース利用状況が確認できるようになりました。さらに、チャートには CPU とメモリの上限値も表示され、*スケールアップ* および *スケールアウト* イベントを含めた利用状況の推移を追跡できます。これにより、ワークロードをより深く理解し、自信を持ってリサイズ操作を計画できるようになります。


![unnamed (1).png](/uploads/unnamed_1_301ef80db2.png)
## 柔軟なスケーリングによる料金への影響 [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E6%9F%94%E8%BB%9F%E3%81%AA%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0%E3%81%AB%E3%82%88%E3%82%8B%E6%96%99%E9%87%91%E3%81%B8%E3%81%AE%E5%BD%B1%E9%9F%BF)


従来、ストリーミング ClickPipes はデフォルトで Medium サイズのレプリカごとに **$0\.05/時間** の固定料金で提供されていました。今回、レプリカサイズを設定できるようになったことで、デフォルトを Extra Small に変更し、料金モデルも更新しました。料金はレプリカサイズとレプリカ数に応じて決定され、最安で **$0\.0125/時間** から利用可能です。詳細な料金については [ClickPipes 料金ドキュメント](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-pricing) をご参照ください。




| レプリカサイズ | コンピュートユニット | RAM | vCPU | 料金/時間（レプリカあたり） |
| --- | --- | --- | --- | --- |
| Extra Small | 0\.0625 | 512 MiB | 0\.125 | $0\.0125 |
| Small | 0\.125 | 1 GiB | 0\.25 | $0\.025 |
| Medium | 0\.25 | 2 GiB | 0\.5 | $0\.05 |
| Large | 0\.5 | 4 GiB | 1\.0 | $0\.10 |
| Extra Large | 1\.0 | 8 GiB | 2\.0 | $0\.20 |



> **注記**: コンピュート料金に加え、ClickPipes は **$0\.04/GB** のデータ取り込みコストが発生します。詳細は [ClickPipes 料金ドキュメント](https://clickhouse.com/docs/cloud/manage/billing/overview#clickpipes-pricing) をご確認ください。


## 次のステップ [\#](/jp/blog/clickpipes-flexible-scaling-monitoring-jp#%E6%AC%A1%E3%81%AE%E3%82%B9%E3%83%86%E3%83%83%E3%83%97)


柔軟なスケーリングと強化されたリソースモニタリングによって、ストリーミング ClickPipes のコストとパフォーマンスのバランスを完全に制御できるようになりました。これにより、データ取り込みワークロードの変化にもより適切に備えることができます。詳細については [ドキュメント](https://clickhouse.com/docs/integrations/clickpipes) を参照し、ストリーミング ClickPipes のデプロイライフサイクル管理方法をご確認ください。
