# 📈 AI-Powered Stock Analysis Platform

An interactive **Streamlit-based stock analysis dashboard** combining **technical indicators**, **machine-learning trend prediction**, and **AI-style explanations**.

> ⚠️ Educational project only — **not financial advice**.

---

## 🚀 Key Features

* Dynamic stock symbols (AAPL, MSFT, RELIANCE.NS, etc.)
* Two modes:

  * **Short-term ML (5-day history)** – stable predictions
  * **Intraday (1-day view)** – smart fallback when data is limited
* Technical indicators: **SMA & RSI** (user-controlled)
* ML-based trend prediction with confidence score
* Rule-based fallback when ML data is insufficient
* Explainable AI-style natural language insights
* Caching for faster performance

---

## 🧱 Architecture Overview

```
User Input → Market Data → Indicators → ML / Fallback → AI Explanation → Streamlit UI
```

**Code separation:**

* `indicators.py` – indicator logic
* `ml_model.py` – ML pipeline
* `ai_explainer.py` – explanation layer
* `streamlit_app.py` – UI & orchestration

---

## 🛠 Tech Stack

* Python
* Streamlit
* yfinance
* Plotly
* scikit-learn
* Pandas / NumPy

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

App opens at `http://localhost:8501`.

---

## 🧠 Highlights

* Handles real-world data availability issues gracefully
* Designed with ML safety checks and fallbacks
* Focus on explainability over black-box predictions

---

## 👤 Author

**Abhinav Thakur**

