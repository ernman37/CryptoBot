<!--
    File: Trader.md
    Creator: Ernest M Duckworth IV
    Created: Tuesday Apr 19 2022 at 12:42:20 AM
    For: CryptoBot
    Description: This is the Design and Documentation file for Trader
--->
# Trader

### Members

- log: <logger>
- market: <ccxt.binanceus()>
- tradeQueue: <queue>
- lastUpdate: <timeStamp>
- balances: <ccxt.fetch_balance()>

#### Libraries

- ccxt
- time
- queue
- logging

#### Models

- CoinAPI

### Methods

#### Main Methods

- Constructor(accountConfig)
  - accountConfig: { apiKey: <apiKey>, secret: <secretKey>}
  - sets market with accountConfig using `ccxt.binanceus(acountConfig)`
  - creates trade queue to be shared with analyzer
  - on successful account link fetches all balances in account

- tradeForever()
  - waits until Analyzer has placed an order in the tradeQueue
  - on queue.get() calls `Trader.executeTrade(newTrade)`

#### Trade Methods
- executeTrade()
  - type checks the new trade to ensure that values passed are valid
  - determines `newTrade.type` and attempts to create buy or sell order

##### Buy Methods

- executeBuy(weight, coin)
  - If there is free USD in account and it is greater than 10 dollars then create order for coin
  - Gets amount from `Trader.determineBuyWeight(weight)`
  - Gets USD -> coin, conversion from `Trader.determineCoinAmount(coin, cashAmount)`
  - Buys coinAmount of coin
  - returns <boolean> representing success

- determineBuyWeight(coin, weight)
  - determines how much cash to use from account while still upholding minimum purchase amount for the next trade
  - Must be over 10 dollars on trade and must be over 10 dollars left in account after trade
  - returns <float> representing how much cash to spend on buy

- determineCoinAmount(coin, cashAmount)
  - Converts <cashAmount> to <coinAmount>
  - returns coin amount of cashAmount

- getCoinSymbol(coin)
  - returns market symbol of coin
    - "{coin}/USD"

##### Sell Methods

- executeSell(weight, coin)
  - determines if there is enough coin to sell, coinCashAmount > 10
  - determines amount to sell from the weight 
  - creates `ccxt.create_market_sell(coin, amount)`
  - returns success of sell order

- determineSellAmount(weight, coin)
  - determines how much to sell of coin based on how much is owned and how much will be left over after intial sell
  - amount owned must be greater than $10 and amount left has to be greater than $10, otherwise we just sell all
  - returns coinAmount to sell


#### Getter Methods
- getPriceOfCoin(coin)
  - returns the current **USD** price of Coin

- getAllBalances()
  - returns the entire `ccxt.fetch_balance()` 
  - Includes entire list of free, used, total for all coins and USD

- getAllCoinBalances(coin)
  - returns the all balances of coin

- getFreeBalances()
  - returns list of every free tradable asset and their corresponding amount

- getFreeCoinBalance(coin)
  - returns amount of coin that is currently tradeable

- getFreeUSDBalance()
  - returns amount of tradable USD

- getUsedBalances()
  - returns list of every used traded asset and their corresponding amount

- getUsedCoinBalance(coin)
  - returns amount of used coin

- getUsedUSDBalance()
  - returns amount of used USD

- getTotalBalances()
  - returns amount of all tradeable assets and the sum of their free and used amounts 

- getTotalCoinBalance()
  - returns total amount of coin (sum of free and used)

- getTotalUSDBalance()
  - returns total amount of USD

- updateBalances()
  - Updates the `Trader.balances` so that we have correct account information
  - sets the new `Trader.lastUpdated` time
  - returns the new balances object

#### Trader.tradeQueue objects

- The Queue will have either a Buy or a Sell order, their objects need to be created specifically so that the Trader can correctly parse information and create successful order

Buy:
```{
    type: "buy",
    weight: range(.75,1),
    coin: ticker
}```

Sell:
```{
    type: "sell",
    weight: range(.75,1),
    coin: ticker
}```
