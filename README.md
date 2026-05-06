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
