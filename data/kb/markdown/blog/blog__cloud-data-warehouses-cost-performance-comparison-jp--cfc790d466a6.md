# 主要5大クラウドデータウェアハウスのコストパフォーマンス比較



> **要約**  
>   
> **Snowflake**、**Databricks**、**ClickHouse Cloud、BigQuery**、**Redshift**を10億行、100億行、1000億行の規模でベンチマークし、各ベンダーの実際のコンピュート課金ルールを適用しました。  
>   
> 
> 大規模な分析ワークロードにおいて、**ClickHouse Cloudは他のすべてのシステムよりも桁違いに優れたコストパフォーマンスを提供します**。


## クラウドウェアハウスのコストパフォーマンスを比較する方法 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%82%AF%E3%83%A9%E3%82%A6%E3%83%89%E3%82%A6%E3%82%A7%E3%82%A2%E3%83%8F%E3%82%A6%E3%82%B9%E3%81%AE%E3%82%B3%E3%82%B9%E3%83%88%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%82%92%E6%AF%94%E8%BC%83%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95)


データセットと一連の分析クエリがあります。それらを実行できる複数のクラウドデータウェアハウスがあります。そして質問はシンプルです：



> **分析ワークロードにおいて、1ドルあたり最も高いパフォーマンスを得られるのはどこか？**


価格表ではこれに答えられません。


[答えられないのです](/blog/how-cloud-data-warehouses-bill-you)。異なるベンダーはコンピュートの計測方法が異なり、容量の価格設定が異なり、「コンピュートリソース」の定義が異なるため、その数値を額面通りに比較することはできません。


そこで私たちは、主要な5つのクラウドデータウェアハウスすべてで*同じ*本番環境由来の分析ワークロードを実行しました：


- **Snowflake**
- **Databricks**
- **ClickHouse Cloud**
- **BigQuery**
- **Redshift**


そして、**10億**、**100億**、**1000億**行という3つのスケールで実行し、データが増えるにつれてコストとパフォーマンスがどのように変化するかを確認しました。


短いバージョンが必要な場合は、ネタバレをどうぞ：**コストパフォーマンスはシステム間で線形にスケールしません。**



> **ClickHouse Cloudは他のすべてのシステムよりも桁違いに優れたコストパフォーマンスを提供します。**


![Blog-Costs-animation01_small.gif](/uploads/Blog_Costs_animation01_small_de9ac301cc.gif)
詳細、チャート、方法論が必要な場合は、読み進めてください。



> **再現可能なパイプライン**：  
> この投稿のすべての結果は、[Bench2Cost](/blog/how-cloud-data-warehouses-bill-you#before-we-dive-in-how-we-calculate-costs-with-bench2cost)を使用して生成されています。これは、オープンで完全に再現可能なベンチマークパイプラインです。
> Bench2Costは各システムの実際の**コンピュート**課金モデルを生の実行時間に適用するため、コスト比較が正確で検証可能です。
>   
>   
> 
> **ストレージは焦点ではありません**：  
> 
> Bench2Costはすべてのシステムの**ストレージコスト**も計算しますが、ストレージ価格はシンプルで、ベンダー間で類似しており、分析ワークロードのコンピュートと比較して無視できるため、ここでは強調していません。
>   
>   
> 
> **隠れたストレージの勝利**：  
> 
> とはいえ、チャートからリンクされている結果JSONの生の数値を見ると、**ClickHouse Cloudはストレージサイズとストレージコストの両方で他のすべてのシステムを静かに打ち負かしており、多くの場合桁違いです**が、これはこの比較の範囲外です。


## インタラクティブベンチマークエクスプローラー [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%A9%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%83%99%E3%83%B3%E3%83%81%E3%83%9E%E3%83%BC%E3%82%AF%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%97%E3%83%AD%E3%83%BC%E3%83%A9%E3%83%BC)


静的なチャートはストーリーテリングには最適ですが、完全なデータセットの表面をかすめるだけです。


そこで、私たちは新しいものを構築しました：**完全にインタラクティブなベンチマークエクスプローラー**を**ブログ内に埋め込みました**。


ベンダー、ティア、クラスターサイズ、データセットスケールを自由に組み合わせることができます。ランタイム、コスト、コストパフォーマンスランキングを切り替え、この研究の背後にある完全な結果を探索できます。



これらの数値をどのように生成したかを理解したい場合は、すべて投稿の最後にある[付録](/blog/cloud-data-warehouses-cost-performance-comparison#appendix-benchmark-methodology)に文書化されています。


まず10億行から始めて、各スケールでのシステムのパフォーマンスを見ていきましょう。


*(付録で説明されているように、各システムを評価するために標準的な43クエリのClickBench分析ワークロードを使用しています。)*


## 10億行：ベースライン [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#10%E5%84%84%E8%A1%8C%E3%83%99%E3%83%BC%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%B3)



> **10億スケールはベースラインとしてのみ含めていますが、現代のデータプラットフォームにとってより現実的なストレスポイントは100億、1000億、それ以上です。**  
>   
> 
> 今日の分析ワークロードは、数百億、数千億、さらには数兆行で日常的に動作しています。
> [Teslaはストレステストのために**1京行以上**をClickHouseに取り込みました](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale)、そして[ClickPy](https://clickpy.clickhouse.com/)、私たちのPythonクライアントテレメトリデータセットは、すでに **[2兆行](https://sql.clickhouse.com/?query=U0VMRUNUCiAgICAgICAgZm9ybWF0UmVhZGFibGVRdWFudGl0eShzdW0oY291bnQpKSBBUyB0b3RhbCwgdW5pcUV4YWN0KHByb2plY3QpIGFzIHByb2plY3RzIEZST00gcHlwaS5weXBpX2Rvd25sb2Fkcw&run_query=true)** を超えています。


以下の[散布図](/blog/cloud-data-warehouses-cost-performance-comparison#how-to-read-the-scatter-plot-charts)は、5つのシステムそれぞれについて、10億行のClickBench実行の合計実行時間（横軸）と合計コンピュートコスト（縦軸）を示しています。


*(明確さのために目盛りラベルを非表示にしていますが、点の位置は完全に正確なままです。上記のインタラクティブベンチマークエクスプローラーには完全な数値軸が表示されます。)*


![Blog-Costs.008.png](/uploads/Blog_Costs_008_3d74ce58e7.png)
*(表示される構成は各エンジンの全範囲を表しています。[詳細は付録](/blog/cloud-data-warehouses-cost-performance-comparison#what-configurations-we-compare)を参照してください。)*
10億行では、チャートは3つの明確な[象限の動作](/blog/cloud-data-warehouses-cost-performance-comparison#how-to-read-the-scatter-plot-charts)を明らかにします。




| カテゴリ | システム / ティア | 実行時間 | コスト |
| --- | --- | --- | --- |
| **大きなグループが理想的な象限に該当します — 十分に高速*かつ*リーズナブルな価格 — しかし、1ドルあたりの価値プロファイルは非常に異なります。** | | | |
| `高速 & 低コスト` | **ClickHouse Cloud** ([9ノード](https://clickhouse.com/blog/clickhouse-parallel-replicas)) | [\~23秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_1B/aws.9.236.parallel_replicas.json) | [\~$0\.67](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_1B/aws.9.236.parallel_replicas.json) |
| `高速 & 低コスト` | **BigQuery Enterprise（容量）** | [\~38秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_1B/result_enriched.json) | [\~$0\.80](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_1B/result_enriched.json) |
| `高速 & 低コスト` | **Redshift Serverless（128 RPU）** | [\~64秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_1B/enriched_1b.json) | [\~$0\.85](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_1B/enriched_1b.json) |
| `高速 & 低コスト` | **Databricks（Large）** | [\~80秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_Large_enriched.json) | [\~$0\.62](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_Large_enriched.json) |
| `高速 & 低コスト` | **Snowflake（Large）** | [\~127秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/large_enriched.json) | [\~$0\.85](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/large_enriched.json) |
| **これらの2つは許容できる速度を提供しますが、価格が高額です。** | | | |
| `高速 & 高コスト` | **Snowflake（4X\-Large）** | [\~45秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/4xl_enriched.json) | [\~$4\.8](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/4xl_enriched.json) |
| `高速 & 高コスト` | **Databricks（4X\-Large）** | [\~59秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_4X-Large_enriched.json) | [\~$6\.1](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_4X-Large_enriched.json) |
| **BigQuery On\-Demandは高速ですが、TiBあたりのスキャン課金により、メインプロットから完全に外れます。** | | | |
| `高速 & 高コスト`（チャート外） | **BigQuery On\-Demand** | [\~38秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_1B/result_enriched.json) | [\~$16\.9](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_1B/result_enriched.json) |
| **これらのティアは安価ですが、非常に遅いです。** | | | |
| `低速 & 低コスト` | **Databricks（2X\-Small）** | [\~712秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_2X-Small_enriched.json) | [\~$0\.55](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_1B/clickbench_2X-Small_enriched.json) |
| `低速 & 低コスト` | **Snowflake（X\-Small）** | [\~785秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/xs_enriched.json) | [\~$0\.65](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_1B/xs_enriched.json) |


コスト効率を直接比較するために、以下のチャートは実行時間とコストを単一のコストパフォーマンススコアに集約しています（[方法論の定義](/blog/cloud-data-warehouses-cost-performance-comparison#how-we-measure-overall-cost-performance-ranking)）：


![Blog-Costs.009.png](/uploads/Blog_Costs_009_18d232f919.png)
画像は明確になります：


- **ClickHouse Cloudは最も強力な総合コストパフォーマンスを提供します**。最も低い*実行時間 × コスト*値を持ち、他のすべてはそれと比較されます。
- **BigQuery（容量モード）**が次に続き、このデータセットサイズではClickHouseの約**2倍悪い**です。
- **他のほとんどの構成は急速に落ち込みます**。*実行時間 × コスト*が上昇するにつれて：**3〜4倍悪い**から、より大きなSnowflakeとDatabricksティアでは**2桁の倍数**まで。



> 真のストーリーはデータが増えたときに始まります。  
>   
> 10億行は現代の基準ではまだ小さく、データが100億行と1000億行にスケールするにつれて経済性は急速に変化し、ほとんどのシステムは「高速 \& 低コスト」ゾーンから急激に外れ始めます。


## 100億行：亀裂が現れ始める [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#100%E5%84%84%E8%A1%8C%E4%BA%80%E8%A3%82%E3%81%8C%E7%8F%BE%E3%82%8C%E5%A7%8B%E3%82%81%E3%82%8B)


以下の[散布図](/blog/cloud-data-warehouses-cost-performance-comparison#how-to-read-the-scatter-plot-charts)は、5つのシステムそれぞれについて、100億行のClickBench実行の合計実行時間（横軸）と合計コンピュートコスト（縦軸）を示しています。


*(前述のとおり、視覚的な明確さのために目盛りラベルを非表示にしていますが、点の位置は実際の基礎値を反映しています。上記のインタラクティブベンチマークエクスプローラーには完全な数値軸が含まれています。)*


![Blog-Costs.011.png](/uploads/Blog_Costs_011_a2429a91bc.png)
*(表示される構成は各エンジンの全範囲を表しています。[詳細は付録](/blog/cloud-data-warehouses-cost-performance-comparison#what-configurations-we-compare)を参照してください。)*
100億行では、最初の真の分離が現れます。実行時間が延び、コストが上昇するにつれて、システムは「高速 \& 低コスト」[象限](/blog/cloud-data-warehouses-cost-performance-comparison#how-to-read-the-scatter-plot-charts)から外れ始めます。




| カテゴリ | システム / ティア | 実行時間 | コスト |
| --- | --- | --- | --- |
| **これらは100億行でも理想的な象限にある唯一の2つのシステムですが、速度プロファイルは非常に異なります。** | | | |
| `高速 & 低コスト` | **ClickHouse Cloud** ([20ノード](https://clickhouse.com/blog/clickhouse-parallel-replicas)) | [\~67秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_10B/aws.20.236.parallel_replicas.json) | [\~$4\.27](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_10B/aws.20.236.parallel_replicas.json) |
| `高速 & 低コスト` | **Databricks（Large）** | [\~604秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_Large_enriched.json) | [\~$4\.70](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_Large_enriched.json) |
| **これらのシステムはまだ合理的に高速ですが、データが増えるにつれて価格が急激に上昇します。** | | | |
| `高速 & 高コスト` | **Snowflake（4X\-Large）** | [\~135秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/4xl_enriched.json) | [\~$14\.41](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/4xl_enriched.json) |
| `高速 & 高コスト` | **Databricks（4X\-Large）** | [\~188秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_4X-Large_enriched.json) | [\~$19\.28](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_4X-Large_enriched.json) |
| `高速 & 高コスト` | **BigQuery Enterprise（容量）** | [\~350秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_10B/result_enriched.json) | [\~$11\.73](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_10B/result_enriched.json) |
| **BigQuery On\-Demandは合理的に高速に実行されますが、オンデマンド課金モデルによりコストが高く、散布図の軸範囲をはるかに超えています。** | | | |
| `高速 & 高コスト`（チャート外） | **BigQuery On\-Demand** | [\~350秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_10B/result_enriched.json) | [\~$169](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_10B/result_enriched.json) |
| **コストは低いままですが、実行時間は数分または数時間の範囲に漂います。** | | | |
| `低速 & 低コスト` | **Snowflake（Large）** | [\~1,213秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/large_enriched.json) | [\~$8\.09](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/large_enriched.json) |
| `低速 & 低コスト` | **Snowflake（X\-Small）** | [\~9,547秒（2\.6時間）](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/xs_enriched.json) | [\~$7\.96](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_10B/xs_enriched.json) |
| **これらの2つは、はるかに高速な代替品よりも遅く*、かつ*高価です。** | | | |
| `低速 & 高コスト` | **Redshift Serverless（128 RPU）** | [\~1,068秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_10B/enriched_10b.json) | [\~$13\.58](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_10B/enriched_10b.json) |
| `低速 & 高コスト` | **Databricks（2X\-Small）** | [\~17,558秒（4\.9時間）](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_2X-Small_enriched.json) | [\~$13\.66](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_10B/clickbench_2X-Small_enriched.json) |


[コストパフォーマンススコア](/blog/cloud-data-warehouses-cost-performance-comparison#how-we-measure-overall-cost-performance-ranking)を見ると、分離は明白になります：


![Blog-Costs.012.png](/uploads/Blog_Costs_012_7d7df43431.png)
100億行でギャップは広がります：


- **ClickHouse Cloudは明確なリーダーであり続けます**。大きなマージンでトップのコストパフォーマンススポットを維持しています。
- **次善のシステムはすでに大きく遅れています**。ClickHouseよりも**7〜13倍悪い**です（Snowflake 4X\-L、Databricks Large、Databricks 4X\-Large）。
- **BigQuery Enterprise**はさらに後退し、約**14倍悪い**です。
- その後、すべてが長い尾に崩壊し、**数十から数百倍悪く**、Redshift Serverless（128 RPU）、Snowflake L、BigQuery On\-Demand、Snowflake X\-Small、Databricks 2X\-Smallが含まれます。



> 100億行では、経済性が急激に分岐します：ClickHouse Cloudは他のすべてのシステムよりも桁違いに優れたコストパフォーマンスを提供します。


## 1000億行：真のストレステスト [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#1000%E5%84%84%E8%A1%8C%E7%9C%9F%E3%81%AE%E3%82%B9%E3%83%88%E3%83%AC%E3%82%B9%E3%83%86%E3%82%B9%E3%83%88)


以下の[散布図](/blog/cloud-data-warehouses-cost-performance-comparison#how-to-read-the-scatter-plot-charts)は、5つのシステムそれぞれについて、1000億行のClickBench実行の合計実行時間（横軸）と合計コンピュートコスト（縦軸）を示しています。


*(前述のとおり、視覚的な明確さのために目盛りラベルを非表示にしていますが、点の位置は実際の基礎値を反映しています。上記のインタラクティブベンチマークエクスプローラーには完全な数値軸が含まれています。)*


![Blog-Costs.014.png](/uploads/Blog_Costs_014_291362ced8.png)
*(表示される構成は各エンジンの全範囲を表しています。[詳細は付録](/blog/cloud-data-warehouses-cost-performance-comparison#what-configurations-we-compare)を参照してください。**両軸は対数スケールであるため、垂直および水平のジャンプは見た目よりもさらに大きいです。**)*
1000億行では、分離は劇的になります。ClickHouse Cloudは、このスケールでも「高速 \& 低コスト」領域にしっかりとどまる唯一のシステムです。


他のすべてのエンジンは現在、「低速 \& 高コスト」にしっかりと押し込まれており、実行時間は数分から数時間の範囲で、コストは桁違いに高くなっています。




| カテゴリ | システム / ティア | 実行時間 | コスト |
| --- | --- | --- | --- |
| **ClickHouse Cloudは1000億行でも高速*かつ*低コストを維持する唯一のシステムです。効率ゾーンにある唯一のシステムです。** | | | |
| `高速 & 低コスト` | **ClickHouse Cloud** ([20ノード](https://clickhouse.com/blog/clickhouse-parallel-replicas)) | [\~275秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_100B/aws.20.236.parallel_replicas.json) | [\~$17\.62](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/clickhouse-cloud/results_100B/aws.20.236.parallel_replicas.json) |
| **他のすべてのシステムは1000億行で低速 \& 高コスト象限に入り、ClickHouseよりも遅く*、かつ*大幅に高価です。** | | | |
| `低速 & 高コスト` | **Databricks（4X\-Large）** | [\~1,049秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_100B/clickbench_4X-Large_enriched.json) | [\~$107\.69](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_100B/clickbench_4X-Large_enriched.json) |
| `低速 & 高コスト` | **Snowflake（4X\-Large）** | [\~1,212秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_100B/4xl_enriched.json) | [\~$129\.26](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_100B/4xl_enriched.json) |
| `低速 & 高コスト` | **BigQuery Enterprise（容量）** | [\~3,870秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_100B/result_enriched.json) | [\~$126\.52](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_100B/result_enriched.json) |
| `低速 & 高コスト`（チャート外） | **BigQuery On\-Demand** | [\~3,870秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_100B/result_enriched.json) | [\~$1,692\.84](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/bigquery/results_100B/result_enriched.json) |
| `低速 & 高コスト` | **Redshift Serverless（128 RPU）** | [\~5,016秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_100B/enriched_100b.json) | [\~$55\.06](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/redshift-serverless/results_100B/enriched_100b.json) |
| `低速 & 高コスト` | **Databricks（Large）** | [\~11,821秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_100B/clickbench_Large_enriched.json) | [\~$91\.94](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/databricks/results_100B/clickbench_Large_enriched.json) |
| `低速 & 高コスト` | **Snowflake（Large）** | [\~21,119秒](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_100B/large_enriched.json) | [\~$140\.80](https://github.com/ClickHouse/examples/blob/main/blog-examples/Bench2Cost/snowflake/results_100B/large_enriched.json) |


*(SnowflakeとDatabricksの最小ウェアハウスサイズはここには示されていません。1000億行では数日間実行されるため、この比較の範囲をはるかに超えています。)*


そして[コストパフォーマンススコア](/blog/cloud-data-warehouses-cost-performance-comparison#how-we-measure-overall-cost-performance-ranking)ビューは、ギャップを見逃すことを不可能にします：


![Blog-Costs.015.png](/uploads/Blog_Costs_015_a93e315273.png)
1000億行では、コストパフォーマンスのスプレッドが大幅に増加します：


- **ClickHouse Cloudは明確なリーダーであり続けます（最高の総合コストパフォーマンス）。**
- 次善のシステム、 **Databricks（4X\-Large）** は、**23倍悪い**まで落ちます。
- **Snowflake（4X\-L）**は**32倍悪い**で続きます。
- **BigQuery Enterprise、Redshift Serverless（128 RPU）、Databricks（Large）、Snowflake（L）**は**数百倍悪い**範囲に入ります。
- **BigQuery On\-Demand**はチャートの底に崩壊し、**1,350倍悪い**です。



> 私たちが**1000億行**で止めたのは、ClickHouse Cloudが限界に達したからではなく、[達していませんでした](https://clickpy.clickhouse.com/)、同じベンチマークを**1兆行**以上に押し上げることが、他のほとんどのシステムにとって**法外に高価**であるか、または数日間の実行イベントになるからです。  
>   
> 1000億では、いくつかのウェアハウスはすでに単一のClickBench実行で **$100〜$1,700**のコンピュート請求を発生させており、より小さなティアは数日間実行されます。


## 最高のコストパフォーマンスを提供するのは誰ですか？ [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E6%9C%80%E9%AB%98%E3%81%AE%E3%82%B3%E3%82%B9%E3%83%88%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%82%92%E6%8F%90%E4%BE%9B%E3%81%99%E3%82%8B%E3%81%AE%E3%81%AF%E8%AA%B0%E3%81%A7%E3%81%99%E3%81%8B)


私たちはシンプルな質問から始めました。今、データでそれに答えることができます：



> 分析ワークロードにおいて、1ドルあたり最も高いパフォーマンスを得られるのはどこか？


より大きなスケール — 100億、そして1000億行 — に押し上げると、トレンドは明白になります：すべての主要なクラウドデータウェアハウスが「低速 \& 高コスト」に向かって漂います。


**1つを除いて。**


1000億行のストレステストを含むすべてのスケールで、**ClickHouse Cloudは「高速 \& 低コスト」にとどまる唯一のシステムです**。他のすべてのシステムは遅く、高価、またはその両方になります。


  

![Blog-Costs-animation01_small.gif](/uploads/Blog_Costs_animation01_small_de9ac301cc.gif)
  


> **大規模な分析ワークロードにおいて、ClickHouse Cloudは他のすべてのシステムよりも桁違いに優れたコストパフォーマンスを提供します。**


そして、ここにキッカーがあります：SnowflakeとDatabricksはすでに、提供する最大のウェアハウスサイズで、ハードリミットに達していました。


ClickHouse Cloudにはそのような上限はありません。


私たちが20コンピュートノードで止めたのは、ClickHouse Cloudが限界に達したからではなく、結論がすでに決定的だったからです。


ベンチマークをどのように実行したかを正確に確認したい場合は、完全な方法論が以下の付録に含まれています。


  
  



## 付録：ベンチマーク方法論 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E4%BB%98%E9%8C%B2%E3%83%99%E3%83%B3%E3%83%81%E3%83%9E%E3%83%BC%E3%82%AF%E6%96%B9%E6%B3%95%E8%AB%96)


このセクションは、5つのシステムすべてでベンチマークを実行し、価格を正規化した方法の完全な詳細を提供します。


### ベンチマークセットアップ [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%83%99%E3%83%B3%E3%83%81%E3%83%9E%E3%83%BC%E3%82%AF%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97)


この分析は[ClickBench](https://benchmark.clickhouse.com/)に基づいており、**[本番環境由来の匿名化されたデータセット](https://github.com/ClickHouse/ClickBench/?tab=readme-ov-file#overview)**と**43の現実的な分析クエリ**（クリックストリーム、ログ、ダッシュボードなど）を使用しており、合成データではありません。


しかし、標準データセットは約1億行で、現在の基準では小さいです。今日のデータセットは頻繁に数十億、数兆、さらには数京で動作します。[Teslaは負荷テストのために1京行以上をClickHouseに取り込みました](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse#proving-the-system-at-scale)、そして[ClickPy](https://clickpy.clickhouse.com/)、私たちのPythonクライアントテレメトリデータセットは、すでに[2兆行](https://sql.clickhouse.com/?query=U0VMRUNUCiAgICAgICAgZm9ybWF0UmVhZGFibGVRdWFudGl0eShzdW0oY291bnQpKSBBUyB0b3RhbCwgdW5pcUV4YWN0KHByb2plY3QpIGFzIHByb2plY3RzIEZST00gcHlwaS5weXBpX2Rvd25sb2Fkcw&run_query=true)を超えています。


データが増えるにつれてコストとパフォーマンスがどのように進化するかを理解するために、**ClickBenchを10億、100億、1000億行に拡張し**、3つのスケールすべてで完全な43クエリベンチマークを再実行しました。


*結果を公正で再現可能に保つために、標準的な[ClickBenchルール](https://github.com/ClickHouse/ClickBench/?tab=readme-ov-file#overview)に従いました：チューニングなし、エンジン固有の最適化なし、最小/最大コンピュート設定の変更なし。これにより、すべての結果が、ハンドチューニングやワークロード固有のトリック（例：マテリアライズドビューで集計を事前計算）なしで、各システムが箱から出してどのように動作するかを反映することを保証します。*


互換性のない課金モデルを持つシステム間で結果を比較可能にするために、コンパニオン投稿の[Bench2Costフレームワーク](/blog/how-cloud-data-warehouses-bill-you#before-we-dive-in-how-we-calculate-costs-with-bench2cost)を使用しました。これは、生のクエリごとの実行時間を取得し、各ベンダーの実際のコンピュート価格モデルを適用し、すべてのシステム上のすべてのクエリの**実行時間とコンピュートコスト**、さらに**ストレージコストとシステムメタデータ**を含む統一されたデータセットを生成します。


### 比較する構成 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E6%AF%94%E8%BC%83%E3%81%99%E3%82%8B%E6%A7%8B%E6%88%90)


インタラクティブベンチマークエクスプローラーでは*すべての*ティアとクラスターサイズを比較できますが、この投稿では、比較をシンプルで一貫性のあるものにしています：


- **[Snowflake](/blog/how-cloud-data-warehouses-bill-you#snowflake)と[Databricks](/blog/how-cloud-data-warehouses-bill-you#databricks-sql-serverless)**：それぞれ3つのウェアハウスサイズ、**最小**、**中規模サイズ**、**最大**のEnterpriseティアサイズを含め、完全な実用的なスペクトルをカバーします。*（Snowflake固有の詳細、Gen 2ウェアハウス、QAS、新しいウェアハウスサイズについては、以下のメモを参照してください。）*
- **[ClickHouse Cloud](/blog/how-cloud-data-warehouses-bill-you#clickhouse-cloud)**：ClickHouse Cloudには固定されたウェアハウス形状がないため、「小/中/大」ティアは存在しません。代わりに、データセットサイズごとに**1つの固定されたClickHouse Cloud Enterpriseティア構成**を使用します。
- **[BigQuery](/blog/how-cloud-data-warehouses-bill-you#bigquery)**：BigQueryはチャートに2回表示されます。これは、クラスターサイズの概念を持たない完全なサーバーレスシステムですが、2つの課金モデルを提供しているためです。ワークロードを1回実行し（2000スロットのベース容量で）、その後、同じ実行時間をEnterprise（使用された**スロット容量ベース**）価格と**オンデマンド**（スキャンされたTiBあたり）価格の両方を使用して価格設定します。
- **[Redshift Serverless](/blog/how-cloud-data-warehouses-bill-you#redshift-serverless)**：Redshift Serverlessは1回表示されます。これは同様にウェアハウスサイズやティアを持たないためです。**デフォルトの128 RPUベース構成**を使用します。


すべての価格は、該当する場合、同じクラウドプロバイダーとリージョン（AWS us\-east）で取得されます。BigQueryは例外で、GCP us\-eastを使用します。


ベンダーが複数の価格ティアを提供する場合（例：Enterprise対Standard/Basic）、一貫性のためにEnterpriseティアを使用しますが、相対的なコストパフォーマンスの違いはティア間で広く同じままです。インタラクティブベンチマークエクスプローラーで代替ティアを探索することで、これを確認できます。


これにより、10億、100億、1000億行にわたって公正で、解釈可能で、一貫した比較が維持されます。


### Snowflake Gen2、QAS、新しいウェアハウスサイズ、Interactiveウェアハウスに関する注記 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#snowflake-gen2qas%E6%96%B0%E3%81%97%E3%81%84%E3%82%A6%E3%82%A7%E3%82%A2%E3%83%8F%E3%82%A6%E3%82%B9%E3%82%B5%E3%82%A4%E3%82%BAinteractive%E3%82%A6%E3%82%A7%E3%82%A2%E3%83%8F%E3%82%A6%E3%82%B9%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%B3%A8%E8%A8%98)


このベンチマークでは、**Snowflakeの標準Gen 1ウェアハウス**を使用しました。これは今日ほとんどのリージョンでデフォルトの構成のままです。


[Gen 2ウェアハウス](https://docs.snowflake.com/en/en/user-guide/warehouses-gen2)は、同じTシャツサイズで[25〜35%多くのクレジット/時間を消費](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)し、その可用性はクラウド/リージョンによって異なるため、Gen 1に焦点を当てることで、環境間で一貫した比較を維持します。


また、**SnowflakeのQuery Acceleration Service（[QAS](https://docs.snowflake.com/en/user-guide/query-acceleration-service)）を有効にしませんでした**。  

QASはウェアハウスの上に**サーバーレスバーストコンピュート**を追加し、スパイキーまたはスキャンヘビーなクエリフラグメントを加速できますが、[追加の課金ディメンションを導入する](https://docs.snowflake.com/en/user-guide/query-acceleration-service#query-acceleration-service-cost)ため、クリーンなベースライン比較を維持するために、この研究では除外しています。


Snowflakeは**4X\-Largeよりも大きいウェアハウスサイズ**も導入しました \- [具体的には](https://docs.snowflake.com/en/user-guide/warehouses-overview#warehouse-size)**5X\-Large**と**6X\-Large**です。これらは[2024年初頭に開始](https://docs.snowflake.com/en/release-notes/performance-improvements-2024)され、その後クラウド全体に拡大しましたが、4X\-Largeは最も広く使用される上位ティアのままであるため、ここでは最大サイズとして選択しました。


Snowflakeの[Interactiveウェアハウス](https://docs.snowflake.com/en/user-guide/interactive)（プレビュー）は、低レイテンシ、高同時実行ワークロードに最適化されています。これらは標準ウェアハウスよりも[1時間あたりの価格が低い](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)です（例：XSで0\.6対1クレジット/時間）が、[SELECTクエリに5秒のタイムアウトを強制](https://docs.snowflake.com/en/user-guide/interactive#limitations-of-interactive-warehouses)し、[1時間の最小課金期間](https://docs.snowflake.com/en/user-guide/interactive#cost-and-billing-considerations)を持ち、各再開は完全な最小料金をトリガーします。



> Snowflakeは多くの相互作用するパフォーマンス変数を提供します — Gen 1対Gen 2、QAS、5XL/6XLティア、Interactiveウェアハウス。最初のベンチマークでこれらを混合することを意図的に避け、比較をクリーンに保ちました。Snowflake固有のフォローアップ記事で、これらの構成を深く探索します。


### ホット対コールドランタイムに関する注記 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%83%9B%E3%83%83%E3%83%88%E5%AF%BE%E3%82%B3%E3%83%BC%E3%83%AB%E3%83%89%E3%83%A9%E3%83%B3%E3%82%BF%E3%82%A4%E3%83%A0%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%B3%A8%E8%A8%98)


ClickBenchに沿って、**ホット**ランタイムを報告します。これは3回の実行のうちの最良のものとして定義され、すべての場所でクエリ結果キャッシュを**無効にしました**。コールドスタートベンチマークは含まれていません：クラウドウェアハウスは非常に異なるデータキャッシング動作を公開し、ほとんどはOS レベルのページキャッシュのリセットやオンデマンドでのコンピュートの再起動を許可しません。コールド条件は標準化できないため、公正で再現可能な結果のいずれも生成しません。


### ネイティブストレージ形式に関する注記 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%83%8D%E3%82%A4%E3%83%86%E3%82%A3%E3%83%96%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8%E5%BD%A2%E5%BC%8F%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%B3%A8%E8%A8%98)


このベンチマークの各システムは、**そのクエリエンジンのネイティブストレージ形式**を使用して評価されます。たとえば、ClickHouse CloudのMergeTree、DatabricksのDelta Lake、Snowflakeの独自のマイクロパーティション形式、BigQueryのCapacitorカラムナーストレージです。これにより、各エンジンが設計および最適化された条件下で測定されることを保証します。


補足として、SnowflakeやClickHouse Cloudを含むいくつかのシステムは、Delta Lake、Apache Iceberg、またはApache Hudiなどのオープンテーブル形式を直接クエリすることもできます。ただし、この研究は厳密にネイティブパフォーマンスとコストに焦点を当てています。オープンテーブル形式でこれらのエンジンを比較する別のベンチマークが計画されています。お楽しみに。


### メータリング粒度に関する注記 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E3%83%A1%E3%83%BC%E3%82%BF%E3%83%AA%E3%83%B3%E3%82%B0%E7%B2%92%E5%BA%A6%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%B3%A8%E8%A8%98)


5つのシステムすべてで比較を一貫して保つために、1つの簡略化を行います：


**すべてのシステムが完璧な秒単位の粒度でコンピュートを課金しているかのように扱います。**


実際には、[コンパニオン投稿](/blog/how-cloud-data-warehouses-bill-you)で詳述されているように：


- Snowflake、Databricks、ClickHouse Cloudは、アイドルタイムアウト後にのみ課金を停止し、それぞれがウェアハウス/サービスが実行されているときに**1分間の最小料金**を持っています。
- BigQueryとRedshift Serverlessは使用を**秒単位**で計測しますが、それでも**最小料金ウィンドウ**を適用します（例：BigQueryのスロット消費の1分間最小、Redshift ServerlessのRPU使用の1分間最小）。


### 範囲と機能の違いに関する注記 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E7%AF%84%E5%9B%B2%E3%81%A8%E6%A9%9F%E8%83%BD%E3%81%AE%E9%81%95%E3%81%84%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%B3%A8%E8%A8%98)


この分析は1つの質問を見ています：



> データがスケールするにつれて、分析ワークロードを実行するのにいくらかかるか？


比較をクリーンに保つために、意図的に43クエリベンチマークの**コンピュートコストのみに焦点を当てています**。より広範なプラットフォーム機能（ガバナンス、エコシステム統合、ワークロード管理、レイクハウス機能、MLツールなど）を比較しようと**しません**。これらは間接的にベンダーがコンピュートの価格をどのように設定するかに影響を与える可能性がありますが。


### 「総合コストパフォーマンスランキング」の測定方法 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E7%B7%8F%E5%90%88%E3%82%B3%E3%82%B9%E3%83%88%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%81%AE%E6%B8%AC%E5%AE%9A%E6%96%B9%E6%B3%95)


完全に異なる課金モデルを持つシステムを比較するために、1つのシンプルでスケール独立なメトリックを使用します：


`コストパフォーマンススコア = 実行時間 × コスト`


*(小さい方が良い)*


このメトリックは、コストパフォーマンスランキングの背後にある直感を捉えています：


- **高速なシステムはより良いスコアを獲得します**
- **低コストのシステムはより良いスコアを獲得します**
- **低速または高コストのシステムはすぐに膨張します**
- **コストとランタイムは複合します**。非効率性は互いに掛け算されます


これは私たちが気にする質問に直接答えます：



> **このシステムがワークロードを完了するのにどれくらい高価か？**


すべての結果を正規化して、**最良のシステムがベースライン（1×）になり**、他のすべてのシステムは**N×悪い**として表示され、ランキングを一目で比較しやすくします。


### 散布図チャートの読み方 [\#](/jp/blog/cloud-data-warehouses-cost-performance-comparison-jp#%E6%95%A3%E5%B8%83%E5%9B%B3%E3%83%81%E3%83%A3%E3%83%BC%E3%83%88%E3%81%AE%E8%AA%AD%E3%81%BF%E6%96%B9)


上記のセクションで使用している「合計実行時間対合計コンピュートコスト」散布図の読み方に関する2つの簡単なメモ：


- **両軸は対数スケールを使用しています。** システム間の違いは、より大きなデータ量で桁違いに及ぶため、対数\-対数ビューはすべてを読みやすく保ちます。
- **プロットを一目で解釈しやすくするために、4つの象限を重ねました**（「高速 \& 低コスト」、「高速 \& 高コスト」など）。これらの象限は**純粋に視覚的**です。これらは中央値または統計的カットポイントに基づいて**いません**。読者を方向付けるシンプルな方法です。


興味深いのは、データセットが増えるにつれてシステムが象限間をどのように移動するかです。

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.
