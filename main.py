import os
from google import genai

# Garante que o cliente pega a chave do ambiente do Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = "AQ.Ab8RN6JNNH6la6C84sK4PdpsOKtdPS73lmUIRubtlSnaaiS5PA"
client = genai.Client(api_key=api_key)

@app.post("/chat")
async def chat_endpoint(payload: dict):
    user_message = payload.get("message") or payload.get("prompt") or payload.get("texto") or ""
    response_text = ""
    
    # 1ª Tentativa: Modelo principal
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_message,
        )
        response_text = response.text
    except Exception as e:
        print("Modelo principal instável, tentando fallback...", e)
        # 2ª Tentativa: Modelo secundário
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=user_message,
            )
            response_text = response.text
        except Exception as err:
            print("ERRO DETALHADO NO BACKEND:", err)
            raise HTTPException(status_code=500, detail=str(err))
            
    # Retorno compatível com qualquer frontend
    return {
        "response": response_text,
        "reply": response_text,
        "resposta": response_text,
        "message": response_text
    }