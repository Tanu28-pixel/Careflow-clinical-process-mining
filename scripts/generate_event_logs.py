
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

activities = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Lab Test",
    "Treatment",
    "Discharge"
]

records = []
start_date = datetime(2026, 1, 1, 8, 0)

for patient_num in range(1, 201):
    case_id = f"P{patient_num:03d}"
    current_time = start_date + timedelta(
        minutes=random.randint(0, 1440 * 30)
    )

    # Every patient begins with registration and triage
    journey = ["Registration", "Triage", "Doctor Consultation"]

    # Some patients return to triage after X-Ray
    if random.random() < 0.30:
        journey += ["X-Ray", "Triage", "Doctor Consultation"]
    elif random.random() < 0.50:
        journey += ["X-Ray"]

    # Some patients require a lab test
    if random.random() < 0.60:
        journey.append("Lab Test")

    journey += ["Treatment", "Discharge"]

    for activity in journey:
        records.append({
            "Case_ID": case_id,
            "Activity_Name": activity,
            "Timestamp": current_time
        })

        # Simulate different waiting periods
        current_time += timedelta(
            minutes=random.randint(10, 120)
        )

df = pd.DataFrame(records)

# Sort events chronologically within each patient case
df = df.sort_values(
    ["Case_ID", "Timestamp"]
).reset_index(drop=True)

# Save CSV inside the project's data folder
output_path = Path(__file__).resolve().parent.parent / "data"
output_path.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path / "raw_event_logs.csv", index=False)

print("Event log generated successfully!")
print("Total events:", len(df))
print("Total patient cases:", df["Case_ID"].nunique())
print(df.head(10))