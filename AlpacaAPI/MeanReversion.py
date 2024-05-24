import alpaca_trade_api as trade
import pandas as pd
import numpy as np


def loadKeys():
    with open("AlpacaAPI\Keys.txt") as file:
        try:
           API_KEY = file.readline().strip()
           SECRET_KEY = file.readline().strip()
        except Exception as e:
            print(f"{e}")
        return API_KEY, SECRET_KEY

API_KEY, SECRET_KEY = loadKeys()
print(API_KEY)
print(SECRET_KEY)
    
