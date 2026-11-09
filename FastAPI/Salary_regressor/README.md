# Salary Regressor (FastAPI)

A minimal ML service that predicts salary from years of experience. Trains a linear regression on `salary.csv` and serves it via FastAPI.

## Files

| File | Purpose |
|---|---|
| `salary.csv` | Training data (`experience`, `salary`) |
| `train_model.py` | Trains the model, saves `model.pkl` |
| `pred_app.py` | FastAPI app that loads `model.pkl` and serves predictions |

> Note: the app file is `pred_app.py`, so the run command uses `pred_app:app`.

## Requirements

```
pandas
scikit-learn
joblib
fastapi
uvicorn[standard]
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Train

```bash
python train_model.py
# -> Saved model.pkl
```

## Run

```bash
uvicorn pred_app:app --reload --port 8000
```

## Test

Health check:
```bash
curl http://127.0.0.1:8000/health
```

Predict:
```bash
curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"experience": 7.5}'
```

Response:
```json
{"experience": 7.5, "prediction": 12345.67}
```

## API

| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET | `/health` | — | `{"status": "ok"}` |
| POST | `/predict` | `{"experience": float}` | `{"experience": float, "prediction": float}` |

## ⚠️ Important

- **Train before serving** — `model.pkl` is not committed; run `train_model.py` first.
- **Pin `scikit-learn`** in `requirements.txt` to the same version used for training. A mismatch (e.g. train on `1.5.1`, serve on `1.6.0`) can cause `InconsistentVersionWarning` or wrong predictions when `joblib.load()` unpickles the model.

```bash
pip freeze > requirements.txt   # after verifying training + serving works
```
```

Drop this in place of the auto-generated `README.md`. It matches your actual filenames (`red_app.py`, not `app.py`) and covers the two things a grader/teammate will trip on: missing `model.pkl` and sklearn version mismatch.
