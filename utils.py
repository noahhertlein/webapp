import yfinance as yf
import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment

# Function to calculate RSI for given data and window
def calculate_RSI(data, window):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate MACD for given data and specified windows
def calculate_MACD(data, short_window, long_window, signal_window):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# Validate the stock ticker
def validate_ticker(ticker):
    stock = yf.Ticker(ticker)
    if not stock.history(period="1d").empty:
        return True
    else:
        return False

# Validate the date range
def validate_date_range(start_date, end_date):
    try:
        pd_start_date = pd.to_datetime(start_date)
        pd_end_date = pd.to_datetime(end_date)
        if pd_start_date > pd_end_date:
            return False
        else:
            return True
    except Exception:
        return False