from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Modelo de entrada para o endpoint de texto livre
class FreeformInput(BaseModel):
    description: str

# Função que interpreta a descrição do projeto
def interpretar_descricao(texto: str) -> str:
    # Aqui você pode usar NLP ou regex para extrair dados reais
    # Por enquanto, vamos simular uma análise simples
    linhas = texto.strip().split("\n")
    resposta = ["📊 Análise do Projeto com base na descrição recebida:\n"]

    for linha in linhas:
        if linha.strip():
            resposta.append(f"• {linha.strip()}")

    resposta.append("\n✅ Recomendação: Monitorar riscos e revisar cronograma.")
    return "\n".join(resposta)

# Endpoint que recebe a descrição e retorna a análise
@app.post("/analyze_freeform/")
def analyze_freeform(data: FreeformInput):
    analysis = interpretar_descricao(data.description)
    return analysis

# Para rodar localmente (opcional)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
