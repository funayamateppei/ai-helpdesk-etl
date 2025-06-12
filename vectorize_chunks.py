import os
from text_normalizer import get_gemini_embedding

def get_gemini_embedding_for_chunk(text):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    return get_gemini_embedding(text, GEMINI_API_KEY, task_type="retrieval_document")

def vectorize_chunks(all_chunks):
    vectorized_chunks = []
    for i, chunk_info in enumerate(all_chunks):
        text = chunk_info["chunk"]
        url = chunk_info["url"]
        embedding = get_gemini_embedding_for_chunk(text)
        if embedding:
            vectorized_chunks.append({
                "chunk": text,
                "url": url,
                "embedding": embedding
            })
        else:
            print(f"embedding取得失敗: {url}")
    return vectorized_chunks