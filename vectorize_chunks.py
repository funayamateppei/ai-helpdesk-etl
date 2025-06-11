import os
import google.generativeai as genai

def get_gemini_embedding(text):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Gemini embedding取得エラー: {e}")
        return None

def vectorize_chunks(all_chunks):
    vectorized_chunks = []
    for i, chunk_info in enumerate(all_chunks):
        text = chunk_info["chunk"]
        url = chunk_info["url"]
        embedding = get_gemini_embedding(text)
        if embedding:
            vectorized_chunks.append({
                "chunk": text,
                "url": url,
                "embedding": embedding
            })
        else:
            print(f"embedding取得失敗: {url}")
    return vectorized_chunks