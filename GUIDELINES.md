# VISION LOOP — MASTER OPERATIONAL & DEVELOPMENT GUIDELINES
*Comprehensive Enterprise Standard Operating Procedures (SOP), Architectural Principles & Governance Protocols*

---

## 🏛️ 1. Core Enterprise Principles & Statutory Framework

1. **Sole Proprietorship Structure:**
   * Vision Loop operates as a zero-touch Indian Sole Proprietorship, 100% beneficially owned by **Sapna Jaiswal** (PAN: `BGVPJ3356G`, Aadhaar: `XXXX-XXXX-4390`).
   * Primary operational headquarters and fleet base depot: **Lucknow, Uttar Pradesh, India** (UP State Code `09`).
   * Operating Corridors: **Lucknow – Kanpur – Delhi NCR Commercial Freight Corridors**.
2. **Statutory Tax Framework (SAC 997311):**
   * All transport asset leases are invoiced under Service Accounting Code **SAC 997311** (18% GST).
   * **100% Input Tax Credit (ITC)** is claimed on commercial goods vehicle purchases, insurance, and charging infrastructure under **Section 17(5)(a)** of the CGST Act.
3. **Statutory Payment Protection (MSMED Act 2006):**
   * Registered under Micro Enterprise Activity **NIC 77101** (Renting/Leasing of Motor Vehicles).
   * Mandates invoice settlement within **45 days**. Delayed settlements automatically accrue compound interest at **3x the RBI Bank Rate** under Section 16 with monthly rest.
4. **Self-Sustaining Treasury & Zero Debt:**
   * **15% of gross monthly revenue** is automatically swept into High-Yield Liquid Overnight Treasury Funds (~6.8% CAGR).
   * Generates sufficient liquid replacement capital by Month 36 to purchase replacement/expansion assets with **zero debt distress or external loans**.

---

## 🔒 2. Public Domain Financial Privacy & Data Governance

> ### ⚠️ MANDATORY PRIVACY DIRECTIVE:
> **All exact financial contract figures, customer invoice rates, specific monthly revenue run rates, and private cash flow ledgers MUST NEVER be published or displayed in public domains (e.g., Public GitHub Repositories, Public GitHub.io Website, Public Bios, Landing Pages, Marketing Collateral).**

### Rules of Public vs. Private Boundaries:
* ✅ **Public Domains (GitHub README, Website, Public Docs):**
  * Showcase the **structural statutory model** (SAC 997311 18% GST, 100% ITC benefit, 15% Sinking Fund reserve sweep, 2-Month Escrow buffer).
  * Use institutional language: *"Custom Corporate Fleet Lease Plans"*, *"Competitive Institutional Rates"*, *"Automated Zoho Invoicing"*.
* 🔐 **Private Local Vaults (`data/credentials/`, `data/finance/`, `.env`, MongoDB):**
  * Ring-fence exact rupee amounts, accounting ledger balances, customer contract IDs, and bank feed settlements.
  * Always verify that `.gitignore` prevents private credentials and KYC PDFs from being committed.

---

## 🧪 3. Mathematical Invariance & Anti-Corruption Verification

Vision Loop enforces zero tolerance for data corruption or business regression.

1. **29 Mathematical Invariants:**
   * All financial equations ($Base + GST = Total$, $CGST + SGST = GST$, $SinkingFund = 15\% \times Base$, $Deposit = 2 \times Base$) are mathematically tested.
   * Statutory regex checksums for Indian PAN (10 chars, 4th char `P` for Individual, `C` for Company) and GSTIN (15 chars, state code prefix matching location).
   * OEM Battery SLA guardrails (max 70% DC fast charge, 42°C thermal limit) and Standstill Immobilizer safety.
2. **Cryptographic Knowledge Graph Signature:**
   * The canonical Knowledge Graph (`knowledge_graph.json`, 17 Nodes, 16 Edges) is cryptographically signed with a SHA-256 hash (`d42948761edf4be3...`).
   * Any change to graph nodes or relationships requires running `python scripts/verify_data_integrity.py` before committing.
3. **Automated Unit Testing:**
   * Run `python -m pytest tests/` on all builds.
   * All 24 unit tests across legal, finance, telematics, comms, and AI agents must pass 100%.

---

## 🤖 4. Autonomous Operations & Multi-Agent Swarm

Vision Loop operates with zero human operational friction through a containerized **AI Multi-Agent Swarm**:

1. **Financial Sentinel (`services/ai-agent-service`):**
   * Reconciles bank feeds on the 1st of each month.
   * Automatically synthesizes Zoho Books invoices with SAC 997311 tax splits and sends dynamic UPI QR / e-NACH links.
2. **Telematics Sentinel:**
   * Continuously ingests CAN-Bus telemetry streams.
   * Scores battery warranty preservation metrics (SoH %, SoC %, temperature, fast-charge ratio) and schedules 10,000 km periodic servicing.
3. **Legal & Compliance Sentinel:**
   * Audits MSMED Act 45-day payment timelines.
   * Executes multi-tier polite-to-firm payment reminders and legal notices.
4. **Executive Agent:**
   * Synthesizes daily operational briefs and pushes actionable alerts to the **Telegram Mobile Command Bot (`@VisionLoop_Bot`)**.
5. **Verifiable Event Logging:**
   * Every operational tick, sweep, or alert is cryptographically hashed and logged to [`data/operations/live_operational_events.json`](file:///d:/VisionLoop/data/operations/live_operational_events.json) via `visionloop_finance.operations_logger`.

---

## 🛡️ 5. IoT Telematics & Hardware Safety Guardrails

1. **Standstill Immobilization Protocol:**
   * Remote motor cut-off or immobilizer relay engagement is **STRICTLY PROHIBITED** when the vehicle is in motion.
   * The system strictly verifies `speed == 0.0 km/h` before issuing an immobilizer relay lock command.
2. **OEM Battery Warranty SLA Preservation:**
   * DC fast charging ratio must remain capped at **≤ 70%** of total charging volume.
   * Battery operating temperature must not exceed **42.0°C**.
   * Normal operating buffer is maintained between **15% and 90% SoC** to prevent lithium-ion cell degradation.

---

## 📦 6. Code Architecture & Python IP Packages (`packages/`)

All core enterprise capabilities are built as reusable, standalone Python packages:

* [`packages/visionloop-finance/`](file:///d:/VisionLoop/packages/visionloop-finance/): SAC 997311 GST Engine, 15% Sinking Fund Allocator, MSMED Act 3x RBI Interest Calculator, Dynamic UPI QR Generator, Operations Logger.
* [`packages/visionloop-telematics/`](file:///d:/VisionLoop/packages/visionloop-telematics/): CAN-Bus Stream Parser, Tata OEM Battery SLA Scorer, 2dsphere Geofence Engine, Standstill Immobilizer Relay.
* [`packages/visionloop-legal/`](file:///d:/VisionLoop/packages/visionloop-legal/): Dynamic Commercial Lease Synthesizer, Indian PAN/GSTIN Validator, Statutory MSME Compliance Auditor.
* [`packages/visionloop-comms/`](file:///d:/VisionLoop/packages/visionloop-comms/): Telegram Command Bot Engine, WhatsApp Cloud API Dispatcher, Multi-Stage Escalation Collection Engine.
* [`packages/visionloop-sdk/`](file:///d:/VisionLoop/packages/visionloop-sdk/): Unified Master Enterprise SDK.

---

## 🔐 7. Security, Secrets Management & Ring-Fenced Data Vault

1. **Local Secrets Vault:**
   * All API keys, passwords, recovery emails, and personal access tokens (PATs) reside strictly in `.env` and `data/credentials/`.
   * These directories are permanently declared in [`.gitignore`](file:///d:/VisionLoop/.gitignore).
2. **DPDP Act 2023 Compliance:**
   * Personal identifiable information (Aadhaar, PAN, phone numbers) must remain masked in public documentation.
   * Full consent audit trails are preserved in `data/kyc/proprietor_kyc_dossier.json`.

---

## 🚀 8. Git & Deployment Protocols

1. **Dockerized Microservices:**
   * All 8 containers (`dashboard-ui`, `core-api`, `zoho-connector`, `ai-agent-service`, `telematics-ingestor`, `telegram-bot`, `mongo`, `redis`) launch synchronously via `docker compose up --build -d`.
2. **GitHub Pages Global CDN:**
   * The public web platform is automatically published from the `/docs` directory on branch `main` at **`https://visionloop-org.github.io/visionloop/`**.
   * Clean Vanilla CSS glassmorphism, responsive breakpoints, semantic HTML5, and rich aesthetic typography (`Outfit`, `JetBrains Mono`) are mandatory.
