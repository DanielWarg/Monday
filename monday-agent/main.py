from fastapi import FastAPI
from pydantic import BaseModel
import os
import asyncio

from .livekit_ingest import get_ingest
from .telemetry import telemetry

app = FastAPI(title="Monday Agent (Fas B)")

class HealthResponse(BaseModel):
    ok: bool
    stt: dict
    telemetry: dict

class TokenResponse(BaseModel):
    ok: bool
    token: str

@app.on_event("startup")
async def startup_event():
    # För enkelhet: koppla upp mot LiveKit automatiskt om env‑token finns via GET /token från UI:s serverless
    # I produktion genererar man en riktig JWT. Här förutsätter vi att frontend hämtar token och att agent kan få en egen.
    pass

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    ing = get_ingest()
    return HealthResponse(ok=True, stt=ing.stt_info(), telemetry=telemetry.snapshot())

@app.get("/token", response_model=TokenResponse)
async def token() -> TokenResponse:
    mock = os.getenv("LIVEKIT_MOCK_TOKEN", "agent-mock-livekit-token")
    return TokenResponse(ok=True, token=mock)

# Hjälp‑endpoint för att manuellt starta ingest (med en klient‑token)
class ConnectRequest(BaseModel):
    token: str

class ConnectResponse(BaseModel):
    ok: bool

@app.post("/connect", response_model=ConnectResponse)
async def connect(req: ConnectRequest) -> ConnectResponse:
    ing = get_ingest()
    asyncio.create_task(ing.connect(req.token))
    return ConnectResponse(ok=True)
