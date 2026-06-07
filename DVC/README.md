
[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-13ADC7?style=flat&logo=dvc)](https://dvc.org/)
[![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?style=flat&logo=git)](https://git-scm.com/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat&logo=python)](https://python.org/)


# Data Version Control (DVC)

**DVC (Data Version Control)** is an open-source tool that helps track and manage **datasets, machine learning models, and ML pipelines** in the same way Git tracks source code.

It stores large files (data/models) outside Git while keeping lightweight references to them inside the repository.

### Why is DVC Needed?

Git works well for code but struggles with:

* Large datasets
* Machine learning models
* Frequent changes to data files

DVC solves this by:

* **Versioning datasets and models** just like code.
* **Tracking experiments** and their results.
* **Enabling reproducibility**, so others can recreate the same training process.
* **Reducing repository size** by storing large files in remote storage (e.g., cloud storage, shared servers).
* **Facilitating team collaboration** on data-heavy projects.

### Example

Without DVC:

```text
Git → code only
dataset.csv (2 GB) → difficult to manage
```

With DVC:

```text
Git → code + dataset metadata
DVC → actual dataset storage and versioning


# DVC Example Project: Salary Prediction with Versioned Datasets

## Project Overview

This project demonstrates Data Version Control (DVC) by simulating a real-world scenario where a dataset grows incrementally over time. We create synthetic salary data based on years of experience and train linear regression models on progressively larger datasets.

### What You'll Learn

- Track datasets with DVC (not Git)
- Version large files efficiently
- Train models on different dataset versions
- Reproduce results across dataset versions
- Understand the difference between Git (code) and DVC (data)

### Dataset Evolution

| Version | Rows | Description |
|---------|------|-------------|
| v1 | 500 | Initial dataset |
| v2 | 1000 | Added 500 more rows |
| v3 | 1500 | Complete dataset |

## Project Structure

```
.
├── dataset.csv          # Tracked by DVC (not in Git)
├── dataset.csv.dvc      # DVC metadata file (in Git)
├── generate_salary_data.py
├── train.py
├── model.pkl            # Trained model (in Git or DVC)
└── .gitignore           # Ignores dataset.csv
```

## Step-by-Step Guide

### 1. Generate the Data

Run the script to create 1500 rows of synthetic salary data:

```python
# generate_salary_data.py
import pandas as pd
import numpy as np

np.random.seed(42)  # For reproducibility

# Generate 1500 rows
n_rows = 1500
experience = np.random.uniform(0, 15, n_rows)  # 0 to 15 years

# Base salary: 30,000 + 5,000 * experience + some noise
noise = np.random.normal(0, 5000, n_rows)
salary = 30000 + 5000 * experience + noise

# Add some outliers (higher salaries for some)
outlier_indices = np.random.choice(n_rows, 50, replace=False)
salary[outlier_indices] = salary[outlier_indices] + np.random.normal(15000, 5000, 50)

# Make salary never negative
salary = np.maximum(salary, 20000)

# Create DataFrame
df = pd.DataFrame({
    'experience': np.round(experience, 1),
    'salary': np.round(salary, -2)  # Round to nearest hundred
})

# Shuffle the data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save full dataset
df.to_csv('orig_data.csv', index=False)
print(f"Generated {len(df)} rows of salary data")
print(f"Experience range: {df['experience'].min()} to {df['experience'].max()} years")
print(f"Salary range: ${df['salary'].min():,.0f} to ${df['salary'].max():,.0f}")
print(f"First 5 rows:\n{df.head()}")
```

Now extract the first 500 rows as `dataset.csv`:

```python
import pandas as pd
df = pd.read_csv('orig_data.csv')
df.head(500).to_csv('dataset.csv', index=False)
```

### 2. Initialize Git and DVC

```bash
git init
dvc init
```

### 3. Track First Dataset with DVC

```bash
dvc add dataset.csv
ls -la
```

This creates:
- `dataset.csv.dvc` - the DVC metadata file
- `dataset.csv` is now tracked by DVC (not Git)
- `.gitignore` was updated to ignore the actual CSV file

### 4. Commit to Git

```bash
git add dataset.csv.dvc .gitignore
git status
git commit -m "v1: First 500 rows of salary dataset"
```

**Important notes:**
- Without `git add dataset.csv.dvc`, Git doesn't know DVC is tracking anything
- Without `.gitignore`, Git might accidentally track the actual CSV (DVC's job)

### 5. Create Training Script

```python
# train.py
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load the data
print("Loading dataset.csv...")
data = pd.read_csv('dataset.csv')
X = data[['experience']]
y = data['salary']

# Train model
print("Training linear regression model...")
model = LinearRegression()
model.fit(X, y)

# Make predictions and evaluate
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)

# Print results
print(f"\nResults for dataset (rows):")
print(f"Formula: salary = {model.coef_[0]:.2f} × experience + {model.intercept_:.2f}")
print(f"R² Score: {r2:.4f}")

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
print("\nModel saved as model.pkl")
```

### 6. Train First Model (v1)

```bash
python train.py
```

### 7. Commit First Model

```bash
git add train.py model.pkl
git commit -m "v1: Trained linear regression model on 500 rows"
git tag -a v1-model -m "Model trained on first 500 salary records"
git log --oneline
```

### 8. Add Next 500 Rows (Version 2)

Append rows 501-1000 to `dataset.csv`:

```python
import pandas as pd
orig = pd.read_csv('orig_data.csv')
df = pd.read_csv('dataset.csv')
combined = pd.concat([df, orig.iloc[500:1000]])
combined.to_csv('dataset.csv', index=False)
```

Update DVC tracking:

```bash
dvc status
git status
dvc add dataset.csv
```

### 9. Commit Version 2

```bash
git add dataset.csv.dvc
git commit -m "v2: Added next 500 rows (total 1000 rows)"
git tag v2-data
python train.py  # Retrain the model
```

### 10. Commit Updated Model

```bash
git add model.pkl
git commit -m "v2: Model retrained on 1000 rows"
git tag v2-model
```

### 11. View All Versions

```bash
git log --oneline
git tag
```

## Current State

At this stage you have:
- Git initialized
- DVC initialized  
- `dataset.csv` tracked by DVC
- `dataset.csv.dvc` and `.gitignore` committed to Git
- Multiple versions of both data and models tagged

## Homework Exercises

### Exercise 1: Complete the Dataset
Add the final 500 rows (1001-1500) and train the third model version.

**Tasks:**
1. Append rows 1001-1500 from `orig_data.csv` to `dataset.csv`
2. Update DVC tracking with `dvc add dataset.csv`
3. Commit the new data version as `v3-data`
4. Retrain the model with `python train.py`
5. Commit the new model as `v3-model`

### Exercise 2: Track Models with DVC

Repeat the entire project, but this time track `model.pkl` with DVC instead of Git.

**Steps:**
1. Instead of `git add model.pkl`, use `dvc add model.pkl`
2. Commit `model.pkl.dvc` to Git instead of the pickle file
3. Compare the repository size difference between tracking models with Git vs DVC

**Why this matters:** Large model files (hundreds of MB to GB) should NOT be stored in Git. DVC handles them efficiently, just like datasets.

## Key Takeaways

| File Type | Tracking Tool | Why |
|-----------|--------------|-----|
| Source code (.py) | Git | Small, text-based, needs version control |
| Small models (<10MB) | Git | Can be stored directly |
| Large models (>10MB) | DVC | Too big for Git |
| Datasets (any size) | DVC | Not code, often too large for Git |
| DVC metadata (.dvc) | Git | Small pointer files, track versions |

## Requirements

```
pandas
numpy
scikit-learn
dvc
```

Install with:

```bash
pip install pandas numpy scikit-learn dvc
```

## Additional Commands

```bash
# Check DVC status
dvc status

# View DVC tracked files
dvc list .

# Pull data from remote storage (if configured)
dvc pull

# Push data to remote storage
dvc push
```

## Remote Storage Setup (Optional)

To share DVC-tracked data across teams, configure remote storage:

```bash
dvc remote add -d myremote s3://my-bucket/dvc-store
dvc push
```

Other remote options: GCS, Azure, SSH, HDFS, local directory.
