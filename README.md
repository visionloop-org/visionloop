# Vision Loop 🚀
### Fully Automated Sole Proprietorship Asset Rental Enterprise

Vision Loop is an AI-driven, fully containerized asset rental enterprise headquartered in India. Starting with commercial electric vehicles (Tata Intra EV), Vision Loop operates with zero human operational friction through automated Zoho Books financial rails, real-time IoT telematics ingestion, autonomous AI agents, and a **24/7 Telegram Mobile Command Bot**.

---

## 🏗️ Tech Stack & Architecture

* **Containerization:** Docker & Docker Compose (8 Microservices)
* **Database & Caching:** MongoDB 7.0 (Unstructured Document Store), Redis 7
* **Backend Core:** FastAPI (Python 3.11), Motor Async Driver, Pydantic v2
* **Accounting & Compliance:** Zoho Books REST API (OAuth 2.0, SAC 997311, 18% GST, e-NACH/UPI QR)
* **Mobile & Messaging:** Telegram Bot API (Mobile Command Center), WhatsApp Cloud API
* **AI Autonomous Engine:** Multi-agent swarm (Financial Sentinel, Telematics Sentinel, Legal Auditor, Executive Briefer)
* **IoT & Telematics:** Ingestion engine for CAN-Bus & GPS streams, battery SoC/SoH, and remote standstill immobilizer
* **Frontend:** Glassmorphic modern React + Vite dashboard

---

## ⚡ Quick Start with Docker

1. **Clone the repository and copy environment variables:**
   ```bash
   cp .env.example .env
   ```

2. **Launch all 8 services via Docker Compose:**
   ```bash
   docker compose up --build
   ```

3. **Access Services:**
   * 🖥️ **Command Center Dashboard:** [http://localhost:3000](http://localhost:3000)
   * 🤖 **Telegram Bot Service:** [http://localhost:8004](http://localhost:8004)
   * 🔌 **Core REST API & Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   * 📊 **Zoho Connector API:** [http://localhost:8001/docs](http://localhost:8001/docs)
   * 🤖 **AI Multi-Agent Service:** [http://localhost:8002/docs](http://localhost:8002/docs)
   * 📡 **Telematics & IoT Ingestor:** [http://localhost:8003/docs](http://localhost:8003/docs)

---

## 📱 Telegram Mobile Bot Commands
* `/start` — Interactive control menu with quick-action buttons
* `/status` — Live fleet radar (SoC %, Speed, Odometer, Location)
* `/revenue` — Monthly run rate (₹84,960/mo) & cash flow stats
* `/treasury` — 15% Sinking Fund reserve & escrow status
* `/aiswarm` — Trigger autonomous AI Swarm cycle
* `/lock` — Engage standstill emergency motor cut-off

---

## 📦 Modular Reusable IP Packages (`packages/`)
* [`visionloop-finance`](file:///d:/VisionLoop/packages/visionloop-finance/): Zoho Books, SAC 997311, Sinking Fund Treasury, MSMED Act 45-day interest.
* [`visionloop-telematics`](file:///d:/VisionLoop/packages/visionloop-telematics/): CAN-Bus stream parser, Battery Warranty SLA Scorer, Standstill immobilizer.
* [`visionloop-legal`](file:///d:/VisionLoop/packages/visionloop-legal/): Dynamic Lease Agreement synthesizer, Indian PAN/GSTIN validator.
* [`visionloop-comms`](file:///d:/VisionLoop/packages/visionloop-comms/): Telegram Bot Dispatcher, WhatsApp Cloud API collection reminders.
* [`visionloop-sdk`](file:///d:/VisionLoop/packages/visionloop-sdk/): Unified master SDK for cross-project integration.
