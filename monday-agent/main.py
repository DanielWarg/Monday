from fastapi import FastAPI
from pydantic import BaseModel
import os
import asyncio

from .livekit_ingest import get_ingest
from .telemetry import telemetry
from .llm.harmony import ChatRequest, call_ollama

app = FastAPI(title="Monday Agent (Fas C)")

class HealthResponse(BaseModel):
    ok: bool
    stt: dict
    telemetry: dict

class TokenResponse(BaseModel):
    ok: bool
    token: str

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    ing = get_ingest()
    return HealthResponse(ok=True, stt=ing.stt_info(), telemetry=telemetry.snapshot())

@app.get("/token", response_model=TokenResponse)
async def token() -> TokenResponse:
    mock = os.getenv("LIVEKIT_MOCK_TOKEN", "agent-mock-livekit-token")
    return TokenResponse(ok=True, token=mock)

class ConnectRequest(BaseModel):
    token: str

class ConnectResponse(BaseModel):
    ok: bool

@app.post("/connect", response_model=ConnectResponse)
async def connect(req: ConnectRequest) -> ConnectResponse:
    ing = get_ingest()
    asyncio.create_task(ing.connect(req.token))
    return ConnectResponse(ok=True)

class ChatIn(BaseModel):
    prompt: str

class ChatOut(BaseModel):
    ok: bool
    text: str

@app.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn) -> ChatOut:
    res = await call_ollama(ChatRequest(prompt=body.prompt))
    return ChatOut(ok=True, text=res.text)
