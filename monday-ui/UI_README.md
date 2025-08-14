# Monday UI – HUD (Fas D)

HUD lyssnar på LiveKit‑metadata för transkript och spelar upp inkommande ljud från en lokal track som agenten publicerar (TTS).

## Testa TTS
- Anslut agenten till rummet (`POST /connect` med klient‑token)
- Kör: `POST /speak` med `{ "text": "Hej från agenten" }`
- UI ska spela upp ljud (stub i Fas D om Piper saknas)

Övrigt se Fas B för transkript och anslutning.
