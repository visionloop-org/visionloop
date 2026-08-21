import pytest
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-comms"))

from visionloop_comms import (
    CollectionReminderEngine, 
    WhatsAppDispatcher,
    TelegramDispatcher
)

def test_collection_reminder_engine():
    msg = CollectionReminderEngine.generate_message(
        lessee_name="SwiftLogix Express Delivery",
        invoice_number="VL-INV-2026-001",
        amount=84960.0,
        due_date="05 Aug, 2026",
        stage="DUE_DATE",
        upi_link="upi://pay?pa=visionloop@icici&am=84960.00"
    )
    assert "Namaste SwiftLogix Express Delivery" in msg
    assert "₹84,960.00" in msg
    assert "VL-INV-2026-001" in msg
    assert "upi://pay?" in msg

@pytest.mark.asyncio
async def test_telegram_dispatcher():
    tg = TelegramDispatcher()
    res = await tg.send_message(text="Test Alert")
    assert res["status"] == "simulated_success"
    assert res["channel"] == "Telegram Bot API"

    fleet_str = TelegramDispatcher.format_fleet_status({
        "name": "Tata Intra EV",
        "asset_tag": "VL-EV-001",
        "registration_number": "DL-01-EV-2026",
        "current_soc_pct": 92.5
    })
    assert "VISION LOOP — LIVE FLEET RADAR" in fleet_str
    assert "Tata Intra EV" in fleet_str

@pytest.mark.asyncio
async def test_whatsapp_dispatcher():
    wa = WhatsAppDispatcher()
    res = await wa.send_text_message(to_phone="+919876543210", text_body="Hello from Vision Loop")
    assert res["status"] == "simulated_success"
    assert res["recipient"] == "+919876543210"
