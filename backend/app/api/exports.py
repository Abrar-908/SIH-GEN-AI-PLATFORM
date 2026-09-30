import os
import json
import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import GeneratedOutput, Project
from app.exporters.pdf_exporter import PDFExporter
from app.exporters.docx_exporter import DocxExporter
from app.exporters.pptx_exporter import PPTXExporter
from app.exporters.text_exporter import TextExporter
from app.core.config import EXPORTS_DIR
from app.services.audit_service import AuditService

router = APIRouter(prefix="/export", tags=["export"])

@router.post("/pdf")
def export_pdf(output_id: int = Query(...), db: Session = Depends(get_db)):
    output = db.query(GeneratedOutput).filter(GeneratedOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    filename = f"{output.output_type.lower().replace(' ', '_')}_{output.id}_{int(time.time())}.pdf"
    
    sources = []
    if output.source_references_json:
        try:
            sources = json.loads(output.source_references_json)
        except Exception:
            sources = []

    filepath = PDFExporter.generate_pdf(
        filename=filename,
        title=output.title,
        content_markdown=output.content_markdown,
        output_type=output.output_type,
        source_references=sources
    )

    AuditService.log(
        db,
        action="Output Exported",
        source=filename,
        details=f"Exported {output.output_type} to PDF."
    )

    return {
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
        "file_type": "PDF",
        "file_size": os.path.getsize(filepath)
    }

@router.post("/docx")
def export_docx(output_id: int = Query(...), db: Session = Depends(get_db)):
    output = db.query(GeneratedOutput).filter(GeneratedOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    filename = f"{output.output_type.lower().replace(' ', '_')}_{output.id}_{int(time.time())}.docx"

    sources = []
    if output.source_references_json:
        try:
            sources = json.loads(output.source_references_json)
        except Exception:
            sources = []

    filepath = DocxExporter.generate_docx(
        filename=filename,
        title=output.title,
        content_markdown=output.content_markdown,
        output_type=output.output_type,
        source_references=sources
    )

    AuditService.log(
        db,
        action="Output Exported",
        source=filename,
        details=f"Exported {output.output_type} to DOCX."
    )

    return {
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
        "file_type": "DOCX",
        "file_size": os.path.getsize(filepath)
    }

@router.post("/pptx")
def export_pptx(output_id: int = Query(...), db: Session = Depends(get_db)):
    output = db.query(GeneratedOutput).filter(GeneratedOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    filename = f"presentation_{output.id}_{int(time.time())}.pptx"

    slides = []
    if output.structured_json:
        try:
            data = json.loads(output.structured_json)
            slides = data.get("slides", [])
        except Exception:
            slides = []

    filepath = PPTXExporter.generate_pptx(
        filename=filename,
        title=output.title,
        structured_slides=slides,
        content_markdown=output.content_markdown
    )

    AuditService.log(
        db,
        action="Output Exported",
        source=filename,
        details=f"Exported presentation to PowerPoint (.pptx)."
    )

    return {
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
        "file_type": "PPTX",
        "file_size": os.path.getsize(filepath)
    }

@router.post("/text")
def export_text_format(output_id: int = Query(...), format_type: str = Query("md"), db: Session = Depends(get_db)):
    output = db.query(GeneratedOutput).filter(GeneratedOutput.id == output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")

    fmt = format_type.lower()
    if fmt == "json":
        filename = f"{output.output_type.lower().replace(' ', '_')}_{output.id}.json"
        data = {
            "title": output.title,
            "output_type": output.output_type,
            "content_markdown": output.content_markdown,
            "structured_json": json.loads(output.structured_json) if output.structured_json else {},
            "source_references": json.loads(output.source_references_json) if output.source_references_json else []
        }
        filepath = TextExporter.export_json(filename, data)
    else:
        ext = "txt" if fmt == "txt" else "md"
        filename = f"{output.output_type.lower().replace(' ', '_')}_{output.id}.{ext}"
        filepath = TextExporter.export_text(filename, output.content_markdown)

    AuditService.log(
        db,
        action="Output Exported",
        source=filename,
        details=f"Exported {output.output_type} as {format_type.upper()}."
    )

    return {
        "filename": filename,
        "download_url": f"/api/export/download/{filename}",
        "file_type": format_type.upper(),
        "file_size": os.path.getsize(filepath)
    }

@router.get("/download/{filename}")
def download_file(filename: str):
    filepath = EXPORTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    media_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".json": "application/json"
    }
    ext = filepath.suffix.lower()
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type=media_types.get(ext, "application/octet-stream")
    )

@router.get("/recent")
def list_recent_exports():
    files = []
    for f in EXPORTS_DIR.glob("*.*"):
        if f.is_file():
            files.append({
                "filename": f.name,
                "file_type": f.suffix.lstrip(".").upper(),
                "file_size": f.stat().st_size,
                "created_at": f.stat().st_ctime,
                "download_url": f"/api/export/download/{f.name}"
            })
    files.sort(key=lambda x: x["created_at"], reverse=True)
    return files[:20]
