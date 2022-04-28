'''
    File: Trader.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:48 PM
    For: Crypto Bot
    Description: Will access the Market for buying and selling of crypto/paper trading
'''
from CoinApi import CoinApi
import queue, logging, ccxt, time, sys
from threading import Lock

class Trader:
    def __init__(self, apiKey, secretKey, stopLoss=.015):
        self.log = logging.getLogger()
        self.log.error("Setting up Trader")
        self.stopLoss = stopLoss
        self.trading = True
        self.doneTrading = False
        self.lock = Lock()
        try:
            account = Trader.buildAccountConfig(apiKey, secretKey)
            self.market = ccxt.binanceus(account)
            self.tradeQueue = queue.Queue()
            self.lastUpdate = time.time()
            self.balances = self.updateBalances(True)
            self.coinBuys = dict()
            self.buys = 0
            self.sells = 0
            self.successful = 0
            self.failure = 0
            self.successRate = 0
            self.averageReturn = 0
            self.sumOfReturns = 0 
        except ccxt.AuthenticationError as e:
            self.log.error(e)
            self.trading = False
            self.doneTrading = True
            exit(1)

    @staticmethod
    def buildAccountConfig(apiKey, secretKey):
        return {
            "apiKey": apiKey,
            "secret": secretKey
        }

    # Tells us if we can buy more
    # Will always be able to sell the coins that it has to ensure profits/losses
    def setTrading(self, canBuy=True):
        self.lock.acquire()
        try:
            self.trading = canBuy
            if self.trading:
                self.log.error("Set to Buy and Sell")
            else:
                self.log.error("Set to Sell out of positions")
        finally: 
            self.lock.release()
        return self.trading

    def hardExit(self):
        self.lock.acquire()
        try:
            self.doneTrading = True
            self.trading = False
            freeBalances = self.getFreeBalances()
            for coin in freeBalances:
                if coin != "USD" and freeBalances[coin] != 0 and freeBalances[coin] * self.getPriceOfCoin(coin) > 10.50:
                    self.executeSell(1, coin)
        except Exception as E:
            self.log.error(E)
        finally: 
            self.lock.release()
        return True

    def tradeForever(self):
        self.log.error("Trading Forever")
        while not self.doneTrading:
            while not self.tradeQueue.empty() and not self.doneTrading:
                newTrade = self.tradeQueue.get()
                self.acquireLockAndTrade(newTrade)
            time.sleep(1)
        sys.exit(0)

    def acquireLockAndTrade(self, newTrade):
        self.lock.acquire()
        tradeStatus = False
        try:
            tradeStatus = self.executeTrade(newTrade)
            if self.checkForExit():
                self.log.error("Trader has finished all trades shutting down")
                self.doneTrading = True
        except Exception as E:
            self.log.error(E)
        finally:
            self.lock.release()
        return tradeStatus
    
    def checkForExit(self):
        if self.trading:
            return False
        freeBalances = self.getFreeBalances()
        done = True
        for coin in freeBalances:
            if coin != "USD" and freeBalances[coin] != 0 and freeBalances[coin] * self.getPriceOfCoin(coin) > 10.10:
                self.log.error("Cannot Shut down Trader yet waiting for exit on coin \'" + coin + "\'")
                done = False
        return done

    def executeTrade(self, newTrade):
        if not self.checkTrade(newTrade):
            return False
        tradeType = newTrade['type']
        coin = newTrade['coin'].replace('USD', '')
        weight = newTrade['weight']
        self.log.error("Creating \'" + tradeType + "\' order for coin \'" + coin + "\' with weight: " + str(weight))
        if tradeType == 'buy':
            if self.trading:
                return self.executeBuy(weight, coin)
            else:
                self.log.error("Set to Shut Down will not buy in any more positions for coin \'" + coin + "\'")
                return False
        elif tradeType == 'sell':
            return self.executeSell(weight, coin)
            
    def checkTrade(self, newTrade):
        tradeType = newTrade['type']
        if not tradeType in ['buy', 'sell', 'wait']:
            self.log.error("Cannot create trade of type: " + str(tradeType) + " needs to be \'buy\' or \'sell\'")
            return False
        coin = newTrade['coin'].replace('USD', '')
        if not coin in self.balances:
            self.log.error("Cannot create trade for coin: " + str(coin) + " coin not in BinanceUs")
            return False
        if not coin in self.coinBuys:
            self.coinBuys[coin] = 0
        if self.hitStopLoss(coin):
            self.executeSell(1, coin)
            self.log.error("Coin: " + coin + " has hit its stop loss exiting position")
            return False
        if tradeType == 'wait':
            self.log.error("Waiting on Coin \'" + coin + "\' to enter buy/sell entry point")
            return False
        weight = newTrade['weight']
        if weight < .75:
            self.log.error("Will not Create Trade for Weight under .75, weight: " + str(weight))
            return False
        return True

    def hitStopLoss(self, coin):
        coinPrice = self.getPriceOfCoin(coin)
        coinBalance = self.getFreeCoinBalance(coin)
        coinUSD = coinPrice * coinBalance
        if coinUSD < 11:
            return False
        lastBuy = self.coinBuys[coin]
        if lastBuy == 0:
            return False
        if coinUSD / lastBuy > (1 - self.stopLoss):
            return False
        return True

    def executeBuy(self, weight, coin):
        if self.getFreeUSDBalance() < 10.00:
            self.log.error("Cannot Create Buy for \'" + coin + "\' there is no money available!")
            return False
        cashAmount = self.determineBuyWeight(weight)
        coinAmount = self.determineCoinAmount(coin, cashAmount)
        if not coinAmount:
            return False
        coinSymbol = self.getCoinSymbol(coin)
        startUSD = self.getFreeUSDBalance()
        try:
            self.market.create_market_buy_order(coinSymbol, coinAmount)
            self.buys = self.buys + 1
            self.updateBalances(True)
        except Exception as e:
            self.log.error(e)
            return False
        endUSD = self.getFreeUSDBalance()
        self.coinBuys[coin] = self.coinBuys[coin] + startUSD - endUSD
        self.log.error("Created \'buy\' order for coin \'" + coin + "\' for $" + str(cashAmount))
        return True

    def determineBuyWeight(self, weight):
        self.updateBalances(True)
        freeCash = self.getFreeUSDBalance()
        buyAmount = (freeCash / 3.00) * weight
        if buyAmount < 12.00:
            buyAmount = 12.00
        if freeCash - buyAmount < 10.00:
            buyAmount = freeCash - .10
        return buyAmount

    def determineCoinAmount(self, coin, cashAmount):
        coinPrice = self.getPriceOfCoin(coin)
        if not coinPrice:
            return False
        coinAmount = cashAmount / coinPrice
        return coinAmount

    def getCoinSymbol(self, coin):
        return coin.replace("USD", "") + "/USD"

    def executeSell(self, weight, coin):
        amountToSell = self.determineSellAmount(weight, coin)
        currentPrice = self.getPriceOfCoin(coin)
        soldAmount = amountToSell * currentPrice
        if currentPrice * amountToSell < 10.00:
            self.log.error("Cant make \'sell\' order for \'" + coin + "\' balance is: " + str(self.getFreeCoinBalance(coin)))
            return False
        symbol = self.getCoinSymbol(coin)
        try:
            self.market.create_market_sell_order(symbol, amountToSell)
            self.sells = self.sells + 1
            self.updateBalances(True)
        except Exception as e:
            self.log.error(e)
            return False
        self.log.error("Created \'sell\' order for coin \'" + coin + "\' for $" + str(soldAmount))
        self.determineSuccess(coin, soldAmount)
        self.coinBuys[coin] = 0
        return True

    def determineSellAmount(self, weight, coin):
        amountOwned = self.getFreeCoinBalance(coin)
        currentPrice = self.getPriceOfCoin(coin)
        amountToSell = amountOwned * weight
        amountLeft = amountOwned - amountToSell
        if amountLeft * currentPrice < 11.00:
            amountToSell = amountOwned
        return amountToSell

    def getPriceOfCoin(self, coin):
        entireMarket = self.market.fetch_markets()
        found = False
        if not "USD" in coin:
            coin = coin + "USD"
        for exchange in entireMarket:
            if coin == exchange['id']:
                found = True
        if not found:
            self.log.error("No Valid USD conversion for \'" + coin + "\'")
            return False
        return CoinApi.getCurrentCoinPrice(coin)

    def determineSuccess(self, coin, soldAmount):
        if self.coinBuys[coin] == 0:
            self.sells = self.sells - 1 
            return False #Buy log was not recorded during this session therefore we cannot calculate success rate
        if self.coinBuys[coin] > soldAmount:
            self.log.error("Trade for " + coin + " was a negative return")
            self.failure = self.failure + 1
        else:
            self.log.error("Trade for " + coin + " was a positive return")
            self.successful = self.successful + 1
        self.successRate = (self.successful / self.sells) * 100
        returnPercentage = soldAmount / self.coinBuys[coin]
        if returnPercentage < 1:
            returnPercentage = -(1 - returnPercentage)
        else:
            returnPercentage = returnPercentage - 1
        self.sumOfReturns = self.sumOfReturns + returnPercentage
        self.averageReturn = (self.sumOfReturns / self.sells) * 100
        self.log.error("New SuccessRate: " + str(self.successRate) + ", Average Return: " + str(self.averageReturn) + "%")

    def getAllBalances(self):
        return self.updateBalances()
    
    def getAllCoinBalances(self, coin):
        self.updateBalances()
        if not coin in self.balances:
            self.log.error("Coin:" + str(coin) + "not in balances")
            return False
        return self.balances[coin]

    def getFreeBalances(self):
        self.updateBalances()
        return self.balances['free']

    def getFreeCoinBalance(self, coin):
        return self.getAllCoinBalances(coin)['free']
    
    def getFreeUSDBalance(self):
        return self.getAllCoinBalances('USD')['free']

    def getUsedBalances(self):
        self.updateBalances()
        return self.balances['used']

    def getUsedCoinBalance(self, coin):
        return self.getAllCoinBalances(coin)['used']
    
    def getUsedUSDBalance(self):
        return self.getAllCoinBalances('USD')['used']

    def getTotalBalances(self):
        self.updateBalances()
        return self.balances['total']

    def getTotalCoinBalance(self, coin):
        return self.getAllCoinBalances(coin)['total']

    def getTotalUSDBalance(self):
        return self.getAllCoinBalances('USD')['total']

    def getPortfolioUSDBalance(self):
        totals = self.getTotalBalances()
        totalUSD = totals["USD"]
        for coin in totals:
            if not totals[coin] == 0 and not coin == 'USD':
                totalUSD = totalUSD + (self.getPriceOfCoin(coin) * totals[coin])
        return totalUSD

    def updateBalances(self, forceUpdate = False):
        if time.time() - self.lastUpdate > 60 or forceUpdate:
            self.balances = self.market.fetch_balance()
            self.lastUpdate = time.time()
        return self.balances
