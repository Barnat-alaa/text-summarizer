from openai import OpenAI

class LLMHandler:
    def __init__(self):

        self.client = OpenAI(
            base_url="https://api.scaleway.ai/v1",
            api_key="f8f289d6-97e8-4933-a643-896f4166ade0"
        )
        self.model = "llama-3.1-70b-instruct"  

    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Envoie une requête au modèle de langage pour résumer le texte.

        :param text: Texte à résumer.
        :param max_length: Longueur maximale du résumé .
        :return: Le résumé généré par le modèle et gere les erreurs avec les Exceptions.
        """
        try:
            if len(text) > 10000:
                raise ValueError("Le texte est trop long pour être traité.")

            
            response = self.client.chat.completions.create(
                model=self.model,
                messages = [
                    {"role": "system", "content": "Tu es un assistant spécialisé dans la synthèse de textes. Chaque phrase que tu produis doit être concise, complète et se terminer correctement.Tu dois aussi réspécter la limitation de nombre de mots imposé."},
                    {"role": "user", "content": f"Résume ce texte en {max_length} mots maximum. Commence directement par le résumé, sans introduction. Le résumé doit être composé de trois phrases très courtes et précises : {text}"}
                ],
                # max_tokens= (max_length + 50), //J'ai supprimé cette limitation, car elle interrompait les messages de manière abrupte au milieu d'une phrase.
                stop=["\n"]
            )

            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            print(f"Erreur lors de la génération du résumé : {e}")
            raise  

    def check_api(self) -> bool:
        
        try:
            # Envoie une requête de test simple pour vérifier la connectivité de l'API
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui répond à des questions."},
                    {"role": "user", "content": "Réponds simplement par 'OK'."}
                ],
                max_tokens=5  # Limite la réponse à 5 tokens pour économiser des ressources
            )

            # Vérifie si la réponse est valide
            if test_response.choices[0].message.content.strip().lower() == "ok":
                return True
            else:
                return False

        except Exception as e:
            print(f"Erreur lors de la vérification de l'API : {e}")
            return False