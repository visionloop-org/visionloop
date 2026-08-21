"""
VisionLoop Comms Module
Reusable AI Messaging, WhatsApp & Telegram Bot Automation Engine
"""

from .reminder_templates import CollectionReminderEngine
from .whatsapp_dispatch import WhatsAppDispatcher
from .telegram_dispatch import TelegramDispatcher

__all__ = [
    "CollectionReminderEngine",
    "WhatsAppDispatcher",
    "TelegramDispatcher"
]
