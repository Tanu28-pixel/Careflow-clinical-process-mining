
import pandas as pd
from pathlib import Path

# Locate the project and raw event log
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw_event_logs.csv"

required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

valid_activities = {
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Lab Test",
    "Treatment",
    "Discharge",
}

print("=== CAREFLOW DATA QUALITY REPORT ===")

# Check file existence
if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")

df = pd.read_csv(file_path)

# Check required columns before further validation
missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

print("Total rows:", len(df))
print("Missing required columns:", missing_columns)

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

# Check blank values in required fields
for column in required_columns:
    df[column] = df[column].astype("string").str.strip()
    df[column] = df[column].replace("", pd.NA)

print("\nMissing values:")
print(df[required_columns].isna().sum())

# Check duplicate records
print("\nDuplicate rows:", df.duplicated().sum())

# Check patient IDs
print("Unique patient cases:", df["Case_ID"].nunique())
print("Missing or blank patient IDs:", df["Case_ID"].isna().sum())

# Check activity names
print("Unique activities:", df["Activity_Name"].nunique())
print("Missing or blank activity names:", df["Activity_Name"].isna().sum())

unexpected_activities = sorted(
    set(df["Activity_Name"].dropna()) - valid_activities
)
print("Unexpected activities:", unexpected_activities)

# Parse timestamps and identify invalid values
timestamps = pd.to_datetime(df["Timestamp"], errors="coerce", utc=True)
invalid_timestamps = timestamps.isna()
print("Invalid timestamps:", int(invalid_timestamps.sum()))

# Check chronological ordering within each patient
check_df = df[["Case_ID"]].copy()
check_df["Timestamp"] = timestamps

valid_rows = check_df.dropna(
    subset=["Case_ID", "Timestamp"]
).sort_values(["Case_ID", "Timestamp"], kind="stable")

# Compare original row order within each patient to timestamp order
original_valid = check_df.dropna(
    subset=["Case_ID", "Timestamp"]
).copy()

ordering_violations = 0
for _, group in original_valid.groupby("Case_ID", sort=False):
    values = group["Timestamp"]
    ordering_violations += int((values.diff().dropna() < pd.Timedelta(0)).sum())

print("Chronological ordering violations:", ordering_violations)

# Summary
checks_passed = (
    len(df) > 0
    and not missing_columns
    and df[required_columns].isna().sum().sum() == 0
    and df.duplicated().sum() == 0
    and len(unexpected_activities) == 0
    and invalid_timestamps.sum() == 0
    and ordering_violations == 0
)

print("\n=== FINAL RESULT ===")
print("PASS: All data quality checks passed." if checks_passed
      else "WARNING: Data quality issues were found.")

if not checks_passed:
    raise SystemExit(1)

