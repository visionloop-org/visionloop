import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from app.config import settings
from app.bot import (
    start_command, status_command, revenue_command, treasury_command, 
    aiswarm_command, callback_router, handle_natural_language_ai_prompt
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vision Loop — Telegram Bot & Antigravity AI Command Service",
    description="Bidirectional mobile command center, natural language prompt execution & IoT immobilizer control.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BroadcastMessage(BaseModel):
    message: str
    chat_id: Optional[str] = None
    parse_mode: str = "HTML"

telegram_app: Optional[Application] = None
polling_task: Optional[asyncio.Task] = None

@app.on_event("startup")
async def startup_telegram():
    global telegram_app, polling_task
    token = settings.TELEGRAM_BOT_TOKEN
    
    if token and not token.startswith("dummy") and not token.startswith("your_"):
        try:
            logger.info("Initializing Telegram Bot Application with Antigravity AI Bridge...")
            telegram_app = Application.builder().token(token).build()
            
            # Register Command Handlers
            telegram_app.add_handler(CommandHandler("start", start_command))
            telegram_app.add_handler(CommandHandler("status", status_command))
            telegram_app.add_handler(CommandHandler("revenue", revenue_command))
            telegram_app.add_handler(CommandHandler("treasury", treasury_command))
            telegram_app.add_handler(CommandHandler("aiswarm", aiswarm_command))
            telegram_app.add_handler(CallbackQueryHandler(callback_router))
            
            # Register Natural Language AI Message Handler
            telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_natural_language_ai_prompt))
            
            await telegram_app.initialize()
            await telegram_app.start()
            
            # Start polling in background
            polling_task = asyncio.create_task(telegram_app.updater.start_polling())
            logger.info("Telegram Bot Polling & Antigravity AI Bridge started successfully.")
        except Exception as e:
            logger.warning(f"Telegram Bot failed to start (running in simulation mode): {e}")
    else:
        logger.info("No live TELEGRAM_BOT_TOKEN found. Telegram service running in simulation / API dispatch mode.")

@app.on_event("shutdown")
async def shutdown_telegram():
    global telegram_app, polling_task
    if telegram_app and telegram_app.updater:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()

@app.get("/")
def health_check():
    return {
        "service": "Vision Loop Telegram Bot & Antigravity AI Bridge",
        "status": "online",
        "bot_configured": bool(settings.TELEGRAM_BOT_TOKEN and not settings.TELEGRAM_BOT_TOKEN.startswith("your_")),
        "admin_chat_configured": bool(settings.TELEGRAM_ADMIN_CHAT_ID),
        "ai_agent_bridge": "active"
    }

@app.post("/broadcast")
async def broadcast_alert(payload: BroadcastMessage):
    """Broadcasts a high-priority alert to the proprietor via Telegram."""
    chat_id = payload.chat_id or settings.TELEGRAM_ADMIN_CHAT_ID
    
    if telegram_app and chat_id:
        try:
            await telegram_app.bot.send_message(
                chat_id=chat_id,
                text=payload.message,
                parse_mode=payload.parse_mode
            )
            return {"status": "dispatched", "chat_id": chat_id}
        except Exception as e:
            logger.error(f"Failed to dispatch Telegram message: {e}")
            
    # Simulation response if live token is not set
    return {
        "status": "simulated_success",
        "recipient": chat_id or "simulated_admin_chat",
        "message_preview": payload.message[:100] + "..."
    }
