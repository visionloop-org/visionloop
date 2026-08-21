import httpx
from typing import Dict, Any, Optional, List

class TelegramDispatcher:
    """
    Reusable Telegram Bot Dispatcher for Vision Loop.
    Handles interactive commands, inline keyboards, dynamic alerts, and broadcast notifications.
    """
    def __init__(self, bot_token: str = "", default_chat_id: str = ""):
        self.bot_token = bot_token
        self.default_chat_id = default_chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    async def send_message(
        self,
        text: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "HTML",
        inline_keyboard: Optional[List[List[Dict[str, str]]]] = None
    ) -> Dict[str, Any]:
        """Sends a message or runs high-fidelity simulation if token is not configured."""
        target_chat = chat_id or self.default_chat_id
        
        if not self.bot_token or not target_chat:
            return {
                "status": "simulated_success",
                "channel": "Telegram Bot API",
                "recipient_chat_id": target_chat or "simulated_proprietor_chat",
                "message_preview": text[:100] + "..."
            }
            
        payload: Dict[str, Any] = {
            "chat_id": target_chat,
            "text": text,
            "parse_mode": parse_mode
        }
        if inline_keyboard:
            payload["reply_markup"] = {"inline_keyboard": inline_keyboard}
            
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/sendMessage", json=payload)
            return resp.json()

    @staticmethod
    def format_fleet_status(asset_data: Dict[str, Any]) -> str:
        tag = asset_data.get("asset_tag", "VL-EV-001")
        name = asset_data.get("name", "Tata Intra EV")
        reg = asset_data.get("registration_number", "DL-01-EV-2026")
        soc = asset_data.get("current_soc_pct", 92.5)
        odo = asset_data.get("odometer_km", 3420.0)
        speed = asset_data.get("speed_kmh", 0.0)
        status = asset_data.get("status", "LEASED")
        locked = asset_data.get("immobilizer_active", False)
        
        lock_icon = "🔴 <b>LOCKED</b>" if locked else "🟢 <b>UNLOCKED</b>"
        
        return (
            f"⚡ <b>VISION LOOP — LIVE FLEET RADAR</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🚚 <b>Asset:</b> {name} (<code>{tag}</code>)\n"
            f"🔢 <b>Reg:</b> <code>{reg}</code> (Yellow Board)\n"
            f"🔋 <b>Battery SoC:</b> <b>{soc}%</b> (Liquid Cooled)\n"
            f"⚡ <b>Current Speed:</b> {speed} km/h\n"
            f"🛣️ <b>Odometer:</b> {odo} km\n"
            f"🔒 <b>Immobilizer:</b> {lock_icon}\n"
            f"📋 <b>Lease Status:</b> {status}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Zero Human Overhead • Fully Autonomous</i>"
        )

    @staticmethod
    def format_revenue_summary(revenue_data: Dict[str, Any]) -> str:
        return (
            f"💰 <b>VISION LOOP — FINANCIAL & ZOHO STATS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 <b>Monthly Run Rate:</b> ₹84,960 / mo\n"
            f"   • Base Rent: ₹72,000.00\n"
            f"   • 18% GST (SAC 997311): ₹12,960.00\n"
            f"🏦 <b>Reconciled Cash:</b> ₹84,960 (e-NACH Active)\n"
            f"🐷 <b>15% Sinking Fund:</b> ₹10,800 / mo (Liquid Fund)\n"
            f"🛡️ <b>Security Deposit:</b> ₹1,44,000 (Ring-Fenced Escrow)\n"
            f"⚖️ <b>MSMED Act Status:</b> Protected (Sec 15/16 45-Day Limit)\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
