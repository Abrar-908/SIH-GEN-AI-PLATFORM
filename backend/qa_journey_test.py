import os
import sys
import json
import time
import requests

BASE_URL = "http://127.0.0.1:8000/api"

def log_test(step_num, name, status, details=""):
    badge = "[PASS]" if status else "[FAIL]"
    print(f"{badge} Step {step_num}: {name} - {details}")

def run_qa_suite():
    print("=" * 70)
    print("INTELTRANSFORM AI - COMPLETE END-TO-END QA VERIFICATION SUITE")
    print("=" * 70)

    session = requests.Session()
    failures = []

    # 1. Health check
    try:
        r = session.get(f"{BASE_URL}/health")
        assert r.status_code == 200, f"Status {r.status_code}"
        data = r.json()
        assert data.get("status") == "healthy"
        assert data.get("demo_mode") is True
        log_test(1, "API Health Check", True, f"Service: {data.get('service')} (Demo Mode: {data.get('demo_mode')})")
    except Exception as e:
        log_test(1, "API Health Check", False, str(e))
        failures.append("Step 1: Health check")

    # 2. System Settings
    try:
        r = session.get(f"{BASE_URL}/settings")
        assert r.status_code == 200
        settings = r.json()
        assert "ai_provider" in settings
        assert "chunk_size" in settings
        log_test(2, "Fetch Settings", True, f"Provider: {settings.get('ai_provider')}, Chunk Size: {settings.get('chunk_size')}")
    except Exception as e:
        log_test(2, "Fetch Settings", False, str(e))
        failures.append("Step 2: Settings")

    # 3. Load Sample Document
    sample_doc_id = None
    try:
        r = session.get(f"{BASE_URL}/documents/sample")
        assert r.status_code == 200
        sample_doc = r.json()
        sample_doc_id = sample_doc.get("document_id")
        assert sample_doc_id is not None
        assert sample_doc.get("chunk_count") > 0
        assert len(sample_doc.get("chunks", [])) > 0
        log_test(3, "Load Sample Incident Document", True, f"Doc ID: {sample_doc_id}, Chunks: {sample_doc.get('chunk_count')}, Filename: {sample_doc.get('filename')}")
    except Exception as e:
        log_test(3, "Load Sample Incident Document", False, str(e))
        failures.append("Step 3: Sample Document")

    # 4. Upload Synthetic Custom Document (Testing PDF/TXT upload flow)
    uploaded_doc_id = None
    try:
        test_content = """# SMART INDIA HACKATHON 2024 CYBER INCIDENT
Incident ID: SIH-2024-DEF-0987
Classification: TOP SECRET / RESTRICTED
Date: 2026-09-30 04:15 UTC
Location: Central Power Distribution Grid, Western Node

1. EXECUTIVE OVERVIEW
At 04:15 UTC on September 30, automated network boundary intrusion detection systems (IDS) flagged unauthorized encrypted tunneling originating from IP 198.51.100.42 targeting SCADA telemetry controllers.
Immediate automated isolation protocols disconnected subnet 10.240.12.0/24 within 4 minutes, preventing kinetic disruptions to municipal transformers.

2. TECHNICAL ATTRIBUTION & INDICATORS OF COMPROMISE
The adversary utilized an unpatched vulnerability in Fortinet SSL-VPN (CVE-2024-21762) combined with living-off-the-land binaries (certutil.exe, powershell.exe) to inject memory-only Cobalt Strike beacons.
IOCs:
- SHA-256: 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
- C2 IP: 198.51.100.42:443
- Ingress: /remote/login

3. RECOMMENDED REMEDIATION ACTIONS
- Patch all perimeter VPN gateways immediately to firmware 7.4.3+.
- Enforce FIDO2 hardware MFA tokens across all administrative jump boxes.
- Rotate all domain controller krbtgt passwords and Kerberos ticketing keys.
"""
        files = {"file": ("sih_custom_incident.txt", test_content.encode("utf-8"), "text/plain")}
        r = session.post(f"{BASE_URL}/documents/upload", files=files)
        assert r.status_code == 200, f"Status: {r.status_code}, {r.text}"
        uploaded_doc = r.json()
        uploaded_doc_id = uploaded_doc.get("document_id")
        assert uploaded_doc_id is not None
        assert uploaded_doc.get("chunk_count") >= 1
        log_test(4, "Upload Custom Incident Document", True, f"Doc ID: {uploaded_doc_id}, Chunks: {uploaded_doc.get('chunk_count')}")
    except Exception as e:
        log_test(4, "Upload Custom Incident Document", False, str(e))
        failures.append("Step 4: Upload Document")

    # 5. Test RAG Vector Store Search
    try:
        target_doc = uploaded_doc_id or sample_doc_id
        r = session.post(f"{BASE_URL}/rag/search", json={"document_id": target_doc, "query": "Cobalt Strike SCADA telemetry", "top_k": 3})
        assert r.status_code == 200
        rag_res = r.json()
        assert len(rag_res) > 0
        log_test(5, "RAG Semantic Retrieval", True, f"Retrieved {len(rag_res)} relevant chunks with scores")
    except Exception as e:
        log_test(5, "RAG Semantic Retrieval", False, str(e))
        failures.append("Step 5: RAG Search")

    # 6. Create New Transformation Project
    project_id = None
    try:
        proj_payload = {
            "name": "SIH Western Grid Incident Response",
            "description": "Multi-format transformation for executives, security ops, and public advisory",
            "source_document_id": uploaded_doc_id or sample_doc_id,
            "audience": "Executive",
            "tone": "Urgent",
            "language": "English",
            "detail_level": "Detailed",
            "objective": "Brief",
            "style": "Technical",
            "selected_outputs": [
                "Executive Summary",
                "Security Advisory",
                "Presentation",
                "FAQ / Q&A",
                "Technical Brief"
            ]
        }
        r = session.post(f"{BASE_URL}/projects", json=proj_payload)
        assert r.status_code == 200
        proj_data = r.json()
        project_id = proj_data.get("id")
        assert project_id is not None
        log_test(6, "Create Transformation Project", True, f"Project ID: {project_id} ('{proj_data.get('name')}')")
    except Exception as e:
        log_test(6, "Create Transformation Project", False, str(e))
        failures.append("Step 6: Create Project")

    # 7. Run Multi-Format Transformation Pipeline
    outputs = []
    try:
        trans_payload = {
            "project_id": project_id,
            "selected_outputs": [
                "Executive Summary",
                "Security Advisory",
                "Presentation",
                "FAQ / Q&A",
                "Technical Brief"
            ],
            "audience": "Executive",
            "tone": "Urgent",
            "language": "English",
            "detail_level": "Detailed",
            "objective": "Brief",
            "style": "Technical"
        }
        r = session.post(f"{BASE_URL}/transform", json=trans_payload)
        assert r.status_code == 200, f"Status: {r.status_code}, Detail: {r.text}"
        outputs = r.json()
        assert len(outputs) == 5
        types_gen = [o["output_type"] for o in outputs]
        log_test(7, "Execute Transformation Pipeline", True, f"Generated {len(outputs)} formats: {', '.join(types_gen)}")
    except Exception as e:
        log_test(7, "Execute Transformation Pipeline", False, str(e))
        failures.append("Step 7: Transformation Pipeline")

    # 8. Verify Source Grounding & Citations on Outputs
    for i, out in enumerate(outputs):
        try:
            assert len(out.get("content_markdown", "")) > 100
            assert out.get("word_count", 0) > 20
            sources = out.get("source_references", [])
            assert len(sources) > 0, f"Output {out['output_type']} has no source references"
            # Verify source structure
            s0 = sources[0]
            assert "chunk_id" in s0
            assert "citation" in s0 or "reference" in s0 or "section" in s0
            log_test(8 + i * 0.1, f"Verify Grounding [{out['output_type']}]", True, f"Word Count: {out.get('word_count')}, Citations: {len(sources)}, Confidence: {out.get('confidence_score')}%")
        except Exception as e:
            log_test(8 + i * 0.1, f"Verify Grounding [{out.get('output_type', 'Unknown')}]", False, str(e))
            failures.append(f"Step 8.{i}: Grounding {out.get('output_type')}")

    # 9. Verify Hallucination / Consistency Validation
    first_output = outputs[0] if outputs else None
    if first_output:
        try:
            r = session.get(f"{BASE_URL}/validate/output/{first_output['id']}")
            assert r.status_code == 200
            val_res = r.json()
            assert val_res.get("consistency_score", 0) >= 80.0
            assert val_res.get("supported_claims_count", 0) > 0
            log_test(9, "Factuality & Hallucination Validation", True, f"Score: {val_res.get('consistency_score')}%, Supported: {val_res.get('supported_claims_count')}, Unsupported: {val_res.get('unsupported_claims_count')}")
        except Exception as e:
            log_test(9, "Factuality & Hallucination Validation", False, str(e))
            failures.append("Step 9: Validation")

    # 10. Human Review: Edit and Versioning
    if first_output:
        try:
            orig_md = first_output["content_markdown"]
            edited_md = orig_md + "\n\n### Analyst Review Note (SIH Evaluation)\nVerified zero operational damage to grid. Critical security recommendations validated by lead analyst."
            r = session.put(f"{BASE_URL}/transform/output/{first_output['id']}", json={"content_markdown": edited_md, "change_summary": "Added analyst review notes"})
            assert r.status_code == 200
            updated_out = r.json()
            assert "Analyst Review Note" in updated_out["content_markdown"]

            # Verify version was created
            r_ver = session.get(f"{BASE_URL}/transform/output/{first_output['id']}/versions")
            assert r_ver.status_code == 200
            vers = r_ver.json()
            assert len(vers) >= 1
            log_test(10, "Human-in-the-Loop Edit & Versioning", True, f"Saved new edit. Total versions tracked: {len(vers)}")
        except Exception as e:
            log_test(10, "Human-in-the-Loop Edit & Versioning", False, str(e))
            failures.append("Step 10: Edit & Versioning")

    # 11. Selective Section Regeneration
    if first_output:
        try:
            r = session.post(f"{BASE_URL}/transform/output/{first_output['id']}/regenerate-section", json={
                "output_id": first_output["id"],
                "section_name": "Recommended Actions",
                "current_content": first_output["content_markdown"],
                "guidance": "Emphasize immediate hardware token isolation"
            })
            assert r.status_code == 200
            regen_out = r.json()
            assert len(regen_out.get("content_markdown", "")) > 50
            log_test(11, "Selective Section Regeneration", True, "Successfully updated section without regenerating entire document")
        except Exception as e:
            log_test(11, "Selective Section Regeneration", False, str(e))
            failures.append("Step 11: Section Regeneration")

    # 12. Approval and Rejection Workflow
    if first_output:
        try:
            r = session.post(f"{BASE_URL}/transform/output/{first_output['id']}/approve")
            assert r.status_code == 200
            appr = r.json()
            assert appr.get("approval_state") == "Approved"

            # Reject another output to test rejection state
            if len(outputs) > 1:
                r_rej = session.post(f"{BASE_URL}/transform/output/{outputs[1]['id']}/reject")
                assert r_rej.status_code == 200
                rej = r_rej.json()
                assert rej.get("approval_state") == "Rejected"

            log_test(12, "Approval & Governance Workflow", True, "Successfully Approved output #1 and Rejected output #2")
        except Exception as e:
            log_test(12, "Approval & Governance Workflow", False, str(e))
            failures.append("Step 12: Approval Workflow")

    # 13. File Exporters: PDF, DOCX, PPTX, MD, JSON
    export_formats = [
        ("PDF", "pdf", session.post, f"{BASE_URL}/export/pdf?output_id={first_output['id']}"),
        ("DOCX", "docx", session.post, f"{BASE_URL}/export/docx?output_id={first_output['id']}"),
        ("MD", "md", session.post, f"{BASE_URL}/export/text?output_id={first_output['id']}&format_type=md"),
        ("JSON", "json", session.post, f"{BASE_URL}/export/text?output_id={first_output['id']}&format_type=json"),
    ]
    # Find presentation output for PPTX
    pres_out = next((o for o in outputs if o["output_type"] == "Presentation"), None)
    if pres_out:
        export_formats.append(("PPTX", "pptx", session.post, f"{BASE_URL}/export/pptx?output_id={pres_out['id']}"))

    for fmt_name, ext, func, url in export_formats:
        try:
            r = func(url)
            assert r.status_code == 200, f"Status: {r.status_code}, Body: {r.text}"
            exp_data = r.json()
            download_url = exp_data.get("download_url")
            assert download_url is not None
            # Download file
            full_dl_url = f"http://127.0.0.1:8000{download_url}"
            r_dl = session.get(full_dl_url)
            assert r_dl.status_code == 200
            file_bytes = len(r_dl.content)
            assert file_bytes > 50
            log_test(13, f"Export & Download [{fmt_name}]", True, f"Filename: {exp_data.get('filename')} ({file_bytes} bytes)")
        except Exception as e:
            log_test(13, f"Export & Download [{fmt_name}]", False, str(e))
            failures.append(f"Step 13: Export {fmt_name}")

    # 14. History Page verification
    try:
        r = session.get(f"{BASE_URL}/history")
        assert r.status_code == 200
        hist = r.json()
        assert len(hist) > 0
        log_test(14, "History Repository Query", True, f"Retrieved {len(hist)} transformation runs")
    except Exception as e:
        log_test(14, "History Repository Query", False, str(e))
        failures.append("Step 14: History Query")

    # 15. Dashboard Analytics
    try:
        r = session.get(f"{BASE_URL}/dashboard/stats")
        assert r.status_code == 200
        stats = r.json()
        assert stats.get("documents_processed", 0) > 0
        assert stats.get("outputs_generated", 0) > 0
        log_test(15, "Dashboard Analytics & Metrics", True, f"Docs: {stats.get('documents_processed')}, Outputs: {stats.get('outputs_generated')}, Pass Rate: {stats.get('validation_pass_rate')}")
    except Exception as e:
        log_test(15, "Dashboard Analytics & Metrics", False, str(e))
        failures.append("Step 15: Dashboard Stats")

    # 16. Enterprise Audit Logs
    try:
        r = session.get(f"{BASE_URL}/audit-logs")
        assert r.status_code == 200
        logs = r.json()
        assert len(logs) > 0
        latest_action = logs[0].get("action")
        log_test(16, "Audit Logs Compliance Trail", True, f"Found {len(logs)} tamper-evident audit records. Latest: '{latest_action}'")
    except Exception as e:
        log_test(16, "Audit Logs Compliance Trail", False, str(e))
        failures.append("Step 16: Audit Logs")

    # 17. Transformation Templates
    try:
        r = session.get(f"{BASE_URL}/templates")
        assert r.status_code == 200
        templates = r.json()
        assert len(templates) > 0
        log_test(17, "Transformation Templates Catalog", True, f"Found {len(templates)} preconfigured transformation templates")
    except Exception as e:
        log_test(17, "Transformation Templates Catalog", False, str(e))
        failures.append("Step 17: Templates")

    # 18. Recent Exports Repository
    try:
        r = session.get(f"{BASE_URL}/export/recent")
        assert r.status_code == 200
        recent_exp = r.json()
        assert len(recent_exp) > 0
        log_test(18, "Recent Exports Repository", True, f"Found {len(recent_exp)} downloadable export artifacts")
    except Exception as e:
        log_test(18, "Recent Exports Repository", False, str(e))
        failures.append("Step 18: Recent Exports")

    print("=" * 70)
    if not failures:
        print("ALL 18 END-TO-END QA TESTS PASSED WITH 100% SUCCESS!")
        print("IntelTransform AI is robust, fully verified, and ready for demonstration.")
    else:
        print(f"QA TEST RUN COMPLETED WITH {len(failures)} FAILURE(S):")
        for f in failures:
            print(f" - {f}")
    print("=" * 70)

    return len(failures) == 0

if __name__ == "__main__":
    success = run_qa_suite()
    sys.exit(0 if success else 1)
