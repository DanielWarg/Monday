from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ToolSpec(BaseModel):
    name: str
    description: str
    schema: Dict[str, Any]

class LLMRequest(BaseModel):
    prompt: str
    tools: List[ToolSpec] = []
    system: Optional[str] = None  # Harmony‑template i senare faser

class LLMResponse(BaseModel):
    text: Optional[str] = None
    tool_call: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None

# TODO (Fas C): Koppla mot Ollama (gpt‑oss:20b) och Harmony‑prompt.
