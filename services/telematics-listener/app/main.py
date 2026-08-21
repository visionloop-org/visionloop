import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.simulator import simulator
from app.config import settings

app = FastAPI(
    title="Vision Loop — IoT Telematics Listener & Simulator",
    description="Real-time ingestion and simulation engine for Tata Intra EV telematics (CAN-Bus, GPS, Battery SoC).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulation_task = None

async def background_telemetry_loop():
    """Continuous background loop pushing live telemetry every interval."""
    while True:
        try:
            await simulator.step()
        except Exception:
            pass
        await asyncio.sleep(settings.SIMULATION_INTERVAL_SEC)

@app.on_event("startup")
async def start_background_tasks():
    global simulation_task
    simulation_task = asyncio.create_task(background_telemetry_loop())

@app.get("/")
def health_check():
    return {
        "service": "Vision Loop Telematics Ingestor",
        "status": "active",
        "simulating_asset": simulator.asset_tag,
        "current_soc_pct": simulator.soc_pct,
        "odometer_km": simulator.odometer_km,
        "interval_sec": settings.SIMULATION_INTERVAL_SEC
    }

@app.post("/simulate/step")
async def trigger_single_step():
    """Manually advance simulation by one step."""
    return await simulator.step()

@app.post("/simulate/charge")
def set_charging_state(charging: bool = True):
    """Force charging state on the simulated Tata Intra EV."""
    simulator.charging_status = "CHARGING_FAST" if charging else "DISCHARGING"
    if charging:
        simulator.speed_kmh = 0.0
    return {"status": "success", "charging_status": simulator.charging_status}
