# 環境構築

このセクションではpythonの実行環境を作っていきます。

ハンズオン当日はここから一緒に作業をしていきます。

## ハンズオン用の作業ディレクトリを作る

```bash
mkdir rag-hanzon
```

::: tip 📁 作業ディレクトリ
以降の作業は全てこのディレクトリ内で行います。
:::

## Python環境の構築

ハンズオンで使うPythonを実行するための仮想環境を作ります

### 仮想環境を作成する
```bash
python3 -m venv .venv
```

### 仮想環境を有効化する

::: code-group

```cmd [Windows]
.venv\Scripts\activate
```

```bash [macOS/Linux]
source .venv/bin/activate
```

:::


`which python`を実行してみましょう。

```bash
❯ which python
/Users/kitamuratakashi/projects/rag-20250703/.venv/bin/python
```

## パッケージのインストール

ハンズオンで使うパッケージをインストールします。

```bash
pip install llama-index llama-index-llms-ollama llama-index-embeddings-ollama
```

今回は以下のパッケージを追加します。
- llama-index
  - RAGのAugmented（拡張・増強）
  - 検索で取得した情報を整理して、コンテキストとして拡張・増強する
- llama-index-llms-ollama
  - RAGのGeneration（生成）
  - 拡張したコンテキストを使って回答を生成する
- llama-index-embeddings-ollama
  - RAGのRetrieval（検索・取得）
  - 質問に関連するドキュメントやチャンクを検索・取得する
  - どの情報がユーザの質問に関連するかを見つけてくれる
![ざっくりイメージ](./images/llama-flow.png)

::: info モデルの役割
[事前準備で用意してもらった2種類のモデル](/guide/preparation.html#%E3%83%A2%E3%83%86%E3%82%99%E3%83%AB%E3%81%AE%E3%82%BF%E3%82%99%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%88%E3%82%99)は

`llama-index-llms-ollama`と`llama-index-embeddings-ollama`でそれぞれ必要になります
:::


これでハンズオンの準備が完了しました。次のセクションへ移りましょう👉
