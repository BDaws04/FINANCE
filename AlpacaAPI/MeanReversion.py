import pandas as pd
import numpy as np
import Statistics as stats


def loadKeys():
    with open("AlpacaAPI\Keys.txt") as file:
        try:
           API_KEY = file.readline().strip()
           SECRET_KEY = file.readline().strip()
        except Exception as e:
            print(f"{e}")
        return API_KEY, SECRET_KEY

API_KEY, SECRET_KEY = loadKeys()
stats.getData(API_KEY, SECRET_KEY)
    
