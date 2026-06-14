from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET_COLUMN = "price"
REQUIRED_CAB_COLUMNS = [
    "price",
    "distance",
    "cab_type",
    "source",
    "destination",
    "name",
    "time_stamp",
]

MAIN_FEATURES = [
    "distance",
    "cab_type",
    "source",
    "destination",
    "name",
    "hour",
    "day",
    "month",
    "day_of_week",
]

NUMERIC_FEATURES = ["distance", "hour", "day", "month", "day_of_week"]
CATEGORICAL_FEATURES = ["cab_type", "source", "destination", "name"]


def load_raw_data(path):
    """Load file CSV."""
    return pd.read_csv(Path(path))


def clean_cab_rides(df):
    """Bersihkan data."""
    missing_columns = [column for column in REQUIRED_CAB_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Kolom hilang: {missing_columns}")

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=["price"])
    cleaned = cleaned[cleaned["distance"] > 0]
    cleaned = cleaned[cleaned["price"] > 0]
    cleaned = cleaned.drop_duplicates()
    return cleaned.reset_index(drop=True)


def create_time_features(df):
    """Ubah timestamp ke fitur waktu."""
    if "time_stamp" not in df.columns:
        raise ValueError("Butuh kolom 'time_stamp'.")

    data = df.copy()
    data["datetime"] = pd.to_datetime(data["time_stamp"], unit="ms", errors="coerce")
    invalid_datetime_rows = int(data["datetime"].isna().sum())
    data.attrs["invalid_datetime_rows"] = invalid_datetime_rows

    if invalid_datetime_rows > 0:
        data = data.dropna(subset=["datetime"]).copy()

    data["hour"] = data["datetime"].dt.hour
    data["day"] = data["datetime"].dt.day
    data["month"] = data["datetime"].dt.month
    data["day_of_week"] = data["datetime"].dt.dayofweek
    return data.reset_index(drop=True)


def get_feature_target(df, include_surge=False):
    """Return X, y, dan list fitur."""
    data = df.copy()
    if not {"hour", "day", "month", "day_of_week"}.issubset(data.columns):
        data = create_time_features(data)

    feature_columns = MAIN_FEATURES.copy()
    numeric_features = NUMERIC_FEATURES.copy()
    categorical_features = CATEGORICAL_FEATURES.copy()

    if include_surge:
        feature_columns.append("surge_multiplier")
        numeric_features.append("surge_multiplier")

    required_columns = feature_columns + [TARGET_COLUMN]
    missing_columns = [column for column in required_columns if column not in data.columns]
    if missing_columns:
        raise ValueError(f"Kolom hilang: {missing_columns}")

    X = data[feature_columns].copy()
    y = data[TARGET_COLUMN].copy()
    return X, y, feature_columns, numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features, scale_numeric=True):
    """Buat preprocessor."""
    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"
    try:
        categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )
    return preprocessor
