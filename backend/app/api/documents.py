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

@router.post("/sample/load", response_model=DocumentExtractResponse)
def load_sample_document(db: Session = Depends(get_db)):
    """
    Creates and loads the pre-configured synthetic Cybersecurity Incident Report.
    Ensures immediate, flawless testing without requiring user file upload.
    """
    sample_text = """CYBERSECURITY INCIDENT INVESTIGATION REPORT: SIMULATED ENTERPRISE EXTRUSION
CLASSIFICATION: TLP:AMBER | RESTRICTED
INCIDENT ID: CIR-2026-0924-APX
DATE OF OCCURRENCE: SEPTEMBER 24, 2026
REPORTING AGENCY: GLOBAL CYBER DEFENSE OPERATIONS CENTER (GCDOC)

1. EXECUTIVE INCIDENT SUMMARY
At 02:40 UTC on September 24, 2026, the Tier-1 Security Operations Center identified an anomalous lateral authentication burst originating from perimeter edge VPN gateway Node-04 (IP: 194.26.29.114). The threat actor exploited a recently disclosed token authentication vulnerability (CVE-2026-4821) allowing ephemeral session impersonation without secondary token confirmation. Automated heuristics flagged unusual Kerberos ticket requests against internal directory controllers. Containment protocol Delta was invoked at 03:14 UTC, completing host isolation within 72 minutes of confirmation. Forensic audits confirm zero customer financial ledgers or unencrypted PII records were exfiltrated.

2. INCIDENT CHRONOLOGY & TIMELINE
- 02:40 UTC: Ingress perimeter alarm triggered on VPN Gateway node 04 in Frankfurt.
- 02:48 UTC: Threat actor attempts living-off-the-land reconnaissance via WMI and encoded PowerShell.
- 02:58 UTC: Adversary attempts credential extraction on staging database host DB-STG-02.
- 03:14 UTC: SOC tier-2 analyst triggers air-gap subnet quarantine protocol.
- 03:30 UTC: Revocation of all active KRBTGT ticket signing keys and Kerberos tokens.
- 03:52 UTC: Containment achieved across all 4 isolated servers; MTTD: 18 minutes; MTTC: 72 minutes.

3. ATTACK VECTOR & SYSTEM IMPACT
The threat actor capitalized on boundary firmware unpatched state (version 14.1.2 vs required 14.2.8). In-memory reflective DLL injection was utilized to bypass standard disk heuristics.
Systems Affected:
- 4 staging application servers in Frankfurt and Mumbai availability zones.
- 18 internal operational workstations quarantined for forensic imaging.
- Secondary business reporting portal suffered 4.2 hours of preventive offline maintenance.
- Zero immutable financial transaction logs compromised due to hardware-isolated cryptographic enclave.

4. OBSERVED INDICATORS OF COMPROMISE (IoCs)
- Command & Control IPs: 194.26.29.114, 89.185.85.102
- Suspicious Domain: update-telemetry.syncdns-cdn[.]com
- Payload Dropper SHA-256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- Reflective Loader SHA-256: 7d793037a0760186574b0282f2f435e709c6c04d66fa8aaa879d9543f4c71992
- Mutex: Global\\SyncPerimeter_2026

5. MITIGATION & STRATEGIC RECOMMENDATIONS
Immediate remediations executed:
1. Deployed vendor emergency patch KB-994821 across all edge appliances.
2. Enforced mandatory FIDO2 hardware token MFA for all administrative roles.
3. Completed double-rotation of KRBTGT domain passwords.
4. Budget allocation: $42,000 committed for external third-party CIRT certification.
5. Instituted continuous source-grounded policy verification via IntelTransform AI."""

    sample_path = SAMPLES_DIR / "sample_incident_report.txt"
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write(sample_text)

    # Check if already in DB
    existing = db.query(SourceDocument).filter(SourceDocument.filename == "sample_incident_report.txt").first()
    if existing:
        doc_record = existing
    else:
        parse_result = DocumentParserService.parse_file(str(sample_path), settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        doc_record = SourceDocument(
            filename="sample_incident_report.txt",
            file_type="TXT",
            file_size=len(sample_text.encode("utf-8")),
            storage_path=str(sample_path),
            raw_text=sample_text,
            page_count=parse_result.get("page_count", 2),
            title="Cybersecurity Incident Report – Simulated",
            metadata_json=json.dumps({"headings": parse_result.get("headings", [])})
        )
        db.add(doc_record)
        db.commit()
        db.refresh(doc_record)

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
        db.commit()

    # Re-fetch chunks
    chunks_list = []
    for ch in doc_record.chunks:
        chunks_list.append({
            "chunk_id": ch.chunk_id,
            "chunk_index": ch.chunk_index,
            "page_number": ch.page_number,
            "section_name": ch.section_name,
            "text": ch.text,
            "token_count": ch.token_count
        })

    vector_store.index_document(doc_record.id, chunks_list)

    AuditService.log(
        db,
        action="Document Uploaded",
        source="sample_incident_report.txt",
        details="Loaded pre-configured synthetic cybersecurity incident report."
    )

    return DocumentExtractResponse(
        document_id=doc_record.id,
        filename=doc_record.filename,
        page_count=doc_record.page_count,
        chunk_count=len(chunks_list),
        headings=["EXECUTIVE INCIDENT SUMMARY", "INCIDENT CHRONOLOGY & TIMELINE", "ATTACK VECTOR & SYSTEM IMPACT", "INDICATORS OF COMPROMISE (IoCs)", "MITIGATION & RECOMMENDATIONS"],
        sample_text=(sample_text[:600] + "..."),
        chunks=[
            {
                "chunk_id": c["chunk_id"],
                "page_number": c["page_number"],
                "section_name": c["section_name"],
                "text": c["text"]
            }
            for c in chunks_list
        ]
    )
