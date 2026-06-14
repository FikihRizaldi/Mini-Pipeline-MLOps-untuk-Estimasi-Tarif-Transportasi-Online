from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocessing import (
    build_preprocessor,
    clean_cab_rides,
    create_time_features,
    get_feature_target,
    load_raw_data,
)


def train_test_split_data(X, y, test_size=0.2, random_state=42):
    """Bagi data train/test."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_baseline_models(
    preprocessor,
    X_train,
    y_train,
    random_state=42,
    rf_sample_size=100_000,
):
    """Latih model regresi."""
    model_specs = {
        "Dummy Regressor": DummyRegressor(strategy="mean"),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=50,
            max_depth=15,
            random_state=random_state,
            n_jobs=-1,
        ),
    }

    trained_models = {}
    for model_name, estimator in model_specs.items():
        model_pipeline = Pipeline(
            steps=[
                ("preprocessor", clone(preprocessor)),
                ("model", estimator),
            ]
        )

        if model_name == "Random Forest Regressor" and len(X_train) > rf_sample_size:
            X_fit, _, y_fit, _ = train_test_split(
                X_train,
                y_train,
                train_size=rf_sample_size,
                random_state=random_state,
            )
        else:
            X_fit = X_train
            y_fit = y_train

        model_pipeline.fit(X_fit, y_fit)
        trained_models[model_name] = model_pipeline

    return trained_models


def evaluate_model(model, X_test, y_test):
    """Evaluasi metrik (MAE, RMSE, R2)."""
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2,
    }


def save_model(model, path):
    """Simpan model."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def main():
    project_root = Path(__file__).resolve().parents[1]
    raw_path = project_root / "data" / "raw" / "cab_rides.csv"
    processed_path = project_root / "data" / "processed" / "cleaned_cab_rides.csv"
    model_path = project_root / "models" / "baseline_price_model.joblib"

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    cab_rides = load_raw_data(raw_path)
    rows_before_cleaning = len(cab_rides)

    cleaned_cab_rides = clean_cab_rides(cab_rides)
    cleaned_cab_rides.to_csv(processed_path, index=False)
    rows_after_cleaning = len(cleaned_cab_rides)

    model_data = create_time_features(cleaned_cab_rides)
    X, y, feature_columns, numeric_features, categorical_features = get_feature_target(
        model_data,
        include_surge=False,
    )

    X_train, X_test, y_train, y_test = train_test_split_data(X, y)
    preprocessor = build_preprocessor(numeric_features, categorical_features)
    trained_models = train_baseline_models(preprocessor, X_train, y_train)

    results = []
    for model_name, model in trained_models.items():
        metrics = evaluate_model(model, X_test, y_test)
        results.append({"Model": model_name, **metrics})

    results_df = pd.DataFrame(results).sort_values("MAE").reset_index(drop=True)
    best_model_name = results_df.loc[0, "Model"]
    best_model = trained_models[best_model_name]
    save_model(best_model, model_path)

    print("Training selesai.")
    print(f"Baris sblm cleaning: {rows_before_cleaning:,}")
    print(f"Baris stlh cleaning: {rows_after_cleaning:,}")
    print(f"Fitur: {feature_columns}")
    print(f"Model terbaik: {best_model_name}")
    print(f"Lokasi model: {model_path}")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    main()
