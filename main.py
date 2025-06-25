from fastapi import FastAPI, Request
from uuid import uuid4

app = FastAPI()

# Armazenamento em memória
project_db = {}

def safe_float(value):
    try:
        return float(str(value).replace(",", "."))
    except:
        return 0.0

@app.post("/submit_project/")
async def submit_project(request: Request):
    body = await request.json()

    project_id = str(uuid4())
    project_db[project_id] = {
        "projectName": body.get("projectName", "Projeto sem nome"),
        "status": body.get("status", "Desconhecido"),
        "physicalProgress": safe_float(body.get("physicalProgress", 0)),
        "financialProgress": safe_float(body.get("financialProgress", 0)),
        "hasRisks": body.get("hasRisks", "Não"),
        "notes": body.get("notes", "")
    }

    return {"projectId": project_id}

@app.get("/analyze_project/{project_id}")
async def analyze_project(project_id: str):
    project = project_db.get(project_id)

    if not project:
        return {"error": "Projeto não encontrado."}

    name = project["projectName"]
    status = project["status"]
    physical = project["physicalProgress"]
    financial = project["financialProgress"]
    risks = project["hasRisks"]
    notes = project["notes"]

    analysis = f"O projeto {name} está atualmente com status {status}. "
    analysis += f"O avanço físico é de {physical}% e o financeiro é de {financial}%. "

    if physical < financial:
        analysis += "Há um possível excesso de gastos em relação ao progresso físico. "
        explanation = "Isso indica que o projeto pode estar gastando mais do que deveria para o nível de execução atual."
    elif financial < physical:
        analysis += "O projeto está avançando fisicamente mais rápido do que o orçamento está sendo executado. "
        explanation = "Isso pode indicar eficiência na execução ou atraso nos repasses financeiros."
    else:
        analysis += "O avanço físico e financeiro estão equilibrados. "
        explanation = "Isso sugere que o projeto está seguindo o cronograma e orçamento conforme o planejado."

    if risks.lower() == "sim":
        analysis += f"⚠️ Foi identificado um risco: {notes}. "
        analysis += "Isso pode impactar o cronograma e o orçamento do projeto. "

    recommendation = "✅ Recomendação: "
    if "equipamento" in notes.lower() or "logística" in notes.lower() or "suprimentos" in notes.lower():
        recommendation += (
            "A equipe responsável pela entrega de equipamentos deve considerar realocar o tempo ocioso para outras frentes do projeto, como planejamento ou testes. "
            "Essa recomendação visa evitar desperdício de tempo e manter o ritmo de avanço em outras áreas enquanto o problema logístico é resolvido."
        )
    else:
        recommendation += (
            "Recomenda-se revisar o plano de ação e reforçar a comunicação entre as áreas envolvidas. "
            "Essa medida ajuda a mitigar riscos e alinhar expectativas entre os times."
        )

    full_response = f"✅ Análise concluída!\n\n{analysis.strip()}\n\nℹ️ {explanation}\n\n{recommendation.strip()}"
    return full_response
