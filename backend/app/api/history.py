import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Transformation, Project, GeneratedOutput

router = APIRouter(prefix="/history", tags=["history"])

@router.get("")
def get_transformation_history(db: Session = Depends(get_db)):
    records = db.query(Transformation).order_by(Transformation.created_at.desc()).all()
    history = []
    
    for t in records:
        proj = t.project
        doc = proj.source_document if proj else None
        
        selected = []
        try:
            selected = json.loads(t.selected_outputs)
        except Exception:
            selected = []

        # Calculate average validation score
        scores = [o.validation.consistency_score for o in t.outputs if o.validation]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 95.0

        history.append({
            "id": t.id,
            "project_id": t.project_id,
            "project_name": proj.name if proj else f"Project #{t.project_id}",
            "source_filename": doc.filename if doc else "Pasted Content",
            "source_type": doc.file_type if doc else "TXT",
            "output_types": selected,
            "outputs_count": len(t.outputs),
            "status": t.status,
            "validation_score": avg_score,
            "created_at": t.created_at,
            "completed_at": t.completed_at
        })

    return history
