from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

app = FastAPI(
    title="AmkyawDev Tools",
    description="AI-powered coding platform with Agent Orchestrator",
    version="1.0.0"
)

# Secure CORS Configuration
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", 
    "https://amkyawdev-tools.vercel.app,https://amkyawdev-tools-git-*.vercel.app,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global error handler - never expose internal details"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "amkyawdev-tools"}

@app.get("/")
async def root():
    return {"message": "AmkyawDev Tools API", "docs": "/docs"}

# Include routers
try:
    from app.api.routes.agent import router as agent_router
    app.include_router(agent_router, prefix="/api/agent", tags=["Agent"])
except ImportError as e:
    pass

try:
    from app.api.routes.knowledge import router as knowledge_router
    app.include_router(knowledge_router, prefix="/api/knowledge", tags=["Knowledge"])
except ImportError:
    pass

try:
    from app.api.routes.files import router as file_router
    app.include_router(file_router, prefix="/api/files", tags=["Files"])
except ImportError:
    pass

try:
    from app.api.routes.telegram import router as telegram_router
    app.include_router(telegram_router, prefix="/api/telegram", tags=["Telegram"])
except ImportError:
    pass

try:
    from app.api.routes.orchestrator import router as orchestrator_router
    app.include_router(orchestrator_router, prefix="/api/orchestrator", tags=["Orchestrator"])
except ImportError:
    pass