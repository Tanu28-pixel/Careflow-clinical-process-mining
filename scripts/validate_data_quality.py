
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw_event_logs.csv"

df = pd.read_csv(file_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce", utc=True)

print("=== DATA QUALITY REPORT ===")
print("Total rows:", len(df))
print("Missing values:\n", df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Unique patient cases:", df["Case_ID"].nunique())
print("Unique activities:", df["Activity_Name"].nunique())
print("Invalid timestamps:", df["Timestamp"].isna().sum())
print("Missing patient IDs:", df["Case_ID"].isna().sum())
print("Missing activity names:", df["Activity_Name"].isna().sum())

valid_activities = {
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Lab Test",
    "Treatment",
    "Discharge"
}

unexpected = sorted(
    set(df["Activity_Name"].dropna()) - valid_activities
)
print("Unexpected activities:", unexpected)

print("\nValidation check complete.")
