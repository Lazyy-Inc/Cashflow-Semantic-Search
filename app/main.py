import json
import numpy as np
import faiss
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# CHEMINS ABSOLUS
index = faiss.read_index("/app/index.faiss")
with open("/app/meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

app = FastAPI(title="Semantic Search API")

@app.get("/search")
def search(query: str = Query(..., description="Transaction name à chercher")):
    embedding = model.encode([query], normalize_embeddings=True)
    embedding = np.array(embedding, dtype=np.float32)

    scores, ids = index.search(embedding, k=3)
    results = []
    for i, idx in enumerate(ids[0]):
        results.append({
            "match": meta[idx],
            "score": float(scores[0][i])
        })

    return {"query": query, "results": results}
