from fastapi import FastAPI, Request

app = FastAPI()

# Função para converter texto em número com segurança
def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except:
        return 0.0

@app.post("/analyze_project/")
async def analyze_project(request: Request):
    body = await request.json()

    # Pega os dados do corpo da requisição
    project_name = body.get("projectName", "Projeto sem nome")
    status = body.get("status", "Desconhecido")
    physical = safe_float(body.get("physicalProgress", 0))
    financial = safe_float(body.get("financialProgress", 0))
    risks = body.get("hasRisks", "Não")
    notes = body.get("notes", "")

    # Análise
    analysis = f"O projeto **{project_name}** está atualmente com status **{status}**. "
    analysis += f"O avanço físico é de **{physical}%** e o financeiro é de **{financial}%**. "

    # Interpretação
    if physical < financial:
        analysis += "Há um possível excesso de gastos em relação ao progresso físico. "
        explanation = "Isso indica que o projeto pode estar gastando mais do que deveria para o nível de execução atual."
    elif financial < physical:
        analysis += "O projeto está avançando fisicamente mais rápido do que o orçamento está sendo executado. "
        explanation = "Isso pode indicar eficiência na execução ou atraso nos repasses financeiros."
    else:
        analysis += "O avanço físico e financeiro estão equilibrados. "
        explanation = "Isso sugere que o projeto está seguindo o cronograma e orçamento conforme o planejado."

    # Riscos
    if risks.lower() == "sim":
        analysis += f"⚠️ Foi identificado um risco: *{notes}*. "
        analysis += "Isso pode impactar o cronograma e o orçamento do projeto. "

    # Recomendação com explicação
    recommendation = "✅ **Recomendação:** "
    if "equipamento" in notes.lower() or "logística" in notes.lower():
        recommendation += (
            "A equipe responsável pela entrega de equipamentos deve considerar realocar o tempo ocioso para outras frentes do projeto, como planejamento ou testes. "
            "Essa recomendação visa evitar desperdício de tempo e manter o ritmo de avanço em outras áreas enquanto o problema logístico é resolvido."
        )
    else:
        recommendation += (
            "Recomenda-se revisar o plano de ação e reforçar a comunicação entre as áreas envolvidas. "
            "Essa medida ajuda a mitigar riscos e alinhar expectativas entre os times."
        )

    # Resposta final formatada
    full_response = f"✅ Análise concluída!\n\n{analysis.strip()}\n\nℹ️ {explanation}\n\n{recommendation.strip()}"
    return full_response

