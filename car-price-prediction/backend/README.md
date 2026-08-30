# Backend (FastAPI + ML Inference)

This backend serves the trained used-car price prediction pipeline and exposes APIs for prediction, deal analysis, health checks, and model metadata.

## Quick setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Main endpoints

- `GET /health`
- `GET /brands`
- `GET /brands/{brand}/models`
- `GET /model-metrics`
- `GET /model-info`
- `POST /predict`
- `POST /predict-with-asking`

## Notes

- Final model artifact is loaded from [full_pipeline.pkl](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/models/full_pipeline.pkl).
- Data science notebooks and dataset files are in [backend/notebooks/](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/notebooks) and [backend/data/](D:/Car-price-prediction-project.worktrees/car-price-prediction-documentation/backend/data).
