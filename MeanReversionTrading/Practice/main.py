import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd



# Function to check if the stock is valid for the model
# Must have a volume over 75k+, and data must be accessible by yfinance
def validStock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')

        if data.empty:
            return False
        
        avg_volume = data['Volume'].mean()
        print(avg_volume)

        if avg_volume > 75000:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error for symbol {symbol}: {e}")
        return False

def calculateBollingerBandsAndSMA(data, stds):
    SMA = (data['Close'].sum() / len(data['Close']))
    standard_deviation = data['Close'].std()
    UpperBand = SMA + (stds * standard_deviation)
    LowerBand = SMA - (stds * standard_deviation)
    UpperBandWEAK = SMA + (stds/2 * standard_deviation)
    LowerBandWEAK = SMA - (stds/2 * standard_deviation)

    return SMA, UpperBand, LowerBand, UpperBandWEAK, LowerBandWEAK

    
def fetchMetricData(symbol, period='5d', interval='1m'):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)
    return data

def fetchData(symbol, period='1d', interval='1m'):
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period, interval=interval)

def plot(data, SMA, UB, LB, UB2, LB2):
    data['Close'].plot(title=f"{symbol} price over the last 5 days", color='k')
    plt.axhline(y=SMA, color='y', linestyle ='--', label='SMA')
    plt.axhline(y=UB, color='g', label='Upper Bound')
    plt.axhline(y=LB, color='r', label='Lower Bound')
    plt.axhline(y=UB2, color='g', linestyle ='--', label='Upper Bound Weak')
    plt.axhline(y=LB2, color='r', linestyle ='--', label='Lower Bound Weak')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()



symbol = 'AAPL'
if (validStock(symbol)):
   metricData = fetchMetricData(symbol)
   SMA, UpperBand, LowerBand, UpperBandWEAK, LowerBandWEAK = calculateBollingerBandsAndSMA(metricData, 2)
   data = fetchData(symbol)
   plot(data, SMA, UpperBand, LowerBand, UpperBandWEAK, LowerBandWEAK)
else:
    exit(0)




    


