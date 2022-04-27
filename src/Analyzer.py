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
    def __init__(self, coinsData, scanQueue, tradeQueue):
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
        numOfIndicators = 1
        weight = 0
        weight += self.analyzeRSI(indicators['rsi'])
        # Further analysis on several indicators here
        weight = weight / numOfIndicators
        self.createBuyorSell(weight, coin)

    # Basic RSI trading strategy
    def analyzeRSI(self, rsi):
        recentRSI = rsi.iloc[-1]
        lastRSI = rsi.iloc[-2]
        #Overbought "sell"
        if recentRSI > 50 or lastRSI > 50:
            self.log.error("RSI is in an overbought zone: " + str(recentRSI))
            if recentRSI > lastRSI:
                self.log.error("RSI is greater than before waiting for optimal exit RSI")
                return 0
            return -(recentRSI / 50)
        #Oversold "buy"
        elif recentRSI < 40 or lastRSI < 40:
            self.log.error("RSI is in an oversold zone: " + str(recentRSI))
            if recentRSI < lastRSI:
                self.log.error("RSI is less than before waiting for optimal exit RSI")
                return 0
            return recentRSI / 40
        #Neutral "wait"
        else:
            self.log.error("RSI is in a neutral zone: " + str(recentRSI))
            return 0

    def createBuyorSell(self, weight, coin):
        self.log.error("Weight for Coin \'" + coin + "\' is: " + str(weight))
        order = Analyzer.createWait(coin)
        if (weight < -.75):
            order = Analyzer.createSell(weight, coin) 
        elif (weight > .75):
            order = Analyzer.createBuy(weight, coin)
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
    def createWait(coin):
        order = Analyzer.createOrder(0, coin, "wait")
        return order

    @staticmethod
    def createOrder(weight, coin, orderType):
        order = {
            "type": orderType,
            "weight": abs(weight),
            "coin": coin
        }
        return order



