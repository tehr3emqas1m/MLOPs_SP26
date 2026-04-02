# Iris Flower Classifier — FastAPI + Docker
![Static Badge](https://img.shields.io/badge/Python-orange)
![Static Badge](https://img.shields.io/badge/Scikitlearn-red) 
![Static Badge](https://img.shields.io/badge/FastAPI-gray) 
![Static Badge](https://img.shields.io/badge/uvicorn-yellowgreen)
![Static Badge](https://img.shields.io/badge/joblib-green)
![Static Badge](https://img.shields.io/badge/jinja2-green)
![Static Badge](https://img.shields.io/badge/Docker-blue)

A machine learning web app that classifies Iris flowers using a Random Forest model, served via FastAPI and containerized with Docker.

---

<img width="1313" height="602" alt="Screenshot from 2026-04-02 13-08-08" src="https://github.com/user-attachments/assets/5079c268-4b01-4920-9f49-789c8b6520e2" />

## 📁 Project Structure

<pre>
ml-project/
├── train_model.py        # Training script
├── Dockerfile    
├── model/
│   └── model.pkl         # Saved model (created after training)
├── app/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── static/           # Frontend assets
│   └── templates/        # HTML templates
└── venv/                 # Virtual environment
</pre>

---

## Getting Started

### 1. Set Up the Project
```bash
mkdir ml-project && cd ml-project
mkdir -p app/static app/templates model
python3 -m venv venv0
source venv0/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r app/requirements.txt
```

<details>
<summary>📄 requirements.txt</summary>
```
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.0
joblib==1.3.2
jinja2==3.1.2
python-multipart==0.0.6
numpy==1.24.3
```

</details>

---

## Train the Model

Create `train_model.py` in the project root:
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
joblib.dump(clf, "model/model.pkl")
```

Then run:
```bash
python train_model.py
```

---

## FastAPI Application

Create `app/main.py`:
```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, os, numpy as np

app = FastAPI(title="Iris Flower Classifier")

app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model_path = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}")
model = joblib.load(model_path)

SPECIES = ["Setosa", "Versicolor", "Virginica"]

class IrisRequest(BaseModel):
    data: list

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(input: IrisRequest):
    features = np.array(input.data).reshape(1, -1)
    prediction = model.predict(features)
    proba = model.predict_proba(features)
    return {
        "prediction": int(prediction[0]),
        "species": SPECIES[prediction[0]],
        "confidence": float(max(proba[0]))
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": True}
```

---

## HTML Frontend

Create `app/templates/index.html`:

<details>
<summary>📄 index.html</summary>
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iris Flower Classifier</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; }
        label { font-weight: bold; color: #2c3e50; flex: 1; }
        input { padding: 10px; width: 150px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }
        input:focus { outline: none; border-color: #667eea; }
        button { width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 20px; transition: transform 0.2s; }
        button:hover { transform: translateY(-2px); }
        #result { margin-top: 30px; padding: 20px; border-radius: 10px; font-size: 18px; text-align: center; display: none; }
        .prediction { font-size: 24px; font-weight: bold; color: #27ae60; }
        .confidence { font-size: 14px; color: #7f8c8d; margin-top: 10px; }
        .error { color: #e74c3c; font-weight: bold; }
        .loading { color: #667eea; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌸 Iris Flower Classifier</h1>
        <form id="predictForm">
            <div class="form-group"><label>Sepal Length:</label><input type="number" step="0.1" id="sepal_length" required placeholder="cm"></div>
            <div class="form-group"><label>Sepal Width:</label><input type="number" step="0.1" id="sepal_width" required placeholder="cm"></div>
            <div class="form-group"><label>Petal Length:</label><input type="number" step="0.1" id="petal_length" required placeholder="cm"></div>
            <div class="form-group"><label>Petal Width:</label><input type="number" step="0.1" id="petal_width" required placeholder="cm"></div>
            <button type="submit">🔮 Predict Species</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
        document.getElementById("predictForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const resultDiv = document.getElementById("result");
            const vals = ["sepal_length","sepal_width","petal_length","petal_width"].map(id => parseFloat(document.getElementById(id).value));
            if (vals.some(isNaN)) { resultDiv.style.display="block"; resultDiv.innerHTML='<span class="error">❌ Please enter valid numbers!</span>'; return; }
            resultDiv.style.display="block";
            resultDiv.innerHTML='<span class="loading">🤔 Analyzing flower measurements...</span>';
            try {
                const res = await fetch("/predict", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ data: vals }) });
                const result = await res.json();
                resultDiv.innerHTML = `<div class="prediction">🌸 ${result.species}</div><div class="confidence">Confidence: ${(result.confidence*100).toFixed(1)}%</div>`;
            } catch { resultDiv.innerHTML='<span class="error">❌ Prediction failed. Please try again.</span>'; }
        });
    </script>
</body>
</html>
```

</details>

---

## Run Locally
```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Docker Deployment

### Dockerfile (project root folder)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
COPY model/ /app/model/
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### .dockerignore
```
venv/
__pycache__/
*.pyc
.git/
.DS_Store
*.pkl
!model/*.pkl
train_model.py
```

### Build & Run
```bash
docker build --no-cache -t iris-classifier_m .
docker run -p 5000:5000 iris-classifier_m
```

> **Note:** If Docker Desktop isn't running: `systemctl --user start docker-desktop`

Visit: [http://localhost:5000](http://localhost:5000)

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `POST` | `/predict` | Predict iris species |
| `GET` | `/health` | Health check |

**Example request:**
```json
{ "data": [5.1, 3.5, 1.4, 0.2] }
```

**Example response:**
```json
{ "prediction": 0, "species": "Setosa", "confidence": 0.99 }
```

---

## Iris Species

![Three-species-of-IRIS-flower](https://github.com/user-attachments/assets/c3df8d38-480d-4a83-83eb-b6495b0eabc2)


| Class | Species |
|-------|---------|
| 0 | Setosa |
| 1 | Versicolor |
| 2 | Virginica |
