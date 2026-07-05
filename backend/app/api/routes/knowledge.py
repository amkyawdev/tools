from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.api.dependencies import get_neon
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
class KnowledgeUpsertRequest(BaseModel):
    title:str
    content:str
    tags:Optional[list[str]]=[]
    source:Optional[str]=None
@router.get("/search")
async def search_knowledge(q:str=Query(...,description="Search query"),limit:int=Query(10,ge=1,le=50),db=Depends(get_neon)):
    try:
        results=await db.search_knowledge(query=q,limit=limit)
        return {"query":q,"results":results}
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.post("/upsert")
async def upsert_knowledge(request:KnowledgeUpsertRequest,db=Depends(get_neon)):
    try:
        await db.save_knowledge(title=request.title,content=request.content,tags=request.tags,source=request.source)
        return {"status":"ok"}
    except Exception as e:
        logger.error(f"Knowledge upsert error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
