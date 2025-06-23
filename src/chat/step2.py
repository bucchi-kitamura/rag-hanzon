from llama_index.llms.ollama import Ollama

def main():
    llm = Ollama(
        model="schroneko/gemma-2-2b-jpn-it"
    )

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
        response = llm.complete(user_input)
        # 応答の末尾に余分な空白文字が入ることがあるのでstripを使って削除する
        print(f"🤖: {response.text.strip()}\n")

if __name__ == "__main__":
    main()