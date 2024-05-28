from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.enums import TimeInForce, OrderSide
from Keys import loadKeys
import time
from datetime import datetime, timezone, timedelta
import pytz
import pandas as pd

"""
This method involves using RSI2 indicator, and purchases the stock when it falls below 10
This means the stock has fallen excessively relative to a gain, suggesting a climb back to the mean
Once it reaches this place, the bot purchases the stock, then it places a sell limit order for the mean price
"""

def getSMA(stock: str, client: StockHistoricalDataClient):

    today = datetime.now()
    todayFormatted = today.strftime("%Y-%m-%d")
    prevDate = today - timedelta(days=14)
    prevDateFormatted = prevDate.strftime("%Y-%m-%d")

    requestParameters = StockBarsRequest(
        symbol_or_symbols=stock,
        timeframe=TimeFrame.Day,
        start=prevDateFormatted,
        end=todayFormatted,
    )

    SMAData = client.get_stock_bars(requestParameters)
    SMAdf = SMAData.df

    prices = SMAdf['close']
    SMAPeriod = 14

 
    SMA = prices.rolling(window=SMAPeriod).mean().iloc[SMAPeriod - 1]
    return SMA

def placeBracketOrder(client: TradingClient, stock, volume, sellPrice, order):

    requestParameters = MarketOrderRequest(
        symbol=stock,
        qty=volume,
        side=OrderSide.BUY,
        time_in_force = TimeInForce.GTC,
        take_profit = TakeProfitRequest(sellPrice),
        client_order_id = order,

    )

    bracketOrder = client.submit_order(order_data=requestParameters)


def calcRSI2(prices: pd.Series):

    delta = prices.diff()

    gain = delta.where(delta > 0, 0)
    loss = delta.where(delta > 0, 0)

    avgGain = gain.mean()
    avgLoss = loss.mean()

    rs = avgGain / avgLoss

    rsi2 = 100 - (100/(1 + rs))
    return rsi2


def getRSI2(stock, client: StockHistoricalDataClient):

    currentTimeUTC = datetime.now(timezone.utc)
    eastern_tz = pytz.timezone('US/Eastern')
    currentTimeET = currentTimeUTC.astimezone(eastern_tz)

    delta = timedelta(minutes=-2)
    prevTimeET = currentTimeET + delta

    currentTimeETISO = currentTimeET.isoformat()
    prevTimeETISO = prevTimeET.isoformat()

    requestParameters = StockBarsRequest(
        symbol_or_symbols=stock,
        timeframe=TimeFrame.Minute,
        start=prevTimeETISO,
        end=currentTimeETISO,
    )

    stockBarData = client.get_stock_bars(requestParameters)
    stockData = stockBarData.df

    if len(stockData) != 2:
        return
    
    global prices
    prices = stockData['close']
    
    rsi2 = calcRSI2(prices)
    return rsi2 <= 10

def marketOpen(client):
    clock = client.get_clock()
    return clock.is_open

def runBot(stock):
    API_KEY, SECRET_KEY = loadKeys()

    client = TradingClient(API_KEY, SECRET_KEY, paper=True)
    historicalClient = StockHistoricalDataClient(API_KEY, SECRET_KEY)

    asset = client.get_asset(stock)

    if not asset.tradable:
        print("Invalid stock inputted")
        exit(0)

    account = client.get_account()

    if account.trading_blocked:
        print("Account is unable to trade")
        exit(0)

    global activeOrder
    activeOrder = False 
    balance = account.equity
    orderN = 0
    
    while True:
        if marketOpen():
            if getRSI2(stock, historicalClient) and activeOrder == False:
                buyPrice = prices.iloc[-1]
                volume = round(((balance * 0.05) / buyPrice), 3)

                SMA = getSMA()

                if SMA < buyPrice:
                    sellPrice = round(buyPrice * 1.05, 3)
                else:
                    sellPrice = round(SMA, 3)

                placeBracketOrder(client, stock, volume, sellPrice, orderN)

                activeOrder == True

                while activeOrder:
                    position = client.get_open_position(stock)

                    if position is None:
                        activeOrder == False
                        orderN += 1
                    else:
                        time.sleep(60)

            else:
                time.sleep(60)
        else:
            time.sleep(900)
    
if __name__ == '__main__':
    runBot('AAPL')