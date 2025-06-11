import json
from sklearn.decomposition import PCA

with open('vectorized_chunks.json', encoding='utf-8') as f:
    data = json.load(f)

embeddings = [item['embedding'] for item in data]
pca = PCA(n_components=3)
reduced = pca.fit_transform(embeddings)

output = []
for i, item in enumerate(data):
    output.append({
        'chunk': item['chunk'],
        'url': item['url'],
        'x': reduced[i, 0],
        'y': reduced[i, 1],
        'z': reduced[i, 2]
    })

with open('vectorized_chunks_3d.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)