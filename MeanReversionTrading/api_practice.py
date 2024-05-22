from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt

def getAPIKey():
    with open ("C:/Users/hp/Desktop/GitHub-Projects/FINANCE/MeanReversionTrading/api_key.txt", 'r') as file:
        key = file.read().strip()
    return key
    
API_KEY = getAPIKey()
ts = TimeSeries(key=API_KEY, output_format='pandas')

symbol = 'AAPL'

data, meta_data = ts.get_monthly_adjusted(symbol=symbol)

plt.figure(figsize=(10,5))
data['4. close'].plot(color='blue')
plt.title('Historical Stock prices for AAPL')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
