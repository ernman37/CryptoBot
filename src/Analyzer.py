'''
    File: Analyzer.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:39 PM
    For: Crypto Bot
    Description: Will analyze all data of the coins 
'''
import pandas as pd
from Trader import Trader
import queue, logging
from CoinData import CoinData

from CoinQueue import Queue

class Analyzer:
    def __init__(self, coinsData: list[CoinData], scanQueue: Queue, tradeQueue: Queue):
        self.log = logging.getLogger()
        self.log.error("Setting up Analyzer")
        self.coinsData = coinsData
        self.scanQueue = scanQueue

    def analyzeForever(self):
        while True:
            if not self.scanQueue.isEmpty():
                coinTicker = self.scanQueue.get()
                self.log.error("Got Coin: " + str(coinTicker) +  " from queue")
                self.analyzeCoin(coinTicker)

    def analyzeCoin(self, ticker):
        self.analyzeIndicators(ticker)
        pass

    def analyzeIndicators(self, ticker):
        pass

    def createBuyorSell(self, weight):
        pass


