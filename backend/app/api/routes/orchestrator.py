"""
Orchestrator API Routes
Main API endpoints for the AI Agent Orchestrator.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import ipaddress
import re

from app.api.dependencies import get_openrouter, get_neon, get_browserless, get_skill_loader
from app.core.orchestrator import Orchestrator, InputChannel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# SSRF Protection: Blocked URL patterns
BLOCKED_URL_PATTERNS = [
    r'^file://',
    r'^http://(localhost|127\.0\.0\.1|0\.0\.0\.0)',
    r'^https?://(169\.254\.169\.254|metadata\.googlecloud\.internal)',
    r'@',  # URLs with credentials
]
BLOCKED_URL_REGEX = [re.compile(p, re.IGNORECASE) for p in BLOCKED_URL_PATTERNS]

# Blocked IP ranges
BLOCKED_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),
]


def validate_url(url: str) -> bool:
    """Validate URL to prevent SSRF attacks."""
    # Check against blocked patterns
    for pattern in BLOCKED_URL_REGEX:
        if pattern.match(url):
            logger.warning(f"SSRF attempt blocked: {url}")
            return False
    
    # Check if it's a valid HTTP(S) URL
    if not url.startswith(('http://', 'https://')):
        logger.warning(f"Invalid URL scheme: {url}")
        return False
    
    try:
        # Parse and check hostname
        from urllib.parse import urlparse
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        
        # Resolve hostname and check IP
        import socket
        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            for blocked_range in BLOCKED_IP_RANGES:
                if ip_obj in blocked_range:
                    logger.warning(f"SSRF attempt - blocked IP: {ip}")
                    return False
        except socket.gaierror:
            pass  # Let it fail naturally
        
        return True
    except Exception:
        return False


class OrchestratorRequest(BaseModel):
    message: str = Field(..., max_length=10000, description="User message")
    channel: str = Field(default="web", description="Input channel: web, telegram, cli, voice, api")
    session_id: Optional[str] = Field(None, max_length=100, description="Session ID for context continuity")
    skills: Optional[List[str]] = Field(None, max_length=10, description="Skill names to load")
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
async def scrape_url(
    url: str = Query(..., max_length=2000, description="URL to scrape"),
    browserless=Depends(get_browserless), 
    openrouter=Depends(get_openrouter)
):
    """Scrape a URL and optionally summarize with AI."""
    if not browserless:
        raise HTTPException(status_code=503, detail="Web scraper not configured")
    
    # SSRF Protection
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid or blocked URL")

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


@router.get("/services/status", include_in_schema=False)
async def services_status(openrouter=Depends(get_openrouter), neon=Depends(get_neon), browserless=Depends(get_browserless)):
    """Get status of all services. Hidden from public docs."""
    from app.services.kafka_service import KafkaService
    kafka = KafkaService()
    return {
        "status": "ok",
        "services": {
            "llm": {"available": openrouter is not None},
            "neon": {"available": neon is not None},
            "browserless": {"available": browserless is not None},
            "kafka": kafka.get_status(),
        }
    }
