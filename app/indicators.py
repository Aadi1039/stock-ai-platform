import pandas as pd
import numpy as np
def calculate_sma(series, window=20):
    return series.rolling(window).mean()
def calculate_rsi(series, window=14):
    delta=series.diff()
    gain=delta.where(delta>0,0.0)
    loss=-delta.where(delta<0,0.0)
    avg_gain=gain.rolling(window).mean()
    avg_loss=loss.rolling(window).mean()
    rs=avg_gain/avg_loss
    rsi=100-(100/(1+rs))
    rsi=rsi.where(avg_loss!=0,100)
    return rsi