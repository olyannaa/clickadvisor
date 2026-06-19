# PostgresからClickHouseへ: データモデリングのヒント


先月、当社は[PeerDBを買収しました](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database)。PeerDBはPostgresのCDCを専門とする企業で、[PeerDB](https://www.peerdb.io/)を使うと、[Postgres](https://www.postgresql.org/)から[ClickHouse](https://clickhouse.com/)へのデータレプリケーションが高速かつ簡単に行えます。PeerDBのユーザーからよくある質問として、「データをどのようにClickHouseにモデル化するとClickHouseの利点を最大限活かせるか」というものがあります。


この質問が出る理由は、ClickHouseとPostgresのデータモデルが異なるからです。それぞれ最適化された目的別データベースであり、Postgresはトランザクション(OLTP)向け、ClickHouseは分析(OLAP)向けのカラムナデータベースだからです。本ガイドでは、Postgresの世界から来たユーザー向けに、ClickHouseのデータモデリングの基本を解説します。なお、これはブログシリーズの第1弾で、今後も続編を予定しています。


## ReplacingMergeTree tableエンジン [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#replacingmergetree-table%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%B3)


PeerDBは、PostgreSQLのテーブルを[ReplacingMergeTree](https://clickhouse.com/docs/ja/engines/table-engines/mergetree-family/replacingmergetree)エンジンでClickHouseにマッピングします。ClickHouseは追記型のワークロードで最も高いパフォーマンスを発揮し、[頻繁なUPDATEは推奨されません](https://clickhouse.com/docs/ja/guides/developer/mutations)。ここで特に強力なのがReplacingMergeTreeです。


`ReplacingMergeTree`は、データの取り込みと変更の両方が行われるワークロードをサポートします。テーブルは追記専用で、ユーザーによるUPDATEはバージョン付きのINSERTとして取り込まれます。ReplacingMergeTreeエンジンはバックグラウンドで行をマージしながら重複排除を行うため、ClickHouseはリアルタイムの取り込みで非常に高いパフォーマンスを発揮します。


PeerDBでは、PostgresからのINSERTとUPDATEがClickHouse側では異なるバージョン（`_peerdb_version`）を持つ新しい行として取り込まれます。`ReplacingMergeTree`テーブルエンジンは、Ordering Key（ORDER BY カラム）を使ってバックグラウンドで重複を処理し、最新の`_peerdb_version`を持つ行だけを最終的に残します。PostgreSQLからのDELETEは、`_peerdb_is_deleted`カラムを使って削除フラグ付きの新規行として反映されます。以下のスニペットは、ClickHouse上の`public_goals`テーブル定義例です。



```
clickhouse-cloud :) SHOW CREATE TABLE public_goals;
CREATE TABLE peerdb.public_goals
(
    `id` Int64,
    `owned_user_id` String,
    `goal_title` String,
    `goal_data` String,
    `enabled` Bool,
    `ts` DateTime64(6),
    `_peerdb_synced_at` DateTime64(9) DEFAULT now(),
    `_peerdb_is_deleted` Int8,
    `_peerdb_version` Int64
)
ENGINE = SharedReplacingMergeTree
('/clickhouse/tables/{uuid}/{shard}', '{replica}', _peerdb_version)
PRIMARY KEY id
ORDER BY id
SETTINGS index_granularity = 8192

```

## 同じ行が重複して見えることがある場合、どう対応するか？ [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E5%90%8C%E3%81%98%E8%A1%8C%E3%81%8C%E9%87%8D%E8%A4%87%E3%81%97%E3%81%A6%E8%A6%8B%E3%81%88%E3%82%8B%E3%81%93%E3%81%A8%E3%81%8C%E3%81%82%E3%82%8B%E5%A0%B4%E5%90%88%E3%81%A9%E3%81%86%E5%AF%BE%E5%BF%9C%E3%81%99%E3%82%8B%E3%81%8B)


ReplacingMergeTreeはバックグラウンドで非同期に重複排除を行うため、重複を完全になくすことは保証されません。そのため、クエリ結果に同じ行や同じ主キーを持つ行が異なるバージョンで表示されることがあります。これは想定どおりの動作です。重複を取り除くには、いくつか方法があります。


### クエリにFINALを使う [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E3%82%AF%E3%82%A8%E3%83%AA%E3%81%ABfinal%E3%82%92%E4%BD%BF%E3%81%86)


ClickHouseには[FINAL](https://clickhouse.com/docs/ja/sql-reference/statements/select/from#final-modifier)というユニークな修飾子があり、クエリ実行時に行のマージ（重複排除）を行います。重複排除はWHERE句の後、GROUP BYなどの集計の前に実行されます。


過去にはFINALを使うとクエリ性能が低下するという懸念がありましたが、ClickHouseの最近のリリースでは[FINALクエリのパフォーマンスが大幅に改善](https://github.com/ClickHouse/ClickHouse/issues/11722)されています。そのため、まずはFINAL句を使ってみて、クエリのパフォーマンスを評価してみるのがいいでしょう。以下はFINAL句の例です。



```
SELECT owner_user_id, COUNT(*) FROM goals FINAL 
WHERE enabled = true GROUP BY owner_user_id;

```

### argMaxを使ってクエリ時に重複排除する [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#argmax%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%82%AF%E3%82%A8%E3%83%AA%E6%99%82%E3%81%AB%E9%87%8D%E8%A4%87%E6%8E%92%E9%99%A4%E3%81%99%E3%82%8B)


ClickHouseの[argMax](https://clickhouse.com/docs/ja/sql-reference/aggregate-functions/reference/argmax)は、クエリ実行時に動的に重複排除するのに便利な関数です。バージョンやタイムスタンプ列に基づいて最新のレコードだけを取りたい場合によく使います。


たとえば、`peerdb.public_goals`テーブルでidが主キー、`_peerdb_version`がバージョンを示す場合、argMaxを使って各`id`の最大`_peerdb_version`を持つ行を選択できます。これで元データを変更せずに重複を取り除き、サブクエリで集計を行えます。以下はargMaxの例です。



```
SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM
(
    SELECT
        id,
        argMax(owned_user_id, _peerdb_version) AS owned_user_id,
        argMax(goal_title, _peerdb_version) AS goal_title,
        argMax(goal_data, _peerdb_version) AS goal_data,
        argMax(enabled, _peerdb_version) AS enabled,
        argMax(ts, _peerdb_version) AS ts,
        argMax(_peerdb_synced_at, _peerdb_version) AS _peerdb_synced_at,
        argMax(_peerdb_is_deleted, _peerdb_version) AS _peerdb_is_deleted,
        max(_peerdb_version) AS _peerdb_version
    FROM peerdb.public_goals
    WHERE enabled = true
    GROUP BY id
) AS deduplicated_goals
GROUP BY owned_user_id;

```

### WINDOW FUNCTIONSを使う [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#window-functions%E3%82%92%E4%BD%BF%E3%81%86)


ClickHouseの[ウィンドウ関数](https://clickhouse.com/docs/ja/sql-reference/window-functions)を使って、idごとに`_peerdb_version`が最大の行だけを選択し、重複を排除することもできます。以下は例です。



```
SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM
(
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY _peerdb_version DESC) AS rn
    FROM peerdb.public_goals
    WHERE enabled = true
) AS ranked_goals
WHERE rn = 1
GROUP BY owned_user_id;

```

### Viewsを使って重複排除を簡単にする [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#views%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E9%87%8D%E8%A4%87%E6%8E%92%E9%99%A4%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E3%81%99%E3%82%8B)


[VIEW](https://clickhouse.com/docs/ja/sql-reference/statements/create/view)を使って重複排除のロジックをカプセル化し、BIツールなどから常に最新データだけを簡単に参照できるようにする方法もあります。たとえば、ウィンドウ関数で最新バージョンだけを残すVIEWを作成できます。



```
CREATE VIEW goals AS
SELECT * FROM
(
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY _peerdb_version DESC) AS rn
    FROM peerdb.public_goals
    WHERE enabled = true
) WHERE rn = 1;

```


```
SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM goals
GROUP BY owned_user_id;

```

## Nullableカラム [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#nullable%E3%82%AB%E3%83%A9%E3%83%A0)


Postgresから移行して驚くことの一つに、ClickHouseでは、[`Nullable`](https://clickhouse.com/docs/ja/sql-reference/data-types/nullable)で明示的に指定しない限りNULL値を格納しないという仕様があります。たとえば日付のカラムであれば、NULLを格納する代わりに`1970-01-01`のようなデフォルト値を使うので、想定外に感じるかもしれません。これはカラムナデータベースとしての特性で、NULLを格納すると[クエリパフォーマンスに影響](https://clickhouse.com/docs/ja/sql-reference/data-types/nullable)を与えるためです。そのため、ClickHouseではユーザーが`Nullable`を明示する必要があります。


PeerDBでは、`PEERDB_NULLABLE`という設定を導入しており、`true`を指定すると、PostgresでNULLがあり得るカラムを自動的に`Nullable`扱いでClickHouseにマッピングしてくれます。そのため、手動で`Nullable`を定義する必要はありません。詳しくは[こちらのPR](https://github.com/PeerDB-io/peerdb/pull/2001)を参照してください。


## **データ型** [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B)


ClickHouseは数値、テキスト、タイムスタンプ、日付、配列から、最近追加された[JSON](https://github.com/ClickHouse/ClickHouse/issues/54864)型まで、多彩なデータ型をサポートしています。Postgresの多くのデータ型は、ほとんど修正なしでClickHouseに格納できます。


参考までに、PeerDBがPostgresからClickHouseへデータをレプリケートするときに使っている[データ型マトリックス](https://docs.peerdb.io/datatypes/datatype-matrix)を共有します。


## The Ordering Key [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#the-ordering-key)


### Ordering Keyとは？ [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#ordering-key%E3%81%A8%E3%81%AF)


Ordering Keyを正しく選ぶことはClickHouseにおけるクエリ性能の要です。テーブル作成時に指定する`ORDER BY`句で定義され、Postgresにおけるインデックスのような役割を果たしますが、分析用途に最適化されています。PostgresのB\-treeインデックスが行ごとにポインタを管理するのとは異なり、ClickHouseはSparse Indexingを用います。


1. **データはOrdering Keyに基づいてソート**: ORDER BYで指定されたカラムに基づき、ディスク上のデータがソートされます。値が近いもの同士がまとまるため、[圧縮](https://clickhouse.com/docs/ja/data-compression/compression-in-clickhouse)が効きやすくなります。
2. **Ordering Keyはスパースインデックスも作成**: Ordering Keyによりカラムの範囲のみを保存するスパースインデックスも作られます。エントリが各行を指すのではなく、ソートされた行のまとまりを指すため、インデックス自体が小さく、バイナリサーチで素早くデータの範囲を絞り込めます。詳しくは[こちら](https://clickhouse.com/docs/ja/migrations/postgresql/designing-schemas#primary-ordering-keys-in-clickhouse)を参照してください。


Ordering Keyは、Postgresの[BRIN](https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-BRIN)インデックスに似た考え方ですが、ClickHouseではデータがOrdering Keyに基づいて自動的にソート（パーツの非同期マージ）されるため、取り込み時にユーザーがソートを意識する必要はありません。


### 適切なOrdering Keyの選び方 [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E9%81%A9%E5%88%87%E3%81%AAordering-key%E3%81%AE%E9%81%B8%E3%81%B3%E6%96%B9)


Ordering Keyを選ぶ際は、クエリのWHERE句でよく使うカラムを優先的に指定します。**カーディナリティ（重複の少なさ）が低いカラムから順番に並べる**と圧縮効率も高まり、クエリ性能も上がります。より詳しい内容は[こちら](https://clickhouse.com/docs/ja/data-modeling/schema-design#choosing-an-ordering-key)を参照してください。


### **PRIMARY KEYとOrdering Keyの違い** [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#primary-key%E3%81%A8ordering-key%E3%81%AE%E9%81%95%E3%81%84)


`public_goals`テーブル定義をみると`PRIMARY KEY`が指定されていますが、`ORDER BY`句もあります。両者の違いは何でしょうか？


1. `PRIMARY KEY`を指定した場合、そのカラムがスパースインデックスとして使われ、`ORDER BY`句で指定されたカラム順でディスク上のデータがソートされます。そして`ReplacingMergeTree`でのデータの重複排除にも使われます。
2. `PRIMARY KEY`を指定しなかった場合、Ordering Keyが自動的に`PRIMARY KEY`にもなり、スパースインデックスとして機能します。



> **NOTE:** `PRIMARY KEY`のカラムは、常にOrdering Keyの先頭に含める必要があります。インデックスと物理的なデータの順序が一致することで、不要なデータスキャンを最小化し、クエリ性能を最大化できます。


**`PRIMARY KEY`と`ORDER BY`が異なる例**


たとえば、クエリで`customer_id`を使うことが多く、`id`ではあまりフィルタしないケースを考えます。この場合、`PRIMARY KEY`を`customer_id`にして、`ORDER BY`を`customer_id, id`にすると、スパースインデックスが小さくなって効率的になり、データの重複排除も`id`単位で行えます。



> **NOTE:** Postgresの`PRIMARY KEY`は一意性を保証しますが、ClickHouseではそうではなく、スパースインデックスの定義に使われるという点が異なります。


### Ordering Keyの変更 [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#ordering-key%E3%81%AE%E5%A4%89%E6%9B%B4)


Ordering Key（[こちら](https://clickhouse.com/docs/ja/migrations/postgresql/designing-schemas#primary-ordering-keys-in-clickhouse)に解説あり）は、クエリ性能に直結するので非常に重要です。PeerDBではデフォルトでPostgreSQLの`PRIMARY KEY`をOrdering Keyとして使いますが、変更する方法はいくつかあります。


### マテリアライズドビューを使う [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E3%83%9E%E3%83%86%E3%83%AA%E3%82%A2%E3%83%A9%E3%82%A4%E3%82%BA%E3%83%89%E3%83%93%E3%83%A5%E3%83%BC%E3%82%92%E4%BD%BF%E3%81%86)


マテリアライズドビューを使うと、新しいOrdering Keyを持つテーブルを作成できます。重複排除のために、`ReplacingMergeTree`を使う場合は主キーとなるカラムをOrdering Keyの末尾に含めるのがおすすめです。以下は例です。



```
CREATE MATERIALIZED VIEW goals_mv
ENGINE = ReplacingMergeTree(_peerdb_version)
ORDER BY (enabled, ts, id) POPULATE AS
SELECT * FROM peerdb.public_goals;

```

**NOTE:** マテリアライズドビュー作成後は、前のセクションで説明した重複対応策を適用して、クエリ時の重複排除をきちんと行ってください。


### 目的のOrdering Keyを使ったテーブルを事前定義する [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#%E7%9B%AE%E7%9A%84%E3%81%AEordering-key%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%82%92%E4%BA%8B%E5%89%8D%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)


Ordering Keyを変えたい場合は、あらかじめ目的のOrdering Keyで新しいテーブルを作り、既存のテーブルと入れ替える方法もあります。手順は以下です。


**1\. Dummy Mirrorを作成する**: PeerDBでダミーのミラーを作り、必要なメタデータカラムやデータ型を定義した既定テーブルを生成します。


**2\. 新しいOrdering Keyでテーブルを作成**: PeerDBが作成したテーブルを参考に、新しいOrdering Keyを使ったテーブルを作ります。重複排除の観点から、主キーのカラムをOrdering Keyの末尾に入れるのがおすすめです。以下は例です。



```
CREATE TABLE public_events_new AS public_events
ENGINE = ReplacingMergeTree(_peerdb_version)
ORDER BY (user_id,id);

```

**3\. 古いテーブルを削除**:



```
DROP TABLE public_events;

```

**4\. 新しいテーブルの名前を変更**:



```
RENAME TABLE public_events_new TO public_events;

```

**5\. MIRRORを新テーブルに向けて開始**: MIRROR設定を新しいテーブルに向けます。PeerDBは内部的に`CREATE TABLE IF NOT EXISTS`を使っているので、そのまま新テーブルにデータが取り込まれます。


## DELETEの扱い [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#delete%E3%81%AE%E6%89%B1%E3%81%84)


前述のとおり、PostgreSQLのDELETEは`_peerdb_is_deleted`カラムに削除フラグを立てた行として取り込まれます。この削除フラグが立った行をクエリから除外したい場合は、ClickHouseの行レベルポリシーを使うことができます。例は以下のとおりです。



```
CREATE ROW POLICY policy_name ON table_name
FOR SELECT USING _peerdb_is_deleted = 0;

```

このポリシーを設定すると、`_peerdb_is_deleted`が0の行だけがSELECTクエリで参照されるようになります。


## Conclusion [\#](/jp/blog/postgres-to-clickhouse-data-modeling-tips-jp#conclusion)


ここまで読んでいただきありがとうございます。PostgreSQLからClickHouseへ移行するときにありがちなデータモデリング上の注意点を中心に解説しました。次回のブログでは、さらに高度なトピックとしてJOINや効率的なSQLの書き方などを深掘りする予定です。もしPostgresからClickHouseへのデータレプリケーションを試してみたい方は、以下のリンクからPeerDBやClickHouseを触っていただくか、直接お問い合わせください！


1. [ClickHouse Cloudを無料で試す](https://clickhouse.com/docs/en/cloud-quick-start)
2. [PeerDB Cloudを無料で試す](https://auth.peerdb.cloud/signup)
3. [PostgresからClickHouseへのレプリケーションドキュメント](https://docs.peerdb.io/mirror/cdc-pg-clickhouse)
4. [PeerDBチームに直接連絡する](https://www.peerdb.io/sign-up)
