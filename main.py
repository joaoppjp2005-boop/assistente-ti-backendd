import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

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

# Esta é a rota que o frontend chama
@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        return {"response": "Erro: GEMINI_API_KEY não configurada no Render."}
    
    try:
        genai.configure(api_key=GEMINI_API_KEY.strip())
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(req.message)
        
        if response and response.text:
            return {"response": response.text}
        return {"response": "Sem resposta do modelo."}
    except Exception as e:
        return {"response": f"Erro na API: {str(e)}"}
