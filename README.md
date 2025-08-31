# Cashflow Semantic Search API

API de recherche sémantique pour les catégories et sous-catégories de transactions cashflow, utilisant l'IA pour comprendre l'intention derrière les requêtes.

## 🚀 Fonctionnalités

- **Recherche sémantique** : Comprend le sens des transactions plutôt que juste le texte
- **Embeddings** : Utilise le modèle `all-MiniLM-L6-v2` de SentenceTransformers
- **Index FAISS** : Recherche ultra-rapide grâce à l'indexation vectorielle
- **API REST** : Interface FastAPI avec documentation interactive
- **Traductions automatiques** : Intégration avec Tolgee pour les traductions

## 📦 Architecture

```
cashflow-semantic-search/
├── app/
│   ├── fetch_data.py      # Récupération données + traductions
│   ├── indexer.py         # Création index FAISS
│   ├── main.py            # API FastAPI
│   └── __init__.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Installation

### Prérequis

- Docker et Docker Compose
- Python 3.11+ (pour développement local)
- Clés API Tolgee (optionnel)

### Avec Docker (Recommandé)

```bash
# Cloner le repository
git clone git@github.com:lazyy-inc/cashflow-semantic-search.git
cd cashflow-semantic-search

# Copier les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Construire et lancer
docker-compose up --build

# L'API sera disponible sur http://localhost:8078
```

### Développement local

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos variables

# Générer les données et l'index
python app/fetch_data.py
python app/indexer.py

# Lancer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ⚙️ Configuration

Variables d'environnement requises :

```env
# Tolgee Translation API
TOLGEE_API_KEY=your_tolgee_api_key
TOLGEE_URL=https://app.tolgee.io/v2/projects/123/translations

# Categories API
CATEGORY_URL=https://api.example.com/categories
```

## 📡 API Endpoints

### 🔍 Recherche sémantique

**GET** `/search?query=string`

Recherche les catégories correspondant sémantiquement à la requête.

**Exemple :**
```bash
curl "http://localhost:8078/search?query=restaurant"
```

**Réponse :**
```json
{
  "query": "restaurant",
  "results": [
    {
      "match": {
        "id": 123,
        "name": "Restaurants",
        "type": "category"
      },
      "score": 0.856
    },
    {
      "match": {
        "id": 456,
        "name": "Fast Food",
        "parent": 123,
        "type": "subcat"
      },
      "score": 0.723
    }
  ]
}
```

### 📚 Documentation Interactive

L'API inclut une documentation automatique :

- **Swagger UI** : http://localhost:8078/docs
- **ReDoc** : http://localhost:8078/redoc

## 🏗️ Workflow de développement

### Mise à jour des données

1. Modifier les sources de données dans `.env`
2. Régénérer les données :
```bash
python app/fetch_data.py
python app/indexer.py
```

### Ajouter un nouveau modèle

1. Modifier `indexer.py` avec le nouveau modèle
2. Régénérer l'index FAISS
3. Mettre à jour `main.py` pour charger le nouveau modèle

## 🐛 Dépannage

### Problèmes courants

**Erreur de connexion API :**
- Vérifier les variables d'environnement
- Vérifier la connectivité réseau

**Index FAISS manquant :**
```bash
python app/fetch_data.py
python app/indexer.py
```

**Problèmes de mémoire :**
- Réduire la taille du batch dans `indexer.py`
- Utiliser un modèle plus léger

### Logs et monitoring

```bash
# Voir les logs Docker
docker-compose logs -f semantic-search

# Entrer dans le conteneur
docker exec -it semantic-search /bin/bash
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📊 Performance

- Temps de réponse : < 100ms pour la plupart des requêtes
- Supporte jusqu'à 1000 requêtes simultanées
- Index FAISS avec recherche approximative pour la vitesse

## 🔮 Améliorations futures

- [ ] Cache Redis pour les résultats fréquents
- [ ] Endpoint batch pour multiples requêtes
- [ ] Métriques et monitoring Prometheus
- [ ] Tests unitaires et d'intégration
- [ ] Support multi-langues
- [ ] Interface web de démonstration

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Équipe

Développé par l'équipe **Lazyy** - Simplifiant la gestion financière grâce à l'IA.

---

**Note** : Assurez-vous de ne jamais commiter les fichiers `.env` ou les clés API dans le repository!
```

## Fichier supplémentaire recommandé : `.env.example`

Créez aussi un fichier `.env.example` :

```env
# Tolgee Translation API
TOLGEE_API_KEY=your_tolgee_api_key_here
TOLGEE_URL=https://app.tolgee.io/v2/projects/your-project-id/translations

# Categories API
CATEGORY_URL=https://api.yourdomain.com/categories

# Optional: Debug settings
DEBUG=true
LOG_LEVEL=INFO
```
