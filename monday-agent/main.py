from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Monday Agent (Fas A)")

class HealthResponse(BaseModel):
    ok: bool

class TokenResponse(BaseModel):
    ok: bool
    token: str

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(ok=True)

@app.get("/token", response_model=TokenResponse)
async def token() -> TokenResponse:
    mock = os.getenv("LIVEKIT_MOCK_TOKEN", "agent-mock-livekit-token")
    return TokenResponse(ok=True, token=mock)
