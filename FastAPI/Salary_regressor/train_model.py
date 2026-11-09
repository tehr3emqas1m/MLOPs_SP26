
# train_model.py
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

df = pd.read_csv("salary_full.csv")
X = df[["experience"]]
y = df["salary"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("Saved model.pkl")