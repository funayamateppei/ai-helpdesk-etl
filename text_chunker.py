from typing import List

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    if not text:
        return []
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def split_all_pages(pages: list, chunk_size: int = 500, overlap: int = 50) -> list:
    all_chunks = []
    for page in pages:
        page_id = page.get("id")
        page_url = page.get("url")
        text = page.get("text", "")
        if not text.strip():
            continue
        chunks = split_text(text, chunk_size=chunk_size, overlap=overlap)
        for chunk in chunks:
            all_chunks.append({
                "page_id": page_id,
                "url": page_url,
                "chunk": chunk
            })
    return all_chunks
