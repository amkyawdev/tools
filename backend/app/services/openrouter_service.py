import os
from typing import Optional
from openai import AsyncOpenAI
from app.utils.logger import setup_logger
logger=setup_logger(__name__)

# Working Free Models (Verified)
FREE_MODELS={
    "chat": [
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "google/gemma-4-31b-it:free",
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "openrouter/free",
    ],
    "code": [
        "poolside/laguna-m.1:free",      # ⭐ Best for Coding Agent
        "poolside/laguna-xs.2:free",     # Fast Coding
        "poolside/laguna-xs-2.1:free",   # Fast Coding
        "cohere/north-mini-code:free",
        "qwen/qwen3-coder:free",          # 1M context
    ],
    "vision": [
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "nvidia/nemotron-nano-12b-v2-vl:free",
    ],
    "tools": [
        "nvidia/nemotron-3-ultra-550b-a55b:free",
    ]
}

class OpenRouterService:
    def __init__(self):
        self.api_key=os.getenv("OPENROUTER_API_KEY","")
        self.base_url=os.getenv("OPENROUTER_BASE_URL","https://openrouter.ai/api/v1")
        self.default_model=os.getenv("OPENROUTER_DEFAULT_MODEL","nvidia/nemotron-3-ultra-550b-a55b:free")
        self.default_code_model=os.getenv("OPENROUTER_CODE_MODEL","poolside/laguna-m.1:free")
        self.client=AsyncOpenAI(api_key=self.api_key,base_url=self.base_url) if self.api_key else None
    def get_free_models(self,category:str="chat")->list[str]:
        return FREE_MODELS.get(category,FREE_MODELS["chat"])
    def _enforce_free_model(self,model:str,category:str="chat")->str:
        all_free=set()
        for models in FREE_MODELS.values():
            all_free.update(models)
        default=self.default_model if category=="chat" else self.default_code_model
        if model in all_free:
            return model
        logger.warning(f"Model '{model}' is not in free list, falling back to {default}")
        return default
    async def chat_completion(self,messages:list[dict],model:Optional[str]=None,temperature:float=0.7,max_tokens:int=4096)->dict:
        if not self.client:
            raise ValueError("OpenRouter API key not configured")
        model_name=self._enforce_free_model(model or self.default_model,"chat")
        logger.info(f"Calling OpenRouter with model: {model_name}")
        response=await self.client.chat.completions.create(model=model_name,messages=messages,temperature=temperature,max_tokens=max_tokens)
        return response.model_dump()
    async def stream_chat_completion(self,messages:list[dict],model:Optional[str]=None,temperature:float=0.7,max_tokens:int=4096):
        if not self.client:
            raise ValueError("OpenRouter API key not configured")
        model_name=self._enforce_free_model(model or self.default_model,"chat")
        stream=await self.client.chat.completions.create(model=model_name,messages=messages,temperature=temperature,max_tokens=max_tokens,stream=True)
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
