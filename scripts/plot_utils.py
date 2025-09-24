import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import numpy as np
import os
import pandas as pd

def plot_axis_individual(df, models, alerts, errors, axis_cols):

    os.makedirs("plots", exist_ok=True)
    for col in axis_cols:
        if col not in models:
            continue

        x = np.arange(len(df))
        if len(x) == 0:
            print(f"⏳ Skipping plot for {col} — no data yet.")
            continue
        y = df[col].values
        y_pred = models[col].predict(x.reshape(-1, 1))

        plt.figure(figsize=(10, 4))
        plt.plot(x, y, label="Actual", alpha=0.6)
        plt.plot(x, y_pred, label="Regression", linestyle='--')

        for alert in alerts:
            if alert["axis"] == col:
                plt.scatter(alert["index"], alert["value"], color='orange', marker='x', label="Alert")

        for error in errors:
            if error["axis"] == col:
                plt.scatter(error["index"], error["value"], color='red', marker='s', label="Error")

        
        # Add summary text in top-left corner
        slope = models[col].coef_[0]
        intercept = models[col].intercept_
        num_alerts = sum(1 for a in alerts if a["axis"] == col)
        num_errors = sum(1 for e in errors if e["axis"] == col)

        summary_text = (
            f"Slope: {slope:.2f}\n"
            f"Intercept: {intercept:.2f}\n"
            f"Alerts: {num_alerts}\n"
            f"Errors: {num_errors}"
        )

        plt.text(0.01, 0.95, summary_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

        plt.title(f"{col} — Current vs Regression")
        plt.xlabel("Time")
        plt.ylabel("Current (Amps)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"plots/{col}_plot.png")
        plt.show()

def plot_stream_with_regression(df, models, alerts=None, errors=None):
    """
    Live visualization of streaming data with regression predictions, actual values,
    residual shading, and anomaly markers.
    """
    clear_output(wait=True)
    plt.figure(figsize=(14, 6))

    # Identify axis columns
    axis_cols = [col for col in df.columns if "Axis" in col]

    # Time labels (relative index for streaming window)
    time_labels = list(range(-(len(df) - 1), 1))

    # --- Plot actual current values ---
    for col in axis_cols:
        plt.plot(time_labels, df[col].values, label=f"{col} (actual)", alpha=0.6)

    # --- Plot regression predictions + residual shading ---
    for col in axis_cols:
        if col in models:
            preds = models[col].predict(df[axis_cols])  # predict using trained model
            plt.plot(time_labels, preds, linestyle="--", label=f"{col} (regression)", alpha=0.8)

            # Residual shading (difference between actual and predicted)
            plt.fill_between(
                time_labels,
                df[col].values,
                preds,
                color="gray",
                alpha=0.2
            )

    # --- Overlay alerts ---
    if alerts:
        alert_x = [-len(df) + alert['index'] for alert in alerts]
        alert_y = [df.loc[alert['index'], alert['axis']] for alert in alerts]
        plt.scatter(alert_x, alert_y, color='orange', marker='x', s=80, label='Alert')

    # --- Overlay errors ---
    if errors:
        error_x = [-len(df) + error['index'] for error in errors]
        error_y = [df.loc[error['index'], error['axis']] for error in errors]
        plt.scatter(error_x, error_y, color='red', marker='s', s=80, label='Error')

    # --- Styling ---
    plt.title("Realtime Current with Regression, Residuals & Anomalies", fontsize=14)
    plt.xlabel("Time (seconds ago)", fontsize=12)
    plt.ylabel("Current (Amps)", fontsize=12)
    plt.ylim(0, 60)
    plt.legend(loc="upper left", fontsize=9, ncol=2)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    display(plt.gcf())
    plt.close()


def plot_stream_combined_with_summary(df, alerts, errors):
    from IPython.display import clear_output, display
    import matplotlib.pyplot as plt

    clear_output(wait=True)
    plt.figure(figsize=(14, 6))

    # Extract axis columns and clean numeric data
    axis_cols = [col for col in df.columns if "Axis" in col]
    numeric_df = df[axis_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Time labels: seconds ago, relative to current window
    time_labels = list(range(-(len(numeric_df) - 1), 1))
    plt.stackplot(time_labels, numeric_df.T.values, labels=axis_cols, alpha=0.6)

    # Map actual alert/error indices to relative positions in the current window
    index_map = {abs_idx: rel_idx for rel_idx, abs_idx in enumerate(df.index)}

    # Overlay alerts at peak value
    if alerts:
        alert_x = [-len(df) + alert['index'] for alert in alerts]
        #alert_y = [df.loc[alert['index'], alert['axis']] for alert in alerts]
        alert_y = [df.loc[alert['index'], axis_cols].max() for alert in alerts]
        plt.scatter(alert_x, alert_y, color='orange', marker='x', label='Alert')

    # Overlay errors at peak value
    if errors:
        error_x = [-len(df) + error['index'] for error in errors]
        #error_y = [max(df.loc[error['index'], axis_cols]) for error in errors]
        error_y = [df.loc[error['index'], axis_cols].max() for error in errors]
        plt.scatter(error_x, error_y, color='red', marker='s', label='Error')


    # Title and labels
    plt.title("Realtime Current (Amps, stacked)", fontsize=14)
    plt.xlabel("Time (seconds ago)", fontsize=12)
    plt.ylabel("Current (Amps)", fontsize=12)
    plt.ylim(0, 60)
    plt.legend(loc="upper left", fontsize=9, ncol=2)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    display(plt.gcf())
    plt.close()

def plot_stream_combined_with_summary_old(df, alerts, errors):
    
    clear_output(wait=True)
    plt.figure(figsize=(14, 6))

    # Extract axis columns and clean numeric data
    axis_cols = [col for col in df.columns if "Axis" in col]
    numeric_df = df[axis_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Time labels: seconds ago, relative to current window
    time_labels = list(range(-(len(numeric_df) - 1), 1))

    # Stacked area chart
    plt.stackplot(time_labels, numeric_df.T.values, labels=axis_cols, alpha=0.6)

    # Overlay alerts
    if alerts:
        alert_x = [-len(df) + alert['index'] for alert in alerts]
        alert_y = [alert['value'] for alert in alerts]
        plt.scatter(alert_x, alert_y, color='orange', marker='x', label='Alert')

    # Overlay errors
    if errors:
        error_x = [-len(df) + error['index'] for error in errors]
        error_y = [error['value'] for error in errors]
        plt.scatter(error_x, error_y, color='red', marker='s', label='Error')

    # Title and labels
    plt.title("Realtime Current (Amps, stacked)", fontsize=14)
    plt.xlabel("Time (seconds ago)", fontsize=12)
    plt.ylabel("Current (Amps)", fontsize=12)
    plt.ylim(0, 60)
    plt.legend(loc="upper left", fontsize=9, ncol=2)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    display(plt.gcf())
    plt.close()
