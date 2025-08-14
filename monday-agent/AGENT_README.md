# Monday Agent – Fas B (STT → LiveKit)

FastAPI‑agent med STT (Whisper) som lyssnar på LiveKit‑rummet och publicerar transkript som metadata:
- `transcript_partial` (grå, löpande)
- `transcript_final` (commit efter EOU)

## Miljö
Skapa `.env` baserat på `.env.example`:
```
LIVEKIT_URL=ws(s)://<livekit-server>
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
STT_ENGINE=whisper
WHISPER_MODEL=small
WHISPER_DEVICE=auto
VAD_THRESHOLD=0.6
MAX_LATENCY_MS=800
```

## Kör (mock)
```
cd monday-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001
```

## Anslut till rum
- Hämta en klient‑token (ex. via UI `/api/token` eller egen JWT‑generator)
- POST `http://127.0.0.1:8001/connect` med `{ "token": "<client-token>" }`
- Health: `GET /health` visar STT (model/device) och telemetri (p50/p95)

## Telemetri
- p50/p95 för time‑to‑first‑partial och time‑to‑final
- Antal VAD‑triggers och fel

## Noteringar
- En enkel VAD/EOU baserad på energi används. Justera `VAD_THRESHOLD` för miljön.
- Inga LLM/TTS/verktyg körs i Fas B.
