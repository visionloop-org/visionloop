---
name: visionloop-ops
description: >
  Vision Loop operational task automation skill. Use this skill for any
  repeated operational task in the VisionLoop workspace — knowledge graph
  updates, integrity verification, video payload generation, GST compliance
  checks, and pre-commit pipeline operations.
  Activate when the user asks to: run checks, update the graph, verify data,
  generate video assets, or perform any repeated operational task.
---

# Vision Loop Ops Skill

## Core Philosophy
**Prefer tools over manual steps. Prefer scripts over inline commands. Prefer MCP calls over scripts where an MCP is available.**

```
Priority order (highest to lowest):
  1. Call an MCP tool                 → fastest, most reusable
  2. Run a repo script (scripts/)     → second best
  3. Run a shell command              → use only for one-offs
  4. Manual file editing              → last resort
```

---

## Available MCP Servers

### 1. VisionLoop Operations MCP (`visionloop-mcp`)
Running at `http://localhost:8765` when Docker Compose is up.

| Tool | Description |
|---|---|
| `kg_update` | Scan repo and update knowledge_graph.json |
| `kg_verify` | Run 71 integrity invariants, return pass/fail |
| `kg_query` | Query nodes/edges by type or label |
| `video_generate_payload` | Generate a YouTube video payload JSON for a topic |
| `tts_generate` | Generate Hindi TTS audio from a script string |
| `gst_validate_pan` | Validate a PAN number format |
| `gst_validate_gstin` | Validate a GSTIN number and extract state code |
| `run_tests` | Run full pytest suite and return results JSON |

Start the MCP server:
```bash
docker compose up mcp-server -d
```

---

## Repo Scripts (when MCP is unavailable)

| Script | Command | When to use |
|---|---|---|
| `update_knowledge_graph.py` | `python scripts/update_knowledge_graph.py` | After adding new files |
| `verify_data_integrity.py` | `python scripts/verify_data_integrity.py` | Before any commit |
| `install_hooks.py` | `python scripts/install_hooks.py` | After fresh clone |

---

## Repeated Task Playbooks

### A. Add a new service/document to the repo
1. Create the file in the correct `data/` subdirectory
2. Run: `python scripts/update_knowledge_graph.py` (or call `kg_update` via MCP)
3. Verify: `python scripts/verify_data_integrity.py`
4. Commit — pre-commit hook runs steps 2 & 3 automatically

### B. Generate a YouTube video payload
1. Call MCP tool: `video_generate_payload(topic, language="hi-IN", format="LONGFORM")`
2. Review the returned JSON payload
3. Save to `data/media/<topic>_video_payload.json`
4. Commit — pre-commit hook auto-registers the new file in the knowledge graph

### C. Run a full system health check
```bash
python scripts/verify_data_integrity.py && python -m pytest tests/ -q
```

### D. Generate Hindi voiceover audio
```bash
python scripts/generate_tts.py --script "data/media/SCRIPT.md" --lang hi-IN --output data/media/audio/
```

---

## Rules for This Workspace

1. **Never hardcode node/edge counts in tests** — use `>=` minimums.
2. **Every new file added to `data/`** must be captured in the knowledge graph before commit.
3. **All video payloads** must pass the 4-inquest `ChiefAuditorVerificationAgent` before committing.
4. **No personal PAN, Aadhaar, or bank data** is ever committed in plaintext — always blurred or redacted.
5. **All Python scripts** must include `sys.stdout.reconfigure(encoding='utf-8')` for Windows compatibility.
