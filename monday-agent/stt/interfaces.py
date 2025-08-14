from pydantic import BaseModel
from typing import Optional

class STTRequest(BaseModel):
    audio_chunk: bytes
    language: Optional[str] = None

class STTResult(BaseModel):
    text: str
    confidence: float

# TODO (Fas B): Implementera STT‑engine enligt STT_ENGINE och returnera STTResult.
