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
This file is testing MeanReversionTrading MethodOne
RESULTS:
1? beats BUYANDHOLD: NO
2? beats SPY: NO

1) Calculates the RSI2
2) Calculates the 14 day SMA
3) Buys when the RSI2 is below 10, 5% of balance.
4) Sells either at 5% profit, or when the stock re-reaches the 14 day SMA
"""

def rollingSMA(data: DataFrame):
    data['14_day_SMA'] = data['close'].rolling(window=14).mean()
    return data

def calculateRSI2(gains, losses):
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    if avg_loss == 0:
        rs = float('inf')
    else:
        rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))
    return rsi

def simulateTrades(prices: DataFrame, cash: int):

    SMA = rollingSMA(dailyData)

    activeOrder = False
    buyPrice = 0
    sellPrice = 0
    volume = 0
    current_date = None

    prices['prev_close'] = prices['close'].shift(1)
    gains = []
    losses = []

    rolling_cash = []
    rolling_cash.append(cash)

    for index, row in prices.iterrows():
        
        symbol,date = index
        price = row['close']
        prev_price = row['prev_close']
        date = index[1].date()

        if current_date == None:
            current_date = date

        if current_date != date:
            rolling_cash.append(cash)
            current_date = date

        if activeOrder == True:
            if price >= sellPrice:
                cash = cash + (volume * price)
                activeOrder = False
                volume = 0
                buyPrice = 0
                sellPrice = 0
                continue
            else:
                continue

        if pd.notna(prev_price):
            change = price - prev_price

            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

            if len(gains) > 2:
                gains.pop(0)
                losses.pop(0)
            
            if len(gains) == 2 and len(losses) == 2:

                rsi2 = calculateRSI2(gains, losses)

                if rsi2 < 10:
                    activeOrder = True
                    buyPrice = price

                    volume = (cash * 0.05) / buyPrice
                    cash = cash - (volume * buyPrice)

                    if current_date in SMA.index:
                        smaVal = SMA.at[current_date, '14_day_SMA']
                    else:
                        smaVal = 0
                    
                    if pd.notna(smaVal) and smaVal > buyPrice:
                        sellPrice = smaVal
                    else:
                        sellPrice = buyPrice * 1.05
    return rolling_cash
                
def plotGraph(spy: DataFrame, stock: DataFrame, balance: float, label: str, bot: list):
    
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
    plt.plot(bot, label='Bot', color='green')

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
    startingBalance = 10000
    global dailyData
    dailyData, minuteData, spy = loadData(API_KEY, SECRET_KEY, stock)

    rollingCash = simulateTrades(minuteData, startingBalance)
    plotGraph(spy, dailyData, startingBalance, stock, rollingCash)
    
if __name__ == '__main__':
    test('AAPL')