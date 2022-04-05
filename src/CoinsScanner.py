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

    def scanForever(self):
        while True:
            if self.isNewCoin():
                self.fetchAllNewCandles()
            else:
                time.sleep(1)

    def isNewCoin(self):
        newTime = self.timeInMinutes()
        if self.currentTime != newTime:
            self.currentTime = newTime
            return True
        return False

    def fetchAllNewCandles(self):
        for coin in self.tickerList:
            while not self.coins[coin].addNewCandle():
                time.sleep(2) # Sleep for a little if we fetched last candle

    def timeInMinutes(self):
            secs = time.time()
            mins = secs / 60
            return int(mins)  