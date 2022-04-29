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
from threading import Lock
import logging
import copy

class CoinData:
    log = logging.getLogger
    candleTypes = [
        'time',
        'open',
        'high',
        'low',
        'close',
        'volume'
    ]

    def __init__(self, coinTicker, timeFrame='1m'):
        self.lock = Lock()
        self.coin = coinTicker
        self.timeFrame = timeFrame
        self.candles = pd.DataFrame()
        self.buildCoinData()

    def buildCoinData(self):
        self.lock.acquire()
        try:
            self.candles = CoinApi.getCandles(self.coin)
            self.updateIndicators()
        finally:
            self.lock.release()

    
    def updateIndicators(self):
        self.indicators = pd.DataFrame()
        self.indicators['rsi'] = ta.rsi(self.candles['close'])

        # Indicators to possibly be used in the near future with a more sophisticated trading strategy
        #self.indicators['atr'] = ta.atr(self.candles['high'], self.candles['low'], self.candles['close'])
        #self.indicators['obv'] = ta.obv(self.candles['close'], self.candles['volume'])
        #self.addDataFrameToIndicators(ta.adx(self.candles['high'], self.candles['low'], self.candles['close']))
        #self.addDataFrameToIndicators(ta.bbands(self.candles['close']))
        #self.addDataFrameToIndicators(ta.macd(self.candles['close']))
        #self.addDataFrameToIndicators(ta.stoch(self.candles['high'], self.candles['low'], self.candles['close']))
        #for dataFrame in ta.ichimoku(self.candles['high'], self.candles['low'], self.candles['close']):
        #    self.addDataFrameToIndicators(dataFrame)

    def addDataFrameToIndicators(self, dataFrame):
        for symbol in dataFrame:
            self.indicators[symbol] = dataFrame[symbol]

    def addNewCandle(self):
        self.lock.acquire()
        status = True
        try:
            #Check to make sure data has the most recent candle
            newCandle = CoinApi.getLatestClosedCandles(self.coin)
            newMin = int(newCandle["time"] / 60000)
            timeDif = newMin - self.getLastCandleTime()
            if timeDif > 1:
                newCandles = CoinApi.getLatestClosedCandles(self.coin, timeDif)
                self.addCandles(newCandles)
            elif timeDif == 1:
                self.addCandle(newCandle)
            else: # timeDif == 0
                status = False
        finally:
            self.lock.release()
        return status

    def getLastCandleTime(self):
        return int(self.candles["time"].iloc[-1] / 60000)

    def addCandles(self, candles):
        for candle in candles:
            self.addCandle(candle)

    def addCandle(self, candle):
        self.candles = self.candles.append(candle, ignore_index=True)
        self.updateIndicators()
    
    def getCurrentPrice(self):
        return CoinApi.getCurrentCoinPrice(self.coin)

    def getCandles(self):
        self.lock.acquire()
        try:
            candles = copy.deepcopy(self.candles)
        finally:
            self.lock.release()
        return candles
    
    def getIndicators(self):
        self.lock.acquire()
        try:
            indicators = copy.deepcopy(self.indicators)
        finally:
            self.lock.release()
        return indicators
