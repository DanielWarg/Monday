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
- A) Skeleton (klar)
- B) STT i agenten, transkript till UI via LiveKit‑metadata (denna PR)
- C) LLM via Ollama (gpt‑oss:20b) med Harmony‑template
- D) TTS (Piper) tillbaka till rummet
- E) Tool‑register med Pydantic‑schema, confidence‑tröskel och router‑fallback, strikt validering
- F) Telemetri (p50/p95, refusal‑rate, tool‑hit‑rate, schemafel) och UI‑indikatorer

## Miljönycklar
- UI: `NEXT_PUBLIC_LIVEKIT_URL`, `NEXT_PUBLIC_TOKEN_URL`
- Agent: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `STT_ENGINE=whisper`, `WHISPER_MODEL`, `WHISPER_DEVICE`, `VAD_THRESHOLD`, `MAX_LATENCY_MS`

## Start i mock‑läge
- UI: se `monday-ui/UI_README.md`
- Agent: se `monday-agent/AGENT_README.md`

## PR 2 – Acceptanskriterier (Fas B)
- [ ] Agenten ansluter till LiveKit, tar emot audio och publicerar `transcript_partial` p50 ≤ 800 ms och `transcript_final` p50 < 2.5 s
- [ ] UI visar partial i realtid och flyttar texten till historik vid final
- [ ] Ingen LLM/TTS/verktyg körs
- [ ] `GET /health` visar STT (model/device) och telemetri p50/p95
- [ ] README‑filer uppdaterade med körning, env och teststeg

Se även `AUDIT.md` och respektive del‑README.
