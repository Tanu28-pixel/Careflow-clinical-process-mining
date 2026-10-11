
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

# Check required columns
required_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing_columns = [
    col for col in required_columns if col not in df.columns
]
print("Missing required columns:", missing_columns)

# Check chronological order within each patient
ordered_df = df.sort_values(["Case_ID", "Timestamp"])
time_differences = ordered_df.groupby("Case_ID")["Timestamp"].diff()

out_of_order = (time_differences < pd.Timedelta(0)).sum()
print("Chronological ordering violations:", out_of_order)

# Check whether any patient IDs are blank
blank_patient_ids = (
    df["Case_ID"].isna()
    | df["Case_ID"].astype(str).str.strip().eq("")
).sum()
print("Blank patient IDs:", blank_patient_ids)
