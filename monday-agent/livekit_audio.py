from __future__ import annotations
from typing import Optional
import numpy as np
from livekit import rtc
from livekit_ingest import get_ingest

class AudioPublisher:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self._source: Optional[rtc.AudioSource] = None
        self._track: Optional[rtc.LocalAudioTrack] = None

    def _ensure_track(self) -> None:
        if self._source is None:
            self._source = rtc.AudioSource(self.sample_rate, 1)
        if self._track is None:
            self._track = rtc.LocalAudioTrack.create_audio_track("agent-tts", self._source)
            room = get_ingest().room
            if not room:
                raise RuntimeError("Room is not connected")
            room.local_participant.publish_track(self._track)

    def publish_pcm16(self, pcm_bytes: bytes) -> None:
        self._ensure_track()
        if not self._source:
            return
        # Convert bytes -> int16 numpy -> push in frames of 20ms (320 samples at 16k)
        arr = np.frombuffer(pcm_bytes, dtype=np.int16)
        frame_size = int(self.sample_rate * 0.02)  # 20ms
        num_frames = (len(arr) + frame_size - 1) // frame_size
        for i in range(num_frames):
            start = i * frame_size
            end = min(len(arr), start + frame_size)
            chunk = arr[start:end]
            if chunk.size == 0:
                continue
            data = chunk.tobytes()
            frame = rtc.AudioFrame(data=data, sample_rate=self.sample_rate, num_channels=1)
            self._source.capture_frame(frame)

_publisher: Optional[AudioPublisher] = None

def get_publisher() -> AudioPublisher:
    global _publisher
    if _publisher is None:
        _publisher = AudioPublisher()
    return _publisher
