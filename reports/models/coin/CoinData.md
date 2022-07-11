<!--
    File: CoinData.md
    Creator: Ernest M Duckworth IV
    Created: Tuesday Apr 19 2022 at 01:06:02 PM
    For: CryptoBot
    Description: Documentation for CoinData
--->
# CoinData

### Libraries

- pandas
- pandas_ta
- threading
- copy

### Models

- CoinApi

### Members

#### Static

- candleTypes: <list(ohlcv)>
  - list of strings [open, high, low, close, volume]

#### Instanced 

- lock: <threading.lock>
- coin: <string>
- timeFrame: <string>
- candles: <pandas.DataFrame>
- indicators: <pandas.DataFrame>

### Methods

- Constructor(coinTicker, timeFrame='1m')
  - Creates all members
  - Loads coinTicker candles from `CoinApi`
  - builds `CoinData.indicators` from candles loaded using pandas_ta

- buildCoinData()
  - helper for Constructor for locking
  - acquires lock updates candles and indicators
  - releases lock

- updateIndicators()
  - updates all of the indicators that we are choosing to analyze 
    - RSI
    - ATR
    - ADX
    - BBANDS
    - MACD
    - STOCH
    - ICHIMOKU

- addDataFrameToIndicators(dataFrame)
   - Adds each row in the DataFrame to indicators

- addNewCandle()
  - Aquires the lock on object
  - adds new candle(s) from `CoinApi`
  - releases lock

- getLastCandleTime()
  - Returns the timestamp from the last loaded candle

- addCandles(candles)
  - candles: <pandas.Series[]>
  - Adds each candles in the candles array to candles

- addCandle(candle)
  - candle: <pandas.Series[]>
  - Adds candle to candles 

- getCurrentPrice()
  - returns the USD price of the coin that CoinData is tied to 

- getCandles()
  - returns `CoinData.candles` deep copy

- getIndicators()
  - returns `CoinData.indicators` deep copy
