import os
import time
from dotenv import load_dotenv
from notion_client import Client as NotionClient

# .envファイルから環境変数を読み込む
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
if not NOTION_TOKEN:
    print("エラー: NOTION_TOKENが設定されていません。")
    exit()
notion = NotionClient(auth=NOTION_TOKEN)

def extract_text_from_block(block):
    text = ""
    block_type = block.get("type")
    if block_type in [
        "paragraph", "heading_1", "heading_2", "heading_3",
        "bulleted_list_item", "numbered_list_item", "toggle", "quote", "callout"
    ]:
        rich_text_array = block.get(block_type, {}).get("rich_text", [])
        for rich_text_item in rich_text_array:
            text += rich_text_item.get("plain_text", "")
        text += "\n"
    elif block_type == "table_row":
        for cell in block.get("table_row", {}).get("cells", []):
            for rich_text_item in cell:
                text += rich_text_item.get("plain_text", "") + "\t"
            text = text.strip() + "\n"
    elif block_type == "code":
        rich_text_array = block.get("code", {}).get("rich_text", [])
        for rich_text_item in rich_text_array:
            text += rich_text_item.get("plain_text", "")
        text += "\n"
        caption_array = block.get("code", {}).get("caption", [])
        if caption_array:
            text += "キャプション: "
            for caption_item in caption_array:
                text += caption_item.get("plain_text", "")
            text += "\n"
    # image, file, pdfは無視する！
    # elif block_type in ["file", "pdf", "image"]:
    #     ...（何もしない）
    return text

def get_child_page_ids(page_id):
    child_ids = []
    try:
        next_cursor = None
        while True:
            response = notion.blocks.children.list(block_id=page_id, start_cursor=next_cursor)
            for block in response.get("results", []):
                if block.get("type") == "child_page":
                    child_ids.append(block.get("id"))
            next_cursor = response.get("next_cursor")
            if not next_cursor:
                break
            time.sleep(0.34)
    except Exception as e:
        print(f"子ページID取得エラー: {e}")
    return child_ids

def get_page_info(page_id):
    try:
        page_info = notion.pages.retrieve(page_id=page_id)
        page_title_parts = page_info.get("properties", {}).get("title", {}).get("title", [])
        page_title = "".join([part.get("plain_text", "") for part in page_title_parts])
        page_url = page_info.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")
        return page_title, page_url
    except Exception as e:
        print(f"ページ情報取得エラー: {e}")
        return "", ""

def get_page_text(page_id):
    text = ""
    try:
        blocks = []
        next_cursor = None
        while True:
            response = notion.blocks.children.list(block_id=page_id, start_cursor=next_cursor)
            blocks.extend(response.get("results", []))
            next_cursor = response.get("next_cursor")
            if not next_cursor:
                break
            time.sleep(0.34)
        for block in blocks:
            text += extract_text_from_block(block)
    except Exception as e:
        print(f"ページテキスト取得エラー: {e}")
    return text.strip()

def get_all_pages_recursive(page_id, depth=0, max_depth=None):
    page_title, page_url = get_page_info(page_id)
    page_text = get_page_text(page_id)
    child_ids = get_child_page_ids(page_id)
    page_data = {
        "id": page_id,
        "title": page_title,
        "url": page_url,
        "text": page_text,
        "children": child_ids
    }
    all_pages = [page_data]
    for child_id in child_ids:
        all_pages.extend(get_all_pages_recursive(child_id, depth=depth+1, max_depth=max_depth))
    return all_pages
