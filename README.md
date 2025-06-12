# ai-helpdesk-etl

Notion 連携 AI ナレッジ Q&A ボット

## 概要

- Notion のナレッジを自動で分割・ベクトル化し、Google Gemini API を用いて Q&A ができる社内ヘルプデスクボット
- 質問内容も embedding し、Notion チャンクとコサイン類似度でマッチング、LLM で要約・回答
- embedding/LLM ともに Google Gemini API で統一
- 3D 可視化（Plotly.js）でナレッジ分布と質問の位置をプロット

## 構成ファイル

- `notion_loader.py` ... Notion API からページ・テキスト取得
- `notion_processor.py` ... Notion 全ページ → チャンク分割 →embedding→ 保存
- `text_chunker.py` ... 文単位でチャンク分割
- `vectorize_chunks.py` ... チャンクを Gemini で embedding
- `qa_bot.py` ... 質問 →embedding→ 最も近い chunk→LLM 要約 → 返答
- `text_normalizer.py` ... embedding 前のテキスト正規化
- `pca_vectorize.py` ... embedding を PCA で 3 次元化
- `pca.html` ... 3D 分布可視化（Plotly.js）

## 使い方

### 1. セットアップ

- 必要なパッケージをインストール
  ```zsh
  pip install -r requirements.txt
  ```
- `.env`ファイルに API キーを設定
  ```
  GOOGLE_API_KEY=your-gemini-api-key
  NOTION_API_KEY=your-notion-api-key
  NOTION_ROOT_PAGE_ID=your-root-page-id
  ```

### 2. Notion データ取得・ベクトル化

- Notion から全ページ取得＆チャンク分割・ベクトル化
  ```zsh
  python3 notion_processor.py
  ```
- `vectorized_chunks.json`に保存される

### 3. Q&A 実行

- 質問を入力して AI Q&A
  ```zsh
  python3 qa_bot.py
  ```
- 質問 embedding は`question_vectors.json`に保存

### 4. 3D 可視化

- ベクトルを PCA で 3 次元化＆Plotly.js で可視化
  ```zsh
  python3 pca_vectorize.py
  open pca.html
  ```
- `pca.html`でナレッジ分布＆質問位置を 3D 表示

## 注意

- Notion の親ページは自動で除外される
- Gemini リクエスト上限に注意
