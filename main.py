from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/analyze_project/")
async def analyze_project(request: Request):
    body = await request.json()
    print("📦 Corpo recebido:", body)
    return {"debug": body}
