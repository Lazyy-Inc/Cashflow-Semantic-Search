import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOLGEE_API_KEY = os.getenv("TOLGEE_API_KEY")
TOLGEE_URL = os.getenv("TOLGEE_URL")
CATEGORY_URL = os.getenv("CATEGORY_URL")
CATEGORY_API_KEY = os.getenv("CATEGORY_API_KEY")

# Fetch traductions
resp = requests.get(
    TOLGEE_URL,
    headers={
        "Accept": "application/json",
        "X-API-Key": TOLGEE_API_KEY
    }
)
translations = resp.json().get("en", {})

# Fetch catégories
categories = requests.get(
    CATEGORY_URL,
    headers={
        "Accept": "application/json",
        "X-API-Key": CATEGORY_API_KEY
    }
).json()

def translate_key(key: str) -> str:
    return translations.get(key, key)

# Remplacer clés par traductions
for cat in categories:
    cat["name"] = translate_key(cat["name"])
    for sub in cat.get("subcategories", []):
        sub["name"] = translate_key(sub["name"])

# Sauvegarde - CHEMIN ABSOLU
data_path = "/app/data.json"
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print(f"✅ Données traduites sauvegardées dans {data_path}")
