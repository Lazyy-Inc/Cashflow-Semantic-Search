import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# CHEMIN ABSOLU
with open("/app/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts, meta = [], []
for cat in data:
    texts.append(cat["name"])
    meta.append({"id": cat["id"], "name": cat["name"], "type": "category"})

    for sub in cat.get("subcategories", []):
        texts.append(sub["name"])
        meta.append({
            "id": sub["id"],
            "name": sub["name"],
            "parent": cat["id"],
            "type": "subcat"
        })

embeddings = model.encode(texts, normalize_embeddings=True)
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings, dtype=np.float32))

# CHEMINS ABSOLUS
faiss.write_index(index, "/app/index.faiss")
with open("/app/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"✅ Index FAISS créé avec {len(texts)} entrées.")
