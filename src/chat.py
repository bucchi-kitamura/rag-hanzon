from llama_index.core import Settings
from llama_index.llms.ollama import Ollama


def main():
    """メイン関数"""
    # LLMで使用するモデルを設定
    try:
        Settings.llm = Ollama(model="schroneko/gemma-2-2b-jpn-it")

        print("LLMと会話をする準備ができました。終了するには 'exit' と入力してください。\n")

        while True:
            # ユーザーの入力待ち状態 ここでプロンプトを入力する
            user_input = input("あなた: ")

            # 終了条件 ユーザーが特定のキーワードを入力したら対話を終了する
            if user_input.lower() in ["exit", "終了"]:
                print("チャットボットを終了します。")
                break

            # 空の状態でEnterを押された場合はスキップする
            if not user_input.strip():
                continue

            print("🤖: 考え中...")

            # LLM呼び出し ユーザーの入力をLLMに渡して、レスポンスを取得する
            response = Settings.llm.complete(user_input)
            print(f"🤖: {response.text.strip()}\n")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


# Pythonファイルが直接実行された場合、以下のコードが実行される
# モジュールとしてインポートされた場合に実行されないようにするためのPythonのお作法
# これを書かないと、このファイルをインポートした時にmain関数が実行されてしまう
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nチャットボットを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
