from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.models.code import CodeGenerationRequest, CodeGenerationResponse
from app.api.dependencies import get_openrouter, get_skill_loader
from app.core.agent import CoderAgent
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
@router.post("/chat",response_model=ChatResponse)
async def chat(request:ChatRequest,openrouter=Depends(get_openrouter),skill_loader=Depends(get_skill_loader)):
    try:
        agent=CoderAgent(openrouter_service=openrouter,skill_loader=skill_loader)
        response=await agent.chat(messages=request.messages,skills=request.skills,model=request.model)
        return ChatResponse(message=response["message"],skills_used=response.get("skills_used",[]),tokens_used=response.get("tokens_used",0))
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.post("/generate",response_model=CodeGenerationResponse)
async def generate_code(request:CodeGenerationRequest,openrouter=Depends(get_openrouter),skill_loader=Depends(get_skill_loader)):
    try:
        agent=CoderAgent(openrouter_service=openrouter,skill_loader=skill_loader)
        result=await agent.generate_code(prompt=request.prompt,language=request.language,skills=request.skills,context=request.context)
        return CodeGenerationResponse(code=result["code"],language=result.get("language",request.language),explanation=result.get("explanation",""),file_path=result.get("file_path"))
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.get("/skills")
async def list_skills(skill_loader=Depends(get_skill_loader)):
    skills=skill_loader.list_skills()
    return {"skills":skills}
