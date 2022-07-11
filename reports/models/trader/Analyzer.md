<!--
    File: Analyzer.md
    Creator: Ernest M Duckworth IV
    Created: Tuesday Apr 19 2022 at 01:05:28 PM
    For: CryptoBot
    Description: Analyzer design doc
--->
# Analyzer

### Libraries

- pandas
- queue
- logging

### Models

- CoinData

### Members

- log: <logger>
- coinsData: <list(CoinData)>
- scanQueue: <queue>
- tradeQueue: <queue>

### Methods

#### Main Methods

- constructor(coinsData, scanQueue, tradeQueue)
  - coinsData: <list(CoinData)>
  - scanQueue, tradeQueue: <queue>
  - coinsData is shared with `Scanner`
  - scanQueue is shared with `Scanner`
  - tradeQueue is shared with `Trader`

- analyzeForever()
  - Forever reads tickers from `Analyzer.scanQueue`
  - Begins to analyze fetched coins corresponding data

#### Analyze Methods

- analyzeCoin(coin)
  - analyzes the coin fundamental coin movements
    - the actual candles themselves
  - analyzes the coin indicators using known strategies
    - RSI, ATR, Supertrend, etc...
  - Based on analyzations creates weight from range(-1, 1)
    - negative: sell
    - positive: buy
  - If weight is in correct area then it creates a "buy/sell" order to place into `Analyzer.tradeQueue`

- analyzeIndicators(coin)
  - analyzes the coins indicators
  - returns a weight of what decision should be made

- createBuyorSell(weight, coin)
  - based on the weight it will create a buy, sell or do nothing
  - if buy or sell is created that will be placed into the `Analyzer.tradeQueue` so that `Trader` can execute trade and analyzer can continue to analyze

#### Static Methods

- createSell(weight, coin)
  - creates sell order with weight for coin

- createBuy(weight, coin)
  - creates sell order with weight for coin

- createOrder(weight, coin, type)
  - Creates type order with weight for coin

#### Order Format

```
order = {
    type: "buy" || "sell",
    weight: range(-1, 1)
    coin: coinTicker
}
```