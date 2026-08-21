# Vision Loop — Agent & Developer Tooling Guidelines

> **This document governs how all agents, developers, and AI assistants interact with this workspace.**
> Read this before starting any task. These are not suggestions — they are operating standards.

---

## Core Principle

**Always use the highest-level tool available. Never do manually what a tool can do automatically.**

```
Priority Ladder (top = always preferred):
  ┌─────────────────────────────────────────────┐
  │  1. MCP Tool Call        ← fastest, reusable │
  │  2. Repo Script          ← battle-tested     │
  │  3. Shell command        ← one-offs only     │
  │  4. Manual file edit     ← absolute last     │
  └─────────────────────────────────────────────┘
```

---

## 1. MCP Server (Model Context Protocol)

The Vision Loop MCP server is a **Docker-hosted tool API** that exposes all repeated tasks as callable endpoints. Start it once, call it everywhere.

### Start the MCP Server
```bash
docker compose up mcp-server -d
```

### Tool Manifest
```
http://localhost:8765/tools   ← lists all available tools
http://localhost:8765/        ← interactive Swagger UI
```

### Available MCP Tools

| Tool | Endpoint | When to use |
|---|---|---|
| `kg_update` | `POST /tools/kg_update` | After adding any new file to `data/` |
| `kg_verify` | `POST /tools/kg_verify` | Before every commit |
| `kg_query` | `POST /tools/kg_query` | When looking up graph nodes |
| `video_generate_payload` | `POST /tools/video_generate_payload` | Start of every new YouTube video |
| `tts_generate` | `POST /tools/tts_generate` | Generate Hindi voiceover audio |
| `gst_validate_pan` | `POST /tools/gst_validate_pan` | Before using any PAN in a document |
| `gst_validate_gstin` | `POST /tools/gst_validate_gstin` | Before using any GSTIN in a document |
| `run_tests` | `POST /tools/run_tests` | Validate code changes |

### Example MCP Call
```bash
curl -X POST http://localhost:8765/tools/gst_validate_gstin \
  -H "Content-Type: application/json" \
  -d '{"gstin": "09BGVPJ3356G1ZK"}'
```

---

## 2. Workspace Skills

Skills are loaded automatically by the agent when relevant tasks are requested. They live in `.agents/skills/`.

| Skill | Path | Activate for |
|---|---|---|
| `visionloop-ops` | `.agents/skills/visionloop-ops/` | Knowledge graph, integrity, pre-commit, scripts |
| `youtube-production` | `.agents/skills/youtube-production/` | Any YouTube video, script, or short |
| `gst-compliance` | `.agents/skills/gst-compliance/` | GST registration, filing, PAN/GSTIN, SAC codes |

**Agent rule:** Before starting any task, check if a skill covers it. If yes, load the skill first.

---

## 3. Repo Scripts

Scripts in `scripts/` are the fallback when the MCP server is not running.

| Script | Command | Trigger |
|---|---|---|
| `update_knowledge_graph.py` | `python scripts/update_knowledge_graph.py` | After new files added |
| `verify_data_integrity.py` | `python scripts/verify_data_integrity.py` | Before commit |
| `install_hooks.py` | `python scripts/install_hooks.py` | After fresh clone (one-time) |

---

## 4. Git Pre-Commit Hook (Automatic)

The pre-commit hook runs automatically on every `git commit`. It cannot be skipped accidentally.

```
git commit
    │
    ▼
STEP 1: Knowledge Graph Auto-Update  (scripts/update_knowledge_graph.py)
    │     Discovers new files, adds typed nodes, recalculates SHA-256
    ▼
STEP 2: Data Integrity Verification  (scripts/verify_data_integrity.py)
    │     71 mathematical & structural invariants
    ▼
STEP 3: Pytest Suite                 (python -m pytest tests/ -q)
    │     31 automated unit tests
    ▼
COMMIT APPROVED  (or blocked with error details)
```

Emergency bypass (use sparingly): `git commit --no-verify`

---

## 5. When to Create a New Tool / Skill / MCP Endpoint

**Create a new MCP tool when:**
- A task will be repeated more than 3 times
- The task involves external validation (PAN, GSTIN, API calls)
- The output is machine-readable JSON consumed by other tools

**Create a new Skill when:**
- A domain requires 2+ pages of context to work correctly
- The task requires specific file paths, formats, or business rules
- Multiple agents will need the same reference knowledge

**Create a new Script when:**
- The task runs in the pre-commit pipeline
- The task modifies core data files (knowledge_graph.json, etc.)
- The task needs to run in CI/CD without Docker

**Create a new Docker service when:**
- The tool requires heavy dependencies (ML models, FFmpeg, etc.)
- The tool needs persistent state between calls
- Multiple agents need concurrent access

---

## 6. Data & Compliance Rules

These rules apply to every agent interaction in this workspace. No exceptions.

| Rule | Detail |
|---|---|
| **PAN / Aadhaar / Bank data** | Never committed in plaintext. Always blurred (25px Gaussian) in video. Always masked in logs. |
| **Knowledge graph** | Updated automatically by pre-commit hook. Never manually edit `knowledge_graph.json` node counts in tests. |
| **Test counts** | Use `>=` minimum assertions — never hardcode exact node/edge counts. |
| **Windows encoding** | All Python scripts must include `sys.stdout.reconfigure(encoding='utf-8')`. |
| **AI disclosure** | All video descriptions and public content must include the AI-Generated Content disclaimer. |
| **Jurisdiction** | All operations are in Uttar Pradesh (State Code 09). Patna/Bihar = OUT OF SCOPE. |

---

## 7. Workflow for Common Tasks

### A. Add a new YouTube tutorial
1. Load skill: `youtube-production`
2. Call MCP: `POST /tools/video_generate_payload` with topic and CTA
3. Review and refine the script in `data/media/`
4. `git commit` — pre-commit hook auto-registers the new file in the knowledge graph

### B. Add a new service offering
1. Load skill: `visionloop-ops`
2. Create `data/services/<SERVICE_NAME>.md`
3. `git commit` — pre-commit hook auto-discovers and adds the node

### C. Validate a GSTIN before using it
1. Call MCP: `POST /tools/gst_validate_gstin` — never validate manually

### D. Verify the full system is healthy
```bash
# With Docker:
curl http://localhost:8765/tools/kg_verify

# Without Docker:
python scripts/verify_data_integrity.py && python -m pytest tests/ -q
```

### E. Start fresh after cloning
```bash
python scripts/install_hooks.py   # installs pre-commit hook
docker compose up mcp-server -d   # starts MCP server
```

---

## 8. Docker Services Reference

| Service | Container | Port | Purpose |
|---|---|---|---|
| MongoDB | `visionloop-mongodb` | 27017 | Unstructured document store |
| Redis | `visionloop-redis` | 6379 | Cache & message broker |
| **MCP Server** | **`visionloop-mcp`** | **8765** | **Operational tool API** |
| Core API | `visionloop-api` | 8000 | Business logic REST API |
| Telegram Bot | `visionloop-telegram` | — | Customer comms bot |

Start all services: `docker compose up -d`
Start MCP only: `docker compose up mcp-server -d`
View logs: `docker compose logs mcp-server -f`
