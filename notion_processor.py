import os
import json
from dotenv import load_dotenv
from notion_loader import get_all_pages_recursive
from text_chunker import split_all_pages
from vectorize_chunks import vectorize_chunks

# .envからPAGE_IDを読み込む
load_dotenv()
PAGE_ID = os.getenv("NOTION_PAGE_ID")
if not PAGE_ID:
    print("NotFound: NOTION_PAGE_ID")
    exit()

# Notionから全ページを再帰的に取得
all_pages = get_all_pages_recursive(PAGE_ID)
# ページごとにテキストをチャンク分割
all_chunks = split_all_pages(all_pages)
print(f"取得したチャンク数: {len(all_chunks)}")

# ベクトル化
vectorized_chunks = vectorize_chunks(all_chunks)
    
# 結果をjsonファイルに保存
# 各チャンクの情報を以下の形式で保存
# {
#   "chunk": text,
#   "url": url,
#   "embedding": embedding
# }
output_file = "vectorized_chunks.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(vectorized_chunks, f, ensure_ascii=False, indent=2)
print(f"Vectorized chunks saved to {output_file}")

exit()
