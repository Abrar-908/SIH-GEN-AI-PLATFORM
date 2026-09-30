import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Project, SourceDocument, GeneratedOutput, AuditLog
from app.schemas.schemas import ProjectCreate, ProjectResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        name=data.name,
        description=data.description,
        source_document_id=data.source_document_id,
        audience=data.audience or "Executive",
        tone=data.tone or "Professional",
        language=data.language or "English",
        detail_level=data.detail_level or "Detailed",
        objective=data.objective or "Brief",
        style=data.style or "Government",
        selected_outputs=json.dumps(data.selected_outputs or []),
        status="Draft"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    AuditService.log(
        db,
        action="Project Created",
        source=f"Project #{project.id}",
        details=f"Created project '{project.name}' with audience={project.audience}."
    )

    return _to_project_response(project)

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [_to_project_response(p) for p in projects]

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _to_project_response(project)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    name = project.name
    db.delete(project)
    db.commit()

    AuditService.log(
        db,
        action="Project Deleted",
        source=f"Project #{project_id}",
        details=f"Deleted project '{name}'."
    )
    return {"message": "Project deleted successfully", "id": project_id}

@router.post("/{project_id}/duplicate", response_model=ProjectResponse)
def duplicate_project(project_id: int, db: Session = Depends(get_db)):
    original = db.query(Project).filter(Project.id == project_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Project not found")

    clone = Project(
        name=f"{original.name} (Copy)",
        description=original.description,
        source_document_id=original.source_document_id,
        audience=original.audience,
        tone=original.tone,
        language=original.language,
        detail_level=original.detail_level,
        objective=original.objective,
        style=original.style,
        selected_outputs=original.selected_outputs,
        status="Draft"
    )
    db.add(clone)
    db.commit()
    db.refresh(clone)

    AuditService.log(
        db,
        action="Project Duplicated",
        source=f"Project #{clone.id}",
        details=f"Cloned from Project #{original.id}."
    )
    return _to_project_response(clone)

def _to_project_response(p: Project) -> ProjectResponse:
    try:
        outputs = json.loads(p.selected_outputs) if p.selected_outputs else []
    except Exception:
        outputs = []

    return ProjectResponse(
        id=p.id,
        name=p.name,
        description=p.description,
        source_document_id=p.source_document_id,
        source_document=p.source_document,
        audience=p.audience,
        tone=p.tone,
        language=p.language,
        detail_level=p.detail_level,
        objective=p.objective,
        style=p.style,
        selected_outputs=outputs,
        status=p.status,
        created_at=p.created_at,
        updated_at=p.updated_at
    )
