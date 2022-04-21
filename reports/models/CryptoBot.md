<!--
    File: CryptoBot.md
    Creator: Ernest M Duckworth IV
    Created: Saturday Apr 16 2022 at 10:24:25 PM
    For: 
    Description:
--->
# CryptoBot

### Members

- Scanner: <Scanner>
- Analyzer: <Analyzer> 
- Trader: <Trader>
- log: <logger>
- coins: <list(coinTicker)>

#### Libraries

- ccxt
- time
- queue
- logging

#### Models

- Scanner
- Analyzer
- Trader

#### Methods

##### Main Methods

- Constructor(coins, accountKeys/Trader, timeFrame="1m")
   - coins: list of Crypto tickers
   - accountKeys/Trader: api keys to initiate ccxt trader or Trader model
   - timeFrame: what minute the candles should be on (must be validated for valid time frame)
- start()
   - starts crypto bot processes
   - Starts `Scanner.scanForever()`
   - Starts `Analyzer.analyzeForever()`
   - Starts `Trader.tradeForever()`
