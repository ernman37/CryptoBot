'''
    File: CoinData.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:04 PM
    For: Crypto Bot
    Description: Holds the data for a single coin
                 Indicators + Candles
                 Plus current market access
'''
import pandas as pd
import pandas_ta as ta
from CoinApi import CoinApi

class CoinData:
    def __init__(self, coinTicker, timeFrame='1m'):
        self.coin = coinTicker
        self.timeFrame = timeFrame
        self.candles = pd.DataFrame()
        self.buildCoinData()
        self.indicators = pd.DataFrame()
        self.updateIndicators()

    def buildCoinData(self):
        self.candles = CoinApi.getCandles(self.coin)
    
    def updateIndicators(self):
        self.indicators['rsi'] = ta.rsi(self.candles['close'])
        self.indicators['atr'] = ta.atr(self.candles['high'], self.candles['low'], self.candles['close'])
        self.addDataFrameToIndicators(ta.adx(self.candles['high'], self.candles['low'], self.candles['close']))
        self.addDataFrameToIndicators(ta.bbands(self.candles['close']))
        self.addDataFrameToIndicators(ta.macd(self.candles['close']))
        self.addDataFrameToIndicators(ta.stoch(self.candles['high'], self.candles['low'], self.candles['close']))
        for dataFrame in ta.ichimoku(self.candles['high'], self.candles['low'], self.candles['close']):
            self.addDataFrameToIndicators(dataFrame)

    def addDataFrameToIndicators(self, dataFrame):
        for symbol in dataFrame:
            self.indicators[symbol] = dataFrame[symbol]

    def isNewCandle(self):
        #check if there is a new candle
        pass

    def getCurrentPrice(self):
        return CoinApi.getCurrentCoinPrice(self.coin)
