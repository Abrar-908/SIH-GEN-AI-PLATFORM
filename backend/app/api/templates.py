import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Template
from app.schemas.schemas import TemplateResponse

router = APIRouter(prefix="/templates", tags=["templates"])

INITIAL_TEMPLATES = [
    {
        "name": "Cybersecurity Advisory",
        "category": "Cybersecurity",
        "description": "Standard national/enterprise vulnerability and threat advisory with CVSS, IoCs, and mitigation steps.",
        "target_audience": "Technical Team",
        "tone": "Formal",
        "language": "English",
        "detail_level": "Detailed",
        "objective": "Warn",
        "content_style": "Government",
        "output_types": ["Security Advisory", "Executive Summary", "X/Twitter Post"]
    },
    {
        "name": "Executive Intelligence Brief",
        "category": "Intelligence",
        "description": "Strategic C-suite briefing synthesizing critical developments, business risk, and containment metrics.",
        "target_audience": "Executive",
        "tone": "Professional",
        "language": "English",
        "detail_level": "Standard",
        "objective": "Brief",
        "content_style": "Corporate",
        "output_types": ["Executive Summary", "Presentation", "LinkedIn Post"]
    },
    {
        "name": "Incident Report Summary",
        "category": "Operations",
        "description": "Chronological operational incident summary detailing root cause, containment, and system recovery.",
        "target_audience": "Security Analyst",
        "tone": "Technical",
        "language": "English",
        "detail_level": "Detailed",
        "objective": "Analyze",
        "content_style": "Technical",
        "output_types": ["Security Advisory", "Infographic", "Video Package"]
    },
    {
        "name": "Threat Intelligence Brief",
        "category": "Intelligence",
        "description": "Deep-dive threat cluster profiling, adversary attribution, and forward defense recommendations.",
        "target_audience": "Security Analyst",
        "tone": "Formal",
        "language": "English",
        "detail_level": "Very Detailed",
        "objective": "Analyze",
        "content_style": "Government",
        "output_types": ["Intelligence Brief", "Security Advisory"]
    },
    {
        "name": "Executive Presentation",
        "category": "Leadership",
        "description": "Board-ready presentation deck with visual hierarchy, key metrics, and speaker notes.",
        "target_audience": "Executive",
        "tone": "Professional",
        "language": "English",
        "detail_level": "Standard",
        "objective": "Summarize",
        "content_style": "Corporate",
        "output_types": ["Presentation", "Executive Summary"]
    },
    {
        "name": "Public Awareness Post",
        "category": "Communications",
        "description": "Citizen-centric or multi-channel social advisory demystifying complex technical threats.",
        "target_audience": "General Public",
        "tone": "Simplified",
        "language": "English",
        "detail_level": "Brief",
        "objective": "Educate",
        "content_style": "Social Media",
        "output_types": ["LinkedIn Post", "X/Twitter Post", "Infographic"]
    }
]

def seed_templates(db: Session):
    count = db.query(Template).count()
    if count == 0:
        for t in INITIAL_TEMPLATES:
            tmpl = Template(
                name=t["name"],
                category=t["category"],
                description=t["description"],
                target_audience=t["target_audience"],
                tone=t["tone"],
                language=t["language"],
                detail_level=t["detail_level"],
                objective=t["objective"],
                content_style=t["content_style"],
                output_types=json.dumps(t["output_types"]),
                system_prompt="Standard domain-specific system instruction"
            )
            db.add(tmpl)
        db.commit()

@router.get("", response_model=List[TemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    seed_templates(db)
    templates = db.query(Template).all()
    results = []
    for t in templates:
        types = []
        try:
            types = json.loads(t.output_types)
        except Exception:
            types = []
        results.append(TemplateResponse(
            id=t.id,
            name=t.name,
            category=t.category,
            description=t.description,
            target_audience=t.target_audience,
            tone=t.tone,
            language=t.language,
            detail_level=t.detail_level,
            objective=t.objective,
            content_style=t.content_style,
            output_types=types,
            created_at=t.created_at
        ))
    return results
