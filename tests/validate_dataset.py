
from pathlib import Path
import pandas as pd
import json

# Project directories
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "raw"
OUTPUT_DIR = ROOT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXPECTED_FILES = [
    "customers.csv",
    "delivery_events.csv",
    "driver_monthly_metrics.csv",
    "drivers.csv",
    "facilities.csv",
    "fuel_purchases.csv",
    "loads.csv",
    "maintenance_records.csv",
    "routes.csv",
    "safety_incidents.csv",
    "trailers.csv",
    "trips.csv",
    "truck_utilization_metrics.csv",
    "trucks.csv"
]

print("=" * 60)
print("ECOFLEET - DATASET VALIDATION")
print("=" * 60)

# Verify that all required files exist
missing_files = [
    name for name in EXPECTED_FILES
    if not (DATA_DIR / name).is_file()
]

if missing_files:
    print("Missing files:", missing_files)
    raise SystemExit(1)

print("All 14 required CSV files are present.")

report = []
total_rows = 0

# Analyze each CSV file
for filename in EXPECTED_FILES:

    df = pd.read_csv(DATA_DIR / filename)

    rows = len(df)
    columns = len(df.columns)
    duplicates = int(df.duplicated().sum())
    missing = df.isnull().sum()

    total_rows += rows

    print("\n" + "-" * 60)
    print(f"Table: {filename}")
    print(f"Rows: {rows:,}")
    print(f"Columns: {columns}")
    print(f"Duplicate rows: {duplicates}")

    print("\nColumn names:")
    print(list(df.columns))

    print("\nMissing values:")

    if missing.sum() == 0:
        print("No missing values.")
    else:
        print(missing[missing > 0].to_string())

    report.append({
        "table": filename,
        "rows": rows,
        "columns": columns,
        "column_names": list(df.columns),
        "data_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        },
        "duplicate_rows": duplicates,
        "missing_values": {
            col: int(value)
            for col, value in missing.items()
            if value > 0
        }
    })

# Generate a JSON quality report
output_file = OUTPUT_DIR / "dataset_quality_report.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump({
        "total_tables": len(report),
        "total_rows": total_rows,
        "tables": report
    }, file, indent=4)

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Total tables: {len(report)}")
print(f"Total records: {total_rows:,}")
print(f"Quality report: {output_file}")

print("\nDataset inspection completed successfully.")
