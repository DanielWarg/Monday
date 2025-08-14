# Monday — UI‑only HUD

Detta repo heter nu Monday och innehåller endast gränssnittet (Next.js HUD) utan backend‑beroenden. All funktion som kräver server/WS/Spotify är avstängd; syftet är att visa grafiken lokalt.

## Starta i dev

```
cd monday-ui
npm install
npm run dev -- --hostname 127.0.0.1 -p 3200
```

Öppna: `http://127.0.0.1:3200`

## Statisk export

```
cd monday-ui
npm run build
python3 -m http.server 3201 -d ./out
```

Öppna: `http://127.0.0.1:3201`

## Struktur

- `monday-ui/`: Next.js 15 + React 19 + Tailwind v4, PWA aktiverad för prod‑build (kan stängas av).
- `monday-agent/`: ej använd i denna UI‑only‑variant.

## Noteringar

- Kamera/mikrofon, geolokalisering, WS och Spotify är avstängda med feature‑flaggor.
- För ren statisk visning, använd export enligt ovan.

## Licens

TBD
