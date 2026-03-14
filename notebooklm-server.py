#!/usr/bin/env python3
"""
Connecteur REST API Claude-NotebookLM
Exposes NotebookLM content pour intégration avec Claude
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.auth.transport.requests
from google.oauth2 import service_account
import google.generativeai as genai
import os
import json
from typing import Optional

app = Flask(__name__)
CORS(app)

# Configuration
NOTEBOOKLM_API_KEY = os.getenv('NOTEBOOKLM_API_KEY')
PORT = os.getenv('PORT', 5000)

class NotebookLMConnector:
    """Connecteur pour accéder à NotebookLM"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
    
    def get_notebook(self, notebook_id: str) -> Optional[dict]:
        """Récupère un notebook NotebookLM spécifique"""
        try:
            # Récupère le contenu du notebook via l'API Google
            response = genai.get_notebook(notebook_id)
            return {
                'id': notebook_id,
                'content': response,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def query_notebook(self, notebook_id: str, query: str) -> dict:
        """Interroge un notebook avec une question"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(
                f"""Basé sur le notebook {notebook_id}, répondez à : {query}"""
            )
            return {
                'query': query,
                'response': response.text,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

# Initialiser le connecteur
connector = NotebookLMConnector(NOTEBOOKLM_API_KEY)

# Routes API

@app.route('/health', methods=['GET'])
def health():
    """Vérification de santé du serveur"""
    return jsonify({'status': 'healthy', 'service': 'claude-notebooklm-connector'})

@app.route('/api/notebooks/<notebook_id>', methods=['GET'])
def get_notebook(notebook_id):
    """Récupère un notebook spécifique"""
    result = connector.get_notebook(notebook_id)
    return jsonify(result)

@app.route('/api/query', methods=['POST'])
def query():
    """Envoie une requête à un notebook"""
    data = request.get_json()
    notebook_id = data.get('notebook_id')
    query_text = data.get('query')
    
    if not notebook_id or not query_text:
        return jsonify({'error': 'notebook_id et query sont requis'}), 400
    
    result = connector.query_notebook(notebook_id, query_text)
    return jsonify(result)

@app.route('/api/claude-integration', methods=['POST'])
def claude_integration():
    """Intégration directe avec Claude"""
    data = request.get_json()
    notebook_id = data.get('notebook_id')
    message = data.get('message')
    
    if not notebook_id or not message:
        return jsonify({'error': 'notebook_id et message sont requis'}), 400
    
    result = connector.query_notebook(notebook_id, message)
    return jsonify(result)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Erreur serveur interne'}), 500

if __name__ == '__main__':
    print(f'Démarrage du connecteur Claude-NotebookLM sur le port {PORT}')
    app.run(host='0.0.0.0', port=int(PORT), debug=True)
