# ClickHouse Cloudの進化：新機能、優れたパフォーマンス、そしてニーズに合わせた提供


ClickHouse Cloud は [驚異的な速さで構築](https://clickhouse.com/blog/building-clickhouse-cloud-from-scratch-in-a-year) され、2022年12月にリリースされました。リリース以来、すでに1,000社以上が当社のマネージドサービスにワークロードを移行しており、彼らは毎日合計で55億件のクエリを実行し、3500兆（3\.5 quadrillion）レコードをスキャンし、100PBのデータを扱っています。


過去2年間にわたり、私たちはユーザーと密に連携する中で貴重な知見を得てきました。継続的にフィードバックに耳を傾け、新機能をリリースすることで進化するニーズに応えています。まずは、主要なクラウドプロバイダ（AWS、GCP、Azure、AliCloud）への対応や、サポートリージョンの拡充に取り組みました。現在では[合計25のリージョン](https://clickhouse.com/docs/en/cloud/reference/supported-regions)をサポートしています。


さらに、データのオンボーディング、運用管理、アナリスト向けツールに関するタイムトゥバリュー短縮を目的とした新機能を追加してきました。いくつかの例を挙げると:


- **ClickPipes** を発表しました。これはまず [Kafka互換サービスに対応したマネージドなインジェストサービス](https://clickhouse.com/docs/en/integrations/clickpipes) から始まり、Amazon Kinesisなど他のストリーミングサービスや、[オブジェクトストレージからの継続的およびバルクロード](https://clickhouse.com/blog/s3-gcs-clickpipes-beta)にも対応しています。
- PeerDB と提携し、ClickPipes に最高水準の **チェンジデータキャプチャ (CDC)** 技術を組み込みました。最初は[Postgres向け](https://clickhouse.com/docs/en/integrations/clickpipes/postgres)にフォーカスし、今後さらなるコネクタを追加予定です。
- Arctype と連携し、GenAI（生成系AI）を活用した**SQLコンソール**を ClickHouse Cloud向けに最適化し、これをさらに拡張して[クエリAPIエンドポイント](https://clickhouse.com/docs/en/get-started/query-endpoints)や[ダッシュボード](https://clickhouse.com/docs/en/cloud/manage/dashboards)を追加しました。これらを[クラウドコンソールにネイティブ統合](https://clickhouse.com/blog/clickhouse-cloud-console-rebuilt)することで、スムーズなユーザー体験を実現しています。
- ClickHouse Cloud の強力な機能の一つである**マネージドデータベースアップグレード**をさらに強化し、変更管理と[リリースチャネル](https://clickhouse.com/docs/en/manage/updates#release-channels-upgrade-schedule)の導入に多大なリソースを投じることで、アップグレードの管理や柔軟性を高めました。
- データを自社VPCに保持したまま[完全マネージドサービスの利点を享受できる](https://clickhouse.com/docs/en/cloud/reference/byoc) **BYOC (Bring\-Your\-Own\-Cloud) デプロイオプション**をAWS向けに追加しました。


## 既存デプロイの進化 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E6%97%A2%E5%AD%98%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%81%AE%E9%80%B2%E5%8C%96)


この2年間にわたり、私たちはクラウドの構築と運用を続ける中で、ユーザーのワークロードや要求事項について多くを学びました。新機能の開発だけでなく、クラウドの基盤アーキテクチャを根本から進化させる取り組みにも注力してきました。  

2025年に向けて、これらの知見に基づいた大きなアップデートを、メインの ClickHouse Cloud に実装していきます。


### コンピュート同士の分離 (Compute\-compute separation) [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%83%88%E5%90%8C%E5%A3%AB%E3%81%AE%E5%88%86%E9%9B%A2-compute-compute-separation)


ClickHouse Cloud では、[コンピュート同士の分離](https://clickhouse.com/docs/en/cloud/reference/warehouses) をサポートするようになりました。これは複数のコンピュートレプリカが同じ基盤ストレージに同時アクセスする仕組みで、異なるワークロードに合わせてコンピュート資源を独立にスケーリングし、かつデータの重複を防ぐことが可能になります。


これにより、ワークロードごとの性能が安定し、相互干渉が少なくなります。たとえば、書き込み処理と読み取り処理、APIユーザーと人間のオペレーター、あるいは異なるタイプの利用者をそれぞれ専用のコンピュートグループに分け、リソースを制限・割り当てできます。コンピュートをグループごとに分離することで、全体的にコンピュートを過剰プロビジョニングすることなく、必要十分なサイズにできるため大幅なコスト削減も期待できます（詳細は[こちらのブログ](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud)をご覧ください）。



> "以前は8時間かかっていた処理が、今では30分以内で完了します。しかも他のサービスへの影響は目立ちません。文句なしの素晴らしい機能です！"
> 
> 
> Cypress.io


![warehouses_evolution.png](/uploads/warehouses_evolution_e72e540598.png)
### 自動スケーリングの進化 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E8%87%AA%E5%8B%95%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0%E3%81%AE%E9%80%B2%E5%8C%96)


今回、新しい垂直スケーリングの仕組みとして「make before break（MBB）」を導入しました。このアプローチでは、スケーリング操作中に古いレプリカを削除する前に、新しいサイズのレプリカを追加します。これにより、スケーリング時に処理リソースが減少することがなくなるため、実行中ワークロードへの影響を最小限に抑えることができます。特にスケールアップは高いリソース使用率をトリガーに行うため、レプリカを先に削除してしまうと負荷がさらに高くなるリスクがありますが、この方法ならそれを回避可能です。その結果、より柔軟にスケールアップ・スケールダウンのポリシーを採用し、突発的なワークロードに合わせてコンピュートリソースを自動的に最適化できるようになりました。


また、水平スケーリングに関するコントロールも導入し、APIやUIを通じてレプリカ数を変更できるようになりました。これにより、より多くの並列処理能力が必要なシナリオで、動的にコンピュート容量を増やせるようになります。


### マネージドアップグレードの改善 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%83%9E%E3%83%8D%E3%83%BC%E3%82%B8%E3%83%89%E3%82%A2%E3%83%83%E3%83%97%E3%82%B0%E3%83%AC%E3%83%BC%E3%83%89%E3%81%AE%E6%94%B9%E5%96%84)


先に触れたように、安全なマネージドアップグレードはユーザーにとって大きなメリットがあります。データベースの新機能を活用しつつ、十分にテストされた形でアップグレードを行い、万が一問題が起きればすぐにロールバックします。今回のリリースでは、アップグレードの際にも「make before break (MBB)」のアプローチを適用しました。これによって、稼働中のワークロードに対する影響をさらに軽減しています。


### さらなるデプロイパターン [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%81%95%E3%82%89%E3%81%AA%E3%82%8B%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3)


今回、新たに「シングルレプリカサービス」という概念を導入します。これはスタンドアロンのサービスとしても、またウェアハウス（warehouses）内の一要素としても利用可能です。スタンドアロンでの小規模シングルレプリカはテストワークロード向けに設計されており、新しいアイデアやプロジェクトを極めて低コストで試したい開発者にとって魅力的です。この仕組みをベースに新しい Basic（ベーシック）ティアを提供します。


一方、ウェアハウス内では、シングルレプリカでもより大きなサイズを選択でき、高可用性が要求されない（再実行が可能な）ETLジョブなどのワークロードで使えます。また、2レプリカのサービスもこれまでより幅広いスケールで使えるようになります。


### パフォーマンスと効率の向上 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%81%A8%E5%8A%B9%E7%8E%87%E3%81%AE%E5%90%91%E4%B8%8A)


私たちは、新しいデータベースバージョンをロールアウトする際に常にパフォーマンス回帰テストを行い、ユーザーの利用体験が最良となるよう努めています。過去2年間で多くの最適化を行った結果、**同じコンピュートユニットでも1\.5～2倍ほど高速かつ効率よくクエリを実行できるようになり**、ユーザーのコスト削減につながっています。


これらの改善は、多数のデータベース最適化から成り立っています。特に大きいのは、[SharedMergeTree](https://clickhouse.com/blog/clickhouse-cloud-boosts-performance-with-sharedmergetree-and-lightweight-updates) の導入です。これはクラウド環境でのストレージを最適化し、メタデータの伝播と高頻度の挿入を効率化します。さらに、一時的なローカルファイルシステムキャッシュを導入して、小規模クエリのパフォーマンスを向上させ、キャッシュ事前ウォームアップ（prewarm）機能により最新データのレプリカ間伝播を高速化し、最新データへのアクセスもスピードアップしました。非同期インサート（Asynchronous inserts）を導入したことで、さらに小さく頻繁な書き込みが可能になり、大量書き込みのための外部バッチ処理の必要性を削減しました。加えて、新しい“analyzer”をデータベースレベルに実装し、追加のクエリ最適化やクエリのパース・解釈の効率化を実現しています。


また、常に基盤ハードウェアの見直しも行い、既存ワークロードをより良い環境へ移行しています。例として、AWSではGravitonインスタンスに移行しました。エネルギー効率に優れたGravitonアーキテクチャにより、平均で25%ものパフォーマンス向上が見込まれるため、クエリ速度の向上とリソース利用の効率化が実現しました（詳細は[こちらのブログ](https://clickhouse.com/blog/graviton-boosts-clickhouse-cloud-performance)をご覧ください）。


![graviton.png](/uploads/graviton_31b36ccb30.png)
## エンタープライズ向けの新プラン「Enterprise Offering」の導入 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%97%E3%83%A9%E3%82%A4%E3%82%BA%E5%90%91%E3%81%91%E3%81%AE%E6%96%B0%E3%83%97%E3%83%A9%E3%83%B3enterprise-offering%E3%81%AE%E5%B0%8E%E5%85%A5)


私たちは、さらに厳しい要件を持つユーザー向けにエンタープライズティアを新たに提供します。業界特有のセキュリティやコンプライアンス機能、ハードウェアやアップグレードに対する制御、先進的なディザスタリカバリを主眼としています。


### 先進的なセキュリティとコンプライアンス [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E5%85%88%E9%80%B2%E7%9A%84%E3%81%AA%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E3%81%A8%E3%82%B3%E3%83%B3%E3%83%97%E3%83%A9%E3%82%A4%E3%82%A2%E3%83%B3%E3%82%B9)


オブジェクトストレージの追加保護レイヤーとして Transparent Data Encryption (TDE) をサポートし、必要に応じて Customer Managed Encryption Keys (CMEK) を変更できるようになります。これは高いプライバシーを求める組織が必須とする場合が多い機能です。さらにクラウドコンソールのシングルサインオン、業界固有のコンプライアンスとしてまずはHIPAA（今後はPCIも予定）に対応します。


### アップグレード制御の高度化 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%82%A2%E3%83%83%E3%83%97%E3%82%B0%E3%83%AC%E3%83%BC%E3%83%89%E5%88%B6%E5%BE%A1%E3%81%AE%E9%AB%98%E5%BA%A6%E5%8C%96)


リリースチャネル機能をさらに発展させ、「スケジュールされたアップグレード (scheduled upgrades)」を導入します。ユーザーは各サービスごとにアップグレードの曜日と時間帯を指定可能です。間もなく「slow」リリースチャネルも追加されます。これを使用すると、アップグレードを2週間遅らせて実行でき、重要なアップグレードの計画と準備に十分な時間を確保できるようになります。


### 高度なディザスタリカバリ [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E9%AB%98%E5%BA%A6%E3%81%AA%E3%83%87%E3%82%A3%E3%82%B6%E3%82%B9%E3%82%BF%E3%83%AA%E3%82%AB%E3%83%90%E3%83%AA)


デフォルトでは、2つ以上のレプリカを持つサービスは複数のアベイラビリティゾーンに跨ってデプロイされるため、ゾーン障害にも耐性があります。今回の拡張により、ユーザーはバックアップを自分のクラウドアカウントにエクスポートできるようになります。これにより、カスタムのディザスタリカバリポリシーを独自に実行可能です。今後はリージョン全体の障害に備えるためのクロスリージョンバックアップを計画しており、より迅速な復旧を可能にする予定です。


### ハードウェアとリージョンの高度なプロファイル [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%83%8F%E3%83%BC%E3%83%89%E3%82%A6%E3%82%A7%E3%82%A2%E3%81%A8%E3%83%AA%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AE%E9%AB%98%E5%BA%A6%E3%81%AA%E3%83%97%E3%83%AD%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)


これまでは Dedicated サービスタイプとして提供していたカスタムハードウェアプロファイルを、エンタープライズティアの機能の一部として再編します。CPU `1:8の HighMem` と、`1:2 の HighCPU` プロファイルを、デフォルトで提供している汎用（1）プロファイルに加えて利用可能にします。


また、エンタープライズティアの特典として、一般公開されていないプライベートリージョンへのアクセスも追加します。個別のリクエストに応じてサポートチームがケースバイケースで評価し、提供します。


### サポート体制の進化 [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E4%BD%93%E5%88%B6%E3%81%AE%E9%80%B2%E5%8C%96)


最後に、サポートサービスも拡充します。エンタープライズティアユーザー向けには、S1（緊急度1）の重大インシデントに対する応答時間を30分以内とする24x7のSLAを導入します。また、専任のテクニカルアカウントマネージャー（TAM）を用意し、設計のベストプラクティスやソリューションアーキテクチャ、移行、運用最適化などに関するコンサルティング支援を提供します。


## 次のステップ [\#](/jp/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings-jp#%E6%AC%A1%E3%81%AE%E3%82%B9%E3%83%86%E3%83%83%E3%83%97)


上記のエンタープライズティア導入に合わせ、従来の Development（開発）と Production（本番）ティアを再編し、進化するユーザーニーズに合わせたプラン構成とします。新しいアイデアやプロジェクトの検証に特化した Basic（ベーシック）ティアと、大規模な本番運用を対象とした Scale（スケール）ティアに分ける形です。


新規ユーザーとしてこれらの機能を試してみたい方は、[こちら](https://console.clickhouse.cloud/signUp)から300ドルの無料トライアルを開始できます。既存ユーザーの方は、製品内で表示されるガイダンスに従って既存のデプロイを新しいティアに移行できます。詳細については[こちらのFAQ](https://clickhouse.com/docs/en/cloud/manage/jan-2025-faq)をご確認ください。
