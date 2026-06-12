import os
import sys
import queue
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add current directory to path so we can import main
sys.path.append(os.getcwd())

from mainbackup import handle_command
from config import FEATURES

app = FastAPI(title="FRIDAY AI Bridge")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextVoice:
    """Captured speech as text for the web interface."""

    def __init__(self):
        self._responses: queue.Queue[str] = queue.Queue()

    def speak(self, text: str, language: str = None) -> None:
        self._responses.put(text)

    def listen(self, language: str = None) -> Optional[str]:
        return None

    def get_greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        return "Good evening"

    def drain(self) -> List[str]:
        msgs = []
        while not self._responses.empty():
            try:
                msgs.append(self._responses.get_nowait())
            except queue.Empty:
                break
        return msgs


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    status: str
    responses: List[str]


@app.post("/command", response_model=CommandResponse)
async def process_command(request: CommandRequest):
    voice = TextVoice()
    try:
        # We run the synchronous handle_command
        # In a real app, you might want to run this in a threadpool
        handle_command(request.command, voice)
        responses = voice.drain()
        return CommandResponse(status="success", responses=responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/amplitude")
async def get_amplitude():
    """Returns a fake real-time amplitude for visualization when FRIDAY is speaking."""
    import random

    return {"amplitude": random.uniform(0.1, 1.0)}


@app.get("/security/scan")
async def security_scan():
    from modules.security_vault.hacking_suite import scan_network

    res = scan_network("192.168.1.0/24")
    return {"result": res}


@app.get("/security/audit")
async def security_audit():
    from modules.security_vault.hacking_suite import audit_local_ports

    res = audit_local_ports()
    return {"result": res}


@app.get("/finance/market")
async def finance_market():
    from modules.integrations.finance_intelligence import get_market_summary

    res = get_market_summary()
    return {"result": res}


@app.get("/finance/price/{symbol}")
async def finance_price(symbol: str):
    from modules.integrations.finance_intelligence import (
        get_stock_price,
        get_crypto_price,
    )

    if any(s in symbol.upper() for s in ["BTC", "ETH", "SOL", "DOGE"]):
        res = get_crypto_price(symbol)
    else:
        res = get_stock_price(symbol)
    return {"result": res}


@app.post("/autonomous/task")
async def add_auto_task(description: str, interval: int):
    from modules.core.autonomous_agent import global_agent

    res = global_agent.add_task(description, interval)
    return {"result": res}


@app.get("/os/organize")
async def os_organize():
    from modules.os_control.master_automation import organize_desktop

    res = organize_desktop()
    return {"result": res}


@app.post("/research")
async def run_research(topic: str):
    from modules.integrations.internet_entity import deep_research

    res = deep_research(topic)
    return {"result": res}


@app.get("/status")
async def get_status():
    return {"status": "online", "features": FEATURES}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
