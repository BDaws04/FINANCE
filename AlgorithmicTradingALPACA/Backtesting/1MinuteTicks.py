import matplotlib.pyplot as plt 
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta 
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from Keys import loadKeys
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

"""
File for testing trading strategies, where the required ticks is one minute
This is a general file, particular changes for testing a particular stock/strategy should not be saved to this master file
"""

def plotGraph(spy: DataFrame, stock: DataFrame, balance: float, label: str):
    
    spyPrices = spy['close']
    stockPrices = stock['close']

    spyStart = spyPrices.iloc[0]
    stockStart = stockPrices.iloc[0]

    spyMultiplier = balance / spyStart
    stockMultiplier = balance / stockStart

    spyArray = spyPrices.values
    stockArray = stockPrices.values
    spyArray *= spyMultiplier
    stockArray *= stockMultiplier

    plt.figure(figsize=(10,6))
    plt.plot(spyArray, label = 'SPY', color='red')
    plt.plot(stockArray, label=label, color='blue')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price Comparison: SPY vs BUYANDHOLD vs Strategy')
    plt.legend()
    plt.grid(True)

    plt.show()

def loadData(api: str, secret: str, stock: str):

    currentDate = datetime.today()
    oneYearAgoDate = currentDate - timedelta(days=365)
    oneYearAgoDateF = oneYearAgoDate.strftime('%Y-%m-%d')

    client = StockHistoricalDataClient(api, secret)
    dailyDataParameters = StockBarsRequest(
        symbol_or_symbols=stock,
        start=oneYearAgoDateF,
        timeframe=TimeFrame.Day
    )
    dailyDataParametersSPY = StockBarsRequest(
        symbol_or_symbols='SPY',
        start=oneYearAgoDateF,
        timeframe=TimeFrame.Day
    )

    minuteDataParameters = StockBarsRequest(
        symbol_or_symbols=stock,
        start=oneYearAgoDateF,
        timeframe=TimeFrame.Minute
    )
    dailyData = client.get_stock_bars(dailyDataParameters)
    minuteData = client.get_stock_bars(minuteDataParameters)
    spyData = client.get_stock_bars(dailyDataParametersSPY)

    dailyDataDF = dailyData.df
    minuteDataDF = minuteData.df
    spyDataDF = spyData.df

    return dailyDataDF, minuteDataDF, spyDataDF

def test(stock: str):
    API_KEY, SECRET_KEY = loadKeys()
    starting_balance = 10000
    dailyData, minuteData, spy = loadData(API_KEY, SECRET_KEY, stock)

    plotGraph(spy, dailyData, 10000, stock)
    
if __name__ == '__main__':
    test('AAPL')