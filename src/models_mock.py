import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

import mlflow
import mlflow.sklearn

# Create synthetic regression data
X, y = make_regression(n_samples=100, n_features=2, noise=0.1, random_state=42)

# Define and train regression models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree Regressor": DecisionTreeRegressor(),
    "Random Forest Regressor": RandomForestRegressor(),
    "XGBoost Regressor": XGBRegressor(),
}

# Save models using MLflow
mlflow.set_tracking_uri("sqlite:///src/models/mlflow.db")
for model_name, model in models.items():
    with mlflow.start_run() as run:
        model.fit(X, y)
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_params({"model_name": model_name})
