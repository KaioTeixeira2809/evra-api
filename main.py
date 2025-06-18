from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProjectData(BaseModel):
    projectName: str
    status: str
    physicalProgress: float
    financialProgress: float
    hasRisks: str
    riskDescription: str
    notes: str

@app.post("/analyze_project/")
def analyze_project(data: ProjectData):
    projectName = data.projectName
    status = data.status
    physical = data.physicalProgress
    financial = data.financialProgress
    hasRisks = data.hasRisks.lower()
    riskDescription = data.riskDescription
    notes = data.notes

    delay = "Alta" if physical < 70 else ("Média" if physical < 90 else "Baixa")
    budget = "Alta" if financial > 80 else ("Média" if financial > 60 else "Baixa")
    risk = "Alto" if hasRisks == "sim" else "Baixo"

    recommendations = []
    if delay == "Alta":
        recommendations.append("Reavaliar o cronograma.")
    if budget == "Alta":
        recommendations.append("Revisar o orçamento.")
    if risk == "Alto":
        recommendations.append("Mitigar riscos identificados.")

    summary = f"""
Projeto: {projectName}
- Status: {status}
- Avanço físico: {physical}%
- Avanço financeiro: {financial}%
- Riscos: {riskDescription if hasRisks == 'sim' else 'Nenhum'}

Análise:
- Atraso: {delay}
- Orçamento: {budget}
- Risco geral: {risk}

Recomendações:
- {'\\n- '.join(recommendations)}

Observações: {notes}
"""

    return {"summary": summary}
