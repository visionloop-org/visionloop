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
│   ├── aadhar_img_0_Im4.png            # Front-side Aadhaar scan (Patna registered address)
│   ├── aadhar_img_1_Im5.png            # Back-side Aadhaar scan (Photo & UID)
│   └── proprietor_kyc_dossier.json     # Machine-readable validated KYC parameters
│
├── brand/                              # Official Brand Assets & Design System
│   └── logo.png                        # Official 3D electric-cyan loop logo & icon
│
├── legal/                              # Commercial Contracts & Counterparty Agreements
│   └── COMMERCIAL_VEHICLE_LEASE_AGREEMENT.md  # Master Commercial Lease Agreement (24 Mo)
│
├── compliance/                         # Institutional Handbooks & Regulatory Guides
│   ├── INCORPORATION_AND_GST_GUIDE.md  # Sole Proprietorship, Udyam MSME & GST guide
│   ├── BUSINESS_BEST_PRACTICES_MANUAL.md # 15% Sinking Fund & DPDP Act 2023 operating rules
│   ├── GOOGLE_ACCOUNT_AND_GCP_SETUP.md # Official Google Account & GCP setup guide
│   ├── GITHUB_AND_PAGES_SETUP.md       # GitHub Account & GitHub.io Pages deployment guide
│   └── EXECUTIVE_BIO_AND_BRAND_STORY.md # Official Executive Bio & Brand Story for Sapna Jaiswal
│
├── knowledge_graph/                    # Canonical Ontological Knowledge Graph
│   ├── knowledge_graph.json            # Machine-readable 13-node graph with SHA-256 hash
│   └── KNOWLEDGE_GRAPH.md              # Mathematical invariant specifications & Mermaid diagrams
│
├── operations/                         # Autonomous Operational Journals & Growth Models
│   ├── AUTONOMOUS_OPERATIONS_LEDGER.md # Canonical chronological operations log
│   ├── SELF_SUSTAINING_GROWTH_MODEL.md # 5-Year exponential debt-free scale model
│   └── live_operational_events.json    # Machine-readable SHA-256 event stream
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
* **PAN Number:** `BGVPJ3356G` (Individual 4th Char `P`)
* **Aadhaar Number:** `9847 1618 4390` (Masked: `XXXX-XXXX-4390`)
* **Registered Address:** `72/75 A, Kaliasthan, Near Police Station, Dinapur-Cum-Khagaul, Patna, Bihar - 801503`
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
  * 13 Ontological Nodes, 12 Semantic Relationships.
  * SHA-256 Checksum: `5e4ed39a70bc860b70c53b81df4bbdd14cceccd3de4c1af3c1d6611e52075937`.
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
