import json
import hashlib
from pathlib import Path

def test_knowledge_graph_structure():
    """
    Knowledge graph structure test — dynamic version.

    The graph grows automatically via the pre-commit auto-discovery hook.
    We assert >= minimum counts (original hand-crafted baseline) and verify
    that all critical core nodes are present. Exact counts are NOT asserted
    because they increase whenever new assets are added to the repository.
    """
    kg_path = Path(__file__).resolve().parent.parent / "knowledge_graph.json"
    assert kg_path.exists(), "knowledge_graph.json must exist"

    with open(kg_path, "r", encoding="utf-8") as f:
        kg = json.load(f)

    assert "nodes" in kg and "edges" in kg, "Graph must have nodes and edges arrays"

    # Dynamic minimum: at least the original 23 hand-crafted nodes and 22 edges
    assert len(kg["nodes"]) >= 23, f"Expected >= 23 nodes, found {len(kg['nodes'])}"
    assert len(kg["edges"]) >= 22, f"Expected >= 22 edges, found {len(kg['edges'])}"

    # All node IDs must be unique
    node_ids = [n["id"] for n in kg["nodes"]]
    assert len(node_ids) == len(set(node_ids)), "Duplicate node IDs detected in knowledge graph"

    # All nodes must have required fields
    for node in kg["nodes"]:
        assert "id" in node,    f"Node missing 'id': {node}"
        assert "type" in node,  f"Node missing 'type': {node.get('id', '?')}"
        assert "label" in node, f"Node missing 'label': {node.get('id', '?')}"

    # Core hand-crafted nodes must always be present
    REQUIRED_CORE_NODES = {
        "ENTITY:VISION_LOOP",
        "PROPRIETOR:SAPNA_JAISWAL",
        "ASSET:VL-EV-001",
        "CONTRACT:VL-LEASE-2026-001",
        "TAX:SAC_997311",
        "TREASURY:SINKING_FUND",
        "AI_SWARM:SENTINELS",
    }
    present_ids = set(node_ids)
    missing = REQUIRED_CORE_NODES - present_ids
    assert not missing, f"Required core nodes missing from graph: {missing}"

    # Schema metadata fields must be present
    assert "schema_version" in kg, "Missing schema_version"
    assert "sha256_checksum" in kg, "Missing sha256_checksum"
    assert "integrity_status" in kg, "Missing integrity_status"


def test_knowledge_graph_financial_identities():
    kg_path = Path(__file__).resolve().parent.parent / "knowledge_graph.json"
    with open(kg_path, "r", encoding="utf-8") as f:
        kg = json.load(f)
        
    nodes = {n["id"]: n for n in kg["nodes"]}
    contract = nodes["CONTRACT:VL-LEASE-2026-001"]["properties"]
    tax = nodes["TAX:SAC_997311"]["properties"]
    treasury = nodes["TREASURY:SINKING_FUND"]["properties"]
    
    base = contract["monthly_base_rent_inr"]
    gst = contract["monthly_gst_inr"]
    total = contract["total_monthly_invoiced_inr"]
    
    assert base == 72000.00
    assert gst == 12960.00
    assert total == 84960.00
    assert round(base + gst, 2) == total
    
    assert tax["cgst_amount_inr"] == 6480.00
    assert tax["sgst_amount_inr"] == 6480.00
    assert tax["cgst_amount_inr"] + tax["sgst_amount_inr"] == gst
    
    assert treasury["monthly_inflow_inr"] == round(base * 0.15, 2)
    assert treasury["monthly_inflow_inr"] == 10800.00

def test_knowledge_graph_edge_referential_integrity():
    kg_path = Path(__file__).resolve().parent.parent / "knowledge_graph.json"
    with open(kg_path, "r", encoding="utf-8") as f:
        kg = json.load(f)
        
    node_ids = {n["id"] for n in kg["nodes"]}
    for edge in kg["edges"]:
        assert edge["source"] in node_ids, f"Missing source node: {edge['source']}"
        assert edge["target"] in node_ids, f"Missing target node: {edge['target']}"
