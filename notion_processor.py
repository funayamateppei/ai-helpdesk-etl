import os
from dotenv import load_dotenv
from notion_loader import get_all_pages_recursive
from text_chunker import split_all_pages

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

exit()
