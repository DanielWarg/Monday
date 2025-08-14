# Monday UI – HUD (Fas B)

HUD lyssnar på LiveKit‑metadata och visar transkript i realtid:
- `transcript_partial`: visas i grått som live‑text
- `transcript_final`: committas till historiken

## Kör lokalt (dev)

1. `.env` (kan återanvändas från Fas A):
   - `NEXT_PUBLIC_LIVEKIT_URL` (ws(s)://…)
   - `NEXT_PUBLIC_TOKEN_URL` (default `/api/token`)
2. Installera och starta:

```
cd monday-ui
npm install
npm run dev -- --hostname 127.0.0.1 -p 3200
```

Öppna `http://127.0.0.1:3200`.

## Transkriptpanelen
- Meny: "Visa partials" på/av, "Rensa" historik
- Indikator: "Lyssnar…" när inkommande audio upptäcks

## Notering
- Ingen LLM/TTS/verktyg i Fas B. Endast STT.
