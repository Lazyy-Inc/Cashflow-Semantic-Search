import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Chargement du modèle
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# CHEMIN ABSOLU
with open("/app/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts, meta = [], []
empty_count = 0
valid_subcats = 0

for cat in data:
    if not cat.get("name"):
        print(f"⚠️ Catégorie ignorée (nom vide): ID {cat.get('id')}")
        continue

    cat_desc = cat.get("description", "").strip()
    cat_context = f"Category: {cat['name']}. {cat_desc}" if cat_desc else f"Category: {cat['name']}"

    for sub in cat.get("subcategories", []):
        if not sub.get("name"):
            print(f"⚠️ Sous-catégorie ignorée (nom vide): ID {sub.get('id')}")
            continue

        sub_desc = sub.get("description", "").strip()
        sub_context = f"SubCategory: {sub['name']}. {sub_desc}" if sub_desc else f"SubCategory: {sub['name']}"

        # Récupérer les transactions valides
        txn_names = [
            txn["name"].strip()
            for txn in sub.get("transactions", [])
            if txn.get("name") and isinstance(txn.get("name"), str) and txn["name"].strip() != ""
        ]

        if not txn_names:
            empty_count += 1
            continue

        valid_subcats += 1

        # On regroupe les transactions comme mots-clés
        keywords = ", ".join(txn_names)
        full_text = f"{sub_context} - {cat_context} - keywords: {keywords}"

        texts.append(full_text)
        meta.append({
            "id": sub["id"],
            "parent": cat["id"],
            "categoryName": cat["name"],
            "subCategoryName": sub["name"],
            "categoryDescription": cat_desc,
            "subCategoryDescription": sub_desc,
            "keywords": txn_names  # on garde la liste brute pour usage futur
        })

print(f"📊 Statistiques:")
print(f"   - Sous-catégories valides: {valid_subcats}")
print(f"   - Sous-catégories ignorées (aucune transaction): {empty_count}")

if not texts:
    print("❌ Aucune sous-catégorie valide à encoder!")
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

print(f"✅ Index créé avec {len(texts)} sous-catégories")

