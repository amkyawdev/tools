from fastapi import Depends

# Service cache
_service_cache = {}


def _try_get(service_name: str, factory):
    """Generic service getter with caching."""
    if service_name not in _service_cache:
        try:
            _service_cache[service_name] = factory()
        except Exception:
            _service_cache[service_name] = None
    return _service_cache[service_name]


# OpenRouter Service
try:
    from app.services.openrouter_service import OpenRouterService
    def get_openrouter():
        return _try_get("openrouter", OpenRouterService)
except ImportError:
    def get_openrouter():
        return None


# Skill Loader
try:
    from app.core.skill_loader import SkillLoader
    def get_skill_loader():
        return _try_get("skill_loader", SkillLoader)
except ImportError:
    def get_skill_loader():
        return None


# Neon Service
try:
    from app.services.neon_service import NeonService
    def get_neon():
        return _try_get("neon", NeonService)
except ImportError:
    def get_neon():
        return None


# NVIDIA Service
try:
    from app.services.nvidia_service import NvidiaService
    def get_nvidia():
        return _try_get("nvidia", NvidiaService)
except ImportError:
    def get_nvidia():
        return None


# Browserless Service (WebScraper)
try:
    from app.services.web_scraper_service import WebScraperService
    def get_browserless():
        return _try_get("browserless", WebScraperService)
except ImportError:
    def get_browserless():
        return None


# Kafka Service
try:
    from app.services.kafka_service import KafkaService
    def get_kafka():
        return _try_get("kafka", KafkaService)
except ImportError:
    def get_kafka():
        return None
