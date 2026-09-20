import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend online!"}

@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        return {"response": "Erro: GEMINI_API_KEY não configurada no Render."}
    
    try:
        # Inicializa o cliente oficial da Google
        client = genai.Client(api_key=GEMINI_API_KEY.strip())
        
        # Lista de modelos para tentar (o 1.5-flash possui cota diária alta)
        models_to_try = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-3.6-flash"]
        
        for model_id in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=req.message,
                )
                if response and response.text:
                    return {"response": response.text}
            except Exception:
                continue
                
        return {"response": "Limite de requisições temporariamente atingido. Aguarde cerca de 1 minuto e tente novamente."}
        
    except Exception as e:
        return {"response": f"Erro no serviço da API: {str(e)}"}
