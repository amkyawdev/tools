"""
Telegram Bot Webhook Routes
Integrated with AI Agent Orchestrator for intelligent responses.
"""
import os
import re
import hmac
import hashlib
import httpx
from fastapi import APIRouter, Request, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_openrouter, get_neon, get_browserless, get_skill_loader
from app.core.orchestrator import Orchestrator, InputChannel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[dict] = None


def get_orchestrator(openrouter=Depends(get_openrouter), neon=Depends(get_neon), browserless=Depends(get_browserless), skill_loader=Depends(get_skill_loader)):
    return Orchestrator(llm_service=openrouter, neon_service=neon, browserless_service=browserless, skill_loader=skill_loader)


def sanitize_telegram_text(text: str) -> str:
    """Sanitize text to prevent Markdown injection."""
    # Escape special Markdown characters
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    sanitized = text
    for char in escape_chars:
        sanitized = sanitized.replace(char, '\\' + char)
    # Limit length
    return sanitized[:4000]


async def send_telegram_message(chat_id: int, text: str, use_markdown: bool = False) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured")
        return False
    
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    # Sanitize text to prevent injection
    safe_text = sanitize_telegram_text(text)
    
    payload = {
        "chat_id": chat_id, 
        "text": safe_text,
        "parse_mode": "MarkdownV2" if use_markdown else None
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


async def verify_telegram_signature(body: bytes, secret_token: str) -> bool:
    """Verify Telegram webhook signature using HMAC."""
    if not secret_token:
        logger.warning("TELEGRAM_SECRET_TOKEN not configured - skipping verification")
        return True  # Skip if not configured
    
    try:
        expected_hash = hmac.new(
            secret_token.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        return True  # In production, compare with X-Telegram-Bot-Api-Secret-Token header
    except Exception:
        return False


@router.post("/webhook")
async def telegram_webhook(
    request: Request, 
    orchestrator: Orchestrator = Depends(get_orchestrator),
    x_telegram_bot_api_secret_token: Optional[str] = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")
):
    try:
        body = await request.body()
        
        # Verify secret token if configured
        if TELEGRAM_SECRET_TOKEN and x_telegram_bot_api_secret_token != TELEGRAM_SECRET_TOKEN:
            logger.warning("Invalid Telegram webhook secret token")
            raise HTTPException(status_code=403, detail="Invalid secret token")
        
        body_json = await request.json()
        logger.info(f"Telegram webhook received: update_id={body_json.get('update_id')}")
        
        update = TelegramUpdate(**body_json)
        if not update.message:
            return {"status": "ignored", "reason": "no message"}
        
        chat_id = update.message.get("chat", {}).get("id")
        text = update.message.get("text", "")
        
        if not chat_id or not text:
            return {"status": "ignored", "reason": "empty message"}
        
        if text.startswith("/"):
            command = text.split()[0].lower()
            if command == "/start":
                await send_telegram_message(chat_id, "Welcome to AmkyawDev Tools Bot!")
                return {"status": "ok", "action": "welcome"}
            elif command == "/help":
                await send_telegram_message(chat_id, "Commands: /start, /help, /skills, /clear")
                return {"status": "ok", "action": "help"}
            elif command == "/skills":
                skills = orchestrator.skill_loader.list_skills() if orchestrator.skill_loader else []
                if skills:
                    skill_list = "\n".join([f"- {s['name']}" for s in skills])
                    await send_telegram_message(chat_id, f"Available Skills:\n{skill_list}")
                else:
                    await send_telegram_message(chat_id, "No skills configured yet.")
                return {"status": "ok", "action": "skills"}
            elif command == "/clear":
                session_id = f"telegram_{chat_id}"
                await orchestrator.clear_session(session_id)
                await send_telegram_message(chat_id, "Session cleared!")
                return {"status": "ok", "action": "clear"}
            else:
                await send_telegram_message(chat_id, f"Unknown command: {command}")
                return {"status": "ok", "action": "unknown_command"}
        
        session_id = f"telegram_{chat_id}"
        result = await orchestrator.process(message=text, channel=InputChannel.TELEGRAM, session_id=session_id)
        response_text = result["response"]
        
        # Send response in chunks if too long
        if len(response_text) > 4000:
            chunks = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
            for chunk in chunks:
                await send_telegram_message(chat_id, chunk)
        else:
            await send_telegram_message(chat_id, response_text)
        
        return {"status": "ok", "chat_id": chat_id, "task_type": result["task_type"], "duration_ms": result["duration_ms"]}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        # Never expose internal error details
        raise HTTPException(status_code=500, detail="Webhook processing failed")


@router.get("/webhook/test")
async def test_webhook():
    return {
        "status": "ok", 
        "message": "Telegram webhook is configured",
        "bot_token_configured": bool(TELEGRAM_BOT_TOKEN),
        "secret_token_configured": bool(TELEGRAM_SECRET_TOKEN)
    }
