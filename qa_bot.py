import json
import numpy as np
import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

# --- .envからAPIキーを読み込む ---
load_dotenv()

# --- 設定 ---
VECTOR_FILE = "vectorized_chunks.json"
SIM_THRESHOLD = 0.5

# --- ユーティリティ ---
def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def get_embedding(text: str) -> List[float]:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "":
        print("[致命的エラー] GEMINI_API_KEYが設定されていません！.envや環境変数を確認してね！")
        exit(1)
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_query"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Gemini embedding取得エラー: {e}")
        return None

def find_most_similar(query_emb: List[float], chunks: List[dict]):
    sims = [cosine_similarity(query_emb, c["embedding"]) for c in chunks]
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
    import os
    import json
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append({
        "question": question,
        "embedding": embedding
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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
