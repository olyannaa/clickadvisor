# 2025年1月リリース



pre div.p\-2 {
 margin\-bottom: 2rem;
}

また1ヶ月が経過し、つまり新しいリリースの時期がやってきました！


ClickHouse バージョン 25\.1 には、新機能が 15 件 🦃、パフォーマンス最適化が 36 件 ⛸️、そしてバグ修正が 77 件 🏕️ 含まれています。


このリリースでは、2 レベルのハッシュマップを使用してパラレルハッシュ結合アルゴリズムをさらに高速化し、テーブルレベルの MinMax インデックスを導入し、Merge テーブルを改善し、オートインクリメント機能を追加するなど、多くのアップデートが行われました！


## 新しいコントリビューター [\#](/jp/blog/clickhouse-release-25-01-jp#%E6%96%B0%E3%81%97%E3%81%84%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%BC)


25\.1 で新しく参加されたコントリビューターの皆さん、ようこそ！  

ClickHouse のコミュニティがこれほどまでに成長していることに驚きと感謝の気持ちでいっぱいです。ClickHouse がここまで広く使われるようになったのは、皆さんの貢献のおかげです。


新しく参加されたコントリビューターのお名前はこちらです:


*Artem Yurov, Gamezardashvili George, Garrett Thomas, Ivan Nesterov, Jesse Grodman, Jony Mohajan, Juan A. Pedreira, Julian Meyers, Kai Zhu, Manish Gill, Michael Anastasakis, Olli Draese, Pete Hampton, RinChanNOWWW, Sameer Tamsekar, Sante Allegrini, Sergey, Vladimir Zhirov, Yutong Xiao, heymind, jonymohajanGmail, mkalfon, ollidraese*


ヒント: どうやってこのリストを生成しているのか気になる方は … [こちら](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9) をご覧ください。



[プレゼンテーションのスライド](https://presentations.clickhouse.com/release_25.1/) もご覧いただけます。




---


## より高速になったパラレルハッシュ結合 [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%88%E3%82%8A%E9%AB%98%E9%80%9F%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%9F%E3%83%91%E3%83%A9%E3%83%AC%E3%83%AB%E3%83%8F%E3%83%83%E3%82%B7%E3%83%A5%E7%B5%90%E5%90%88)


### コントリビューション: Nikita Taranov [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-nikita-taranov)


[パラレルハッシュ結合](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join) は、バージョン 24\.11 以降 [デフォルトの結合戦略](https://clickhouse.com/blog/clickhouse-release-24-11#parallel-hash-join-is-the-default-join-strategy) となっており、すでに ClickHouse のインメモリで最速の [ハッシュテーブル](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions) を用いた [結合アルゴリズム](https://clickhouse.com/blog/clickhouse-fully-supports-joins-how-to-choose-the-right-algorithm-part5#imdb-large-join-runs) と言えます。それでもなお、[以前お約束した](https://clickhouse.com/blog/clickhouse-release-24-05#cross-join-improvements)通り、細部への[きめ細やかな配慮](https://clickhouse.com/docs/en/concepts/why-clickhouse-is-so-fast#meticulous-attention-to-detail)を重ねながら、リリースのたびに結合パフォーマンスの向上を追求し続けています。


バージョン 24\.7 では、[パラレルハッシュ結合のハッシュテーブルのアロケーション](https://clickhouse.com/blog/clickhouse-release-24-07#faster-parallel-hash-join) を改善しました。バージョン 24\.12 では、パラレルハッシュ結合でどちらのテーブルを `build phase` に使用すべきかを [自動的に判定する](https://clickhouse.com/blog/clickhouse-release-24-12#automatic-join-reordering) 機能を追加しました。そして今回の 25\.1 では、アルゴリズムの `probe phase` をさらに高速化しました。


まず最初に、`build phase` と `probe phase` が以前どのように動いていたかを簡単に解説しましょう。下図は、リリース前の ClickHouse におけるパラレルハッシュ結合の仕組みを示したものです（クリックで拡大）:


[![](/uploads/25_01_01_8cfbd11186.png)](/uploads/25_01_01_8cfbd11186.png)


アルゴリズムの ① **build phase** では、右側のテーブルのデータを分割し、`N` 本の処理スレッドで並行して処理することで、`N` 個のハッシュテーブルに平行してデータを格納します。`N` は設定項目の `max_threads` で制御され、例では `N=4` です。各処理スレッドが実行するループは次のとおりです:


1. 右側のテーブルから未処理の行ブロックを読み込む。
2. 各行の結合キーに対して「インスタンスハッシュ関数（図中の青色）」を適用し、その結果をスレッド数 (`N`) で剰余を取ることで、どのハッシュテーブルインスタンスに入れるかを決定する。
3. 続けて「挿入ハッシュ関数（図中の黄色）」を適用し、その結果をキーとして、② 右テーブルの行データを該当のハッシュテーブルインスタンスに挿入する。
4. 1 に戻って繰り返す。


アルゴリズムの ③ **probe phase** では、左側のテーブルのデータを分割し、`N` 本の処理スレッドで並行して処理します（`N` は先ほどと同様に `max_threads` で制御されます）。各処理スレッドが実行するループは次のとおりです:


1. 左側のテーブルから未処理の行ブロックを読み込む。
2. 各行の結合キーに対してビルドフェーズと同じ「インスタンスハッシュ関数（青色）」を適用し、その結果を `N` で剰余を取ることで、どのハッシュテーブルインスタンスを参照すべきかを決定する。
3. 続けてビルドフェーズと同じ「挿入ハッシュ関数（黄色）」を適用し、その結果をキーとして、選択されたハッシュテーブルインスタンスに ④ lookup を実行する。
4. lookup が成功し結合キーの値が一致すれば、⑤ 結合した行を返す。
5. 1 に戻って繰り返す。


パラレルハッシュ結合の `build phase` は、複数のハッシュテーブルを同時に作成できるため高速化に寄与します。一方、[非パラレルハッシュ結合](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#hash-join) では、[単一](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#description) のハッシュテーブルしか使わず、サイズが大きいテーブルを結合するときに挿入処理がボトルネックとなる可能性がありました。ただし、ハッシュテーブルは読み込みに関しては[スレッドセーフ](https://en.wikipedia.org/wiki/Thread_safety)であるため、非パラレルハッシュ結合の `probe phase` は単一のハッシュテーブルを並行で効率的に読み込むことができます。


しかし、パラレルハッシュ結合の場合、`build phase` を並行実行すると、前述のように `probe phase` で左側テーブルの入力ブロックをスレッドごとに分割して適切なハッシュテーブルインスタンスに振り分けるというオーバーヘッドが発生します。


この問題を解決するため、25\.1 では `probe phase` で単一の共有ハッシュテーブルを利用するように変更しました。これにより、入力ブロックの分割や振り分けが不要となり、オーバーヘッドが削減され効率が向上します。


次の図は、改善後のパラレルハッシュ結合の仕組みを示しています（クリックで拡大）:


[![](/uploads/25_01_02_cb04311596.png)](/uploads/25_01_02_cb04311596.png)


① **build phase** は以前と同様に並行で実行されます。ただし、`max_threads` \= `N` の場合でも、`N` 個のハッシュテーブルインスタンスを個別に作るのではなく、`N` 個の [two\-level hash table](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions) インスタンスを使います。これらのインスタンスにある 256 個のバケットは、`N` 本のスレッドによって重複のない形で並行に埋められます:


- **hash table instance \#0** は **bucket \#0**, **bucket \#`N`**, **bucket \#(`N` \* 2\)**, … のみを担当
- **hash table instance \#1** は **bucket \#1**, **bucket \#`N` \+ 1**, **bucket \#(`N` \* 2 \+ 1\)**, … のみを担当
- **hash table instance \#2** は **bucket \#2**, **bucket \#`N` \+ 2**, **bucket \#(`N` \* 2 \+ 2\)**, … のみを担当
- **hash table instance \#3** は **bucket \#3**, **bucket \#`N` \+ 3**, **bucket \#(`N` \* 2 \+ 3\)**, … のみを担当
- 以降も同様…


具体的には、各スレッドは以下のようなループを実行します:


1. 右テーブルから未処理の行ブロックを読み込む。
2. 結合キーに「挿入ハッシュ関数（黄色）」を適用し、その結果を `256` で剰余を取ることでターゲットとなるバケット番号を求める。
3. バケット番号をさらにスレッド数で剰余を取り、どの two\-level hash table インスタンスに割り当てるかを決定する。
4. 2 で得られた挿入ハッシュ関数の結果をキーとして、② 選択されたインスタンスの該当バケットに行データを挿入する。
5. 1 に戻って繰り返す。


`N` 個の two\-level hash table インスタンスで、各インスタンスのバケットを相互に重ならない形で並列に構築することで、`build phase` 後にこれら `N` 個のインスタンスを単一の two\-level hash table に ③ マージするときも、バケット同士をそのまま再配置すればいいだけなので効率的（定数時間）に処理が行えます。


④ **probe phase** では、すべての `N` 本のスレッドが、この共有 two\-level hash table を並行して読み込むことができます。非パラレルハッシュ結合と同じ要領です。各スレッドは次のようなループを行います:


1. 左側のテーブルから未処理の行ブロックを読み込む。
2. `build phase` と同じ「挿入ハッシュ関数（黄色）」を結合キーに適用し、その結果を 256 で剰余を取って、共有 two\-level hash table のどのバケットを参照するかを決定する。
3. 選択されたバケットに対して ⑤ lookup を実行する。
4. lookup が成功し、結合キーの値が一致すれば ⑥ 結合した行を返す。
5. 1 に戻って繰り返す。


なお、以前はビルドフェーズとプローブフェーズで 2 種類のハッシュ関数が使われていましたが、この実装変更後は、両フェーズとも単一のハッシュ関数のみを使うようになりました。two\-level hash table での間接参照は、軽量な剰余演算を加える程度のオーバーヘッドしか発生しません。


続いて、新しいパラレルハッシュ結合の速度向上を実測してみましょう。AWS EC2 の m6i.8xlarge インスタンス（vCPU 32 個、メモリ 128 GiB）でテストを行いました。


まず、次のクエリを ClickHouse バージョン 24\.12 で実行します:



```
SELECT
    count(c),
    version()
FROM numbers_mt(100000000) AS a
INNER JOIN
(
    SELECT
        number,
        toString(number) AS c
    FROM numbers(2000000)
) AS b ON (a.number % 10000000) = b.number
SETTINGS join_algorithm = 'parallel_hash';

```


```
   ┌─count(c)─┬─version()──┐
1. │ 20000000 │ 24.12.1.27 │
   └──────────┴────────────┘

1 row in set. Elapsed: 0.521 sec. Processed 102.00 million rows, 816.00 MB (195.83 million rows/s., 1.57 GB/s.)
Peak memory usage: 259.52 MiB.

```

次に、同じクエリを ClickHouse バージョン 25\.1 で実行します:



```
SELECT
    count(c),
    version()
FROM numbers_mt(100000000) AS a
INNER JOIN
(
    SELECT
        number,
        toString(number) AS c
    FROM numbers(2000000)
) AS b ON (a.number % 10000000) = b.number
SETTINGS join_algorithm = 'parallel_hash';

```


```
   ┌─count(c)─┬─version()─┐
1. │ 20000000 │ 25.1.3.23 │
   └──────────┴───────────┘

1 row in set. Elapsed: 0.330 sec. Processed 102.00 million rows, 816.00 MB (309.09 million rows/s., 2.47 GB/s.)
Peak memory usage: 284.96 MiB.

```

0\.521 秒から 0\.330 秒へと、およそ **36\.66%** の高速化です。


同じマシンで [TPC\-H データセット](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch)（スケールファクター 100）でも速度を比較しました。卸売りサプライヤーのデータウェアハウスをモデル化したテーブルを、[公式ドキュメント](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch#data-generation-and-import) に従って作成・ロードしています。


`lineitem` テーブルと `orders` テーブルを結合する典型的なクエリを、まずは ClickHouse 24\.12 で実行した際のホットラン（連続 3 回実行して最も速い結果）を見てみます:



```
SELECT
    count(),
    version()
FROM lineitem AS li
INNER JOIN orders AS o ON li.l_orderkey = o.o_orderkey
SETTINGS join_algorithm = 'parallel_hash';

```


```
   ┌───count()─┬─version()──┐
1. │ 600037902 │ 24.12.1.27 │
   └───────────┴────────────┘

1 row in set. Elapsed: 3.100 sec. Processed 750.04 million rows, 3.00 GB (241.97 million rows/s., 967.89 MB/s.)
Peak memory usage: 16.79 GiB.

```

次に、同じクエリを ClickHouse 25\.1 で実行した結果です:



```
SELECT
    count(),
    version()
FROM lineitem AS li
INNER JOIN orders AS o ON li.l_orderkey = o.o_orderkey
SETTINGS join_algorithm = 'parallel_hash';

```


```
   ┌───count()─┬─version()─┐
1. │ 600037902 │ 25.1.3.23 │
   └───────────┴───────────┘

1 row in set. Elapsed: 2.112 sec. Processed 750.04 million rows, 3.00 GB (355.15 million rows/s., 1.42 GB/s.)
Peak memory usage: 16.19 GiB.

```

3\.100 秒から 2\.112 秒へ、およそ **31\.87%** の高速化です。


**来月以降のリリースでも、さらに結合パフォーマンスを追求していきますので、お楽しみに！（そう、今後もずっとやります！）**




---


## テーブルレベルの MinMax インデックス [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%83%AC%E3%83%99%E3%83%AB%E3%81%AE-minmax-%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9)


### コントリビューション: Smita Kulkarni [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-smita-kulkarni)


[MinMax インデックス](https://clickhouse.com/docs/en/optimize/skipping-indexes#minmax) は、各ブロックに対して最小値と最大値を保持するインデックスで、ある程度ソートされている列に対して効果を発揮します。  

ただしデータが完全にランダムである場合は [あまり効果的ではありません](https://clickhouse.com/docs/en/guides/best-practices/sparse-primary-indexes#note-about-data-skipping-index)。


25\.1 以前は、このインデックスを各列ごとに指定する必要がありましたが、25\.1 では `add_minmax_index_for_numeric_columns` 設定を利用することで、数値型カラムすべてに一括して MinMax インデックスを付与できるようになりました。


例として、[StackOverflow データセット](https://clickhouse.com/docs/en/getting-started/example-datasets/stackoverflow)（質問や回答、タグなど 5,000 万件超）を使ってみましょう。まずは `stackoverflow` というデータベースを作成します:



```
CREATE DATABASE stackoverflow;

```

続いて、MinMax インデックスを適用しない場合のテーブル作成例は以下のとおりです:



```
CREATE TABLE stackoverflow.posts
(
    `Id` Int32 CODEC(Delta(4), ZSTD(1)),
    `PostTypeId` Enum8('Question' = 1, 'Answer' = 2, 'Wiki' = 3, 'TagWikiExcerpt' = 4, 'TagWiki' = 5, 'ModeratorNomination' = 6, 'WikiPlaceholder' = 7, 'PrivilegeWiki' = 8),
    `AcceptedAnswerId` UInt32,
    `CreationDate` DateTime64(3, 'UTC'),
    `Score` Int32,
    `ViewCount` UInt32 CODEC(Delta(4), ZSTD(1)),
    `Body` String,
    `OwnerUserId` Int32,
    `OwnerDisplayName` String,
    `LastEditorUserId` Int32,
    `LastEditorDisplayName` String,
    `LastEditDate` DateTime64(3, 'UTC') CODEC(Delta(8), ZSTD(1)),
    `LastActivityDate` DateTime64(3, 'UTC'),
    `Title` String,
    `Tags` String,
    `AnswerCount` UInt16 CODEC(Delta(2), ZSTD(1)),
    `CommentCount` UInt8,
    `FavoriteCount` UInt8,
    `ContentLicense` LowCardinality(String),
    `ParentId` String,
    `CommunityOwnedDate` DateTime64(3, 'UTC'),
    `ClosedDate` DateTime64(3, 'UTC')
)
ENGINE = MergeTree
ORDER BY (PostTypeId, toDate(CreationDate), CreationDate);

```

次に、数値型のカラムすべてに MinMax インデックスを適用するテーブルを作成してみます。



```
CREATE TABLE stackoverflow.posts_min_max
(
   `Id` Int32 CODEC(Delta(4), ZSTD(1)),
   `PostTypeId` Enum8('Question' = 1, 'Answer' = 2, 'Wiki' = 3, 'TagWikiExcerpt' = 4, 'TagWiki' = 5, 'ModeratorNomination' = 6, 'WikiPlaceholder' = 7, 'PrivilegeWiki' = 8),
   `AcceptedAnswerId` UInt32,
   `CreationDate` DateTime64(3, 'UTC'),
   `Score` Int32,
   `ViewCount` UInt32 CODEC(Delta(4), ZSTD(1)),
   `Body` String,
   `OwnerUserId` Int32,
   `OwnerDisplayName` String,
   `LastEditorUserId` Int32,
   `LastEditorDisplayName` String,
   `LastEditDate` DateTime64(3, 'UTC') CODEC(Delta(8), ZSTD(1)),
   `LastActivityDate` DateTime64(3, 'UTC'),
   `Title` String,
   `Tags` String,
   `AnswerCount` UInt16 CODEC(Delta(2), ZSTD(1)),
   `CommentCount` UInt8,
   `FavoriteCount` UInt8,
   `ContentLicense` LowCardinality(String),
   `ParentId` String,
   `CommunityOwnedDate` DateTime64(3, 'UTC'),
   `ClosedDate` DateTime64(3, 'UTC')
)
ENGINE = MergeTree
PRIMARY KEY (PostTypeId, toDate(CreationDate), CreationDate)
ORDER BY (PostTypeId, toDate(CreationDate), CreationDate, CommentCount)
SETTINGS add_minmax_index_for_numeric_columns=1;

```

最初のテーブルでは、PRIMARY KEY としてソートキーと同じ `(PostTypeId, toDate(CreationDate), CreationDate)` を使用しました。今回のテーブルではそれに加えて、`CommentCount` をソートキーに含めることで MinMax インデックスをより有効に活用しています。


こうすることで、`CommentCount` をはじめ、関連性の高い `FavoriteCount` や `AnswerCount` と組み合わせたフィルタリングを行うクエリを効率的に実行できます。


下記のクエリで、すべての数値カラムに MinMax インデックスが作成されたことを確認できます:



```
SELECT name, type, granularity
FROM system.data_skipping_indices
WHERE (database = 'stackoverflow') AND (`table` = 'posts_min_max');

```


```
┌─name───────────────────────────────┬─type───┬─granularity─┐
│ auto_minmax_index_Id               │ minmax │           1 │
│ auto_minmax_index_AcceptedAnswerId │ minmax │           1 │
│ auto_minmax_index_Score            │ minmax │           1 │
│ auto_minmax_index_ViewCount        │ minmax │           1 │
│ auto_minmax_index_OwnerUserId      │ minmax │           1 │
│ auto_minmax_index_LastEditorUserId │ minmax │           1 │
│ auto_minmax_index_AnswerCount      │ minmax │           1 │
│ auto_minmax_index_CommentCount     │ minmax │           1 │
│ auto_minmax_index_FavoriteCount    │ minmax │           1 │
└────────────────────────────────────┴────────┴─────────────┘

```

`granularity` が `1` となっており、各グラニュールごとに MinMax インデックスが作成されていることがわかります。


それでは、両方のテーブルにデータを挿入してみましょう。まずは `posts` テーブルに挿入します:



```
INSERT INTO stackoverflow.posts 
SELECT * 
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/*.parquet');

```

その後、`posts` のデータを読み出して `posts_min_max` に取り込みます:



```
INSERT INTO stackoverflow.posts_min_max
SELECT *
FROM stackoverflow.posts;

```

完了したら、それぞれのテーブルを対象にクエリを実行してみます。  

たとえば、「コメント数が 50 超かつ ViewCount が 10000 超の質問を取得する」クエリは次のとおりです:



```
SELECT Id, ViewCount, CommentCount
FROM stackoverflow.posts
WHERE PostTypeId = 'Question'
AND CommentCount > 50 AND ViewCount > 10000;

```


```
SELECT Id, ViewCount, CommentCount
FROM stackoverflow.posts_min_max
WHERE PostTypeId = 'Question'
AND CommentCount > 50 AND ViewCount > 10000;

```

両方のテーブルで結果は同じです（下記は例としての出力）:



```
┌───────Id─┬─ViewCount─┬─CommentCount─┐
│ 44796613 │     40560 │           61 │
│  3538156 │     89863 │           57 │
│ 33762339 │     12104 │           55 │
│  5797014 │     82433 │           55 │
│ 37629745 │     43433 │           89 │
│ 16209819 │     12343 │           54 │
│ 57726401 │     23950 │           51 │
│ 24203940 │     11403 │           56 │
│ 43343231 │     32926 │           51 │
│ 48729384 │     26346 │           56 │
└──────────┴───────────┴──────────────┘

```

実行時間はいずれのテーブルもノートパソコン環境でおよそ 20 ミリ秒ほどでした。データ量が小さいので、MinMax インデックスの有無による違いは目立ちません。  

とはいえ、クエリプランを確認すると、両テーブルの動作の違いを見て取れます。`EXPLAIN indexes=1` を先頭につけてクエリを実行してみます。


`posts` テーブルの場合:



```
┌─explain─────────────────────────────────────┐
│ Expression ((Project names + Projection))   │
│   Expression                                │
│     ReadFromMergeTree (stackoverflow.posts) │
│     Indexes:                                │
│       PrimaryKey                            │
│         Keys:                               │
│           PostTypeId                        │
│         Condition: (PostTypeId in [1, 1])   │
│         Parts: 3/4                          │
│         Granules: 3046/7552                 │
└─────────────────────────────────────────────┘

```

プライマリインデックスにより、スキャンするグラニュールが `7552` から `3046` に減少しています。


続いて `posts_min_max` テーブルの場合:



```
┌─explain─────────────────────────────────────────────┐
│ Expression ((Project names + Projection))           │
│   Expression                                        │
│     ReadFromMergeTree (stackoverflow.posts_min_max) │
│     Indexes:                                        │
│       PrimaryKey                                    │
│         Keys:                                       │
│           PostTypeId                                │
│         Condition: (PostTypeId in [1, 1])           │
│         Parts: 2/9                                  │
│         Granules: 3206/7682                         │
│       Skip                                          │
│         Name: auto_minmax_index_ViewCount           │
│         Description: minmax GRANULARITY 1           │
│         Parts: 2/2                                  │
│         Granules: 3192/3206                         │
│       Skip                                          │
│         Name: auto_minmax_index_CommentCount        │
│         Description: minmax GRANULARITY 1           │
│         Parts: 2/2                                  │
│         Granules: 82/3192                           │
└─────────────────────────────────────────────────────┘

```

こちらのテーブルは元のグラニュール数が微妙に異なりますが、まずプライマリインデックスで `7682` から `3206` に減少し、次に `ViewCount` の MinMax インデックスで `3206` から `3192`、さらに `CommentCount` の MinMax インデックスで `3192` から `82` へと大幅に絞り込まれているのがわかります。




---


## バイナリ形式で書き込む前に確認を行う [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%83%90%E3%82%A4%E3%83%8A%E3%83%AA%E5%BD%A2%E5%BC%8F%E3%81%A7%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%82%80%E5%89%8D%E3%81%AB%E7%A2%BA%E8%AA%8D%E3%82%92%E8%A1%8C%E3%81%86)


### コントリビューション: Alexey Milovidov [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-alexey-milovidov)


バイナリ形式をターミナルに直接出力しようとするとき、ClickHouse が本当にそれを出力したいのか確認を求めるようになりました。  

たとえば、`posts` テーブルの全レコードを Parquet 形式で出力するクエリは以下のとおりです:



```
SELECT *
FROM stackoverflow.posts
FORMAT Parquet;

```

実行すると、以下のように表示されます:



```
The requested output format `Parquet` is binary and could produce side-effects when output directly into the terminal.
If you want to output it into a file, use the "INTO OUTFILE" modifier in the query or redirect the output of the shell command.
Do you want to output it anyway? [y/N]

```

おそらく、Parquet の形式で 5000 万件以上のデータをターミナルに垂れ流すのは望ましくないでしょうから、`N` を押せば実際に出力は行われません（クエリ自体は完了します）。




---


## 列名の短縮 [\#](/jp/blog/clickhouse-release-25-01-jp#%E5%88%97%E5%90%8D%E3%81%AE%E7%9F%AD%E7%B8%AE)


### コントリビューション: Alexey Milovidov [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-alexey-milovidov-1)


もうひとつ便利な改善点として、プリティ形式 (Pretty formats) を使う場合に、カラム名が自動で短縮されるようになりました。  

たとえば、次のクエリで StackOverflow データセットのカラムに対して分位点を求める例を見てみましょう:



```
SELECT
    quantiles(0.5, 0.9, 0.99)(ViewCount),
    quantiles(0.5, 0.9, 0.99)(CommentCount)
FROM stackoverflow.posts;

```

実行すると、それぞれのカラム名が短縮されます:



```
┌─quantiles(0.⋯)(ViewCount)─┬─quantiles(0.⋯mmentCount)─┐
│ [0,1559,22827.5500000001] │ [1,4,11]                 │
└───────────────────────────┴──────────────────────────┘

```



---


## オートインクリメント [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%AA%E3%83%BC%E3%83%88%E3%82%A4%E3%83%B3%E3%82%AF%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88)


### コントリビューション: Alexey Milovidov [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-alexey-milovidov-2)


Keeper に格納される名前付き分散カウンターを実装した新関数 `generateSerialID` により、テーブルのオートインクリメントを実現できるようになりました。この関数はバッチ処理によって高速であり、並行かつ分散された環境でも安全に動作します。


関数は `name` パラメータを受け取り、次のように呼び出せます:



```
select number, generateSerialID('MyCounter')
FROM numbers(10);

```


```
┌─number─┬─generateSeri⋯MyCounter')─┐
│      0 │                        0 │
│      1 │                        1 │
│      2 │                        2 │
│      3 │                        3 │
│      4 │                        4 │
│      5 │                        5 │
│      6 │                        6 │
│      7 │                        7 │
│      8 │                        8 │
│      9 │                        9 │
└────────┴──────────────────────────┘

```

同じクエリを再度実行すると、値は 10 から続きます:



```
┌─number─┬─generateSeri⋯MyCounter')─┐
│      0 │                       10 │
│      1 │                       11 │
│      2 │                       12 │
│      3 │                       13 │
│      4 │                       14 │
│      5 │                       15 │
│      6 │                       16 │
│      7 │                       17 │
│      8 │                       18 │
│      9 │                       19 │
└────────┴──────────────────────────┘

```

これをテーブルスキーマ内で使うこともできます:



```
CREATE TABLE test
(
  id UInt64 DEFAULT generateSerialID('MyCounter'),
  data String
)
ORDER BY id;

```

データを挿入してみましょう:



```
INSERT INTO test (data) 
VALUES ('Hello'), ('World');

```

テーブルを参照すると:



```
SELECT *
FROM test;

```


```
┌─id─┬─data──┐
│ 20 │ Hello │
│ 21 │ World │
└────┴───────┘

```

のように、自動で連番が振られているのがわかります。




---


## Merge テーブルの改善 [\#](/jp/blog/clickhouse-release-25-01-jp#merge-%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%81%AE%E6%94%B9%E5%96%84)


### コントリビューション: Alexey Milovidov [\#](/jp/blog/clickhouse-release-25-01-jp#%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AA%E3%83%93%E3%83%A5%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3-alexey-milovidov-3)


Merge テーブルエンジンを使うと、複数のテーブルを 1 つにまとめることができます。また、同様の機能が `merge` テーブル関数を通じても利用可能です。


25\.1 以前のバージョンでは、最初に見つかったテーブル構造をそのまま適用する仕様でしたが、25\.1 からはカラムが共通または Variant のデータ型に標準化されるようになりました。


例として、以下のように 2 つのテーブルを作成してみます:



```
CREATE TABLE players (
  name String, 
  team String
)
ORDER BY name;
CREATE TABLE players_new (
  name String,
  team Array(String)
)
ORDER BY name;

```

データを挿入します:



```
INSERT INTO players VALUES ('Player1', 'Team1');
INSERT INTO players_new VALUES ('Player2', ['Team2', 'Team3']);

```

その後、`merge` テーブル関数を使って両方のテーブルをクエリしてみましょう:



```
SELECT *, * APPLY(toTypeName)
FROM merge('players*')
FORMAT Vertical;

```


```
Row 1:
──────
name:             Player1
team:             Team1
toTypeName(name): String
toTypeName(team): Variant(Array(String), String)

Row 2:
──────
name:             Player2
team:             ['Team2','Team3']
toTypeName(name): String
toTypeName(team): Variant(Array(String), String)

2 rows in set. Elapsed: 0.001 sec.

```

`team` カラムが、`players` テーブルの `String` 型と `players_new` テーブルの `Array(String)` 型を組み合わせた **Variant** 型になっていることがわかります。


同じように、Merge テーブルエンジンを使う場合は次のようにすれば OK です:



```
CREATE TABLE players_merged
ENGINE = Merge(currentDatabase(), 'players*');

```

新しいテーブルの構造を確認してみると:



```
DESCRIBE TABLE players_merged
SETTINGS describe_compact_output = 1;

```


```
┌─name─┬─type───────────────────────────┐
│ name │ String                         │
│ team │ Variant(Array(String), String) │
└──────┴────────────────────────────────┘

```

`team` カラムが **Variant(Array(String), String)** 型として認識されているのがわかります。
