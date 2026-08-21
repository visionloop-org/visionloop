import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-finance"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-telematics"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-legal"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-comms"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-sdk"))

from visionloop_sdk import VisionLoopSDK

def test_unified_sdk():
    vl = VisionLoopSDK()
    
    # 1. Test Finance sub-namespace
    tax = vl.finance.tax.calculate(base_rent=72000.0)
    assert tax.total_invoiced_amount == 84960.0
    
    # 2. Test Legal sub-namespace
    is_valid, state = vl.legal.kyc.validate_gstin("07AAACS1234F1Z5")
    assert is_valid is True
    assert state == "Delhi"
    
    # 3. Test Telematics sub-namespace
    safe, msg = vl.telematics.immobilizer.can_safely_immobilize(speed_kmh=0.0)
    assert safe is True
    
    # 4. Test Comms sub-namespace
    reminder = vl.comms.reminders.generate_message(
        lessee_name="SwiftLogix",
        invoice_number="INV-001",
        amount=84960.0,
        due_date="10th Aug"
    )
    assert "INV-001" in reminder
