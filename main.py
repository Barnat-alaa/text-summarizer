from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_handler import LLMHandler

app = FastAPI()

llm_handler = LLMHandler()


class SummarizeRequest(BaseModel):
    text: str

# Route pour vérifier l'état du serveur
@app.get("/health")
def health_check():
    """
    Ce point de terminaison vérifie si le serveur fonctionne.

    Retourne :
        dict : Un message indiquant que le serveur est en fonctionnement.

    Exceptions :
        HTTPException : Si le serveur ne fonctionne pas, retourne un code de statut 500 avec un message d'erreur.
    """
    try:
        # Simuler une vérification de l'état (par exemple, vérifier la connexion à la base de données, les services externes, etc.)
        # Si tout est en ordre, retourner un message de succès
        return {"status": "Le serveur est en fonctionnement"}
    except Exception as e:
        # Si quelque chose ne va pas, lever une HTTPException avec un code de statut 500
        raise HTTPException(status_code=500, detail="Le serveur ne fonctionne pas")
   


# Route pour résumer un texte
@app.post("/summarize")
def summarize_text(request: SummarizeRequest):
    """
    Reçoit un texte brut (format JSON) et retourne un résumé généré par le LLM.

    :param request: JSON payload with a "text" field.
    :return: Résumé du texte.
    """
    summary = llm_handler.summarize_text(request.text)
    if summary:
        return {"summary": summary}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du résumé")