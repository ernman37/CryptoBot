'''
    File: CoinsScanner.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:25 PM
    For: Crypto Bot
    Description: Scans a list of coins data for analysis
'''
from CoinData import CoinData
import time, logging, queue, sys

class CoinsScanner:
    def __init__(self, coins, queue: queue.Queue, timeFrame='1m'):
        self.log = logging.getLogger()
        self.log.error("Setting up Scanner")
        self.tickerList = list(coins)
        self.queue = queue
        self.coins = dict()
        for coin in coins:
            self.coins[coin] = CoinData(coin, timeFrame=timeFrame)
            self.queue.put(coin)
        self.currentTime = self.timeInMinutes()

    def scanForever(self):
        self.log.error("Begginning To Scan Forever")
        while True:
            if self.isNewCoin():
                self.log.error("Fetching new coins")
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
            self.log.error("Added new candle to " + coin)
            while self.queue.full():
                time.sleep(1)
            self.queue.put(coin)

    def timeInMinutes(self):
            secs = time.time()
            mins = secs / 60
            return int(mins)  