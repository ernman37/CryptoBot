<!--
    File: CoinApi.md
    Creator: Ernest M Duckworth IV
    Created: Tuesday Apr 19 2022 at 01:05:46 PM
    For: CryptoBot
    Description: Design doc for CoinAPI
--->
# CoinAPI

**This is a static class**

### Static Members

- market: <ccxt.binanceus()>
- candleTypes: <list(tohlcv)>
  - `['time', 'open', 'high', 'low', 'close', 'volume']`
- candleTimes: <list(candleTimes)>
- timeFrame: <candleTime>

### Static Methods

- getAllUSDTradables()
  - returns a list of all USD tradable coins

- setTimeFrame(newTimeFrame)
  - sets new timeFrame if its valid

- getLatestClosedCandles(ticker, size=1)
  - returns a list of `pandas.series` candles of length size

- getCandles(ticker, limit=100)
  - returns a `pandas.DataFrame` of candles for ticker given

- fetchRawCandles(ticker, limit)
   - returns raw data from `ccxt.ohlvc(ticker, timeFrame=CoinAPI.timeFrame, limit=limit)`

- asDataFrame(candles)
   - candles: rawCandles 
   - returns candles as `pandas.DataFrame`

- asCandleSeries(candle)
   - candle: rawCandle
   - returns candle as `pandas.Series`

- getCurrentCoinPrice(ticker)
  - returns current price of the coin for ticker in USD

- getMarket()
  