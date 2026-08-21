# VISION LOOP — DATA VAULT & ASSET INVENTORY
*Centralized Repository of Enterprise Datasets, KYC Documents, Legal Agreements & Canonical Ontologies*

---

## 📂 1. Directory Tree Overview

```
data/
├── README.md                           # This canonical master inventory file
│
├── kyc/                                # Proprietor Identity & Statutory KYC Dossier
│   ├── aadhar.pdf                      # Original UIDAI Aadhaar document (Sapna Jaiswal)
│   ├── sapna_pan.pdf                   # Original Income Tax Dept PAN card (Sapna Jaiswal)
│   ├── aadhar_img_0_Im4.png            # Front-side Aadhaar scan (Sealed in private vault)
│   ├── aadhar_img_0_Im5.png            # QR-coded Aadhaar verification scan
│   ├── pan_img_0_Im6.png               # Income Tax Dept PAN card scan
│   └── proprietor_kyc_dossier.json     # Machine-readable KYC record & metadata
│
├── brand/                              # Official Brand Assets & Design System
│   └── logo.png                        # Official 3D electric-cyan loop logo & icon
│
├── business_model/                     # Master Enterprise Business Architecture
│   └── ENTERPRISE_BUSINESS_MODEL_AND_PROCESS_ARCHITECTURE.md # 3 Verticals, unit economics & lifecycle
│
├── legal/                              # Commercial Contracts & Binding Legal Instruments
│   ├── MASTER_COMMERCIAL_FLEET_LEASE_AGREEMENT.md # 36-Month SAC 997311 lease contract
│   ├── NO_OBJECTION_CERTIFICATE_PREMISES_NOC.md # Lucknow registered office spousal consent NOC
│   ├── TERMS_OF_USE_AND_PUBLIC_LICENSING.md # Multi-tier public license (Apache-2.0, CC BY-SA 4.0)
│   ├── POWER_OF_ATTORNEY_OPERATIONAL_AUTHORIZATION.md # Special operational PoA
│   └── MSME_STATUTORY_PROTECTION_FRAMEWORK.md # Sections 15 & 16 interest clauses
│
├── compliance/                         # Institutional Handbooks & Regulatory Guides
│   ├── INCORPORATION_AND_GST_GUIDE.md  # Sole Proprietorship, Udyam MSME & GST guide
│   ├── GST_REGISTRATION_APPLICATION_DOSSIER.md # 1:1 Form GST REG-01 filing blueprint
│   ├── STRICT_SAFETY_AND_SECURITY_PROTOCOLS.md # 5-Pillar strict enterprise safety & security guardrails
│   ├── BUSINESS_BEST_PRACTICES_MANUAL.md # 15% Sinking Fund & DPDP Act 2023 operating rules
│   ├── OPERATIONAL_AND_DEVELOPMENT_GUIDELINES.md # Master SOP and architectural guidelines
│   ├── PUBLIC_DOMAIN_FINANCIAL_PRIVACY_POLICY.md # Financial privacy rule for public channels
│   ├── YOUTUBE_INDIA_STATUTORY_AND_COMMUNITY_GUIDELINES.md # IT Rules 2021, ASCI & DPDP Act 2023 guide
│   ├── YOUTUBE_MONETIZATION_AND_GST_GUIDE.md # Google AdSense FIRC, LUT & W-8BEN tax guide
│   ├── GOOGLE_ACCOUNT_AND_GCP_SETUP.md # Official Google Account & GCP setup guide
│   ├── GITHUB_AND_PAGES_SETUP.md       # GitHub Account & GitHub.io Pages deployment guide
│   └── EXECUTIVE_BIO_AND_BRAND_STORY.md # Official Executive Bio & Brand Story for Sapna Jaiswal
│
├── services/                           # Commercial Service Suites & Offerings
│   └── GST_FILING_AND_REGISTRATION_CONSULTING_SERVICE.md # Sole Proprietorship GST filing as a service
│
├── media/                              # Commercial Digital Media & YouTube Architecture
│   ├── YOUTUBE_COMMERCIAL_CHANNEL_STRATEGY.md # Content programming & FIRC AdSense monetization
│   ├── YOUTUBE_GST_REGISTRATION_EPISODE_SCRIPT.md # Master 10-min 4K tutorial & 45s Shorts script
│   ├── YOUTUBE_VIDEO_PRODUCTION_PARAMETERS.md # Shorts (9:16) & Long-form (16:9) technical specs
│   └── brand_voice_guidelines.json     # Multilingual voice-over parameters (English & Hindi)
│
├── knowledge_graph/                    # Canonical Ontological Knowledge Graph
│   ├── knowledge_graph.json            # Machine-readable 23-node graph with SHA-256 hash
│   └── KNOWLEDGE_GRAPH.md              # 35 Invariant specifications & Mermaid topology diagrams
│
├── operations/                         # Autonomous Operational Ledgers & Swarm Blueprints
│   ├── AUTONOMOUS_OPERATIONS_LEDGER.md # Chronological event stream with SHA-256 signatures
│   ├── MULTI_AGENT_HIERARCHY_BLUEPRINT.md # 3-Tier agent swarm hierarchy & cross-examination protocol
│   ├── SELF_SUSTAINING_GROWTH_MODEL.md # 5-Year exponential debt-free fleet scaling model
│   └── live_operational_events.json    # Structured machine-readable event ledger
│
├── credentials/                        # Master Credentials & Secrets Vault
│   ├── CREDENTIALS_AND_ACCOUNTS_VAULT.md # Master logins, passwords & recovery records
│   └── ENTERPRISE_CREDENTIALS_VAULT.json # Machine-readable credentials JSON
│
├── seed_data/                          # Database Seed Assets & MongoDB Records
│   ├── init-mongo.js                   # Primary MongoDB 7.0 initialization & index script
│   ├── assets_seed.json                # Seed document for Tata Intra EV (DL-01-EV-2026)
│   └── lessees_seed.json               # Seed document for SwiftLogix Express Delivery
│
└── finance/                            # Statutory Tax, Pricing & Treasury Reserve Models
    └── pricing_and_tax_matrix.json     # SAC 997311 18% GST breakdown & 15% sinking fund model
```

---

## 🗂️ 2. Detailed Data Asset Inventory

### 2.1 Proprietor Identity & KYC (`data/kyc/`)
* **Proprietor:** **Sapna Jaiswal** (D/O Sanjay Jaiswal)
* **Proprietor Status:** **Verified Individual Sole Proprietor** (Income Tax & UIDAI Verified)
* **Privacy & Governance:** **DPDP Act 2023 Compliant** (Raw Identity Assets Sealed in Ring-Fenced Vault)
* **Registered Office & Base Hub:** **Lucknow, Uttar Pradesh, India** (Corridors: Lucknow - Kanpur - Delhi NCR)
* **JSON Metadata:** [`data/kyc/proprietor_kyc_dossier.json`](file:///d:/VisionLoop/data/kyc/proprietor_kyc_dossier.json)

### 2.2 Commercial Legal Contracts (`data/legal/`)
* **Document:** [`data/legal/COMMERCIAL_VEHICLE_LEASE_AGREEMENT.md`](file:///d:/VisionLoop/data/legal/COMMERCIAL_VEHICLE_LEASE_AGREEMENT.md)
* **Lessor:** Vision Loop (Sole Proprietorship, Sapna Jaiswal)
* **Lessee:** SwiftLogix Express Delivery Pvt Ltd (PAN: `AAACS1234F`, GSTIN: `07AAACS1234F1Z5`)
* **Asset:** Tata Intra EV (Yellow Board: `DL-01-EV-2026`, VIN: `MAT612345N2A09876`)
* **Term:** 24 Months @ ₹84,960.00 / month (incl. 18% GST)

### 2.3 Compliance & Best Practices (`data/compliance/`)
* **Incorporation & GST Dossier:** [`data/compliance/INCORPORATION_AND_GST_GUIDE.md`](file:///d:/VisionLoop/data/compliance/INCORPORATION_AND_GST_GUIDE.md)
  * Udyam MSME Registration under **NIC 77101** (Rental/Leasing of Motor Vehicles).
  * 100% Input Tax Credit (ITC) claimable under Section 17(5)(a) of CGST Act.
* **Operating Manual:** [`data/compliance/BUSINESS_BEST_PRACTICES_MANUAL.md`](file:///d:/VisionLoop/data/compliance/BUSINESS_BEST_PRACTICES_MANUAL.md)
  * 15% Sinking Fund liquid treasury allocation.
  * DPDP Act 2023 data fiduciary compliance and customer consent safeguards.

### 2.4 Enterprise Knowledge Graph (`data/knowledge_graph/`)
* **Canonical JSON:** [`data/knowledge_graph/knowledge_graph.json`](file:///d:/VisionLoop/data/knowledge_graph/knowledge_graph.json)
  * 17 Ontological Nodes, 16 Semantic Relationships.
  * SHA-256 Checksum: `d42948761edf4be3e3ca1a05bdc5bb10152e2eb1356cb751ae9b0769ac2b82cd`.
* **Specification:** [`data/knowledge_graph/KNOWLEDGE_GRAPH.md`](file:///d:/VisionLoop/data/knowledge_graph/KNOWLEDGE_GRAPH.md)

### 2.5 Seed Data & MongoDB Schemas (`data/seed_data/`)
* **MongoDB Initialization:** [`data/seed_data/init-mongo.js`](file:///d:/VisionLoop/data/seed_data/init-mongo.js)
* **Assets Collection Seed:** [`data/seed_data/assets_seed.json`](file:///d:/VisionLoop/data/seed_data/assets_seed.json)
* **Lessees Collection Seed:** [`data/seed_data/lessees_seed.json`](file:///d:/VisionLoop/data/seed_data/lessees_seed.json)

### 2.6 Financial & Tax Models (`data/finance/`)
* **Pricing & Tax Matrix:** [`data/finance/pricing_and_tax_matrix.json`](file:///d:/VisionLoop/data/finance/pricing_and_tax_matrix.json)
  $$\begin{aligned}
  \text{Base Rent} &= \mathbf{₹72,000.00 / \text{month}} \\
  \text{18\% GST (SAC 997311)} &= \mathbf{₹12,960.00 / \text{month}} \quad (\text{CGST } ₹6,480 + \text{SGST } ₹6,480) \\
  \text{Gross Total Billed} &= \mathbf{₹84,960.00 / \text{month}} \\
  \text{15\% Sinking Fund} &= \mathbf{₹10,800.00 / \text{month}} \\
  \text{Security Deposit} &= \mathbf{₹1,44,000.00}
  \end{aligned}$$

---

## 🔒 3. Data Governance & Privacy Guardrails

1. **Digital Personal Data Protection (DPDP) Act, 2023 Compliance:**
   * Aadhaar numbers stored in data schemas must remain masked (`XXXX-XXXX-4390`).
   * Original PDF/image assets in `data/kyc/` are restricted to administrative authorization only.
2. **Cryptographic Invariance Guarantee:**
   * All statutory calculations must pass the automated validator (`scripts/verify_data_integrity.py`) with zero deviation.
