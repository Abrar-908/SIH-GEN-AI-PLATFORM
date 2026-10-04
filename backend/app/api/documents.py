import os
import shutil
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings, UPLOADS_DIR, SAMPLES_DIR
from app.models.models import SourceDocument, DocumentChunk
from app.services.document_parser import DocumentParserService
from app.rag.vector_store import vector_store
from app.services.audit_service import AuditService
from app.schemas.schemas import SourceDocumentResponse, DocumentExtractResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentExtractResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".doc", ".txt", ".md", ".json"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload a PDF, DOCX, or TXT file."
        )

    # Save to disk
    safe_filename = Path(file.filename).name.replace(" ", "_")
    target_path = UPLOADS_DIR / safe_filename
    
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(target_path)
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        parse_result = DocumentParserService.parse_file(
            str(target_path),
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to extract document contents: {str(e)}")

    # Create DB Record
    doc_record = SourceDocument(
        filename=file.filename,
        file_type=parse_result.get("file_type", "UNKNOWN"),
        file_size=file_size,
        storage_path=str(target_path),
        raw_text=parse_result.get("raw_text", ""),
        page_count=parse_result.get("page_count", 1),
        title=parse_result.get("title", file.filename),
        metadata_json=json.dumps({"headings": parse_result.get("headings", [])})
    )
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)

    # Create chunks
    chunk_schemas = []
    chunk_dicts_for_rag = []
    for c in parse_result.get("chunks", []):
        chunk_obj = DocumentChunk(
            document_id=doc_record.id,
            chunk_index=c["chunk_index"],
            chunk_id=c["chunk_id"],
            page_number=c["page_number"],
            section_name=c["section_name"],
            text=c["text"],
            token_count=c["token_count"]
        )
        db.add(chunk_obj)
        chunk_schemas.append(c)
        chunk_dicts_for_rag.append(c)

    db.commit()

    # Index in Vector Store
    vector_store.index_document(doc_record.id, chunk_dicts_for_rag)

    # Audit log
    AuditService.log(
        db,
        action="Document Uploaded",
        source=file.filename,
        details=f"Parsed {len(chunk_schemas)} chunks across {doc_record.page_count} page(s)."
    )

    return DocumentExtractResponse(
        document_id=doc_record.id,
        filename=doc_record.filename,
        page_count=doc_record.page_count,
        chunk_count=len(chunk_schemas),
        headings=parse_result.get("headings", []),
        sample_text=(parse_result.get("raw_text", "")[:600] + "..."),
        chunks=[
            {
                "chunk_id": c["chunk_id"],
                "page_number": c["page_number"],
                "section_name": c["section_name"],
                "text": c["text"]
            }
            for c in chunk_schemas
        ]
    )

def load_sample_document(db: Session) -> DocumentExtractResponse:
    sample_file = SAMPLES_DIR / "sample_incident_report.txt"
    if not sample_file.exists():
        sample_file.write_text("Incident Report: Simulated Enterprise Intrusion...", encoding="utf-8")

    existing = db.query(SourceDocument).filter(SourceDocument.filename == "sample_incident_report.txt").first()
    if existing and existing.chunks:
        headings = []
        if existing.metadata_json:
            try:
                headings = json.loads(existing.metadata_json).get("headings", [])
            except Exception:
                headings = ["Executive Incident Summary", "Incident Chronology", "Attack Vector", "Indicators of Compromise"]
        if not headings:
            headings = ["Executive Incident Summary", "Incident Chronology", "Attack Vector", "Indicators of Compromise"]

        # Ensure vector store indexed
        if existing.id not in vector_store._indexes:
            chunks_data = [
                {
                    "chunk_id": ch.chunk_id,
                    "chunk_index": ch.chunk_index,
                    "page_number": ch.page_number,
                    "section_name": ch.section_name,
                    "text": ch.text
                }
                for ch in existing.chunks
            ]
            vector_store.index_document(existing.id, chunks_data)

        return DocumentExtractResponse(
            document_id=existing.id,
            filename=existing.filename,
            page_count=existing.page_count,
            chunk_count=len(existing.chunks),
            headings=headings,
            sample_text=(existing.raw_text[:600] + "..." if existing.raw_text else ""),
            chunks=[
                {
                    "chunk_id": c.chunk_id,
                    "page_number": c.page_number,
                    "section_name": c.section_name,
                    "text": c.text
                }
                for c in existing.chunks
            ]
        )

    parse_result = DocumentParserService.parse_file(
        str(sample_file),
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    doc_record = SourceDocument(
        filename="sample_incident_report.txt",
        file_type="TXT",
        file_size=os.path.getsize(sample_file),
        storage_path=str(sample_file),
        raw_text=parse_result.get("raw_text", ""),
        page_count=parse_result.get("page_count", 1),
        title="Simulated Cybersecurity Incident Report",
        metadata_json=json.dumps({"headings": parse_result.get("headings", [])})
    )
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)

    chunk_schemas = []
    chunk_dicts_for_rag = []
    for c in parse_result.get("chunks", []):
        chunk_obj = DocumentChunk(
            document_id=doc_record.id,
            chunk_index=c["chunk_index"],
            chunk_id=c["chunk_id"],
            page_number=c["page_number"],
            section_name=c["section_name"],
            text=c["text"],
            token_count=c["token_count"]
        )
        db.add(chunk_obj)
        chunk_schemas.append(c)
        chunk_dicts_for_rag.append(c)

    db.commit()
    vector_store.index_document(doc_record.id, chunk_dicts_for_rag)

    AuditService.log(
        db,
        action="Sample Document Loaded",
        source="sample_incident_report.txt",
        details=f"Loaded and indexed {len(chunk_schemas)} chunks for demonstration."
    )

    return DocumentExtractResponse(
        document_id=doc_record.id,
        filename=doc_record.filename,
        page_count=doc_record.page_count,
        chunk_count=len(chunk_schemas),
        headings=parse_result.get("headings", []),
        sample_text=(parse_result.get("raw_text", "")[:600] + "..."),
        chunks=[
            {
                "chunk_id": c["chunk_id"],
                "page_number": c["page_number"],
                "section_name": c["section_name"],
                "text": c["text"]
            }
            for c in chunk_schemas
        ]
    )

@router.post("/sample/load", response_model=DocumentExtractResponse)
def load_sample_post(db: Session = Depends(get_db)):
    return load_sample_document(db)

@router.get("/sample", response_model=DocumentExtractResponse)
def load_sample_get(db: Session = Depends(get_db)):
    return load_sample_document(db)


@router.get("/{document_id}", response_model=SourceDocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(SourceDocument).filter(SourceDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Ensure indexed in RAG
    if document_id not in vector_store._indexes:
        chunks_data = [
            {
                "chunk_id": ch.chunk_id,
                "chunk_index": ch.chunk_index,
                "page_number": ch.page_number,
                "section_name": ch.section_name,
                "text": ch.text
            }
            for ch in doc.chunks
        ]
        vector_store.index_document(doc.id, chunks_data)

    return doc

@router.post("/{document_id}/extract", response_model=DocumentExtractResponse)
def re_extract_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(SourceDocument).filter(SourceDocument.id == document_id).first()
    if not doc or not doc.storage_path or not os.path.exists(doc.storage_path):
        raise HTTPException(status_code=404, detail="Document or file storage not found")

    parse_result = DocumentParserService.parse_file(doc.storage_path, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    
    # Re-index
    vector_store.index_document(doc.id, parse_result.get("chunks", []))
    
    return DocumentExtractResponse(
        document_id=doc.id,
        filename=doc.filename,
        page_count=doc.page_count,
        chunk_count=len(parse_result.get("chunks", [])),
        headings=parse_result.get("headings", []),
        sample_text=(parse_result.get("raw_text", "")[:600] + "..."),
        chunks=[
            {
                "chunk_id": c["chunk_id"],
                "page_number": c["page_number"],
                "section_name": c["section_name"],
                "text": c["text"]
            }
            for c in parse_result.get("chunks", [])
        ]
    )
