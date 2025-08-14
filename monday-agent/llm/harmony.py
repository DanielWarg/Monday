from __future__ import annotations
from typing import List, Dict, Any, Optional
import os
import httpx
from pydantic import BaseModel

HARMONY_TEMPLATE = """
System:
- Du är Monday-agenten. Svara kort på svenska.
- Om verktyg krävs (inte i Fas C), svara med saklig text ändå.

Användarkontext:
{context}

Fråga:
{prompt}
"""

class ChatRequest(BaseModel):
    prompt: str
    context: Optional[List[str]] = None
    model: str = os.getenv("MODEL_NAME", "gpt-oss:20b")

class ChatResponse(BaseModel):
    text: str
    provider: str = "ollama"

async def call_ollama(req: ChatRequest) -> ChatResponse:
    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    tpl = HARMONY_TEMPLATE.format(context="\n".join(req.context or []), prompt=req.prompt)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{host}/api/generate", json={"model": req.model, "prompt": tpl, "stream": False})
        r.raise_for_status()
        j = r.json()
        text = j.get("response") or j.get("text") or ""
        return ChatResponse(text=text)
