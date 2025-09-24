# LinearRegression
Assignment 2: Streaming Data for Predictive Maintenance with Linear Regression-Based Alerts

## Name:        Jatinder Pal Singh
## Student ID:  9083762


# Final Project Report: Predictive Maintenance via Streaming Regression

# 🔍 Real-Time Anomaly Detection in Multiaxis Current Streams

This project simulates real-time monitoring of electrical current across multiple axes using regression-based anomaly detection. It visualizes streaming data, flags alerts and errors based on learned thresholds, and plots results dynamically for diagnostic insight.

---

## 📦 Project Overview

- **Goal**: Detect anomalies in multiaxis current data using regression models trained on historical patterns.
- **Data Source**: Synthetic and real CSV datasets streamed row-by-row from a Neon PostgreSQL database.
- **Detection Logic**: Alerts and errors are triggered when residuals exceed learned thresholds.
- **Visualization**: A stacked area chart displays current values over time, with alert/error markers plotted at peak values.

---

## ⚙️ Setup Instructions

### Clone the Repository
git clone [https://github.com/jatindercc/LinearRegression](https://github.com/jatindercc/LinearRegression.git)

### Synthetic Data
Synthetic test data was generated using the mean and standard deviation of training data. This allows testing the model’s robustness and anomaly detection logic.


### Regression & Alert Logic
- Model Training
- Each axis is modeled using linear regression against time and other axes.
- Residuals (actual - predicted) are calculated for each row.
### Threshold Discovery
- Residual distributions are analyzed to compute:
- Alert threshold: 95th percentile
- Error threshold: 99th percentile
### Anomaly Detection
- Alerts: Current > T
- Errors: Current > MaxC or < MinC
- Events are logged to CSV with timestamp, axis, and value
### Conclusion

This system demonstrates predictive maintenance using streaming regression, anomaly detection, and real-time visualization. It is scalable to multiple machines and adaptable to domain-specific thresholds.
