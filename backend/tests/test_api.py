import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "IntelTransform AI" in data["service"]

def test_load_sample_and_rag():
    # Load synthetic cybersecurity incident report
    resp = client.post("/api/documents/sample/load")
    assert resp.status_code == 200
    doc_data = resp.json()
    assert doc_data["document_id"] > 0
    assert doc_data["chunk_count"] > 0

    # Test RAG search
    rag_resp = client.post("/api/rag/search", json={
        "document_id": doc_data["document_id"],
        "query": "perimeter VPN token exploit CVE-2026-4821",
        "top_k": 3
    })
    assert rag_resp.status_code == 200
    rag_data = rag_resp.json()
    assert len(rag_data["results"]) > 0
    assert "chunk_id" in rag_data["results"][0]

def test_project_and_transformation():
    # Create project
    sample_resp = client.post("/api/documents/sample/load")
    doc_id = sample_resp.json()["document_id"]

    p_resp = client.post("/api/projects", json={
        "name": "SIH Triage Automation Test",
        "description": "Automated test project",
        "source_document_id": doc_id,
        "audience": "Executive",
        "tone": "Professional",
        "language": "English",
        "detail_level": "Detailed",
        "objective": "Brief",
        "style": "Government",
        "selected_outputs": ["Executive Summary", "Security Advisory", "Presentation", "LinkedIn Post"]
    })
    assert p_resp.status_code == 200
    project = p_resp.json()
    project_id = project["id"]

    # Run transformation
    t_resp = client.post("/api/transform", json={
        "project_id": project_id,
        "selected_outputs": ["Executive Summary", "Security Advisory", "Presentation", "LinkedIn Post"]
    })
    assert t_resp.status_code == 200
    outputs = t_resp.json()
    assert len(outputs) == 4

    first_output = outputs[0]
    output_id = first_output["id"]
    assert first_output["output_type"] in ["Executive Summary", "Security Advisory", "Presentation", "LinkedIn Post"]
    assert len(first_output["source_references"]) > 0
    assert first_output["validation"] is not None

    # Test Section Regeneration
    regen_resp = client.post(f"/api/transform/output/{output_id}/regenerate-section", json={
        "output_id": output_id,
        "section_name": "Recommended Actions",
        "current_content": "Old actions",
        "feedback": "Emphasize hardware security keys and air-gapped backup"
    })
    assert regen_resp.status_code == 200
    regen_data = regen_resp.json()
    assert "Regenerated" in regen_data["content_markdown"]

    # Test Exports
    pdf_resp = client.post(f"/api/export/pdf?output_id={output_id}")
    assert pdf_resp.status_code == 200
    assert pdf_resp.json()["download_url"].startswith("/api/export/download/")

    docx_resp = client.post(f"/api/export/docx?output_id={output_id}")
    assert docx_resp.status_code == 200
    assert docx_resp.json()["download_url"].startswith("/api/export/download/")

    # Find Presentation output for PPTX export
    presentation_output = next((o for o in outputs if o["output_type"] == "Presentation"), outputs[0])
    pptx_resp = client.post(f"/api/export/pptx?output_id={presentation_output['id']}")
    assert pptx_resp.status_code == 200
    assert pptx_resp.json()["download_url"].startswith("/api/export/download/")

def test_audit_logs_and_templates():
    audit_resp = client.get("/api/audit-logs")
    assert audit_resp.status_code == 200
    assert len(audit_resp.json()) > 0

    tmpl_resp = client.get("/api/templates")
    assert tmpl_resp.status_code == 200
    assert len(tmpl_resp.json()) >= 6

def test_dashboard_stats():
    stats_resp = client.get("/api/dashboard/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["documents_processed"] >= 1
    assert stats["outputs_generated"] >= 1
