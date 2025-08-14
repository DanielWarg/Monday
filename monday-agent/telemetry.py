from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import threading
import bisect

@dataclass
class Distribution:
    values: List[float] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, v: float) -> None:
        with self.lock:
            bisect.insort(self.values, v)

    def quantile(self, q: float) -> float:
        with self.lock:
            if not self.values:
                return 0.0
            idx = int(max(0, min(len(self.values) - 1, round(q * (len(self.values) - 1)))))
            return float(self.values[idx])

@dataclass
class Telemetry:
    ttfp_ms: Distribution = field(default_factory=Distribution)  # time-to-first-partial
    ttf_ms: Distribution = field(default_factory=Distribution)   # time-to-final
    vad_triggers: int = 0
    errors: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def inc_vad(self) -> None:
        with self.lock:
            self.vad_triggers += 1

    def inc_errors(self) -> None:
        with self.lock:
            self.errors += 1

    def snapshot(self) -> Dict[str, float]:
        return {
            "p50_ttfp_ms": self.ttfp_ms.quantile(0.50),
            "p95_ttfp_ms": self.ttfp_ms.quantile(0.95),
            "p50_ttf_ms": self.ttf_ms.quantile(0.50),
            "p95_ttf_ms": self.ttf_ms.quantile(0.95),
            "vad_triggers": float(self.vad_triggers),
            "errors": float(self.errors),
        }

telemetry = Telemetry()
