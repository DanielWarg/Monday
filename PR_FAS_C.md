# feat: Fas C – LLM via Ollama (Harmony)

## Sammanfattning
- Lägger till LLM‑stöd i agenten via Ollama (modell: `gpt-oss:20b`).
- Harmony‑template för konsekvent promptformat.
- Ny endpoint: `POST /chat` → `{ ok, text }`.
- Ingen verktygsanvändning och ingen TTS i denna fas.
- Dokumentation uppdaterad (`AGENT_README.md`, rot‑`README.md`).

## Miljö
- `OLLAMA_HOST` (t.ex. `http://127.0.0.1:11434`)
- `MODEL_NAME=gpt-oss:20b`

## Test
```
curl -s -X POST http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Hej!"}'
# → { "ok": true, "text": "..." }
```

## Acceptanskriterier
- [ ] `POST /chat` returnerar text från Ollama (gpt‑oss:20b)
- [ ] Harmony‑template används för prompt
- [ ] Ingen TTS eller verktyg i denna fas
- [ ] README uppdaterad med miljö och körinstruktioner
