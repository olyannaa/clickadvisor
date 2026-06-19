# ClickHouseの新たな強力なJSONデータ型の開発プロセス


## はじめに [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)


[JSON](https://www.json.org/json-en.html)は現代のデータシステムで半構造化および非構造化データを扱うための共通言語となっています。ロギングや[オブザーバビリティ](https://clickhouse.com/blog/the-state-of-sql-based-observability)のシナリオ、リアルタイムデータストリーミング、モバイルアプリのストレージ、機械学習のパイプラインにおいても、JSONの柔軟な構造により、分散システム間でデータをキャプチャし送信するための共通のフォーマットとなっています。


ClickHouseでは、シームレスなJSONサポートの重要性を[認識](https://github.com/ClickHouse/ClickHouse/issues/23516)していました。しかし、JSONは単純なように見えても、大規模に効果的に活用するには独特の課題があり、それを以下に簡単に説明します。


### 課題 1: 真の列指向ストレージ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E8%AA%B2%E9%A1%8C-1-%E7%9C%9F%E3%81%AE%E5%88%97%E6%8C%87%E5%90%91%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8)


ClickHouseは [市場で最速](https://benchmark.clickhouse.com/)の[分析データベースの一つ](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf)です。そのようなパフォーマンスのレベルは、正しいデータの“オリエンテーション”でしか達成できません。ClickHouseは、テーブルをディスク上のカラムデータファイルのコレクションとして保存する[真の](https://clickhouse.com/docs/en/about-us/distinctive-features#true-column-oriented-database-management-system) [列指向データベース](https://clickhouse.com/engineering-resources/what-is-columnar-database)であり、これにより最適な [圧縮](https://clickhouse.com/docs/en/data-compression/compression-in-clickhouse) やハードウェア効率の高い、高速な[ベクトル化](https://clickhouse.com/docs/en/development/architecture)列操作（フィルターや[集計](https://clickhouse.com/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations)など）が可能になります。


JSONデータでも同じレベルのパフォーマンスを可能にするには、真の列指向ストレージをJSONに実装し、JSONパスが圧縮され、他の数値と同様に効率よく処理（フィルタリングやベクトル化された集計など）できるようにする必要がありました。


そのため、次の図に示すように、JSONドキュメントを文字列列にそのまま保存して（後で[パース](https://clickhouse.com/docs/en/sql-reference/functions/json-functions)する）というような方法は避けましょう。


![JSON-01.png](/uploads/JSON_01_1b40b01231.png)
JSONパスの各ユニークな値を真の列指向の形式で保存することを目指しました:


![JSON-02.png](/uploads/JSON_02_c5811c3a53.png)
### 課題 2: 型の統一なしに動的に変化するデータ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E8%AA%B2%E9%A1%8C-2-%E5%9E%8B%E3%81%AE%E7%B5%B1%E4%B8%80%E3%81%AA%E3%81%97%E3%81%AB%E5%8B%95%E7%9A%84%E3%81%AB%E5%A4%89%E5%8C%96%E3%81%99%E3%82%8B%E3%83%87%E3%83%BC%E3%82%BF)


JSONパスを真の列指向の方法で保存できる場合、次の課題は、JSONが同じJSONパスに対して異なるデータ型の値を許可することです。ClickHouseの場合、これらの異なるデータ型は事前に知られていない場合があり、互換性がない可能性があります。さらに、最小の共通型に統一するのではなく、すべてのデータ型を保存する方法を見つける必要がありました。たとえば、同じJSONパス`a`に値として2つの整数と1つの浮動小数点数がある場合、次の図のようにすべてを浮動小数点数としてディスクに保存したくありません:


![JSON-03.png](/uploads/JSON_03_d34ab653ae.png)
このようなアプローチは、混在する型のデータの整合性を保持せず、同じパス`a`の下に次に保存される値が配列であるような、より複雑なシナリオもサポートしないでしょう:


![JSON-04.png](/uploads/JSON_04_85b5392a1b.png)
### 課題 3: ディスク上のカラムデータファイルの雪崩の防止 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E8%AA%B2%E9%A1%8C-3-%E3%83%87%E3%82%A3%E3%82%B9%E3%82%AF%E4%B8%8A%E3%81%AE%E3%82%AB%E3%83%A9%E3%83%A0%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E9%9B%AA%E5%B4%A9%E3%81%AE%E9%98%B2%E6%AD%A2)


JSONパスを真の列指向の方法で保存することは、データ圧縮やベクトル化されたデータ処理の利点があります。しかし、多数のユニークなJSONキーが存在するシナリオでは、新しいユニークなJSONパスごとに新しいカラムファイルを作成すると、ディスク上のカラムファイルの雪崩状態に陥る可能性があります:


![JSON-05.png](/uploads/JSON_05_8c3f9a39b4.png)
これは多くの[ファイルディスクリプター](https://en.wikipedia.org/wiki/File_descriptor)（それぞれがメモリにスペースを必要とする）を必要とし、多数のファイルを処理する必要があるため、マージのパフォーマンスに影響を与え、パフォーマンスの問題を引き起こす可能性があります。そのため、カラムの作成に制限を導入する必要がありました。これにより、JSONストレージを効果的にスケーリングし、ペタバイト規模のデータセットに対する高性能な分析を保証します。


### 課題 4: 密なストレージ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E8%AA%B2%E9%A1%8C-4-%E5%AF%86%E3%81%AA%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8)


多数のユニークだがスパースなJSONキーが存在するシナリオでは、特定のJSONパスに実際の値がない行に対してNULLやデフォルト値を冗長に保存（および処理）するのを避けたいと考えました。以下の図で示すとおりです:


![JSON-06.png](/uploads/JSON_06_81504bcb8e.png)
代わりに、各ユニークなJSONパスの値を密で非冗長な方法で保存したいと考えました。これにより、JSONストレージをPBデータセットに対する高性能な分析のためにスケーリングすることができます。


### 新たに大幅に強化されたJSONデータ型 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E6%96%B0%E3%81%9F%E3%81%AB%E5%A4%A7%E5%B9%85%E3%81%AB%E5%BC%B7%E5%8C%96%E3%81%95%E3%82%8C%E3%81%9Fjson%E3%83%87%E3%83%BC%E3%82%BF%E5%9E%8B)


伝統的な実装が直面するボトルネックなくJSONデータのハイパフォーマンスな処理を提供するために新たに開発された強化型[JSONデータ型](https://clickhouse.com/docs/en/sql-reference/data-types/newjson)を発表します。


この初回の投稿では、この機能の開発にあたっての課題（および[過去の制限](https://github.com/ClickHouse/ClickHouse/issues/54864)）に対応しながら、なぜ私たちの実装が列指向ストレージの上に構築されたJSONの最高の実装であるかをお見せします。次にサポートする機能を提供します:


- 動的に変化するデータ: 同じJSONパスに対して異なるデータ型（時には互換性がなく、事前に知られていない）の値を許可し、最小の共通型に統一することなく混合型データの整合性を維持します。
- **高性能かつ密で真の列指向ストレージ**: 挿入された任意のJSONキーのパスをネイティブで密なサブカラムとして保存・読み込みし、高いデータ圧縮を可能にし、従来の型で見られるクエリ性能を維持します。
- **スケーラビリティ**: 保存されるサブカラムの数を制限することで、PBデータセットに対する高性能な分析のためにJSONストレージをスケーリングします。
- **チューニング**: JSON解析のヒント（JSONパスのための明示的な型、解析中にスキップすべきパスなど）を提供します。


この投稿の残りの部分では、JSONを超えた広範なアプリケーションを持つ基礎的なコンポーネントを最初に構築することにより、新しいJSON型の開発について説明します。


## ビルディングブロック 1 \- Variant型 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%83%93%E3%83%AB%E3%83%87%E3%82%A3%E3%83%B3%E3%82%B0%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF-1---variant%E5%9E%8B)


[Variantデータ型](https://clickhouse.com/docs/en/sql-reference/data-types/variant)は、新しいJSONデータ型を実装するための最初の構成要素です。この型はJSONの外でも使用できる完全に独立した機能として[設計](https://clickhouse.com/blog/clickhouse-release-24-01#variant-type)され、同じテーブルカラム内で異なるデータ型の値を効率的に保存（および読み取り）できます。最小の共通型に統一することはありません。これで[最初の](/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-1-true-column-oriented-storage)および[2つ目の](/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-2-dynamically-changing-data-without-type-unification)課題を解決します。


### ClickHouseにおける従来のデータ保存 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#clickhouse%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E5%BE%93%E6%9D%A5%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E4%BF%9D%E5%AD%98)


新しいVariantデータ型がない場合、ClickHouseテーブルのカラムはすべて固定型であり、挿入されるすべての値は対象のカラムの正しいデータ型であるか、必要な型に暗黙的に強制されなければなりません。


Variant型の動作をよりよく理解するための準備として、以下の図は固定データ型のカラムを持つ[MergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family)ファミリのテーブルが、ディスク上でどのようにデータを保存するか（[データパート](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#mergetree-data-storage)ごとに）を示しています:


![JSON-07.png](/uploads/JSON_07_c5da8ca64b.png)
上記の図で例示されたテーブルを再現するためのSQLコードは[こちら](https://gist.github.com/tom-clickhouse/558b82bb6e7dbb00dbbf0f669012b64a)です。各カラムにはデータ型が注釈として付けられていることに注意してください。例えば、カラム`C1`は`Int64型`です。ClickHouseは[列指向データベース](https://clickhouse.com/docs/en/faq/general/columnar-database)であるため、各テーブルカラムの値はディスク上で別々に（高度に[圧縮](https://clickhouse.com/docs/en/data-compression/compression-in-clickhouse)された）カラムファイルに保存されます。カラム`C2`が[Nullable](https://clickhouse.com/docs/en/sql-reference/data-types/nullable)であるため、ClickHouseはNULLマスクを保持する別のファイルを[使用](https://clickhouse.com/docs/en/sql-reference/data-types/nullable#storage-features)し、通常のカラムファイルに加えてNULLと空（デフォルト）値を区別するために用います。テーブルカラム`C3`については、ClickHouseがどのように[配列](https://clickhouse.com/docs/en/sql-reference/data-types/array)を保存することをネイティブにサポートしているかを示しており、各テーブル行の配列のサイズをディスク上の別のファイルで保存しています。これらのサイズ値は、データファイル内の配列要素にアクセスするための対応するオフセットを計算するために使用されます。


### 動的に変化するデータのためのストレージ拡張 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E5%8B%95%E7%9A%84%E3%81%AB%E5%A4%89%E5%8C%96%E3%81%99%E3%82%8B%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8%E6%8B%A1%E5%BC%B5)


新しいVariantデータ型を使用すると、上記のテーブルのすべてのカラムからのすべての値を単一のカラムに保存できます。次の図は、クリックして拡大すると、そのカラムがどのように機能し、ClickHouseの列指向ストレージを基にディスク上でどのように実装されているか（データパートごとに）をスケッチしています:


[![](/uploads/JSON_08_c04e3510ad.png)](/uploads/JSON_08_c04e3510ad.png)


図に示す例のテーブルを再現するためのSQLコードは[こちら](https://gist.github.com/tom-clickhouse/c4f3da235843252b7b5c38472bdeba5d)です。この例では、ClickHouseのテーブル列`C`に対してVariant型を指定しました。これにより、列`C`に整数、文字列、整数の配列を混在して格納できるようになります。このようなカラムに対して、ClickHouseは同じデータ型のすべての値を別々のサブカラムに保存します（Variant型のカラムデータファイルで、それ自体は[前の](/blog/a-new-powerful-json-data-type-for-clickhouse#traditional-data-storage-in-clickhouse)例のカラムデータファイルとほぼ同一に見えます）。例えば、すべての整数値は`C.Int64 .bin`ファイルに保存され、すべての文字列値は`C.String .bin`に保存され、そして他の型も同様です。


### サブタイプ間の切り替えのための識別子カラム [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%B5%E3%83%96%E3%82%BF%E3%82%A4%E3%83%97%E9%96%93%E3%81%AE%E5%88%87%E3%82%8A%E6%9B%BF%E3%81%88%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E8%AD%98%E5%88%A5%E5%AD%90%E3%82%AB%E3%83%A9%E3%83%A0)


ClickHouseテーブルの各行で使用されているタイプを知るために、ClickHouseは各データタイプに識別子を割り当て、これらの識別子を含む追加の(`UInt8`)カラムデータファイル（上図の`C.variant_discr.bin`）を保存します。各discriminator値は、ソートされた使用タイプ名のリストへのインデックスを表します。discriminator 255は`NULL`値用に予約されており、これは設計上、Variantが最大255の異なる具体的なタイプを持つことができることを意味します。


特に注意すべきは、[NULLマスクファイル](/blog/a-new-powerful-json-data-type-for-clickhouse#traditional-data-storage-in-clickhouse)を別途持つ必要がなく、NULLとデフォルトの値を区別することです。


さらに、[識別子のコンパクトなシリアル化形式](/blog/a-new-powerful-json-data-type-for-clickhouse#one-more-detail---compact-discriminator-serialization)が存在し、（典型的なJSONシナリオに最適化するために）特別な形式が用意されています。


### 密なデータストレージ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E5%AF%86%E3%81%AA%E3%83%87%E3%83%BC%E3%82%BF%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8)


Variantタイプのカラムデータファイルは密です。これらのファイルに`NULL`値を保存しません。多くのユニークだがスパースなJSONキーが存在するシナリオでは、特定のJSONパスに対して実際の値がない行に対してデフォルト値を保存しません（[この](/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-4-dense-storage)図で示されている反例として）。これで、[第4の](/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-4-dense-storage)課題を解決します。


この密なVariant型のストレージのため、識別子カラムの行を対応するVariant型のカラムデータファイルの行にマッピングする必要もあります。この目的のために、`UInt64`オフセットカラム（上図の`offsets`）が存在し、メモリ上にしか存在しないが（識別子カラムファイルから動的に作成可能）、ディスクには保存されません。


例えば、上図のClickHouseテーブルの行6の値を取得するために、ClickHouseは識別子カラムの行6を検査して要求された値を含むVariant型カラムデータファイル`C.Int64 .bin`を特定します。さらに、ClickHouseはoffsetsファイルの行6を調べて、`C.Int64 .bin`ファイル内の要求された値の具体的な`offsets`を知っています。そのため、ClickHouseテーブルの行6の要求値は44です。


### Variant型の任意のネスト [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#variant%E5%9E%8B%E3%81%AE%E4%BB%BB%E6%84%8F%E3%81%AE%E3%83%8D%E3%82%B9%E3%83%88)


Variantカラム内にネストされる型の順序は関係ありません: `Variant(T1, T2)` \= `Variant(T2, T1)`です。さらに、Variant型は任意のネストを許可し、Variant内で使われるVariant型の1つとしてVariant型を使用できます。別の図を用いて（クリックして拡大可能）、これを示します:


[![](/uploads/JSON_09_ceb9570915.png)](/uploads/JSON_09_ceb9570915.png)


この図に示された例のテーブルを複製するためのSQLコードは[こちら](https://gist.github.com/tom-clickhouse/56b56271239eb2b7c9a8ca970f62611f)です。今回は、Variantカラム`C`を使用して、整数、文字列、Variant値を含む配列のミックスを格納することを指定しました。上の図は、ClickHouseが内部で、上記で説明したVariantストレージのアプローチをどのように配列カラムデータファイル内にネストして、ネストされたVariant型を実現しているかをスケッチしています。


### サブカラムとしてのVariantネスト型の読み取り [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%B5%E3%83%96%E3%82%AB%E3%83%A9%E3%83%A0%E3%81%A8%E3%81%97%E3%81%A6%E3%81%AEvariant%E3%83%8D%E3%82%B9%E3%83%88%E5%9E%8B%E3%81%AE%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A)


Variant型は、サブカラムとして型名を使用してVariantカラムから単一のネスト型の値を読み取ることを[サポート](https://clickhouse.com/docs/en/sql-reference/data-types/variant#reading-variant-nested-types-as-subcolumns)します。たとえば、上記のテーブルの`C`サブカラムの`Int64`型のすべての整数値を`C.Int64`という構文を使用して読み取ることができます:



```
SELECT C.Int64
FROM test;

   ┌─C.Int64─┐
1. │      42 │
2. │    ᴺᵁᴸᴸ │
3. │    ᴺᵁᴸᴸ │
4. │      43 │
5. │    ᴺᵁᴸᴸ │
6. │    ᴺᵁᴸᴸ │
7. │      44 │
8. │    ᴺᵁᴸᴸ │
9. │    ᴺᵁᴸᴸ │
   └─────────┘

```

## ビルディングブロック 2 \- Dynamic型 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%83%93%E3%83%AB%E3%83%87%E3%82%A3%E3%83%B3%E3%82%B0%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF-2---dynamic%E5%9E%8B)


Variant型の後には、Dynamic型の実装が続きます。この[Dynamic](https://clickhouse.com/docs/en/sql-reference/data-types/dynamic)型は、JSONコンテキストの外でも単独で使用できる[独自の特長を持つ機能](https://clickhouse.com/blog/clickhouse-release-24-05#dynamic-data-type)として実装されています。


Dynamic型はVariant型の強化版と見なされ、2つの重要な新機能を導入します:


1. 単一のテーブルカラム内に任意のデータ型の値を保存し、すべての型を事前に知って指定する必要はありません。
2. サブカラムデータファイルとして保存される型の数を制限する可能性。これにより、[部分的に](/blog/a-new-powerful-json-data-type-for-clickhouse#preventing-an-avalanche-of-column-files)3番目の課題である[ディスク上のカラムデータファイルの雪崩現象](/blog/a-new-powerful-json-data-type-for-clickhouse#storage-extension-for-dynamically-changing-data)を解決します。


次にこれら2つの新機能について簡単に説明します。


### サブタイプを指定する必要はありません [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%B5%E3%83%96%E3%82%BF%E3%82%A4%E3%83%97%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%99%E3%82%8B%E5%BF%85%E8%A6%81%E3%81%AF%E3%81%82%E3%82%8A%E3%81%BE%E3%81%9B%E3%82%93)


次の図は、クリックして拡大可能で、単一のDynamicカラムを持つClickHouseテーブルとそのディスク上の保存方法（データパートごとに）を示しています:


[![](/uploads/JSON_10_92f1907815.png)](/uploads/JSON_10_92f1907815.png)


この図に示されるテーブルを再現するためのSQLコードは[こちら](https://gist.github.com/tom-clickhouse/cba68ca35a5926d2145a186bec695d73)です。Dynamicカラム`C`には、Variant型で行うように、事前に型を指定せずに任意の型の値を挿入できます。


内部的に、DynamicカラムはVariantカラムと[同様](/blog/a-new-powerful-json-data-type-for-clickhouse#storage-extension-for-dynamically-changing-data)にディスク上にデータを保存し、特に構造に関する追加情報を保持します。図は、保存方法の差異を示しており、Dynamicカラムがサブカラムと保存するための`C.dynamic_structure.bin`という追加のファイルを持ち、保存された型のリストとそのVariant型カラムデータファイルのサイズの統計を含んでいることを示しています。このメタデータは、サブカラムの読み取りとデータパートのマージに使用されます。


### カラムファイルの雪崩を防ぐ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%AB%E3%83%A9%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E9%9B%AA%E5%B4%A9%E3%82%92%E9%98%B2%E3%81%90)


Dynamic型は、型定義で`max_types`パラメータを指定することで、サブカラムデータファイルとして保存される型の数を制限することもサポートしています: `Dynamic(max_types=N)`ここで0\<\= N \<255。`max_types`のデフォルト値は32です。この制限が達成されると、残りのすべての型は特別な構造を持つ単一のカラムデータファイルに保存されます。次の図でその例を示しています（クリックして拡大可能）:


[![](/uploads/JSON_11_c3698916bb.png)](/uploads/JSON_11_c3698916bb.png)


上記の図に示された例のテーブルを生成するためのSQLスクリプトは[こちら](https://gist.github.com/tom-clickhouse/c30b287d0a4a514b1019fcbed1584467)です。今回は、max\_typesパラメータを3に設定したDynamicカラムCを使用します。


したがって、最初の3つの使用タイプのみが個別のカラムデータファイルに保存されます（これは圧縮と分析クエリに効率的です）。さらに使用される追加のタイプ（上の例のテーブルで緑色でハイライトされている部分）からのすべての値は、`String`タイプを持つ単一のカラムデータファイル（`C.SharedVariant.bin`）にまとめて保存されます。SharedVariantの各行には、以下のデータを含む文字列値が含まれています：\<[binary\_encoded\_data\_type](https://clickhouse.com/docs/en/sql-reference/data-types/data-types-binary-encoding)\>\<binary\_value\>。この構造を使用することで、単一のカラム内に異なるタイプの値を保存（および取得）することができます。


### サブカラムとしてダイナミックネスト型の読み取り [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%B5%E3%83%96%E3%82%AB%E3%83%A9%E3%83%A0%E3%81%A8%E3%81%97%E3%81%A6%E3%83%80%E3%82%A4%E3%83%8A%E3%83%9F%E3%83%83%E3%82%AF%E3%83%8D%E3%82%B9%E3%83%88%E5%9E%8B%E3%81%AE%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A)


Variant型と同様に、Dynamic型は[サポート](https://clickhouse.com/docs/en/sql-reference/data-types/dynamic#reading-dynamic-nested-types-as-subcolumns)しており、Dynamicカラムから特定のネストされた型の値をサブカラムとして読み取ることができます。型名を使用します：



```
SELECT C.Int64
FROM test;

   ┌─C.Int64─┐
1. │      42 │
2. │    ᴺᵁᴸᴸ │
3. │    ᴺᵁᴸᴸ │
4. │      43 │
5. │    ᴺᵁᴸᴸ │
6. │    ᴺᵁᴸᴸ │
7. │      44 │
8. │    ᴺᵁᴸᴸ │
9. │    ᴺᵁᴸᴸ │
   └─────────┘

```

## ClickHouse JSON型: すべてをひとつにまとめる [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#clickhouse-json%E5%9E%8B-%E3%81%99%E3%81%B9%E3%81%A6%E3%82%92%E3%81%B2%E3%81%A8%E3%81%A4%E3%81%AB%E3%81%BE%E3%81%A8%E3%82%81%E3%82%8B)


VariantおよびDynamic型の実装後、ClickHouseの列指向ストレージ上に新たな強力なJSON型を実装するために必要なすべての構成要素が揃い、[課題](/blog/a-new-powerful-json-data-type-for-clickhouse#introduction)を克服するためのサポートが整いました：


- **動的に変化するデータ:** 同じJSONパスに対して異なるデータ型（時には互換性がない場合や事前に判明しない場合もある）の値を許可し、型の統一なしに混合型データの整合性を保ちます。
- **高性能で密度が高い、真の列指向ストレージ:** ネイティブで密度のあるサブカラムとして挿入されたJSONキーを保存および読み取り、高いデータ圧縮と従来の型で見られたクエリ性能を維持します。
- **スケーラビリティ:** 個別に保存されるサブカラムの数を制限することができ、PBデータセットに対する高性能分析のためのJSONストレージをスケールします。
- **チューニング:** JSON解析のヒント（JSONパスの明示的な型、解析時にスキップされるべきパスなど）を許可します。


新しい[JSON型](https://clickhouse.com/docs/en/sql-reference/data-types/newjson)は、任意の構造を持つJSONオブジェクトの保存を可能にし、JSONパスをサブカラムとして使用してその中のすべてのJSON値を読み取ることができます。


### JSON型の宣言 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#json%E5%9E%8B%E3%81%AE%E5%AE%A3%E8%A8%80)


新しい型には、いくつかのオプションパラメータとヒントが宣言に含まれています：



```
<column_name> JSON(
  max_dynamic_paths=N, 
  max_dynamic_types=M, 
  some.path TypeName, 
  SKIP path.to.skip, 
  SKIP REGEXP 'paths_regexp')

```

ここで：


- `max_dynamic_paths`（デフォルト値`1024`）は、サブカラムとして個別に保存されるJSONキーパスの数を指定します。この制限を超えた場合、他のすべてのパスは特殊な構造を持つ単一のサブカラムにまとめて保存されます。
- `max_dynamic_types`（デフォルト値`32`）は`0`から`254`の間の値で、`Dynamic`型を持つ単一のJSONキーパスカラムに対して、個別のカラムデータファイルとして保存される異なるデータタイプの数を指定します。この制限を超えた場合、新しいタイプはすべて特殊な構造を持つ単一のカラムデータファイルにまとめて保存されます。
- `some.path TypeName`は特定のJSONパスに対するタイプヒントです。このようなパスは常に指定された型のサブカラムとして保存され、パフォーマンスが保証されます。
- `SKIP path.to.skip`はJSON解析中にスキップすべき特定のJSONパスに対するヒントです。このようなパスはJSONカラムに保存されることはありません。指定されたパスがネストされたJSONオブジェクトの場合、ネストされたオブジェクト全体がスキップされます。
- `SKIP REGEXP 'path_regexp`はJSON解析中にパスをスキップするために使用される正規表現を含むヒントです。この正規表現にマッチするすべてのパスはJSONカラムに保存されることはありません。


### 真の列指向JSONストレージ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E7%9C%9F%E3%81%AE%E5%88%97%E6%8C%87%E5%90%91json%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8)


以下の図（クリックすると拡大表示できます）は、単一のJSONカラムを持つClickHouseテーブルとそのカラムのJSONデータがClickHouseの列指向ストレージ上でどのように効率的に実装されているかを示しています（各データパートあたり）：


[![](/uploads/JSON_12_f4326293fb.png)](/uploads/JSON_12_f4326293fb.png)


以下のSQLコードを[使用して](https://gist.github.com/tom-clickhouse/c52ab757aca15723427032f305c73656)、上の図で示されるようにテーブルを再作成します。我々の例のテーブルのカラム`C`は`JSON`型で、JSONパス`a.b`と`a.c`の型を指定する2つの型ヒントを提供しました。


私たちのテーブルカラムには6つのJSONドキュメントが含まれており、それぞれのユニークなJSONキーのパスの葉の値は、通常のカラムデータファイルとして（型付きJSONパス、型ヒント付きパスの場合、図の`C.a.b`や`C.a.c`を参照）または動的サブカラムとして（動的JSONパス、データが動的に変化する可能性のあるパスの場合、図の`C.a.d`、`C.a.d.e`、`C.a.e`を参照）、ディスクに保存されます。後者の場合、ClickHouseは[動的データ型](/blog/a-new-powerful-json-data-type-for-clickhouse#building-block-2---dynamic-type)を使用します。


加えて、JSON型は動的パスに関するメタデータ情報や各動的パスの非NULL値の統計（カラムシリアル化時に計算される）を含む特別なファイル（`object_structure`）を使用しています。このメタデータはサブカラムの読み取りとデータパーツのマージに使用されます。


### カラムファイルの雪崩を防ぐ [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%AB%E3%83%A9%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E9%9B%AA%E5%B4%A9%E3%82%92%E9%98%B2%E3%81%90-1)


1つのJSONキーのパス内で動的型が多く存在するシナリオや、動的JSONキーのユニークなパスが大量に存在するシナリオでディスク上に多くのカラムファイルが爆発的に増加するのを防ぐために、JSON型は以下を許可しています：


(1\) 単一のJSONキーのパスに対してどれだけ多くの異なるデータ型が個別のカラムデータファイルとして保存されるかを`max_dynamic_types`（デフォルト値`32`）パラメータで制限する。


(2\) JSONキーのパスがサブカラムとして個別に保存される数を`max_dynamic_paths`（デフォルト値`1024`）パラメータで制限する。


これが[第三](/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-3-prevention-of-avalanche-of-column-data-files-on-disk)の課題を解決するものです。


(1\)の例は[上記](/blog/a-new-powerful-json-data-type-for-clickhouse#preventing-column-file-avalanche)に示されています。そして、(2\)については、他の図を使用して示します（クリックすると拡大表示できます）：


[![](/uploads/JSON_13_846ce6ca7c.png)](/uploads/JSON_13_846ce6ca7c.png)


この図のテーブルを再現するためのSQLコードは[こちら](https://gist.github.com/tom-clickhouse/c02b49fc5ec275aaa6e9d463311048ba)です。前の例と同様に、私たちのClickHouseテーブルのカラム`C`は`JSON`型で、JSONパス`a.b`と`a.c`の型を指定する同じ2つの型ヒントを提供しました。


さらに、`max_dynamic_paths`パラメータを3に設定しました。これにより、ClickHouseは最初の3つの動的JSONパスの葉の値のみを動的サブカラムとして保存します（Dynamic型を使用する）。


追加の動的JSONパスは、それらの型情報と値（上の例のテーブルで緑色でハイライトされている部分）がすべて共有データとして保存されます \- 上図の`C.object_shared_data.size0.bin`、`C.object_shared_data.paths.bin`、`C.object_shared_data.values.bin`ファイルを参照してください。共有データファイル（`object_shared_data.values`）は`String`型であることに注意してください。各エントリは、以下のデータを含む文字列値です：\<[binary\_encoded\_data\_type](https://clickhouse.com/docs/en/sql-reference/data-types/data-types-binary-encoding)\>\<binary\_value\>。


共有データと共に、サブカラムの読み取りやデータパーツのマージに使用される追加の統計情報を`object_structure.bin`ファイルに保存します。共有データカラムに保存されている（現在のところ最初の10000の）パスの非NULL値に関する統計を保存しています。


### JSONパスの読み取り [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#json%E3%83%91%E3%82%B9%E3%81%AE%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A)


JSON型は、パス名をサブカラムとして使用して、各パスのリーフ値を読み取ることを[サポート](https://clickhouse.com/docs/en/sql-reference/data-types/newjson#reading-json-paths-as-subcolumns)しています。たとえば、上記の例でJSONパス`a.b`のすべての値を`C.a.b`という文法で読み取れます：



```
SELECT C.a.b
FROM test;

   ┌─C.a.b─┐
1. │    10 │
2. │    20 │
3. │    30 │
4. │    40 │
5. │    50 │
6. │    60 │
   └───────┘

```

要求されたパスの型がJSON型の宣言で型ヒントによって指定されていない場合、そのパスの値は常にDynamic型を持ちます：



```
SELECT
    C.a.d,
    toTypeName(C.a.d)
FROM test;

   ┌─C.a.d───┬─toTypeName(C.a.d)─┐
1. │ 42      │ Dynamic           │
2. │ 43      │ Dynamic           │
3. │ ᴺᵁᴸᴸ    │ Dynamic           │
4. │ foo     │ Dynamic           │
5. │ [23,24] │ Dynamic           │
6. │ ᴺᵁᴸᴸ    │ Dynamic           │
   └─────────┴───────────────────┘

```

また、特別なJSON構文`JSON_column.some.path.:TypeName`を使用してDynamic型のサブカラムを読み取ることも可能です：



```
SELECT C.a.d.:Int64
FROM test;


   ┌─C.a.d.:`Int64`─┐
1. │             42 │
2. │             43 │
3. │           ᴺᵁᴸᴸ │
4. │           ᴺᵁᴸᴸ │
5. │           ᴺᵁᴸᴸ │
6. │           ᴺᵁᴸᴸ │
   └────────────────┘

```

さらに、JSON型はサポートしており、特別な構文`JSON_column.^some.path`を使用して、JSON型でネストされたJSONオブジェクトをサブカラムとして読み取ることができます：



```
SELECT C.^a
FROM test;

┌─C.^`a`───────────────────────────────────────┐
1. │ {"b":10,"c":"str1","d":"42"}                 │
2. │ {"b":20,"c":"str2","d":"43"}                 │
3. │ {"b":30,"c":"str3","e":"44"}                 │
4. │ {"b":40,"c":"str4","d":"foo","e":"baz"}      │
5. │ {"b":50,"c":"str5","d":["23","24"]}          │
6. │ {"b":60,"c":"str6","d":{"e":"bar"},"e":"45"} │
└──────────────────────────────────────────────┘

```


```
SELECT toTypeName(C.^a)
FROM test
LIMIT 1;

   ┌─toTypeName(C.^`a`)───────┐
1. │ JSON(b UInt32, c String) │
   └──────────────────────────┘

```


> 現時点では、ドット構文はパフォーマンス上の理由でネストされたオブジェクトを読み取りません。データはパスごとにリテラル値を非常に効率的に読み取れるように保存されていますが、パスごとにすべてのサブオブジェクトを読み取るには、より多くのデータを読み込む必要があり、時には遅くなることもあります。したがって、オブジェクトを返したい場合には、代わりに.^を使用する必要があります。現在、２つの異なる`.`構文を統一する[計画](https://github.com/ClickHouse/ClickHouse/issues/68428)をしています。


## もう一つの詳細 \- コンパクトなディスクリミネータのシリアル化 [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%82%82%E3%81%86%E4%B8%80%E3%81%A4%E3%81%AE%E8%A9%B3%E7%B4%B0---%E3%82%B3%E3%83%B3%E3%83%91%E3%82%AF%E3%83%88%E3%81%AA%E3%83%87%E3%82%A3%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%9F%E3%83%8D%E3%83%BC%E3%82%BF%E3%81%AE%E3%82%B7%E3%83%AA%E3%82%A2%E3%83%AB%E5%8C%96)


多くのシナリオでは、動的なJSONパスはほとんど同じ型の値を持つことがあります。この場合、Dynamic型の[ディスクリミネータファイル](/blog/a-new-powerful-json-data-type-for-clickhouse#discriminator-column-for-switching-between-subtypes)には主に同じ数（型ディスクリミネータ）が含まれることになります。


同様に、多くのユニークでスパースなJSONパスを保存する場合、それぞれのパスのディスクリミネータファイルには主に値255（NULL値を示す）が含まれることになります。


両方の場合においてディスクリミネータファイルは十分に圧縮されますが、すべての行が同じ値を持つ場合にはかなり冗長になる可能性があります。


これを最適化するために、ディスクリミネータのシリアル化の特別なコンパクト形式を実装しました。[通常の](/blog/a-new-powerful-json-data-type-for-clickhouse#discriminator-column-for-switching-between-subtypes)`UInt8`値としてディスクリミネータを記述する代わりに、[ターゲットグラニュール](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-organized-into-granules-for-parallel-data-processing)内ですべてのディスクリミネータが同じ場合、3つの値のみをシリアル化します ([8192](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings#index_granularity) 値の代わりに):


1. コンパクトグラニュールフォーマットのインジケータ
2. このグラニュール内の値の数のインジケータ
3. ディスクリミネータ値


この最適化は、MergeTreeの設定`use_compact_variant_discriminators_serialization`（デフォルトで有効）によって制御できます。


## ここからが始まりです [\#](/jp/blog/a-new-powerful-json-data-type-for-clickhouse-jp#%E3%81%93%E3%81%93%E3%81%8B%E3%82%89%E3%81%8C%E5%A7%8B%E3%81%BE%E3%82%8A%E3%81%A7%E3%81%99)


この記事では、JSONの基礎的な構成要素を最初に作成することで、私たちの新しいJSON型をゼロからどのように開発したかを概説しました。


この新しいJSON型は、現在は非推奨となった[Object('json')](https://clickhouse.com/docs/en/sql-reference/data-types/object-data-type)データ型を置き換えることを目的として設計されており、その制限を克服し、全体的な機能性を改善しています。


新しい実装は現在、テスト目的で[リリース](https://clickhouse.com/blog/clickhouse-release-24-08#json-data-type)されており、機能セットはまだ完成していません。私たちの[JSONロードマップ](https://github.com/ClickHouse/ClickHouse/issues/68428)には、テーブルの主キーやデータスキッピングインデックス内でJSONキーパスを使用するなど、いくつかの強力な機能拡張が含まれています。


また、新しいJSONタイプを実装するために作成した基盤ブロックは、ClickHouseがXML、YAML、その他の半構造化タイプをサポートするための道を開きました。


今後の投稿では、実際のデータを使用して新しいJSONタイプの主要なクエリ機能を紹介し、データ圧縮とクエリパフォーマンスのベンチマークを示します。また、JSONの実装の内部動作についても詳しく説明し、データがメモリ内でどのように効率的にマージされ処理されるかを解説します。


ClickHouse Cloudを使用していて、新しいJSONデータタイプをテストしたい場合は、プライベートプレビューを有効にするために[サポートにご連絡](https://clickhouse.com/docs/en/cloud/support)ください。
