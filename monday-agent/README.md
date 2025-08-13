# Monday Agent

Minimal FastAPI-tokenserver för UI-utveckling.

Start (utveckling):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 7071
```

Endpoint:
- GET /token → { token: "mock-token", url: LIVEKIT_URL }

Byt senare till riktig LiveKit-JWT i stället för mock-token.
