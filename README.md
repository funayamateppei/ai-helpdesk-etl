# ai-helpdesk-etl

## セットアップ手順

1. **リポジトリをクローンする**

   ```bash
   git clone <このリポジトリのURL>
   cd ai-helpdesk-etl
   ```

2. **仮想環境を作る**

   ```bash
   python3 -m venv .venv
   ```

3. **仮想環境を有効化する**

   ```bash
   source .venv/bin/activate
   ```

4. **必要なパッケージをインストールする**

   ```bash
   pip install -r requirements.txt
   ```

5. **環境変数ファイル（.env）を用意する**

   - `.env` ファイルをプロジェクト直下に作って、必要な API キーなどをセットしてください

6. **スクリプトを実行する**
   ```bash
   python <メインのスクリプト名>.py
   ```

---

## よくある困りごと Q&A

- 仮想環境を抜けたいときは？
  ```bash
  deactivate
  ```
- パッケージが入らない・変な場所に入るときは？
  - 仮想環境が有効になってるか確認する

---
