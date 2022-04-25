'''
    File: Trader.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:48 PM
    For: Crypto Bot
    Description: Will access the Market for buying and selling of crypto/paper trading
'''
from CoinApi import CoinApi
import queue, logging
import ccxt
import time

class Trader:
    def __init__(self, apiKey, secretKey):
        self.log = logging.getLogger()
        self.log.error("Setting up Trader")
        try:
            account = Trader.buildAccountConfig(apiKey, secretKey)
            self.market = ccxt.binanceus(account)
            self.tradeQueue = queue.Queue()
            self.lastUpdate = time.time()
            self.balances = self.updateBalances(True)
        except ccxt.AuthenticationError as e:
            self.log.error(e)
            exit(1)

    @staticmethod
    def buildAccountConfig(apiKey, secretKey):
        return {
            "apiKey": apiKey,
            "secret": secretKey
        }

    def tradeForever(self):
        self.log.error("Trading Forever")
        while True:
            while not self.tradeQueue.empty():
                newTrade = self.tradeQueue.get()
                self.executeTrade(newTrade)
            time.sleep(1)

    def executeTrade(self, newTrade):
        tradeType = newTrade['type']
        if not tradeType in ['buy', 'sell']:
            self.log.error("Cannot create trade of type: " + str(tradeType) + " needs to be \'buy\' or \'sell\'")
            return False
        coin = newTrade['coin'].replace('USD', '')
        if not coin in self.balances:
            self.log.error("Cannot create trade for coin: " + str(coin) + " coin not in BinanceUs")
            return False
        weight = newTrade['weight']
        if weight < .75:
            self.log.error("Will not Create Trade for Weight under .75, weight: " + str(weight))
            return False
        self.log.error("Creating \'" + tradeType + "\' order for coin \'" + coin + "\' with weight: " + str(weight))
        if tradeType == 'buy':
            return self.executeBuy(weight, coin)
        else:
            return self.executeSell(weight, coin)

    def executeBuy(self, weight, coin):
        if self.getFreeUSDBalance() < 10.00:
            self.log.error("Cannot Create Buy for \'" + coin + "\' there is no money available!")
            return False
        cashAmount = self.determineBuyWeight(weight)
        coinAmount = self.determineCoinAmount(coin, cashAmount)
        if not coinAmount:
            return False
        coinSymbol = self.getCoinSymbol(coin)
        try:
            self.market.create_market_buy_order(coinSymbol, coinAmount)
        except Exception as e:
            self.log.error(e)
            return False
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
        if currentPrice * amountToSell < 10.50:
            self.log.error("Cant make \'sell\' order for \'" + coin + "\' balance is: " + str(self.getFreeCoinBalance(coin)))
            return False
        symbol = self.getCoinSymbol(coin)
        try:
            self.market.create_market_sell_order(symbol, amountToSell)
        except Exception as e:
            self.log.error(e)
            return False
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
    
    def updateBalances(self, forceUpdate=False):
        if time.time() - self.lastUpdate > 60 or forceUpdate:
            self.balances = self.market.fetch_balance()
            self.lastUpdate = time.time()
        return self.balances
