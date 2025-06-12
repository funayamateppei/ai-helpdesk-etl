import re

def normalize_text(text: str) -> str:
    # 全角→半角、記号・カッコ・タイトル除去、空白統一など
    text = text.lower()
    text = re.sub(r'[【】]', '', text)
    text = re.sub(r'[（）()]', '', text)
    text = re.sub(r'[\n\r]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    # ここに表現ゆれ吸収の辞書置換も追加できる
    return text

def get_gemini_embedding(text: str, api_key: str, task_type: str = "retrieval_document"):
    import google.generativeai as genai
    norm_text = normalize_text(text)
    genai.configure(api_key=api_key)
    try:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=norm_text,
            task_type=task_type
        )
        return response["embedding"]
    except Exception as e:
        print(f"Gemini embedding取得エラー: {e}")
        return None
