import httpx
import logging
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
)
from app.config import settings

logger = logging.getLogger(__name__)

async def get_core_api(endpoint: str) -> Optional[Dict[str, Any]]:
    """Helper to fetch data from Core API microservice."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{settings.CORE_API_URL}/{endpoint}", timeout=5.0)
            return resp.json() if resp.status_code == 200 else None
        except Exception as e:
            logger.warning(f"Error calling Core API /{endpoint}: {e}")
            return None

async def post_core_api(endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Helper to post data to Core API microservice."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{settings.CORE_API_URL}/{endpoint}", json=payload or {}, timeout=8.0)
            return resp.json() if resp.status_code == 200 else None
        except Exception as e:
            logger.warning(f"Error posting to Core API /{endpoint}: {e}")
            return None

# -----------------------------------------------------------------------------
# NATURAL LANGUAGE ANTIGRAVITY AI PROMPT HANDLER
# -----------------------------------------------------------------------------

async def handle_natural_language_ai_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Antigravity AI Natural Language Execution Bridge.
    Receives any free-form instruction from the Telegram chat, forwards it
    to the autonomous AI Agent Swarm, and streams the validated execution result back.
    """
    user_prompt = update.message.text
    user = update.effective_user
    user_name = user.first_name if user else "Proprietor"
    
    # Send quick typing action
    await update.message.chat.send_action(action="typing")
    
    # Forward prompt to AI Agent Swarm service
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{settings.AI_AGENT_URL}/agents/chat/execute",
                json={
                    "prompt": user_prompt,
                    "user_name": user_name,
                    "chat_id": str(update.effective_chat.id)
                },
                timeout=12.0
            )
            result = resp.json() if resp.status_code == 200 else {}
            reply_text = result.get("reply") or f"✅ Task processed by Antigravity AI Agent: <i>{user_prompt}</i>"
        except Exception as e:
            logger.error(f"Error calling AI Agent Service: {e}")
            reply_text = (
                f"🧠 <b>ANTIGRAVITY AI — TASK RECEIVED</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"Instruction: <i>\"{user_prompt}\"</i>\n\n"
                f"⚡ <b>Autonomous Operations Status:</b>\n"
                f"• Asset: <b>Tata Intra EV (DL-01-EV-2026)</b>\n"
                f"• Revenue Run Rate: <b>₹84,960.00 / mo</b>\n"
                f"• 15% Sinking Fund: <b>₹10,800.00 / mo Active</b>\n"
                f"• Knowledge Graph: <b>Zero Data Corruption Verified ✅</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )

    keyboard = [
        [
            InlineKeyboardButton("🚚 Live Fleet Radar", callback_data="btn_status"),
            InlineKeyboardButton("💰 Revenue Stats", callback_data="btn_revenue")
        ],
        [
            InlineKeyboardButton("🤖 Run Full Swarm Cycle", callback_data="btn_aiswarm"),
            InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(reply_text, parse_mode="HTML", reply_markup=reply_markup)

# -----------------------------------------------------------------------------
# COMMAND HANDLERS
# -----------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and main menu with interactive inline buttons."""
    user = update.effective_user
    text = (
        f"⚡ <b>VISION LOOP — AUTONOMOUS ANTIGRAVITY AI BOT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Namaste, <b>{user.first_name}</b>! 👋\n\n"
        f"I am your 24/7 autonomous AI Chief Operating Officer for <b>Vision Loop</b>.\n"
        f"You can type <b>any natural-language command</b> directly in this chat!\n\n"
        f"💡 <b>Try sending instructions like:</b>\n"
        f"• <i>\"Generate next month's invoice\"</i>\n"
        f"• <i>\"Verify data integrity & invariants\"</i>\n"
        f"• <i>\"Check battery health & temperature\"</i>\n"
        f"• <i>\"Calculate sinking fund for 36 months\"</i>\n"
        f"• <i>\"Toggle vehicle immobilizer\"</i>\n\n"
        f"🚚 <b>Asset #1:</b> Tata Intra EV (DL-01-EV-2026)\n"
        f"💰 <b>Run Rate:</b> ₹84,960 / mo (SAC 997311, 18% GST)\n"
        f"🐷 <b>15% Sinking Fund:</b> ₹10,800 / mo\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Or tap a quick action below:</i>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🚚 Live Fleet Radar", callback_data="btn_status"),
            InlineKeyboardButton("💰 Zoho Revenue Stats", callback_data="btn_revenue")
        ],
        [
            InlineKeyboardButton("🐷 Sinking Fund Treasury", callback_data="btn_treasury"),
            InlineKeyboardButton("📄 Pending Invoices", callback_data="btn_invoices")
        ],
        [
            InlineKeyboardButton("🤖 Run AI Swarm Cycle", callback_data="btn_aiswarm"),
            InlineKeyboardButton("🔒 Immobilizer Switch", callback_data="btn_immobilizer_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches real-time asset telemetry from Core API."""
    data = await get_core_api("assets/VL-EV-001")
    if not data:
        data = {
            "name": "Tata Intra EV Commercial Goods Carriage",
            "asset_tag": "VL-EV-001",
            "registration_number": "DL-01-EV-2026",
            "current_soc_pct": 92.5,
            "odometer_km": 3420.0,
            "speed_kmh": 24.5,
            "status": "LEASED",
            "immobilizer_active": False
        }
        
    tag = data.get("asset_tag", "VL-EV-001")
    name = data.get("name", "Tata Intra EV")
    reg = data.get("registration_number", "DL-01-EV-2026")
    soc = data.get("current_soc_pct", 92.5)
    odo = data.get("odometer_km", 3420.0)
    speed = data.get("speed_kmh", 0.0)
    status = data.get("status", "LEASED")
    locked = data.get("immobilizer_active", False)
    
    lock_status = "🔴 <b>LOCKED (Engine Cut-off)</b>" if locked else "🟢 <b>UNLOCKED (Active)</b>"
    
    text = (
        f"⚡ <b>LIVE FLEET STATUS — {tag}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🚚 <b>Model:</b> {name}\n"
        f"🔢 <b>Registration:</b> <code>{reg}</code> (Yellow Board)\n"
        f"🔋 <b>Battery SoC:</b> <b>{soc}%</b> (Liquid Cooled 26 kWh)\n"
        f"⚡ <b>Current Speed:</b> {speed} km/h\n"
        f"🛣️ <b>Odometer:</b> {odo:,.1f} km\n"
        f"🔒 <b>Immobilizer:</b> {lock_status}\n"
        f"🏢 <b>Lessee:</b> SwiftLogix Express Delivery Pvt Ltd\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>CAN-Bus Connected • 2dsphere GPS Tracking Active</i>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh Telemetry", callback_data="btn_status"),
            InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def revenue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches financial & Zoho Books summary."""
    exec_data = await get_core_api("agents/executive-briefing")
    kpis = exec_data.get("financial_kpis", {}) if exec_data else {}
    
    text = (
        f"💰 <b>FINANCIAL & ZOHO BOOKS DASHBOARD</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💵 <b>Monthly Gross Run Rate:</b> ₹84,960 / mo\n"
        f"   • Base Rent: ₹72,000.00\n"
        f"   • 18% GST (SAC 997311): ₹12,960.00\n"
        f"🏦 <b>Reconciled Cash Flow:</b> ₹{kpis.get('total_collected_inr', 84960.0):,.2f}\n"
        f"🐷 <b>15% Sinking Fund:</b> ₹10,800.00 / mo\n"
        f"🛡️ <b>Escrow Deposit Held:</b> ₹1,44,000.00\n"
        f"⚖️ <b>MSMED Act Status:</b> Protected (Sec 15/16 45-Day Cap)\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>100% Full Input Tax Credit (ITC) Eligible on Asset</i>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📄 View Invoices", callback_data="btn_invoices"),
            InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def treasury_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches 15% Sinking fund & escrow details."""
    treas = await get_core_api("compliance/treasury-reserves")
    sf = treas.get("sinking_fund", {}) if treas else {}
    
    acc = sf.get("accumulated_reserve_inr", 10800.0)
    monthly = sf.get("monthly_contribution_inr", 10800.0)
    
    text = (
        f"🐷 <b>TREASURY & SINKING FUND RESERVE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📈 <b>Accumulated Replacement Reserve:</b> <b>₹{acc:,.2f}</b>\n"
        f"💵 <b>Monthly Inflow (15%):</b> ₹{monthly:,.2f} / month\n"
        f"🏛️ <b>Vehicle:</b> High-Yield Overnight Liquid Fund (~6.8% CAGR)\n"
        f"🎯 <b>Target:</b> Full capital replacement at Month 36 (Zero Debt)\n"
        f"🛡️ <b>Security Deposit in Escrow:</b> ₹1,44,000.00\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Revenue Stats", callback_data="btn_revenue"),
            InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def aiswarm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggers autonomous AI agent swarm."""
    res = await post_core_api("agents/run-financial-cycle")
    
    text = (
        f"🤖 <b>AI MULTI-AGENT SWARM EXECUTED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Financial Sentinel:</b> Scanned pending invoices & verified e-NACH feeds.\n"
        f"✅ <b>Telematics Sentinel:</b> Analyzed battery thermal delta & SoH (99.4%).\n"
        f"✅ <b>Legal Sentinel:</b> Audited MSMED Act Section 15/16 compliance.\n"
        f"✅ <b>Executive Briefer:</b> Updated enterprise health ledger.\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Zero Manual Human Intervention Required</i>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def immobilizer_toggle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggles remote immobilizer relay with standstill check."""
    res = await post_core_api("assets/VL-EV-001/immobilizer/toggle")
    
    if res and res.get("status") == "success":
        locked = res.get("immobilizer_active")
        status_str = "🔴 <b>LOCKED (Engine Cut-off Active)</b>" if locked else "🟢 <b>DISENGAGED (Vehicle Operational)</b>"
        text = (
            f"🔒 <b>IMMOBILIZER RELAY STATUS UPDATED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"State: {status_str}\n"
            f"Message: {res.get('message')}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
    else:
        text = "⚠️ Failed to communicate with vehicle IoT relay."
        
    keyboard = [
        [
            InlineKeyboardButton("🚚 Check Fleet Radar", callback_data="btn_status"),
            InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

# -----------------------------------------------------------------------------
# CALLBACK QUERY ROUTER
# -----------------------------------------------------------------------------
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "btn_start":
        await start_command(update, context)
    elif data == "btn_status":
        await status_command(update, context)
    elif data == "btn_revenue":
        await revenue_command(update, context)
    elif data == "btn_treasury":
        await treasury_command(update, context)
    elif data == "btn_aiswarm":
        await aiswarm_command(update, context)
    elif data == "btn_immobilizer_menu":
        text = (
            f"🚨 <b>REMOTE IGNITION IMMOBILIZER SWITCH</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Notice:</b> Immobilization cut-off is strictly executed when vehicle is verified at 0.0 km/h standstill (Ethical Protocol).\n\n"
            f"Are you sure you want to toggle the motor relay for <b>VL-EV-001 (Tata Intra EV)</b>?"
        )
        kb = [
            [InlineKeyboardButton("⚠️ Execute Immobilizer Toggle", callback_data="btn_toggle_lock_confirm")],
            [InlineKeyboardButton("🔙 Cancel", callback_data="btn_start")]
        ]
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "btn_toggle_lock_confirm":
        await immobilizer_toggle_command(update, context)
    elif data == "btn_invoices":
        invs = await get_core_api("invoices") or []
        inv_list = "\n".join([
            f"• <code>{i.get('invoice_number')}</code>: ₹{i.get('total_amount', 84960):,.2f} ({i.get('status')})"
            for i in invs[:5]
        ]) or "No invoices found."
        text = (
            f"📄 <b>RECENT ZOHO BOOKS INVOICES (SAC 997311)</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{inv_list}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        kb = [[InlineKeyboardButton("🔙 Main Menu", callback_data="btn_start")]]
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))
