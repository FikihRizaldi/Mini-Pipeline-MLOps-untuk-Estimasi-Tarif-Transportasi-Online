from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(y_true, y_pred):
    """Hitung metrik regresi."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2,
        "Mean Actual Price": float(pd.Series(y_true).mean()),
        "Median Actual Price": float(pd.Series(y_true).median()),
    }


def create_prediction_result_dataframe(X_test, y_test, y_pred):
    """Gabung prediksi dan error."""
    result_df = X_test.copy()
    result_df["actual_price"] = pd.Series(y_test, index=X_test.index)
    result_df["predicted_price"] = y_pred
    result_df["error"] = result_df["actual_price"] - result_df["predicted_price"]
    result_df["absolute_error"] = result_df["error"].abs()
    return result_df


def evaluate_by_group(result_df, group_column):
    """Hitung metrik per grup."""
    if group_column not in result_df.columns:
        raise ValueError(f"Kolom '{group_column}' tidak tersedia untuk evaluasi grup.")

    group_table = (
        result_df.groupby(group_column, observed=True)
        .agg(
            row_count=("absolute_error", "size"),
            MAE=("absolute_error", "mean"),
            RMSE=("error", lambda values: np.sqrt(np.mean(np.square(values)))),
        )
        .reset_index()
        .sort_values("MAE", ascending=False)
    )
    return group_table


def create_ct_checklist(metrics, group_error_tables):
    """Buat checklist CT."""
    overall_mae = metrics["MAE"]
    overall_rmse = metrics["RMSE"]
    overall_r2 = metrics["R2 Score"]
    group_threshold = overall_mae * 1.5

    rows = [
        {
            "Check Name": "Cek threshold MAE",
            "Metric / Rule": "MAE <= 2.00",
            "Current Value": f"{overall_mae:.4f}",
            "Threshold": "2.00",
            "Status": "PASS" if overall_mae <= 2.00 else "WARNING",
            "Recommendation": "Monitor MAE.",
        },
        {
            "Check Name": "Cek threshold RMSE",
            "Metric / Rule": "RMSE <= 3.50",
            "Current Value": f"{overall_rmse:.4f}",
            "Threshold": "3.50",
            "Status": "PASS" if overall_rmse <= 3.50 else "WARNING",
            "Recommendation": "Cek error besar jika RMSE naik.",
        },
        {
            "Check Name": "Cek threshold R2 score",
            "Metric / Rule": "R2 Score >= 0.85",
            "Current Value": f"{overall_r2:.4f}",
            "Threshold": "0.85",
            "Status": "PASS" if overall_r2 >= 0.85 else "WARNING",
            "Recommendation": "Cek fitur/model jika R2 turun.",
        },
    ]

    group_names = {
        "distance_group": "Error per grup jarak",
        "cab_type": "Error per cab_type",
        "name": "Error per layanan",
    }

    for group_key, check_name in group_names.items():
        table = group_error_tables.get(group_key)
        if table is None or table.empty:
            rows.append(
                {
                    "Check Name": check_name,
                    "Metric / Rule": "Bisa direview",
                    "Current Value": "Tidak ada",
                    "Threshold": f"<= {group_threshold:.4f}",
                    "Status": "WARNING",
                    "Recommendation": "Buat tabel error.",
                }
            )
            continue

        max_group_mae = float(table["MAE"].max())
        status = "PASS" if max_group_mae <= group_threshold else "WARNING"
        rows.append(
            {
                "Check Name": check_name,
                "Metric / Rule": "MAE grup tidak boleh wajar",
                "Current Value": f"{max_group_mae:.4f}",
                "Threshold": f"<= {group_threshold:.4f}",
                "Status": status,
                "Recommendation": "Cek kualitas fitur.",
            }
        )

    rows.extend(
        [
            {
                "Check Name": "Review distribusi error",
                "Metric / Rule": "Review distribusi residual",
                "Current Value": "Direview di notebook",
                "Threshold": "Tidak ada pola aneh",
                "Status": "PASS",
                "Recommendation": "Lanjut cek plot.",
            },
            {
                "Check Name": "Robustness jarak pendek/jauh",
                "Metric / Rule": "Review per jarak",
                "Current Value": "Direview per grup",
                "Threshold": "MAE tidak wajar",
                "Status": "PASS",
                "Recommendation": "Lanjut cek per grup.",
            },
        ]
    )

    return pd.DataFrame(
        rows,
        columns=["Check Name", "Metric / Rule", "Current Value", "Threshold", "Status", "Recommendation"],
    )


def save_report(path, content):
    """Simpan laporan."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path
