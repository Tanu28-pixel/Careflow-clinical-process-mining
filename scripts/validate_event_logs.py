
import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / "data" / "raw_event_logs.csv"
df = pd.read_csv(file_path)

print("Dataset shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique activities:")
print(df["Activity_Name"].unique())

print("\nEvents per patient:")
print(df.groupby("Case_ID").size().describe())

print("\nDuplicate rows:", df.duplicated().sum())