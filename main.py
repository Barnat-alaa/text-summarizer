from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from llm_handler import LLMHandler
from sqlalchemy.orm import Session
from database import SessionLocal, Summary, engine, Base

Base.metadata.create_all(bind=engine) #i added this to create the summary.db file when it launches

app = FastAPI()

llm_handler = LLMHandler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SummarizeRequest(BaseModel):
    text: str  

#route qui envoie un message d'acceuil
@app.get("/")
def welcome_message():
    return {
        "message": "Bienvenue ! Ceci est un serveur FastAPI pour résumer des textes."
    }

# Route pour vérifier l'état du serveur
@app.get("/health")
def health_check():
    """
    Ce point de terminaison vérifie si le serveur et l'API fonctionnent.

    Retourne :
        dict : Un message indiquant que le serveur est en fonctionnement.

    Exceptions :
        HTTPException : Si le serveur ou l'API ne fonctionne pas, retourne un code de statut 500 avec un message d'erreur.
    """
    try:
        # Vérifie si l'API fonctionne
        if not llm_handler.check_api():
            raise Exception("L'API de résumé de texte ne fonctionne pas.")

        return {"status": "Le serveur est en fonctionnement"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Le serveur ne fonctionne pas : {str(e)}")
   

# Route pour résumer un texte
@app.post("/summarize")
def summarize_text(request: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Reçoit un texte brut (format JSON) et retourne un résumé généré par le LLM.
    Enregistre également le texte et le résumé dans la base de données.

    :param request: JSON payload with a "text" field.
    :return: Résumé du texte et ID de l'entrée dans la base de données.
    """
    # générer le résumé via llm_handler
    summary = llm_handler.summarize_text(request.text)
    if not summary:
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du résumé")

    # enregistre le texte et le résumé dans la data base
    try:
        db_summary = Summary(text=request.text, summarized_text=summary)
        db.add(db_summary)
        db.commit()
        db.refresh(db_summary)
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")  # Log the full error message
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement dans la base de données: {str(e)}")

    # Envoyer le résumé et l'ID de l'entrée dans la base de données
    return {"summary": summary, "id": db_summary.id}