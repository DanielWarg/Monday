# feat: Fas A – Monday skeleton

## Sammanfattning
- Monorepo-struktur etablerad: `monday-ui/` (HUD) och `monday-agent/` (FastAPI-agent)
- Mock-tokenflöde: UI `/pages/api/token.ts` + agent `GET /token`
- UI visar anslutningsstatus (mockad), mic-knapp och placeholders för paneler
- Agent kör FastAPI med `GET /health` och `GET /token`, pipeline-mappar skapade med interfaces + TODO
- Dokumentation: `README.md`, `AUDIT.md`, `UI_README.md`, `AGENT_README.md`
- Inga verkliga beroenden till LiveKit/LLM/STT/TTS (allt mock i Fas A)

## Checklista (AC)
- [x] Repo har `monday-ui/` och `monday-agent/` med beskrivna filer
- [x] UI kan låtsas-joina via `/api/token` och visar anslutningsstatus (simulerad)
- [x] Agent svarar på `/token` (mock) och `/health`
- [x] `.env.example` finns i `monday-ui/` (se not nedan för agent)
- [x] `README.md`, `UI_README.md`, `AGENT_README.md`, `AUDIT.md` är ifyllda
- [x] Inga kopplingar till verklig LiveKit/LLM/STT/TTS

> Not: Vissa miljöer blockerar skrivning av filer som heter `.env.example`. Om `monday-agent/.env.example` saknas i PR-diff, följ `AGENT_README.md` och skapa den lokalt med innehållet som dokumenterats.

## Test
- UI
  - `cd monday-ui && npm install && npm run dev -- --hostname 127.0.0.1 -p 3200`
  - Öppna `http://127.0.0.1:3200`. Statusfält visar `Ansluter` → `Ansluten` via mock‑token.
- Agent (mock)
  - `cd monday-agent && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - `uvicorn main:app --host 127.0.0.1 --port 8001`
  - Verifiera `GET /health` och `GET /token`

## Nästa faser (TODO)
- B) STT i agenten, transkript till UI via LiveKit‑metadata
- C) LLM via Ollama (gpt‑oss:20b) med Harmony-template
- D) TTS (Piper) tillbaka till rummet
- E) Tool-register + router-fallback + strikt schema-validering
- F) Telemetri och UI-indikatorer
