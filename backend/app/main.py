from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes.agent import router as agent_router
from app.api.routes.knowledge import router as knowledge_router
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
def _safe_import_router(module_path,router_name):
    try:module=__import__(module_path,fromlist=[router_name]);return getattr(module,router_name)
    except ImportError as e:logger.warning(f"Skipping {module_path}: {e}");return None
@asynccontextmanager
async def lifespan(app):
    logger.info("🚀 AmkyawDev Tools starting up...")
    yield
    logger.info("👋 AmkyawDev Tools shutting down...")
app=FastAPI(title="AmkyawDev Tools",description="AI-powered coding platform",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(agent_router,prefix="/api/agent",tags=["Agent"])
app.include_router(knowledge_router,prefix="/api/knowledge",tags=["Knowledge"])
files_router=_safe_import_router("app.api.routes.files","router")
if files_router:app.include_router(files_router,prefix="/api/files",tags=["Files"])
telegram_router=_safe_import_router("app.api.routes.telegram","router")
if telegram_router:app.include_router(telegram_router,prefix="/api/telegram",tags=["Telegram"])
@app.get("/health")
async def health_check():
    return{"status":"healthy","service":"amkyawdev-tools","routes":[r.path for r in app.routes if hasattr(r,"path")]}