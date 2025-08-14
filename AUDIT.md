AUDIT – friday_jarvis till Monday

Denna AUDIT sammanfattar vad vi tar med från referensprojektet friday_jarvis och vad vi förändrar i Monday för att uppnå en ren separering mellan UI och agent, införa strikt schema‑validering, Harmony‑template, fallback‑router och telemetri.

Vad vi tar med
- Agentupplägg (Python):
  - HTTP‑API för kommandon, verktyg och hälsa.
  - Modulärt tänk: separata mappar för STT, LLM, TTS, verktyg.
- Verktygsidéer:
  - Webbsök, väder, say/display, och routing mellan verktyg.
  - Idé om “dry‑run”/riskbedömning innan åtgärd.
- Realtidsflöde:
  - LiveKit som bärare för ljud i realtid (tas in i Monday i kommande faser).

Vad vi förändrar
- Ren separation (arkitektur):
  - monday-ui/ blir en ren HUD/klient utan affärslogik (endast UI + LiveKit‑klientstub + tokenhämtning).
  - monday-agent/ blir Python‑agent med tokenserver och pipeline (STT/LLM/TTS/Tools) – helt frikopplat från UI.
- Strikt schema‑validering:
  - All I/O i agenten valideras med Pydantic (in‑/utdata för varje steg och verktyg).
  - Verktyg definierar egna Pydantic‑scheman för anrop och svar, inklusive konfidens.
- Harmony‑template (LLM):
  - Används för konsekvent promptstruktur och tool‑calling.
  - Verktyg/handlingar exponeras via schema, inte fri text.
- Fallback‑router:
  - Router med konfidens‑tröskel; vid låg konfidens → säkrare fallback eller förfrågan om klargörande till användaren.
  - Router agerar också som policy‑punkt (whitelist/blacklist) för verktyg.
- Telemetri:
  - p50/p95 per steg (STT/LLM/TTS/Tools), refusal‑rate, tool‑hit‑rate, schemafel.
  - UI‑indikatorer för “assistant_speaking” och “tool_called”.

Praktiska val i Monday
- Monorepo:
  - Rot: README.md, AUDIT.md, .gitignore.
  - monday-ui/ (Next.js‑HUD): mic‑knapp, statusfält (ansluten/lyssnar/talar), transkriptpanel, tool‑logg, LiveKit‑klientstub som hämtar mock‑token via /api/token (UI‑serverless).
  - monday-agent/ (FastAPI): /health och /token (mock), tomma moduler för stt/, llm/, tts/, tools/, router/, prompts/ med interface‑filer (TODO) och strikt schema‑kontrakt.
- Inga externa beroenden i Fas A:
  - Ingen riktig LiveKit, STT, LLM eller TTS – allt mockas och ersätts senare.

Skillnader mot friday_jarvis
- UI hålls 100% fri från verktygs/LLM‑anrop – endast tokenhämtning och HUD.
- Agenten centraliserar all affärslogik och verktyg – isolerat från UI.
- Konsekvent validering med Pydantic på varje gränssnitt.
- Harmoniserad promptdesign (Harmony) + verktygsanrop via schema i senare faser.
- Router med fallback och konfidensbedömning.
- Inbyggd telemetri och tydliga UI‑signaler för status.

Nästa steg
- Fas A (denna PR): leverera körbart skelett med mockad token och tomma moduler.
- Faser B–F: implementera STT → LLM (Ollama, gpt‑oss:20B, Harmony) → TTS → verktyg+router → telemetri.
