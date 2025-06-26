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
        print("🔍 モデルの設定が完了しました")

        # RAGで使用するドキュメントを読み込む
        # 第1引数にディレクトリ名を指定
        print("🔍 ドキュメント読み込み中...")
        documents = SimpleDirectoryReader("data").load_data()
        print("🔍 ドキュメントの読み込みが完了しました")

        # インデックスの作成
        print("🔍 ベクトルインデックスを作成中...")
        index = VectorStoreIndex.from_documents(documents)
        print("✅ インデックスの作成が完了しました")

        # クエリエンジンの作成
        print("🔍 クエリエンジンの作成中...")
        query_engine = index.as_query_engine()
        print("🔍 クエリエンジンの作成が完了しました")

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

            # クエリの実行
            # query_engine.query()は内部で以下を自動処理:
            # - Retrieval: 関連文書の検索
            # - Augmented: 検索結果で質問を拡張
            # - Generation: 拡張された情報でLLMが回答生成
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
