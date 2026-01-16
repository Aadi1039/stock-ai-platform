import os
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


# Paths for saved artifacts

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "trend_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


# Feature preparation
def prepare_ml_data(data):
    df = data.copy()

    df["return"] = df["Close"].pct_change()
    df["sma_diff"] = df["Close"] - df["SMA"]
    df["rsi"] = df["RSI"]

    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df = df.dropna()

    X = df[["return", "sma_diff", "rsi"]]
    y = df["target"]

    return X, y


def predict_trend(data):
    X, y = prepare_ml_data(data)

    # Not enough data → let Streamlit fallback
    if len(X) < 10:
        return None, None

    os.makedirs(MODEL_DIR, exist_ok=True)

    
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = LogisticRegression()
        model.fit(X_scaled, y)

        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)

   
    X_scaled = scaler.transform(X)
    latest_features = X_scaled[-1].reshape(1, -1)

    prob_up = model.predict_proba(latest_features)[0][1]
    prediction = "UP" if prob_up > 0.5 else "DOWN"

    return prediction, prob_up
