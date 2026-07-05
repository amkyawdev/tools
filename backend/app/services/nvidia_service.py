import os
from typing import Optional
from openai import AsyncOpenAI
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
NIM_MODELS={"chat":["nvidia/nemotron-3-nano-30b-a3b","nvidia/nemotron-mini-4b-instruct","meta/llama-3.2-3b-instruct"],"code":["mistralai/codestral-22b-instruct-v0.1","deepseek-ai/deepseek-coder-6.7b-instruct","bigcode/starcoder2-15b"]}
class NvidiaService:
    def __init__(self):
        self.api_key=os.getenv("NVIDIA_API_KEY","")
        self.base_url=os.getenv("NVIDIA_BASE_URL","https://integrate.api.nvidia.com/v1")
        self.default_model=os.getenv("NVIDIA_DEFAULT_MODEL","nvidia/nemotron-3-nano-30b-a3b")
        self.default_code_model=os.getenv("NVIDIA_CODE_MODEL","mistralai/codestral-22b-instruct-v0.1")
        self.client=AsyncOpenAI(api_key=self.api_key,base_url=self.base_url) if self.api_key else None
    def get_models(self,category:str="chat")->list[str]:
        return NIM_MODELS.get(category,NIM_MODELS["chat"])
    async def chat_completion(self,messages:list[dict],model:Optional[str]=None,temperature:float=0.7,max_tokens:int=4096)->dict:
        if not self.client:
            raise ValueError("NVIDIA API key not configured")
        model_name=model or self.default_model
        logger.info(f"Calling NVIDIA NIM with model: {model_name}")
        response=await self.client.chat.completions.create(model=model_name,messages=messages,temperature=temperature,max_tokens=max_tokens)
        return response.model_dump()
