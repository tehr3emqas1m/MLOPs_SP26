

# MLflow?

MLflow is an open-source platform that manages the end-to-end machine learning lifecycle:

- **Track experiments** - Log and compare parameters, metrics, and artifacts (models, plots)
- **Manage models** - Store, version, and deploy models to production
- **Package code** - Reproduce runs with consistent environments (conda, docker)
- **Deploy models** - Serve models via REST API or to cloud platforms

# MLflow Iris Classification Project

Now let's use MLflow to track and compare Random Forest's different hyperparameters (`n_estimators=1` vs `2`) by 
automatically logging accuracy metrics, parameters, and models, then visualizing everything in the MLflow UI to see which performs better on the Iris dataset.

## Setup

### 1. Create project structure

```bash
# Create a new folder for your project
mkdir mlflow-iris-project

# Go into that folder
cd mlflow-iris-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install mlflow scikit-learn

# Verify installation
mlflow --version
```

### 2. Create the training script

Create a file named `train.py`:

```python
import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Start MLflow run
mlflow.set_experiment("Iris_Project")

with mlflow.start_run():
    # 1. Log parameter
    mlflow.log_param("n_estimators", 1)
    
    # Train model
    model = RandomForestClassifier(n_estimators=1)
    model.fit(X_train, y_train)
    
    # 2. Log metric
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    
    # 3. Log model
    mlflow.sklearn.log_model(model, "my_model")
    
    print(f"Accuracy: {accuracy}")
    print("Done! Check MLflow UI")
```

### 3. Run experiments

**Terminal 1** - Start MLflow UI:
```bash
mlflow ui
```

**Terminal 2** - Run training script:
```bash
python train.py
```

Open your browser and navigate to: `http://localhost:5000`

### 4. Second experiment (with n_estimators=2)

Update the `n_estimators` parameter in `train.py` from `1` to `2`:

```python
# Change this line from 1 to 2
mlflow.log_param("n_estimators", 2)

# And update the model
model = RandomForestClassifier(n_estimators=2)
```

Run the script again:
```bash
python train.py
```

## Complete code for both experiments

### Experiment 1: n_estimators = 1

```python
import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Start MLflow run
mlflow.set_experiment("Iris_Project")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 1)
    model = RandomForestClassifier(n_estimators=1)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "my_model")
    
    print(f"Accuracy: {accuracy}")
```

### Experiment 2: n_estimators = 2

```python
import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Start MLflow run
mlflow.set_experiment("Iris_Project")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 2)
    model = RandomForestClassifier(n_estimators=2)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "my_model")
    
    print(f"Accuracy: {accuracy}")
```

## Results

After running both experiments, open the MLflow UI (`http://localhost:5000`) to:

- Compare accuracy metrics between runs
- View logged parameters (`n_estimators`)
- Download saved models
- Visualize experiment history

