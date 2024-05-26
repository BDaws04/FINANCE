import pandas as pd
import numpy as np
import Statistics as stats
from alpaca.trading.client import TradingClient
from alpaca.trading.client import GetAssetsRequest
import time


# This function will be used to load the API keys from a file
def loadKeys():
    with open("AlpacaAPI\Keys.txt") as file:
        try:
           API_KEY = file.readline().strip()
           SECRET_KEY = file.readline().strip()
        except Exception as e:
            print(f"{e}")
        return API_KEY, SECRET_KEY
    

#Functions to get data about account and the exchange vv
def tradableStock(client, stock):
    stockAsset = client.get_asset(stock)
    if stockAsset.tradable:
        return True
    else:
        return False
    
def getTradableStocks(client):
    search_params = GetAssetsRequest(asset_class='us_equity')
    assets = client.get_all_assets(search_params)
    tradableStocks = []
    for asset in assets:
        if asset.tradable:
            tradableStocks.append(asset.symbol)
    print(tradableStocks)
    return tradableStocks

def openPositions(client):
   portfolio = client.get_all_positions()
   for position in portfolio:
       print(f"Symbol: {position.symbol}, Quantity: {position.qty}, Market Value: {position.market_value}")
    

def getPositon(client, stock):
    position = client.get_position(stock)
    print(f"Symbol: {position.symbol}, Quantity: {position.qty}, Market Value: {position.market_value}")
    return position
#Functions to get data about account and the exchange ^^


# This function will be used to run the bot
def runBot():
    API_KEY, SECRET_KEY = loadKeys()
    tradingClient = TradingClient(API_KEY, SECRET_KEY, paper=True)
    while True:
        ...
        time.sleep(60)


if __name__ == "__main__":
    runBot()

    
