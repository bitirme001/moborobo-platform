# Moborobo Backend

FastAPI service for smart waste node telemetry, database persistence, and collection route calculation.

- FastAPI
- SQLAlchemy
- SQLite by default through `DATABASE_URL=sqlite:///./moborobo.db`
- CORS enabled for the Vite frontend
- Seeded demo nodes matching the frontend map

## Quick Start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API starts at `http://localhost:8000`. Interactive docs are available at `http://localhost:8000/docs`.

## Environment

Copy `.env.example` if you want to override defaults:

```bash
cp .env.example .env
```

Supported variables:

- `DATABASE_URL`: SQLAlchemy database URL. Defaults to `sqlite:///./moborobo.db`.
- `FRONTEND_ORIGINS`: comma-separated allowed frontend origins.

## Endpoints

- `GET /health`: health check.
- `GET /nodes`: all known garbage nodes.
- `GET /nodes/{node_id}`: one garbage node.
- `POST /nodes/{node_id}/telemetry`: records telemetry and updates the node status.
- `GET /route`: nearest-neighbor collection route for currently full nodes.

Example telemetry payload:

```json
{
  "weightKg": 28.4,
  "fillPercent": 92,
  "isFull": true,
  "recordedAt": "2026-05-07T13:20:00Z"
}
```

When creating a brand-new node through telemetry, include `lat` and `lng`.
