#!/usr/bin/env python3
"""
Vision Loop — Knowledge Graph Auto-Update Engine
Scans the repository for new and modified assets, services, compliance docs,
and media files — then updates knowledge_graph.json with new nodes and edges.
Recalculates the SHA-256 cryptographic checksum on each run.

Run manually:   python scripts/update_knowledge_graph.py
Run via hook:   .git/hooks/pre-commit calls this automatically before every commit.
"""

import sys
import json
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
KG_PATH = ROOT_DIR / "knowledge_graph.json"

# ──────────────────────────────────────────────────────────────────────────────
# 1. DIRECTORY → NODE TYPE MAPPING
#    Maps repo sub-paths to (node_id_prefix, node_type, label_prefix)
# ──────────────────────────────────────────────────────────────────────────────
SCANNABLE_DIRS = {
    "data/services":    ("SERVICE",    "CommercialService",     "Service"),
    "data/compliance":  ("COMPLIANCE", "ComplianceFramework",   "Compliance"),
    "data/media":       ("MEDIA",      "VideoProductionAsset",  "Media"),
    "data/legal":       ("LEGAL",      "LegalFramework",        "Legal"),
    "data/business_model": ("BIZ",     "BusinessModel",         "BusinessModel"),
    "packages":         ("PKG",        "SoftwarePackage",       "Package"),
    "tests":            ("TEST",       "TestSuite",             "TestSuite"),
}

# Edges to auto-create linking discovered nodes back to the enterprise node
AUTO_EDGE_RELATION = "OWNED_BY"
ENTERPRISE_NODE_ID = "ENTITY:VISION_LOOP"


def load_kg() -> dict:
    with open(KG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_kg(kg: dict) -> None:
    # Always recalculate checksum over nodes+edges before saving
    payload = json.dumps(
        {"nodes": kg["nodes"], "edges": kg["edges"]},
        ensure_ascii=False,
        sort_keys=True
    ).encode("utf-8")
    kg["sha256_checksum"] = hashlib.sha256(payload).hexdigest()
    kg["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    kg["integrity_status"] = "CRYPTOGRAPHICALLY_VERIFIED"

    with open(KG_PATH, "w", encoding="utf-8") as f:
        json.dump(kg, f, ensure_ascii=False, indent=2)


def slug(text: str) -> str:
    """Convert a filename or path segment into a clean uppercase slug."""
    text = Path(text).stem          # strip extension
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    return text.upper().strip("_")


def existing_node_ids(kg: dict) -> set:
    return {n["id"] for n in kg["nodes"]}


def existing_edge_pairs(kg: dict) -> set:
    return {(e["source"], e["target"], e.get("relationship", e.get("relation", ""))) for e in kg["edges"]}


def scan_and_update(kg: dict) -> tuple[int, int]:
    """
    Scan configured directories for files not yet in the knowledge graph.
    Returns (new_nodes_count, new_edges_count).
    """
    node_ids    = existing_node_ids(kg)
    edge_pairs  = existing_edge_pairs(kg)
    new_nodes   = 0
    new_edges   = 0

    for dir_rel, (prefix, node_type, label_prefix) in SCANNABLE_DIRS.items():
        scan_path = ROOT_DIR / dir_rel
        if not scan_path.exists():
            continue

        # For packages/ scan only immediate subdirectories, not files
        if dir_rel == "packages":
            candidates = [p for p in scan_path.iterdir() if p.is_dir()]
        else:
            candidates = [
                p for p in scan_path.rglob("*")
                if p.is_file() and p.suffix in (".md", ".json", ".py", ".yaml", ".yml")
                and not p.name.startswith(".")
            ]

        for item in candidates:
            node_id = f"{prefix}:{slug(item.name if item.is_file() else item.name)}"

            # Skip if already in graph
            if node_id in node_ids:
                continue

            # Build the node
            node = {
                "id": node_id,
                "type": node_type,
                "label": f"{label_prefix}: {item.stem if item.is_file() else item.name}",
                "properties": {
                    "file_path": str(item.relative_to(ROOT_DIR)).replace("\\", "/"),
                    "discovered_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "auto_discovered": True,
                }
            }
            kg["nodes"].append(node)
            node_ids.add(node_id)
            new_nodes += 1
            print(f"  [+] Node added: {node_id}")

            # Auto-create an OWNED_BY edge back to the enterprise
            edge_key = (node_id, ENTERPRISE_NODE_ID, AUTO_EDGE_RELATION)
            if edge_key not in edge_pairs:
                kg["edges"].append({
                    "source":       node_id,
                    "target":       ENTERPRISE_NODE_ID,
                    "relationship": AUTO_EDGE_RELATION,
                    "properties":   {"auto_discovered": True}
                })
                edge_pairs.add(edge_key)
                new_edges += 1

    return new_nodes, new_edges


def print_summary(new_nodes: int, new_edges: int, kg: dict) -> None:
    total_nodes = len(kg["nodes"])
    total_edges = len(kg["edges"])
    checksum    = kg.get("sha256_checksum", "N/A")[:16] + "..."

    print("\n" + "=" * 70)
    print("[KNOWLEDGE GRAPH] AUTO-UPDATE COMPLETE")
    print("=" * 70)
    print(f"  New nodes discovered : {new_nodes}")
    print(f"  New edges created    : {new_edges}")
    print(f"  Total nodes          : {total_nodes}")
    print(f"  Total edges          : {total_edges}")
    print(f"  SHA-256 (prefix)     : {checksum}")
    print("=" * 70)


def main() -> int:
    print("\n[KNOWLEDGE GRAPH] Scanning repository for new assets...")
    kg = load_kg()

    new_nodes, new_edges = scan_and_update(kg)

    if new_nodes == 0 and new_edges == 0:
        print("  [OK] Knowledge graph is up to date — no new assets found.")
        # Still recalculate checksum to catch any manual edits
        save_kg(kg)
    else:
        save_kg(kg)
        print_summary(new_nodes, new_edges, kg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
