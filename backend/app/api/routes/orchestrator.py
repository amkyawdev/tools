"""
Orchestrator API Routes
Main API endpoints for the AI Agent Orchestrator.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

from app.api.dependencies import get_openrouter, get_neon, get_browserless, get_skill_loader
from app.core.orchestrator import Orchestrator, InputChannel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


class OrchestratorRequest(BaseModel):
    message: str = Field(..., description="User message")
    channel: str = Field(default="web", description="Input channel: web, telegram, cli, voice, api")
    session_id: Optional[str] = Field(None, description="Session ID for context continuity")
    skills: Optional[list[str]] = Field(None, description="Skill names to load")
    context: Optional[dict] = Field(None, description="Additional context data")


class OrchestratorResponse(BaseModel):
    response: str
    task_type: str
    session_id: str
    duration_ms: int
    metadata: dict = {}
    actions: list = []


def get_orchestrator(openrouter=Depends(get_openrouter), neon=Depends(get_neon), browserless=Depends(get_browserless), skill_loader=Depends(get_skill_loader)):
    return Orchestrator(llm_service=openrouter, neon_service=neon, browserless_service=browserless, skill_loader=skill_loader)


@router.post("/process", response_model=OrchestratorResponse)
async def process_message(request: OrchestratorRequest, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Process a message through the AI Agent Orchestrator."""
    try:
        channel = InputChannel(request.channel.lower())
    except ValueError:
        channel = InputChannel.WEB

    result = await orchestrator.process(
        message=request.message,
        channel=channel,
        session_id=request.session_id,
        skills=request.skills,
        context=request.context,
    )
    return OrchestratorResponse(**result)


@router.post("/scrape")
async def scrape_url(url: str = Query(...), browserless=Depends(get_browserless), openrouter=Depends(get_openrouter)):
    """Scrape a URL and optionally summarize with AI."""
    if not browserless:
        raise HTTPException(status_code=503, detail="Web scraper not configured")

    html = await browserless.fetch_page(url=url)
    if not html:
        raise HTTPException(status_code=502, detail="Failed to fetch page")

    result = {"url": url, "html_length": len(html), "html_preview": html[:500] + "..." if len(html) > 500 else html}

    if openrouter and len(html) > 500:
        try:
            messages = [
                {"role": "system", "content": "Summarize this web page content concisely."},
                {"role": "user", "content": f"URL: {url}\n\nContent:\n{html[:8000]}"},
            ]
            response = await openrouter.chat_completion(messages=messages)
            result["summary"] = response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"AI summarization failed: {e}")

    return result


@router.get("/session/{session_id}")
async def get_session(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Get information about a session."""
    info = await orchestrator.get_session_info(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    return info


@router.delete("/session/{session_id}")
async def clear_session(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """Clear a session from memory."""
    await orchestrator.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


@router.get("/services/status")
async def services_status(openrouter=Depends(get_openrouter), neon=Depends(get_neon), browserless=Depends(get_browserless)):
    """Get status of all services."""
    from app.services.kafka_service import KafkaService
    kafka = KafkaService()
    return {
        "llm": {"configured": openrouter is not None, "service": "openrouter"},
        "neon": {"configured": neon is not None, "service": "neon-postgresql"},
        "browserless": {"configured": browserless is not None, "service": "browserless"},
        "kafka": kafka.get_status(),
    }
