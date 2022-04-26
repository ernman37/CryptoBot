<!--
    File: Scanner.md
    Creator: Ernest M Duckworth IV
    Created: Tuesday Apr 19 2022 at 01:05:35 PM
    For: CryptoBot
    Description: Design doc for Scanner model
--->
# Scanner

### Members

- log: logger
- tickerList: list(coinTickers)
- queue: queue
- coins: dict(CoinData)
- currentTime = timeStamp

#### Libraries

- time, logging, queue, sys

#### Models

- CoinData

### Methods

#### Main Methods
- constructor(coins, queue, timeFrame='1m')
  - coins: list of coins to trade
  - queue: queue for analyzer
  - timeFrame is the candles that are loaded (default is '1m')
  - builds all `Scanner.coins` which is a dict of CoinData keyed with their corresponding ticker 

- scanForever()
  - Scans list of coins forever
  - Uses Unix timestamp to check if it needs to scan for new coins yet
  - if there is a new coin then call `Scanner.fetchAllNewCandles()`


#### Scanning Methods

- isNewCoin()
  - Uses lastFetchedTimeStamp to compare to currentTimeStamp in order to determine if there is new candles to add
  - returns <Boolean> determining if there is a new Candle

- fetchAllNewCandles()
  - fetches candle(s) for all coins in `Scanner.coins`
  - puts coin ticker in `Scanner.queue` which is shared with Analyzer, upon successful candle fetch

- timeInMinutes():
  - returns current time in minutes for easy testing if x amount of time has passed 

#### Scanner.queue format

- This queue represents is shared between `Scanner` and `Analyzer`
- in this scenario we can think of `Scanner` as the producer and `Analyzer` as the consumer
- `Scanner` puts coin ticker of newly updated `CoinData` in queue
- `Analyzer` then pulls coin and accesses the `CoinData` by its ticker
