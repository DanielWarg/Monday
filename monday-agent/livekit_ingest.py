from __future__ import annotations
import asyncio
import json
import os
import time
from typing import Optional
import numpy as np
from livekit import rtc

from .stt.whisper import WhisperSTT, WhisperConfig
from .stt.interfaces import STTResult
from .telemetry import telemetry

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

class Ingest:
    def __init__(self) -> None:
        self.room: Optional[rtc.Room] = None
        self.stt = WhisperSTT(WhisperConfig())
        self._audio_buffer = bytearray()
        self._connected = False

    async def connect(self, token: str) -> None:
        self.room = rtc.Room()
        await self.room.connect(LIVEKIT_URL, token)
        self._connected = True
        @self.room.on("track_subscribed")
        def _on_track_subscribed(track, *_):
            if isinstance(track, rtc.RemoteAudioTrack):
                stream = rtc.AudioStream(track)
                async def reader():
                    async for frame in stream:
                        # frame is pcm16 mono at 48000 hz → resample to 16k
                        pcm = np.frombuffer(frame.data, dtype=np.int16).astype(np.float32) / 32768.0
                        # naive resample by decimation
                        ratio = 48000 // 16000
                        pcm16k = (pcm[::ratio] * 32768.0).astype(np.int16).tobytes()
                        def on_partial(res: STTResult) -> None:
                            asyncio.create_task(self.send_metadata({
                                "type": "transcript_partial",
                                "text": res.text,
                                "ts": time.time()
                            }))
                        try:
                            final = self.stt.accept_audio(pcm16k, on_partial=on_partial)
                            if final and final.text:
                                await self.send_metadata({
                                    "type": "transcript_final",
                                    "text": final.text,
                                    "ts": time.time(),
                                })
                        except Exception:
                            telemetry.inc_errors()
                asyncio.create_task(reader())

    async def send_metadata(self, payload: dict) -> None:
        if not self.room:
            return
        data = json.dumps(payload).encode("utf-8")
        await self.room.local_participant.publish_data(data, reliable=True)

    def stt_info(self) -> dict:
        return self.stt.info()

_ingest: Optional[Ingest] = None

def get_ingest() -> Ingest:
    global _ingest
    if _ingest is None:
        _ingest = Ingest()
    return _ingest
