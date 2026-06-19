# ClickHouse CloudでExecutable UDFがパブリックベータとして利用可能になりました


本日、**実行可能 UDF が ClickHouse Cloud でパブリックベータとして利用可能になった**ことを発表できることを嬉しく思います。Python で関数を書き、zip としてクラスタにアップロードすれば、組み込み関数と同じように SQL から呼び出せます。ClickHouse は長期間生存するサンドボックスプロセスのプールを管理し、クエリ速度で行データをそれらに流します。関数は SQL が使えるあらゆる場所で呼び出し可能です。アドホッククエリ、JOIN、さらには INSERT のたびに発火するマテリアライズドビューでも利用できます。


これはまったく新しいアイデアではありません。実行可能 UDF はセルフホスト版の ClickHouse では以前から提供してきました。[2023 年の SQL から OpenAI を呼び出す記事](https://clickhouse.com/blog/clickhouse-open-ai-user-defined-functions-udfs)でも同じ仕組みを取り上げています。今回新しいのは、自前のサーバを動かさなくてもこれが使えるようになった点です。モデルコードはデータがある場所に置かれ、マネージドサンドボックス内で実行され、デプロイは Cloud コンソールの 1 つのアップロード画面だけで完結します。


これが何を可能にするかを示すために、デモを構築しました。小さな PyTorch オートエンコーダで約 60 億件の株式取引ティックをインジェスト時にインラインで異常度スコアリングし、Next.js のフロントエンドが埋め込みを消費します。ノートブック、UDF バンドル、SQL、Web アプリの完全なソースは[こちらのリポジトリ](https://github.com/ClickHouse/stock-anomaly-udf)にあります。


![packedbubble チャートと S&P 500 リーダーボードを備えた異常検知ダッシュボード](/uploads/hero_dashboard_5c8d3ce323.png)
## この機能が解決する課題 [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%81%93%E3%81%AE%E6%A9%9F%E8%83%BD%E3%81%8C%E8%A7%A3%E6%B1%BA%E3%81%99%E3%82%8B%E8%AA%B2%E9%A1%8C)


学習済みモデルがあり、ClickHouse にデータのストリームがあるとします。これまで両者を同じ場所で動かすには、おおむね次の 3 つの選択肢しかありませんでした。


1. **別途スコアリングサービスを立ち上げる。** こうするとモデルサーバ、行データをそこにルーティングするインジェストパイプライン、スコアを ClickHouse に書き戻す仕組みを保守する必要があります。モデルはもはやデータの近くにあるとは言えません。
2. **モデルを純粋な SQL に翻訳する。** 一部のツリーベースモデルであれば可能です。埋め込みを含むモデルでは苦痛そのものです。再学習のたびに数千行の SQL を手で再生成することになります。
3. **オフラインでバッチスコアリングし、後で結合する。** 鮮度が失われます。今しがた発生した取引の「異常」は、今すぐ反応できてこそ意味があります。


実行可能 UDF はこれら 3 つを 1 つに集約します。推論コードを普通の Python ファイルとして書き、ClickHouse にそれを指し示し、SQL から呼び出します。関数は、必要なクエリと一緒にインラインで実行されます。マテリアライズドビューの中でも実行でき、本記事ではまさにそれをやっています。


## 構築したもの [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%9F%E3%82%82%E3%81%AE)


昨年公開した[「Building StockHouse」](https://clickhouse.com/blog/building-stockhouse)では、ClickHouse が株式取引ティックの絶え間ない大量データをリアルタイムでどう処理するかを示しました。あの記事はインジェストとクエリレイヤで止まっていました。当然次に出てくる疑問は、「すべての取引が届いた瞬間に学習済みモデルを適用したくなったらどうするか?」です。


問題の形を分かりやすく示せるので、教師なしの異常検知セットアップを選びました。


- 小規模なオートエンコーダ(約 27 万パラメータ)を、5,000 万件の過去取引ティックで学習します。入力は、ハッシュ化したティッカー、7 つの数値特徴(価格、サイズ、取引所など)、6 つの周期エンコードされた時間特徴です。
- 各取引に対して、モデルは **32 次元の埋め込み**と**再構成誤差**を生成します。誤差が大きいということは、モデルがこのような取引パターンで学習されていないことを意味します。つまり、その銘柄の履歴における通常パターンと比較して*形状的に異常*ということです。
- このモデルをラップする UDF が `embed_trade` です。このシステム内で ML 固有のピースはこれだけです。あとはすべて普通の SQL です。スコアの集約、銘柄ごとのベースライン、ビュー、すべて SQL です。


データフローは次のとおりです。



```
            ┌───────────────────────────┐
            │  default.trades           │     ← upstream feed (e.g. Polygon)
            └──────────────┬────────────┘
                           │ INSERT
                           ▼
            ┌───────────────────────────┐
            │  trades_embeddings_mv     │     ← fires on every INSERT
            │  (calls embed_trade UDF)  │
            └──────────────┬────────────┘
                           │
                           ▼
            ┌───────────────────────────┐
            │  default.trades_embeddings│     ← same trade + 32-dim
            │                           │       embedding + recon_score
            └──────────────┬────────────┘
              ▲            │
              │            │ refresh hourly
              │            ▼
              │  ┌──────────────────────┐
              │  │ trades_baselines     │     ← per-symbol score
              │  │ trades_dim_baselines │       distribution stats
              │  └──────────────────────┘
              │
              └──── consumed by webapp queries
                    (anomalies are defined relative
                     to each symbol's own baselines)

```

`INSERT INTO trades` のすべてはマテリアライズドビューを経由し、スコアリングされ、`trades_embeddings` に格納されます。Web アプリはモデルを再実行することはありません。読み取るのは `trades_embeddings` と 2 つの軽量なベースラインテーブルだけです。高コストな推論は取引ごとにインジェストとインラインでちょうど 1 回だけ行われ、ダウンストリームのクエリはすべて通常の集約です。


## オートエンコーダの学習 [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%82%AA%E3%83%BC%E3%83%88%E3%82%A8%E3%83%B3%E3%82%B3%E3%83%BC%E3%83%80%E3%81%AE%E5%AD%A6%E7%BF%92)


モデル自体は ML 的には小さくて特に目新しくありませんが、UDF がランタイムにロードできるアーティファクトを生成しなければならないため、学習パイプラインには一見の価値があります。完全なウォークスルーは [`notebook/train_and_deploy_udf.ipynb`](https://github.com/ClickHouse/stock-anomaly-udf/blob/main/notebook/train_and_deploy_udf.ipynb) にあります。要約すると以下のとおりです。


1. **学習データを Parquet チャンクとしてストリーミング。** `default.trades` に対する SELECT で 14 個の入力特徴(価格、サイズ、取引所、コンディションコード数、ハッシュ化ティッカー、時刻と曜日の周期エンコード)をサーバ側で算出します。ノートブックは結果を `query_arrow_stream` 経由で取得し、500 万行ごとの Parquet チャンクをローカルディスクに書き出します。メモリ上には何も保持しません。
2. **`StandardScaler` をインクリメンタルにフィット。** `partial_fit` 経由の Welford アルゴリズムは、データセット全体での 1 回の `scaler.fit()` と同じ平均と分散を、限定的なメモリで得られます。フィットするのは 7 つの数値ベース特徴のみです。ハッシュ化ティッカーは整数キー、周期特徴はすでに妥当なスケールにあります。
3. **オートエンコーダを学習。** `TradeAutoencoderV2` は 4 層のエンコーダで 32 次元の潜在空間に圧縮し、対称なデコーダで数値特徴空間に戻します。シンボルの埋め込み参照は入力層で `sym_idx = xxHash32(sym) % NUM_HASH_BUCKETS` として行われます。損失は再構成された数値特徴の MSE です。学習は `IterableDataset` 経由で Parquet チャンクから行をストリーミングし、200 バッチの移動平均損失が 5 ウィンドウ連続で改善しなければ停止します。
4. **アーティファクトを 2 つ保存。** `scaler_params.pt` は `mean_` と `scale_` を Float32 テンソルとして保持します。`trade_autoencoder_v2.pt` はモデルの `state_dict` とコンストラクタの kwargs を含む `config` dict を保持します。UDF の `main.py` は起動時にこれらを読み込み、モデルを再構築します。
5. **バンドルをパッケージング。** ノートブックの最後のセルで `main.py`、`requirements.txt`、2 つの `.pt` ファイルを `embed_trade.zip` に圧縮し、アップロード可能な状態にします。


## Cloud への UDF のデプロイ [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#cloud-%E3%81%B8%E3%81%AE-udf-%E3%81%AE%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4)


デプロイのインターフェースは Cloud コンソールにある単一のアップロード画面です。名前、コードとモデルファイルが入った zip、いくつかのランタイムパラメータを指定するだけです。


![引数リストとランタイム設定が表示された ClickHouse Cloud UDF デプロイページ](/uploads/cloud_udf_deployment_95cd9b3a7d.png)
`embed_trade` では次のように設定します。


- **タイプ:** `executable_pool`。長期間生存するプロセスで、モデルはメモリ上にホットな状態に保たれます。
- **プールサイズ:** レプリカあたり `10`。各プロセスは起動時に 2MB のモデルをロードし(約 1\.5 秒)、以降の呼び出しでそれを再利用します。
- **ランタイム:** `python3.11`。依存関係(`torch==2.4.1`、`numpy==1.26.4`)は zip 内の `requirements.txt` から取得されます。
- **フォーマット:** `TabSeparated`。UDF は入力 1 行ごとに stdin から 1 行の TSV を読み取り、`(embedding, recon_score)` を stdout に出力します。
- **14 個の引数**。それぞれ明示的な ClickHouse 型を持ちます。シグネチャはオートエンコーダの学習スキーマと厳密に一致します。完全な対応表は [`udf/cloud-deployment.md`](udf/cloud-deployment.md) を参照してください。


これにより、関数は組み込み関数と同じように SQL から呼び出せます。


```
1WITH
2    fromUnixTimestamp64Milli(t, 'America/New_York') AS ts,
3    embed_trade(
4        xxHash32(sym), p, s, x, z, toUInt64(length(c)), trfi, trft,
5        toUInt8(toHour(ts)), toUInt8(toDayOfWeek(ts, 1)),
6        sin((toHour(ts) * 2 * pi()) / 24),
7        cos((toHour(ts) * 2 * pi()) / 24),
8        sin((toDayOfWeek(ts, 1) * 2 * pi()) / 7),
9        cos((toDayOfWeek(ts, 1) * 2 * pi()) / 7)
10    ) AS result
11SELECT
12    sym, i, x, p, s, c, t, q, z, trfi, trft, inserted_at,
13    result.2 AS recon_score,
14    result.1 AS embedding
15FROM stockhouse.trades limit 10;
```
興味深いのは、これが「できる」ということではなく、その呼び出しを「どこに置けるか」という点です。


## 取り込みと同時に、すべての取引をインラインでスコアリング [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E5%8F%96%E3%82%8A%E8%BE%BC%E3%81%BF%E3%81%A8%E5%90%8C%E6%99%82%E3%81%AB%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E5%8F%96%E5%BC%95%E3%82%92%E3%82%A4%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%81%A7%E3%82%B9%E3%82%B3%E3%82%A2%E3%83%AA%E3%83%B3%E3%82%B0)


`embed_trade` をマテリアライズドビューに組み込みます。


```
1CREATE MATERIALIZED VIEW trades_embeddings_mv
2TO trades_embeddings
3AS
4WITH
5    fromUnixTimestamp64Milli(t, 'America/New_York') AS ts,
6    embed_trade(
7        xxHash32(sym), p, s, x, z, toUInt64(length(c)), trfi, trft,
8        toUInt8(toHour(ts)), toUInt8(toDayOfWeek(ts, 1)),
9        sin((toHour(ts) * 2 * pi()) / 24),
10        cos((toHour(ts) * 2 * pi()) / 24),
11        sin((toDayOfWeek(ts, 1) * 2 * pi()) / 7),
12        cos((toDayOfWeek(ts, 1) * 2 * pi()) / 7)
13    ) AS result
14SELECT
15    sym, i, x, p, s, c, t, q, z, trfi, trft, inserted_at,
16    result.2 AS recon_score,
17    result.1 AS embedding
18FROM trades;
```
`INSERT INTO trades` のたびに、この MV が発火します。Python プールがそのバッチをスコアリングし、結果を `trades_embeddings` に書き込みます。他のムーバーも、他のサービスも、別途のスケジューラも存在しません。SQL だけです。


これは、Cloud で実行可能 UDF がサポートされる前には実現できなかった部分です。同等のサービスアーキテクチャを構築するなら、`trades` から読み出してバッチ化し、モデルサーバーに POST して結果を書き戻す Kafka コンシューマーが必要になります。最終状態は同じでも、動く部品はずっと増えます。ここでは DDL 一文で済むのです。


パフォーマンスの形は予想通りです。1 行あたりのコストはモデルのフォワードパス(ウォーム済みプールで数ミリ秒)に TSV シリアライゼーションを加えたものです。ClickHouse は行をチャンクにまとめて UDF へ渡します。プールは並列でいくつかの推論を同時実行します。3 レプリカのクラスター上で、手動スケーリングなしに \~35K rows/sec を数時間維持しながら、\~6B 行の履歴データをバックフィルしました。同じ UDF、同じ MV、同じ SQL です。


## 「異常」に意味を持たせる [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E7%95%B0%E5%B8%B8%E3%81%AB%E6%84%8F%E5%91%B3%E3%82%92%E6%8C%81%E3%81%9F%E3%81%9B%E3%82%8B)


オートエンコーダーは、各取引について生の `recon_score` を返します。これはデータセット全体でおおよそ 0\.00002 から 1,000,000\+ までの範囲の数値です。「0\.062 を超える取引は異常」という単純なフィルター(モデルの学習分布から得たグローバルな 99 パーセンタイルを利用)は一見妥当に思えますが、実際にデータを見るとそうではありません。


BRK.A や LLY のような一部の銘柄は、株価が異常に高いため、すべての取引がこの閾値を超えてしまいます。これらの銘柄の分布全体が、グローバル分布の右側の裾に位置しているからです。そうした銘柄に対して「100% が異常」という統計は、技術的には正しくても実用上は無意味です。


そこで、「異常」を各銘柄自身の履歴に対して相対的に再定義します。銘柄ごとに、その**生涯にわたる `recon_score` の p95** を維持しておきます。ある取引が *その銘柄にとって* 異常であるとは、その銘柄自身の p95 を超えていることを意味します。構成上、典型的なウィンドウでは約 5% の取引がこれに該当します。この割合が 5% を大きく上回ってスパイクしたとき、その銘柄は本当に異常なウィンドウに突入していると言えます。


銘柄ごとのベースラインは、別の ClickHouse テーブルに保持されます:


```
1CREATE TABLE trades_baselines (
2    sym         LowCardinality(String),
3    p50         Float32,
4    p95         Float32,
5    p99         Float32,
6    -- ...
7    computed_at DateTime
8)
9ENGINE = MergeTree
10ORDER BY sym;
```
**更新可能なマテリアライズドビュー** は、1時間ごとにデータを再投入します:


```
1CREATE MATERIALIZED VIEW trades_baselines_mv
2REFRESH EVERY 1 HOUR
3TO trades_baselines
4AS
5SELECT
6    sym,
7    quantiles(0.5, 0.95, 0.99)(recon_score) AS qs,
8    qs[1] AS p50, qs[2] AS p95, qs[3] AS p99,
9    -- ...
10FROM trades_embeddings
11WHERE NOT has(c, 15) AND NOT has(c, 12)   -- exclude auction prints
12GROUP BY sym;
```
Refreshable MV はリフレッシュのたびに、ターゲットテーブルをアトミックに truncate して置き換えます。プレーンな `MergeTree` が適切なエンジンです。`FINAL` も不要、重複排除ロジックも不要、読み取り時のオーバーヘッドもありません。


リーダーボードクエリでは、**ライブトレードを baselines テーブルと JOIN** し、シンボルごとに自身のベースラインに対する異常値の件数をカウントします:


```
1SELECT
2    e.sym,
3    countIf(e.recon_score > b.p95) AS anomaly_count,
4    round(sumIf(e.s, e.recon_score > b.p95) * 100.0 / sum(e.s), 2) AS pct_of_volume
5FROM stockhouse.trades_embeddings AS e
6INNER JOIN stockhouse.trades_baselines AS b ON e.sym = b.sym
7WHERE e.t >= now() - INTERVAL 1 HOUR
8GROUP BY e.sym
9ORDER BY pct_of_volume DESC
10LIMIT 50;
```
このクエリは、\~1\.7秒（CTE としてインラインでベースラインを再計算する場合）から
\~0\.27秒（事前計算済みのテーブルと結合する場合）へと短縮されます。同じ結果で、おおよそ6倍
高速です。高コストな部分は、ページを読み込むたびではなく、1時間に1回だけマテリアライズされます。


## Webアプリ [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#web%E3%82%A2%E3%83%97%E3%83%AA)


Webアプリは Next.js \+ Click UI \+ Highcharts のデモです。`trades_embeddings`
とベースラインテーブルを利用します。


**アノマリーダッシュボード**は、自身のベースラインを超える取引量の割合で S\&P 500 銘柄をランク付けします。


![バブルチャートと詳細テーブルを備えたダッシュボード](/uploads/hero_dashboard_5c8d3ce323.png)
パックドバブルチャートは、各銘柄を `pct_of_volume`（その銘柄の生涯 p95 を上回る取引が、対象ウィンドウ内の全取引量に占める割合）に基づいてサイズと色で表現します。バブルが赤くて大きい銘柄ほど、その時間帯にアノマリーが集中していたことを意味します。左側のテーブルは同じ並び順で、OHLC、最大スコア、銘柄ごとのベースラインを並べて表示します。


**銘柄ドリルダウン**は、特定のティッカーにズームインします。


![ローソク足と出来高バー、異常取引のテーブルを表示する銘柄ドリルダウン](/uploads/symbol_drilldown_2844f51814.png)
上部にはローソク足と出来高ペインがあります。両方の軸は単一のプロットエリアで重なっており、価格軸は下方向に引き伸ばされ、ローソク足を上部65%に、出来高バーを下部30%に押し込んでいます。異常取引テーブルの任意の行にホバーすると、対応するローソク足の出来高バーが黄色く塗りつぶされ、その取引がバケットの総出来高に占める割合に応じたサイズになります。クロスヘアはローソク足の中央にスナップします。


**類似検索**は、取引をクリックするとドリルダウン上にモーダルで開きます。


![レーダーチャートと類似取引テーブルを備えた類似性モーダル](/uploads/similarity_modal_80d0258023.gif)
レーダーチャートは、各取引の13個の入力次元を、その銘柄の生涯における各次元の最小値・最大値・平均値で正規化してプロットします。平均値は常に `0.5` にマッピングされるため、ベースライン系列はチャートの中央に正確な13角形として描画されます。偏差が一目で分かります。類似取引の行にホバーすると、それが重ねて表示されます。最も類似した50件の取引は、同一銘柄の embedding 列に対する `cosineDistance(embedding, target_embedding)` から得られます。


**モデルドリフトモニター**は、スコア分布を経時的に追跡します。


![モデルドリフトの週次 p50/p95/p99/max チャートと銘柄ごとのドリフトライン](/uploads/drift_monitor_f552fa5951.png)
`recon_score` の週次 p50、p95、p99、最大値を、モデルが当初キャリブレートされた静的しきい値を示す水平参照線とともに表示します。週を追うごとに p99 が上昇し始めたなら、市場がモデルの学習分布から乖離しており、再学習のタイミングです。


**オークションプリントモニター**は、極端なテール部分の専用ビューです。寄付き
（c\=12）と引け（c\=15）のオークションプリントは、その膨大な株数のため、数千から数百万のスコアを記録します。


![上位オークションテーブルと日次カウントチャートを備えたオークションプリントモニター](/uploads/auction_monitor_39b129720c.png)
これらを他の場所でフィルタリングしなければ、あらゆるビューを支配してしまうでしょう。そこで、これらは独自のページを持っています。


## もう一つ：ネットワークアクセス UDF（プライベートベータ） [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%82%82%E3%81%86%E4%B8%80%E3%81%A4%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9-udf%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%99%E3%83%BC%E3%82%BF)


ここまで紹介してきたものはすべて、決定論的なパス上で動作します。`embed_trade`
は取り込み時に行をスコア付けし、ベースラインは1時間ごとにリフレッシュされ、Webアプリは事前計算済みテーブルを読み取ります。読み取りパス上にはどこにも外部呼び出しがありません。これは、負荷を支える部分に求められる形です。安価で、予測可能で、消えてしまう可能性のある上流が存在しません。


しかし、取引がアノマリーとしてフラグ付けされた後、当然次に浮かぶ疑問は*なぜ*かということです。その答えは ClickHouse の外側にあります — ニュース API、SEC ファイリング、取引停止通知、ソーシャルシグナルなどです。これらを取り込むには、UDF からのネットワークアクセスが必要です。


**ネットワークアクセス対応の実行可能 UDF は、ClickHouse Cloud でプライベートベータ提供中です。** 有効化すると、UDF ランタイムは許可された任意のホストへのアウトバウンド HTTPS 呼び出しを行えます。このリポジトリでは、これを利用する2つの新しい UDF を追加しました：


### `nearby_events` [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#nearby_events)


`(sym, t, window_min)` を与えると、2つの外部ソースを呼び出し、その取引時刻付近のイベントを JSON 配列として返します：


1. **Massive News API**（Polygon は最近 **Massive** にブランド変更されましたが、
`api.polygon.io` エンドポイントは以前と同様に応答します）。
2. **SEC EDGAR**（無料、公開、API キー不要）。

```
1SELECT
2    sym,
3    JSONLength(nearby_events(sym, t, 120)) AS n_events
4FROM stockhouse.trades_embeddings
5WHERE recon_score > 1.0
6LIMIT 5;
```
これは `url()` でも *ほぼ* 実現できます。これを UDF にしている違いは以下の通りです。


- **インプロセスでの合成。** Polygon の結果と EDGAR のファイリングを、1 回の Python 呼び出しの中で重複排除・ソート・件数制限まで行えます。SQL で 2 つの `url()` 呼び出しをチェーンすると、同じロジックを `UNION ALL` と下流の `arrayJoin`/`groupArray` 配管に押し込むことになり、動作はするものの見栄えが悪くなります。
- **環境変数による認証。** Polygon API キーはプールプロセスの起動時に `POLYGON_API_KEY` から読み込まれます。SQL には一切登場しません。
- **プロセスごとの LRU キャッシュ。** 各プールワーカーは `(sym, minute, window)` をキーに直近の結果を保持します。UI 上で同じトレードに 2 回ホバーしても、API 呼び出しは 2 回ではなく 1 回で済みます。
- **コネクションの再利用。** プロセスごとに長寿命の `requests.Session()` を保持し、HTTP コネクションをそのワーカーが稼働している間(数時間に及ぶ)生かし続けます。


### `classify_trade` [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#classify_trade)


`(sym, t)` を与えると、`nearby_events` の内部処理を介してコンテキストを取得し、**Anthropic Claude** に対して、その異常なトレードの最も可能性の高い原因を分類するよう問い合わせます。戻り値は型付きタプルです:


```
1WITH classify_trade('LLY', 1778777944818) AS c
2SELECT c.1 AS cause, c.2 AS confidence, c.3 AS summary;
```
原因は固定された分類体系に制約されます: `earnings`、`m_and_a`、`halt`、`rumor`、`sector_move`、`block_trade`、`no_news_found`。これは Anthropic の **tool\-use** メカニズムによって強制されます。モデルは、`input_schema` の `cause` フィールドに `enum` を含むツールを呼び出すよう要求されるため、レスポンスは必ずパース可能であり、cause は必ず既知の値のいずれかになることが保証されます。自由形式のテキストを正規表現でパースする必要も、「モデルが 'earnings' に近いが余分な単語を含む何かを返した」というフォローアップロジックも不要です。


Web アプリの類似度モーダルを覚えていますか? `classify_trade` と `nearby_events` は、そのモーダルの上部に固定される **「なぜ異常なのか?」** パネルを駆動しています。トレードを開くと、このパネルは両方の UDF を並列で呼び出し、以下を表示します:


- 分類された原因と信頼度の数値を示すバッジ
- モデルが書いた 1〜2 文のサマリー
- 判断の根拠となったニュースの見出しと提出書類の短いリスト


![Why-anomalous パネルを示す類似度モーダル。原因バッジ、サマリー、イベント一覧を表示](/uploads/why_anomalous_ef01e5439a.png)
### なぜこれが重要なのか [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%81%AA%E3%81%9C%E3%81%93%E3%82%8C%E3%81%8C%E9%87%8D%E8%A6%81%E3%81%AA%E3%81%AE%E3%81%8B)


`url()` は ClickHouse に長年存在しており、アドホックな取得には適しています。ネットワークアクセス UDF はそれ以外の部分を埋めます: ステートフルなクライアント、認証ライフサイクル、マルチステップのパイプライン、構造化された LLM 出力、プロセスごとのキャッシュなどです。「実行する必要があるコード」と「クエリする必要があるデータ」の境界線がより薄くなります。


3 つの API 呼び出しと LLM プロンプトを含む 200 行の Python 関数を `SELECT` の中に入れることができます。他の誰もその存在を知る必要はありません。


**自身のクラスターで試してみたいですか?** ネットワークアクセス UDF はプライベートベータ中です — ClickHouse Cloud サポートに連絡して有効化してもらいましょう!


## ここが興味深いポイント [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%81%93%E3%81%93%E3%81%8C%E8%88%88%E5%91%B3%E6%B7%B1%E3%81%84%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88)


ほとんどの ML on streaming data アーキテクチャは統合コストを支払っています。モデルはどこかにあり、データは別のどこかにあります。それらをつなぐ接着剤がそれ自体一つのシステムになっています。このリポジトリのセットアップはそれをフラットにします。ClickHouse Cloud クラスター、2MB の Python ファイル、そしてそれらを結びつける 1 つの DDL ステートメントがあるだけです。


Web アプリの UI ロジックはすべて SQL クエリです。システム内で唯一の ML は異常検知ですが、それすら「Web アプリ内の ML」ではなく、テーブルのカラムにすぎません。「この銘柄の直近 1 時間がどれだけ異常か」の計算、「コサイン距離で類似トレードを見つける」クエリ、銘柄ごとの p95 ベースライン、それらすべてを最新に保つマテリアライズドビュー。これらはすべて、標準的な ClickHouse テーブルに対して動作する標準的な SQL 機能です。


Cloud の実行可能 UDF は、ClickHouse の上に新しい抽象化を追加するものではありません。Python を SQL の一部にする手段を提供するものです。


## 再現する [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E5%86%8D%E7%8F%BE%E3%81%99%E3%82%8B)


プロジェクト全体は [https://github.com/clickhouse/stock\-anomaly\-udf](https://github.com/clickhouse/stock-anomaly-udf) にあります。



```
stock-anomaly-udf/
├── notebook/   # オートエンコーダーの学習、重みのエクスポート、UDF zip のパッケージング
├── udf/        # デプロイ可能なバンドル: main.py、モデルの重み、デプロイ手順
├── sql/        # ソーススキーマ、auto-embed MV、2 つのリフレッシュ可能なベースライン MV
└── web/        # Next.js のデモアプリ

```

### クイックスタート [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E3%82%AF%E3%82%A4%E3%83%83%E3%82%AF%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88)


1. **UDF をクラスターに配置する。**


	- `udf/embed_trade/` の内容を zip 化します:
	
	```
	cd udf/embed_trade && zip embed_trade.zip main.py requirements.txt *.pt
	
	```
	- Cloud UDF デプロイ UI 経由でアップロードします。[`udf/cloud-deployment.md`](https://github.com/ClickHouse/stock-anomaly-udf/blob/main/udf/cloud-deployment.md) に従って設定してください。
2. **SQL ファイルを順番に実行する:**



```
:run sql/01_source_schema.sql
:run sql/02_embeddings_mv.sql
:run sql/03_score_baselines.sql
:run sql/04_dim_baselines.sql

```
3. **過去データのバックフィル**(オプション)。MV と同じ SELECT パターンを使い、任意の時間範囲を対象に `trades_embeddings` へ一括 INSERT を実行します。手順 2 の MV は、それ以降 `default.trades` へ INSERT されるすべてのデータを自動的に取り込みます。
4. **Web アプリを起動する:**



```
cd web
cp .env.example .env.local   # CH_HOST/PORT/USER/PASS/DB を記入
npm install
npm run dev

```

<http://localhost:3000> を開きます。


`notebook/` のノートブックでは、独自のオートエンコーダーをエンドツーエンドで学習する手順を説明しています。`default.trades` から学習データを Parquet チャンクとしてストリーミングし、`StandardScaler` をインクリメンタルに適合させ、early stopping で学習を行い、成果物をデプロイ可能なバンドルとして zip 化します。


## 実行可能 UDF を試す [\#](/jp/blog/executable-udfs-clickhouse-cloud-beta-jp#%E5%AE%9F%E8%A1%8C%E5%8F%AF%E8%83%BD-udf-%E3%82%92%E8%A9%A6%E3%81%99)


パブリックベータは本日より ClickHouse Cloud で利用可能です。これを使って面白いものを作ったら、ぜひお知らせください!

### 今すぐ始めましょう

ClickHouseが皆さんのデータでどのように動作するか興味はありませんか? わずか数分でClickHouse Cloudを使い始められ、$300の無料クレジットも受け取れます。[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-825-sign-up&utm_blogctaid=825)
