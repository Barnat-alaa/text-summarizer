FROM python:3.9-slim

WORKDIR /app

#copier les fichiers dans le conteneur
COPY requirements.txt .
COPY main.py .
COPY database.py .
COPY llm_handler.py .

#installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

#le port d'écoute
EXPOSE 8000

#lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]