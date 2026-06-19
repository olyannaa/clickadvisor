# ClickHouse vs Snowflakeによるリアルタイム分析 \- 比較と移行


title  

ClickHouse vs Snowflakeによるリアルタイム分析 \- 比較と移行


![clickhouse_vs_snowflake_simple.png](/uploads/clickhouse_vs_snowflake_simple_165592b77b.png)
## 要約 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E8%A6%81%E7%B4%84)


この「ClickHouse vs. Snowflake」ブログシリーズは2つのパートで構成されており、それぞれ独立して読むことができます。各パートは以下のとおりです。


- 比較と移行 \- 本記事では、ClickHouseとSnowflakeのアーキテクチャ上の類似点と相違点を概説し、ClickHouse Cloudがリアルタイム分析に特に適した機能をレビューします。SnowflakeからClickHouseへのワークロード移行に興味がある方のために、データセットの違いやデータ移行方法についても解説します。
- [ベンチマークとコスト分析](/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis) \- シリーズのもう一つの記事では、提案するアプリケーションを支える一連のリアルタイム分析用クエリを両システムでベンチマークし、さまざまな最適化を試した上でコストを直接比較しています。私たちの結果によると、ClickHouse Cloudはパフォーマンスとコストの両面でSnowflakeを上回りました。


	- 本番運用では、ClickHouse CloudはSnowflakeより3〜5倍コスト効率が高い
	- クエリ速度はSnowflakeと比較して2倍以上高速
	- データ圧縮率はSnowflakeより38%優れている



## 目次 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E7%9B%AE%E6%AC%A1)


- [はじめに](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#introduction)
- [ClickHouse vs Snowflake](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#clickhouse-vs-snowflake)
	- [類似点](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#similarities)
	- [相違点](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#differences)
	- [リアルタイム分析](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#real-time-analytics)
	- [クラスタリング vs ORDER BY](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#clustering-vs-ordering)
	- [データ移行](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#migrating-data)
		- [Snowflakeからのアンロード](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#unloading-from-snowflake)
		- [ClickHouseへのインポート](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#importing-to-clickhouse)
- [結論](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#conclusion)
- [付録](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#appendix)
	- [データ型](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#data-types)
	- [数値型](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#numerics)
	- [文字列](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#strings)
	- [セミ構造化](/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide#semi-structured)



## はじめに [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)


Snowflakeはオンプレミスのレガシーなデータウェアハウスのワークロードをクラウドに移行することを主目的としたクラウドデータウェアハウスです。大規模な長時間レポート処理に最適化されています。データをクラウドへ移行するにつれ、データオーナーはこのデータをどのように活用してさらに価値を引き出せるかを検討するようになります。たとえば、社内外で使うリアルタイムアプリケーションに活用するといったケースです。そこで、リアルタイム分析に最適化されたデータベースであるClickHouseの必要性に気づきます。


私たちはこの比較を公正に行うよう努めており、Snowflakeがデータウェアハウス用途で素晴らしい機能をいくつも備えていることも認めています。私たちはClickHouseの専門家ではありますが、Snowflakeに関しては必ずしも専門家ではありません。Snowflakeに詳しいユーザーからのフィードバックや改善の提案を歓迎しています。Snowflakeが他のユースケースにも利用可能であることは承知していますが、本記事の範囲はリアルタイム分析に絞られています。


## ClickHouse vs Snowflake [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#clickhouse-vs-snowflake)


### 類似点 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E9%A1%9E%E4%BC%BC%E7%82%B9)


Snowflakeはクラウドベースのデータウェアハウスプラットフォームで、大量データの格納・処理・分析をスケーラブルかつ効率的に行うためのソリューションを提供します。ClickHouse同様、Snowflakeは既存技術の上に構築されたものではなく、独自のSQLクエリエンジンとカスタムアーキテクチャを採用しています。


Snowflakeのアーキテクチャは、[共有ディスク](https://en.wikipedia.org/wiki/Shared-disk_architecture)（私たちは「共有ストレージ」という用語を好みます）と[共有ナッシング](https://en.wikipedia.org/wiki/Shared-nothing_architecture)アーキテクチャをハイブリッドに組み合わせたものと説明されます。つまり、オブジェクトストア（S3など）を使ってすべての計算ノードからアクセスできる（共有ディスク）一方、クエリに応じて各計算ノードがデータの一部をローカルに保持する（共有ナッシング）仕組みです。これは理論上、[両方の利点を兼ね備えている](https://www.geeksforgeeks.org/difference-between-shared-nothing-architecture-and-shared-disk-architecture/)とされます。共有ディスクアーキテクチャのシンプルさと、共有ナッシングアーキテクチャのスケーラビリティを兼ね備えているわけです。


この設計は、オブジェクトストレージを主要なストレージとして利用することを前提としており、ほぼ無限の同時アクセス性と高い耐久性、スケーラブルなスループットを実現しています。


![snowflake_architecture.png](/uploads/snowflake_architecture_e3c612c8e9.png)
*クレジット: [https://docs.snowflake.com/en/user\-guide/intro\-key\-concepts](https://docs.snowflake.com/en/user-guide/intro-key-concepts)*
一方、ClickHouseはオープンソースかつクラウドホスティングされた製品で、共有ディスクと共有ナッシングのどちらの構成にもデプロイすることができます。後者はセルフマネージド環境で一般的です。CPUやメモリのスケールアップは容易ですが、共有ナッシング構成ではクラスタ構成変更の際にデータのレプリケーションや管理にまつわる古典的な課題やオーバーヘッドが発生します。


このため、ClickHouse CloudではSnowflakeと同様のコンセプトを持つ共有ストレージアーキテクチャを採用しています。S3やGCSなどのオブジェクトストアに単一コピーのデータを格納し、ほぼ無制限のストレージ容量と強力な冗長性が得られます。すべてのノードはこの単一コピーのデータと各ノード固有のローカルSSDキャッシュにアクセスできます。ノード数やスペックを調整することでCPUやメモリをスケールさせます。Snowflakeと同様、S3のスケーラビリティ特性によって、ノードを追加してもディスクI/Oやネットワークがボトルネックになりにくく、並行アクセスが増えても性能が落ちにくいのが特長です。


![clickhouse_architecture.png](/uploads/clickhouse_architecture_53f247b7b1.png)
### 相違点 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E7%9B%B8%E9%81%95%E7%82%B9)


基盤となるストレージ形式やクエリエンジン以外にも、これらのアーキテクチャにはいくつか細かな違いがあります。


- Snowflakeの計算リソースは、[ウェアハウス](https://docs.snowflake.com/en/user-guide/warehouses)という概念を通じて提供されます。これは一定サイズのノード数で構成されます。Snowflakeはウェアハウスの具体的な構成を公開していませんが、一般的には[各ノードに8vCPU、16GiB、200GBのローカルストレージ（キャッシュ用）がある](https://select.dev/posts/snowflake-warehouse-sizing)と理解されています。ノード数はTシャツサイズ方式で決まり、たとえばX\-Smallは1ノード、Smallは2ノード、Mediumは4ノード、Largeは8ノードといった具合です。これらのウェアハウスはオブジェクトストア上にあるデータをどれでもクエリすることが可能です。クエリ負荷がかかっていないアイドル時はウェアハウスが停止し、クエリが来ると再開します。ストレージコストは常に請求されますが、ウェアハウスの料金はアクティブな時間だけ発生します。
- ClickHouse Cloudも同様に、ノードとそのローカルキャッシュストレージを使った仕組みを利用します。ただしTシャツサイズではなく、ユーザーは合計CPUとメモリを指定してサービスをデプロイし、それに応じて（あらかじめ定義した上限内で）クエリ負荷に合わせて自動的に垂直・水平方向にスケールします。ClickHouse Cloudのノードは現在、Snowflakeの1:2とは異なり1。現時点では、Snowflakeのウェアハウスほど厳密にデータと疎結合ではありませんが、将来的には疎結合の構成も可能です。ノードはアイドルになると自動的に停止し、クエリが来ると再開します。必要に応じて手動でリサイズもできます。
- ClickHouse Cloudのクエリキャッシュは各ノード固有であり、Snowflakeのようにサービスレイヤーで共有していません。それでも、ベンチマークではSnowflakeより高いパフォーマンスを示しました。
- SnowflakeとClickHouse Cloudはクエリ同時実行数を増やすために異なるアプローチを取っています。Snowflakeは[マルチクラスタウェアハウス](https://docs.snowflake.com/en/user-guide/warehouses-multicluster#benefits-of-multi-cluster-warehouses)という機能で並列化を図り、クエリ同時実行数を増やします（クエリレイテンシ自体は改善しません）。一方ClickHouseでは、垂直または水平スケールによってメモリやCPUを増やすことでこれを実現します。本記事では同時実行数よりもレイテンシに主眼を置いているため詳細は扱いませんが、Snowflakeが[ウェアハウスごとの同時実行数をデフォルトで8に制限](https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level)しているのに対し、ClickHouse Cloudは1ノードあたり1000クエリまで実行可能である点は注目に値します。
- Snowflakeはデータセットに対してコンピュートサイズを変更でき、ウェアハウスの再開も速い点があるため、アドホッククエリの体験は良好です。データウェアハウスやデータレイク用途では、これが他システムに対する優位性につながる場合があります。


追加の機能やデータ型における類似点・相違点については後述します。


### リアルタイム分析 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%83%AA%E3%82%A2%E3%83%AB%E3%82%BF%E3%82%A4%E3%83%A0%E5%88%86%E6%9E%90)


ベンチマークの結果から、ClickHouseは以下の観点でリアルタイム分析アプリケーションにおいてSnowflakeを上回っています。


- **クエリレイテンシ**: Snowflakeのクエリは、テーブルにクラスタリングを適用して最適化してもなお高めのレイテンシが生じます。テーブルをSnowflake側でクラスタリングキーに含め、ClickHouse側でPRIMARY KEYに含めた列でフィルタをかけた場合でも、Snowflakeでは同等のパフォーマンスを達成するのにClickHouseの2倍以上の計算リソースが必要でした。Snowflakeの[永続的なクエリキャッシュ](https://docs.snowflake.com/en/user-guide/querying-persisted-results)は一部のレイテンシ問題を緩和しますが、フィルタ条件が多様化すると効果が薄れます。また、キャッシュはデータが変更されると無効化されるため、新しいデータが取り込まれるようなユースケースではキャッシュの恩恵を受けにくい可能性があります。今回のベンチマークではそのケースを想定していませんが、実際の運用ではもっと新しいデータが継続的に追加されるでしょう。  

ClickHouseのクエリキャッシュはノード固有であり、[トランザクションレベルの一貫性](https://clickhouse.com/blog/introduction-to-the-clickhouse-query-cache-and-design)を保証しませんが、[リアルタイム分析には向いている](https://clickhouse.com/blog/introduction-to-the-clickhouse-query-cache-and-design)設計です。ユーザーはクエリごとに[クエリキャッシュの使用](https://clickhouse.com/docs/en/operations/settings/settings#use-query-cache)を制御でき、[サイズ](https://clickhouse.com/docs/en/operations/settings/settings#query-cache-max-size-in-bytes)やクエリのキャッシュ対象となる[実行回数・時間](https://clickhouse.com/docs/en/operations/settings/settings#enable-writes-to-query-cache)などの制限も設定できます。
- **コスト削減**: Snowflakeではクエリが一定時間走らないとウェアハウスが自動で休止し、課金がストップする仕組みがあります。ただし、このアイドルチェックは[60秒までしか下げられません](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse)。そして、クエリが届くと数秒以内にウェアハウスが再開します。リソースを使った分だけ課金されるので、アドホッククエリ主体のワークロードにはメリットがあります。  

しかし、多くのリアルタイム分析ワークロードでは継続的なデータ取り込みと頻繁なクエリ実行が必要となり、アイドルになるタイミングがほぼありません（例: 外部に公開されているダッシュボードなど）。結果としてウェアハウスは常にアクティブになり、Snowflakeのアイドル停止機能によるコストメリットが活かせません。一方、ClickHouse Cloudは1秒あたりのコスト単価がSnowflakeより低いため、常時稼働が求められるリアルタイム分析ワークロードでは最終的な料金が大幅に下がります。
- **機能に関する予測可能な価格設定**: マテリアライズドビューやクラスタリング（ClickHouseのORDER BYに相当）などは、リアルタイム分析で高いパフォーマンスを得るうえで不可欠な機能です。Snowflakeではこれらの機能が追加課金や高い料金プランを必要とし、さらにバックグラウンドでどれだけ処理が走るかは予測しづらいです。一方、ClickHouse Cloudではこれらの機能を使っても基本コストに追加料金はかかりません（挿入時のCPU・メモリ使用量が増える程度）。私たちのベンチマークでは、これらの違いやクエリの高速化、圧縮率の高さが合わさって、トータルコストをSnowflakeより大きく下げられることが分かりました。


さらにClickHouseには、リアルタイム分析機能を幅広くサポートする次のような特長があるという声もユーザーから寄せられています。


- [アグリゲートコンビネータ](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states)や[配列関数](https://clickhouse.com/docs/en/sql-reference/functions/array-functions/)などの特殊な分析関数が豊富で、複雑なクエリも短い構文で書け、パフォーマンスや可読性を向上できる
- Snowflakeほど厳しくないエイリアス制約など、分析向けに設計されたクエリ構文
- ENUMや精密指定可能な数値型など、より豊富なデータ型サポート。特にSnowflakeでは数値の精度指定があってもディスク消費には影響せず、ClickHouseでは型を厳密にすることで非圧縮時メモリを削減できる
- [ファイルやデータ形式](https://clickhouse.com/blog/data-formats-clickhouse-csv-tsv-parquet-native)の幅広いサポート（Snowflakeの[制限された形式](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)よりも多い）により、分析データのインポート・エクスポートが簡単
- S3やMySQL、PostgreSQL、MongoDB、Delta Lakeなど、さまざまなデータレイクやデータストアに対してアドホックでフェデレーテッドクエリを実行可能
- 列ごとに[カスタムスキーマやコーデック](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema)を指定することで高い圧縮率を実現可能。ベンチマークでもこの機能を活用して圧縮率を高めました
- セカンダリインデックスとプロジェクション機能をサポート。[セカンダリインデックス](https://clickhouse.com/docs/en/optimize/skipping-indexes)には[インバーテッドインデックス](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/invertedindexes#usage)も含まれ、テキスト検索にも対応。[プロジェクション](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#projections)はクエリごとに最適化を行うための仕組みです。プロジェクションはSnowflakeのマテリアライズドビューと似ていますが、[制限](https://docs.snowflake.com/en/user-guide/views-materialized#limitations-on-creating-materialized-views)が少なく、すべてのアグリゲート関数をサポートしています。プロジェクション自体でコストが増加することはなく（Snowflakeでは機能使用によって1\.5倍課金される場合がある）、ストレージ使用量増加分のみが影響します。ベンチマーク分析でこれらの機能が有効であることを示します。
- マテリアライズドビューもサポート。Snowflakeのマテリアライズドビュー（ClickHouseのプロジェクションに近い）とは異なり、ClickHouseのマテリアライズドビューはデータの挿入時にのみトリガーが実行されます。
	- 結果は別のテーブルに格納可能で、もとのデータを保持する必要はありません。要約したデータだけでいいなら、ストレージ削減と高いパフォーマンスを両立できます。
	- JOINやWHEREフィルタをサポートし、またマテリアライズドビューをチェーンさせることもできます。


### クラスタリング vs ORDER BY [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%AA%E3%83%B3%E3%82%B0-vs-order-by)


ClickHouseもSnowflakeもカラム指向データベースです。行指向に比べてCPUキャッシュやSIMD命令を効率的に活用でき、特定のカラムをソートしておくと圧縮率が上がります。どちらも最適な読み取りパフォーマンスにはソートやインデックスが重要で、実装の違いはあるものの、概念としては類似しています。


ClickHouseでは、スパースインデックスとソートされたデータを中心とした構造を採用しています。テーブル作成時に`ORDER BY`でカラムのタプルを指定し、ディスク上のソート順を決定します。一般的には[頻繁に使われるクエリのフィルタ列を、カーディナリティが低い順に並べる](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes)とよいとされています。また、`ORDER BY`を省略するとデフォルトでPRIMARY KEYが使われますが、`PRIMARY KEY`と`ORDER BY`を両方指定することも可能です（`PRIMARY KEY`は`ORDER BY`の先頭と一致している必要があります）。スパースインデックスはディスク上がソートされていることを前提として動くため、効率的にデータをスキップできます。


Snowflakeは[マイクロパーティション](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)と呼ばれる独自構造を使いつつ、[クラスタリング](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)という機能で似たコンセプトを提供しています。クラスタリングキーに指定されたカラムをもとにマイクロパーティションが割り振られ、同じ値を持つデータが近接配置されるようになります。これはClickHouseの`ORDER BY`と同様、ディスク上のデータが並ぶ順序を制御し、クエリや圧縮において同様の利点を得ることができます。


ただし、実装上はいくつかの違いがあります。


- ClickHouseは、データ挿入時に`ORDER BY`に従って自動的にソートとインデックス構築を行います。これによる追加コストはほぼなく、高速に更新が必要なテーブルでも適切に最適化されます。
- Snowflakeはバックグラウンドでの[自動クラスタリング](https://docs.snowflake.com/en/user-guide/tables-auto-reclustering)によってデータを再配置し、クレジットが消費されます。これにかかる料金を事前に予測するのは難しく、多数の行があるテーブルでこそ威力を発揮する一方で[頻繁に更新されるテーブルには推奨していない](https://docs.snowflake.com/en/user-guide/tables-clustering-keys#benefits-of-defining-clustering-keys-for-very-large-tables)です。カラムのカーディナリティによってコストが大きく左右され、Snowflakeでは`to_date`などの式を使ってカーディナリティを下げることを推奨しています。さらに、クラスタリングによる恩恵が得られるまでには時間がかかり、すぐに最適化されるわけではありません。
- Snowflakeはマイクロパーティション方式なので、高コストではあるものの[再クラスタリング](https://docs.snowflake.com/en/user-guide/tables-clustering-keys#credit-and-storage-impact-of-reclustering)が可能です。一方ClickHouseでは、テーブルを完全に再書き込みしなければ再ソートできません。


両システムとも、分析処理では一般的に`GROUP BY`やソート、フィルタリングで特定のカラムをよく使用するため、こうしたソート/クラスタリングの設定は重要になります。クラスタリング/ORDER BYに指定するカラムはできるだけ多くのクエリで恩恵を受けられるよう選択し、カラムの並び順にも気を配る必要があります。


カラム選択の推奨事項は両システムでほぼ共通しています。


- 選択的なフィルタで頻繁に使うカラムを採用する。`GROUP BY`に使われるカラムもメモリ効率で役立つ
- カーディナリティが十分に高いカラムを使う（コイントスのように50%の行しか絞れないものは避ける）
- 複数カラムが必要な場合は、カーディナリティが低いカラムから高いカラムの順に並べる。特にClickHouseでは[この点が非常に重要](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-cardinality/)ですが、Snowflakeも考え方は同じと思われます。


*注: 上記の推奨事項は似ていますが、Snowflakeは[高カーディナリティカラムをクラスタリングキーに指定するのを推奨していません](https://docs.snowflake.com/en/user-guide/tables-clustering-keys#strategies-for-selecting-clustering-keys)。これはClickHouseには当てはまりません。タイムスタンプなどカーディナリティが高い列はClickHouseでもORDER BYの候補になります。*


このガイドラインを踏まえた上で、私たちのベンチマークを行いました。


### データ移行 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%83%87%E3%83%BC%E3%82%BF%E7%A7%BB%E8%A1%8C)


SnowflakeからClickHouseにデータを移行する場合、S3などのオブジェクトストアを中継ストレージとして利用することができます。SnowflakeとClickHouseの`COPY INTO`や`INSERT INTO SELECT`コマンドを組み合わせ、次のような流れで転送します。


![migrating_clickhouse_snowflake.png](/uploads/migrating_clickhouse_snowflake_93a30b945c.png)
#### Snowflakeからのアンロード [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#snowflake%E3%81%8B%E3%82%89%E3%81%AE%E3%82%A2%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)


Snowflakeからのエクスポートには、図のように[External Stage](https://docs.snowflake.com/en/sql-reference/sql/create-stage)を使います。これは[ClickHouseのS3テーブルエンジン](https://clickhouse.com/docs/en/engines/table-engines/integrations/s3)と似ており、外部にホストされたファイルのまとまりをSQLで参照できるようにします。


SnowflakeとClickHouse間のデータ移行には、型情報を維持し、圧縮効率も良く、ネスト構造を扱えるParquet形式を推奨します。[JSONの`ndjson`形式](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#required-parameters)を使う方法もありますが、こちらは可読性を除けばデータ量が増加する傾向があります。



> 以下の例では65億行のPyPiデータセットをエクスポートしています。このスキーマとデータセットは、[publicなBigQueryテーブル](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=pypi&page=dataset)から取得したもので、[こちら](https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/)のとおりPiPなどのツールを使ったPythonパッケージのダウンロード履歴を記録しています。詳細は[ベンチマーク記事](/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis)で紹介していますが、550億行以上の大きなデータセットであり、リアルタイム分析における一般的なデータ構造に近いものとして選びました。


下記の例では、SnowflakeでParquetの[名前付きファイル形式](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)を作成し、次にエクスポート先のS3を表すExternal Stageを宣言してから、`COPY INTO`コマンドでエクスポートします。このステージはS3バケットへの抽象化レイヤーで、権限付与も行いやすくなります。


SnowflakeではS3への書き込み権限を付与する方法が[複数](https://docs.snowflake.com/en/user-guide/data-load-s3-config)あります。サンプルを簡単にするため今回はキーとシークレットを直接使っていますが、本番環境では[Snowflake Storage Integration](https://docs.snowflake.com/en/user-guide/data-load-s3-config-aws-iam-user)を使うことを推奨します。



```
CREATE FILE FORMAT my_parquet_format TYPE = parquet;

CREATE OR REPLACE STAGE my_ext_unload_stage 
URL='s3://datasets-documentation/pypi/sample/'
CREDENTIALS=(AWS_KEY_ID='<key>' AWS_SECRET_KEY='<secret>')
FILE_FORMAT = my_parquet_format;

-- 全ファイルに「pypi」プレフィックスを適用し、最大ファイルサイズを150MBに指定
COPY INTO @my_ext_unload_stage/pypi from pypi max_file_size=157286400 header=true;

```

Snowflake側のスキーマは以下です。



```
CREATE TABLE PYPI (
   timestamp TIMESTAMP,
   country_code varchar,
   url varchar,
   project varchar,
   file OBJECT,
   installer OBJECT,
   python varchar,
   implementation OBJECT,
   distro VARIANT,
   system OBJECT,
   cpu varchar,
   openssl_version varchar,
   setuptools_version varchar,
   rustc_version varchar,
   tls_protocol varchar,
   tls_cipher varchar
) DATA_RETENTION_TIME_IN_DAYS = 0;

```

Parquetにエクスポートするとサイズは約5\.5TiB、1ファイル150MB上限で分割されます。AWS us\-east\-1にある2X\-LARGEサイズのウェアハウスで処理時間は30分程度です。`header=true`を指定しているのはカラム名を出力するためです。VARIANTやOBJECTカラムは[デフォルトでJSON文字列](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location#usage-notes)として出力されるので、ClickHouseにインサートする際にキャストが必要になります。


#### ClickHouseへのインポート [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#clickhouse%E3%81%B8%E3%81%AE%E3%82%A4%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%88)


一度オブジェクトストアに書き出してしまえば、ClickHouseの[s3テーブル関数](https://clickhouse.com/docs/en/sql-reference/table-functions/s3)などを使ってテーブルへ取り込めます。以下の例のように実行します。


以下のようなターゲットスキーマを想定します。



```
CREATE TABLE default.pypi
(
	`timestamp` DateTime64(6),
	`date` Date MATERIALIZED timestamp,
	`country_code` LowCardinality(String),
	`url` String,
	`project` String,
	`file` Tuple(filename String, project String, version String, type Enum8('bdist_wheel' = 0, 'sdist' = 1, 'bdist_egg' = 2, 'bdist_wininst' = 3, 'bdist_dumb' = 4, 'bdist_msi' = 5, 'bdist_rpm' = 6, 'bdist_dmg' = 7)),
	`installer` Tuple(name LowCardinality(String), version LowCardinality(String)),
	`python` LowCardinality(String),
	`implementation` Tuple(name LowCardinality(String), version LowCardinality(String)),
	`distro` Tuple(name LowCardinality(String), version LowCardinality(String), id LowCardinality(String), libc Tuple(lib Enum8('' = 0, 'glibc' = 1, 'libc' = 2), version LowCardinality(String))),
	`system` Tuple(name LowCardinality(String), release String),
	`cpu` LowCardinality(String),
	`openssl_version` LowCardinality(String),
	`setuptools_version` LowCardinality(String),
	`rustc_version` LowCardinality(String),
	`tls_protocol` Enum8('TLSv1.2' = 0, 'TLSv1.3' = 1),
	`tls_cipher` Enum8('ECDHE-RSA-AES128-GCM-SHA256' = 0, 'ECDHE-RSA-CHACHA20-POLY1305' = 1, 'ECDHE-RSA-AES128-SHA256' = 2, 'TLS_AES_256_GCM_SHA384' = 3, 'AES128-GCM-SHA256' = 4, 'TLS_AES_128_GCM_SHA256' = 5, 'ECDHE-RSA-AES256-GCM-SHA384' = 6, 'AES128-SHA' = 7, 'ECDHE-RSA-AES128-SHA' = 8)
)
ENGINE = MergeTree
ORDER BY (date, timestamp)

```

Snowflake側でOBJECTやVARIANTだった構造化データはJSON文字列として出力されるため、[JSONExtract関数](https://clickhouse.com/docs/en/sql-reference/functions/json-functions#jsonextractjson-indices_or_keys-return_type)を使ってインサート時にタプルへ変換します。



```
INSERT INTO pypi
SELECT
	TIMESTAMP,
	COUNTRY_CODE,
	URL,
	PROJECT,
	JSONExtract(ifNull(FILE, '{}'), 'Tuple(filename String, project String, version String, type Enum8(\'bdist_wheel\' = 0, \'sdist\' = 1, \'bdist_egg\' = 2, \'bdist_wininst\' = 3, \'bdist_dumb\' = 4, \'bdist_msi\' = 5, \'bdist_rpm\' = 6, \'bdist_dmg\' = 7))') AS file,
	JSONExtract(ifNull(INSTALLER, '{}'), 'Tuple(name LowCardinality(String), version LowCardinality(String))') AS installer,
	PYTHON,
	JSONExtract(ifNull(IMPLEMENTATION, '{}'), 'Tuple(name LowCardinality(String), version LowCardinality(String))') AS implementation,
	JSONExtract(ifNull(DISTRO, '{}'), 'Tuple(name LowCardinality(String), version LowCardinality(String), id LowCardinality(String), libc Tuple(lib Enum8(\'\' = 0, \'glibc\' = 1, \'libc\' = 2), version LowCardinality(String)))') AS distro,
	JSONExtract(ifNull(SYSTEM, '{}'), 'Tuple(name LowCardinality(String), release String)') AS system,
	CPU,
	OPENSSL_VERSION,
	SETUPTOOLS_VERSION,
	RUSTC_VERSION,
	TLS_PROTOCOL,
	TLS_CIPHER
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/pypi/2023/pypi*.parquet')
SETTINGS input_format_null_as_default = 1, input_format_parquet_case_insensitive_column_matching = 1

```

ここでは、[`input_format_null_as_default=1`](https://clickhouse.com/docs/en/operations/settings/formats#input_format_null_as_default)と[`input_format_parquet_case_insensitive_column_matching=1`](https://clickhouse.com/docs/en/operations/settings/formats#input_format_parquet_case_insensitive_column_matching)を有効にし、null値をデフォルトに変換し、列名の大小文字を区別しないようにしています。


[Azure](https://docs.snowflake.com/en/user-guide/data-unload-azure)や[Google Cloud](https://docs.snowflake.com/en/user-guide/data-unload-gcs)を使う場合も同様に処理できます。ClickHouseにはそれぞれの[専用テーブル関数](https://clickhouse.com/docs/en/sql-reference/table-functions/azureBlobStorage)などが用意されています。


## 結論 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E7%B5%90%E8%AB%96)


本記事では、リアルタイム分析をユースケースとした場合にSnowflakeとClickHouseがどのように比較されるかを、両システムの類似点や相違点とともに見てきました。リアルタイム分析で有用なClickHouseの機能を挙げ、Snowflakeからワークロードを移行する際の考慮点も解説しました。[次の記事](/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis)では、サンプルのリアルタイム分析アプリケーションを構築し、圧縮や挿入パフォーマンスの違い、代表的なクエリのベンチマークを行います。その結果をコスト分析とともに紹介し、ClickHouse Cloud導入時のコスト削減可能性を示します。




---


## 付録 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E4%BB%98%E9%8C%B2)


SnowflakeからClickHouseへリアルタイム分析ワークロードを移行する際に知っておくべき主要な概念を、以下にまとめます。データ型の違いやクラスタリングとORDER BYの相違を補足的に解説します。


### データ型 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B)


#### 数値型 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E6%95%B0%E5%80%A4%E5%9E%8B)


SnowflakeとClickHouseを比較すると、SnowflakeよりClickHouseのほうが数値型の精度指定が細かいことに気づくでしょう。Snowflakeは数値型に`Number`を使っており、精度（桁数）とスケール（小数点以下の桁数）を指定します（最大38桁）。整数は`Number`の精度とスケールを0にしたものと同じです。Snowflakeではマイクロパーティションレベルで最小限のバイトで格納するため、ユーザーが指定する精度やスケールは実際のディスク使用量に大きく影響しません。圧縮で相殺される部分もあります。一方、`Float64`型を使用すると、精度を一部失う代わりにさらに広い範囲の値を扱えます。


ClickHouseは、符号付き・符号なしの複数のビット幅を持つ整数型と浮動小数点型を提供し、明示的に精度を指定してメモリ消費を抑えることができます。`Decimal`型はSnowflakeの`Number`と同等ですが、最大76桁までサポートするためSnowflakeの倍の精度があります。浮動小数点は`Float32`と`Float64`の2種類があり、精度が必要ない場合は`Float32`で圧縮とメモリを節約できます。


#### 文字列 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E6%96%87%E5%AD%97%E5%88%97)


ClickHouseとSnowflakeでは文字列型の扱い方に違いがあります。SnowflakeのVARCHARはUTF\-8でエンコードされたUnicode文字列を保持し、最大長を指定しても実際の使用バイト数だけが格納されます。その他のTEXTやNCharなどの型はVARCHARのエイリアスです。  

ClickHouseは[生バイト列](https://clickhouse.com/docs/en/sql-reference/data-types/string)として文字列を保持し、エンコーディングはユーザー側が管理します。クエリ時にエンコーディングを扱うための[関数](https://clickhouse.com/docs/en/sql-reference/functions/string-functions#lengthutf8)が用意されています（[こちら](https://utf8everywhere.org/#cookie)の考え方も参照）。実装的には、ClickHouseのString型はSnowflakeのBinary型に近いと言えます。  

また、[照合順序（コレーション）](https://docs.snowflake.com/en/sql-reference/collation)はSnowflakeと[ClickHouse](https://clickhouse.com/docs/en/sql-reference/statements/select/order-by#collation-support)の双方がサポートしています。


#### セミ構造化 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-comparison-migration-guide-jp#%E3%82%BB%E3%83%9F%E6%A7%8B%E9%80%A0%E5%8C%96)


SnowflakeとClickHouseはどちらもセミ構造化データのために豊富な型サポートを提供しています。Snowflakeは[VARIANT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured)を中心に[ARRAYやOBJECT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured)を定義し、ClickHouseは[JSON型](https://clickhouse.com/docs/en/sql-reference/data-types/json)や[Tuple、Nested型](https://clickhouse.com/docs/en/sql-reference/data-types/nested-data-structures/nested)で実現します。SnowflakeのARRAYやOBJECTもVARIANTの制約付きにすぎず、内部型を厳密に指定できないのが特徴です。


一方、ClickHouseはNamed TupleやNested型によって、階層化された構造を明示的に定義できます。サブカラムごとに型を厳密に指定し、そこに圧縮やコーデックを適用できます。Snowflakeでは内部まで型を細かく指定できないため、[最適な圧縮を得るために構造をフラット化する](https://docs.snowflake.com/en/user-guide/semistructured-considerations#storing-semi-structured-data-in-a-variant-column-vs-flattening-the-nested-structure)ことを推奨しています。また、Snowflakeにはセミ構造化データに[サイズ制限](https://docs.snowflake.com/en/user-guide/semistructured-considerations#data-size-limitations)があります。


以下の表は、SnowflakeとClickHouseの型対応をまとめたものです。




| **Snowflake** | **ClickHouse** | **備考** |
| --- | --- | --- |
| [NUMBER](https://docs.snowflake.com/en/sql-reference/data-types-numeric) | [Decimal](https://clickhouse.com/docs/en/sql-reference/data-types/decimal) | ClickHouseではSnowflakeの倍となる76桁までの精度とスケールをサポート |
| [FLOAT, FLOAT4, FLOAT8](https://docs.snowflake.com/en/sql-reference/data-types-numeric#data-types-for-floating-point-numbers) | [Float32, Float64](https://clickhouse.com/docs/en/sql-reference/data-types/float) | Snowflakeでは浮動小数点は常に64ビット |
| [VARCHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar) | [String](https://clickhouse.com/docs/en/sql-reference/data-types/string) |  |
| [BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary) | [String](https://clickhouse.com/docs/en/sql-reference/data-types/string) |  |
| [BOOLEAN](https://docs.snowflake.com/en/sql-reference/data-types-logical) | [Bool](https://clickhouse.com/docs/en/sql-reference/data-types/boolean) |  |
| [DATE](https://docs.snowflake.com/en/sql-reference/data-types-datetime#date) | [Date](https://clickhouse.com/docs/en/sql-reference/data-types/date), [Date32](https://clickhouse.com/docs/en/sql-reference/data-types/date32) | SnowflakeのDATEはClickHouseのDateより広い範囲をカバー。ClickHouseのDateは2バイトでコンパクト |
| [TIME(N)](https://docs.snowflake.com/en/sql-reference/data-types-datetime#time) | 直接の対応はないが、[DateTime](https://clickhouse.com/docs/en/sql-reference/data-types/datetime)や[DateTime64(N)](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64)で表現可能 | DateTime64は同様に小数点以下の精度を扱える |
| [TIMESTAMP](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp) \- [TIMESTAMP\_LTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz), [TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz), [TIMESTAMP\_TZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) | [DateTime](https://clickhouse.com/docs/en/sql-reference/data-types/datetime) と [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) | DateTimeおよびDateTime64では列ごとにTZパラメータを設定可能。設定がない場合はサーバーのタイムゾーンが使われる。クライアント側で`--use_client_time_zone`を使うこともできる |
| [VARIANT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#variant) | [JSON, Tuple, Nested](https://clickhouse.com/docs/en/integrations/data-formats/json) | ClickHouseのJSON型はまだ実験的機能。挿入時に型を推論する。Tuple, Nested, Arrayを使って明示的に型を定義する方法もある |
| [OBJECT](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#object) | [Tuple, Map, JSON](https://clickhouse.com/docs/en/integrations/data-formats/json) | OBJECTとMapはどちらもキーがStringの構造。Snowflakeでは値もVARIANTで、キーごとに型が異なる可能性がある。ClickHouseでは値の型を厳密にする必要があるため、混在型を扱うにはJSON型やTupleで明示的に定義する |
| [ARRAY](https://docs.snowflake.com/en/sql-reference/data-types-semistructured#array) | [Array](https://clickhouse.com/docs/en/sql-reference/data-types/array), [Nested](https://clickhouse.com/docs/en/sql-reference/data-types/nested-data-structures/nested) | SnowflakeのARRAYはVARIANTのサブタイプ。一方ClickHouseのArrayは要素が強く型付けされる |
| [GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#geography-data-type) | [Point, Ring, Polygon, MultiPolygon](https://clickhouse.com/docs/en/sql-reference/data-types/geo) | Snowflakeは座標系(WGS 84\)を固定的に適用。ClickHouseはクエリ時に指定する |
| [GEOMETRY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#geometry-data-type) | [Point, Ring, Polygon, MultiPolygon](https://clickhouse.com/docs/en/sql-reference/data-types/geo) |  |


このほかClickHouseには以下のような型もあります。


- [ipv4](https://clickhouse.com/docs/en/sql-reference/data-types/ipv4)と[ipv6](https://clickhouse.com/docs/en/sql-reference/data-types/ipv6)などのIP専用型（Snowflakeより効率的に格納できる場合がある）
- [FixedString](https://clickhouse.com/docs/en/sql-reference/data-types/fixedstring) \- ハッシュなど固定長のバイト列を扱うのに便利
- [LowCardinality](https://clickhouse.com/docs/en/sql-reference/data-types/lowcardinality) \- どんな型でも辞書エンコードをかけられる。カーディナリティが10万未満のときに有効
- [Enum](https://clickhouse.com/docs/en/sql-reference/data-types/enum) \- 小さな整数値で名前付き定数を格納できる
- [UUID](https://clickhouse.com/docs/en/sql-reference/data-types/uuid) \- UUIDを効率的に格納
- [ベクトル](https://clickhouse.com/blog/vector-search-clickhouse-p2)は`Array(Float32)`などで表現可能で、距離関数にも対応


さらに、ClickHouseでは[アグリゲート関数の中間状態](https://clickhouse.com/docs/en/sql-reference/data-types/aggregatefunction)を格納できるというユニークな機能があります。これは実装依存の形式ですが、マテリアライズドビューなどと組み合わせることで、挿入時の集計結果の状態を保持し、後から[マージ関数](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-state)を適用して素早く集計結果を取得できます（詳しくは[こちら](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states#working-with-aggregation-states)）。


[お問い合わせ](https://clickhouse.com/company/contact?loc=snowflake-blog-comparing-and-migrating&utm_source=clickhouse&utm_medium=blog&utm_campaign=snowflake)いただければ、ClickHouse Cloudを用いたリアルタイム分析の詳細をご案内します。あるいは[こちら](https://clickhouse.cloud/signUp?loc=snowflake-blog-comparing-and-migrating-footer&utm_source=clickhouse&utm_medium=blog&utm_campaign=snowflake)からClickHouse Cloudを始めると、300ドル分のクレジットが付与されます。
