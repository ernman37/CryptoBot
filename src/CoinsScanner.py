'''
    File: CoinsScanner.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:25 PM
    For: Crypto Bot
    Description: Scans a list of coins data for analysis
'''
from CoinData import CoinData
import time

class CoinsScanner:
    def __init__(self, coins, timeFrame='1m'):
        self.tickerList = list(coins)
        self.coins = dict()
        for coin in coins:
            self.coins[coin] = CoinData(coin, timeFrame=timeFrame)
        self.currentTime = self.timeInMinutes()

    def timeInMinutes(self):
        secs = time.time()
        mins = secs / 60
        return int(mins)

    def scanForever(self):
        while True:
            newTime = self.timeInMinutes()
            if self.isNewCoin():
                self.fetchAllNewCandles()
            else:
                time.sleep(1)

    def isNewCoin(self):
        newTime = self.timeInMinutes()
        if self.currentTime != newTime:
            time.sleep(2) #Allow where we are fetching to have a little bit of update time
            self.currentTime = newTime
            return True
        return False

    def fetchAllNewCandles(self):
        for coin in self.tickerList:
            self.coins[coin].addNewCandle()

