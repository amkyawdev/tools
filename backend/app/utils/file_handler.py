import io
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import UploadFile

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/amkyawdev-tools/uploads"))


class FileHandler:
    """Handles file upload, listing, and export (ZIP / PDF)."""

    def __init__(self, upload_dir: Optional[Path] = None) -> None:
        self.upload_dir = upload_dir or UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------

    async def save_upload(
        self, file: UploadFile, skill: Optional[str] = None
    ) -> dict:
        """Persist an uploaded file to disk."""
        target_dir = self.upload_dir
        if skill:
            target_dir = target_dir / skill
            target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / file.filename
        content = await file.read()

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        logger.info(f"Saved upload: {file_path} ({len(content)} bytes)")

        return {
            "filename": file.filename,
            "path": str(file_path),
            "size": len(content),
            "content_type": file.content_type or "application/octet-stream",
            "skill": skill,
            "uploaded_at": datetime.utcnow().isoformat(),
        }

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    async def export_zip(self, skill: Optional[str] = None) -> bytes:
        """Bundle uploaded files into a ZIP archive."""
        buffer = io.BytesIO()
        target_dir = self.upload_dir
        if skill:
            target_dir = target_dir / skill

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in target_dir.rglob("*"):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(self.upload_dir))
                    zf.write(file_path, arcname)

        logger.info(f"Exported ZIP ({buffer.tell()} bytes)")
        return buffer.getvalue()

    async def export_pdf(self, skill: Optional[str] = None) -> bytes:
        """Export file listing as a simple PDF (requires fpdf2)."""
        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            target_dir = self.upload_dir
            if skill:
                target_dir = target_dir / skill

            for file_path in target_dir.rglob("*"):
                if file_path.is_file():
                    pdf.cell(200, 10, txt=f"File: {file_path.name}", ln=True)

            return pdf.output(dest="S").encode("latin-1")
        except ImportError:
            logger.warning("fpdf2 not installed — returning empty PDF body")
            return b"PDF export requires fpdf2 library."

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    async def list_files(self, skill: Optional[str] = None) -> list[dict]:
        """List all uploaded files, optionally filtered by skill."""
        target_dir = self.upload_dir
        if skill:
            target_dir = target_dir / skill

        if not target_dir.exists():
            return []

        files: list[dict] = []
        for file_path in target_dir.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.upload_dir)),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(
                            stat.st_mtime
                        ).isoformat(),
                    }
                )

        return files
