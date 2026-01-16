def generate_ai_explanation(symbol,trend,confidence,latest_row):
    rsi=latest_row['RSI']
    sma_diff=latest_row['Close']-latest_row['SMA']
    explanation= f"""
The model predicts a {trend} trend for {symbol} with a confidence of {confidence:.2f}.
Key Reasons:
- RSI is {rsi:.2f}, which indicates {'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral'} conditions.
- The price is {'above' if sma_diff > 0 else 'below'} the 20-period moving average, suggesting {'bullish' if sma_diff > 0 else 'bearish'} momentum.

This analysis is for educational purposes only and not financial advice.
"""

    return explanation.strip()