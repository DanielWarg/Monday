# Monday UI – HUD (Fas A)

Denna del är en ren HUD/klient utan affärslogik. LiveKit är stubbat och token hämtas från en mock‑endpoint i samma UI.

## Kör lokalt (dev)

1. Kopiera `.env.example` till `.env` och fyll i vid behov:
   - `NEXT_PUBLIC_LIVEKIT_URL` (kan lämnas tomt i Fas A)
   - `NEXT_PUBLIC_TOKEN_URL` (t.ex. `/api/token`)
2. Installera och starta:

```
cd monday-ui
npm install
npm run dev -- --hostname 127.0.0.1 -p 3200
```

Öppna `http://127.0.0.1:3200`.

## Mock-token
- `pages/api/token.ts` returnerar `{ ok: true, token: "mock-livekit-token" }`.
- UI anropar `NEXT_PUBLIC_TOKEN_URL` (default `/api/token`) och visar anslutningsstatus (simulerad).

## Notering
- Byggläge i detta repo använder statisk export. API‑routes fungerar i dev, men ingår inte i statisk export. För Fas A räcker dev.
