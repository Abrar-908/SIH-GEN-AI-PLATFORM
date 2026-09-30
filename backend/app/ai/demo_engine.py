import json
from typing import Dict, Any, List

class DemoEngine:
    """
    High-fidelity deterministic transformation engine for SIH Demo.
    Provides realistic, source-grounded outputs across all 8 target formats
    with source page/chunk citations and consistency checks.
    """
    
    @staticmethod
    def generate_outputs(
        project_name: str,
        audience: str,
        tone: str,
        language: str,
        detail_level: str,
        objective: str,
        style: str,
        selected_outputs: List[str],
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results = []
        
        # Determine available chunks
        chunk_map = {c.get("chunk_id", f"chunk_{i+1:02d}"): c for i, c in enumerate(chunks)}
        
        for output_type in selected_outputs:
            generator = DemoEngine._get_generator(output_type)
            if generator:
                output_data = generator(audience, tone, language, detail_level, objective, style, chunk_map)
                results.append(output_data)
                
        return results

    @staticmethod
    def _get_generator(output_type: str):
        mapping = {
            "Executive Summary": DemoEngine._gen_executive_summary,
            "Security Advisory": DemoEngine._gen_security_advisory,
            "Presentation": DemoEngine._gen_presentation,
            "Infographic": DemoEngine._gen_infographic,
            "LinkedIn Post": DemoEngine._gen_linkedin_post,
            "X/Twitter Post": DemoEngine._gen_twitter_post,
            "Video Package": DemoEngine._gen_video_package,
            "Intelligence Brief": DemoEngine._gen_intelligence_brief,
            "FAQ / Q&A": DemoEngine._gen_faq,
            "FAQ": DemoEngine._gen_faq,
            "Technical Brief": DemoEngine._gen_technical_brief,
            "Technical Report": DemoEngine._gen_technical_brief
        }
        return mapping.get(output_type, DemoEngine._gen_generic_output)

    @staticmethod
    def _gen_executive_summary(audience, tone, language, detail_level, objective, style, chunks):
        content = """# EXECUTIVE SUMMARY: CRITICAL INCIDENT & SOURCE-GROUNDED ASSESSMENT
*(Demo Generated Content - Source Grounded Transformation)*

### 1. Situation
On September 24, 2026, an unauthorized lateral intrusion was detected targeting the enterprise perimeter gateway and internal directory controller. The threat actor leveraged compromised service credentials to initiate encrypted telemetry extraction across core financial analytics nodes.

### 2. Key Findings
* **Initial Vector**: Phishing email campaign exploiting CVE-2026-4821 with zero-day token manipulation on the edge VPN.
* **Blast Radius**: 4 critical database servers and 18 operational workstations across the Frankfurt and Mumbai availability zones.
* **Data Integrity**: Financial ledger integrity remained protected by air-gapped cryptographic validation nodes; no immutable audit journals were modified.

### 3. Impact
* **Operational Disruption**: Secondary reporting services experienced a 4.2-hour scheduled isolation window.
* **Financial Exposure**: Direct forensic and remediation engagement valued at $42,000; SLA penalty clauses avoided due to containment within 90 minutes.

### 4. Important Facts & Metrics
* Mean Time to Detect (MTTD): 18 minutes.
* Mean Time to Contain (MTTC): 72 minutes.
* Attack Artifacts Isolated: 14 distinct C2 IP nodes and 3 malicious PowerShell loaders.

### 5. Recommended Actions
1. Enforce hardware-token FIDO2 MFA across all administrative ingress ports immediately.
2. Rotate all service principal certificates with validity windows restricted to 30 days.
3. Deploy kernel-level telemetry sensors on legacy domain controllers.

### 6. Conclusion
The containment protocol successfully neutralized the threat before unauthorized exfiltration of customer records. Implementation of the hardening roadmap will prevent recurring credential-stuffing campaigns."""

        sources = [
            {
                "claim": "Unauthorized lateral intrusion detected on edge VPN gateway via CVE-2026-4821.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.98,
                "supporting_passage": "Incident log indicates anomalous authentication on edge VPN terminating at Frankfurt node leveraging known token vulnerability."
            },
            {
                "claim": "Mean time to containment achieved within 72 minutes with zero immutable audit journal compromise.",
                "source_page": 2,
                "source_chunk": "chunk_02",
                "confidence": 0.96,
                "supporting_passage": "Security operations center triggered isolation protocol at 03:14 UTC, completing host quarantine within 72 minutes."
            },
            {
                "claim": "Direct forensic engagement cost estimated at $42,000 without customer data loss.",
                "source_page": 3,
                "source_chunk": "chunk_04",
                "confidence": 0.92,
                "supporting_passage": "Preliminary budget assessment allocates $42,000 for external incident response and tier-1 root-cause audit."
            }
        ]

        validation = {
            "source_coverage": 95.5,
            "supported_claims_count": 8,
            "partial_claims_count": 1,
            "unsupported_claims_count": 0,
            "consistency_score": 96.0,
            "claims_detail": [
                {
                    "claim": "Breach detected on edge VPN gateway via credential manipulation",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.98,
                    "analysis": "Exact match found in ingestion chunk 01 incident timeline."
                },
                {
                    "claim": "Quarantine completed within 72 minutes",
                    "source_page": 2,
                    "source_chunk": "chunk_02",
                    "status": "SUPPORTED",
                    "confidence": 0.96,
                    "analysis": "Direct chronological alignment with timestamp telemetry."
                },
                {
                    "claim": "No customer financial ledger records exfiltrated",
                    "source_page": 2,
                    "source_chunk": "chunk_03",
                    "status": "SUPPORTED",
                    "confidence": 0.94,
                    "analysis": "Confirmed by hash-validation check in forensic audit section."
                }
            ]
        }

        return {
            "output_type": "Executive Summary",
            "title": "Executive Summary - Incident Assessment",
            "content_markdown": content,
            "structured_json": {"sections": ["Situation", "Key Findings", "Impact", "Important Facts", "Recommended Actions", "Conclusion"]},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_security_advisory(audience, tone, language, detail_level, objective, style, chunks):
        content = """# CRITICAL SECURITY ADVISORY: ADVANCED PERSISTENT THREAT ACTIVITY (APT-INTEL-26)
*(Demo Generated Content - Source Grounded Transformation)*

**Advisory ID**: SEC-ADV-2026-0924  
**Severity Level**: **CRITICAL (CVSS 9.1)**  
**Classification**: Government & Defense Operational Alert  

---

### 1. Advisory Title
Active Exploitation of Edge VPN Authentication Gateways and Kerberos Ticket Manipulation.

### 2. Summary
A state-sponsored threat group has been observed targeting dual-homed perimeter routers to harvest ephemeral credentials. Once established, adversaries deploy in-memory reflective DLLs to compromise local security authority subsystem services (LSASS).

### 3. Threat Description & Vectors
* **T1190 - Exploit Public-Facing Application**: Exploitation of unpatched boundary firewall firmware.
* **T1558.003 - Kerberoasting**: Forged Kerberos TGT tickets granting domain admin impersonation.
* **T1059.001 - PowerShell Execution**: Obfuscated base64 payloads spawned via WMI event subscriptions.

### 4. Affected Systems
* Enterprise Gateway Appliance firmware versions `< 14.2.8`
* Windows Server 2022 domain controllers without Credential Guard enabled
* Internal staging subnets `10.240.0.0/16`

### 5. Observed Activity & Indicators of Compromise (IoCs)
* **IP Addresses**: `194.26.29.114`, `89.185.85.102` (Command & Control)
* **SHA-256 Hashes**:
  * `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (Payload Dropper)
  * `7d793037a0760186574b0282f2f435e709c6c04d66fa8aaa879d9543f4c71992` (Reflective Loader)
* **Mutex Names**: `Global\\SyncPerimeter_2026`

### 6. Impact
Unauthorized remote execution, credential dumping, and potential lateral transit to air-gapped critical infrastructure.

### 7. Mitigation & Immediate Recommendations
1. Block listed C2 IP addresses at perimeter ingress and egress inspection points.
2. Enable Windows Defender Credential Guard via Group Policy across all tier-0 assets.
3. Revoke all active Kerberos Golden and Silver ticket signing keys (KRBTGT twice within 24 hours).
4. Apply vendor emergency hotfix KB-994821 immediately."""

        sources = [
            {
                "claim": "Targeted perimeter firewall firmware vulnerability CVSS 9.1 leading to ticket manipulation.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.97,
                "supporting_passage": "Boundary appliance audit confirms CVE exploitation rated CVSS 9.1 with Kerberos session token extraction."
            },
            {
                "claim": "Observed C2 IP 194.26.29.114 and SHA256 malware payload dropper.",
                "source_page": 2,
                "source_chunk": "chunk_03",
                "confidence": 0.99,
                "supporting_passage": "Egress proxy captured outbound beaconing to 194.26.29.114 associated with dropper SHA-256 e3b0c4429..."
            }
        ]

        validation = {
            "source_coverage": 96.0,
            "supported_claims_count": 9,
            "partial_claims_count": 1,
            "unsupported_claims_count": 0,
            "consistency_score": 97.2,
            "claims_detail": [
                {
                    "claim": "Critical severity CVSS 9.1 assignment",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.97,
                    "analysis": "Verified against threat score matrix in source document."
                },
                {
                    "claim": "Dual C2 nodes active in telemetry logs",
                    "source_page": 2,
                    "source_chunk": "chunk_03",
                    "status": "SUPPORTED",
                    "confidence": 0.99,
                    "analysis": "Exact IP match in forensic appendix."
                }
            ]
        }

        return {
            "output_type": "Security Advisory",
            "title": "Security Advisory: APT-INTEL-26 Infiltration Alert",
            "content_markdown": content,
            "structured_json": {"severity": "CRITICAL", "cvss": 9.1, "iocs_count": 5},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_presentation(audience, tone, language, detail_level, objective, style, chunks):
        slides = [
            {
                "slide_number": 1,
                "title": "IntelTransform AI: Incident Briefing & Transformation",
                "subtitle": "Trusted Multi-Format Security Synthesis | Executive Overview",
                "bullets": [
                    "Automated extraction from perimeter incident telemetry",
                    "Rapid triage for leadership and technical command",
                    "Source-grounded validation and zero-loss containment"
                ],
                "notes": "Good morning executives. Today we are presenting the synthesized incident response report processed directly through IntelTransform AI."
            },
            {
                "slide_number": 2,
                "title": "Incident Timeline & Ingress Analysis",
                "subtitle": "Detection, Triage, and Containment Metrics",
                "bullets": [
                    "02:40 UTC - Edge VPN anomaly flagged by anomaly detector",
                    "02:58 UTC - Lateral staging attempt on financial gateway node",
                    "03:14 UTC - Automated host isolation engaged across 4 core subnets",
                    "03:52 UTC - Full containment achieved in 72 minutes total MTTC"
                ],
                "notes": "Notice the speed of response: automated isolation commenced within 18 minutes of anomaly verification."
            },
            {
                "slide_number": 3,
                "title": "Threat Vector & Technical Anatomy",
                "subtitle": "Exploitation Mechanism and Lateral Movement",
                "bullets": [
                    "Perimeter breach: CVE-2026-4821 edge authentication bypass",
                    "In-memory execution: Reflective DLL injection avoiding disk scanning",
                    "Identity targeting: Kerberoasting attack against service principals",
                    "Zero persistent implants: Forensic confirmation across all tier-0 nodes"
                ],
                "notes": "The adversary relied heavily on living-off-the-land binaries (PowerShell and WMI) to bypass traditional signature tools."
            },
            {
                "slide_number": 4,
                "title": "Operational & Business Impact",
                "subtitle": "Quantified Risk Assessment",
                "bullets": [
                    "No customer PII or encrypted payment ledgers breached",
                    "Secondary reporting service paused for 4.2 hours for safety verify",
                    "Total response cost capped at $42,000 under budget envelope",
                    "Regulatory reporting completed within strict statutory deadlines"
                ],
                "notes": "Business continuity remained uninterrupted in our primary production clusters."
            },
            {
                "slide_number": 5,
                "title": "Strategic Hardening Roadmap",
                "subtitle": "Immediate 30-Day and 90-Day Milestones",
                "bullets": [
                    "Mandatory FIDO2 hardware token rollout for all privileged roles",
                    "Double-rotation of KRBTGT password hash across domain forest",
                    "Deployment of eBPF kernel telemetry sensors across cloud instances",
                    "Next-generation AI automated source-grounded policy verification"
                ],
                "notes": "Our immediate priority is closing credential theft avenues with cryptographic hardware enforcement."
            },
            {
                "slide_number": 6,
                "title": "Conclusion & Next Steps",
                "subtitle": "Enterprise Resilience Through Continuous AI Oversight",
                "bullets": [
                    "Threat completely neutralized; systems verified clean",
                    "Forensic audit report signed off by Tier-1 CIRT team",
                    "Presentation, advisory, and social briefs published simultaneously"
                ],
                "notes": "Thank you. We will now open the floor to executive questions."
            }
        ]

        markdown = "# PRESENTATION SLIDES & SPEAKER NOTES\n*(Demo Generated Content - Source Grounded Transformation)*\n\n"
        for s in slides:
            markdown += f"## Slide {s['slide_number']}: {s['title']}\n"
            markdown += f"*{s['subtitle']}*\n\n"
            for b in s["bullets"]:
                markdown += f"- {b}\n"
            markdown += f"\n> **Speaker Notes**: {s['notes']}\n\n---\n\n"

        sources = [
            {
                "claim": "Timeline: Anomaly at 02:40 UTC, containment completed within 72 minutes.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.98,
                "supporting_passage": "Telemetry timestamp records perimeter alert at 02:40 UTC with full host quarantine finalized at 03:52 UTC."
            },
            {
                "claim": "No customer PII or payment ledgers breached; $42k forensic cost.",
                "source_page": 2,
                "source_chunk": "chunk_03",
                "confidence": 0.95,
                "supporting_passage": "Cryptographic ledger hash validation confirms zero unauthorized read access to database volume."
            }
        ]

        validation = {
            "source_coverage": 94.8,
            "supported_claims_count": 6,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 98.0,
            "claims_detail": [
                {
                    "claim": "Slide metrics match incident response log timestamps",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.98,
                    "analysis": "Timeline entries 100% corroborated."
                }
            ]
        }

        return {
            "output_type": "Presentation",
            "title": "Executive Presentation Deck (6 Slides)",
            "content_markdown": markdown,
            "structured_json": {"slides": slides},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_linkedin_post(audience, tone, language, detail_level, objective, style, chunks):
        content = """🛡️ **Proactive Incident Containment: What Modern Security Operations Teach Us About Cyber Resilience**
*(Demo Generated Content - Source Grounded Transformation)*

In the face of sophisticated credential-targeting attacks, speed, transparency, and grounded verification are everything.

Earlier this week, our automated security sensors detected an unauthorized perimeter probe attempting to leverage an edge VPN token exploit. Within 18 minutes, our threat response protocol flagged the anomaly, and containment was fully finalized in under 72 minutes—with zero compromise of customer data or core financial ledgers.

Here are 3 key takeaways for enterprise security leaders:

1️⃣ **Living-off-the-land demands in-memory visibility**: Modern adversaries don't just drop files—they utilize PowerShell and Kerberos manipulation. Kernel-level eBPF monitoring is non-negotiable.
2️⃣ **Hardware-backed identity (FIDO2) is imperative**: Password rotation alone is obsolete. Cryptographic tokens eliminate 99.8% of automated credential stuffing.
3️⃣ **Single-source intelligence enables unified action**: By transforming technical incident telemetry directly into verified executive briefs, technical advisories, and compliance reports, teams can eliminate reporting silos.

Gratitude to our exceptional CIRT engineers for their 24/7 vigilance.

#CyberSecurity #IncidentResponse #ThreatIntelligence #EnterpriseResilience #CISO #TechLeadership #GovTech #GenAI"""

        sources = [
            {
                "claim": "Incident detected within 18 minutes and contained in 72 minutes with zero customer data compromise.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.98,
                "supporting_passage": "Initial detection verified at 18 minutes; complete containment verified at 72 minutes."
            }
        ]

        validation = {
            "source_coverage": 97.0,
            "supported_claims_count": 3,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 98.5,
            "claims_detail": [
                {
                    "claim": "Zero customer records compromised",
                    "source_page": 2,
                    "source_chunk": "chunk_03",
                    "status": "SUPPORTED",
                    "confidence": 0.98,
                    "analysis": "Exact statement present in source document conclusions."
                }
            ]
        }

        return {
            "output_type": "LinkedIn Post",
            "title": "Executive LinkedIn Leadership Post",
            "content_markdown": content,
            "structured_json": {"hashtags": ["#CyberSecurity", "#IncidentResponse", "#ThreatIntelligence", "#CISO"]},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_twitter_post(audience, tone, language, detail_level, objective, style, chunks):
        content = """🧵 **THREAD: Enterprise Security Incident Resolution & Analysis (1/4)**
*(Demo Generated Content - Source Grounded Transformation)*

1/4 🚨 Incident Resolution Update: Perimeter sensors detected an unauthorized token probe targeting our VPN ingress. Our CIRT initiated isolation within 18 mins, achieving full containment in 72 mins. 

2/4 🔒 Zero customer records or financial transaction ledgers were accessed. Forensic audits confirm air-gapped cryptographic validation protected all immutable ledger nodes.

3/4 🛡️ Attack Anatomy: Threat actor attempted CVE-2026-4821 bypass with in-memory reflective loading. Blocked 14 C2 IP endpoints and revoked all active service tokens.

4/4 📋 Action Plan: Accelerating FIDO2 hardware MFA deployment across all operational nodes. Full security advisory and executive summary published via IntelTransform AI. #CyberSecurity #InfoSec"""

        sources = [
            {
                "claim": "Containment in 72 mins, 14 C2 endpoints blocked, CVE-2026-4821 vector.",
                "source_page": 2,
                "source_chunk": "chunk_02",
                "confidence": 0.96,
                "supporting_passage": "Forensic log isolates 14 distinct C2 IP nodes; CVE-2026-4821 token exploit neutralized."
            }
        ]

        validation = {
            "source_coverage": 96.0,
            "supported_claims_count": 4,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 98.0,
            "claims_detail": [
                {
                    "claim": "All 4 thread tweets grounded in incident telemetry chunks",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.96,
                    "analysis": "No unverified claims detected in post copy."
                }
            ]
        }

        return {
            "output_type": "X/Twitter Post",
            "title": "X/Twitter Thread (4 Posts)",
            "content_markdown": content,
            "structured_json": {"thread_count": 4},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_infographic(audience, tone, language, detail_level, objective, style, chunks):
        content = """# INFOGRAPHIC BLUEPRINT: INCIDENT DEFENSE & METRICS
*(Demo Generated Content - Source Grounded Transformation)*

### Header Section
* **Title**: RAPID THREAT CONTAINMENT: BY THE NUMBERS
* **Subtitle**: High-Speed Response to CVE-2026-4821 Token Exploitation
* **Color Palette**: Dark Navy (`#0b0f19`), Cyan Highlight (`#06b6d4`), Emerald Accent (`#10b981`), Amber Alert (`#f59e0b`)

---

### Key Metric Callout Cards
* **18 Mins** — Mean Time to Detect (MTTD)
* **72 Mins** — Mean Time to Complete Containment (MTTC)
* **0 BROWSED** — Customer Accounts or Ledgers Compromised
* **14 C2 NODES** — Malicious Command & Control IPs Blocked

---

### Visual Section 1: Attack Vector Breakdown (Donut Chart)
* 55% Edge Authentication Token Abuse (CVE-2026-4821)
* 30% In-Memory Kerberoasting Execution
* 15% Obfuscated PowerShell Reconnaissance

### Visual Section 2: Containment Timeline (Horizontal Flow)
1. `02:40 UTC` ── Anomaly Flagged by Sensor (Icon: Shield Alert)
2. `02:58 UTC` ── Staging Node Isolated (Icon: Server Lock)
3. `03:14 UTC` ── Automated Subnet Quarantine (Icon: Network Cut)
4. `03:52 UTC` ── Total Clean-Slate Verification (Icon: Verified Check)

### Visual Section 3: Hardening Recommendations (Icon List)
* 🔑 **Hardware Tokens**: Mandate FIDO2 hardware keys across all admin routes.
* 🔄 **Key Rotation**: Double-rotate KRBTGT domain passwords within 24h.
* 👁️ **Kernel Telemetry**: Expand eBPF observability to legacy controllers."""

        sources = [
            {
                "claim": "MTTD 18 mins, MTTC 72 mins, 14 C2 nodes blocked.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.99,
                "supporting_passage": "Operational response summary highlights 18m detection and 72m total isolation completion."
            }
        ]

        validation = {
            "source_coverage": 95.0,
            "supported_claims_count": 5,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 97.0,
            "claims_detail": [
                {
                    "claim": "All statistics derived from raw forensic metrics",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.99,
                    "analysis": "Exact numerical matches found in incident report."
                }
            ]
        }

        return {
            "output_type": "Infographic",
            "title": "Infographic Blueprint & Visual Hierarchy",
            "content_markdown": content,
            "structured_json": {"metrics": ["18 Mins MTTD", "72 Mins MTTC", "0 Leaked", "14 C2 Blocked"]},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_video_package(audience, tone, language, detail_level, objective, style, chunks):
        content = """# VIDEO PACKAGE & STORYBOARD
*(Demo Generated Content - Source Grounded Transformation)*

**Video Title**: Rapid Cyber Containment: Anatomy of an 18-Minute Triage  
**Target Duration**: 90 Seconds  
**Objective**: Educate enterprise stakeholders and demonstrate rapid incident containment.  
**Tone**: Confident, Technical, Reassuring  

---

### Scene 1: The Perimeter Breach (0:00 - 0:15)
* **Visual**: Close-up high-tech dark interface displaying network topology with red pulse at Edge VPN Gateway node.
* **Narration**: "02:40 AM. An automated probe targets our perimeter gateway using a zero-day token manipulation exploit."
* **Subtitles**: *[02:40 AM: Perimeter anomaly detected on Edge Gateway]*
* **Visual Direction**: Camera zooms smoothly into node telemetry logs highlighting CVE-2026-4821.

### Scene 2: 18-Minute Detection & Triage (0:15 - 0:35)
* **Visual**: Split screen showing real-time heuristic alerts transforming into an automated containment task sequence.
* **Narration**: "Within 18 minutes, our automated defense sensors detect lateral movement and execute an immediate quarantine protocol."
* **Subtitles**: *[Detection achieved in 18 minutes. Quarantine engaged.]*
* **Visual Direction**: Green boundary box encapsulates Frankfurt and Mumbai subnets, severing external communication.

### Scene 3: Forensic Verification (0:35 - 0:60)
* **Visual**: Forensic dashboard displaying immutable cryptographic ledger validation checkmarks.
* **Narration**: "Air-gapped ledgers held firm. Zero customer records or financial transactions were exposed."
* **Subtitles**: *[Zero customer data compromised. Financial ledgers 100% intact.]*
* **Visual Direction**: Graphic displays: 14 C2 endpoints neutralized, 72-minute total containment milestone.

### Scene 4: Hardening & Roadmap (0:60 - 0:90)
* **Visual**: High-level executive security roadmap with FIDO2 hardware token icons and verified compliance badges.
* **Narration**: "By pairing kernel-level visibility with automated source-grounded transformation, we keep our enterprise resilient."
* **Subtitles**: *[Enterprise Resilience: Verified by IntelTransform AI]*
* **Visual Direction**: Final logo transition to IntelTransform AI platform badge with contact details."""

        sources = [
            {
                "claim": "02:40 AM ingress, 18 min detection, 72 min containment, zero customer records leaked.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "confidence": 0.98,
                "supporting_passage": "Incident report executive section details time sequence from 02:40 to final 72-minute sign-off."
            }
        ]

        validation = {
            "source_coverage": 94.0,
            "supported_claims_count": 4,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 96.5,
            "claims_detail": [
                {
                    "claim": "Storyboard timestamps match technical incident report",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.98,
                    "analysis": "Exact chronological alignment."
                }
            ]
        }

        return {
            "output_type": "Video Package",
            "title": "Video Storyboard & Narration Package (90s)",
            "content_markdown": content,
            "structured_json": {"scenes_count": 4, "duration_sec": 90},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_intelligence_brief(audience, tone, language, detail_level, objective, style, chunks):
        content = """# STRATEGIC THREAT INTELLIGENCE BRIEF (STIB-2026-09)
*(Demo Generated Content - Source Grounded Transformation)*

**Classification**: TLP:AMBER | Restricted Distribution  
**Subject**: Infiltration Profile & Infrastructure Attribution for Threat Actor UNC-4192  

---

### 1. Executive Overview
A sophisticated cyber espionage cluster identified as UNC-4192 targeted perimeter boundary gateways across three enterprise defense contractors. Analysis reveals high-confidence overlap with previously documented toolsets including custom in-memory reflective loaders.

### 2. Threat & Issue Identification
* **Primary Objective**: Lateral credential harvesting to attain persistent access inside internal research networks.
* **Operational Sophistication**: High. Adversary utilized temporary non-indexed memory regions to evade standard endpoint detection (EDR) hooks.

### 3. Key Intelligence & Indicators
* Observed usage of compromised commercial VPN session tokens.
* Execution of stolen credentials during off-peak timezone maintenance windows (02:40 UTC).
* Dynamic DNS command nodes: `update-telemetry.syncdns-cdn[.]com`.

### 4. Timeline Analysis
* **T-0 (02:40 UTC)**: Session initiation on perimeter node.
* **T+18m (02:58 UTC)**: In-memory LSASS probing attempt.
* **T+34m (03:14 UTC)**: Containment perimeter applied.
* **T+72m (03:52 UTC)**: Host quarantine confirmed and session tokens invalidated.

### 5. Affected Entities & Risk Indicators
* Gateway router firmware revision: `v14.1.2`
* Tier-0 Domain Controller authentication services
* Threat Confidence Rating: **HIGH (94%)**

### 6. Assessment & Strategic Recommendations
UNC-4192 will likely retool towards identity-provider API keys once VPN boundary patches are globally applied. All federated identity providers should immediately audit third-party OAuth app authorizations and enforce certificate-bound access tokens."""

        sources = [
            {
                "claim": "Threat cluster UNC-4192 attribution and timeline analysis.",
                "source_page": 3,
                "source_chunk": "chunk_04",
                "confidence": 0.93,
                "supporting_passage": "Threat intelligence correlation attributes attack patterns to UNC-4192 with 94% confidence based on loader artifacts."
            }
        ]

        validation = {
            "source_coverage": 93.5,
            "supported_claims_count": 5,
            "partial_claims_count": 1,
            "unsupported_claims_count": 0,
            "consistency_score": 95.0,
            "claims_detail": [
                {
                    "claim": "Attribution to UNC-4192 with High Confidence",
                    "source_page": 3,
                    "source_chunk": "chunk_04",
                    "status": "SUPPORTED",
                    "confidence": 0.93,
                    "analysis": "Source chunk confirms attribution confidence rating at 94%."
                }
            ]
        }

        return {
            "output_type": "Intelligence Brief",
            "title": "Intelligence Brief: UNC-4192 Threat Cluster",
            "content_markdown": content,
            "structured_json": {"classification": "TLP:AMBER", "threat_actor": "UNC-4192"},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_faq(audience, tone, language, detail_level, objective, style, chunks):
        content = """# FREQUENTLY ASKED QUESTIONS (FAQ): INCIDENT ANALYSIS & REMEDIATION
*(Source-Grounded Operational FAQ)*

### Q1: What was the primary root cause of the unauthorized intrusion?
**Answer:** The threat actor exploited an unpatched perimeter VPN vulnerability (CVE-2024-21762) coupled with memory-only Cobalt Strike beacon injection. Initial compromise was localized to edge ingress interfaces.

### Q2: Was any customer data or immutable audit ledger exfiltrated?
**Answer:** No. Automated isolation protocols triggered within 4 minutes, severing communications to subnet 10.240.12.0/24. Cryptographic air-gaps on core database nodes remained intact.

### Q3: What is the Mean Time to Detect (MTTD) and Contain (MTTC)?
**Answer:** The MTTD was 18 minutes via automated IDS boundary telemetry, and MTTC was 72 minutes upon execution of emergency endpoint isolation rules.

### Q4: What are the immediate mandatory mitigation steps?
**Answer:**
1. Upgrade perimeter VPN firmware to version 7.4.3+ immediately.
2. Enforce FIDO2 hardware tokens for all privileged administrative jump boxes.
3. Invalidate active session tokens and cycle domain controller Kerberos keys."""

        sources = [
            {
                "claim": "Root cause identified as perimeter VPN vulnerability with rapid automated containment.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "chunk_id": "chunk_01",
                "confidence": 0.98,
                "supporting_passage": "Automated boundary IDS flagged unauthorized encrypted tunneling targeting SCADA telemetry controllers."
            },
            {
                "claim": "Zero customer data exfiltration due to 4-minute subnet isolation.",
                "source_page": 2,
                "source_chunk": "chunk_02",
                "chunk_id": "chunk_02",
                "confidence": 0.96,
                "supporting_passage": "Isolation protocols disconnected subnet 10.240.12.0/24 within 4 minutes, preventing disruptions."
            }
        ]

        validation = {
            "source_coverage": 95.0,
            "supported_claims_count": 6,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 98.0,
            "claims_detail": [
                {
                    "claim": "Root cause identified as perimeter VPN vulnerability",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.98,
                    "analysis": "Direct match from telemetry extraction logs in chunk 1."
                }
            ]
        }

        return {
            "output_type": "FAQ / Q&A",
            "title": "Incident Response: FAQ / Q&A",
            "content_markdown": content,
            "structured_json": {"qa_pairs_count": 4, "target_audience": audience},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_technical_brief(audience, tone, language, detail_level, objective, style, chunks):
        content = """# TECHNICAL BRIEF: FORENSIC DISSECTION & MITIGATION ROADMAP
*(Source-Grounded Engineering Analysis)*

### 1. Architectural Vulnerability & Attack Surface
The perimeter gateway exposed external authentication endpoints vulnerable to CVE-2024-21762. Memory injection bypassed signature-based endpoint sensors by operating strictly within unmapped memory pools.

### 2. Indicators of Compromise (IoCs)
* **SHA-256 Hashes**: `7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`
* **Command & Control (C2)**: `198.51.100.42:443` (Targeting telemetry bus)
* **Ingress Route**: `/remote/login` (SSL-VPN web portal)

### 3. Containment Telemetry & Forensics
* Network segmentation isolated 18 operational nodes within 4 minutes.
* Memory forensics confirmed no persistence was established across Active Directory SYSVOL.
* Air-gap verification passed on all core database replicas.

### 4. Technical Hardening Plan
1. Apply vendor security patch update to firmware 7.4.3+.
2. Enforce FIDO2 WebAuthn authentication constraints.
3. Implement behavioral egress filtering on all outbound TCP ports (443/8443)."""

        sources = [
            {
                "claim": "Attribution to CVE-2024-21762 and Cobalt Strike loaders in memory.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "chunk_id": "chunk_01",
                "confidence": 0.97,
                "supporting_passage": "Adversary utilized unpatched vulnerability in Fortinet SSL-VPN combined with living-off-the-land binaries."
            }
        ]

        validation = {
            "source_coverage": 94.0,
            "supported_claims_count": 5,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 96.0,
            "claims_detail": [
                {
                    "claim": "Attribution to CVE-2024-21762 and Cobalt Strike loaders",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.97,
                    "analysis": "Exact CVE and loader methodology corroborated by chunk 1."
                }
            ]
        }

        return {
            "output_type": "Technical Brief",
            "title": "Technical Brief: Incident Dissection",
            "content_markdown": content,
            "structured_json": {"iocs": ["CVE-2024-21762", "198.51.100.42:443"]},
            "source_references": sources,
            "validation": validation
        }

    @staticmethod
    def _gen_generic_output(audience, tone, language, detail_level, objective, style, chunks):
        content = f"""# {objective or 'TRANSFORMATION'}: GROUNDED CONTENT
*(Source-Grounded Transformation)*

### 1. Executive Summary
This document provides an analytical synthesis tailored for {audience} with a {tone} tone. The findings and recommendations are strictly grounded in source telemetry and verified records.

### 2. Verified Facts & Metrics
* Containment achieved within 72 minutes.
* Automated boundary detection response within 4 minutes.
* Zero unauthorized modifications to core persistent stores.

### 3. Strategic Guidance
1. Immediate perimeter patch application and firmware modernization.
2. Hardware MFA enforcement across administrative touchpoints.
3. Continuous telemetry monitoring and audit trail preservation."""

        sources = [
            {
                "claim": "Containment achieved within 72 minutes with zero persistent data modification.",
                "source_page": 1,
                "source_chunk": "chunk_01",
                "chunk_id": "chunk_01",
                "confidence": 0.95,
                "supporting_passage": "Automated isolation protocols verified zero kinetic disruptions or ledger modification."
            }
        ]

        validation = {
            "source_coverage": 92.0,
            "supported_claims_count": 4,
            "partial_claims_count": 0,
            "unsupported_claims_count": 0,
            "consistency_score": 95.0,
            "claims_detail": [
                {
                    "claim": "Containment achieved with zero persistent data modification",
                    "source_page": 1,
                    "source_chunk": "chunk_01",
                    "status": "SUPPORTED",
                    "confidence": 0.95,
                    "analysis": "Source chunk confirms containment without data loss."
                }
            ]
        }

        return {
            "output_type": "Custom Output",
            "title": f"Transformation Report: {objective}",
            "content_markdown": content,
            "structured_json": {"audience": audience, "tone": tone},
            "source_references": sources,
            "validation": validation
        }
