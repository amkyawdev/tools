"""
Telegram Bot Webhook Routes
Integrated with AI Agent Orchestrator for intelligent responses.
"""
import os
import httpx
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_openrouter, get_neon, get_browserless, get_skill_loader
from app.core.orchestrator import Orchestrator, InputChannel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[dict] = None


def get_orchestrator(openrouter=Depends(get_openrouter), neon=Depends(get_neon), browserless=Depends(get_browserless), skill_loader=Depends(get_skill_loader)):
    return Orchestrator(llm_service=openrouter, neon_service=neon, browserless_service=browserless, skill_loader=skill_loader)


async def send_telegram_message(chat_id: int, text: str) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured")
        return False
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


@router.post("/webhook")
async def telegram_webhook(request: Request, orchestrator: Orchestrator = Depends(get_orchestrator)):
    try:
        body = await request.json()
        logger.info(f"Telegram webhook received: {body}")
        update = TelegramUpdate(**body)
        if not update.message:
            return {"status": "ignored", "reason": "no message"}
        chat_id = update.message.get("chat", {}).get("id")
        text = update.message.get("text", "")
        user = update.message.get("from", {}).get("username", "unknown")
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
        if len(response_text) > 4000:
            chunks = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
            for chunk in chunks:
                await send_telegram_message(chat_id, chunk)
        else:
            await send_telegram_message(chat_id, response_text)
        return {"status": "ok", "chat_id": chat_id, "task_type": result["task_type"], "duration_ms": result["duration_ms"]}
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/webhook/test")
async def test_webhook():
    return {"status": "ok", "message": "Telegram webhook is configured", "bot_token_configured": bool(TELEGRAM_BOT_TOKEN)}
