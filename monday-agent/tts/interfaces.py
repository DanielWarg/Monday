from pydantic import BaseModel
from typing import Optional

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class TTSResult(BaseModel):
    audio_chunk: bytes

# TODO (Fas D): Implementera Piper TTS.
