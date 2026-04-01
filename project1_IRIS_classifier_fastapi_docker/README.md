# 🌸 Iris Flower Classifier - FastAPI + Docker 🚀

Welcome to the **Iris Flower Classifier**! Train a model on the **IRIS dataset**, deploy it with **FastAPI**, and containerize with **Docker**. See a working ML app in action.

---

## 📂 Project Structure


ml-project/
├── train_model.py # Training script
├── model/ # Saved model
│ └── model.pkl
├── app/
│ ├── main.py # FastAPI app
│ ├── requirements.txt # Dependencies
│ ├── static/ # Frontend assets
│ └── templates/ # HTML templates
└── venv/ # Virtual environment


---

## ⚡ Quick Start

### 1️⃣ Setup

```bash
git clone <repo-url>
cd ml-project
mkdir -p app/static app/templates model
python3 -m venv venv0
source venv0/bin/activate
2️⃣ Install Dependencies
cat > app/requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.0
joblib==1.3.2
jinja2==3.1.2
python-multipart==0.0.6
numpy==1.24.3
EOF
pip install -r app/requirements.txt
3️⃣ Train Model
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
joblib.dump(clf, "model/model.pkl")

Run: python train_model.py

4️⃣ FastAPI App (app/main.py)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, os, numpy as np

app = FastAPI(title="Iris Flower Classifier")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
if not os.path.exists(model_path): raise FileNotFoundError(f"Model not found at {model_path}")
model = joblib.load(model_path)
SPECIES = ["Setosa", "Versicolor", "Virginica"]

class IrisRequest(BaseModel): data: list

@app.get("/", response_class=HTMLResponse)
async def home(request: Request): return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(input: IrisRequest):
    features = np.array(input.data).reshape(1, -1)
    prediction = model.predict(features)
    prediction_proba = model.predict_proba(features)
    return {"prediction": int(prediction[0]), "species": SPECIES[prediction[0]], "confidence": float(max(prediction_proba[0]))}

@app.get("/health")
async def health(): return {"status": "healthy", "model_loaded": True}
5️⃣ Frontend (app/templates/index.html)

Sexy interactive HTML form with gradient styles, input fields for sepal/petal measurements, and live prediction with confidence displayed. (See project code for full HTML + JS.)

6️⃣ Run Locally
cd app
uvicorn main:app --host 0.0.0.0 --port 5000 --reload

Open http://127.0.0.1:5000

7️⃣ Dockerize

Dockerfile:

FROM python:3.9-slim
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
COPY model/ /app/model/
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

.dockerignore:

venv/
__pycache__/
*.pyc
.git/
.DS_Store
*.pkl
!model/*.pkl
train_model.py

Build & run:

docker build -t iris-classifier_m .
docker run -p 5000:5000 iris-classifier_m

Visit http://localhost:5000
