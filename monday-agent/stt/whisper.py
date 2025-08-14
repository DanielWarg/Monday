from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional, List
import os
import time
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel
from .interfaces import STTResult
from ..telemetry import telemetry

@dataclass
class WhisperConfig:
    model_name: str = os.getenv("WHISPER_MODEL", "small")
    device: str = os.getenv("WHISPER_DEVICE", "auto")
    vad_threshold: float = float(os.getenv("VAD_THRESHOLD", "0.6"))
    max_latency_ms: int = int(os.getenv("MAX_LATENCY_MS", "800"))

class WhisperSTT:
    def __init__(self, cfg: Optional[WhisperConfig] = None) -> None:
        self.cfg = cfg or WhisperConfig()
        self.model = WhisperModel(self.cfg.model_name, device=self.cfg.device)
        self.sample_rate = 16000
        self._buffer: List[np.ndarray] = []
        self._last_partial_at: Optional[float] = None
        self._speech_started_at: Optional[float] = None

    def reset(self) -> None:
        self._buffer.clear()
        self._last_partial_at = None
        self._speech_started_at = None

    def _energy_vad(self, pcm: np.ndarray) -> float:
        if pcm.size == 0:
            return 0.0
        # RMS energi (0..1)
        energy = float(np.sqrt(np.mean(np.square(pcm))))
        return energy

    def accept_audio(self, pcm16: bytes, on_partial: Callable[[STTResult], None]) -> Optional[STTResult]:
        # pcm16 är 16‑bit little‑endian mono på 16kHz
        arr = np.frombuffer(pcm16, dtype=np.int16).astype(np.float32) / 32768.0
        self._buffer.append(arr)
        vad_level = self._energy_vad(arr)
        now = time.time()
        if vad_level > self.cfg.vad_threshold:
            if self._speech_started_at is None:
                self._speech_started_at = now
        # Partial: kör snabb transkription på rullande fönster om latensgränsen passerats
        if self._speech_started_at is not None:
            if (self._last_partial_at is None) or ((now - self._last_partial_at) * 1000.0 >= self.cfg.max_latency_ms):
                audio = np.concatenate(self._buffer[-10:]) if len(self._buffer) > 0 else np.array([], dtype=np.float32)
                if audio.size > 0:
                    # Skriv temporärt WAV i minne (faster‑whisper accepterar numpy direkt via transcribe ifrån file=?)
                    # Vi använder transcribe på PCM via numpy array
                    segments, _ = self.model.transcribe(audio, language="sv", vad_filter=False, beam_size=1, temperature=0.0)
                    text = "".join([seg.text for seg in segments]) if segments else ""
                    if text.strip():
                        self._last_partial_at = now
                        elapsed = (now - (self._speech_started_at or now)) * 1000.0
                        telemetry.ttfp_ms.add(elapsed)
                        on_partial(STTResult(text=text.strip(), confidence=0.5))
        # EOU: om energi sjunker under tröskel och vi nyligen talat – final
        if self._speech_started_at is not None and vad_level <= self.cfg.vad_threshold * 0.5:
            # samla hela bufferten till slutlig transkription
            audio = np.concatenate(self._buffer) if len(self._buffer) > 0 else np.array([], dtype=np.float32)
            self.reset()
            if audio.size == 0:
                return None
            t0 = time.time()
            segments, _ = self.model.transcribe(audio, language="sv", vad_filter=False, beam_size=1, temperature=0.0)
            final_text = " ".join([seg.text for seg in segments]).strip() if segments else ""
            telemetry.inc_vad()
            telemetry.ttf_ms.add((time.time() - t0) * 1000.0)
            if final_text:
                return STTResult(text=final_text, confidence=0.8)
        return None

    def info(self) -> dict:
        return {
            "engine": "whisper",
            "model": self.cfg.model_name,
            "device": self.cfg.device,
        }
