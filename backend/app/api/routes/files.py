from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from typing import Optional
import io
from app.utils.file_handler import FileHandler
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
file_handler=FileHandler()
@router.post("/upload")
async def upload_file(file:UploadFile=File(...),skill:Optional[str]=None):
    try:
        result=await file_handler.save_upload(file,skill=skill)
        return {"status":"ok","file":result}
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.get("/export")
async def export_files(format:str=Query("zip",regex="^(zip|pdf)$"),skill:Optional[str]=Query(None)):
    try:
        if format=="zip":
            zip_buffer=await file_handler.export_zip(skill=skill)
            return StreamingResponse(io.BytesIO(zip_buffer),media_type="application/zip",headers={"Content-Disposition":"attachment; filename=export.zip"})
        elif format=="pdf":
            pdf_buffer=await file_handler.export_pdf(skill=skill)
            return StreamingResponse(io.BytesIO(pdf_buffer),media_type="application/pdf",headers={"Content-Disposition":"attachment; filename=export.pdf"})
    except Exception as e:
        logger.error(f"File export error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.get("/list")
async def list_files(skill:Optional[str]=Query(None)):
    try:
        files=await file_handler.list_files(skill=skill)
        return {"files":files}
    except Exception as e:
        logger.error(f"File list error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
