from pydantic import BaseModel
from typing import Any, Dict, Optional

class ToolInput(BaseModel):
    payload: Dict[str, Any]

class ToolOutput(BaseModel):
    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    confidence: Optional[float] = None

# TODO (Fas E): Implementera tool‑register (web_search, weather, say/display) med strikt validering.
