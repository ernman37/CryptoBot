'''
    File: CoinsScanner.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:25 PM
    For: Crypto Bot
    Description: Scans a list of coins data for analysis
'''
from data.CoinData import CoinData
from time import sleep

class CoinsScanner:
    async def __init__(self, coins, timeFrame='1m'):
        self.coins = dict()
        for coin in coins:
            self.coins[coin] = await CoinData(coin, timeFrame=timeFrame)

    def scanForever(self):
        changed = False
           

    def isNewCoin(self):
        pass

