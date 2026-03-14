# Guide d'Installation - Claude NotebookLM Connector

## Conditions Préalables

- Python 3.8+
- pip (Python Package Manager)
- Clé API Google pour NotebookLM
- Docker (optionnel, pour le déploiement en conteneur)

## Installation Locale

### Étape 1: Cloner le Repository

```bash
git clone https://github.com/lebacfrancais21-stack/claude-notebooklm-connector.git
cd claude-notebooklm-connector
```

### Étape 2: Créer un Environnement Virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### Étape 3: Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4: Configurer les Variables d'Environnement

```bash
cp .env.example .env
```

Modifiez `.env` avec vos clés API :

```
NOTEBOOKLM_API_KEY=votre_clé_api_google
CLAUDE_API_KEY=votre_clé_claude
PORT=5000
```

### Étape 5: Démarrer le Serveur

```bash
python notebooklm-server.py
```

Le serveur sera disponible sur `http://localhost:5000`

## Déploiement avec Docker

### Build l'Image

```bash
docker build -t claude-notebooklm-connector:latest .
```

### Exécuter le Conteneur

```bash
docker run -p 5000:5000 \
  -e NOTEBOOKLM_API_KEY=votre_clé \
  -e CLAUDE_API_KEY=votre_clé \
  claude-notebooklm-connector:latest
```

## Vérification de l'Installation

Testez le serveur :

```bash
curl http://localhost:5000/health
```

Vous devriez recevoir :

```json
{"status": "healthy", "service": "claude-notebooklm-connector"}
```

## Intégration avec Claude

Une fois le serveur en cours d'exécution, vous pouvez accéder à vos NotebookLM via l'endpoint : `http://localhost:5000/api/claude-integration`
