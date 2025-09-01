import json
import numpy as np
import faiss
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# CHEMINS ABSOLUS
index = faiss.read_index("/app/index.faiss")
with open("/app/meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

app = FastAPI(title="Semantic Search API")

@app.get("/search")
def search(query: str = Query(..., description="Transaction name à chercher")):
    embedding = model.encode([query], normalize_embeddings=True)
    embedding = np.array(embedding, dtype=np.float32)

    scores, ids = index.search(embedding, k=5)  # Augmenté à 5 résultats
    
    results = []
    for i, idx in enumerate(ids[0]):
        item = meta[idx]
        # Format exact demandé
        result = {
            "id": item["id"],  # ID de la sous-catégorie
            "parent": item["parent"],  # ID de la catégorie
#            "initialTransactionName": item["initialTransactionName"],
            "categoryName": item["categoryName"],
            "subCategoryName": item["subCategoryName"]
        }
        results.append({
            "match": result,
            "score": float(scores[0][i])
        })

    return {"query": query, "results": results}
