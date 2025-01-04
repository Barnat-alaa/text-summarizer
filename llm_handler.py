from openai import OpenAI

class LLMHandler:
    def __init__(self):

        self.client = OpenAI(
            base_url="https://api.scaleway.ai/v1",
            api_key="f8f289d6-97e8-4933-a643-896f4166ade0"
        )
        self.model = "llama-3.1-70b-instruct"  

    def summarize_text(self, text: str, max_length: int = 100) -> str:
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
                messages=[
                {"role": "system", "content": "Tu es un assistant qui résume des textes. Assure-toi que chaque phrase est complète et se termine correctement."},
                {"role": "user", "content": f"Résume ce texte en {max_length} mots maximum. Ne commence pas la réponse par 'Voici un résumé du texte'. Écris directement le résumé, en t'assurant que chaque phrase est complète : {text} et je veux 3 trés courtes phrases qui résument le texte."}
                ],
                # max_tokens= (max_length + 50),
                stop=["\n"]
            )

            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            print(f"Erreur lors de la génération du résumé : {e}")
            raise  