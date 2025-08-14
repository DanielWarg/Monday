# Monday Agent – Fas C (LLM via Ollama)

STT från Fas B kvarstår. Denna fas lägger till LLM (Ollama, gpt‑oss:20B) med Harmony‑template.

## Miljö (utökning)
```
OLLAMA_HOST=http://127.0.0.1:11434
MODEL_NAME=gpt-oss:20b
```

## Endpoints
- `POST /chat` → `{ ok, text }` – kör Harmony‑template mot Ollama
- `GET /health` – oförändrad (STT + telemetri)

## Kör
Se Fas B. Starta även Ollama lokalt med önskad modell. TODO: faktisk modellpull och policies.

## Noteringar
- Inga verktyg eller TTS i Fas C; ren textrespons.
- Harmony-template används för konsekvent uppmaningsformat.
