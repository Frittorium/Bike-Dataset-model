# Bike Rental Demand Prediction

A neural network regression model that predicts hourly bike rental demand from weather and time-of-day data, packaged with a desktop GUI for interactive predictions.

## The Dataset & Problem

The data comes from Kaggle's [Bike Sharing Demand](https://www.kaggle.com/competitions/bike-sharing-demand/) competition: 10,886 hourly records from a bike-share system spanning 2011–2012, with weather conditions (temperature, "feels-like" temperature, humidity, wind speed, weather category), calendar context (season, holiday, working day), and rental counts (casual, registered, total).

The task is a regression problem: given the weather and time context for a given hour, predict how many bikes will be rented. This kind of forecast is useful for fleet rebalancing and staffing decisions in real bike-share systems.

## What I Did

1. Loaded and inspected the raw CSV, checking for missing values, duplicates, and class balance across categorical fields.
2. Ran EDA to understand relationships between weather/time variables and rental count, including correlation analysis and visual trend inspection.
3. Engineered features from the raw columns and encoded categoricals.
4. Scaled inputs and log-transformed the (heavily skewed) target.
5. Trained a PyTorch feed-forward neural network with early stopping.
6. Saved the trained model and preprocessing artifacts, then built a Tkinter GUI and a `predict()` function to serve real-time predictions.

## Why These Decisions

- **Log-transforming the target**: rental counts are strongly right-skewed (skew ≈ 1.24 on raw counts). Applying `log1p` compresses this into something closer to normal, which is easier for the network to learn and keeps large-count hours from dominating the loss.
- **One-hot encoding weather/season/holiday/workingday**: these are unordered categories, not continuous scales, so one-hot avoids implying a false numeric ordering (e.g., that "weather 4" is "worse" in a linear sense than "weather 1" by a fixed amount).
- **Decomposing the datetime into year/month/day/hour/minute**: rental demand is highly cyclical by hour and season; splitting the timestamp lets the model learn these patterns directly rather than treating time as one opaque value.
- **StandardScaler fit only on the training set**: prevents information from the test set leaking into feature scaling.
- **A small feed-forward network (64→32→16→1) with early stopping**: the feature set is modest in size (21 features) and largely tabular/non-sequential, so a compact MLP is appropriate; early stopping (patience of 12 epochs) guards against overfitting given the dataset's size.

## How It's Implemented

- **`regression.ipynb`** — the full pipeline: data loading, EDA, cleaning checks, feature engineering (one-hot encoding + datetime decomposition), an 80/20 train/test split, `StandardScaler` scaling, and a PyTorch `BikeNN` model trained with Adam and MSE loss on the log-transformed target. The trained weights, scaler parameters, and feature ordering are saved to `models/bike_model.pt`.
- **`predict.py`** — loads the saved checkpoint and reconstructs the scaler and model, exposing a single `predict(data: dict) -> int` function that scales the input, runs inference, and reverses the log transform to return a bike count.
- **`Regression_GUI.py`** — a Tkinter form (weather sliders, dropdowns for season/year/month/day, hour/minute spinners, holiday/workday checkboxes) that assembles the same 21-feature dictionary the model was trained on and calls `predict()` to display a live estimate.

## Key Results & Findings

- **EDA**: rentals rise with temperature up to a point and fall off in high wind; humidity only shows a clear effect at the extreme low end. Weather category is heavily imbalanced (7,192 "clear" hours vs. just 1 "heavy rain" hour), and holidays/working days are similarly imbalanced — expected given their real-world frequency.
- **Training**: the model trained for 94 of a maximum 100 epochs before early stopping triggered, reaching a best validation loss (log-scale MSE) of 0.1077 in about 14 seconds on GPU.
- **Final performance**: on the held-out set, the model achieves an **RMSE of ~51.8** and an **MAE of ~32.1** bikes per hour.
- **Known limitation**: the same held-out split was used both to trigger early stopping and to report the final RMSE/MAE, so these numbers likely overstate real-world generalization slightly — a three-way train/validation/test split would give a more reliable estimate. No alternative models (e.g., a linear regression baseline or a different architecture) were trained for comparison, so it's currently unclear how much the neural network is outperforming simpler approaches.
