import csv
import os
from datetime import datetime

def log_to_csv(events, path):
    file_exists = os.path.isfile(path)
    with open(path, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "index", "axis", "value"])
        if not file_exists:
            writer.writeheader()
        for e in events:
            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec='seconds'),
                "index": e["index"],
                "axis": e["axis"],
                "value": e["value"]
            })
    print(f"📄 Logged {len(events)} events to {path}")

def display_summary_stats(df, label):
    axis_cols = [col for col in df.columns if "Axis" in col]
    print(f"\n📊 Summary for {label}:")
    for col in axis_cols:
        mean = df[col].mean()
        std = df[col].std()
        print(f"{col}: Mean = {mean:.2f}, Std = {std:.2f}")