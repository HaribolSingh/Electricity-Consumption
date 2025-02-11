# -*- coding: utf-8 -*-
"""electricity_consumption_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aK50-oVxY24fuhJVtNOxg8RRR7afQ9Cp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/long_data_.csv")

df.head()

# Convert 'Dates' column to datetime format
# Convert 'Dates' column to datetime format
df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y %H:%M:%S') # Specify the correct format

# Check for missing values and duplicates
missing_values = df.isnull().sum()
duplicates = df.duplicated().sum()

# Display dataset info
print(df.info())

# Show missing values and duplicates
print("Missing Values:\n", missing_values)
print("Total Duplicates:", duplicates)

# Display duplicate rows
duplicates_df = df[df.duplicated()]
print(duplicates_df)

# Check for duplicate States + Dates combination
duplicate_entries = df[df.duplicated(subset=['States', 'Dates'], keep=False)]
print(duplicate_entries)

df_grouped = df.groupby(['States', 'Dates']).size().reset_index(name='Count')
df_grouped.sort_values(by='Count', ascending=False).head(10)  # Top 10 cases where multiple entries exist

# Aggregate by summing up Usage for each State per Date
df = df.groupby(['States', 'Dates'], as_index=False).agg({
    'Regions': 'first',  # Region same hoga toh pehla le lenge
    'latitude': 'first',  # Latitude constant rahega ek state ke liye
    'longitude': 'first',  # Longitude bhi same hoga
    'Usage': 'sum'  # Usage ka sum lenge (total consumption)
})

# Verify if duplicates are gone
df_grouped = df.groupby(['States', 'Dates']).size().reset_index(name='Count')
print(df_grouped['Count'].max())  # Should print 1 if all duplicates are resolved

from statsmodels.tsa.stattools import adfuller

result = adfuller(df['Usage'])
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

import matplotlib.pyplot as plt

# Convert 'Dates' column to datetime if not already
df['Dates'] = pd.to_datetime(df['Dates'])

# Sort by date
df = df.sort_values(by='Dates')

# Plot overall electricity usage trend
plt.figure(figsize=(12, 5))
plt.plot(df.groupby('Dates')['Usage'].sum(), label="Total Electricity Usage", color='b')
plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("Electricity Consumption Trend Over Time")
plt.legend()
plt.grid(True)
plt.show()

df[df['Dates'] > '2019-06-30'].head(100)

df['Usage_MA'] = df.groupby('Dates')['Usage'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())

plt.figure(figsize=(12, 5))
plt.plot(df.groupby('Dates')['Usage'].sum(), label="Raw Usage", alpha=0.5)
plt.plot(df.groupby('Dates')['Usage_MA'].sum(), label="7-day Moving Average", color='r')
plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("Electricity Consumption with 7-day Moving Average")
plt.legend()
plt.grid(True)
plt.show()

df_statewise = df.groupby(['Dates', 'States'])['Usage'].sum().unstack()

plt.figure(figsize=(12, 6))
df_statewise.plot(legend=False, alpha=0.5)
plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("State-wise Electricity Consumption Trends")
plt.show()

df['Month'] = df['Dates'].dt.to_period('M')  # Extract Year-Month

plt.figure(figsize=(12, 5))
df.groupby('Month')['Usage'].sum().plot(kind='bar', color='b', alpha=0.7)
plt.xlabel("Month")
plt.ylabel("Total Usage")
plt.title("Monthly Electricity Consumption Trend")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

df_statewise = df.groupby(['States'])['Usage'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 5))
df_statewise.plot(kind='bar', color='g', alpha=0.7)
plt.xlabel("State")
plt.ylabel("Total Usage")
plt.title("Top 10 States with Highest Electricity Consumption")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

import numpy as np

# Group by date to get daily total usage
daily_usage = df.groupby('Dates')['Usage'].sum()

# Calculate IQR
Q1 = daily_usage.quantile(0.25)
Q3 = daily_usage.quantile(0.75)
IQR = Q3 - Q1

# Define threshold for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = daily_usage[(daily_usage < lower_bound) | (daily_usage > upper_bound)]
print("Outlier Dates:", outliers.index)

# Replace outliers with rolling median (smoothing)
df['Usage_Smooth'] = df.groupby('Dates')['Usage'].transform(lambda x: x.rolling(window=7, min_periods=1).median())

# Replace outliers with rolling median
df['Usage_Smooth'] = df.groupby('States')['Usage'].transform(lambda x: x.rolling(window=7, min_periods=1).median())

# Plot comparison
plt.figure(figsize=(12, 5))
plt.plot(df.groupby('Dates')['Usage'].sum(), label="Original Usage", alpha=0.5)
plt.plot(df.groupby('Dates')['Usage_Smooth'].sum(), label="Smoothed Usage", color='r')
plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("Original vs Smoothed Usage (Outlier Handling)")
plt.legend()
plt.grid(True)
plt.show()

df['Usage_Smooth_7'] = df.groupby('States')['Usage'].transform(lambda x: x.rolling(window=7, min_periods=1).median())

# Plot new comparison
plt.figure(figsize=(12, 5))
plt.plot(df.groupby('Dates')['Usage'].sum(), label="Original Usage", alpha=0.5)
plt.plot(df.groupby('Dates')['Usage_Smooth_7'].sum(), label="7-day Smoothed Usage", color='r')
plt.xlabel("Date")
plt.ylabel("Usage")
plt.title("Original vs 7-day Smoothed Usage (More Aggressive Smoothing)")
plt.legend()
plt.grid(True)
plt.show()

df['Dates'] = pd.to_datetime(df['Dates'])
df['Year'] = df['Dates'].dt.year
df['Month'] = df['Dates'].dt.month
df['Week'] = df['Dates'].dt.isocalendar().week
df['Day'] = df['Dates'].dt.day
df['DayOfWeek'] = df['Dates'].dt.dayofweek
df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

df['Lag_1'] = df.groupby('States')['Usage_Smooth'].shift(1)
df['Lag_7'] = df.groupby('States')['Usage_Smooth'].shift(7)
df['Lag_14'] = df.groupby('States')['Usage_Smooth'].shift(14)
df['Rolling_Mean_7'] = df.groupby('States')['Usage_Smooth'].transform(lambda x: x.rolling(window=7).mean())
df['Rolling_Mean_14'] = df.groupby('States')['Usage_Smooth'].transform(lambda x: x.rolling(window=14).mean())

df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

df.head()

from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Aggregating data by date for total demand
df_grouped = df.groupby('Dates')['Usage_Smooth'].sum()

# Train-test split (80% train, 20% test)
train_size = int(len(df_grouped) * 0.8)
train, test = df_grouped[:train_size], df_grouped[train_size:]

# ARIMA Model (order can be tuned)
model = ARIMA(train, order=(5,1,0))
model_fit = model.fit()

# Forecasting
forecast = model_fit.forecast(steps=len(test))

# Plot results
plt.figure(figsize=(12,6))
plt.plot(train, label="Train Data")
plt.plot(test, label="Actual Test Data", color='green')
plt.plot(test.index, forecast, label="ARIMA Forecast", color='red')
plt.legend()
plt.title("ARIMA Forecast vs Actual Demand")
plt.show()

!pip install pmdarima

from pmdarima import auto_arima

# Auto ARIMA to find best (p,d,q)
best_arima = auto_arima(df_grouped, seasonal=True, m=7, trace=True, suppress_warnings=True)
print(best_arima.summary())

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Train SARIMA model with optimal parameters
model = SARIMAX(df_grouped,
                order=(4, 0, 0),
                seasonal_order=(1, 0, 0, 7),
                enforce_stationarity=False,
                enforce_invertibility=False)

sarima_fit = model.fit()
print(sarima_fit.summary())

# Forecasting
forecast = sarima_fit.predict(start=len(train), end=len(train) + len(test) - 1)

# Plot the results
plt.figure(figsize=(10,5))
plt.plot(train, label="Train Data")
plt.plot(test, label="Actual Test Data", color='green')
plt.plot(forecast, label="Optimized SARIMA Forecast", color='red')
plt.legend()
plt.title("SARIMA Forecast vs Actual Demand")
plt.show()

from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

# MAPE (Mean Absolute Percentage Error)
mape = mean_absolute_percentage_error(test, forecast)
print(f"MAPE: {mape:.2f}")

# RMSE (Root Mean Squared Error)
rmse = mean_squared_error(test, forecast)
print(f"RMSE: {rmse:.2f}")

import statsmodels.api as sm

# Residuals calculation
residuals = test - forecast

# Residuals plot
plt.figure(figsize=(10,5))
plt.plot(residuals, label="Residuals")
plt.axhline(0, color='red', linestyle='dashed')
plt.legend()
plt.title("Residual Plot")
plt.show()

# ACF (Autocorrelation Function) of Residuals
sm.graphics.tsa.plot_acf(residuals, lags=30)
plt.show()

from sklearn.model_selection import train_test_split

# Feature & target selection
features = ["Lag_1", "Lag_7", "Lag_14", "Rolling_Mean_7", "Rolling_Mean_14", "Month_sin", "Month_cos", "DayOfWeek_sin", "DayOfWeek_cos"]
target = "Usage_Smooth"

# Splitting the data
train, test = train_test_split(df, test_size=0.2, shuffle=False)

X_train, y_train = train[features], train[target]
X_test, y_test = test[features], test[target]

print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

# Train XGBoost
xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
xgb_model.fit(X_train, y_train)

# Predictions
xgb_pred = xgb_model.predict(X_test)

# Evaluation
xgb_mape = mean_absolute_percentage_error(y_test, xgb_pred)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))

print(f"📌 XGBoost MAPE: {xgb_mape:.4f}")
print(f"📌 XGBoost RMSE: {xgb_rmse:.2f}")

from sklearn.ensemble import RandomForestRegressor

# Train Random Forest
rf_model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
rf_pred = rf_model.predict(X_test)

# Evaluation
rf_mape = mean_absolute_percentage_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

print(f"📌 Random Forest MAPE: {rf_mape:.4f}")
print(f"📌 Random Forest RMSE: {rf_rmse:.2f}")

from sklearn.model_selection import RandomizedSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Randomized Search
rf_tuned = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_grid,
    n_iter=10,
    scoring='neg_mean_absolute_percentage_error',
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

# Train
rf_tuned.fit(X_train, y_train)

# Best Params
print(f"Best RF Params: {rf_tuned.best_params_}")

# Predict with tuned model
rf_best = rf_tuned.best_estimator_
rf_pred_tuned = rf_best.predict(X_test)

# Evaluation
rf_mape_tuned = mean_absolute_percentage_error(y_test, rf_pred_tuned)
rf_rmse_tuned = np.sqrt(mean_squared_error(y_test, rf_pred_tuned))

print(f"📌 Tuned RF MAPE: {rf_mape_tuned:.4f}")
print(f"📌 Tuned RF RMSE: {rf_rmse_tuned:.2f}")

import optuna
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Objective function for optimization
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
        "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.1),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "random_state": 42
    }

    # Train model
    model = XGBRegressor(**params)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # RMSE calculation without 'squared' argument
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Calculate RMSE directly
    return rmse

# Run optimization
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=20)

# Best parameters
best_params_xgb = study.best_params
print("Best XGBoost Params:", best_params_xgb)

# Train XGBoost with best parameters
xgb_best = XGBRegressor(
    n_estimators=300,
    learning_rate=0.043831712339523446,
    max_depth=10,
    min_child_weight=5,
    random_state=42
)

xgb_best.fit(X_train, y_train)

# Predict
y_pred_xgb_tuned = xgb_best.predict(X_test)

from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np  # Make sure NumPy is imported

# Evaluate model
mape_xgb_tuned = mean_absolute_percentage_error(y_test, y_pred_xgb_tuned)

# Calculate RMSE using np.sqrt for older scikit-learn versions
rmse_xgb_tuned = np.sqrt(mean_squared_error(y_test, y_pred_xgb_tuned))

print(f"📌 Tuned XGBoost MAPE: {mape_xgb_tuned:.4f}")
print(f"📌 Tuned XGBoost RMSE: {rmse_xgb_tuned:.2f}")

# Predict using Random Forest
rf_forecast = rf_best.predict(X_test)

# Predict using XGBoost
xgb_forecast = xgb_best.predict(X_test)

# Plot Random Forest vs Actual Demand
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label="Actual Test Data", color='green')
plt.plot(rf_forecast, label="Random Forest Forecast", color='pink', linestyle="dashed")
plt.legend()
plt.title("Random Forest Forecast vs Actual Demand")
plt.xlabel("Time")
plt.ylabel("Electricity Demand")
plt.show()

# Plot XGBoost vs Actual Demand
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label="Actual Test Data", color='green')
plt.plot(xgb_forecast, label="XGBoost Forecast", color='red')
plt.legend()
plt.title("XGBoost Forecast vs Actual Demand")
plt.xlabel("Time")
plt.ylabel("Electricity Demand")
plt.show()