import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="Analyst")  # Admin, Analyst, Reviewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SourceDocument(Base):
    __tablename__ = "source_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, default=0)
    storage_path = Column(String(500), nullable=True)
    raw_text = Column(Text, nullable=True)
    page_count = Column(Integer, default=1)
    title = Column(String(255), nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON string of headings, author, creation date
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="source_document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("source_documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_id = Column(String(50), index=True, nullable=False)  # e.g., "chunk_01"
    page_number = Column(Integer, default=1)
    section_name = Column(String(150), default="General")
    text = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    document = relationship("SourceDocument", back_populates="chunks")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_document_id = Column(Integer, ForeignKey("source_documents.id"), nullable=True)
    
    # Transformation Configurations
    audience = Column(String(50), default="Executive")
    tone = Column(String(50), default="Professional")
    language = Column(String(50), default="English")
    detail_level = Column(String(50), default="Detailed")
    objective = Column(String(50), default="Brief")
    style = Column(String(50), default="Government")
    selected_outputs = Column(Text, default="[]")  # JSON list of output types
    
    status = Column(String(50), default="Draft")  # Draft, Processing, Completed, Failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    source_document = relationship("SourceDocument", back_populates="projects")
    transformations = relationship("Transformation", back_populates="project", cascade="all, delete-orphan")
    outputs = relationship("GeneratedOutput", back_populates="project", cascade="all, delete-orphan")

class Transformation(Base):
    __tablename__ = "transformations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    selected_outputs = Column(Text, nullable=False)  # JSON list
    config_json = Column(Text, nullable=True)
    status = Column(String(50), default="Queued")  # Queued, Processing, Completed, Failed
    current_step = Column(String(100), default="Initialized")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    project = relationship("Project", back_populates="transformations")
    outputs = relationship("GeneratedOutput", back_populates="transformation", cascade="all, delete-orphan")

class GeneratedOutput(Base):
    __tablename__ = "generated_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    transformation_id = Column(Integer, ForeignKey("transformations.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    output_type = Column(String(100), nullable=False)  # Executive Summary, Security Advisory, etc.
    title = Column(String(255), nullable=False)
    content_markdown = Column(Text, nullable=False)
    structured_json = Column(Text, nullable=True)  # JSON dictionary of sections, slides, scene list, etc.
    source_references_json = Column(Text, nullable=True)  # JSON list of source references with claim, page, chunk
    validation_summary_json = Column(Text, nullable=True)  # JSON summary
    status = Column(String(50), default="Generated")  # Generated, In-Review, Approved, Rejected
    approval_state = Column(String(50), default="Draft")  # Draft, Approved, Rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    project = relationship("Project", back_populates="outputs")
    transformation = relationship("Transformation", back_populates="outputs")
    versions = relationship("OutputVersion", back_populates="output", cascade="all, delete-orphan")
    validation = relationship("ValidationResult", back_populates="output", uselist=False, cascade="all, delete-orphan")

class ValidationResult(Base):
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    output_id = Column(Integer, ForeignKey("generated_outputs.id"), nullable=False)
    source_coverage = Column(Float, default=90.0)  # e.g., 94.0
    supported_claims_count = Column(Integer, default=0)
    partial_claims_count = Column(Integer, default=0)
    unsupported_claims_count = Column(Integer, default=0)
    consistency_score = Column(Float, default=92.5)
    claims_detail_json = Column(Text, nullable=False)  # JSON list of verified claims
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    output = relationship("GeneratedOutput", back_populates="validation")

class OutputVersion(Base):
    __tablename__ = "output_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    output_id = Column(Integer, ForeignKey("generated_outputs.id"), nullable=False)
    version_number = Column(Integer, default=1)
    content_markdown = Column(Text, nullable=False)
    structured_json = Column(Text, nullable=True)
    changed_by = Column(String(100), default="Analyst")
    change_summary = Column(String(255), default="Initial generation")
    approval_state = Column(String(50), default="Draft")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    output = relationship("GeneratedOutput", back_populates="versions")

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100), default="Security")
    description = Column(Text, nullable=False)
    target_audience = Column(String(50), default="Executive")
    tone = Column(String(50), default="Professional")
    language = Column(String(50), default="English")
    detail_level = Column(String(50), default="Detailed")
    objective = Column(String(50), default="Brief")
    content_style = Column(String(50), default="Government")
    output_types = Column(Text, default="[]")  # JSON list
    system_prompt = Column(Text, nullable=True)
    sample_structure = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_name = Column(String(100), default="Analyst")
    user_role = Column(String(50), default="Analyst")
    action = Column(String(100), nullable=False)  # "Document Uploaded", "Transformation Started", etc.
    source = Column(String(255), nullable=True)  # Filename or resource
    details = Column(Text, nullable=True)
    status = Column(String(50), default="Success")  # Success, Warning, Error
