# Text Summarizer API

This is a mini-application that summarizes text using a Large Language Model (LLM) via an API built with FastAPI.The application allows users to submit text and receive a summarized version, which is also stored in a SQLite database for future reference.

-To visualize the servers API i used /docs at the end of URL
-To visualize the local Database (SQLite) I used DB Browser (SQLite) 

---

## **Features**
- **Text Summarization**: Summarize long text using a Generative API from Scaleaway which is Llama-3.1-70b-instruct.
- **FastAPI Backend**: A lightweight and fast API framework for handling requests .
- **Database Storage**: Stores the original text and its summary in a SQLite database.
- **Docker Support**: Easy deployment using Docker.

---
## **Setup and Installation**
### **Option 1: Using Docker**
1. Pull the Docker image:
docker pull barnatalaa/text_summarizer:3.0
2. Run the container:
docker run -d -p 8000:8000 --name text_summarizer_container barnatalaa/text_summarizer:3.0
3. Access the API at:
http://localhost:8000
### **Option 2: Running locally**
1. clone the repository:
git clone https://github.com/Barnat-alaa/text-summarizer.git
2. Access the application folder:
cd text-summarizer
3. Temporarily Allow Script Execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
4. Activate Python Virtual Environment
.\venv\Scripts\activate 
5. Install dependencies:
pip install -r requirements.txt
6. Run the FastAPI server:
uvicorn main:app --reload 
7. Access the API at:
http://localhost:8000

---
## **API Endpoints**
### **Endpoint: GET /**
Returns a welcome message.
### **Endpoint: GET /health**
Checks if the server and LLM API are functioning.
### **Endpoint: POST /summarize**
Summarizes the provided text and stores it in the database.
