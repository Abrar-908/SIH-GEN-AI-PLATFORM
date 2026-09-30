from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# --- Source Document Schemas ---
class DocumentChunkSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    chunk_id: str
    page_number: int
    section_name: str
    text: str

class SourceDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_type: str
    file_size: int
    page_count: int
    title: Optional[str] = None
    created_at: datetime
    chunks: Optional[List[DocumentChunkSchema]] = []

class DocumentExtractResponse(BaseModel):
    document_id: int
    filename: str
    page_count: int
    chunk_count: int
    headings: List[str]
    sample_text: str
    chunks: List[DocumentChunkSchema]

# --- Project Schemas ---
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    source_document_id: Optional[int] = None
    audience: Optional[str] = "Executive"
    tone: Optional[str] = "Professional"
    language: Optional[str] = "English"
    detail_level: Optional[str] = "Detailed"
    objective: Optional[str] = "Brief"
    style: Optional[str] = "Government"
    selected_outputs: Optional[List[str]] = []

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str] = None
    source_document_id: Optional[int] = None
    source_document: Optional[SourceDocumentResponse] = None
    audience: str
    tone: str
    language: str
    detail_level: str
    objective: str
    style: str
    selected_outputs: List[str]
    status: str
    created_at: datetime
    updated_at: datetime

# --- Transformation & Generation Schemas ---
class SourceReferenceSchema(BaseModel):
    claim: str
    source_page: int
    source_chunk: str
    confidence: float
    supporting_passage: str
    chunk_id: Optional[str] = None
    citation: Optional[str] = None
    reference: Optional[str] = None
    section: Optional[str] = None

class ValidationClaimSchema(BaseModel):
    claim: str
    source_page: int
    source_chunk: str
    status: str  # "SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED"
    confidence: float
    analysis: str

class ValidationResultSchema(BaseModel):
    id: int
    output_id: int
    source_coverage: float
    supported_claims_count: int
    partial_claims_count: int
    unsupported_claims_count: int
    consistency_score: float
    claims_detail: List[ValidationClaimSchema]
    created_at: datetime

class GeneratedOutputResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    transformation_id: Optional[int] = None
    output_type: str
    title: str
    content_markdown: str
    structured_json: Optional[Dict[str, Any]] = None
    source_references: List[SourceReferenceSchema] = []
    validation: Optional[ValidationResultSchema] = None
    status: str
    approval_state: str
    version_count: Optional[int] = 1
    word_count: Optional[int] = 0
    confidence_score: Optional[float] = 95.0
    created_at: datetime
    updated_at: datetime

class TransformationRequest(BaseModel):
    project_id: int
    selected_outputs: List[str]
    audience: Optional[str] = "Executive"
    tone: Optional[str] = "Professional"
    language: Optional[str] = "English"
    detail_level: Optional[str] = "Detailed"
    objective: Optional[str] = "Brief"
    style: Optional[str] = "Government"
    template_id: Optional[int] = None

class RegenerateSectionRequest(BaseModel):
    output_id: int
    section_name: str
    current_content: str
    feedback: Optional[str] = None

class OutputUpdateRequest(BaseModel):
    content_markdown: str
    approval_state: Optional[str] = None
    change_summary: Optional[str] = "Manual user edit"

class OutputVersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    output_id: int
    version_number: int
    content_markdown: str
    changed_by: str
    change_summary: str
    approval_state: str
    created_at: datetime

# --- Template Schemas ---
class TemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    description: str
    target_audience: str
    tone: str
    language: str
    detail_level: str
    objective: str
    content_style: str
    output_types: List[str]
    created_at: datetime

# --- Audit Log Schemas ---
class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    user_name: str
    user_role: str
    action: str
    source: Optional[str] = None
    details: Optional[str] = None
    status: str

# --- Settings Schemas ---
class SettingsResponse(BaseModel):
    ai_provider: str
    gemini_configured: bool
    openai_configured: bool
    gemini_model: str
    openai_model: str
    temperature: float
    max_tokens: int
    chunk_size: int
    chunk_overlap: int
    top_k: int
    demo_mode: bool

class SettingsUpdateRequest(BaseModel):
    ai_provider: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_model: Optional[str] = None
    openai_model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    top_k: Optional[int] = None
    demo_mode: Optional[bool] = None
