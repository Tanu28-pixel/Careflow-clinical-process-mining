
import pandas as pd
from pathlib import Path

# Locate the project data
project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "raw_event_logs.csv"

df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

# 1. Activity frequency
activity_counts = (
    df.groupby("Activity_Name")
    .agg(
        total_events=("Case_ID", "size"),
        unique_patients=("Case_ID", "nunique")
    )
    .sort_values("total_events", ascending=False)
)

# 2. Time between consecutive activities
df = df.sort_values(["Case_ID", "Timestamp"])
df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)

df["Minutes_To_Next"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

waiting_times = df.dropna(subset=["Minutes_To_Next"])

# 3. Summary
print("\n=== ACTIVITY FREQUENCY ===")
print(activity_counts)

print("\n=== WAITING-TIME SUMMARY (MINUTES) ===")
print(waiting_times["Minutes_To_Next"].describe())

print("\n=== LONGEST GAPS BETWEEN ACTIVITIES ===")
print(
    waiting_times[
        ["Case_ID", "Activity_Name", "Next_Activity", "Minutes_To_Next"]
    ]
    .sort_values("Minutes_To_Next", ascending=False)
    .head(10)
    .to_string(index=False)
)

# 4. Save outputs
output_dir = project_dir / "data"
activity_counts.to_csv(output_dir / "activity_frequency_summary.csv")
waiting_times.to_csv(output_dir / "waiting_time_analysis.csv", index=False)

print("\nAnalysis complete! Results saved in the data folder.")
