import matplotlib.pyplot as plt 
import pandas as pd
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
    minuteDataParameters = StockBarsRequest(
        symbol_or_symbols=stock,
        start=oneYearAgoDateF,
        timeframe=TimeFrame.Minute
    )
    dailyData = client.get_stock_bars(dailyDataParameters)
    minuteData = client.get_stock_bars(minuteDataParameters)

    dailyDataDF = dailyData.df
    minuteDataDF = minuteData.df

    return dailyDataDF, minuteDataDF

def test(stock: str):
    API_KEY, SECRET_KEY = loadKeys()
    starting_balance = 10000
    dailyData, minuteData = loadData(API_KEY, SECRET_KEY, stock)

    print(len(dailyData))
    print(len(minuteData))


if __name__ == '__main__':
    test('AAPL')