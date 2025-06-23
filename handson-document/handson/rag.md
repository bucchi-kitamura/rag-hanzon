# ステップ2 RAG機能
チャット機能ができたので、次はRAG機能を実装していきます。
RAGを使うことで、ローカルのテキストファイルの内容に基づいて回答を生成できるようになります。

## ここでやること

ローカルにあるテキストファイルを読み込んで、その内容に基づいてLLMが回答できるようにします。

### RAGの処理フロー
これらの処理をllama-indexを使って実装していきます！

```
[1. インデックス作成]
文書ファイル → 埋め込みモデル → ベクトル → インデックスに保存

[2. 質問回答]
ユーザーの質問 → 埋め込みモデル → 質問ベクトル
                              ↓
関連文書を検索 ← インデックスから類似ベクトルを探す
                              ↓
検索された文書 + 質問 → LLM → 回答生成
```

### 使用するモデル

- **LLM**: `schroneko/gemma-2-2b-jpn-it` (回答生成)
- **埋め込みモデル**: `nomic-embed-text` (テキストをベクトル化)

## 準備

実行ファイルの作成を作成しましょう

```bash
touch src/rag.py
```

次にRAGにテキストファイルを作ります。
```
# テスト用のテキストファイルを作成
mkdir data && touch data/sample.txt
```
上記のコマンドを実行した後に、`sample.txt`にこのテキストファイルから参照したものが回答に含まれるか確認したいです。

なのでインターネットで公開されていない情報を入れてみましょう。

サンプルとして架空の会社の就業規則・社員プロフィール・会社概要を用意しました。

::: details サンプルテキスト

```md
## サンプル1: 社内規約・制度（非公開情報）

### 株式会社RAGハンズ 就業規則

勤務時間・休憩時間
- 標準勤務時間：9:00〜18:00（休憩時間12:00〜13:00）
- フレックスタイム制度：コアタイム 10:00〜15:00
- 在宅勤務：週3日まで可能（事前申請必要）

休暇制度
- 年次有休暇：入社1年目15日、2年目16日、以降毎年1日追加
- 特別休暇：慶弔休暇、産前産後休暇、育児休暇
- リフレッシュ休暇：勤続5年ごとに5日間の連続休暇
- 誕生日休暇：誕生月に1日取得可能

福利厚生
- 住宅手当：月額3万円（通勤時間1時間以内の場合）
- 資格取得支援：業務関連資格の受験料・教材費を全額補助
- 研修制度：年間10万円まで外部研修参加費用を支給
- 健康診断：年1回の定期健康診断、人間ドック費用補助（3万円まで）

服装規定
- 基本的にはビジネスカジュアル
- 客先訪問時はスーツ着用
- 金曜日はカジュアルデー（ジーンズ・スニーカー可）

携帯電話・PC使用ルール
- 会社貸与PCの私的利用は禁止
- 社内情報のクラウドストレージへの無断アップロード禁止
- パスワードは3ヶ月ごとに変更必須

```
---

```md
## サンプル2: 社員プロフィール（社内ディレクトリ）

### 開発部メンバー紹介

部長：山田 花子（やまだ はなこ）
- 入社年：2015年4月
- 経歴：前職でシステムエンジニア7年、当社で9年
- 専門分野：プロジェクトマネジメント、システム設計
- 保有資格：PMP、情報処理技術者（システムアーキテクト）
- 座席：3F-A101
- 内線：1001
- 趣味：登山、読書
- 一言：チーム一丸となって良いプロダクトを作りましょう！

主任：佐藤 太郎（さとう たろう）
- 入社年：2019年4月
- 経歴：新卒入社、フロントエンド開発5年
- 専門分野：React、Vue.js、UI/UX設計
- 保有資格：応用情報技術者
- 座席：3F-A105
- 内線：1005
- 趣味：ゲーム、アニメ鑑賞
- 一言：新しい技術を学ぶのが大好きです。何でも聞いてください！

田中 次郎（たなか じろう）
- 入社年：2022年10月（中途入社）
- 経歴：前職でWebデザイナー3年、当社でフロントエンド開発2年
- 専門分野：デザインシステム、CSS設計
- 保有資格：ウェブデザイン技能検定2級
- 座席：3F-A108
- 内線：1008
- 趣味：カメラ、コーヒー
- 一言：デザインと開発の橋渡し役として頑張ります！

鈴木 美咲（すずき みさき）
- 入社年：2024年4月
- 経歴：新卒入社、研修期間を経て開発チーム配属
- 専門分野：JavaScript、Python（学習中）
- 座席：3F-A112
- 内線：1012
- 趣味：映画鑑賞、料理
- 一言：まだまだ勉強中ですが、一日でも早く戦力になりたいです！

```
---

```md
## サンプル3: 会社概要・沿革（企業情報）

### 株式会社RAGハンズ 会社概要

基本情報
- 設立：2010年5月15日
- 資本金：5,000万円
- 代表取締役：高橋 隆（たかはし たかし）
- 従業員数：85名（2024年12月現在）
- 本社所在地：東京都渋谷区神宮前3-15-8 テックビル5F
- 事業内容：Webシステム開発、モバイルアプリ開発、DXコンサルティング

沿革
- 2010年5月：東京都新宿区にて創業（従業員3名）
- 2012年3月：本社を渋谷区に移転
- 2015年8月：モバイルアプリ開発事業を開始
- 2018年11月：従業員数50名達成
- 2020年4月：コロナ禍でリモートワーク制度を本格導入
- 2022年7月：DXコンサルティング事業を新設
- 2024年1月：AI・機械学習チームを新設

主要取引先
- ○○商事株式会社（ECサイト開発・保守）
- △△銀行（モバイルバンキングアプリ開発）
- □□製造株式会社（工場管理システム）
- ※※自治体（住民サービスアプリ）

企業理念
「テクノロジーで社会の課題を解決し、豊かな未来を創造する」

行動指針
1. 顧客第一：お客様の成功が私たちの成功
2. 継続的学習：技術の進歩に合わせて常に学び続ける
3. チームワーク：多様な個性を活かしたチーム力
4. 社会貢献：技術を通じて社会に価値を提供

オフィス環境
- フリーアドレス制（固定席とフレキシブル席の併用）
- カフェスペース：コーヒー・軽食無料提供
- 会議室：8室（10名用×4、6名用×2、4名用×2）
- リラックスルーム：仮眠・休憩用スペース
```

:::


この時点のプロジェクト構成
```
rag-hanzon/
├── src/
│   ├── chat.py
│   └── rag.py
└── data/
    └── sample.txt
```

## コード部分
RAG機能の大枠の構成は次の3ステップ
1. テキストファイル読み込み
   - ローカルのテキストファイルをLlamaIndexに読み込む
2. インデックス作成
   - 読み込んだテキストからベクトルインデックスを作成
3. クエリ実行
   - ユーザーの質問に対して関連する内容をインデックスから検索し、LLMが回答を生成

::: code-group

```python [src/rag.py]
# - Settings: llama-index全体の設定を管理
# - SimpleDirectoryReader: ディレクトリからドキュメントを読み込む
# - VectorStoreIndex: ドキュメントをベクトル化して検索可能にする
# - OllamaEmbedding: テキストを数値ベクトルに変換するモデル

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

def main():
    # モデルの設定
    Settings.llm = Ollama(model="schroneko/gemma-2-2b-jpn-it",)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # ドキュメントの読み込み
    # 先ほど用意したテキストファイルを読み込んでもらう
    documents = SimpleDirectoryReader("./src/data").load_data()

    # ベクトルインデックスの作成 
    # イメージとしては意味で検索できる辞書を作成してる
    # 従来（キーワード検索）：「休暇」で検索 → 「休暇」という文字がある文書だけ見つかる
    # ベクトル：「休暇」で検索 → 「有給」「休み」「リフレッシュ」も見つかる
    index = VectorStoreIndex.from_documents(documents)

    # クエリエンジンの作成
    # 検索と回答生成の機能を統合した検索エンジン
    query_engine = index.as_query_engine()

    while True:
        user_input = input("あなた: ")

        if user_input.lower() in ["exit", "終了"]:
            print("チャットボットを終了します。")
            break

        if not user_input.strip():
            continue
        # クエリエンジンを使って回答を生成するように変更する
        response = query_engine.query(user_input)
        print(f"🤖: {response.response.strip()}\n")

if __name__ == "__main__":
    main()
```

```python [src/rag.py]
# - Settings: llama-index全体の設定を管理
# - SimpleDirectoryReader: ディレクトリからドキュメントを読み込む
# - VectorStoreIndex: ドキュメントをベクトル化して検索可能にする
# - OllamaEmbedding: テキストを数値ベクトルに変換するモデル

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
import os

def main():
    # モデルの設定
    Settings.llm = Ollama(model="schroneko/gemma-2-2b-jpn-it",)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # インデックスの保存先ディレクトリ
    PERSIST_DIR = "./storage"

    # 既存のインデックスがあるかチェック
    if os.path.exists(PERSIST_DIR):
        print("📁 既存のインデックスを読み込んでいます...")
        # 保存済みのインデックスを読み込む
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print("✅ インデックスの読み込みが完了しました！")
    else:
        print("🔨 新しいインデックスを作成しています...")
        # ドキュメントの読み込み
        # 先ほど用意したテキストファイルを読み込んでもらう
        documents = SimpleDirectoryReader("./src/data").load_data()

        # ベクトルインデックスの作成
        # イメージとしては意味で検索できる辞書を作成してる
        # 従来（キーワード検索）：「休暇」で検索 → 「休暇」という文字がある文書だけ見つかる
        # ベクトル：「休暇」で検索 → 「有給」「休み」「リフレッシュ」も見つかる
        index = VectorStoreIndex.from_documents(documents)

        # インデックスを保存
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print("💾 インデックスを保存しました！")

    # クエリエンジンの作成
    # 検索と回答生成の機能を統合した検索エンジン
    query_engine = index.as_query_engine()

    while True:
        user_input = input("あなた: ")

        if user_input.lower() in ["exit", "終了"]:
            print("チャットボットを終了します。")
            break

        if not user_input.strip():
            continue
        # クエリエンジンを使って回答を生成するように変更する
        response = query_engine.query(user_input)
        print(f"🤖: {response.response.strip()}\n")

if __name__ == "__main__":
    main()
```

:::



## 動作確認

プログラムの実行
```bash
python src/rag.py
```

動作確認

::: tip 💡 実行結果例
```
❯ python src/rag.py

あなた: 田中さんの内線番号は？
🤖: 1008
</start_of_turn>

```
:::

## まとめ

RAG機能の基本実装が完了しました！

テキストファイルの内容に基づいて、LLMが回答を生成できるようになりましたね。