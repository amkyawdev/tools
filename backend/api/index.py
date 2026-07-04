try:
    from app.main import app
except Exception:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    app=FastAPI(title="AmkyawDev Tools",description="AI-powered coding platform",version="1.0.0")
    app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
    @app.get("/health")
    async def h():return {"status":"healthy","service":"amkyawdev-tools"}
    @app.get("/")
    async def r():return {"message":"AmkyawDev Tools API","docs":"/docs"}
    try:
        from app.api.routes.agent import router as ag
        app.include_router(ag,prefix="/api/agent",tags=["Agent"])
    except Exception:pass
    try:
        from app.api.routes.knowledge import router as kg
        app.include_router(kg,prefix="/api/knowledge",tags=["Knowledge"])
    except Exception:pass
    try:
        from app.api.routes.file import router as fl
        app.include_router(fl,prefix="/api/files",tags=["Files"])
    except Exception:pass