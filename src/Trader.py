'''
    File: Trader.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:48 PM
    For: Crypto Bot
    Description: Will access the Market for buying and selling of crypto/paper trading
'''
from CoinApi import CoinApi

class Trader:
    def __init__(self, accountConfig):
        self.accountConfig = accountConfig
        self.market = CoinApi.getMarket()

