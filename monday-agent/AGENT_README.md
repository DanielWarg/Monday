# Monday Agent – Fas A (Mock)

FastAPI‑agent som exponerar:
- `GET /health` → `{ ok: true }`
- `GET /token` → `{ ok: true, token: "agent-mock-livekit-token" }`

## Kör lokalt

Rekommenderad virtuell miljö:
```
cd monday-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001
```

TODO: Koppla riktiga LiveKit‑nycklar i senare faser (B–F). För Fas A är token mockad och ingen extern tjänst används.

## Struktur (pipeline – tomma moduler)
- `stt/`, `llm/`, `tts/`, `tools/`, `router/`, `prompts/` – varje modul får ett interface och TODO för Fas B–F.
