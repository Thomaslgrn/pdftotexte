# PDF Text Extractor API

Une API FastAPI pour extraire automatiquement le texte des fichiers PDF.

## Fonctionnalités

- Upload de fichiers PDF via une route POST
- Extraction automatique du texte avec pdfplumber
- Support CORS pour les applications frontend
- Validation des types de fichiers
- Gestion d'erreurs robuste
- Prêt pour le déploiement sur Render.com

## Installation locale

1. Cloner le repository
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l'API :
```bash
python main.py
```

Ou avec uvicorn directement :
```bash
uvicorn main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

## Utilisation

### Route principale
- `GET /` - Vérification que l'API fonctionne

### Extraction de texte
- `POST /extract` - Upload et extraction du texte d'un PDF

**Exemple avec curl :**
```bash
curl -X POST "http://localhost:8000/extract" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf"
```

**Réponse JSON :**
```json
{
  "text": "Contenu extrait du PDF...",
  "filename": "document.pdf",
  "pages_processed": 3
}
```

### Vérification de santé
- `GET /health` - Statut de l'API

## Documentation API

Une fois l'API lancée, la documentation interactive est disponible sur :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## Déploiement sur Render.com

1. Pousser le code sur GitHub
2. Connecter le repository à Render.com
3. Créer un nouveau Web Service
4. Le fichier `render.yaml` configure automatiquement le déploiement

### Variables d'environnement
- `PORT` : Port automatiquement défini par Render
- `PYTHON_VERSION` : Version Python (3.11.0)

## Structure du projet

```
pdftotrext_fastapi/
├── main.py              # Application FastAPI principale
├── requirements.txt     # Dépendances Python
├── render.yaml         # Configuration Render.com
└── README.md           # Documentation
```

## Technologies utilisées

- **FastAPI** : Framework web moderne et rapide
- **pdfplumber** : Extraction de texte depuis les PDF
- **uvicorn** : Serveur ASGI
- **python-multipart** : Gestion des uploads de fichiers

## Limitations

- Fonctionne uniquement avec des PDF contenant du texte (pas d'OCR)
- Les PDF scannés ne peuvent pas être traités
- Taille de fichier limitée par la configuration du serveur 