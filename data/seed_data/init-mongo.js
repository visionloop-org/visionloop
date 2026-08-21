// Vision Loop — MongoDB Initialization Script
// Configures collections, indexes, and bootstrap documents

db = db.getSiblingDB('visionloop_db');

// 1. Create collections with indexes
db.createCollection('assets');
db.assets.createIndex({ asset_tag: 1 }, { unique: true });
db.assets.createIndex({ vin: 1 }, { unique: true, sparse: true });
db.assets.createIndex({ registration_number: 1 }, { unique: true, sparse: true });

db.createCollection('lessees');
db.lessees.createIndex({ pan: 1 }, { unique: true });
db.lessees.createIndex({ email: 1 });

db.createCollection('leases');
db.leases.createIndex({ lease_number: 1 }, { unique: true });
db.leases.createIndex({ asset_tag: 1 });
db.leases.createIndex({ status: 1 });

db.createCollection('invoices');
db.invoices.createIndex({ invoice_number: 1 }, { unique: true });
db.invoices.createIndex({ zoho_invoice_id: 1 }, { unique: true, sparse: true });
db.invoices.createIndex({ status: 1 });
db.invoices.createIndex({ invoice_date: -1 });

db.createCollection('telemetry_records');
db.telemetry_records.createIndex({ asset_tag: 1, timestamp: -1 });
db.telemetry_records.createIndex({ location: "2dsphere" });

db.createCollection('agent_action_logs');
db.agent_action_logs.createIndex({ agent_name: 1, created_at: -1 });
db.agent_action_logs.createIndex({ severity: 1 });

// 2. Seed Initial Documents

// Asset #1: Tata Intra EV Commercial Goods Carriage
db.assets.updateOne(
  { asset_tag: 'VL-EV-001' },
  {
    $setOnInsert: {
      asset_tag: 'VL-EV-001',
      name: 'Tata Intra EV Commercial Goods Carriage',
      asset_type: 'COMMERCIAL_EV',
      vin: 'MAT612345N2A09876',
      registration_number: 'DL-01-EV-2026',
      specifications: {
        battery_capacity_kwh: 26.0,
        motor_type: 'Permanent Magnet Synchronous Motor',
        payload_capacity_kg: 1000,
        range_certified_km: 140,
        charging_standard: 'CCS-2 / Type-2 Fast Charging'
      },
      current_state: {
        soc_pct: 92.5,
        soh_pct: 99.4,
        battery_temp_c: 29.2,
        battery_voltage: 384.2,
        odometer_km: 3420.0,
        speed_kmh: 24.5,
        location: {
          type: "Point",
          coordinates: [77.2090, 28.6139] // [lng, lat]
        },
        address_hint: "Connaught Place Commercial Ring, New Delhi",
        immobilizer_active: false,
        status: "LEASED",
        last_serviced_km: 0.0,
        next_service_due_km: 10000.0
      },
      financial_profile: {
        monthly_rental_base: 72000.00,
        sac_code: '997311',
        gst_rate_pct: 18.00,
        monthly_gst_amount: 12960.00,
        total_monthly_invoiced: 84960.00,
        itc_eligibility: '100% Full Input Tax Credit Claimable (Sec 17(5)(a))'
      },
      created_at: new Date(),
      updated_at: new Date()
    }
  },
  { upsert: true }
);

// Lessee: SwiftLogix Express Delivery Pvt Ltd
db.lessees.updateOne(
  { pan: 'AAACS1234F' },
  {
    $setOnInsert: {
      company_name: 'SwiftLogix Express Delivery Pvt Ltd',
      signatory_name: 'Rajesh Sharma (Director)',
      email: 'accounts@swiftlogix.in',
      phone: '+919876543210',
      pan: 'AAACS1234F',
      gstin: '07AAACS1234F1Z5',
      billing_address: 'Plot 42, Okhla Industrial Area Phase-III, New Delhi, Delhi - 110020',
      zoho_customer_id: 'ZB-CUST-883921',
      kyc: {
        verified: true,
        aadhaar_signatory_hash: 'SHA256_eSign_Verified_Rajesh_Sharma',
        pan_verified: true,
        gstin_status: 'ACTIVE'
      },
      security_deposit: {
        amount: 144000.00,
        status: 'HELD_IN_ESCROW',
        reference: 'FD-ICICI-2026-9912'
      },
      created_at: new Date()
    }
  },
  { upsert: true }
);

// Active Commercial Lease Document
db.leases.updateOne(
  { lease_number: 'VL-LEASE-2026-001' },
  {
    $setOnInsert: {
      lease_number: 'VL-LEASE-2026-001',
      asset_tag: 'VL-EV-001',
      lessee_pan: 'AAACS1234F',
      lessee_name: 'SwiftLogix Express Delivery Pvt Ltd',
      start_date: new Date('2026-08-01'),
      end_date: new Date('2028-07-31'),
      financials: {
        base_rent_monthly: 72000.00,
        sac_code: '997311',
        gst_rate_pct: 18.00,
        gst_amount_monthly: 12960.00,
        total_monthly_rent: 84960.00,
        billing_day_of_month: 1,
        payment_due_days: 5
      },
      contract_status: {
        status: 'ACTIVE',
        e_signed: true,
        contract_url: 'https://sign.visionloop.in/docs/VL-LEASE-2026-001.pdf',
        signed_at: new Date('2026-08-01T09:30:00Z')
      },
      created_at: new Date()
    }
  },
  { upsert: true }
);

// Invoices
db.invoices.updateOne(
  { invoice_number: 'VL-INV-2026-08-001' },
  {
    $setOnInsert: {
      invoice_number: 'VL-INV-2026-08-001',
      zoho_invoice_id: 'ZB-INV-99201',
      lease_number: 'VL-LEASE-2026-001',
      asset_tag: 'VL-EV-001',
      lessee_pan: 'AAACS1234F',
      lessee_name: 'SwiftLogix Express Delivery Pvt Ltd',
      invoice_date: new Date('2026-08-01'),
      due_date: new Date('2026-08-05'),
      sac_code: '997311',
      line_items: [
        {
          description: 'Commercial EV Dry Lease (without operator) - Tata Intra EV (DL-01-EV-2026)',
          sac_code: '997311',
          base_amount: 72000.00,
          cgst_rate: 9.0,
          cgst_amount: 6480.00,
          sgst_rate: 9.0,
          sgst_amount: 6480.00,
          igst_rate: 0.0,
          igst_amount: 0.0,
          total_amount: 84960.00
        }
      ],
      tax_summary: {
        taxable_value: 72000.00,
        cgst: 6480.00,
        sgst: 6480.00,
        igst: 0.00,
        total_tax: 12960.00,
        total_payable: 84960.00
      },
      settlement: {
        status: 'PAID',
        payment_method: 'e-NACH Auto-Debit',
        payment_reference: 'NACH-ICICI-20260805-9981',
        paid_at: new Date('2026-08-05T10:30:00Z'),
        receipt_url: 'https://books.zoho.in/secure/receipts/ZB-INV-99201.pdf'
      },
      created_at: new Date()
    }
  },
  { upsert: true }
);

// Initial Telemetry Record
db.telemetry_records.insertOne({
  asset_tag: 'VL-EV-001',
  timestamp: new Date(),
  location: {
    type: "Point",
    coordinates: [77.2090, 28.6139]
  },
  speed_kmh: 24.5,
  soc_pct: 92.5,
  battery_temp_c: 29.2,
  battery_voltage: 384.2,
  odometer_km: 3420.0,
  ignition_on: true,
  charging_status: 'DISCHARGING',
  cell_data: {
    max_cell_v: 3.85,
    min_cell_v: 3.84,
    cell_delta_v: 0.01
  }
});

// Seed AI Action Logs
db.agent_action_logs.insertMany([
  {
    agent_name: 'LEGAL_SENTINEL',
    asset_tag: 'VL-EV-001',
    action_type: 'CONTRACT_E_SIGNED',
    severity: 'INFO',
    summary: 'Commercial Lease Agreement for Tata Intra EV (DL-01-EV-2026) verified via Aadhaar OTP e-Sign by Rajesh Sharma (SwiftLogix).',
    details: { lease_number: 'VL-LEASE-2026-001', sac_code: '997311' },
    created_at: new Date()
  },
  {
    agent_name: 'FINANCIAL_SENTINEL',
    asset_tag: 'VL-EV-001',
    action_type: 'PAYMENT_RECONCILED',
    severity: 'INFO',
    summary: 'e-NACH auto-cleared: ₹84,960 (₹72,000 + 18% GST) received for Invoice VL-INV-2026-08-001. Zoho Books ledger updated.',
    details: { ref: 'NACH-ICICI-20260805-9981', amount: 84960.0 },
    created_at: new Date()
  },
  {
    agent_name: 'TELEMATICS_SENTINEL',
    asset_tag: 'VL-EV-001',
    action_type: 'TELEMETRY_NOMINAL',
    severity: 'INFO',
    summary: 'CAN-Bus scan nominal: Battery SoH 99.4%, Cell delta 0.01V, Operating temperature 29.2°C.',
    details: { soc: 92.5, odometer: 3420.0 },
    created_at: new Date()
  }
]);

print("Vision Loop MongoDB database initialized successfully with unstructured schema!");
