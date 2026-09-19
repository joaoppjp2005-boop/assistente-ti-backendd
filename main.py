import os
from fastapi import FastAPI, HTTPException
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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY.strip())

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend online!"}

@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    try:
        # Tenta o modelo principal
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(req.message)
        return {"response": response.text}
    except Exception as e:
        # Fallback para o modelo alternativo caso o 1.5-flash falhe
        try:
            model_fallback = genai.GenerativeModel("gemini-pro")
            response = model_fallback.generate_content(req.message)
            return {"response": response.text}
        except Exception as err_fallback:
            print(f"ERRO DETALHADO NO BACKEND: {str(e)} | FALLBACK: {str(err_fallback)}")
            raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")
