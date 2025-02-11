# Electricity-Consumption
Overview

This project focuses on forecasting electricity demand using machine learning techniques. The goal is to develop a highly accurate predictive model that can help in energy consumption planning and resource allocation.

Dataset

The dataset contains historical electricity consumption data with features such as:

Usage: Electricity consumption

Date & Time Features: Extracted for trend analysis

Cyclic Encoding: Applied to time-based features


Approach

Data Preprocessing:

Missing value handling

Feature engineering (cyclic encoding, smoothing, rolling window features)

Train-test split

Time Series Baseline Model:

Implemented SARIMA for initial forecasting

Tuned (p, d, q) parameters using Auto-ARIMA

Evaluated using RMSE and MAPE

Machine Learning Models:

Implemented Random Forest and XGBoost for improved forecasting

Fine-tuned hyperparameters to enhance accuracy

Compared models based on RMSE and MAPE

Performance Evaluation:

Baseline SARIMA Model:

MAPE: X

RMSE: X

Tuned XGBoost Model:

MAPE: 4.09%

RMSE: 10.13

Tuned Random Forest Model:

MAPE: 4.01%

RMSE: 11.69

Results

XGBoost outperformed SARIMA and Random Forest in terms of MAPE and RMSE.

Predictions aligned well with actual demand trends.

Machine learning models proved to be more robust for forecasting.
