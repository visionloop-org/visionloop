#!/usr/bin/env python3
"""
Vision Loop — Docker-Hosted MCP Server
Exposes repeated operational tasks as MCP (Model Context Protocol) tools.

Endpoints exposed:
  /tools/kg_update          → Update knowledge graph
  /tools/kg_verify          → Run data integrity verification
  /tools/kg_query           → Query nodes/edges by type or label
  /tools/video_generate_payload → Generate YouTube video payload JSON
  /tools/tts_generate       → Generate Hindi TTS voiceover audio
  /tools/gst_validate_pan   → Validate PAN number format
  /tools/gst_validate_gstin → Validate GSTIN and extract state
  /tools/run_tests          → Run pytest suite and return JSON results

Run locally:  uvicorn server:app --host 0.0.0.0 --port 8765 --reload
Run via Docker: docker compose up mcp-server -d
"""

import re
import sys
import json
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# FastAPI is the HTTP framework — lightweight and async-native
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
except ImportError:
    print("Install dependencies: pip install fastapi uvicorn pydantic", file=sys.stderr)
    sys.exit(1)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent   # services/mcp-server → root
PYTHON  = sys.executable

app = FastAPI(
    title       = "Vision Loop MCP Server",
    description = "Docker-hosted MCP tool server for repeated Vision Loop operational tasks.",
    version     = "1.0.0",
    docs_url    = "/",
)


# ── HEALTH ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "server": "visionloop-mcp", "root": str(ROOT_DIR)}


# ── MODELS ────────────────────────────────────────────────────────────────────

class KGQueryRequest(BaseModel):
    node_type: str | None = None
    label_contains: str | None = None

class VideoPayloadRequest(BaseModel):
    topic: str
    language: str = "hi-IN"
    format: str = "LONGFORM"         # LONGFORM or SHORTS
    duration_minutes: int = 11
    service_cta: str = ""
    chapters: bool = True

class TTSRequest(BaseModel):
    text: str
    language: str = "hi-IN"
    voice: str = "hi-IN-Neural2-B"
    output_filename: str = "voiceover.mp3"

class PANRequest(BaseModel):
    pan: str

class GSTINRequest(BaseModel):
    gstin: str


# ── TOOL: kg_update ───────────────────────────────────────────────────────────

@app.post("/tools/kg_update")
async def kg_update():
    """Scan repo and update knowledge_graph.json with newly discovered assets."""
    script = ROOT_DIR / "scripts" / "update_knowledge_graph.py"
    result = subprocess.run([PYTHON, str(script)], capture_output=True, text=True, cwd=ROOT_DIR)
    return {
        "tool": "kg_update",
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# ── TOOL: kg_verify ───────────────────────────────────────────────────────────

@app.post("/tools/kg_verify")
async def kg_verify():
    """Run all data integrity invariants and return pass/fail with details."""
    script = ROOT_DIR / "scripts" / "verify_data_integrity.py"
    result = subprocess.run([PYTHON, str(script)], capture_output=True, text=True, cwd=ROOT_DIR)
    passed = result.returncode == 0
    return {
        "tool": "kg_verify",
        "passed": passed,
        "summary": "ALL INVARIANTS PASSED" if passed else "INVARIANTS FAILED",
        "output": result.stdout,
    }


# ── TOOL: kg_query ────────────────────────────────────────────────────────────

@app.post("/tools/kg_query")
async def kg_query(req: KGQueryRequest):
    """Query knowledge graph nodes by type or label substring."""
    kg_path = ROOT_DIR / "knowledge_graph.json"
    if not kg_path.exists():
        raise HTTPException(status_code=404, detail="knowledge_graph.json not found")

    with open(kg_path, encoding="utf-8") as f:
        kg = json.load(f)

    results = kg["nodes"]
    if req.node_type:
        results = [n for n in results if n.get("type", "").lower() == req.node_type.lower()]
    if req.label_contains:
        results = [n for n in results if req.label_contains.lower() in n.get("label", "").lower()]

    return {
        "tool": "kg_query",
        "total_nodes": len(kg["nodes"]),
        "matched": len(results),
        "nodes": results,
    }


# ── TOOL: video_generate_payload ─────────────────────────────────────────────

@app.post("/tools/video_generate_payload")
async def video_generate_payload(req: VideoPayloadRequest):
    """
    Generate a structured YouTube video payload JSON for a given topic.
    Returns a machine-readable payload conforming to VisionLoop video standards.
    """
    slug = re.sub(r"[^a-z0-9]+", "_", req.topic.lower()).strip("_")
    duration_sec = req.duration_minutes * 60

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "topic": req.topic,
        "format_type": f"{'LONGFORM_HORIZONTAL_16_9' if req.format == 'LONGFORM' else 'SHORTS_VERTICAL_9_16'}",
        "target_duration_seconds": duration_sec,
        "visual_spec": {
            "aspect_ratio": "16:9" if req.format == "LONGFORM" else "9:16",
            "resolution_width": 3840 if req.format == "LONGFORM" else 1080,
            "resolution_height": 2160 if req.format == "LONGFORM" else 1920,
            "frame_rate_fps": 30,
            "primary_visual_style": "Screen recording with annotated callout overlays + Presenter PiP. No drone footage.",
            "auto_blur_sensitive_pii": True,
            "sensitive_data_blur_zones": [
                "PAN Numbers — 25px Gaussian Blur",
                "Aadhaar Numbers — 25px Gaussian Blur",
                "Bank Account Numbers & IFSC Codes",
                "OTP values during demonstration",
                "Full Residential Addresses",
            ],
        },
        "voiceover_spec": {
            "primary_language": req.language,
            "voice_name": "hi-IN-Neural2-B" if req.language == "hi-IN" else f"{req.language}-Standard-B",
            "target_loudness_lufs": -14.0,
            "sample_rate_hz": 48000,
            "audio_codec": "AAC-LC",
        },
        "youtube_chapters": [] if not req.chapters else [
            {"timestamp": "00:00", "label": "Introduction"},
            {"timestamp": "01:00", "label": "What is this? Legal context"},
            {"timestamp": "02:30", "label": "When to apply — mandatory vs voluntary"},
            {"timestamp": "04:00", "label": "Benefits"},
            {"timestamp": "05:30", "label": "Liabilities & Drawbacks (MUST WATCH)"},
            {"timestamp": "07:00", "label": "Documents required"},
            {"timestamp": "08:30", "label": "Live portal walkthrough Part A"},
            {"timestamp": "09:45", "label": "Live portal walkthrough Part B"},
            {"timestamp": "11:00", "label": f"Vision Loop Service — {req.service_cta}"},
        ],
        "statutory_disclaimers": {
            "ai_content_disclosure": "AI-Generated Content. For educational purposes only. Consult a licensed CA before filing.",
            "content_rating": "U — Universal / All Ages",
            "resident_grievance_officer": "visionloop.in@gmail.com",
            "compliance": "IT Rules 2021 | ASCI Guidelines | DPDP Act 2023",
        },
        "audit": {
            "auditor_agent": "ChiefAuditorVerificationAgent v2.0",
            "status": "PENDING_REVIEW",
            "note": "Run ChiefAuditorVerificationAgent.cross_examine_and_verify() before committing.",
        },
        "output_path": f"data/media/{slug}_video_payload.json",
    }

    return {"tool": "video_generate_payload", "payload": payload}


# ── TOOL: tts_generate ────────────────────────────────────────────────────────

@app.post("/tools/tts_generate")
async def tts_generate(req: TTSRequest):
    """
    Generate Hindi (or other language) TTS voiceover audio using Edge TTS.
    Returns the output file path. Requires edge-tts to be installed.
    """
    output_dir = ROOT_DIR / "data" / "media" / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / req.output_filename

    try:
        result = subprocess.run(
            ["edge-tts", "--voice", req.voice, "--text", req.text, "--write-media", str(output_path)],
            capture_output=True, text=True, timeout=60
        )
        success = result.returncode == 0
        return {
            "tool": "tts_generate",
            "success": success,
            "output_file": str(output_path) if success else None,
            "error": result.stderr if not success else None,
        }
    except FileNotFoundError:
        return {
            "tool": "tts_generate",
            "success": False,
            "error": "edge-tts not installed. Run: pip install edge-tts",
        }


# ── TOOL: gst_validate_pan ────────────────────────────────────────────────────

# PAN format: AAAAA9999A — 5 uppercase alpha, 4 digits, 1 uppercase alpha
# 4th character encodes entity type: P=Individual, C=Company, H=HUF, etc.
PAN_TYPES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm",
             "A": "AOP", "T": "Trust", "B": "BOI", "G": "Government", "J": "AJP"}

@app.post("/tools/gst_validate_pan")
async def gst_validate_pan(req: PANRequest):
    """Validate Indian PAN number format and return entity type."""
    pan = req.pan.strip().upper()
    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    valid = bool(re.match(pattern, pan))
    fourth_char = pan[3] if len(pan) >= 4 else ""
    return {
        "tool": "gst_validate_pan",
        "pan": pan,
        "valid": valid,
        "fourth_letter": fourth_char,
        "entity_type": PAN_TYPES.get(fourth_char, "Unknown") if valid else None,
        "masked": f"{pan[:5]}****{pan[-1]}" if valid else None,
    }


# ── TOOL: gst_validate_gstin ─────────────────────────────────────────────────

INDIAN_STATES = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
    "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana",
    "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh",
    "13": "Nagaland", "14": "Manipur", "15": "Mizoram",
    "16": "Tripura", "17": "Meghalaya", "18": "Assam",
    "19": "West Bengal", "20": "Jharkhand", "21": "Odisha",
    "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "27": "Maharashtra", "29": "Karnataka", "32": "Kerala",
    "33": "Tamil Nadu", "36": "Telangana", "37": "Andhra Pradesh",
}

@app.post("/tools/gst_validate_gstin")
async def gst_validate_gstin(req: GSTINRequest):
    """Validate a GSTIN number, extract state code, PAN, and entity details."""
    gstin = req.gstin.strip().upper()
    pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
    valid = bool(re.match(pattern, gstin))

    if not valid:
        return {"tool": "gst_validate_gstin", "gstin": gstin, "valid": False, "error": "Invalid GSTIN format"}

    state_code = gstin[:2]
    pan_embedded = gstin[2:12]
    entity_code = gstin[12]
    check_digit = gstin[14]

    return {
        "tool": "gst_validate_gstin",
        "gstin": gstin,
        "valid": True,
        "state_code": state_code,
        "state": INDIAN_STATES.get(state_code, f"Unknown State ({state_code})"),
        "pan_embedded": pan_embedded,
        "entity_registration_number": entity_code,
        "check_digit": check_digit,
        "masked_gstin": f"{state_code}{'*' * 10}{gstin[12:]}",
    }


# ── TOOL: run_tests ───────────────────────────────────────────────────────────

@app.post("/tools/run_tests")
async def run_tests():
    """Run full pytest suite and return structured results."""
    result = subprocess.run(
        [PYTHON, "-m", "pytest", "tests/", "-q", "--tb=short", "--json-report", "--json-report-file=-"],
        capture_output=True, text=True, cwd=ROOT_DIR
    )
    passed = result.returncode == 0
    # Parse simple summary from stdout
    summary_line = ""
    for line in result.stdout.splitlines():
        if "passed" in line or "failed" in line or "error" in line:
            summary_line = line.strip()

    return {
        "tool": "run_tests",
        "passed": passed,
        "summary": summary_line,
        "exit_code": result.returncode,
        "stdout": result.stdout[-3000:],  # last 3000 chars to avoid huge payloads
    }


# ── TOOL LIST (MCP manifest) ──────────────────────────────────────────────────

@app.get("/tools")
async def list_tools():
    """Return the MCP tool manifest — all available tools and their descriptions."""
    return {
        "server": "visionloop-mcp",
        "version": "1.0.0",
        "tools": [
            {"name": "kg_update",              "method": "POST", "path": "/tools/kg_update",              "description": "Scan repo and update knowledge_graph.json with new assets"},
            {"name": "kg_verify",              "method": "POST", "path": "/tools/kg_verify",              "description": "Run 71 data integrity invariants"},
            {"name": "kg_query",               "method": "POST", "path": "/tools/kg_query",               "description": "Query graph nodes by type or label"},
            {"name": "video_generate_payload", "method": "POST", "path": "/tools/video_generate_payload", "description": "Generate YouTube video payload JSON"},
            {"name": "tts_generate",           "method": "POST", "path": "/tools/tts_generate",           "description": "Generate Hindi TTS voiceover audio via Edge TTS"},
            {"name": "gst_validate_pan",       "method": "POST", "path": "/tools/gst_validate_pan",       "description": "Validate PAN number format and entity type"},
            {"name": "gst_validate_gstin",     "method": "POST", "path": "/tools/gst_validate_gstin",     "description": "Validate GSTIN and extract state, PAN, entity"},
            {"name": "run_tests",              "method": "POST", "path": "/tools/run_tests",              "description": "Run full pytest suite"},
        ]
    }
