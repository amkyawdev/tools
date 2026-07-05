from fastapi import Depends
try:
    from app.services.openrouter_service import OpenRouterService
    _openrouter=None
    def get_openrouter():
        global _openrouter
        if _openrouter is None:
            _openrouter=OpenRouterService()
        return _openrouter
except ImportError:
    def get_openrouter():
        return None
try:
    from app.core.skill_loader import SkillLoader
    _skill_loader=None
    def get_skill_loader():
        global _skill_loader
        if _skill_loader is None:
            _skill_loader=SkillLoader()
        return _skill_loader
except ImportError:
    def get_skill_loader():
        return None
def _try_get(service_name:str,factory):
    cache=_try_get._cache if hasattr(_try_get,"_cache") else {}
    if service_name not in cache:
        try:
            cache[service_name]=factory()
        except Exception:
            cache[service_name]=None
    _try_get._cache=cache
    return cache[service_name]
try:
    from app.services.neon_service import NeonService
    def get_neon():
        return _try_get("neon",NeonService)
except ImportError:
    def get_neon():
        return None
try:
    from app.services.nvidia_service import NvidiaService
    def get_nvidia():
        return _try_get("nvidia",NvidiaService)
except ImportError:
    def get_nvidia():
        return None
try:
    from app.services.browserless_service import BrowserlessService
    def get_browserless():
        return _try_get("browserless",BrowserlessService)
except ImportError:
    def get_browserless():
        return None
