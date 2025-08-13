from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Monday Agent Token Server")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

class TokenResponse(BaseModel):
    token: str
    url: str

@app.get("/token", response_model=TokenResponse)
def get_token():
    # TODO: skapa JWT för LiveKit via API_KEY/SECRET. Tills vidare mock.
    url = os.getenv("LIVEKIT_URL", "")
    return TokenResponse(token="mock-token", url=url)
