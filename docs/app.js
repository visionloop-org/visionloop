// -----------------------------------------------------------------------------
// Vision Loop — GitHub Pages Interactive Script
// -----------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  console.log('Vision Loop GitHub Pages initialized.');

  // Live Telemetry Simulation
  let soc = 92.5;
  let odo = 3420.0;
  let speed = 24.5;
  let isMoving = true;

  const socValEl = document.getElementById('hero-soc-val');
  const socBarEl = document.getElementById('hero-soc-bar');
  const odoValEl = document.getElementById('hero-odo-val');
  const speedValEl = document.getElementById('hero-speed-val');
  const statusEl = document.getElementById('hero-live-status');

  setInterval(() => {
    // Subtle realistic variations
    if (isMoving) {
      speed = Math.max(0, Math.min(48, speed + (Math.random() * 6 - 3)));
      odo += (speed / 3600) * 2; // small increment
      soc = Math.max(15, soc - 0.01);
      
      // Random red light stop
      if (Math.random() < 0.1) {
        isMoving = false;
        speed = 0.0;
      }
    } else {
      speed = 0.0;
      if (Math.random() < 0.3) {
        isMoving = true;
        speed = 18.0;
      }
    }

    if (socValEl) socValEl.textContent = `${soc.toFixed(1)}%`;
    if (socBarEl) socBarEl.style.width = `${soc.toFixed(1)}%`;
    if (odoValEl) odoValEl.textContent = `${odo.toLocaleString('en-IN', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} km`;
    if (speedValEl) speedValEl.textContent = `${speed.toFixed(1)} km/h`;
    if (statusEl) {
      if (speed === 0) {
        statusEl.textContent = "CAN-BUS (STANDSTILL)";
        statusEl.className = "badge badge-cyan";
      } else {
        statusEl.textContent = "CAN-BUS (IN TRANSIT)";
        statusEl.className = "badge badge-emerald";
      }
    }
  }, 2000);

  // -----------------------------------------------------------------------------
  // Inter-Agent Cross-Examination Dialogue Simulator
  // -----------------------------------------------------------------------------
  const termEl = document.getElementById('dialogue-terminal');
  const btnTreasury = document.getElementById('btn-dialogue-treasury');
  const btnFleet = document.getElementById('btn-dialogue-fleet');
  const btnLegal = document.getElementById('btn-dialogue-legal');

  const dialogues = {
    treasury: [
      { sender: "👑 GARUDA EXECUTIVE", type: "TASK_DELEGATION", text: "Delegate Task: Invoicing under SAC 997311 and 15% Sinking Fund allocation." },
      { sender: "💰 KUBER TREASURY", type: "WORK_PROPOSAL", text: "Proposal: Base ₹72k + 18% GST (CGST ₹6,480 + SGST ₹6,480) = ₹84,960. Sweep 15% Sinking Fund (₹10,800)." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "CHALLENGE_QUESTION", text: "Inquest: Confirm the 15% sinking fund reserve is exactly ₹10,800.00 with zero mathematical drift." },
      { sender: "💰 KUBER TREASURY", type: "RESPONSE_CLARIFICATION", text: "Verified: ₹72,000.00 * 0.15 = exactly ₹10,800.00. Tax split CGST/SGST equals 18.00%." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "AUDIT_APPROVAL", text: "Audit Verdict: PASSED ✓. 2 mathematical invariants verified with zero data corruption." },
      { sender: "👑 GARUDA EXECUTIVE", type: "EXECUTIVE_DECISION", text: "Certified Receipt Issued: Invoice VL-INV-2026-08-002 signed and sealed." }
    ],
    fleet: [
      { sender: "👑 GARUDA EXECUTIVE", type: "TASK_DELEGATION", text: "Delegate Task: Assess Tata Intra EV telematics and standstill immobilizer readiness." },
      { sender: "🚚 AEGIS FLEET", type: "WORK_PROPOSAL", text: "Telemetry: Battery SoH 99.4%, SoC 92.5%, Temp 33.5°C. Standstill Relay requested." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "CHALLENGE_QUESTION", text: "Inquest: What is the current speed? Is the asset in verified 0.0 km/h standstill?" },
      { sender: "🚚 AEGIS FLEET", type: "RESPONSE_CLARIFICATION", text: "Verified: Speed is strictly 0.0 km/h. DC fast charge ratio is 35% (< 70% OEM limit)." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "AUDIT_APPROVAL", text: "Audit Verdict: PASSED ✓. Standstill safety guardrail and Tata OEM warranty satisfied." },
      { sender: "👑 GARUDA EXECUTIVE", type: "EXECUTIVE_DECISION", text: "Certified Receipt Issued: Telemetry verified with zero safety violations." }
    ],
    legal: [
      { sender: "👑 GARUDA EXECUTIVE", type: "TASK_DELEGATION", text: "Delegate Task: Audit MSMED Act 45-day payment enforcement & DPDP Act privacy." },
      { sender: "⚖️ NYAYA LEGAL", type: "WORK_PROPOSAL", text: "Compliance Proposal: MSMED Act Sec 15/16 clauses active. Lucknow Premises NOC executed." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "CHALLENGE_QUESTION", text: "Inquest: Confirm all public surfaces redact raw PAN (BGVPJ3356G) and Aadhaar numbers." },
      { sender: "⚖️ NYAYA LEGAL", type: "RESPONSE_CLARIFICATION", text: "Verified: DPDP Act 2023 ring-fencing active. Raw identifiers sealed in private vaults." },
      { sender: "🔍 CHANAKYA AUDITOR", type: "AUDIT_APPROVAL", text: "Audit Verdict: PASSED ✓. Zero statutory or data privacy non-compliances." },
      { sender: "👑 GARUDA EXECUTIVE", type: "EXECUTIVE_DECISION", text: "Certified Receipt Issued: Enterprise compliance fully authenticated." }
    ]
  };

  function playDialogue(key) {
    if (!termEl) return;
    termEl.innerHTML = "";
    const list = dialogues[key] || dialogues.treasury;
    list.forEach((item, idx) => {
      setTimeout(() => {
        const line = document.createElement("div");
        line.style.marginBottom = "8px";
        let color = "#38bdf8";
        if (item.sender.includes("AUDITOR")) color = "#f59e0b";
        if (item.sender.includes("EXECUTIVE")) color = "#34d399";
        if (item.sender.includes("FLEET")) color = "#a855f7";
        if (item.sender.includes("LEGAL")) color = "#f43f5e";
        
        line.innerHTML = `<span style="color: ${color}; font-weight: bold;">[${item.sender}]</span> <span style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">(${item.type})</span><br/><span style="color: #e2e8f0;">${item.text}</span>`;
        termEl.appendChild(line);
        termEl.scrollTop = termEl.scrollHeight;
      }, idx * 400);
    });
  }

  if (btnTreasury) btnTreasury.addEventListener('click', () => playDialogue('treasury'));
  if (btnFleet) btnFleet.addEventListener('click', () => playDialogue('fleet'));
  if (btnLegal) btnLegal.addEventListener('click', () => playDialogue('legal'));

  // Play initial dialogue
  playDialogue('treasury');

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
