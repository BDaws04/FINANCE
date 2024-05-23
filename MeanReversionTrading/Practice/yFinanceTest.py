import yfinance as yf 
import matplotlib.pyplot as plt
import pandas as pd 

ticker = yf.Ticker('AAPL')
data = ticker.history(period="1d", interval="1m")
key_data = data[['Open', 'High', 'Close', 'Low', 'Volume']]

data['Close'].plot(title="AAPL stock price over the day")
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.grid(True)
plt.show()