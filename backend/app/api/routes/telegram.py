from fastapi import APIRouter, Request, HTTPException
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
@router.post("/webhook")
async def telegram_webhook(request:Request):
    try:
        body=await request.json()
        logger.info(f"Telegram webhook received: {body}")
        message=body.get("message",{})
        chat_id=message.get("chat",{}).get("id")
        text=message.get("text","")
        if not chat_id or not text:
            return {"status":"ignored"}
        return {"status":"received","chat_id":chat_id}
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
