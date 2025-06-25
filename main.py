from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import json
from typing import Dict, Any

app = FastAPI(
    title="PDF Text Extractor API",
    description="API pour extraire le texte des fichiers PDF",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les headers
)

@app.get("/")
async def root():
    """Route de base pour vérifier que l'API fonctionne"""
    return {"message": "PDF Text Extractor API is running!"}

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extrait le texte d'un fichier PDF uploadé
    
    Args:
        file: Fichier PDF à traiter
        
    Returns:
        Dict contenant le texte extrait
    """
    # Vérifier que le fichier est un PDF
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Le fichier doit être au format PDF"
        )
    
    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Extraire le texte avec pdfplumber
        extracted_text = ""
        
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += f"\n--- Page {page_num} ---\n"
                    extracted_text += page_text
                    extracted_text += "\n"
        
        # Si aucun texte n'a été extrait
        if not extracted_text.strip():
            return {
                "text": "Aucun texte n'a pu être extrait de ce PDF. Le fichier pourrait être une image ou un document scanné.",
                "pages_processed": len(pdf.pages) if 'pdf' in locals() else 0
            }
        
        return {
            "text": extracted_text.strip(),
            "filename": file.filename,
            "pages_processed": len(pdf.pages) if 'pdf' in locals() else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction du texte: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Route pour vérifier la santé de l'API"""
    return {"status": "healthy", "service": "PDF Text Extractor API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 