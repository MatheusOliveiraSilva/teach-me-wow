import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

project_root_path = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root_path))

from apps.teacher_agent.api.routers import agent_router
from apps.teacher_agent.api.core.config import API_PREFIX

app = FastAPI(
    title="TeachMeWow Agent API",
    description="API para interagir com o agente de IA do TeachMeWow.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router.router, prefix=API_PREFIX)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 