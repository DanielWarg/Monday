from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RouteCandidate(BaseModel):
    name: str
    confidence: float
    args: Dict[str, Any]

class RouterDecision(BaseModel):
    chosen: Optional[RouteCandidate]
    fallback_used: bool = False
    rationale: Optional[str] = None

# TODO (Fas E): Implementera router med konfidens‑tröskel och fallback.
