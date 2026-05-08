# Moborobo Platform

Web platform for monitoring smart waste nodes, visualizing live status on a map, and displaying the shortest collection route calculated by the backend.

## Structure

- `frontend/`: Vue 3 + Vite + Ant Design Vue + Leaflet UI
- `backend/`: FastAPI service, MQTT listener, route API
- `docs/`: API and integration notes

## Frontend Quick Start

```bash
cd frontend
npm install
npm run dev
```

The frontend expects a backend at `http://localhost:8000` by default and falls back to mock data until the API is ready.

## Backend Quick Start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend creates a local SQLite database and seeds demo nodes on first run. Set `DATABASE_URL` to point SQLAlchemy at another database.
