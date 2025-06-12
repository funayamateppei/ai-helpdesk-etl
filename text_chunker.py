from typing import List
import re

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    if not text:
        return []
    sentences = re.split(r'(?<=[。.!?\n])', text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) > chunk_size:
            if current:
                chunks.append(current)
            # overlap分だけ前の文を残す
            if overlap > 0 and chunks:
                overlap_text = current[-overlap:]
                current = overlap_text + sent
            else:
                current = sent
        else:
            current += sent
    if current:
        chunks.append(current)
    return [c.strip() for c in chunks if c.strip()]


def split_all_pages(pages: list, chunk_size: int = 500, overlap: int = 50) -> list:
    all_chunks = []
    for page in pages:
        page_id = page.get("id")
        page_url = page.get("url")
        page_title = page.get("title", "")
        text = page.get("text", "")
        if not text.strip():
            continue
        chunks = split_text(text, chunk_size=chunk_size, overlap=overlap)
        for chunk in chunks:
            chunk_with_title = f"【{page_title}】\n{chunk}"
            all_chunks.append({
                "page_id": page_id,
                "url": page_url,
                "chunk": chunk_with_title
            })
    return all_chunks
