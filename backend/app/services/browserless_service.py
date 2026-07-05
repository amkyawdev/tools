import os
from typing import Optional
import httpx
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
class BrowserlessService:
    def __init__(self):
        self.api_key=os.getenv("BROWSERLESS_API_KEY","")
        self.base_url=os.getenv("BROWSERLESS_BASE_URL","https://chrome.browserless.io")
        self.available=bool(self.api_key)
    async def fetch_page(self,url:str)->Optional[str]:
        if not self.available:
            logger.warning("Browserless API key not configured")
            return None
        endpoint=f"{self.base_url}/content?token={self.api_key}"
        payload={"url":url}
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response=await client.post(endpoint,json=payload)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.error(f"Browserless fetch failed: {e}")
                return None
    async def screenshot(self,url:str)->Optional[bytes]:
        if not self.available:
            logger.warning("Browserless API key not configured")
            return None
        endpoint=f"{self.base_url}/screenshot?token={self.api_key}"
        payload={"url":url,"options":{"fullPage":True}}
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response=await client.post(endpoint,json=payload)
                response.raise_for_status()
                return response.content
            except Exception as e:
                logger.error(f"Browserless screenshot failed: {e}")
                return None
    async def pdf(self,url:str)->Optional[bytes]:
        if not self.available:
            logger.warning("Browserless API key not configured")
            return None
        endpoint=f"{self.base_url}/pdf?token={self.api_key}"
        payload={"url":url}
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response=await client.post(endpoint,json=payload)
                response.raise_for_status()
                return response.content
            except Exception as e:
                logger.error(f"Browserless PDF failed: {e}")
                return None
