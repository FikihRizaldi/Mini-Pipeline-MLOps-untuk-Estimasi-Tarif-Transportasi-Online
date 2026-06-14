import pandas as pd


REQUIRED_COLUMNS = [
    "price",
    "distance",
    "cab_type",
    "source",
    "destination",
    "name",
    "time_stamp",
]

CATEGORICAL_COLUMNS = ["source", "destination", "cab_type", "name"]


def _result(check_name, rule, failed_rows, status, recommendation):
    return {
        "Check Name": check_name,
        "Rule": rule,
        "Failed Rows": int(failed_rows),
        "Status": status,
        "Recommendation": recommendation,
    }


def validate_required_columns(df, required_columns):
    missing_columns = [column for column in required_columns if column not in df.columns]
    failed_rows = len(df) if missing_columns else 0
    status = "FAIL" if missing_columns else "PASS"
    recommendation = (
        f"Tambah kolom: {missing_columns}."
        if missing_columns
        else "Kolom lengkap."
    )
    return _result(
        "Kolom wajib",
        f"Wajib: {', '.join(required_columns)}",
        failed_rows,
        status,
        recommendation,
    )


def validate_no_missing_target(df, target_column="price"):
    if target_column not in df.columns:
        return _result(
            "Target price",
            f"Kolom '{target_column}' harus ada",
            len(df),
            "FAIL",
            "Tambah kolom target.",
        )

    failed_rows = df[target_column].isna().sum()
    status = "FAIL" if failed_rows > 0 else "PASS"
    recommendation = (
        "Hapus baris null."
        if failed_rows > 0
        else "Target valid."
    )
    return _result(
        "Target price",
        "Target 'price' tidak boleh null",
        failed_rows,
        status,
        recommendation,
    )


def validate_positive_distance(df):
    if "distance" not in df.columns:
        return _result(
            "distance > 0",
            "Kolom 'distance' harus > 0",
            len(df),
            "FAIL",
            "Perbaiki kolom distance.",
        )

    failed_rows = (df["distance"] <= 0).sum()
    status = "FAIL" if failed_rows > 0 else "PASS"
    recommendation = (
        "Hapus distance <= 0."
        if failed_rows > 0
        else "Distance valid."
    )
    return _result("distance > 0", "distance harus > 0", failed_rows, status, recommendation)


def validate_positive_price(df):
    if "price" not in df.columns:
        return _result(
            "price > 0",
            "Kolom 'price' harus > 0",
            len(df),
            "FAIL",
            "Perbaiki kolom price.",
        )

    failed_rows = (df["price"] <= 0).sum()
    status = "FAIL" if failed_rows > 0 else "PASS"
    recommendation = (
        "Hapus price <= 0."
        if failed_rows > 0
        else "Price valid."
    )
    return _result("price > 0", "price harus > 0", failed_rows, status, recommendation)


def validate_no_missing_categorical_columns(df, categorical_columns):
    results = []
    for column in categorical_columns:
        if column not in df.columns:
            results.append(
                _result(
                    f"{column} tidak null",
                    f"Kolom '{column}' tidak boleh null",
                    len(df),
                    "FAIL",
                    f"Perbaiki kolom {column}.",
                )
            )
            continue

        failed_rows = df[column].isna().sum()
        status = "FAIL" if failed_rows > 0 else "PASS"
        recommendation = (
            f"Hapus null di {column}."
            if failed_rows > 0
            else f"{column} valid."
        )
        results.append(
            _result(
                f"{column} tidak null",
                f"Kolom '{column}' tidak boleh null",
                failed_rows,
                status,
                recommendation,
            )
        )
    return results


def validate_timestamp_convertible(df, timestamp_column="time_stamp"):
    if timestamp_column not in df.columns:
        return _result(
            "time_stamp valid datetime",
            f"Kolom '{timestamp_column}' harus bisa dikonversi ke datetime",
            len(df),
            "FAIL",
            "Perbaiki kolom timestamp.",
        )

    converted = pd.to_datetime(df[timestamp_column], unit="ms", errors="coerce")
    failed_rows = converted.isna().sum()
    status = "FAIL" if failed_rows > 0 else "PASS"
    recommendation = (
        "Hapus timestamp tidak valid."
        if failed_rows > 0
        else "Timestamp valid."
    )
    return _result(
        "time_stamp valid datetime",
        "time_stamp harus valid konversi pd.to_datetime",
        failed_rows,
        status,
        recommendation,
    )


def validate_no_exact_duplicate_rows(df):
    failed_rows = df.duplicated().sum()
    status = "WARNING" if failed_rows > 0 else "PASS"
    recommendation = (
        "Hapus baris duplikat."
        if failed_rows > 0
        else "Tidak ada duplikat."
    )
    return _result(
        "Tidak ada baris duplikat",
        "Data tidak boleh ada duplikat persis",
        failed_rows,
        status,
        recommendation,
    )


def run_all_validations(df):
    results = [
        validate_required_columns(df, REQUIRED_COLUMNS),
        validate_no_missing_target(df, target_column="price"),
        validate_positive_distance(df),
        validate_positive_price(df),
        validate_timestamp_convertible(df, timestamp_column="time_stamp"),
        validate_no_exact_duplicate_rows(df),
    ]
    results.extend(validate_no_missing_categorical_columns(df, CATEGORICAL_COLUMNS))

    column_order = ["Check Name", "Rule", "Failed Rows", "Status", "Recommendation"]
    return pd.DataFrame(results, columns=column_order)
