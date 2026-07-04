from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI(title="AmkyawDev Tools",description="AI-powered coding platform",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/health")
async def health_check():
    return{"status":"healthy","service":"amkyawdev-tools"}
@app.get("/")
async def root():
    return{"message":"AmkyawDev Tools API","docs":"/docs"}
try:
    from app.api.routes.agent import router as agent_router
    app.include_router(agent_router,prefix="/api/agent",tags=["Agent"])
except ImportError:pass
try:
    from app.api.routes.knowledge import router as knowledge_router
    app.include_router(knowledge_router,prefix="/api/knowledge",tags=["Knowledge"])
except ImportError:pass