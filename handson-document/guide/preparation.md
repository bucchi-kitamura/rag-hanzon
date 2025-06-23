# 事前準備

ハンズオン参加前に、以下の準備を **各自で** 完了してください。

ダウンロードには時間がかかるため、進行をスムーズにするためにご協力お願いします🙏

::: warning 重要
ハンズオン当日は、この事前準備が完了していることを前提に進めます。

準備に不安がある場合は、ペチオブの[Discord](https://discord.gg/DZGgaE3a7F)からご相談ください。
:::

## 事前準備一覧

- uv
- Ollama
- モデルのダウンロード

## uv

::: tip uvとは
[uv](https://docs.astral.sh/uv/)は高速なPythonパッケージマネージャーです。
Pythonの自動インストールから必要なライブラリの管理まで、Python開発環境を簡単に構築・管理できます。
:::

### インストール
https://docs.astral.sh/uv/getting-started/installation/
::: code-group

```powershell [Windows]
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash [macOS]
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash [macOS（Homebrew）]
brew install uv
```
:::

### 確認

インストール後、新しいターミナルを開いて確認してください

```bash
uv --version
```

::: details uvのバージョンが表示されれば、インストール完了です
uv 0.7.8 (0ddcc1905 2025-05-23)
:::

## Ollamaのインストール

::: tip Ollamaとは
[Ollama](https://ollama.com/)はローカルでLLMを実行するためのツールです。
:::
公式サイトからOllamaをダウンロードして、インストールして下さい。
https://ollama.ai/download


### インストール確認

```bash
ollama --version
# バージョンが表示される事を確認してください
ollama version is 0.9.0
```

## モデルのダウンロード

ハンズオンでは以下の2種類のモデルを使用します：

1. **大規模言語モデル（LLM）** - 質問に対する回答生成
2. **埋め込みモデル** - テキストのベクトル化と類似性検索

### 大規模言語モデル（LLM）

Googleが開発したgemma2を日本語向けに調整したモデルを使用します。

```bash
# メインのLLMモデル（約2.8GB）
ollama pull schroneko/gemma-2-2b-jpn-it
```

::: details 実行結果 モデルダウンロード中の様子
```
pulling manifest 
pulling 1b3b86a920e7: 100% ▕███████████████████████▏ 2.8 GB                         
pulling 4ea0df93422f: 100% ▕███████████████████████▏  445 B                         
pulling 2490e7468436: 100% ▕███████████████████████▏   65 B                         
pulling e2155a2ac827: 100% ▕███████████████████████▏  413 B                         
verifying sha256 digest 
writing manifest 
success 
```
:::

### 埋め込みモデル

```bash
# 埋め込みモデル（約274MB）
ollama pull nomic-embed-text
```

### ダウンロード確認

```bash
ollama list
```

::: details 実行結果 各モデルが一覧に表示されていればインストール完了です
```
NAME                                  ID              SIZE      MODIFIED
nomic-embed-text:latest               0a109f422b47    274 MB    7 seconds ago
schroneko/gemma-2-2b-jpn-it:latest    fcfc848fe62a    2.8 GB    50 minutes ago
```
:::

## 動作確認
モデルをインストールしたのでLLMに挨拶してみましょう！

### LLM

```bash
ollama run schroneko/gemma-2-2b-jpn-it "こんにちは"
```

::: details 実行結果
こんにちは！😊

何か用ですか？
:::

::: tip 出力結果について
毎回異なる回答が表示される可能性があります。LLMは質問のたびに新しい回答を生成するため、全く同じ内容になることはありません。
:::

### 埋め込みモデルの動作確認

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "Hello World"
  }'
```

::: details 実行結果（長いので一部）
```json
{
  "embedding": [
    0.21180304884910583,
    1.2743878364562988,
    // ... ベクトルデータが表示される
  ]
}
```
:::

---

お疲れ様でした！
事前準備が完了したら、後はハンズオン当日までお待ちください。
<!-- 当日は **[プロジェクトセットアップ](/guide/setup)** からみんなで作業していきます！ -->