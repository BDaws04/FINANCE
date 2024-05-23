import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Function to check if the stock is valid for the model
# Must have a volume over 100k+, and data must be accessible by yfinance
def validStock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')

        if data.empty:
            return False
        
        avg_volume = data['Volume'].mean()

        if avg_volume > 10000:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error for symbol {symbol}: {e}")
        return False

# Function to calculate Bollinger Bands and SMA using rolling windows
def calculateBollingerBandsAndSMA(data, window, stds):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    UpperBand = rolling_mean + (stds * rolling_std)
    LowerBand = rolling_mean - (stds * rolling_std)
    return rolling_mean, UpperBand, LowerBand

# Function to fetch data and filter for market hours
def fetchData(symbol, period='5d', interval='60m'):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)
    
    # Convert index to datetime if necessary
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    
    # Filter out times outside regular market hours
    market_open = pd.Timestamp('09:30:00').time()
    market_close = pd.Timestamp('16:00:00').time()
    data = data.between_time(market_open, market_close)

    return data

# Function to plot the data
def plot(data, SMA, UB, LB):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], color='k', label='Close Price')
    plt.plot(SMA, color='y', linestyle='--', label='SMA')
    plt.plot(UB, color='g', linestyle='--', label='Upper Band')
    plt.plot(LB, color='r', linestyle='--', label='Lower Band')
    plt.title(f"{symbol} price over the last 5 days with Bollinger Bands")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()


symbol = 'AAPL'
if validStock(symbol):
    data = fetchData(symbol)
    window = 100  # Common window size for Bollinger Bands
    stds = 2  # Number of standard deviations
    SMA, UpperBand, LowerBand = calculateBollingerBandsAndSMA(data, window, stds)
    plot(data, SMA, UpperBand, LowerBand)
else:
    exit(0)