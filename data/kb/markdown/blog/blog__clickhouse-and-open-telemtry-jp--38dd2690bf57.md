# ClickHouse と OpenTelemetry


今年初めに、ClickHouseチームはClickHouse用のOpenTelemetryエクスポーターの公式サポートと貢献を始めることを決定しました。このエクスポーターは最近、ログとトレースの両方でベータ版に移行しました（現在のOTelエクスポーターエコシステムでの最高レベルです）。このポストでは、このマイルストーンを機会として、OpenTelemetryとClickHouseの統合について紹介したいと思います。


## OpenTelemetryとは何か？ [\#](/jp/blog/clickhouse-and-open-telemtry-jp#opentelemetry%E3%81%A8%E3%81%AF%E4%BD%95%E3%81%8B)


OpenTelemetry（略してOTel）は、Cloud Native Computing Foundation（CNCF）から提供されるオープンソースのフレームワークで、テレメトリーデータの標準化された収集、処理、エクスポートを可能にします。主なオブザーバビリティの柱（トレース、メトリクス、ログ）を軸に、OTelは統一された、ベンダーニュートラルなアプローチを提供し、開発者と運用チームがシステムの健康状態を把握し、分散システムの問題を診断できるようにします。


OTelはまた、複数の言語に対応した計測ライブラリを提供しており、最小限のコード変更でデータ収集を自動化します。OTel Collectorはこのデータフローを管理し、さまざまなバックエンドプラットフォームにテレメトリーデータをエクスポートするゲートウェイとして機能します。一貫したオブザーバビリティの標準を提供することで、OTelはチームが効率的にテレメトリーデータを収集し、複雑なシステムに関する洞察を得るのを助けます。


## OpenTelemetryが重要な理由は？ [\#](/jp/blog/clickhouse-and-open-telemtry-jp#opentelemetry%E3%81%8C%E9%87%8D%E8%A6%81%E3%81%AA%E7%90%86%E7%94%B1%E3%81%AF)


オブザーバビリティの分断されたベンダー主導の状況が支配していますが、OTelは標準化された、柔軟でオープンなアプローチをもたらします。ソフトウェアアプリケーションがより複雑になり、マイクロサービスやクラウドベースのアーキテクチャにまたがると、システム内外で何が起きているのかを追跡することが難しくなります。OTelはこの問題を解決するために、主要なテレメトリーデータの一貫した収集と分析を可能にします。


ベンダーニュートラルなアプローチは特に価値があり、特定のモニタリングツールにロックインされるのを避けることができます。OTelを使用することで、組織はさまざまなオブザーバビリティバックエンド間を簡単に切り替えたり、組み合わせて使用することができ、コスト削減と柔軟性向上が実現できます。テレメトリーデータの標準化されたフォーマットは、マルチクラウドやハイブリッド環境においてもシステム間の統合を簡素化します。


## OpenTelemetry \+ ClickHouse [\#](/jp/blog/clickhouse-and-open-telemtry-jp#opentelemetry--clickhouse)


以前のブログで、ClickHouseのようなツールが大量のオブザーバビリティデータを処理できることから、専有システムに代わるオープンソースの有力な選択肢となることを説明しました。SQLベースのオブザーバビリティは、SQLに慣れたチームに適しており、コスト管理と拡張性を提供します。OTelのようなオープンソースのツールが進化を続ける中、このアプローチはデータニーズの大きい組織にとってますます実用的になっています。


SQLベースのオブザーバビリティスタックの重要なコンポーネントはOpenTelemetry Collectorです。OTelコレクターはSDKや他のソースからテレメトリーデータを収集し、サポートされているバックエンドに転送します。それはテレメトリーデータを受信、処理、エクスポートするための中央集約的なハブとして機能します。OTelコレクターは単一のアプリケーション（エージェント）のためのローカルコレクターとして、または複数のアプリケーション（ゲートウェイ）のための中央集約的なコレクターとして機能できます。


![img09_4566662115.0.png](/uploads/img09_4566662115.png)
コレクターはさまざまなデータフォーマットをサポートするエクスポーターの範囲を含んでいます。エクスポーターはデータを選択したバックエンドまたはオブザーバビリティプラットフォームに送信します、例えばClickHouseのように。開発者は複数のエクスポーターを構成して、必要に応じてテレメトリーデータを異なる宛先にルーティングすることができます。


私たちはClickHouseでの自身のニーズにOpenTelemetryを使用しており、多くの成功したユーザーがそれを採用しているのを見て、公式にClickHouseのためのOTelエクスポーターをサポートし、このコンポーネントの開発に貢献することに決めました。ClickHouse用のOTelエクスポーターは、その管理者（[@hanjm](https://www.github.com/hanjm), [@dmitryax](https://www.github.com/dmitryax), [@Frapschen](https://www.github.com/Frapschen)）とコミュニティの貢献によってすでに良い状態にあり、私たちが本当に求めているのは、規模に応じた重要なユースケースのサポートです。


## すべてを支配する1つのスキーマ [\#](/jp/blog/clickhouse-and-open-telemtry-jp#%E3%81%99%E3%81%B9%E3%81%A6%E3%82%92%E6%94%AF%E9%85%8D%E3%81%99%E3%82%8B1%E3%81%A4%E3%81%AE%E3%82%B9%E3%82%AD%E3%83%BC%E3%83%9E)


スキーマに関する問題は、私たちが最初に取り組むことに決めた課題でした。「一つの方法ですべてに対応する」ことはできません。これは、ClickHouseのためのエクスポーターを設計する際に受け入れるべき厳しい現実です。大規模なデータベースの場合、何をインサートし、どのようにして取り出すかについて良いアイデアを持っている必要があります。ClickHouseは、**あなたのユースケースのためにあなたのスキーマを最適化する**ことで最良のパフォーマンスを発揮します。


OpenTelemetryデータの場合、これはさらに重要です。OpenTelemetryのデザイナーでさえ、SDKを執筆する際にこの問題に直面しました。言語とツールの大規模なエコシステムをどのように単一のテレメトリーパイプラインに適合させるか？各チームはログやトレースの検索パターンを持っており、これをテーブルスキーマをモデル化する際に考慮する必要があります。データはどれだけの期間保持されますか？あなたのアーキテクチャはサービス名でフィルタリングするのが好きですか、それとも他の識別子でパーティションを分ける必要がありますか？Kubernetesのポッド名でフィルタリングするためのカラムが必要ですか？すべての人を含めることは不可能であり、そうすることでパフォーマンスと使い勝手を犠牲にすることはできません。


\*\*「一つの方法ですべてに対応する」\*\*は私たちが望める最善のものであり、ClickHouseエクスポーターの場合も同様です。ログ、トレース、メトリクスのためにデフォルトのスキーマが提供されています。このデフォルトのスキーマは、ほとんどの一般的なテレメトリーユースケースに対して良好なパフォーマンスを発揮しますが、スケールでのロギングソリューションを構築しようとしている場合は、ClickHouse内でデータがどのように保存され、アクセスされているかを理解し、関連する主キーを選択することをお勧めします。これは内部ログソリューションで43ペタバイト以上のOTelデータを保存している場合と同様です（2024年10月時点）。


![log_house_43pb.png](/uploads/log_house_43pb_1d229d40b9.png)
*[LogHouse](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog)からの統計情報、ClickHouse Cloud OTelベースのログプラットフォーム*


エクスポーターはデフォルトで必要なテーブルを作成しますが、本番ワークロードには推奨されません。エクスポーターのコードを変更せずにテーブルスキーマを置き換えたい場合は、自分でテーブルを作成すれば簡単にできます。構成ファイルには、データが送信されるテーブル名のみが定義されます。これにより、カラム名がエクスポーターによってインサートされた内容と一致し、タイプが基になるデータと互換性があることが要求されます。



```
{
  "Timestamp": "2024-06-15 21:48:06.207795400",
  "TraceId": "10c0fcd202c978d6400aaa24f3810514",
  "SpanId": "60e8560ae018fc6e",
  "TraceFlags": 1,
  "SeverityText": "Information",
  "SeverityNumber": 9,
  "ServiceName": "cartservice",
  "Body": "GetCartAsync called with userId={userId}",
  "ResourceAttributes": {
    "container.id": "4ef56d8f15da5f46f3828283af8507ee8dc782e0bd971ae38892a2133a3f3318",
    "docker.cli.cobra.command_path": "docker%20compose",
    "host.arch": "",
    "host.name": "4ef56d8f15da",
    "telemetry.sdk.language": "dotnet",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.version": "1.8.0"
  },
  "ScopeName": "cartservice.cartstore.RedisCartStore",
  "ScopeAttributes": {},
  "LogAttributes": {
    "userId": "71155994-7b72-428a-9d51-43962a82ae43"
  }
}

```

*OpenTelemetryで生成されたログイベントの例*


提供されるデフォルトのスキーマとは大きく異なるスキーマが必要な場合、ClickHouseの[マテリアライズドビュー](https://clickhouse.com/docs/en/observability/schema-design#materialized-views)を使用することができます。デフォルトのテーブルスキーマは利用可能な出発点を提供しますが、エクスポーターがどのようなデータを提供できるかのガイドとしても見ることができます。自分自身のテーブルをモデル化している場合は、特定のカラムを含めるか除外するか、さらにはそのタイプを変更することを選択できます。内部のログでは、これを機会としてKubernetesに関連するカラム、例えばポッド名を抽出しました。次に、特定のクエリパターンに対するパフォーマンスを最適化するために、これをテーブルの主キーに組み込みました。


本番デプロイメントでは、デフォルトでテーブルの作成を無効にするのがベストです。複数のエクスポータープロセスが実行されている場合は、それらがテーブルを作成するために（おそらく異なるバージョンで）競合することになります。この[ユーザーガイド](https://clickhouse.com/docs/en/observability)では、ClickHouseをオブザーバビリティストアとして使用するためのベストプラクティスを挙げています。


以下に、私たちのClickHouse Cloud Logging SolutionであるLogHouseで使用しているカスタムスキーマを示します。



```
CREATE TABLE otel.server_text_log_0
(
	`Timestamp` DateTime64(9) CODEC(Delta(8), ZSTD(1)),
	`EventDate` Date,
	`EventTime` DateTime,
	`TraceId` String CODEC(ZSTD(1)),
	`SpanId` String CODEC(ZSTD(1)),
	`TraceFlags` UInt32 CODEC(ZSTD(1)),
	`SeverityText` LowCardinality(String) CODEC(ZSTD(1)),
	`SeverityNumber` Int32 CODEC(ZSTD(1)),
	`ServiceName` LowCardinality(String) CODEC(ZSTD(1)),
	`Body` String CODEC(ZSTD(1)),
	`Namespace` LowCardinality(String),
	`Cell` LowCardinality(String),
	`CloudProvider` LowCardinality(String),
	`Region` LowCardinality(String),
	`ContainerName` LowCardinality(String),
	`PodName` LowCardinality(String),
	`query_id` String CODEC(ZSTD(1)),
	`logger_name` LowCardinality(String),
	`source_file` LowCardinality(String),
	`source_line` LowCardinality(String),
	`level` LowCardinality(String),
	`thread_name` LowCardinality(String),
	`thread_id` LowCardinality(String),
	`ResourceSchemaUrl` String CODEC(ZSTD(1)),
	`ScopeSchemaUrl` String CODEC(ZSTD(1)),
	`ScopeName` String CODEC(ZSTD(1)),
	`ScopeVersion` String CODEC(ZSTD(1)),
	`ScopeAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
	`ResourceAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
	`LogAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
	INDEX idx_trace_id TraceId TYPE bloom_filter(0.001) GRANULARITY 1,
	INDEX idx_thread_id thread_id TYPE bloom_filter(0.001) GRANULARITY 1,
	INDEX idx_thread_name thread_name TYPE bloom_filter(0.001) GRANULARITY 1,
	INDEX idx_Namespace Namespace TYPE bloom_filter(0.001) GRANULARITY 1,
	INDEX idx_source_file source_file TYPE bloom_filter(0.001) GRANULARITY 1,
	INDEX idx_scope_attr_key mapKeys(ScopeAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_scope_attr_value mapValues(ScopeAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_res_attr_key mapKeys(ResourceAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_res_attr_value mapValues(ResourceAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_log_attr_key mapKeys(LogAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_log_attr_value mapValues(LogAttributes) TYPE bloom_filter(0.01) GRANULARITY 1,
	INDEX idx_body Body TYPE tokenbf_v1(32768, 3, 0) GRANULARITY 1
)
ENGINE = SharedMergeTree
PARTITION BY EventDate
ORDER BY (PodName, Timestamp)
TTL EventTime + toIntervalDay(180)
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1;

```

*LogHouseのOTelスキーマ、ClickHouse Cloud Logging Solution*


LogHouseスキーマに関するいくつかの観察ポイント：


- 順序キー `(PodName, Timestamp)`を使用しています。これは、ユーザーが通常これらのカラムでフィルタリングするクエリアクセスパターンに最適化されています。ユーザーは自分の期待されるワークフローに基づいてこれを変更する必要があります。
- 非常に高いカーディナリティのものを除くすべてのStringカラムに対して`LowCardinality(String)`型を使用しています。これにより、文字列の値が辞書エンコードされ、圧縮が向上し、読み取りパフォーマンスが向上しました。現在の経験則として、10,000以下のユニークな値を持つ文字列カラムに対してこのエンコーディングを適用しています。
- すべてのカラムに対するデフォルトの圧縮コーデックはレベル1のZSTDです。これはデータがS3に保存されているという事実に特有のものです。ZSTDはLZ4のような代替手段と比較して圧縮が遅い場合がありますが、圧縮率が優れており、一貫して高速な解凍を提供します（[約20%のばらつき](https://engineering.fb.com/2016/08/31/core-data/smaller-and-faster-data-compression-with-zstandard/)）。これらはS3をストレージとして使用する際に好ましい特性です。
- [OTelスキーマ](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/c008f8feb719b30d997bd529bb7360372d4a7161/exporter/clickhouseexporter/exporter_logs.go#L144)から継承して、マップのキーおよび値に対してbloom\_filtersを使用しています。これにより、`Bloom フィルター`データ構造に基づいて、マップのキーと値に対してセカンダリインデックスが提供されます。Bloom フィルターは、わずかな確率で偽陽性が発生するコストで、集合のメンバーシップを効率的にテストできるデータ構造です。理論的には、これにより、ディスク上のグラニュールに特定のマップキーや値が含まれているかを迅速に評価することができます。このフィルターは論理的に意味がある場合があります。なぜなら、いくつかのマップキーや値は、ポッド名やタイムスタンプという順序キーと相関しているべきだからです。つまり、特定のポッドには特定の属性があるでしょう。しかし、他のものはすべてのポッドに存在します。これらの値でクエリを実行する場合、フィルタリング条件が少なくとも1行のグラニュールに一致する確率が非常に高いため、これらのクエリの高速化は期待できません（この構成では、ブロックはグラニュールであり、GRANULARITY\=1）。順序キーと列/式の間に相関関係が必要な理由についての詳細は[こちら](https://clickhouse.com/docs/en/optimize/skipping-indexes#skip-best-practices)を参照してください。この一般的なルールは、Namespace などの他の列にも適用されています。一般的に、これらの Bloom フィルターは広範に適用されており、最適化が必要です。これは保留中のタスクです。偽陽性率0\.01も調整されていません。


### 次のステップ [\#](/jp/blog/clickhouse-and-open-telemtry-jp#%E6%AC%A1%E3%81%AE%E3%82%B9%E3%83%86%E3%83%83%E3%83%97)


ClickHouseエクスポーターには改善の余地があります。私たちの目標は、最新のClickHouseサーバーの開発にエクスポーターを最新の状態に保つことです。新しい最適化が見つかり、新しいパフォーマンスベンチマークがテストされると、ログ、トレース、メトリクスのデフォルトスキーマを改善する方法が見つかることでしょう。


多くのオブザーバビリティユースケースに影響を与える特長の1つに、ClickHouseの新しいJSONデータ型のサポートがあります。これにより、ログやトレースの属性がどのように保存され、検索されるかが簡素化されます。新機能に加えて、OTel\+ClickHouseのユーザーは頻繁にリポジトリにフィードバックを提出しており、これが過去1年間で多くの機能改善やバグ修正につながっています。


## 付録: OpenTelemetryへの貢献 [\#](/jp/blog/clickhouse-and-open-telemtry-jp#%E4%BB%98%E9%8C%B2-opentelemetry%E3%81%B8%E3%81%AE%E8%B2%A2%E7%8C%AE)


オープンソースの魔法は、コミュニティの協力的な力にあります：OpenTelemetryに貢献することで、オブザーバビリティの未来に直接的な影響を与え、形作ることができます。コードの改善、ドキュメントの強化、フィードバックの提供、どれだけの貢献であっても、このプロジェクトの範囲を広げ、開発者に利益をもたらします。このセクションでは、いくつかのヒントを共有します。


![society_oss.png](/uploads/society_oss_4277f26f41.png)
OpenTelemetryへの貢献は、ほとんどの他のオープンソースプロジェクトと似ています。メンバーである必要はなく、誰でも貢献できます。問題についての意見を共有したり、プルリクエストを開いたりすることもすべての貢献がプロジェクトに歓迎されます。


コンポーネントのメンテナーとして、貢献するために最も価値のあるものは、実際には最も簡単なことです：フィードバックです。ユーザーがどのようなバグに直面しているかを知ることや、複数のユーザーにとっての体験を向上させる機能のギャップを知ることは非常に価値があります。私たちは内部でClickHouseエクスポーターを使用していますが、私たち自身の使用は他の人の使用とは異なるため、コミュニティから学ぶことはたくさんあります。


もちろん、OpenTelemetryとClickHouseの両方に熟知し、エクスポーターに巧妙な貢献ができるユーザーもいます。例として、最近の[ClickHouseにインサートする前にマップ属性をソートする](https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/33634)取り組みがあります。以前のバージョンでは、ログとトレースの属性は受信した時点で単純にインサートされていました。これは常に最良の圧縮をもたらすわけではありません。同じデータを反映しているかもしれませんが、順序が異なる可能性があります。マップ属性をキーでソートすることによって、ClickHouseの優れた圧縮力を活用することができます。このアイデアは外部の問題でメモされていましたが、まだ追加されていませんでした。コミュニティのユーザーがこれを見つけて、彼らの実装を[プルリクエスト](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/35725)として提出しました。


OpenTelemetryプロジェクトと頻繁にやり取りしている場合、その組織のメンバーになることを検討しても良いでしょう。コミュニティリポジトリにある[完全なガイド](https://github.com/open-telemetry/community/blob/main/guides/contributor/membership.md#member)には、そのプロセスが詳しく説明されていますが、基本的な考え方は、実質的にすでにメンバーであることを示すことです。メンバーシップの申請は、GitHubでのイシュー作成と貢献（イシュー、プルリクエストなど）のリストを添付して提出されます。既存のメンバーが同意すれば、メンバーシップが承認され、組織内でより大きな役割を引き受けることが可能になります。貢献をするために必須ではありませんが、他のメンバーや訪問者に対して、OTelエコシステムに積極的に参加していることを示すことができます。
