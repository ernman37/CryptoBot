'''
    File: Trader.py
    Creator: Ernest M Duckworth IV
    Created: Monday Feb 28 2022 at 03:35:48 PM
    For: Crypto Bot
    Description: Will access the Market for buying and selling of crypto/paper trading
'''
from CoinApi import CoinApi
import queue, logging

class Trader:
    def __init__(self, accountConfig):
        self.log = logging.getLogger()
        self.log.error("Setting up Trader")
        self.accountConfig = accountConfig
        self.market = CoinApi.getMarket()
        self.tradeQueue = queue.Queue()

    def tradeForever(self):
        while True:
            while not self.tradeQueue.empty():
                newTrade = self.tradeQueue.get()
                self.executeTrade(newTrade)

    def executeTrade(self, newTrade):
        pass
