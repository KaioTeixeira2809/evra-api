from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/analyze_project/")
async def analyze_project(request: Request):
    body = await request.json()

    # Pega os dados do corpo da requisição
    project_name = body.get("projectName", "Projeto sem nome")
    status = body.get("status", "Desconhecido")
    physical = float(body.get("physicalProgress", 0))
    financial = float(body.get("financialProgress", 0))
    risks = body.get("hasRisks", "Não")
    notes = body.get("notes", "")

    # Análise simples baseada nos dados
    analysis = f"O projeto **{project_name}** está atualmente com status **{status}**. "
    analysis += f"O avanço físico é de **{physical}%** e o financeiro é de **{financial}%**. "

    # Interpretação
    if physical < financial:
        analysis += "Há um possível excesso de gastos em relação ao progresso físico. "
    elif financial < physical:
        analysis += "O projeto está avançando fisicamente mais rápido do que o orçamento está sendo executado. "
    else:
        analysis += "O avanço físico e financeiro estão equilibrados. "

    # Riscos
    if risks.lower() == "sim":
        analysis += f"⚠️ Foi identificado um risco: *{notes}*. "
        analysis += "Isso pode impactar o cronograma e o orçamento do projeto. "

    # Recomendação
    recommendation = "✅ **Recomendação:** "
    if "equipamento" in notes.lower() or "logística" in notes.lower():
        recommendation += "A equipe responsável pela entrega de equipamentos deve considerar realocar o tempo ocioso para outras frentes do projeto, como planejamento ou testes. "
    else:
        recommendation += "Recomenda-se revisar o plano de ação e reforçar a comunicação entre as áreas envolvidas. "

    # Resposta final
    return {
        "resumo": analysis.strip(),
        "recomendacao": recommendation.strip()
    }
