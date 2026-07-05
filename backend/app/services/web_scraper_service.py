"""
Web Scraper Service - Browserless Integration
Provides web scraping, screenshot, and PDF generation capabilities.
"""
import os
import re
from typing import Optional

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class WebScraperService:
    """
    Web Scraper using Browserless.io
    
    Capabilities:
    - Fetch page HTML content
    - Take screenshots
    - Generate PDFs
    - Extract structured data
    """

    def __init__(self):
        self.api_key = os.getenv("BROWSERLESS_API_KEY", "")
        self.base_url = os.getenv("BROWSERLESS_BASE_URL", "https://chrome.browserless.io")
        self.timeout = int(os.getenv("BROWSERLESS_TIMEOUT", "30"))
        self.enabled = bool(self.api_key)

    async def fetch_page(
        self,
        url: str,
        wait_for: Optional[str] = None,
        goto_options: Optional[dict] = None,
    ) -> Optional[str]:
        """Fetch HTML content from a URL."""
        if not self.enabled:
            logger.warning("Browserless API key not configured")
            return None

        endpoint = f"{self.base_url}/content"
        params = {"token": self.api_key}

        payload = {
            "url": url,
            "gotoOptions": goto_options or {"waitUntil": "networkidle2"},
        }

        if wait_for:
            payload["waitFor"] = wait_for

        try:
            import httpx
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, params=params, json=payload)
                response.raise_for_status()
                
                data = response.json()
                html = data.get("data", {}).get("html") or data.get("html")
                
                if html:
                    logger.info(f"Fetched {len(html)} bytes from {url}")
                    return html
                    
        except Exception as e:
            logger.error(f"Browserless fetch failed for {url}: {e}")

        return None

    async def screenshot(
        self,
        url: str,
        full_page: bool = False,
        selector: Optional[str] = None,
    ) -> Optional[bytes]:
        """Take a screenshot of a page."""
        if not self.enabled:
            logger.warning("Browserless API key not configured")
            return None

        endpoint = f"{self.base_url}/screenshot"
        params = {"token": self.api_key}

        payload = {
            "url": url,
            "options": {
                "fullPage": full_page,
                "type": "png",
            },
        }

        if selector:
            payload["options"]["selector"] = selector

        try:
            import httpx
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(endpoint, params=params, json=payload)
                response.raise_for_status()
                logger.info(f"Screenshot taken for {url}")
                return response.content
                
        except Exception as e:
            logger.error(f"Browserless screenshot failed for {url}: {e}")

        return None

    async def pdf(
        self,
        url: str,
        options: Optional[dict] = None,
    ) -> Optional[bytes]:
        """Generate PDF from a page."""
        if not self.enabled:
            logger.warning("Browserless API key not configured")
            return None

        endpoint = f"{self.base_url}/pdf"
        params = {"token": self.api_key}

        payload = {
            "url": url,
            "options": options or {"printBackground": True, "format": "A4"},
        }

        try:
            import httpx
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(endpoint, params=params, json=payload)
                response.raise_for_status()
                logger.info(f"PDF generated for {url}")
                return response.content
                
        except Exception as e:
            logger.error(f"Browserless PDF failed for {url}: {e}")

        return None

    async def extract_links(self, url: str, selector: str = "a") -> list[dict]:
        """Extract links from a page."""
        html = await self.fetch_page(url)
        if not html:
            return []

        links = []
        pattern = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>([^<]*)</a>')
        
        for match in pattern.finditer(html):
            href = match.group(1)
            text = match.group(2).strip()
            
            if href.startswith(("http://", "https://")):
                links.append({"url": href, "text": text or href})

        logger.info(f"Extracted {len(links)} links from {url}")
        return links

    def get_status(self) -> dict:
        """Get service status."""
        return {
            "enabled": self.enabled,
            "base_url": self.base_url,
            "has_api_key": bool(self.api_key),
        }
