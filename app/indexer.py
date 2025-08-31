import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Chargement du modèle
model = SentenceTransformer("intfloat/multilingual-e5-large")

# CHEMIN ABSOLU
with open("/app/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts, meta = [], []
empty_count = 0

for cat in data:
    if not cat.get("name"):
        print(f"⚠️ Catégorie ignorée (nom vide): ID {cat.get('id')}")
        continue
        
    for sub in cat.get("subcategories", []):
        if not sub.get("name"):
            print(f"⚠️ Sous-catégorie ignorée (nom vide): ID {sub.get('id')}")
            continue
            
        for txn in sub.get("transactions", []):
            # Vérification robuste du nom
            txn_name = txn.get("name")
            if not txn_name or not isinstance(txn_name, str) or txn_name.strip() == "":
                empty_count += 1
                continue
                
            texts.append(txn_name.strip())
            meta.append({
                "id": sub["id"],
                "parent": cat["id"],
                "initialTransactionName": txn_name.strip(),
                "categoryName": cat["name"],
                "subCategoryName": sub["name"]
            })

print(f"📊 Statistiques:")
print(f"   - Transactions valides: {len(texts)}")
print(f"   - Transactions ignorées (noms vides): {empty_count}")

if not texts:
    print("❌ Aucune transaction valide à encoder!")
    exit(1)

# Encodage
embeddings = model.encode(texts, normalize_embeddings=True)
dimension = embeddings.shape[1]

# Création de l'index FAISS
index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings, dtype=np.float32))

# Sauvegarde
faiss.write_index(index, "/app/index.faiss")
with open("/app/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"✅ Index créé avec {len(texts)} transactions")
