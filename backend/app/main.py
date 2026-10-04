import os
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models.models import User, Template, Project, SourceDocument, DocumentChunk, Transformation, GeneratedOutput, ValidationResult, OutputVersion
from app.api.documents import router as documents_router
from app.api.projects import router as projects_router
from app.api.transform import router as transform_router
from app.api.validate import router as validate_router
from app.api.exports import router as exports_router
from app.api.history import router as history_router
from app.api.audit_logs import router as audit_logs_router
from app.api.templates import router as templates_router, seed_templates
from app.api.settings import router as settings_router
from app.api.rag import router as rag_router
from app.api.dashboard import router as dashboard_router
from app.ai.demo_engine import DemoEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = SessionLocal()
    try:
        seed_templates(db)
        admin = db.query(User).filter(User.username == "analyst").first()
        if not admin:
            user = User(
                username="analyst",
                email="analyst@inteltransform.ai",
                full_name="Lead Cyber Intelligence Analyst",
                role="Analyst",
                is_active=True
            )
            db.add(user)
            db.commit()

        p_count = db.query(Project).count()
        if p_count == 0:
            from app.api.documents import load_sample_document
            sample_doc_resp = load_sample_document(db)
            p = Project(
                name="Cybersecurity Perimeter Breach Incident",
                description="Simulated lateral intrusion triage and multi-format transformation.",
                source_document_id=sample_doc_resp.document_id,
                audience="Executive",
                tone="Professional",
                language="English",
                detail_level="Detailed",
                objective="Brief",
                style="Government",
                selected_outputs=json.dumps(["Executive Summary", "Security Advisory", "Presentation", "LinkedIn Post"]),
                status="Draft"
            )
            db.add(p)
            db.commit()
            logger.info("Initialized default sample project for instant SIH demonstration.")
    except Exception as e:
        logger.error(f"Startup initialization warning: {e}")
    finally:
        db.close()
    yield  # Application runs here

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Generative AI Platform for Trusted Multi-Format Content Transformation",
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(dashboard_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(transform_router, prefix="/api")
app.include_router(validate_router, prefix="/api")
app.include_router(exports_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(audit_logs_router, prefix="/api")
app.include_router(templates_router, prefix="/api")
app.include_router(settings_router, prefix="/api")
app.include_router(rag_router, prefix="/api")



@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_provider": settings.AI_PROVIDER,
        "demo_mode": settings.DEMO_MODE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
