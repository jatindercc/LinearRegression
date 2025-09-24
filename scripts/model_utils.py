from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def train_regression_models(df):
    models = {}
    for col in df.columns:
        if "Axis" in col:
            x = np.arange(len(df)).reshape(-1, 1)
            y = df[col].values
            model = LinearRegression().fit(x, y)
            models[col] = model
            print(f"✅ {col}: Slope={model.coef_[0]:.4f}, Intercept={model.intercept_:.4f}")
    return models

def analyze_residuals(df, models):
    thresholds = {}
    for col in df.columns:
        if "Axis" in col and col in models:
            x = np.arange(len(df)).reshape(-1, 1)
            y = df[col].values
            y_pred = models[col].predict(x)
            residuals = y - y_pred

            min_c = np.min(y)
            max_c = np.max(y)
            t = np.std(residuals) * 2

            thresholds[col] = {"MinC": min_c, "MaxC": max_c, "T": t}
            print(f"🔧 {col}: MinC={min_c:.2f}, MaxC={max_c:.2f}, T={t:.2f}")
    return thresholds

def detect_anomalies(df, models, thresholds):
    alerts, errors = [], []
    for i, row in df.iterrows():
        for col in df.columns:
            if "Axis" in col:
                val = row[col]
                if pd.isnull(val): continue
                t = thresholds[col]["T"]
                min_c = thresholds[col]["MinC"]
                max_c = thresholds[col]["MaxC"]
                if val < min_c or val > max_c:
                    errors.append({"index": i, "value": val, "axis": col})
                elif val > t:
                    alerts.append({"index": i, "value": val, "axis": col})
    return alerts, errors