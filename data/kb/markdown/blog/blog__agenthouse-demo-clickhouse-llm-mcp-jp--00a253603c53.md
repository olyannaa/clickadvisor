# AgentHouseのご紹介


![Blog_IntroducingAgentHouse_202504_FNL.png](/uploads/Blog_Introducing_Agent_House_202504_FNL_0639a4c186.png)
## AgentHouseのご紹介 [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#agenthouse%E3%81%AE%E3%81%94%E7%B4%B9%E4%BB%8B)


2024年にAnthropic社が[MCPプロトコル](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)をリリースしてから数週間後、ClickHouseの統合チームは、Anthropic社のSonnetモデルがClickHouseデータベースにアクセスする小規模な社内デモを披露しました。これは、ランダムなデータに対して単純なクエリを実行し、LLMに結果を返すという非常に基本的な統合でした。


ClickHouseの社内DWHチームリーダーとして、そのデモを見た私はすぐにこれを[私のデータウェアハウス](https://clickhouse.com/blog/building-a-data-warehouse-with-clickhouse)に導入したいと思いました。ClickHouseの素晴らしい社内ユーザー（営業、運用、製品、財務、エンジニアリングの各チーム）には、従来のBIツールを使ったりクエリを実行したりする代わりに、データと対話できるようになってほしいのです。


2ヶ月後、私たちはDwaine（Data Warehouse AI Natural Expert）を立ち上げました。これは、社内ユーザーがデータに基づいて質問に答えるのを支援する社内LLMです。「私たちの収益は？」「この顧客は何をしているのか？」「顧客は今どんな問題に直面しているのか？」「ウェブサイトの訪問者数は？コンバージョン率は？」Dwaineは、社内ユーザーがこれらの洞察やその他の情報を得るのに劇的に役立ちました。[LinkedInでの私の小さな個人的な記事](https://www.linkedin.com/pulse/bi-dead-change-my-mind-dmitry-pavlov-2otae)をご覧になった方もいるかもしれません。


この経験を説明した後、多くの人々が私に連絡を取り、デモを依頼してきました。数人の友人やパートナーにDwaineを実演しましたが、彼らは非常に興奮していたものの、機密情報を扱っていたためDwaineと直接対話することができず、その可能性を十分に体験できていないと感じました。


このようにして、[llm.clickhouse.com](https://llm.clickhouse.com)で利用可能なAgentHouseが構築されました。しかし、彼に自己紹介をしてもらいましょう :) これ以降のテキストは、AgentHouse LLMによって書かれています。


## こんにちは、AgentHouseです！ [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%81%AFagenthouse%E3%81%A7%E3%81%99)


私は[AgentHouse](https://llm.clickhouse.com)です。ClickHouseのリアルタイム分析能力と大規模言語モデルの強力な組み合わせを紹介する、完全に対話型のデモ環境です。私の名前は「Agent」（LLMエージェントを表す）と「House」（ClickHouseから）を組み合わせたもので、これらのテクノロジーがどのようにシームレスに連携するかを強調しています。他のデモ環境（[ClickHouse SQL Playground](http://sql.clickhouse.com)および[ADSBビジュアライザー](https://adsb.exposed/)）と共に、アカウントを作成したりデータをアップロードしたりすることなく、さまざまな実際のシナリオでClickHouse Cloudデータベースを試すことができます。


![agenthouse.gif](/uploads/agent_house_v3_7e163b96ca.gif)
## 私の構成要素は何ですか？ [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E7%A7%81%E3%81%AE%E6%A7%8B%E6%88%90%E8%A6%81%E7%B4%A0%E3%81%AF%E4%BD%95%E3%81%A7%E3%81%99%E3%81%8B)


これらが私の主要な構成要素です。


1. **[Anthropicの大規模言語モデル Claude Sonnet](https://www.anthropic.com/claude/sonnet)** \- このLLMは、複雑なコンテキストの理解と構造化データに関する推論に特に優れており、ClickHouseの分析能力にとって理想的なパートナーです。データベーススキーマを理解し、正確なSQLを生成し、クエリ結果を解釈するモデルの能力は、ClickHouseと高度なLLMがなぜ自然な組み合わせであるかを示しています。
2. **[LibreChat UIプロジェクト](https://www.librechat.ai)** \- 人気のあるLLMをすぐに利用できるオープンソースのLLM UIです。オープンソースであること、クリーンなデザイン、そして成長するコミュニティサポートのため、ユーザーインターフェースとしてLibreChatを選択しました。また、このデモの構築にご協力いただいたLibreСhatチームにも感謝いたします。
3. 私の秘密のソースは、ClickHouseチームが開発した **[ClickHouse MCP](https://github.com/ClickHouse/mcp-clickhouse)**（Model Context Protocol）サーバーです。この専用サーバーは、ClickHouseデータベースと大規模言語モデルの間の橋渡しとして機能し、以下を可能にします。


- ClickHouseとLLM間の効率的なデータ転送
- LLMが生成したSQLのインテリジェントなクエリ最適化
- データに関するステートフルな会話のためのコンテキスト管理
- データベースリソースへの安全で制御されたアクセス
- さまざまな公開データセットの合理化された処理


4. **[ClickHouse Cloudデータベース](https://clickhouse.com)** \- ClickHouseデータベースをSaaS（Software\-as\-a\-Service）として提供するフルマネージドのクラウドサービスです。


![Images_PoweringAIAgentsAnalytics_202504_FNL(1).png](/uploads/Images_Powering_AI_Agents_Analytics_202504_FNL_1_54be5a6747.png)
## なぜSonnetとLibreChatなのですか？ [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E3%81%AA%E3%81%9Csonnet%E3%81%A8librechat%E3%81%AA%E3%81%AE%E3%81%A7%E3%81%99%E3%81%8B)


AnthropicのSonnetモデルは、LLMの能力、特に複雑なコンテキストの理解と構造化データに関する推論において大きな進歩を示しており、ClickHouseの分析能力にとって理想的なパートナーです。データベーススキーマを理解し、正確なSQLを生成し、クエリ結果を解釈するモデルの能力は、ClickHouseと高度なLLMがなぜ自然な組み合わせであるかを示しています。


オープンソースであること、クリーンなデザイン、そして成長するコミュニティサポートのため、ユーザーインターフェースとしてLibreChatを使用しています。このインターフェースにより、ユーザーはデータについて自然な会話をしたり、視覚的な成果物（チャート、テーブルなど）を作成したりすることができ、SQLの知識がない人でも複雑な分析タスクにアクセスできるようになります。


## 私の目的 [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E7%A7%81%E3%81%AE%E7%9B%AE%E7%9A%84)



私は、ユーザーがMCPサーバーを介してClickHouseがLLMアプリケーションの理想的なバックエンドとしてどのように機能するかを試すためのテストグラウンドとして特別に作成されました😉。さまざまなユースケースを紹介する複数の公開データセットにアクセスでき、簡単な会話型インターフェースを通じて可能性を探ることができます。これには、以下を含む37の異なるデータセットが含まれます。



- **github** \- GitHubのアクティビティデータ、リポジトリ、ユーザーインタラクションが含まれています。毎時更新されます。
- **pypi** \- `pip`でダウンロードされたすべてのPythonパッケージの行が含まれ、毎日更新されます \- 1\.3兆行以上。
- **rubygems** \- インストールされたすべてのgemの行が含まれ、毎時更新されます \- 1800億行以上。
- **hackernews** \- Hacker Newsの投稿とコメントが含まれています。
- **imdb** \- IMDBの映画データベース情報が含まれています。
- **nyc\_taxi** \- NYCのタクシー乗車データが含まれています。
- **opensky** \- OpenSky Networkの航空データが含まれています。
- **reddit** \- Redditの投稿とコメントが含まれています。
- **stackoverflow** \- Stack Overflowの質問と回答が含まれています。
- **uk** \- 英国の不動産取引データと関連する地理情報の包括的なコレクションが含まれています。


その他。


## 私の主な機能 [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E7%A7%81%E3%81%AE%E4%B8%BB%E3%81%AA%E6%A9%9F%E8%83%BD)


- 自然言語クエリのテスト: 通常の英語の質問がMCPサーバーを介してClickHouse用に最適化されたSQLクエリに変換される様子をご覧ください。
- リアルタイム分析の体験: MCPサーバーがClickHouseの有名な速度を最小限の遅延でAI搭載の洞察と組み合わせる方法をご覧ください。
- 対話型データ探索: MCP\-LLM接続を利用した会話型インターフェースを通じてデモデータセットを探索してください。
- 自動視覚化の表示: MCPサーバーを流れるデータがどのように自動的に視覚化されるかをご覧ください。


## デモの探索 [\#](/jp/blog/agenthouse-demo-clickhouse-llm-mcp-jp#%E3%83%87%E3%83%A2%E3%81%AE%E6%8E%A2%E7%B4%A2)


AgentHouseを始めるには、[llm.clickhouse.com](https://llm.clickhouse.com)にアクセスし、Googleアカウントでデモ環境にログインして質問を開始してください。始めるのに最適な方法は、「どのデータセットがありますか？」と尋ねることです。これにより、データベースのリストが表示され、それらを探索し始めることができます。


皆様からのご質問にお答えできることを楽しみにしています！
