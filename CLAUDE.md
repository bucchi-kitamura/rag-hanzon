# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a hands-on project for building a local RAG (Retrieval-Augmented Generation) system step by step. The project is designed to be minimal initially, allowing for incremental development.

## Development Commands
### Environment Setup
```bash
# Install Python 3.13 (if not already installed)
uv python install 3.13

# Create virtual environment
uv venv --python 3.13

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv sync
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Check code quality
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check . --fix
```

## Core Development Rules
1. パッケージ管理
   - `uv` のみを使用し、`pip` は絶対に使わない
   - インストール方法：`uv add package`
   - ツールの実行：`uv run tool`
   - アップグレード：`uv add --dev package --upgrade-package package`
   - 禁止事項：`uv pip install`、`@latest` 構文の使用

2. コード品質
   - すべてのコードに型ヒントを必須とする
   - パブリックAPIには必ずドキュメンテーション文字列（docstring）を付ける
   - 関数は集中して小さく保つこと
   - 既存のパターンを正確に踏襲すること
   - 行の最大長は88文字まで

## Python Tools
1. Ruff
   - フォーマット実行：`uv run --frozen ruff format .`
   - チェック実行：`uv run --frozen ruff check .`
   - 修正実行：`uv run --frozen ruff check . --fix`
   - 重要な指摘内容：
     - 行の長さ（88文字）
     - インポートのソート（I001）
     - 未使用のインポート
   - 行の折り返し：
     - 文字列は括弧を使う
     - 関数呼び出しは複数行にして適切にインデント
     - インポート文は複数行に分ける

2. 型チェック
   - ツール：`uv run --frozen pyright`
   - 要件：
     - Optional型には明示的なNoneチェックを入れる
     - 文字列の型は狭めて扱う
     - バージョン警告はチェックが通れば無視してよい

3. Pre-commit
   - 設定ファイル：`.pre-commit-config.yaml`
   - 実行タイミング：gitコミット時
   - 使用ツール：Prettier（YAML/JSON用）、Ruff（Python用）
   - Ruffの更新方法：
     - PyPIのバージョンを確認する
     - 設定ファイルのリビジョンを更新する
     - まず設定ファイルをコミットする

## Project Structure
```
rag-hanzon/
├── src/           # ソースコード
├── pyproject.toml # プロジェクト設定とRuff設定
├── .gitignore     # Git除外設定
├── README.md      # プロジェクト説明とセットアップ手順
└── CLAUDE.md      # このファイル
```

## Important Notes
- このプロジェクトは段階的に構築することを前提としている
- RAG関連のパッケージは必要に応じて追加していく
- 最小限の構成から始めて、機能を段階的に実装する