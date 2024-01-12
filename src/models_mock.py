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

# Loop through models and log runs with detailed information
for model_name, model in models.items():
    with mlflow.start_run() as run:
        # Set the experiment name directly in the run
        experiment_name = "_".join(model_name.split())
        mlflow.set_experiment(f"{experiment_name}_experiment")

        # Train the model
        model.fit(X, y)

        # Log the model
        mlflow.sklearn.log_model(model, "model")

        # Log parameters
        mlflow.log_params(
            {"model_name": model_name, "n_samples": 100, "n_features": 2, "noise": 0.1}
        )

        # Evaluate the model (example metrics)
        y_pred = model.predict(X)
        mse = np.mean((y_pred - y) ** 2)
        rmse = np.sqrt(mse)
        r_squared = 1 - (mse / np.var(y))

        # Log metrics
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("root_mean_squared_error", rmse)
        mlflow.log_metric("r_squared", r_squared)
