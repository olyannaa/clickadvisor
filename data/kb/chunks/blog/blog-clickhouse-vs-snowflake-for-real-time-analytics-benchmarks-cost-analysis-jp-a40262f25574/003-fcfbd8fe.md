---
source: blog
url: "https://github.com/ClickHouse/clickhouse_vs_snowflake>\u3067\u4E00\u822C\u516C\
  \u958B\u3055\u308C\u3066\u3044\u307E\u3059\u3002"
topic: clickhouse-vs-snowflake
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 9
---

| 8 | 120 | 30 | 240 | 960 | 8 | 5391 | | ClickHouse | 960GB | 8 | 120 | 30 | 240 | 960 | 16 | 6133 | 2X\-LARGE（256 vCPU相当）と960GB（240 vCPU相当）の中で最良の結果を比べると、**同じようなvCPU数でもClickHouseはSnowflakeより2倍以上のスピードでロードが完了**します。 さらに以下のような補足があります。

- ノードあたりのCPU数が多い構成（708GBなど）だと、最初の挿入時間自体は短くなりますが、その後マージに時間がかかります。対してノード数を増やした構成（960GBなど）なら同時に走るマージも増やせるので、結果的に全体の完了が早くなります。
- Snowflakeでロード性能を最大化するには、vCPU数と同じ数のファイルが必要になると推測されます。Parquetファイルの1つを複数スレッドで並行読み込みできない（[ClickHouseは対応済み](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups#parallelized-reads)）ためです。今回のデータセットは150MiBのファイルを7万個程度用意したため、この点は問題ありませんでした。
- SnowflakeはParquetファイルを150MiB程度にそろえることを推奨しています。PyPI全体のフルデータ（19TiB）は小さいファイル（平均13MiB）が150万個あるため、そのままSnowflakeにロードするとさらに性能が低下すると予想されます。
- SnowflakeはvCPU数を増やすとロード時間が直線的に減るため、総コスト（時間×時給）はある程度一定になりがちです。大きなウェアハウスでロードを一気に終わらせて、終了後にウェアハウスを停止してしまう運用がしやすいわけです。ClickHouse Cloudでも[SharedMergeTree](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates)を使えば同様にリニアに挿入性能をスケールできます。今回の結果は標準のMergeTreeで行ったベンチマークですが、SharedMergeTreeを使う場合の挿入性能の伸びについては[こちら](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/insert_performance/shared_merge_tree)で紹介しています。
- 上記の表にはSnowflakeのクラスタリングに要する時間は含まれていません。クラスタリングはSnowflakeのクエリ性能に必須ですが、非同期で実行されスケジューリングが非決定的のため、正確な計測は難しいです。これらを含めると、Snowflakeの方がさらにロード時間がかかります。

このテストから得られる追加の知見については、[こちら](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/insert_performance)をご覧ください。

#### ストレージ効率と圧縮 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis-jp#%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8%E5%8A%B9%E7%8E%87%E3%81%A8%E5%9C%A7%E7%B8%AE)

ClickHouseでは、先ほどのスキーマでほぼ最大限の圧縮を狙っています。下記に示す通り、`date`と`timestamp`にdeltaコーデックを適用するとさらにサイズを削減できますが、コールドクエリの性能に影響が出る場合がありました。

Snowflakeはクラスタリングなしではデフォルト設定なので圧縮率は劣ります。クラスタリングキーの設定次第で圧縮が大きく変わるため、さまざまなクラスタリングキーで圧縮後サイズを計測し、結果を下図にまとめました。

詳細は[こちら](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/compression)で確認できます。

| Database | ORDER BY/CLUSTER BY | Total size (TiB) | Compression ratio on Parquet |
| --- | --- | --- | --- |
| Snowflake | \- | 1\.99 | 4\.39 |
| Snowflake | (to\_date(timestamp), project) | 1\.33 | 6\.57 |
| Snowflake | (project) | 1\.52 | 5\.75 |
| Snowflake | (project, to\_date(timestamp)) | 1\.77 | 4\.94 |
| Snowflake | (project, timestamp)\* | 1\.05 | 8\.32 |
| ClickHouse | (project, date, timestamp) | 0\.902 | 9\.67 |
| ClickHouse | (project, date, timestamp) \+ delta codec | 0\.87 | 10\.05 |





| Most optional query performance |
| --- |
| Most optimal compression |




> Snowflakeの非圧縮サイズは確認できなかったため、ClickHouse同様の圧縮率を算出できませんでした。その代わり、元のParquet比としての圧縮率を掲載しています。

Snowflakeにクラスタリングを適用すると、今回のユースケースで最大40%程度のデータサイズ削減を得られました。一方、ClickHouseは追加で`date`カラムがあってもSnowflakeよりも高圧縮を実現しており、**Snowflakeの最良ケース(1\.05TiB)より20%近く小さいサイズ(0\.87TiB)になっています**。

ただしSnowflakeで最も圧縮効率が高かったクラスタリングキーは、クエリ性能面では最適ではありません。Snowflakeユーザーは「圧縮率を取るかクエリ性能を取るか」のトレードオフに直面します。

本ベンチマークの目的はリアルタイム分析で高速にクエリを返すことなので、Snowflake側はクエリ速度を最優先するクラスタリングキー（`(to_date(timestamp), project)`）を使う設定にしています。

**実際のクエリ速度重視構成で比較すると、ClickHouse CloudはSnowflakeより38%圧縮に優れた結果（0\.902TiB vs 1\.33TiB）となりました。**

#### Snowflakeにおけるクラスタリングの時間とコスト [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis-jp#snowflake%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%AA%E3%83%B3%E3%82%B0%E3%81%AE%E6%99%82%E9%96%93%E3%81%A8%E3%82%B3%E3%82%B9%E3%83%88)

[Snowflake公式ドキュメント](https://docs.snowflake.com/en/user-guide/tables-auto-reclustering#credit-usage-and-warehouses-for-automatic-clustering)によると、クラスタリングにはクレジットを消費する非同期処理が発生します。特にリアルタイム分析で注文の多いケースでは、データを効果的に並べるための背景処理が走り、利用料金に上乗せされます。私たちの検証では、上記の各クラスタリングキーでクラスタリング処理が安定するまでを計測し、消費クレジットをまとめました（Snowflakeが提供する[AUTOMATIC\_CLUSTERING\_HISTORYビュー](https://docs.snowflake.com/en/user-guide/tables-auto-reclustering#viewing-automatic-clustering-cost)から1時間単位での集計しか取れないため、あくまで概算です）。

| CLUSTER BY | Time taken (mins) | Rows clustered | Bytes clustered | Credits used | Total cost (assuming standard) |
| --- | --- | --- | --- | --- | --- |
| (to\_date(timestamp), project) | 540 | 53818118911 | 1893068905149 | 450 | $990 |
| (project) | 360 | 41243645440 | 1652448880719 | 283 | $566 |
| (project, to\_date(timestamp)) | 180 | 56579552438 | 1315724687124 | 243 | $486 |
| (project, timestamp) | 120 | 50957022860 | 1169499869415 | 149 | $298 |



上の結果を、先ほどの挿入性能比較に加味すると、Snowflakeの効率的なクラスタリングはクエリ性能向上に欠かせないものの、クレジット消費や処理時間が大きいことが分かります。

一方、ClickHouseでは（ORDER BYを設定するのが当たり前のため）追加の課金は発生しません。背景で実行されるマージ処理やソート処理は既存のリソースで行われ、ユーザーが追加でコストを意識する必要はありません。プロジェクションなどにより追加のORDER BYを設定した場合も、ストレージコストがわずかに増えるだけです。Snowflakeのクラスタリングのように別途クレジット消費が積み上がることはありません。

#### クエリ [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis-jp#%E3%82%AF%E3%82%A8%E3%83%AA)

提案アプリケーションが投げると想定される各種クエリをシミュレートし、その性能を比較しました。結果をざっくりまとめますが、詳細や実行ログは各リンク先で公開しています。前提条件は以下の通りです。

- Snowflakeではクラスタリングが完了している状態、ClickHouseではパーツ数が3000以下に落ち着いた状態をテスト。
- すべてのクエリは3回ずつ実行し、コールド（最初の実行）、ホット（最速の実行）を含めて計測。
- ClickHouseはクエリ前に `SYSTEM DROP FILESYSTEM CACHE ON CLUSTER 'default'` を実行してファイルシステムキャッシュをクリア。Snowflakeは同等のコマンドがないため、ウェアハウスを一旦停止→再開でキャッシュをクリアしたとみなす。
- ClickHouseとSnowflakeのクエリキャッシュは無効化（ClickHouse Cloudはデフォルトで無効、Snowflakeは `ALTER USER <user> SET USE_CACHED_RESULT = false;`）。
- 「直近90日」などの日付条件は常に同じ絶対日時を指定し、クエリ結果を再利用しても同じにならないようにしています（キャッシュヒットを排除するため）。

#### クエリ 1：1日あたりのダウンロード数 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis-jp#%E3%82%AF%E3%82%A8%E3%83%AA-11%E6%97%A5%E3%81%82%E3%81%9F%E3%82%8A%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E6%95%B0)

「直近90日間のダウンロード数を日次集計」で折れ線グラフを描画するようなクエリです。人気上位100のプロジェクトについて、以下の集計を行い、続けてランダムな日付範囲にフィルタをかけて再クエリする（ユーザーがドリルダウンした想定）。計200クエリになります。

```
SELECT
    toStartOfDay(date),
    count() AS count
FROM pypi
WHERE (project = 'typing-extensions') AND (date >= (CAST('2023-06-23', 'Date') - toIntervalDay(90)))
GROUP BY date
ORDER BY date ASC

```

詳しい結果は[こちら](https://github.com/ClickHouse/clickhouse_vs_snowflake/tree/main/downloads_per_day)にあります。

*Hot only*

![download_per_day.png](/uploads/download_per_day_a717039d01.png)
まとめると以下の通りです。

- Snowflakeでは、クラスタリングなしだとリアルタイム分析に耐えない7秒以上の応答時間になってしまいます。
- リソースが近しい構成で比べると、ClickHouseはSnowflakeの少なくとも3倍高速（平均値）で、95・99パーセンタイルでも2倍高速。
- ClickHouseの177 vCPU構成でも、Snowflakeの4X\-LARGE（約1024 vCPU）より速いです。本ワークロードではSnowflakeが推奨する追加の並列化があまり効果を発揮しないと推測できます。

#### クエリ 2：Python バージョン別の1日あたりのダウンロード数 [\#](/jp/blog/clickhouse-vs-snowflake-for-real-time-analytics-benchmarks-cost-analysis-jp#%E3%82%AF%E3%82%A8%E3%83%AA-2python-%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E5%88%A5%E3%81%AE1%E6%97%A5%E3%81%82%E3%81%9F%E3%82%8A%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E6%95%B0)

こちらは「Pythonバージョンごとのダウンロード数推移」をグラフにするクエリです。直近90日間、日次で集計してバージョン別にGROUP BYし、さらにプロジェクトでWHEREフィルタをかけます。その後、ランダムな日付レンジで再度クエリしてドリルダウンします。人気上位100プロジェクトで計200クエリです。Pythonバージョン列は低カーディナリティですが、ORDER BY・クラスタリングキーには含まれていません。
