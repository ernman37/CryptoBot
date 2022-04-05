'''
    File: CoinApi.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:34:31 PM
    For: Crypto Bot
    Description: Access the markets API to pull specifc coin data down
'''
import ccxt
import pandas as pd

class CoinApi:
    market = ccxt.binance() 
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
    def setMarket(newMarket):
        #Possibly switch markets
        pass

    @staticmethod
    def setTimeFrame(newTimeFrame):
        if not newTimeFrame in CoinApi.candleTimes:
            return False
        CoinApi.timeFrame = newTimeFrame
        return True

    @staticmethod
    def getLatestClosedCandle(ticker):
        newData = CoinApi.fetchRawCandles(ticker, 1)[0]
        return CoinApi.asCandleSeries(newData)

    @staticmethod
    def getCandles(ticker, limit=100):
        newData = CoinApi.fetchRawCandles(ticker, limit)
        return CoinApi.asDataFrame(newData)

    @staticmethod
    def fetchRawCandles(ticker, limit):
        return CoinApi.market.fetch_ohlcv(ticker, timeframe=CoinApi.timeFrame, limit=limit)

    @staticmethod
    def asDataFrame(candles):
        candles = pd.DataFrame(candles, columns=CoinApi.candleTypes)
        return candles

    @staticmethod
    def asCandleSeries(candle):
        return pd.Series(candle, index=CoinApi.candleTypes)

    @staticmethod
    def getCurrentCoinPrice(ticker):
        orderbook = CoinApi.market.fetch_order_book(ticker)
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        price = ((ask + bid) / 2) if (bid and ask) else None
        return price

    @staticmethod
    def getMarket():
        return CoinApi.market
