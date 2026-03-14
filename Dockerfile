# Image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 5000

# Définir les variables d'environnement
ENV FLASK_APP=notebooklm-server.py
ENV FLASK_ENV=production

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "notebooklm-server:app"]
