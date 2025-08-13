# UI Token-proxy (lokal utveckling)
# Kör: uvicorn token_proxy:app --reload --port 7071
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

app = FastAPI(title="Monday UI token proxy")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

TOKEN_BACKEND = os.getenv("TOKEN_BACKEND", "http://127.0.0.1:7071/token")

@app.get("/api/token")
async def token():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(TOKEN_BACKEND)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"token":"mock-token","url": os.getenv("LIVEKIT_URL",""), "error": str(e)}
