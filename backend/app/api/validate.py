from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import GeneratedOutput, ValidationResult
from app.schemas.schemas import ValidationResultSchema
from app.ai.validator import ContentValidator
import json

router = APIRouter(prefix="/validate", tags=["validate"])

@router.get("/output/{output_id}", response_model=ValidationResultSchema)
def get_output_validation(output_id: int, db: Session = Depends(get_db)):
    val = db.query(ValidationResult).filter(ValidationResult.output_id == output_id).first()
    if not val:
        raise HTTPException(status_code=404, detail="Validation result not found for this output")

    claims = []
    try:
        claims = json.loads(val.claims_detail_json)
    except Exception:
        claims = []

    return ValidationResultSchema(
        id=val.id,
        output_id=val.output_id,
        source_coverage=val.source_coverage,
        supported_claims_count=val.supported_claims_count,
        partial_claims_count=val.partial_claims_count,
        unsupported_claims_count=val.unsupported_claims_count,
        consistency_score=val.consistency_score,
        claims_detail=claims,
        created_at=val.created_at
    )
