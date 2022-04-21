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

class Analyzer:
    def __init__(self, coinsData: list[CoinData], scanQueue: queue, tradeQueue: queue):
        self.log = logging.getLogger()
        self.log.error("Setting up Analyzer")
        self.coinsData = coinsData
        self.scanQueue = scanQueue
        self.tradeQueue = tradeQueue

    def analyzeForever(self):
        while True:
            if not self.scanQueue.empty():
                coinTicker = self.scanQueue.get()
                self.analyzeCoin(coinTicker)

    def analyzeCoin(self, coin):
        self.log.error("Analyzing Coin: " + str(coin))
        self.analyzeIndicators(coin)
        self.createBuyorSell(-1, coin)

    def analyzeIndicators(self, coin):
        pass

    def createBuyorSell(self, weight, coin):
        order = Analyzer.createSell(weight, coin) if (weight < .75) else Analyzer.createBuy(weight, coin)
        self.tradeQueue.put(order)

    @staticmethod
    def createSell(weight, coin):
        order = Analyzer.createOrder(weight, coin, "sell")
        return order

    @staticmethod
    def createBuy(weight, coin):
        order = Analyzer.createOrder(weight, coin, "buy")
        return order

    @staticmethod
    def createOrder(weight, coin, orderType):
        order = {
            "type": orderType,
            "weight": abs(weight),
            "coin": coin
        }
        return order



