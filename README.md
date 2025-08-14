# Monday – Monorepo

Detta repo innehåller två delar:
- `monday-ui/`: HUD/klient (Next.js) – ingen affärslogik
- `monday-agent/`: Python‑agent (FastAPI) – tokenserver + pipeline (modulär)

## Arkitektur
UI ↔ LiveKit ↔ Agent.
- UI hämtar token (mock i Fas A) från `/api/token` (UI) eller agenten.
- Ljud/RTC via LiveKit (kommer i senare faser).
- Affärslogik (STT/LLM/TTS/Tools) sker i agenten.

## Faser
- A) Skeleton (denna PR): mock‑token, tomma moduler
- B) STT i agenten, transkript till UI via LiveKit‑metadata
- C) LLM via Ollama (gpt‑oss:20b) med Harmony‑template
- D) TTS (Piper) tillbaka till rummet
- E) Tool‑register med Pydantic‑schema, confidence‑tröskel och router‑fallback, strikt validering
- F) Telemetri (p50/p95, refusal‑rate, tool‑hit‑rate, schemafel) och UI‑indikatorer

## Miljönycklar
- UI: `NEXT_PUBLIC_LIVEKIT_URL`, `NEXT_PUBLIC_TOKEN_URL`
- Agent: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `OLLAMA_HOST`, `MODEL_NAME`, `STT_ENGINE`, `TTS_ENGINE`

## Start i mock‑läge
- UI: se `monday-ui/UI_README.md`
- Agent: se `monday-agent/AGENT_README.md`

## PR 1 – Acceptanskriterier (Fas A)
- [x] Repo har `monday-ui/` och `monday-agent/` med beskrivna filer
- [x] UI kan låtsas‑joina via `/api/token` och visar anslutningsstatus (simulerad)
- [x] Agent kör FastAPI och svarar på `/token` (mock) och `/health`
- [x] `.env.example` finns i `monday-ui/` (agentens `.env.example` måste ev. skapas manuellt lokalt p.g.a. verktygsbegränsning – se AGENT_README)
- [x] `README.md`, `UI_README.md`, `AGENT_README.md` och `AUDIT.md` är ifyllda och konsekventa
- [x] Inga beroenden till verkliga LLM/STT/TTS eller LiveKit ännu; allt mockat

Se även `AUDIT.md` för beslut från `friday_jarvis`‑audit.
