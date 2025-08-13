# Monday (monorepo)

Fasning:
- A) LiveKit-anslutning (mock-token)
- B) STT → transcript till UI
- C) LLM-svar utan verktyg
- D) TTS tillbaka
- E) Verktygsregister + router-fallback
- F) Fler verktyg

Mappar:
- monday-ui: Next.js HUD (LiveKit-klient, /api/token-proxy)
- monday-agent: FastAPI tokenserver (mock), senare AgentRunner

Starta UI:
```bash
cd monday-ui
npm install
npm run dev -p 3200
```

Starta agent (mock token):
```bash
cd monday-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt httpx
uvicorn main:app --reload --host 127.0.0.1 --port 7071
```

UI kan hämta token via NEXT_PUBLIC_TOKEN_URL eller via /api/token route.
