import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient

def getData(key, secret):
    client = TradingClient(key,secret,paper=True)
    account = client.get_account()

    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    print('${} is available as buying power.'.format(account.buying_power))
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')
  

  