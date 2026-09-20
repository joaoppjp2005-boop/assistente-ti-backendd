import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Permite chamadas de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Captura erros globais para não derrubar as permissões de CORS
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={"response": f"Erro interno do servidor: {str(exc)}"}
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
        return {"response": "Erro: GEMINI_API_KEY não foi configurada nas variáveis do Render."}
    
    try:
        clean_key = GEMINI_API_KEY.strip()
        genai.configure(api_key=clean_key)
        
        # Modelo rápido e otimizado
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(req.message)
        
        if response and response.text:
            return {"response": response.text}
        else:
            return {"response": "A IA não retornou um texto válido. Tente novamente."}
            
    except Exception as e:
        return {"response": f"Erro na chamada do Gemini: {str(e)}"}
