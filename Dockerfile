# Étape 1 : base Python slim
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer torch CPU-only avant le reste
RUN pip install --no-cache-dir \
    torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==2.2.2+cpu \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

# S'assurer que le dossier app est bien un package Python
RUN touch app/__init__.py

# Générer les données et l'index au build (optionnel)
RUN python app/fetch_data.py && python app/indexer.py

# Exposer le port pour Uvicorn
EXPOSE 8000

# Commande pour lancer l'API
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
