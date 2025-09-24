import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(reference_csv, output_csv=None, num_rows=200, inject_anomalies=True):
    df = pd.read_csv(reference_csv)
    axis_cols = [col for col in df.columns if "Axis" in col]

    synthetic = pd.DataFrame(columns=["Trait"] + axis_cols + ["Time"])

    start_time = datetime.now()

    for i in range(num_rows):
        row = {"Trait": "current"}
        for col in axis_cols:
            original_mean = df[col].mean()
            original_std = df[col].std()

            new_mean = original_mean + np.random.uniform(1.0, 3.0)
            new_std = original_std * np.random.uniform(1.2, 1.8)
            value = np.random.normal(loc=new_mean, scale=new_std)

            # Inject anomalies
            if inject_anomalies:
                if np.random.rand() < 0.02:  # ~2% chance of spike
                    value += np.random.uniform(5.0, 10.0)
                elif np.random.rand() < 0.02:  # ~2% chance of drop
                    value -= np.random.uniform(5.0, 10.0)
                elif 50 <= i < 60:  # drift window
                    value += (i - 50) * 0.5

            row[col] = round(value, 2)

        row["Time"] = (start_time + timedelta(seconds=i * 2)).isoformat()
        synthetic.loc[i] = row

    # Save to CSV if path is provided
    if output_csv:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        synthetic.to_csv(output_csv, index=False)
        print(f"✅ Synthetic data with anomalies saved to {output_csv}")

    return synthetic


def generate_synthetic_data_old(reference_csv, output_csv, num_rows=200, inject_anomalies=True):
    df = pd.read_csv(reference_csv)
    axis_cols = [col for col in df.columns if "Axis" in col]

    synthetic = pd.DataFrame()
    for col in axis_cols:
        original_mean = df[col].mean()
        original_std = df[col].std()

        new_mean = original_mean + np.random.uniform(1.0, 3.0)
        new_std = original_std * np.random.uniform(1.2, 1.8)

        values = np.random.normal(loc=new_mean, scale=new_std, size=num_rows)

        if inject_anomalies:
            spike_indices = np.random.choice(num_rows, size=3, replace=False)
            values[spike_indices] += np.random.uniform(5.0, 10.0)

            drop_indices = np.random.choice(num_rows, size=3, replace=False)
            values[drop_indices] -= np.random.uniform(5.0, 10.0)

            drift_start = np.random.randint(50, 150)
            drift = np.linspace(0, 5, 10)
            values[drift_start:drift_start+10] += drift

        synthetic[col] = values

    synthetic["Time"] = np.arange(num_rows)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    synthetic.to_csv(output_csv, index=False)
    print(f"✅ Synthetic data with anomalies saved to {output_csv}")
    return synthetic