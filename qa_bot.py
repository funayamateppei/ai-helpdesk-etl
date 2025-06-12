import json
import numpy as np
import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
from text_normalizer import get_gemini_embedding
from sklearn.decomposition import PCA

# --- .envからAPIキーを読み込む ---
load_dotenv()

# --- 設定 ---
VECTOR_FILE = "vectorized_chunks.json"
SIM_THRESHOLD = 0.7

# --- ユーティリティ ---
def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def get_embedding(text: str) -> List[float]:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    return get_gemini_embedding(text, GEMINI_API_KEY, task_type="retrieval_document")

def find_most_similar(query_emb: List[float], chunks: List[dict]):
    sims = [cosine_similarity(query_emb, c["embedding"]) for c in chunks]
    print(f"類似度スコア: {sims}")
    max_idx = int(np.argmax(sims))
    return chunks[max_idx], sims[max_idx]

def ask_llm(context: str, question: str) -> str:
    prompt = f"""
あなたは社内ナレッジbotです。以下の情報を参考に、エンジニアではない社内からの質問に対して丁寧に日本語で答えてください。
---
参考情報:
{context}
---
質問: {question}
回答:
"""
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

def save_question_vector(question: str, embedding: list, path: str = "question_vectors.json"):
    # ドキュメントのembeddingを全部読み込む
    with open("vectorized_chunks.json", encoding="utf-8") as f:
        doc_data = json.load(f)
    all_embeddings = [item["embedding"] for item in doc_data] + [embedding]
    pca = PCA(n_components=3)
    reduced = pca.fit_transform(all_embeddings)
    # 質問は最後
    qx, qy, qz = reduced[-1][0], reduced[-1][1], reduced[-1][2]
    output = {
        'question': question,
        'x': float(qx),
        'y': float(qy),
        'z': float(qz)
    }
    with open('question_vectors_3d.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    data_q = {
        "question": question,
        "embedding": embedding
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_q, f, ensure_ascii=False, indent=2)

def main():
    print("質問をどうぞ (Ctrl+Cで終了)")
    with open(VECTOR_FILE, encoding="utf-8") as f:
        chunks = json.load(f)
    while True:
        try:
            question = input("\nQ: ")
            query_emb = get_embedding(question)
            save_question_vector(question, query_emb)  # 質問内容とベクトルを保存
            best, sim = find_most_similar(query_emb, chunks)
            if sim < SIM_THRESHOLD:
                print("A: その質問はまだドキュメント化されていないようです。")
                continue
            answer = ask_llm(best["chunk"], question)
            print(f"A: {answer}\n(参考: {best['url']})")
        except KeyboardInterrupt:
            print("\nばいばい👋")
            break
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()
