# ステップ2 RAG機能（テキストファイルのみ）
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
touch src/rag-text.py
```

次にRAGにテキストファイルを作ります。
```
# テスト用のテキストファイルを作成
mkdir -p data && touch data/sample.txt
```
上記のコマンドを実行した後に、`sample.txt`にこのテキストファイルから参照したものが回答に含まれるか確認したいです。

なのでインターネットで公開されていない情報を入れてみましょう。


この時点のプロジェクト構成
```
rag-hanzon/
├── src/
│   ├── chat.py
│   └── rag-text.py
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

```python [src/rag-text.py]
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


def main():
    """メイン関数"""
    try:
        # RAGの初期設定
        # LLMで使用するモデルを設定
        print("🔍 モデルの設定中...")
        Settings.llm = Ollama(model="schroneko/gemma-2-2b-jpn-it")
        # テキストをベクトル化するためのモデルを設定
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
        print("✅ モデルの設定が完了しました")

        # RAGで使用するドキュメントを読み込む
        # 第1引数にディレクトリ名を指定
        print("🔍 ドキュメント読み込み中...")
        documents = SimpleDirectoryReader("data").load_data()
        print("✅ ドキュメントの読み込みが完了しました")

        # インデックスの作成
        print("🔍 ベクトルインデックスを作成中...")
        index = VectorStoreIndex.from_documents(documents)
        print("✅ インデックスの作成が完了しました")

        # クエリエンジンの作成
        print("🔍 クエリエンジンの作成中...")
        query_engine = index.as_query_engine()
        print("✅ クエリエンジンの作成が完了しました")

        print(
            "\nRAGシステムが準備できました。終了するには 'exit' と入力してください。\n"
        )

        while True:
            # ユーザーの入力待ち状態 ここでプロンプトを入力する
            user_input = input("あなた: ")

            # 終了条件 ユーザーが特定のキーワードを入力したら対話を終了する
            if user_input.lower() in ["exit", "終了"]:
                print("RAGシステムを終了します。")
                break

            # 空の状態でEnterを押された場合はスキップする
            if not user_input.strip():
                continue

            print("🤖: 考え中...")

            # RAGクエリの実行
            response = query_engine.query(user_input)
            print(f"🤖: {response.response.strip()}\n")

    except FileNotFoundError as e:
        print(f"❌ エラー: {e}")
        print("まず data ディレクトリとサンプルファイルを作成してください。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nチャットボットを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

:::

## 動作確認

プログラムの実行
```bash
uv run src/rag-text.py
```

動作確認

::: tip 💡 実行結果例
```
❯ uv run src/rag-text.py                                                                                                                                       ✨   17:38 
🔍 モデルの設定中...
✅ モデルの設定が完了しました
🔍 ドキュメント読み込み中...
✅ ドキュメントの読み込みが完了しました
🔍 ベクトルインデックスを作成中...
✅ インデックスの作成が完了しました
🔍 クエリエンジンの作成中...
✅ クエリエンジンの作成が完了しました

RAGシステムが準備できました。終了するには 'exit' と入力してください。

あなた: bucchi-UIって何？
🤖: 考え中...
🤖: bucchi-UIは社内プロジェクト向けに開発されたReactベースのUIコンポーネントライブラリです。
```
:::

## まとめ

RAG機能の基本実装が完了しました！

テキストファイルの内容に基づいて、LLMが回答を生成できるようになりましたね。