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
from time import sleep

class Analyzer:
    def __init__(self, coinsData: list[CoinData], scanQueue: queue, tradeQueue: queue):
        self.log = logging.getLogger()
        self.log.error("Setting up Analyzer")
        self.coinsData = coinsData
        self.scanQueue = scanQueue
        self.tradeQueue = tradeQueue

    def analyzeForever(self):
        while True:
            while not self.scanQueue.empty():
                coinTicker = self.scanQueue.get()
                self.analyzeCoin(coinTicker)
            sleep(1)

    def analyzeCoin(self, coin):
        self.log.error("Analyzing Coin: " + str(coin))
        self.analyzeIndicators(coin)

    def analyzeIndicators(self, coin):
        indicators = self.coinsData[coin].getIndicators()
        weight = 0
        weight += self.analyzeRSI(indicators['rsi'])
        #weight += self.analyzeATR(indicators['atr'])
        #weight += self.analyzeOBV(indicators['obv'])
        self.createBuyorSell(weight, coin)

    def analyzeRSI(self, rsi):
        recentRSI = rsi.iloc[-1]
        if recentRSI > 70:
            self.log.error("RSI is in an overbought zone: " + str(recentRSI))
            return -(recentRSI / 85)
        elif recentRSI < 25:
            self.log.error("RSI is in an oversold zone: " + str(recentRSI))
            return recentRSI / 20
        else:
            self.log.error("RSI is in a neutral zone: " + str(recentRSI))
            return 0

    def analyzeATR(self, atr):
        recentATR = atr.iloc[-1]
        #print(atr)
        return 0

    def analyzeOBV(self, obv):
        #print(obv)
        return 0

    def createBuyorSell(self, weight, coin):
        self.log.error("Weight for Coin \'" + coin + "\' is: " + str(weight))
        order = Analyzer.createSell(weight, coin) if (weight < .75) else Analyzer.createBuy(weight, coin)
        if weight < .7 and weight > -.7:
            return False
        self.tradeQueue.put(order)
        return True

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



