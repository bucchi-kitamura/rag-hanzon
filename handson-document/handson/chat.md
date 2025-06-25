# ステップ1 チャット機能
RAGを使うためにはまずLLMと会話できるようにしないといけないですね。
という訳で早速作っていきましょう。


## ここでやること

まずはローカルからLLMと簡単なチャットを出来るようにします。

先ほどインストールした[llama-index-llms-ollama](/guide/setup.html#%E3%83%8F%E3%82%9A%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B7%E3%82%99%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)を使います。

## 準備

ファイルを作る
```bash
touch src/chat.py
```

src配下にファイルが出来ていればOK
```
rag-hanzon/
├── src/
    └── chat.py
```

## コード部分
LLMと会話をするまでの大枠の構成は次の2ステップ
1. プロンプト入力部分
 - ユーザーからのプロンプトを受け取る処理
2. 回答部分
 - プロンプトをLLMに渡して回答を取得する

::: code-group

```python [src/chat.py]
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

# LLMの設定
Settings.llm = Ollama(
    model="schroneko/gemma-2-2b-jpn-it"
)


def main():
    """メイン関数"""
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
        # 応答の末尾に余分な空白文字が入ることがあるのでstripを使って削除する
        print(f"🤖: {response.text.strip()}\n")


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
```

:::

## 実行手順

### 1. Ollamaが起動していることを確認

```bash
ollama list
```

::: details 正常な出力例
```
NAME                                  ID              SIZE      MODIFIED
nomic-embed-text:latest               0a109f422b47    274 MB    7 seconds ago
schroneko/gemma-2-2b-jpn-it:latest    fcfc848fe62a    2.8 GB    50 minutes ago
```
:::

起動してなければサーバを起動しましょう
```bash
ollama serve
```

### 2. プログラムの実行

```bash
uv run src/chat.py
```

### 3. 動作確認

::: tip 💡 実行結果例
```
> uv run src/chat.py
LLMと会話をする準備ができました。終了するには 'exit' と入力してください。

あなた: こんにちは
🤖: 考え中...
🤖: こんにちは！😊 何か用ですか？

あなた: Pythonについて教えて
🤖: 考え中...
🤖: Pythonは、1991年にグイド・ヴァンロッサムによって開発されたプログラミング言語です。

シンプルで読みやすい構文が特徴で、初心者にも学びやすい言語として人気があります。

あなた: exit
チャットボットを終了します。
```
:::

## まとめ

次のステップでは、チャット機能に**RAG**の仕組みを追加し、ローカルドキュメントの内容について回答できるようにします！

