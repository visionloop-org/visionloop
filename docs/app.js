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
