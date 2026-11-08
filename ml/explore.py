from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
csv = next(DATA_DIR.glob("*.csv"))
df = pd.read_csv(csv)

print(f"file: {csv.name}")
print(f"rows: {len(df):,}")
print(f"columns: {list(df.columns)}")
print(f"fraud rate: {df['isFraud'].mean():.4%}")

print("\ntransactions by type:")
print(df["type"].value_counts())

print("\nfraud by type (count, rate):")
print(df.groupby("type")["isFraud"].agg(["sum", "mean"]))

print(f"\nunique senders:   {df['nameOrig'].nunique():,}")
print(f"unique receivers: {df['nameDest'].nunique():,}")
