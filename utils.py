import yfinance as yf
import pandas as pd

# Function to fetch key ratios for a given ticker
def fetch_ratios(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    key_ratios = {
        'P/E Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        'Price-to-Book': info.get('priceToBook', 'N/A'),
        'Beta': info.get('beta', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A'),
        'Enterprise Value': info.get('enterpriseValue', 'N/A'),
        'Profit Margin': info.get('profitMargins', 'N/A'),
        'Operating Margin': info.get('operatingMargins', 'N/A'),
        'Return on Assets': info.get('returnOnAssets', 'N/A'),
        'Return on Equity': info.get('returnOnEquity', 'N/A'),
        'Revenue Growth': info.get('revenueGrowth', 'N/A'),
        'Earnings Growth': info.get('earningsGrowth', 'N/A'),
        'Total Cash': info.get('totalCash', 'N/A'),
        'Total Debt': info.get('totalDebt', 'N/A'),
        'Total Revenue': info.get('totalRevenue', 'N/A'),
        'Book Value': info.get('bookValue', 'N/A'),
        'Operating Cash Flow': info.get('operatingCashflow', 'N/A'),
        'Fifty-day Moving Average': info.get('fiftyDayAverage', 'N/A'),
        'Two-hundred-day Moving Average': info.get('twoHundredDayAverage', 'N/A'),
        'Shares Outstanding': info.get('sharesOutstanding', 'N/A'),
        'Shares Short': info.get('sharesShort', 'N/A'),
        'Short Ratio': info.get('shortRatio', 'N/A'),
        'Short Percentage of Float': info.get('shortPercentOfFloat', 'N/A'),
        'Forward P/E Ratio': info.get('forwardPE', 'N/A'),
        'Price-to-Sales': info.get('priceToSalesTrailing12Months', 'N/A'),
        'Forward Price-to-Sales': info.get('forwardEps', 'N/A'),
        'PEG Ratio': info.get('pegRatio', 'N/A'),
        'Enterprise-to-Revenue': info.get('enterpriseToRevenue', 'N/A'),
        'Enterprise-to-EBITDA': info.get('enterpriseToEbitda', 'N/A'),
        '52-Week Change': info.get('52WeekChange', 'N/A'),
        'SandP52-Week Change': info.get('SandP52WeekChange', 'N/A'),
        'Last Dividend Value': info.get('lastDividendValue', 'N/A'),
        'Regular Market Day Low': info.get('regularMarketDayLow', 'N/A'),
        'Regular Market Volume': info.get('regularMarketVolume', 'N/A'),
        'Regular Market Previous Close': info.get('regularMarketPreviousClose', 'N/A'),
        'Regular Market Open': info.get('regularMarketOpen', 'N/A'),
        'Average Daily Volume 10 Day': info.get('averageDailyVolume10Day', 'N/A'),
    }
    return key_ratios

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
