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
    market = ccxt.coinbase() 
    timeFrame = '1m'
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

    @staticmethod
    def setMarket(newMarket):
        #Possibly switch markets
        pass

    @staticmethod
    def setTimeFrame(newTimeFrame):
        #Check Time frames
        #Assign if valid
        pass

    @staticmethod
    async def getLatestUnclosedCandle(ticker):
        newData = await CoinApi.getCandles(ticker, 1)[0]
        return CoinApi.asCandleSeries(newData)

    @staticmethod
    async def getLatestClosedCandle(ticker):
        newData = await CoinApi.getCandles(ticker, 2)[1]
        return CoinApi.asCandleSeries(newData)

    @staticmethod
    async def getCandles(ticker, limit=100):
        newData = await CoinApi.market.fetch_ohlcv(ticker, timeframe=CoinApi.timeFrame, limit=limit)
        return CoinApi.asCandleSeries(newData)

    @staticmethod
    def asCandleSeries(candle):
        return pd.Series(candle, index=CoinApi.candleTypes)

    @staticmethod
    async def getCurrentCoinPrice(ticker):
        orderbook = await CoinApi.market.fetch_order_book(ticker)
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        price = ((ask + bid) / 2) if (bid and ask) else None
        return price

    @staticmethod
    def getMarket():
        return CoinApi.market