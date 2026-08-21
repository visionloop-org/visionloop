import json
import hashlib
from pathlib import Path

def test_knowledge_graph_structure():
    kg_path = Path(__file__).resolve().parent.parent / "knowledge_graph.json"
    assert kg_path.exists(), "knowledge_graph.json must exist"
    
    with open(kg_path, "r", encoding="utf-8") as f:
        kg = json.load(f)
        
    assert "nodes" in kg and "edges" in kg
    assert len(kg["nodes"]) == 23
    assert len(kg["edges"]) == 22

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
