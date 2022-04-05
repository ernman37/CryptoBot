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
    candleTypes = [
        'time',
        'open',
        'high',
        'low',
        'close',
        'volume'
    ]

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
        self.indicators = pd.DataFrame()
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

    def addNewCandle(self):
        #Check to make sure data has the most recent candle
        newCandle = CoinApi.getLatestClosedCandle(self.coin)
        newMin = int(newCandle["time"] / 60000)
        timeDif = newMin - self.getLastCandleTime()
        if timeDif > 1:
            newCandles = CoinApi.getCandles(self.coin, timeDif)
            self.addCandles(newCandles)
        elif timeDif == 1:
            self.addCandle(newCandle)
        else: # timeDif == 0
            return False
        self.updateIndicators()
        return True

    def getLastCandleTime(self):
        return int(self.candles["time"].iloc[-1] / 60000)

    def addCandles(self, candles):
        for candle in candles:
            self.addCandle(candle)

    def addCandle(self, candle):
        self.candles = self.candles.append(candle, ignore_index=True)
    
    def getCurrentPrice(self):
        return CoinApi.getCurrentCoinPrice(self.coin)
