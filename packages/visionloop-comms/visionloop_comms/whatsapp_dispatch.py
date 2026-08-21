import httpx
from typing import Dict, Any, Optional

class WhatsAppDispatcher:
    """Dispatches templated messages via Meta WhatsApp Business Cloud API."""
    
    def __init__(self, phone_number_id: str = "", access_token: str = ""):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    async def send_text_message(self, to_phone: str, text_body: str) -> Dict[str, Any]:
        """Dispatches or simulates WhatsApp message transmission."""
        if not self.access_token or not self.phone_number_id:
            # High-fidelity simulation mode
            return {
                "status": "simulated_success",
                "recipient": to_phone,
                "message_preview": text_body[:80] + "...",
                "channel": "WhatsApp Cloud API"
            }
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": text_body}
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.api_url, headers=headers, json=payload)
            return resp.json()
