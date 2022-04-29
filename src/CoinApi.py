'''
    File: CoinApi.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:34:31 PM
    For: Crypto Bot
    Description: Access the markets API to pull specifc coin data down
'''
import ccxt
import pandas as pd
import logging

class CoinApi:
    log = logging.getLogger()
    market = ccxt.binanceus() 
    candleTypes = [
        'time',
        'open',
        'high',
        'low',
        'close',
        'volume'
    ]
    candleTimes = [
        '1m',
        '5m',
        '15m',
        '30m',
        '1h'
    ]
    timeFrame = '1m'

    @staticmethod
    def getAllUSDTradeables():
        fetched = False
        failCount = 0
        allTickers = None
        while not fetched:
            try:
                allTickers = CoinApi.market.fetch_markets()
                fetched = True
            except Exception as E:
                failCount = failCount + 1
                CoinApi.log.error("Could not Fetch all USD coins fail #" + str(failCount))
        usdTickers = list()
        for ticker in allTickers:
            if "/USD" in ticker['symbol'] and not "/USDT" in ticker['symbol'] and not '/USDC' in ticker['symbol'] and not '/BUSD' in ticker['symbol'] and not 'XRP' in ticker['symbol']:
                usdTickers.append(ticker['id'])
        return usdTickers

    @staticmethod
    def setTimeFrame(newTimeFrame):
        if not newTimeFrame in CoinApi.candleTimes:
            return False
        CoinApi.timeFrame = newTimeFrame
        return True

    @staticmethod
    def getLatestClosedCandles(ticker, size=1):
        candles = list()
        for i in range(size):
            newData = CoinApi.fetchRawCandles(ticker, size)[i]
            newCandle = CoinApi.asCandleSeries(newData)
            candles.append(newCandle)
        return candles if size > 1 else candles[0]

    @staticmethod
    def getCandles(ticker, limit=100):
        newData = CoinApi.fetchRawCandles(ticker, limit)
        return CoinApi.asDataFrame(newData)

    @staticmethod
    def fetchRawCandles(ticker, limit):
        fetched = False
        failCount = 0
        candles = None
        while not fetched:
            try:
                candles = CoinApi.market.fetch_ohlcv(ticker, timeframe=CoinApi.timeFrame, limit=limit)
                fetched = True
            except Exception as E:
                failCount = failCount + 1
                CoinApi.log.error("Failed To fetch candles for coin " + ticker + " fail #" + str(failCount))
        return candles

    @staticmethod
    def asDataFrame(candles):
        candles = pd.DataFrame(candles, columns=CoinApi.candleTypes)
        return candles

    @staticmethod
    def asCandleSeries(candle):
        return pd.Series(candle, index=CoinApi.candleTypes)

    @staticmethod
    def getCurrentCoinPrice(ticker):
        fetched = False
        failCount = 0
        orderbook = None
        while not fetched:
            try:
                orderbook = CoinApi.market.fetch_order_book(ticker)
                fetched = True
            except Exception as E:
                failCount = failCount + 1
                CoinApi.log.error("Failed to fetch current coin price, failure #" + str(failCount))
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        price = ((ask + bid) / 2) if (bid and ask) else None
        return price

    @staticmethod
    def getMarket():
        return CoinApi.market
